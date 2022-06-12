from functools import wraps
from flask import redirect, url_for, flash
from serwago.models import DBConnection
from flask_login import current_user



db = DBConnection()

def admin_required(func):
    """
    Modified login_required decorator to restrict access to admin group.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user and current_user.role_id!=2:        # zero means admin, one and up are other groups
            flash("You don't have permission to access this resource.", "warning")
            return redirect(url_for("welcome_page"))
        return func(*args, **kwargs)
    return decorated_view
