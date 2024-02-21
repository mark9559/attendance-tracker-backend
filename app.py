from flask import Flask, request, jsonify
from flask_restful import Api
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_cors import CORS
from models import db, TokenBlocklist
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from views import *

load_dotenv()
import os

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt()
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager()
jwt.init_app(app)
db.init_app(app)
Migrate(app,db)


ADMIN_ROLE_ID = 1
TEACHER_ROLE_ID = 2
STUDENT_ROLE_ID = 3

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None

api.add_resource(Login,'/login')
api.add_resource(AuthenticatedUser, '/authenticated_user')
api.add_resource(Logout, '/logout')
api.add_resource(AddTeacher,'/addteacher')
api.add_resource(AddStudent,'/addstudent')

if __name__=='__main__':
    app.run(debug=True,port=5000)