import os

username = os.environ.get('FEMS_MYSQL_USR', 'root')
password = os.environ.get('FEMS_MYSQL_PWD', 'root')
conn_str = 'mysql://' + username + ':' + password + '@localhost/fems_db'