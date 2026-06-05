import os


DB_CONFIG = {
    "host": os.getenv("QUICKHELP_DB_HOST", "localhost"),
    "port": int(os.getenv("QUICKHELP_DB_PORT", "3306")),
    "user": os.getenv("QUICKHELP_DB_USER", "root"),
    "password": os.getenv("QUICKHELP_DB_PASSWORD", "YOUR_MYSQL_PASSWORD"),
    "database": os.getenv("QUICKHELP_DB_NAME", "quickhelp"),
}

ADMIN_EMAIL = os.getenv("QUICKHELP_ADMIN_EMAIL", "admin@quickhelp.demo")
ADMIN_PASSWORD = os.getenv("QUICKHELP_ADMIN_PASSWORD", "CHANGE_ME")
