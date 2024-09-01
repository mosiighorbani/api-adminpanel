from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_migrate import Migrate
from config import Developement
from blocklist import BLOCKLIST
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address





app = Flask(__name__)
app.config.from_object(Developement)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# .............................................................................................
api = Api(app)
jwt = JWTManager(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


# with app.app_context():
#     from auth.models import UserModel
#     identity = get_jwt_identity()
#     current_user = UserModel.query.filter_by(id=identity).one_or_none()

# from auth.models import UserModel
# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     return UserModel.query.filter_by(id=identity).one_or_none()

# ............................................. Blueprint Settings .............................................
from auth.resources import authApi


api.register_blueprint(authApi)
# ..............................................................................................................



@app.route('/')
def index():
    return jsonify({
        "app name" : "flask admin panel",
        "developer" : "mosiweb.ir",
        "year" : "1403"
        })



if __name__ == '__main__':
    app.run()