from dotenv import dotenv_values
secret = dotenv_values("blockchain-tips/.env")["DB_SECRET_KEY"]

config = dict(
    DEBUG=False,
    SECRET_KEY=secret,
    PONY={
        'provider': 'sqlite',
        'filename': 'db.db3',
        'create_db': True
    }
)
