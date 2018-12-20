import MySQLdb

db_dict = dbconfig.read_db_config()
db = MySQLdb.connect(host=db_dict['host'],
                         user=db_dict['user'],
                         passwd=db_dict['password'],
                         db=db_dict['database'])
cursor = db.cursor()

