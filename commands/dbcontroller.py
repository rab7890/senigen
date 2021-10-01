import datetime
import sqlite3


class DBController:

    def __init__(self, db_file, table_type):

        self.db_file = db_file
        self.type = table_type
        if table_type == 'GENOME':
            self.table_name = 'download_genome_info'
        elif table_type == 'GTDBTK':
            self.table_name = 'gtdbtk_info'
        elif table_type == 'REGION':
            self.table_name = 'region_info'

    ##### main info
    def set_main_error(self, msg):
        print("error update : {}".format(msg))
        conn = sqlite3.connect(self.db_file)
        try:
            conn.execute(
                "UPDATE main_info set is_error = TRUE, error_msg = '{0}', error_type = '{1}' WHERE id = '1';".format(msg,
                                                                                                                   self.type))
            conn.commit()
        except Exception as e:
            print("error is occurred when update set_main_error db.")
        conn.close()

    def init_main_error(self):
        conn = sqlite3.connect(self.db_file)
        conn.execute("UPDATE main_info set is_error = FALSE , error_msg = '', error_type = '' WHERE id = '1';")
        conn.commit()
        conn.close()

    def set_running(self):
        conn = sqlite3.connect(self.db_file)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("UPDATE {0} set progress_current_value = 0 ,status = 'RUNNING', modified_date = datetime('now')"
                     " WHERE id = 1;".format(self.table_name))
        conn.commit()
        conn.close()

    def set_idle(self):
        conn = sqlite3.connect(self.db_file)
        now = str(datetime.datetime.now())
        conn.execute("UPDATE {} set pid = '', status = 'IDLE', modified_date = datetime('now'), progress_total_value = 0,"
                     " progress_current_value = 0 WHERE id = '1';".format(self.table_name))
        conn.commit()
        conn.close()

    def get_status(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.execute('SELECT * FROM {};'.format(self.table_name))
        for row in cursor:
            print(row)

    def set_status_log(self, val):
        conn = sqlite3.connect(self.db_file)
        now = str(datetime.datetime.now())
        val = now + ' : ' + val
        val = val.replace("\'", '')
        conn.execute(
            "UPDATE {0} set status_log = '{1}', modified_date = datetime('now') WHERE id = '1';".format(self.table_name
                                                                                                      , val))
        conn.commit()
        conn.close()

    def init_process(self, total):
        conn = sqlite3.connect(self.db_file)
        conn.execute(
            "UPDATE {0} set progress_total_value = {1}, progress_current_value = 0 WHERE id = '1';".format(self.table_name
                                                                                                         ,total))
        conn.commit()
        conn.close()

    def set_process(self, val, total):
        print("current val - {}".format(val))
        cur = round(val/total * 100, 1)
        conn = sqlite3.connect(self.db_file)
        conn.execute(
            "UPDATE {0} set progress_current_value = '{1}' WHERE id = '1';".format(self.table_name, cur))
        conn.commit()
        conn.close()

    def zero_process(self):
        conn = sqlite3.connect(self.db_file)
        conn.execute(
            "UPDATE {0} set progress_current_value = 0, progress_total_value = 0  WHERE id = '1';".format(self.table_name))
        conn.commit()
        conn.close()

class Process:
    process = ''