from flaskeddit.auth import auth_bp


@auth_bp.route("/register")
def register():
    return "Register"


@auth_bp.route("/login")
def login():
    return "Login"


@auth_bp.route("/logout")
def logout():
    return "Logout"
