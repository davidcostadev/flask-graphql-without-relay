import math


def filters(query, filter):
    if filter:
        query = filter_id(query, filter)

    return query


def filter_id(query, filter, model):
    if filter.id:
        if filter.id.eq:
            query = query.filter(model.id == filter.id.eq)

        if filter.id.in_list:
            query = query.filter(model.id.in_(filter.id.in_list))

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


def sorting_article(query, sorting, model):
    if sorting:
        if sorting.id:
            if sorting.id == 'asc':
                query = query.order_by(model.id.asc())
            else:
                query = query.order_by(model.id.desc())
        if sorting.published_at:
            if sorting.published_at == 'asc':
                query = query.order_by(model.published_at.asc())
            else:
                query = query.order_by(model.published_at.desc())
        if sorting.title:
            if sorting.title == 'asc':
                query = query.order_by(model.title.asc())
            else:
                query = query.order_by(model.title.desc())

    return query
