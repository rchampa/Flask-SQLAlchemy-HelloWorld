__author__ = 'Ricardo'


from flask import Flask
app = Flask(__name__, static_url_path = "")
app.config.from_pyfile('flaskapp.cfg')


import logging
from logging import StreamHandler
file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
#app.logger.setLevel(logging.ERROR)  # set the desired logging level here
app.logger.addHandler(file_handler)


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sqlalchemy_tutorial'
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:@localhost/sqlalchemy_tutorial', convert_unicode=True,echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


Base = declarative_base()
from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)


Base.metadata.create_all(bind=engine)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    return 'Hello World!'

from flask import send_from_directory
@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)



@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'

@app.route('/add')
def add():
    u = User('admin', 'admin@localhost')
    db_session.add(u)
    db_session.commit()


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', 5000, app)
    httpd.serve_forever()