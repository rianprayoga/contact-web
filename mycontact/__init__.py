import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    db_path = os.path.join(app.instance_path,'contact.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_mapping(
        SECRET_KEY = 'dev',
		#DATABASE = os.path.join(app.instance_path,'contact.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from mycontact.model.db_model import db
    from mycontact.model import db_model
    db.init_app(app)
    db_model.init_db(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import manage_contact
    app.register_blueprint(manage_contact.bp)

    return app
