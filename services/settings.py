import secrets

APP_NAME = config("APP_NAME")
APP_VERSION = "3.1.2"
SECRET_KEY = config("SECRET_KEY")
JWT_SECRET_KEY = secrets.token_hex(16)
JWT_CONFIG = {
    "JWT_SECRET_KEY": secrets.token_hex(16),
    "EXP_TIME_MIN": int(config("EXP_TIME_MIN", 45)),
    "REFRESH_TIME_MIN": int(config("REFRESH_TIME_MIN", 15))
}
