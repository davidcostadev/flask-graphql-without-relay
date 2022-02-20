import graphene
import math
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import db_session, Author as AuthorModel, Article as ArticleModel


class Author(SQLAlchemyObjectType):

    class Meta:
        model = AuthorModel


class Article(SQLAlchemyObjectType):

    class Meta:
        model = ArticleModel


class Pagination(graphene.ObjectType):
    totalCount = graphene.Int()
    totalPages = graphene.Int()
    page = graphene.Int()
    limit = graphene.Int()


class ArticleListResult(graphene.ObjectType):
    data = graphene.List(graphene.NonNull(Article))
    pagination = graphene.Field(Pagination)


class FilterIdNumber(graphene.InputObjectType):
    eq = graphene.Int()
    in_list = graphene.List(graphene.NonNull(graphene.Int))


class PaginationInput(graphene.InputObjectType):
    page = graphene.Int(default_value=1)
    limit = graphene.Int(default_value=25)


class ArticleFilter(graphene.InputObjectType):
    id = FilterIdNumber()


class Sorting(graphene.Enum):
    ASC = "asc"
    DESC = "desc"


class ArticleSorting(graphene.InputObjectType):
    id = Sorting()
    title = Sorting()
    published_at = Sorting()


class Query(graphene.ObjectType):

    class Arguments:
        article_filter = ArticleFilter()

    articles = graphene.Field(ArticleListResult,
                              filter=ArticleFilter(),
                              pagination=PaginationInput(),
                              sorting=ArticleSorting())

    def resolve_articles(self,
                         info,
                         filter=None,
                         pagination=None,
                         sorting=None):
        query = Article.get_query(info)
        query = filters(query, filter)
        query = sortingBy(query, sorting)

        return list_result(query, pagination)


def sortingBy(query, sorting):
    if sorting:
        if sorting.id:
            if sorting.id == 'asc':
                query = query.order_by(ArticleModel.id.asc())
            else:
                query = query.order_by(ArticleModel.id.desc())
        if sorting.published_at:
            if sorting.published_at == 'asc':
                query = query.order_by(ArticleModel.published_at.asc())
            else:
                query = query.order_by(ArticleModel.published_at.desc())
        if sorting.title:
            if sorting.title == 'asc':
                query = query.order_by(ArticleModel.title.asc())
            else:
                query = query.order_by(ArticleModel.title.desc())

    return query


def filters(query, filter):
    if filter:
        query = filter_id(query, filter)

    return query


def filter_id(query, filter):
    if filter.id:
        if filter.id.eq:
            query = query.filter(ArticleModel.id == filter.id.eq)

        if filter.id.in_list:
            query = query.filter(ArticleModel.id.in_(filter.id.in_list))

    return query


def list_result(query, pagination=None):
    if pagination:
        page = pagination.get('page', 1)
        limit = pagination.get('limit', 25)
    else:
        page = 1
        limit = 25

    totalItems = query.count()
    totalPages = math.ceil(totalItems / limit)

    query = query.limit(limit).offset((page - 1) * limit)

    return {
        'data': query.all(),
        'pagination': {
            'totalCount': totalItems,
            'totalPages': totalPages,
            'page': page,
            'limit': limit
        }
    }


schema = graphene.Schema(query=Query)