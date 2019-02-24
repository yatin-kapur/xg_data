"""
makeshift update query for now until i wanna work on this shit later
"""

import MySQLdb
import dbconfig

db_dict = dbconfig.read_db_config()
db = MySQLdb.connect(host=db_dict['host'],
                        user=db_dict['user'],
                        passwd=db_dict['password'],
                        db=db_dict['database'])
cursor = db.cursor()
query = """
        update shot_data s
        join league_records l on s.team = l.title
        set s.competition = l.league;
        """

cursor.execute()
db.commit()
db.close()
