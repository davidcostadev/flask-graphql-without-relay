import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from ..models import db_session, Author as AuthorModel, Article as ArticleModel


class Author(SQLAlchemyObjectType):

    class Meta:
        model = AuthorModel


class AuthorSingleResult(graphene.ObjectType):
    data = graphene.Field(Author)


class AuthorInput(graphene.InputObjectType):
    name = graphene.NonNull(graphene.String)


class CreateAuthor(graphene.Mutation):

    class Arguments:
        input = AuthorInput()

    Output = AuthorSingleResult

    def mutate(root, info, input):
        result = AuthorModel(name=input.name)
        db_session.add(result)
        db_session.commit()
        return {'data': result}
