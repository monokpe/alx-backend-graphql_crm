# ALX Backend GraphQL CRM

A Django-based CRM system with GraphQL API endpoints.

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

3. Start the development server:

```bash
python manage.py runserver
```

## GraphQL Endpoint

Visit: http://localhost:8000/graphql

### Test Query

```graphql
{
  hello
}
```

Expected response:

```json
{
  "data": {
    "hello": "Hello, GraphQL!"
  }
}
```

## Project Structure

- `alx_backend_graphql_crm/` - Main Django project
- `crm/` - CRM application with models and admin
- `alx_backend_graphql_crm/schema.py` - GraphQL schema definition
- `alx_backend_graphql_crm/urls.py` - URL configuration with GraphQL endpoint
