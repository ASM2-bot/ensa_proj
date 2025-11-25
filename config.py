class config:
    """configuration de mysql"""
    MYSQL_HOST='localhost'
    MYSQL_USER='root'
    MYSQL_PASSWORD='DG@2005'
    MYSQL_DB='gestion_etudiants'
    MYSQL_PORT=3306

    SECRET_KEY='1101'
    DEBUG=True
    @staticmethod
    def get_db_config():
        return {
            'host':config.MYSQL_HOST,
            'user':config.MYSQL_USER,
            'password':config.MYSQL_PASSWORD,
            'database':config.MYSQL_DB,
            'port':config.MYSQL_PORT
        }