# hack-challenge-project


## User Authentication

** Login

**Route:** `POST /login`

**Request:**
- Parameters:
  - `username`: Username of the user.
  - `password`: Password of the user.
- Body: JSON
  ```json
  {
      "username": "string",
      "password": "string"
  }

**Response:**

-   Success: 200 OK
    -   Body: JSON
     ```json

    `{ "message": "Login successful", 
    "user": { 
    "id": "<ID>", 
    "name": "<NAME>", 
    "username":"<USERNAME>",
     "balance": "<BALANCE>" } 
    }`



-   Failure: 401 Unauthorized or 400 Bad Request
    -   Body: JSON
    ```json
    `{ "error": "Invalid username or password" }`

### Logout

**Route:** `POST /logout`

**Response:**

-   Success: 200 OK
    -   Body: JSON
    ```json
    `{ "message": "Logout successful", 
        "user": { 
        "id": "<ID>", 
        "name": "<NAME>",
        "username": "<USERNAME>", 
        "balance": "<BALANCE>" 
        } 
    }`

-   Failure: 401 Unauthorized
    -   Body: JSON
```json
    `{ "error": "Logout Error" }`

User Management
---------------

### Create User Account

**Route:** `POST /create-account`

**Request:**

-   Parameters:
    -   `name`: Name of the user.
    -   `username`: Username of the user.
    -   `password`: Password of the user.
    -   `password-confirmation`: Password confirmation of the user.
-   Body: JSON
    ```json
    `{ "name": "string", 
        "username": "string", 
        "password": "string", 
        "password-confirmation": "string" 
    }`

**Response:**

-   Success: 200 OK
    -   Body: JSON
    ```json

    `{ "message": "Account created successfully", 
        "user": { 
            "id": "<ID>", 
            "name": "<NAME>",
            "username": "<USERNAME>", 
            "balance": 0 
            } 
    }`

-   Failure: 401 Unauthorized or 400 Bad Request
    -   Body: JSON
    ```json
    `{ "error": "Invalid username or password" }`

Book Management
---------------

### Get All Books

**Route:** `POST /get-all-books`

**Response:**

-   Success: 200 OK
    -   Body: JSON Array
    ```json
    `[ { "id": "<ID>", 
        "title": "<TITLE>", 
        "author": "<AUTHOR>", 
        "genre": "<GENRE>",
        "ratings": "<RATINGS>" 
        }, ...
     ]`

-   Failure: 404 Not Found
    -   Body: JSON
    ```json
    `{ "error": "No books found" }`

### Get Book by ID

**Route:** `POST /get-book-by-id/<int:book_id>`

**Response:**

-   Success: 200 OK
    -   Body: JSON
    ```json
    `{ "id": "<ID>", 
        "title": "<TITLE>", 
        "author": "<AUTHOR>", 
        "genre": "<GENRE>",
        "ratings": "<RATINGS>" 
    }`

-   Failure: 404 Not Found
    -   Body: JSON
    ```json
    `{ "error": "Book with ID {book_id} not found" }`

### Filter Books by Genre

**Route:** `POST /filter-genre`

**Request:**

-   Parameters:
    -   `genre_name`: Name of the genre.
-   Body: JSON
    ```json
    `{ "genre_name": "string" }`

**Response:**

-   Success: 200 OK
    -   Body: JSON Array
    ```json
    `[ 
        { "id": "<ID>", 
        "title": "<TITLE>", 
        "author": "<AUTHOR>", 
        "genre": "<GENRE>",
        "ratings": "<RATINGS>" 
        }, ... 
    ]`

-   Failure: 404 Not Found
    -   Body: JSON
    ```json
    `{ "error": "No books found for genre '{genre_name}'" }`

Ratings Management
------------------

### Sort Books by Ratings Range

**Route:** `POST /sort-by-ratings/<int:min_rating>/<int:max_rating>/<string:order>`

**Request:**

-   Parameters:
    -   `min_rating`: Minimum rating.
    -   `max_rating`: Maximum rating.
    -   `order`: Sorting order ('asc' for ascending, 'desc' for descending).

**Response:**

-   Success: 200 OK
    -   Body: JSON Array
    ```json

    `[ { "id": "<ID>", 
        "title": "<TITLE>", 
        "author": "<AUTHOR>", 
        "genre": "<GENRE>",
        "ratings": "<RATINGS>" 
        }, ... 
    ]`

-   Failure: 404 Not Found or 400 Bad Request
    -   Body: JSON
    ```json
    `{ "error": "Invalid rating range" or "Failed to sort by ratings" }`

### Add Ratings to a Book

**Route:** `POST /add-ratings/<int:user_id>/<int:book_id>/<int:rating>`

**Request:**

-   Parameters:
    -   `user_id`: ID of the user.
    -   `book_id`: ID of the book.
    -   `rating`: Rating to add (between 0 and 5).

**Response:**

-   Success: 200 OK
    -   Body: JSON
    ```json
    `{ "message": "Rating added successfully" }`

-   Failure: 404 Not Found or 400 Bad Request
    -   Body: JSON
    ```json
    `{ "error": "User not found" or "Invalid rating" }`

Favorites Management
--------------------

### Get All Favorites of a User

**Route:** `POST /get-all-favorites`

**Request:**

-   Parameters:
    -   `user_id`: ID of the user.
-   Body: JSON
    ```json
    `{ "user_id": "int" }`

**Response:**

-   Success: 200 OK
    -   Body: JSON Array
    ```json
    `[ { "user_id": "<USER_ID>", "book_id": "<BOOK_ID>" }, ... ]`

-   Failure: 404 Not Found or 400 Bad Request
    -   Body: JSON
    ```json
    `{ "error": "No favorites found for this user" or "User ID is required" }`

### Favorite a Book

**Route:** `POST /favorite-book`

**Request:**

-   Parameters:
    -   `user_id`: ID of the user.
    -   `book_id`: ID of the book.
-   Body: JSON
    ```json
    `{ "user_id": "int", "book_id": "int" }`

**Response:**

-   Success: 200 OK
    -   Body: JSON
    ```json
    `{ "message": "Book favorited successfully" }`

-   Failure: 400 Bad Request
    -   Body: JSON
    ```json
    `{ "error": "Invalid user ID or book ID" }`
