from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    'postgresql+psycopg2://postgres:123asd@localhost:5432/pavement_dev',
    convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String, nullable=True)
    published_at = Column(DateTime, default=func.now())
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(Author,
                          backref=backref('articles',
                                          uselist=True,
                                          cascade='delete,all'))
