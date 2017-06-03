import pymysql.cursors

def get_db():
  connection = pymysql.connect(host='localhost',
                             user='ankit',
                             password='ankitgohel',
                             db='reddit',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
  return connection