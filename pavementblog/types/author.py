import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from ..models import db_session, Author as AuthorModel, Article as ArticleModel


class Author(SQLAlchemyObjectType):

    class Meta:
        model = AuthorModel


class AuthorSingleResult(graphene.ObjectType):
    data = graphene.Field(Author)
