# ALX Backend GraphQL CRM

A Django-based CRM system with GraphQL API endpoints and advanced filtering capabilities.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Populate with sample data:

```bash
python manage.py populate_data
```

4. Start the development server:

```bash
python manage.py runserver
```

## GraphQL Endpoint

Visit: http://localhost:8000/graphql

## Features

### Models

- **Customer**: name, email, phone, created_at
- **Product**: name, description, price, stock, created_at
- **Order**: customer, products, order_date, total_amount, created_at

### Advanced Filtering

The GraphQL API supports comprehensive filtering using django-filter integration:

#### Customer Filters

- `name`: Case-insensitive partial match
- `email`: Case-insensitive partial match
- `created_at__gte`: Created after date
- `created_at__lte`: Created before date
- `phone_pattern`: Custom filter for phone number patterns

#### Product Filters

- `name`: Case-insensitive partial match
- `price__gte`: Price greater than or equal
- `price__lte`: Price less than or equal
- `stock__gte`: Stock greater than or equal
- `stock__lte`: Stock less than or equal
- `low_stock`: Boolean filter for products with stock < 10

#### Order Filters

- `total_amount__gte`: Total amount greater than or equal
- `total_amount__lte`: Total amount less than or equal
- `order_date__gte`: Order date after
- `order_date__lte`: Order date before
- `customer_name`: Filter by customer name (related field)
- `product_name`: Filter by product name (related field)
- `product_id`: Filter by specific product ID

## Example Queries

### Basic Customer Query

```graphql
{
  allCustomers {
    edges {
      node {
        id
        name
        email
        phone
        createdAt
      }
    }
  }
}
```

### Filtered Customer Search

```graphql
{
  allCustomers(name: "john", phonePattern: "+1") {
    edges {
      node {
        id
        name
        email
        phone
      }
    }
  }
}
```

### Product Search with Price Range

```graphql
{
  allProducts(priceGte: 50.0, priceLte: 200.0) {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

### Low Stock Products

```graphql
{
  allProducts(lowStock: true) {
    edges {
      node {
        id
        name
        stock
      }
    }
  }
}
```

### Orders by Customer Name

```graphql
{
  allOrders(customerName: "john") {
    edges {
      node {
        id
        totalAmount
        orderDate
        customer {
          name
        }
        products {
          name
        }
      }
    }
  }
}
```

### Orders with Specific Product

```graphql
{
  allOrders(productId: 1) {
    edges {
      node {
        id
        totalAmount
        customer {
          name
        }
        products {
          name
        }
      }
    }
  }
}
```

## Mutations

### Create Customer

```graphql
mutation {
  createCustomer(name: "New Customer", email: "new@example.com") {
    customer {
      id
      name
      email
    }
    ok
    error
  }
}
```

### Create Product

```graphql
mutation {
  createProduct(name: "New Product", price: 99.99, stock: 10) {
    product {
      id
      name
      price
      stock
    }
    ok
    error
  }
}
```

### Create Order

```graphql
mutation {
  createOrder(customerId: "1", productIds: ["1", "2"]) {
    order {
      id
      totalAmount
      customer {
        name
      }
      products {
        name
      }
    }
    ok
    error
  }
}
```

## Project Structure

- `alx_backend_graphql_crm/` - Main Django project
- `crm/` - CRM application with models, filters, and GraphQL schema
- `crm/models.py` - Django models (Customer, Product, Order)
- `crm/filters.py` - Django-filter classes for advanced filtering
- `crm/schema.py` - GraphQL schema with mutations and queries
- `alx_backend_graphql_crm/schema.py` - Main GraphQL schema
- `alx_backend_graphql_crm/urls.py` - URL configuration with GraphQL endpoint
