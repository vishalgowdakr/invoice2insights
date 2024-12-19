from flask_login import login_user
from flask import redirect, request, flash
from flask_appbuilder.security.manager import AUTH_REMOTE_USER
from flask_appbuilder.security.manager import BaseSecurityManager
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.views import expose

SECRET_KEY = 'd+zT49TdTrEIcFn4e0ZsbQPClmKiXwpGJKOg/So8bfhMKeWJgc3z8r+F'

FEATURE_FLAGS = {
    # Paste this along with other feature flag options
    "EMBEDDED_SUPERSET": True,
}


# Create a custom view to authenticate the user
AuthRemoteUserView = BaseSecurityManager.authremoteuserview


class CustomAuthUserView(AuthRemoteUserView):
    @expose('/login/')
    def login(self):
        token = request.args.get('token')
        next = request.args.get('next')
        sm = self.appbuilder.sm
        session = sm.get_session
        user = session.query(sm.user_model).filter_by(
            username='superuser').first()
        if token == '1234abcd456':
            login_user(user, remember=False, force=True)
            if (next is not None):
                return redirect(next)
            else:
                return redirect(self.appbuilder.get_url_for_index)
        else:
            flash('Unable to auto login', 'warning')
            return super(CustomAuthUserView, self).login()

# Create a custom Security manager that overrides the CustomAuthUserView


class CustomSecurityManager(SupersetSecurityManager):
    authremoteuserview = CustomAuthUserView


# Use our custom authenticator
CUSTOM_SECURITY_MANAGER = CustomSecurityManager

# User remote authentication
AUTH_TYPE = AUTH_REMOTE_USER

TALISMAN_ENABLED = False
ENABLE_CORS = True
HTTP_HEADERS = {"X-Frame-Options": "ALLOWALL"}

print("Config file loaded successfully!")
print("SECRET_KEY:", SECRET_KEY)
