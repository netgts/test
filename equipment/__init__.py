# Этот файл сообщает интерпретатору Python, что каталог 'equipment' является пакетом, и его следует рассматривать
# именно как пакет. Тем самым создаем единое пространство имен
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://developer:111@localhost/devices'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from equipment import routes
