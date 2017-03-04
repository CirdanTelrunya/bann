import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
CSRF_ENABLED = True
SECRET_KEY = 'ad0927507679385fc6fa617808336686049d3d89f7223c2ec3e3253de275ad66'
DEBUG = True
LOG_FILE = os.path.join(basedir, 'log/app_logger.log')