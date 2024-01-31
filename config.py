from os import environ


class Config:
    # Database config
    db_user: str = environ.get('DATABASE_USERNAME')
    db_password: str = environ.get('DATABASE_PASSWORD')
    db_host: str = environ.get('DATABASE_HOST')
    db_port: int = int(environ.get('DATABASE_PORT'))
    db_name: str = environ.get('DATABASE_NAME')

    def __repr__(self) -> str:
        # Defines representation of object
        m = f'Connected to {self.db_name} at {self.db_host}:{self.db_port}'
        return m
