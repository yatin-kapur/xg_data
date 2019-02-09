import MySQLdb
import dbconfig


def insert(table_name, **kwargs):
    db_dict = dbconfig.read_db_config()
    db = MySQLdb.connect(host=db_dict['host'],
                        user=db_dict['user'],
                        passwd=db_dict['password'],
                        db=db_dict['database'])
    cursor = db.cursor()
    template = "replace into %s (%s) values (%s);"
    column_names = []
    values = []
    for k, v in kwargs.items():
        column_names.append(k)
        values.append(v)

    column_string = ""
    for n in column_names:
        column_string += n + ","
    column_string = column_string[:-1]

    value_string = ""
    for v in values:
        if(v is None):
            value = "NULL"
        elif type(v) is int:
            value = str(v)
        elif type(v) is float:
            value = str(v)
        else:
            value = '"' + str(v) + '"'
        value_string += value + ","
    value_string = value_string[:-1]
    sql_insert = template % (table_name, column_string, value_string)

    cursor.execute(sql_insert)
    cursor.close()
    db.commit()
