from sqlite3 import *

import config


class Result:

    @staticmethod
    def create_table():
        connection = connect(config.db_file)
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS results (id integer PRIMARY KEY, result TEXT, date DATE)""")
        connection.close()
        return True

    @staticmethod
    def get_all(limit=None):
        connection = connect(config.db_file)
        if limit is not None:
            query = "SELECT * FROM results LIMIT {}".format(limit)
        else:
            query = "SELECT * FROM results"
        results = connection.execute(query).fetchall()
        connection.close()
        the_results = []
        for result in results:
            result_dict = {'id': result[0], 'result': result[1], 'date': result[2]}
            the_results.append(result_dict)
        return the_results

    @staticmethod
    def get_count():
        conn = connect(config.db_file)
        query = "SELECT count(*) FROM results"
        count = conn.execute(query).fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def exist(result_id):
        connection = connect(config.db_file)
        query = f"SELECT COUNT (*) FROM results WHERE id={result_id}"
        count = connection.execute(query).fetchone()[0]
        connection.close()
        if count > 0:
            return True
        else:
            return False

    @staticmethod
    def add(result, date):
        connection = connect(config.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO results (result,date) VALUES ("{result}","{date}")'
        try:
            cursor.execute(query)
            connection.commit()
            connection.close()
            return True
        except:
            return False

    @staticmethod
    def delete(result_id):
        """ DELETE A SINGLE result BASED ON ID """
        connection = connect(config.db_file)
        cursor = connection.cursor()
        query = f'DELETE FROM results WHERE id="{result_id}"'
        cursor.execute(query)
        connection.commit()
        connection.close()
        return True

    @staticmethod
    def update(result_id, result, date):
        if Result.exist(result_id):
            connection = connect(config.db_file)
            cursor = connection.cursor()
            query = f"UPDATE results SET result='{result}', date='{date}' WHERE id={result_id}"
            try:
                cursor.execute(query)
                connection.commit()
                return True
            except:
                return False
        else:
            return False
