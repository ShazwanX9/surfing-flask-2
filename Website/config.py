from dotenv import load_dotenv
from os import getenv

##############################

# Set Path to .env file
folder_path = "./Website"
env_path = folder_path + "/.env"
load_dotenv(dotenv_path=env_path)

class Config:
    """Set Flask configuration variables from .env file"""

    # Load environment variables
    TESTING = getenv("TESTING")
    FLASK_DEBUG = getenv("FLASK_DEBUG")
    SECRET_KEY = getenv("SECRET_KEY")
    SERVER = getenv("SERVER")
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")

class ConstData:
    """Set CONSTANTS variables from .env file"""

    # Load environment variables
    DB_NAME  = getenv("db_name")
    DB_KEY   = getenv("db_key")
    CONFIG_FILEPATH = getenv("conf_path")
    MY_NAME = getenv("my_name")
    MY_EMAIL = getenv("my_email")
    MY_PHONE = getenv("my_phone")
    
    
