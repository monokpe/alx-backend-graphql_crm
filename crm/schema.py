import graphene
from graphene_django import DjangoObjectType, DjangoFilterConnectionField
from graphene import relay
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter
from django.db import IntegrityError, transaction
from django.utils import timezone
from decimal import Decimal


# Type Definitions
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone", "created_at")
        filterset_class = CustomerFilter
        interfaces = (relay.Node,)


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "stock", "created_at")
        filterset_class = ProductFilter
        interfaces = (relay.Node,)


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = (
            "id",
            "customer",
            "products",
            "order_date",
            "total_amount",
            "created_at",
        )
        filterset_class = OrderFilter
        interfaces = (relay.Node,)


# Input Types
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)


# Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    customer = graphene.Field(CustomerType)
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, name, email):
        try:
            customer = Customer.objects.create(name=name, email=email)
            return CreateCustomer(customer=customer, ok=True)
        except IntegrityError:
            return CreateCustomer(ok=False, error="Email already exists.")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(graphene.NonNull(CustomerInput), required=True)

    created_customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, customers):
        created_list = []
        error_list = []
        for i, customer_data in enumerate(customers):
            try:
                with transaction.atomic():
                    customer = Customer.objects.create(
                        name=customer_data.name, email=customer_data.email
                    )
                    created_list.append(customer)
            except IntegrityError:
                error_list.append(
                    f"Error at index {i}: Email '{customer_data.email}' already exists."
                )
            except Exception as e:
                error_list.append(f"Error at index {i}: {str(e)}")

        return BulkCreateCustomers(created_customers=created_list, errors=error_list)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        price = graphene.Decimal(required=True)
        stock = graphene.Int(default_value=0)

    product = graphene.Field(ProductType)
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, name, price, description=None, stock=0):
        if price <= 0:
            return CreateProduct(ok=False, error="Price must be positive.")
        if stock < 0:
            return CreateProduct(ok=False, error="Stock cannot be negative.")

        product = Product.objects.create(
            name=name, description=description, price=price, stock=stock
        )
        return CreateProduct(product=product, ok=True)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.NonNull(graphene.ID), required=True)
        order_date = graphene.DateTime()

    order = graphene.Field(OrderType)
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, customer_id, product_ids, order_date=None):
        if not product_ids:
            return CreateOrder(ok=False, error="At least one product must be selected.")

        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return CreateOrder(ok=False, error="Invalid customer ID.")

        products = Product.objects.filter(pk__in=product_ids)
        if len(products) != len(product_ids):
            return CreateOrder(ok=False, error="One or more product IDs are invalid.")

        total_amount = sum(product.price for product in products)

        order = Order.objects.create(
            customer=customer,
            order_date=order_date or timezone.now(),
            total_amount=total_amount,
        )
        order.products.set(products)

        return CreateOrder(order=order, ok=True)


class UpdateCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        email = graphene.String()

    customer = graphene.Field(CustomerType)
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, name=None, email=None):
        try:
            customer = Customer.objects.get(pk=id)
            if name is not None:
                customer.name = name
            if email is not None:
                customer.email = email
            customer.save()
            return UpdateCustomer(customer=customer, ok=True)
        except Customer.DoesNotExist:
            return UpdateCustomer(ok=False, error="Customer not found")
        except IntegrityError:
            return UpdateCustomer(ok=False, error="Email already exists.")


class DeleteCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            customer = Customer.objects.get(pk=id)
            customer.delete()
            return DeleteCustomer(ok=True)
        except Customer.DoesNotExist:
            return DeleteCustomer(ok=False, error="Customer not found")


class Query(graphene.ObjectType):
    # Filtered queries using DjangoFilterConnectionField
    all_customers = DjangoFilterConnectionField(CustomerType)
    all_products = DjangoFilterConnectionField(ProductType)
    all_orders = DjangoFilterConnectionField(OrderType)

    # Individual item queries
    customer_by_id = graphene.Field(CustomerType, id=graphene.ID(required=True))
    product_by_id = graphene.Field(ProductType, id=graphene.ID(required=True))
    order_by_id = graphene.Field(OrderType, id=graphene.ID(required=True))

    def resolve_customer_by_id(root, info, id):
        try:
            return Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return None

    def resolve_product_by_id(root, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

    def resolve_order_by_id(root, info, id):
        try:
            return Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    update_customer = UpdateCustomer.Field()
    delete_customer = DeleteCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
