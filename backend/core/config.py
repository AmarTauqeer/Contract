from dotenv import load_dotenv
import os
import redis
import subprocess
load_dotenv()


class ApplicationConfig:
    SECRET_KEY = "amar tauqeer"#os.environ["SECRET_KEY"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"

    # # print(os.system("ping localhost:6389"))
    SESSION_TYPE="filesystem"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True


