import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from ..models import db_session, Author as AuthorModel, Article as ArticleModel


class Author(SQLAlchemyObjectType):

    class Meta:
        model = AuthorModel

    id = graphene.Int()


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


class UpdateAuthor(graphene.Mutation):

    class Arguments:
        id = graphene.Int(required=True)
        input = AuthorInput()

    Output = AuthorSingleResult

    def mutate(root, info, id, input):
        result = db_session.query(AuthorModel).filter(
            AuthorModel.id == id).first()
        result.name = input.name

        db_session.commit()

        return {'data': result}


class DeleteAuthor(graphene.Mutation):

    class Arguments:
        id = graphene.Int(required=True)

    Output = AuthorSingleResult

    def mutate(root, info, id):
        result = AuthorModel.query.filter_by(id=id).one()
        AuthorModel.query.filter_by(id=id).delete()
        db_session.commit()
        return {'data': result}
