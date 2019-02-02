import MySQLdb
import dbconfig
import numpy as np


def get_match_ids(competition, year):
    db_dict = dbconfig.read_db_config()
    db = MySQLdb.connect(host=db_dict['host'],
                         user=db_dict['user'],
                         passwd=db_dict['password'],
                         db=db_dict['database'])
    cursor = db.cursor()
    query = """
            select distinct(id)
            from match_data
            where competition in %s
            and season = %s;
            """
    cursor.execute(query % (competition, year))
    match_ids = np.asarray(cursor.fetchall())
    match_ids = np.reshape(match_ids, len(match_ids), 1)

    return match_ids
