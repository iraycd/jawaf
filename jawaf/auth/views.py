import os
from mako.template import Template
from sanic.response import json, text
from sanic.views import HTTPMethodView
from jawaf.auth.decorators import login_required
from jawaf.auth.users import check_user, check_user_reset_access, decode_user_id, encode_user_id, \
    generate_reset_split_token, log_in, log_out, update_user
from jawaf.conf import settings

class LoginView(HTTPMethodView):
    """Endpoint to handle user login."""
    
    async def post(self, request):
        username = request.form.get('username', '')
        password = request.form.get('password', None)
        next_url = request.form.get('next', None)
        if password is None:
            return json({'message': 'no password'}, status=403)
        user_row = await check_user(username, password)
        if user_row:
            await log_in(request, user_row)
            return json({'message': 'login succeeded', 'next': next, 'username': username}, status=200)
        return json({'message': 'login failed'}, status=403)

class LogoutView(HTTPMethodView):
    """Endpoint to handle user logout."""

    async def post(self, request):
        user_row = request['session'].get('user', None)
        if user_row:
            await log_out(request)
            return json({'message': 'logout succeeded'}, status=200)
        return json({'message': 'not logged in'}, status=401)

class PasswordChangeView(HTTPMethodView):
    """Endpoint to handle user password change."""

    async def post(self, request):
        username = request.form.get('username', '')
        old_password = request.form.get('old_password', None)
        new_password = request.form.get('new_password', None)
        user_row = await check_user(username, old_password)
        if not user_row:
            return json({'message': 'bad user data'}, status=403)
        if user_row.id != request['session']['user'].id:
            return json({'message': 'bad user data'}, status=403)
            if new_password is None:
                return json({'message': 'no password'}, status=403)
        await update_user(database=None, target_username=username, password=new_password)
        return json({'message': 'password changed'}, status=200)

class PasswordResetView(HTTPMethodView):
    """Endpoint to handle user password reset."""

    async def post(self, request, user_id, token):
        user_id = decode_user_id(user_id)
        username = request.form.get('username', None)
        new_password = request.form.get('new_password', None)
        verified = await check_user_reset_access(username, user_id, token, database=None)
        if verified:            
            if new_password is None or username is None:
                return json({'message': 'bad user data'}, status=403)
            await update_user(database=None, target_user_id=user_id, password=new_password)
            return json({'message': 'accepted'}, status=200)
        return json({'message': 'unauthorized'}, status=403)
