# Library Management System Task - Django Rest Framework

## Overview
Library Management System Task built using Django Rest Framework. the system allows users to manage libraries, books, authors and categories,
users can register, log in, borrow and return books, and recieve real-time updates on book availability.
Additionally, the system allows filtering libraries, books and authors based on various criteria.

### Key features include:
User authentication using Djoser, JWT 
Borrow and return books
Real-time updates for book availability using Django Channels
Filter libraries by book categories
Filter books by category, library, and author
Filter authors by library and book categories, with dynamically updating book counts

### API Endpoints:
#### Authentication
POST /auth/signup/: Register a new user.
POST /auth/jwt/create/: Generate access-tokens, refresh-token.
POST /auth/jwt/refresh/: Refresh the access-token.
POST /auth/jwt/verify/: verify the validity of token.
POST /auth/login/: Log in with email and password.
GET /auth/me/: get user's information.
PUT /auth/me/: update user's information.
GET /auth/users/: get all users in the system.
GET /auth/users/{id}/: get a specific user information.
PUT /auth/users/{id}/: update a specific user information.
DELETE /auth/users/{id}/: delete a specific user.
POST /auth/users/activation/: activate user.
DELETE /auth/users/me/: delete my user account.
POST /auth/users/reset_password/: Reset a forgotten password.
POST /auth/users/set_password/: Set the new password.
POST /auth/users/reset_password_confirm/: Confirm the new password.

#### Library
GET /api/library/libraries/: get all libraries brnaches.
GET /api/library/libraries/?category=<category_name>: get filtering libraries which include specific category.
GET /api/library/libraries/?author=<author_name>: get filtering libraries which include specific author.
GET /api/library/libraries/?category=<category_name>&author=<author_name>: get filtering libraries which include specific category and author.

#### Books
GET /api/book/books/: list all books.
GET /api/book/books/{id}/: get a specific book.
##### filter books by:
GET /api/book/books/?category=<category_name>: filter by category.
GET /api/book/books/?library=<library_name>: filter by library.
GET /api/book/books/?author=<author_name>: filter by author.

#### Authors
GET /api/author/authors/: list all books.
GET /api/author/authors/{id}: get a specific author.
##### filter authors by:
GET /api/author/authors/?category=<category_name>: filter by category.
GET /api/author/authors/?library=<library_name>: filter by library.








