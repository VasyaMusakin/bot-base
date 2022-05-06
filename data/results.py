import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


# модель базы данных для результатов игры
class Results(SqlAlchemyBase):
    __tablename__ = 'results'
    maze = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    xo = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    cities = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    all = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"), primary_key=True)
    user = orm.relation('User')
