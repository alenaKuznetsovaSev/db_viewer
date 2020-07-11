from sqlalchemy import create_engine


class Saver:
    """сохраняет результаты в SQL"""

    def __del__(self):
        self.conn.close()

    def __init__(self, database):
        engine = create_engine("sqlite:///"+database+".db")
        self.conn = engine.connect()

    def get_tables(self):
        _SQL = "SELECT name FROM sqlite_master WHERE type ='table';"
        tables = self.conn.execute(_SQL).fetchall()
        res = [table_name[0] for table_name in tables]
        return res

    def get_table(self, table_name):
        _SQL = "SELECT * FROM " + table_name + ";"
        table = self.conn.execute(_SQL).fetchall()
        return table

    def get_table_header(self, table_name):
        return [i[1] for i in self.conn.execute("pragma table_info("+table_name+");").fetchall()]

    def add_item_content_to_sql(self, content):
        # _SQL = "SELECT table_name FROM information_schema.tables WHERE table_name = '" + content['table_name']\
        #        + "' AND table_schema = database();"
        _SQL = "SELECT name FROM sqlite_master WHERE type ='table' AND name LIKE '%s'; " % content['table_name']
        table_exist = self.conn.execute(_SQL).fetchone()
        if table_exist:
            # self.logger.debug("table %s exist " % content['table_name'])
            _SQL = "INSERT INTO "+content['table_name']+" ("
            for k, v in content.items():
                if k != 'table_name':
                    _SQL += k + ", "
            _SQL = _SQL[0: -2] + ") VALUES ("

            for k, v in content.items():
                if k != 'table_name':
                    v = str(v).replace("'", "`")
                    v = v.replace('"', "``")
                    _SQL += "'" + v + "', "

            _SQL = _SQL[0: -2] + """);"""
            # _SQL = re.sub(r'[^\w\s!?.,;:@#$%^&*№><~`\[\]()]', "", _SQL)
            try:
                self.conn.execute(_SQL)
            except Exception as e:
                print("we couldn`t insert into %s this SQL - %s, have this error : %s " % (content['table_name'], _SQL, e))
                # self.logger.error('error msg', e)
                return False, e
        else:
            print("table %s does not exist " % content['table_name'])
            return False
        return True
