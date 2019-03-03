import MySQLdb
import dbconfig


def insert(table_name, lodicts):
    db_dict = dbconfig.read_db_config()
    db = MySQLdb.connect(host=db_dict['host'],
                        user=db_dict['user'],
                        passwd=db_dict['password'],
                        db=db_dict['database'])
    cursor = db.cursor()
    template = "replace into %s (%s) values %s;"
    column_names = []

    # get column names and create column string
    column_names = list(lodicts[0].keys())
    column_string = ""
    for n in column_names:
        column_string += n + ","
    column_string = column_string[:-1]

    # create all the value strings
    values_lst = []
    for vdict in lodicts:
        values = list(vdict.values())
        value_string = "("
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
        value_string = value_string[:-1] + ')'
        # append this into the values list
        values_lst.append(value_string)
    values_str = ','.join(values_lst)
    sql_insert = template % (table_name, column_string, values_str)

    cursor.execute(sql_insert)
    cursor.close()
    db.commit()
