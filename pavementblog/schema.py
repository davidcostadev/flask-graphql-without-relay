import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import db_session, Author as AuthorModel, Article as ArticleModel
from .utils import filters, list_result, sorting_article
from .types import article, author, common


class Query(graphene.ObjectType):

    # class Arguments:
    #     article_filter = ArticleFilter()

    articles = graphene.Field(article.ArticleListResult,
                              filter=article.ArticleFilter(),
                              pagination=common.PaginationInput(),
                              sorting=article.ArticleSorting())

    article = graphene.Field(article.ArticleSingleResult, id=graphene.Int())

    def resolve_articles(self,
                         info,
                         filter=None,
                         pagination=None,
                         sorting=None):
        query = article.Article.get_query(info)
        query = filters(query, filter, ArticleModel)
        query = sorting_article(query, sorting, ArticleModel)

        return list_result(query, pagination, ArticleModel)

    def resolve_article(self, info, id):
        result = db_session.query(ArticleModel).filter(
            ArticleModel.id == id).first()
        return {'data': result}


class Mutations(graphene.ObjectType):
    create_article = article.CreateArticle.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)