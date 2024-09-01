import random
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required
from app import db, limiter
from .models import UserModel
from .schemas import UserSchema, PhoneSchema, ChangePassSchema, UserEditSchema
from blocklist import BLOCKLIST




authApi = Blueprint("Auth", "auth", url_prefix="/api/auth", description="Authentication Endpoints")



@authApi.route("/register")
class UserRegister(MethodView):
    @authApi.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.phone == user_data["phone"]).first():
            abort(409, message="A User with that phone is already exists")
        
        user = UserModel()
        user.name = user_data["name"]
        user.phone = user_data["phone"]
        user.set_password(user_data["password"])
        try:
            db.session.add(user)
            db.session.commit()
            return {"message" : "User Created Successfully"}, 201
        except Exception as ex:
            db.session.rollback()
            return {"message" : f"Error {ex} is happened"}, 400
        
@authApi.route("/login")
class UserLogin(MethodView):
    @authApi.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.phone == user_data["phone"]).first()
        if user and user.check_password(user_data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refrsh_token = create_refresh_token(user.id)
            return {"access_token" : access_token, "refresh_token": refrsh_token}, 200
        
        abort(401, message="Invalid Credentials")

@authApi.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Successfully Logged out"}, 200

@authApi.route('/user/whoami')
class Whoami(MethodView):
    @authApi.response(200, UserSchema)
    @jwt_required(optional=True)
    def get(self):
        # identity = get_jwt_identity()
        current_user = UserModel.query.filter_by(id=get_jwt_identity()).one_or_none()
        # print('current_user : ', current_user)
        return  current_user

@authApi.route("/user/<int:user_id>")
class User(MethodView):
    @authApi.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User is Deleted Successfully"}, 200
        except Exception as ex:
            return {"message": f"Error {ex} is happened"}, 400
        
@authApi.route("/token/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200
        
@authApi.route("/auth-phone")
class AuthPhone(MethodView):
    @authApi.arguments(PhoneSchema)
    @limiter.limit("100/hour") # TODO limited must be changed
    def post(self, user_data):
        user = UserModel.query.filter_by(phone=user_data['phone']).first_or_404()
        if not user:
            abort(409, message="A user with that phone is not exists")
        code = random.randint(100000,999999)
        print(code) # TODO sms must be replaced
        user.code = code
        db.session.commit()
        return {"message": "Verify's Code is Sent To Mobile Number"}, 200

@authApi.route("/reset-password")
class ResetPassword(MethodView):
    @authApi.arguments(ChangePassSchema)
    @limiter.limit("100/hour") # TODO limited must be changed
    def post(self, user_data): # user_data ={phone, new-password, code}
        user = UserModel.query.filter_by(phone=user_data['phone']).first_or_404()
        # print( 'user data : code is -> ', user_data["code"])
        if not user:
            abort(409, message="A user with that phone is not exists")
        if (user.code != user_data["code"]):
            abort(409, message='The Code is Not Correct !!')
        user.set_password(user_data["password"])
        user.code = ""
        db.session.commit()
        return {"message": "User Password is Updated Successfully"}, 200
        
@authApi.route("/user/edit") #TODO /user/edit/<int:id>
class UserEdit(MethodView):
    @authApi.arguments(UserEditSchema)
    @authApi.response(200, UserSchema)
    @jwt_required()
    def put(self, user_data):
        current_user = UserModel.query.filter_by(id=get_jwt_identity()).one_or_none()
        current_user.name = user_data["name"] 
        current_user.username = user_data["username"] 
        current_user.email = user_data["email"] 
        try:
            db.session.commit()
            return current_user
        except Exception:
            db.session.rollback()
            return {"message": "User is not Updated"}, 400
