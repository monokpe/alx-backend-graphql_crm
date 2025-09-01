from django.core.management.base import BaseCommand
from crm.models import Customer, Product, Order
from django.utils import timezone
from decimal import Decimal


class Command(BaseCommand):
    help = "Populate the database with sample data for testing filters"

    def handle(self, *args, **options):
        # Create sample customers
        customers_data = [
            {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
            },
            {
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "+1987654321",
            },
            {
                "name": "Bob Johnson",
                "email": "bob.johnson@example.com",
                "phone": "+1555123456",
            },
            {
                "name": "Alice Brown",
                "email": "alice.brown@example.com",
                "phone": "+1444333222",
            },
            {
                "name": "Charlie Wilson",
                "email": "charlie.wilson@example.com",
                "phone": "+1777888999",
            },
        ]

        customers = []
        for data in customers_data:
            customer, created = Customer.objects.get_or_create(
                email=data["email"], defaults=data
            )
            customers.append(customer)
            if created:
                self.stdout.write(f"Created customer: {customer.name}")

        # Create sample products
        products_data = [
            {
                "name": "Laptop",
                "description": "High-performance laptop",
                "price": Decimal("999.99"),
                "stock": 15,
            },
            {
                "name": "Mouse",
                "description": "Wireless mouse",
                "price": Decimal("29.99"),
                "stock": 50,
            },
            {
                "name": "Keyboard",
                "description": "Mechanical keyboard",
                "price": Decimal("79.99"),
                "stock": 25,
            },
            {
                "name": "Monitor",
                "description": "4K monitor",
                "price": Decimal("299.99"),
                "stock": 8,
            },
            {
                "name": "Headphones",
                "description": "Noise-cancelling headphones",
                "price": Decimal("199.99"),
                "stock": 5,
            },
            {
                "name": "Webcam",
                "description": "HD webcam",
                "price": Decimal("89.99"),
                "stock": 3,
            },
        ]

        products = []
        for data in products_data:
            product, created = Product.objects.get_or_create(
                name=data["name"], defaults=data
            )
            products.append(product)
            if created:
                self.stdout.write(f"Created product: {product.name}")

        # Create sample orders
        orders_data = [
            {
                "customer": customers[0],
                "products": [products[0], products[1]],
                "total_amount": Decimal("1029.98"),
                "order_date": timezone.now(),
            },
            {
                "customer": customers[1],
                "products": [products[2], products[3]],
                "total_amount": Decimal("379.98"),
                "order_date": timezone.now(),
            },
            {
                "customer": customers[2],
                "products": [products[4]],
                "total_amount": Decimal("199.99"),
                "order_date": timezone.now(),
            },
            {
                "customer": customers[3],
                "products": [products[5], products[1]],
                "total_amount": Decimal("119.98"),
                "order_date": timezone.now(),
            },
        ]

        for data in orders_data:
            order, created = Order.objects.get_or_create(
                customer=data["customer"],
                order_date=data["order_date"],
                defaults={"total_amount": data["total_amount"]},
            )
            if created:
                order.products.set(data["products"])
                self.stdout.write(f"Created order: {order}")

        self.stdout.write(
            self.style.SUCCESS("Successfully populated database with sample data!")
        )
