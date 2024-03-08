import os
from dotenv import load_dotenv
import secrets

# Carrega as variáveis de ambiente de um arquivo .env
load_dotenv()

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = "1.0"
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET_KEY = secrets.token_hex(16)
JWT_CONFIG = {
    "JWT_SECRET_KEY": secrets.token_hex(16),
    "EXP_TIME_MIN": int(os.getenv("EXP_TIME_MIN", 45)),
    "REFRESH_TIME_MIN": int(os.getenv("REFRESH_TIME_MIN", 15))
}
