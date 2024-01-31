import pymysql
from config import Config


class Database:
    ''' Class for interacting with the database set up to store river level
    information.

    Used a lot of ideas from the excellent blog "Hackers and Slackers
    here: https://hackersandslackers.com/using-pymysql

    '''
    def __init__(self, config: Config) -> None:
        '''

        '''
        # Load in configuration data
        self.host = config.db_host
        self.username = config.db_user
        self.password = config.db_password
        self.port = config.db_port
        self.dbname = config.db_name
        self.conn = None

    def open_connection(self) -> None:
        ''' Manages connection to database '''
        try:
            if self.conn is None:
                self.conn = pymysql.connect(host=self.host,
                                            user=self.username,
                                            passwd=self.password,
                                            database=self.dbname,
                                            connect_timeout=5)

        except (pymysql.MySQLError, pymysql.err.OperationalError):
            print('Unable to connect to database')

    def run_query(self, query: str) -> None:
        ''' Executes SQL query '''
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                if 'SELECT' in query:
                    # Selecting Data
                    records = []

                    cur.execute(query)
                    result = cur.fetchall()
                    for row in result:
                        records.append(row)

                    return records
                else:
                    # Updating data
                    result = cur.execute(query)
                    self.conn.commit()
                    affected = "{0} rows affected.".format(cur.rowcount)
                    return affected

        except pymysql.MySQLError as e:
            print(e)

        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
