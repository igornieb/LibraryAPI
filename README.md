# Description

I decided to accomplish this task by creating basic book database. I tried to test my code
as much as possible and focus on code readability.

This API consists of:
- Endpoint to log in by user
- Public endpoint to serve data from models with all related objects
- Private endpoint (only for superusers) to create entry with nested objects
- Private endpoint (only for managers) to update entry with nested objects

# How to run

You will need to install docker.

Run terminal in project directory and type `docker-compose up` command. Development server will start on port 8000.

# Tests

To run tests enter app terminal and type in `python manage.py test`.

# Api endpoints

Authentication - JWT token are used for authentication across API views. You can specify expiration time in `docker-compose.yml` file. Basic authentication is also enabled in
settings.py file.

Isbn - a 10 digits number that identifies a specific book, an edition of a book, or a book-like product. It is used to identify specific books
and is validated on object creation. Through this project isbns are used to identify books and access their endpoints.
Example isbns:
- 007462542X
- 9788390021

## /api/auth/register/

### post

Endpoint for creating users.

Request:

```
{
    "first_name":string,
    "last_name":string,
    "username":string,
    "password":string
}
```

Response code: `201`

## /api/auth/token/

### post

Endpoint for logging in, getting access and refresh tokens.

Request:

```
{
    "username":string,
    "password":string
}
```

Response: 

```
{
    "refresh":string
    "access":string,
}
```

Response code: `200`

## /api/auth/token/refresh/

### post

Endpoint for getting new token.

Request:

```
{
    "refresh":string
}
```

Response: 

```
{
    "access":string
}
```

Response code: `200`

## /api/books/

### get

Endpoint for getting book list. Results are paginated.

Request:

```
{
    "count": int,
    "next": int,
    "previous": int,
    "results": [
        {
            "id": int,
            "authors": [
                {
                    "id": int,
                    "first_name": string,
                    "last_name": string
                },
              ...
            ],
            "created_by": {
                "username": string,
                "first_name": string,
                "last_name": string,
                "user_type": S/U
            },
            "isbn": string,
            "title": string,
            "description": string,
            "published_date": datetime
        }
      ...
    ]
}
```

Response code: `200`

### post

Endpoint for creating new book. Only superusers can add new books, on creation they need to specify username of user
that will have permission to alter this book in the future, only users designated as staff can be specified in created_by field.
User is considered as staff if his user_type is set as "S" (staff). By default, users are set as "U" (normal users).

When specifying authors you either need to:
- specify id, first_name, last_name to get existing author
- specify first_name, last_name only to create new author

As per task requirements multiple objects can be assigned to authors field

Request:

```
{
    "authors": [
                 {
                    "id": int,
                    "first_name": string,
                    "last_name": string
                },
              ...
            ],
    "managed_by": string,
    "isbn": string,
    "title": string,
    "description": string,
    "published_date": datetime
}
```

Response: 

```
{
    "id": int,
    "authors": [
        {
            "id": int,
            "first_name": string,
            "last_name": string
        },
         ...
        ],
    "created_by": {
        "username": string,
        "first_name": string,
        "last_name": string,
        "user_type": string
    },
    "managed_by": {
        "username": string,
        "first_name": string,
        "last_name": string,
        "user_type": string
    },
    "isbn": string,
    "title": string,
    "description": string,
    "published_date": datetime
}
```

Response code: `201`


## /api/books/{isbn}

### get

Endpoint for getting book with given isbn.

Response: 

```
{
    "id": int,
    "authors": [
        {
            "id": int,
            "first_name": string,
            "last_name": string
        },
         ...
        ],
    "created_by": {
        "username": string,
        "first_name": string,
        "last_name": string,
        "user_type": string
    },
    "isbn": string,
    "title": string,
    "description": string,
    "published_date": datetime
}
```

Response code: `200`

### patch

Endpoint for editing book with given isbn. Only users that are set as staff and are specified in created_by can use this endpoint.

When specifying authors you either need to:
- specify id, first_name, last_name to get existing author
- specify first_name, last_name only to create new author

As per task requirements multiple objects can be assigned to authors field


Request:

```
{
    "authors": [
        {
            "id": int,
            "first_name": string,
            "last_name": string
        },
         ...
        ],
    "isbn": string,
    "title": string,
    "description": string,
    "published_date": datetime
}
```

Response: 

```
{
    "id": int,
    "authors": [
        {
            "id": int,
            "first_name": string,
            "last_name": string
        },
         ...
        ],
    "created_by": {
        "username": string,
        "first_name": string,
        "last_name": string,
        "user_type": string
    },
    "isbn": string,
    "title": string,
    "description": string,
    "published_date": datetime
}
```

Response code: `200`

