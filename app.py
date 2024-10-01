from flask import Flask
from secrets import token_hex
from routes import *
from config import HOST, PORT
import asyncio

app = Flask(__name__)
app.secret_key = token_hex(16)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
