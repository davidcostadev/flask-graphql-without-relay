import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from ..models import db_session, Author as AuthorModel, Article as ArticleModel
from .author import AuthorSingleResult
from .common import Pagination, FilterIdNumber, Sorting


class Article(SQLAlchemyObjectType):

    class Meta:
        model = ArticleModel

    id = graphene.Int()
    author = graphene.Field(AuthorSingleResult)

    def resolve_author(self, info):
        result = db_session.query(AuthorModel).filter(
            AuthorModel.id == self.author_id).first()
        return {'data': result}


class ArticleSingleResult(graphene.ObjectType):
    data = graphene.Field(Article)


class ArticleListResult(graphene.ObjectType):
    data = graphene.List(graphene.NonNull(Article))
    pagination = graphene.Field(Pagination)


class ArticleFilter(graphene.InputObjectType):
    id = FilterIdNumber()


class ArticleSorting(graphene.InputObjectType):
    id = Sorting()
    title = Sorting()
    published_at = Sorting()


class ArticleInput(graphene.InputObjectType):
    title = graphene.NonNull(graphene.String)
    body = graphene.String()
    published_at = graphene.DateTime()
    author_id = graphene.NonNull(graphene.Int)


class CreateArticle(graphene.Mutation):

    class Arguments:
        input = ArticleInput()

    Output = ArticleSingleResult

    def mutate(root, info, input):
        result = ArticleModel(title=input.title,
                              body=input.get('body', None),
                              published_at=input.published_at,
                              author_id=input.author_id)
        db_session.add(result)
        db_session.commit()
        return {'data': result}
