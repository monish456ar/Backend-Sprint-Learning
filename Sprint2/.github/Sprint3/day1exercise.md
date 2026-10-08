# Redis — Caching & Token Lifecycle

> ***The Film Review Platform API continues throughout Sprint 3. Each day adds a new capability or a test layer to the same codebase established in Sprint 2.***

## Exercise: Film Review Platform — Caching & Token Lifecycle

Several endpoints are read-heavy and repeatedly return identical results within a short window. Refresh tokens also need a server-side invalidation mechanism so that a logout actually prevents further use — currently an issued refresh token cannot be revoked before it expires.

## What You Must Build

### 1. Shared Redis Connection

Configure a Redis connection from the centralized config object and share it across requests.

The Redis connection must **not** be opened and closed for every individual request.

### 2. Film List Read-Through Caching

Add a read-through caching layer to the film list endpoint.

The first request should:

1. Fetch the film list from the database.
2. Serialize the result.
3. Store the serialized result in Redis.
4. Set a defined TTL.
5. Return the result.

Subsequent requests within the TTL window should return the cached result from Redis without querying the database.

### 3. Cache Invalidation

Invalidate the cached film list whenever a film is:

* Created
* Updated
* Soft-deleted

All cached film list entries that could contain the affected film must be explicitly removed.

The next film list request should then fetch the updated data from the database.

### 4. Refresh Token Storage in Redis

Move refresh token storage to Redis.

When a refresh token is issued:

* Store it in Redis.
* Set its TTL to match the token's expiry.

When a user logs out, explicitly delete the refresh token from Redis.

This ensures the refresh token cannot be used again even if its JWT expiry time has not yet been reached.

### 5. `/logout` Endpoint

Create a `/logout` endpoint that:

1. Accepts a valid access token.
2. Identifies the caller.
3. Removes the caller's refresh token from Redis.
4. Returns a success response.

After logout, attempts to use the deleted refresh token must be rejected.

## Expected Flow

### Film List Caching

```text
GET /films
     ↓
Check Redis
     ↓
   ┌───┴───┐
   ↓       ↓
  HIT     MISS
   ↓       ↓
Return   Database
cache      ↓
         Store in Redis
            ↓
         Return data
```

### Cache Invalidation

```text
Create / Update / Soft-delete Film
                ↓
          Update Database
                ↓
       Remove Film Cache
                ↓
        Next GET /films
                ↓
           Redis MISS
                ↓
        Fetch fresh data
                ↓
        Store in Redis
```

### Refresh Token Lifecycle

```text
Login
  ↓
Issue Refresh Token
  ↓
Store in Redis
  ↓
Set TTL
  ↓
Logout
  ↓
Delete Refresh Token
  ↓
Refresh Attempt
  ↓
Token Not Found
  ↓
Reject Request
```

## Completion Checklist

* [x] Shared Redis connection configured from centralized config
* [x] Redis connection reused across requests
* [x] Read-through caching added to `/films`
* [x] Cached film list has a defined TTL
* [x] Film list cache avoids database queries during the TTL window
* [x] Film creation invalidates the cache
* [x] Film update invalidates the cache
* [x] Film soft-delete invalidates the cache
* [x] Refresh tokens stored in Redis
* [x] Refresh-token TTL matches token expiry
* [x] `/logout` endpoint implemented
* [x] Logout removes the refresh token from Redis
* [x] Deleted refresh tokens are rejected on subsequent refresh attempts
