import graphene
import crm.schema

class Query(crm.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(crm.schema.Mutation, graphene.ObjectType):
    # This class will inherit from multiple Mutations
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
