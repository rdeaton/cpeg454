"""
This file is the heart of the code which will be run. See the top-level README
for details on how to set the system up.

As this is the module __init__ file, it specifies which names are available
to be imported with the module. The following gives a synopsis of those names.
Many of these names are to be imported from here, which is the standard Python
way of doing singleton-style classes via import, without the code or indirection
overhead. In addition to providing these names for import, this file contains
the basic setup code to run the application under any condition.

| *app* is an instance of flask.Flask() which is to handling the application.
| *config* is the imported config module.
| *db* is an instance of flask.ext.sqlalchemy.SQLAlchemy which is used for all
  database configuration and querying.
| *database* is the imported database module. This in particular must be imported
  only from the name wifimap.database, as it relies on this code having been
  run to do some setup on the *app* object.
"""

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from optparse import OptionParser
import config
import sys

# Make sure that we have confirguration setup for our application
try:
    from . import config
except ImportError:
    print "Configuration file missing. See README for details on configuration."
    exit(-1)
    
def main():
    global app, db, web, database, pages
    parser = OptionParser()
    parser.add_option("-r", "--reset-db", action="store_true", default=False, dest="reset_db", help="Reset the database.")
    parser.add_option("--server",  action="store_true", default=False, dest="start_server", help="Run the test webserver.")
    parser.add_option("--shell", action="store_true", dest="shell", default=False)
    parser.add_option("--test", action="store_true", dest="test", default=False)
    (options, args) = parser.parse_args()
    print options
    
    if options.reset_db or options.start_server or options.test:
        # Setup the application and database
        app = Flask(__name__.split('.')[0])
        app.config.from_object(config.FlaskConfig)
        app.jinja_env.add_extension('jinja2.ext.do')
        db = SQLAlchemy(app)
        import database
        import web
        if options.reset_db:
            db.drop_all()
            db.create_all()
            #dataset.populate()
            print 'Database reset.'
            exit(0)
        if options.test:
            checkins = database.Checkin.query.all()
            print checkins
                        
            
            
            exit()
            
            
        import pages
        app.run(host='0.0.0.0', port=config.dev_port, use_reloader=True)
    elif options.shell:
        app = Flask(__name__.split('.')[0])
        app.config.from_object(config.FlaskConfig)
        db = SQLAlchemy(app)
    else:
        parser.print_help()
        
def wsgi():
    global app, db, web, database, pages
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config.FlaskConfig)
    app.jinja_env.add_extension('jinja2.ext.do')
    db = SQLAlchemy(app)
    import database
    import web
    import pages
