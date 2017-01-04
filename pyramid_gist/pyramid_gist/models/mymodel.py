from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    email = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    favorite_food = Column(Text)


Index('my_index', MyModel.username, unique=True, mysql_length=255)
