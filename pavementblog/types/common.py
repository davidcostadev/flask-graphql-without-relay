import graphene


class Pagination(graphene.ObjectType):
    totalCount = graphene.Int()
    totalPages = graphene.Int()
    page = graphene.Int()
    limit = graphene.Int()


class FilterIdNumber(graphene.InputObjectType):
    eq = graphene.Int()
    in_list = graphene.List(graphene.NonNull(graphene.Int))


class PaginationInput(graphene.InputObjectType):
    page = graphene.Int(default_value=1)
    limit = graphene.Int(default_value=25)


class Sorting(graphene.Enum):
    ASC = "asc"
    DESC = "desc"
