from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
PHONENUMBER_DIGIKALA = os.getenv('PHONENUMBER')
PASSWORD_DIGIKALA = os.getenv('PASSWORD')
USERNAME_DB = os.getenv('USERNAME_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')
DB_NAME = os.getenv('DB_NAME')