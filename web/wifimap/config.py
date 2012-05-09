# Example configuration file. Copy to config.py in the current or parent directory

# Uncomment this for the database type
db_type = 'mysql'
#db_type = 'sqlite'
htpath = '.'

sqlite_file = 'db.sqlite'

mysql = {}
mysql['user']    = 'wifimap'
mysql['pass']    = 'supersecret'
mysql['host']    = 'localhost'
mysql['port']    = '3306'
mysql['db']      = 'wifimap'
mysql['charset'] = 'utf8'
mysql['driver']  = 'pymysql'
# Recommended for production/speed critical environments on CPython
# mysql['driver']  = 'mysqldb'
# This is used for cryptographic session signing. It needs to be a secret,
# and unique for the launched install. To generate something random and secure,
# try the following:
# >>> import os
# >>> os.urandom(128)
flask_secret_key = "dev_key"
# This should also be kept secret for deployment, but does not need to be
# cryptographically secure
session_salt = "session-saltysalty"

# These should only be changed during development
# Any of these being true in production is an security vulnerability which is
# beyond trivial to exploit. Don't leave these on, ever.
flask_debug = True
flask_test = False
dev_port = 5050

# Don't touch from here down!
if db_type == 'sqlite':
    class FlaskConfig():
        DEBUG = flask_debug
        TESTING = flask_test
        SECRET_KEY = flask_secret_key
        SQLALCHEMY_DATABASE_URI =\
            'sqlite:///%s' % sqlite_file
else:
    class FlaskConfig():
        DEBUG = flask_debug
        TESTING = flask_test
        SECRET_KEY = flask_secret_key
        SQLALCHEMY_DATABASE_URI =\
            'mysql+%(driver)s://%(user)s:%(pass)s@%(host)s:%(port)s/%(db)s?charset=%(charset)s' % mysql
