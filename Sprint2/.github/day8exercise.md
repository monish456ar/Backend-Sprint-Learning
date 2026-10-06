# FastAPI Day 8 — JWT Authentication + RBAC Part 1

## Exercise

### Film Review Platform — Authentication

The platform needs to identify who is making each request. Users can register and log in, while protected resources require a valid authentication token.

## What I Learned Today

Today I learned how JWT authentication is implemented in FastAPI and how it differs from Express authentication syntax. I learned password hashing with `passlib`, JWT creation and verification using `python-jose`, and how access and refresh tokens are used. I also learned how `OAuth2PasswordBearer` extracts the Bearer access token from the request and how `Depends()` can be used to create reusable authentication dependencies.

## Password Hashing

Passwords should never be stored as plain text. I used `passlib` with bcrypt to hash passwords during registration and verify submitted passwords during login.

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"]
)

hashed_password = pwd_context.hash(password)

is_valid = pwd_context.verify(
    entered_password,
    hashed_password
)
```

The original password cannot be recovered from the stored hash.

## JWT Access Token

I learned that a JWT contains a header, payload, and signature. The payload can contain claims such as the user's ID, role, and expiration time.

```python
payload = {
    "sub": str(user.id),
    "role": user.role,
    "exp": expiry
}

token = jwt.encode(
    payload,
    SECRET_KEY,
    algorithm="HS256"
)
```

The `sub` claim is commonly used to identify the user, while `exp` controls when the token expires.

## JWT Verification

I learned that `jwt.decode()` is similar to `jwt.verify()` in Express. It verifies the token signature and checks claims such as expiration.

```python
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=["HS256"]
)
```

If the token is invalid or expired, the request should be rejected.

## Access Token

The access token is short-lived and is sent with normal protected API requests.

```http
Authorization: Bearer <access_token>
```

In FastAPI, `OAuth2PasswordBearer` extracts the Bearer token from the Authorization header. It does not create or verify the JWT.

```python
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)
```

The JWT is created with `jwt.encode()` and verified with `jwt.decode()`.

## Refresh Token

A refresh token is longer-lived than an access token. It is used to obtain a new access token when the current access token expires.

```text
Access Token  → short-lived → normal API requests
Refresh Token → long-lived  → obtain a new access token
```

The login endpoint can return both tokens. The refresh token is sent to the `/refresh` endpoint when a new access token is needed.

Refresh tokens can be stored and tracked in a database or Redis so that they can be validated, expired, and revoked.

## Authentication Dependency

I learned that a FastAPI dependency can be used similarly to authentication middleware in Express.

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"]
    )

    user_id = payload["sub"]

    user = await user_dao.find_by_id(user_id)

    return user
```

A protected route can then use:

```python
@router.get("/profile")
async def profile(
    user = Depends(get_current_user)
):
    return user
```

FastAPI runs the dependency before the route handler and rejects unauthenticated requests.

## Register and Login

The `/register` endpoint accepts a username, email, and password and stores the password as a bcrypt hash.

The `/login` endpoint validates the submitted credentials and, after successful authentication, creates a short-lived access token and a longer-lived refresh token.

```text
/register
    ↓
Hash password
    ↓
Store user

/login
    ↓
Verify password
    ↓
Create access token
Create refresh token
    ↓
Return tokens
```

## Refresh Endpoint

The `/refresh` endpoint accepts a refresh token and validates it before creating a new access token.

```text
Access token expires
        ↓
Client sends refresh token
        ↓
/refresh
        ↓
Validate refresh token
        ↓
Create new access token
```

Expired or revoked/previously used refresh tokens must be rejected.

## Public and Protected Routes

The registration and login endpoints remain public because a user must be able to access them without already being authenticated.

Other application endpoints require a valid access token through the authentication dependency.

```text
/register  → Public
/login     → Public

Other API routes
     ↓
get_current_user
     ↓
Valid token → Continue
Invalid token → Reject
```

## Express → FastAPI JWT Syntax

| Express                     | FastAPI / Python            |
| --------------------------- | --------------------------- |
| `bcryptjs`                  | `passlib`                   |
| `bcrypt.compare()`          | `pwd_context.verify()`      |
| `jwt.sign()`                | `jwt.encode()`              |
| `jwt.verify()`              | `jwt.decode()`              |
| `req.headers.authorization` | `OAuth2PasswordBearer`      |
| Auth middleware             | `Depends(get_current_user)` |
| `req.user`                  | Dependency return value     |

## Exercise Requirements Completed

* Created the concept of `/register` with password hashing.
* Created the concept of `/login` with credential validation.
* Learned how to create short-lived access tokens.
* Learned how to create and use longer-lived refresh tokens.
* Used JWT claims such as `sub`, `role`, and `exp`.
* Learned how `OAuth2PasswordBearer` extracts the access token.
* Created the `get_current_user` dependency concept for protected routes.
* Learned how `/refresh` validates a refresh token and issues a new access token.
* Understood token expiry and refresh-token revocation.
* Kept registration and login publicly accessible while protecting other endpoints.

## Final Authentication Flow

```text
/register
    ↓
Hash Password
    ↓
Create User

/login
    ↓
Verify Password
    ↓
Access Token + Refresh Token
    ↓
Client

Protected Request
    ↓
OAuth2PasswordBearer
    ↓
Extract Access Token
    ↓
get_current_user
    ↓
jwt.decode()
    ↓
Authenticated User
    ↓
Route Handler

Access Token Expired
    ↓
Client sends Refresh Token
    ↓
/refresh
    ↓
Validate Refresh Token
    ↓
New Access Token
    ↓
Client continues API requests
```

## Final Architecture

```text
Client
   ↓
FastAPI Route
   ↓
Authentication Dependency
   ↓
OAuth2PasswordBearer
   ↓
JWT Decode / Verification
   ↓
Current User
   ↓
Protected Route
```
