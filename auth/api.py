import flask

def api(app: flask.Flask):
    @app.route("/api/v1/")
    def index():
        raise NotImplementedError()

    @app.route("/api/v1/oauth", methods=["GET"])
    def oauth_get():
        raise NotImplementedError()

    @app.route("/api/v1/oauth", methods=["POST"])
    def oauth_post():
        raise NotImplementedError()

    @app.route("/api/v1/manage/user/<email>")
    def user_get(email):
        raise NotImplementedError()

    @app.route("/api/v1/manage/user", methods=["POST"])
    def create_user():
        raise NotImplementedError

    @app.route("/api/v1/manage/user/<email>", methods=["POST"])
    def update_user(email):
        raise NotImplementedError()

    @app.route("/api/v1/manage/user/<email>", methods=["DELETE"])
    def update_user(email):
        raise NotImplementedError()