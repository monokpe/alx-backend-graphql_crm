import graphene
import django_filters
from graphene_django import DjangoObjectType
from django.db import models


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")


schema = graphene.Schema(query=Query)
