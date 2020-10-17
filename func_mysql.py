import pymysql.cursors


class mysql:
    def __init__(self, DB_HOST, DB_PORT, DB_USER, DB_PW, DB_NAME):
        self.DB_INFO = [DB_HOST, int(DB_PORT), DB_USER, DB_PW, DB_NAME]

    def sql_conn(self):
        self.conn = pymysql.connect(
            host=self.DB_INFO[0],
            port=self.DB_INFO[1],
            user=self.DB_INFO[2],
            password=self.DB_INFO[3],
            db=self.DB_INFO[4],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def sql_exec(self):
        try:
            with self.conn.cursor() as cursor:
                # Create a new record
                cursor.execute(self.sql)
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.conn.commit()
        finally:
            self.conn.close()
        return

    def sql_insert(self, sql_dict, TBL_NAME):

        self.sql_conn()

        sql_key = ""
        sql_val = ""
        for x in sql_dict.keys():
            sql_key += '{0}, '.format(x)
            sql_val += "'{0}',".format(sql_dict[x])
        # print(sql_key)
        sql_key = sql_key[:-2]
        sql_val = sql_val[:-1].replace(" ", "")
        self.sql = 'INSERT INTO `{0}` ({1}) VALUES ({2})'.format(
            TBL_NAME, sql_key, sql_val)

        self.sql_exec()

    def mult_insert(self, sql_statement, TBL_NAME):

        self.sql_conn()

        self.sql = sql_statement

        self.sql_exec()
