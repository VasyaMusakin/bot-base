import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


# модель базы данных для пользователей
class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    id_tg = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    results = orm.relation("Results", back_populates='user')
