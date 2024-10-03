from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
PHONENUMBER_DIGIKALA = os.getenv('PHONENUMBER')
PASSWORD_DIGIKALA = os.getenv('PASSWORD')
DB_USERNAME = os.getenv('USERNAME_DB')
DB_PASSWORD = os.getenv('PASSWORD_DB')
DB_NAME = os.getenv('DB_NAME')