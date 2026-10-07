FastAPI Day 9 — JWT Authentication + RBAC Part 2

Exercise

Film Review Platform — Role-Based Access Control

Authentication establishes who is making a request. Now the platform must determine what each authenticated user is allowed to do.

The platform has three roles: Admin, Critic, and Viewer. Each role has different permissions that must be enforced at the route layer before the handler runs.

What I Learned Today

Today I learned how Role-Based Access Control (RBAC) is implemented in FastAPI. I learned the difference between authentication and authorization, and how get_current_user() can be combined with a require_role() dependency to check both identity and permissions.

I also learned how FastAPI can use Depends() inside another dependency, how route-level dependencies can enforce authorization without passing a value into the handler, and why authorization should happen before the handler or service is executed.

Authentication vs Authorization

Authentication answers:

Who is this user?

Authorization answers:

Is this user allowed to perform this action?

Authentication
    ↓
Verify JWT
    ↓
Identify User

Authorization
    ↓
Check User Role
    ↓
Allow or Deny Action

get_current_user() handles authentication, while require_role() handles role-based authorization.

get_current_user()

The existing authentication dependency verifies the access token and retrieves the authenticated user.

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

This dependency establishes the identity of the current user.

require_role()

I learned how to create a reusable dependency that accepts the role required by a route.

def require_role(required_role: str):

    async def role_checker(
        user = Depends(get_current_user)
    ):
        if user.role != required_role:
            raise AccessDeniedException(user.role)

        return user

    return role_checker

The dependency first calls get_current_user() and then checks the user's role.

require_role("admin")
        ↓
get_current_user()
        ↓
Verify JWT
        ↓
Get User
        ↓
Check User Role
        ↓
Allowed → Continue
Denied  → 403

Route-Level Authorization

I learned that authorization can be declared at the route level.

@router.delete(
    "/films/{film_id}",
    dependencies=[
        Depends(require_role("admin"))
    ]
)
async def delete_film(film_id: UUID):
    return await film_service.delete_film(film_id)

The dependencies parameter belongs to the FastAPI route decorator. It tells FastAPI to execute the dependency before running the route handler.

The handler does not need the returned user when the dependency is only being used for authorization.

Dependency Chain

FastAPI resolves nested dependencies before executing the route handler.

Request
   ↓
require_role("admin")
   ↓
get_current_user()
   ↓
OAuth2PasswordBearer
   ↓
Extract Bearer Token
   ↓
jwt.decode()
   ↓
Authenticated User
   ↓
Check Role
   ↓
Allowed
   ↓
Route Handler
   ↓
Service

If the role check fails, the handler and service are not executed.

401 vs 403

I learned the difference between authentication and authorization errors.

401 Unauthorized
    ↓
User is not authenticated
    ↓
Missing / invalid / expired token

403 Forbidden
    ↓
User is authenticated
    ↓
User does not have permission

For example:

No valid token
    → 401

Valid token + Viewer tries admin action
    → 403

Custom AccessDeniedException

Instead of raising an HTTPException directly inside the dependency, a custom exception can be used.

class AccessDeniedException(Exception):

    def __init__(self, role: str):
        self.role = role
        self.message = (
            f"Access denied. "
            f"Your role '{role}' is not allowed."
        )

        super().__init__(self.message)

The role dependency can then raise:

if user.role != required_role:
    raise AccessDeniedException(user.role)

A centralized exception handler converts this exception into a 403 response.

@app.exception_handler(AccessDeniedException)
async def access_denied_handler(request, exc):
    return JSONResponse(
        status_code=403,
        content={
            "type": "access_denied",
            "message": exc.message,
            "role": exc.role
        }
    )

Role Model

For this exercise, roles can be stored directly on the user model.

class User(Base):
    ...
    role: str

The three roles are:

admin
critic
viewer

A separate roles and permissions table is possible in larger applications, but it is unnecessary for this exercise because the roles are fixed and simple.

Role vs Permission

A role represents a category of user.

Admin
Critic
Viewer

A permission represents a specific action.

film:create
film:update
film:delete
review:create
review:update
review:delete

A more advanced system can connect roles to many permissions.

User
  ↓
Role
  ↓
Permissions

For this exercise, checking the user's role directly is sufficient.

Role Rules

The Film Review Platform uses the following rules:

Role

Permissions

Admin

Create, update, and soft-delete any film and any review

Critic

Create reviews and update/delete only their own reviews

Viewer

Read-only access

These rules should be enforced consistently across the API.

Admin Authorization

Admins can manage any film and any review.

@router.post(
    "/films",
    dependencies=[Depends(require_role("admin"))]
)
async def create_film(data: FilmCreate):
    return await film_service.create_film(data)

The same authorization pattern can be used for admin-only update and delete operations.

Critic Authorization

Critics can create reviews.

They can also update or delete reviews, but only reviews they own.

Critic
   ↓
Create Review
   → Allowed

Update Own Review
   → Allowed

Delete Own Review
   → Allowed

Update Another User's Review
   → Forbidden

The role check alone is not enough for ownership.

The application must also verify:

current_user.id == review.user_id

This ownership check is a business rule and belongs in the appropriate service logic.

Viewer Authorization

Viewers are read-only users.

Viewer
   ↓
GET films
GET reviews
GET profile
   → Allowed

Create / Update / Delete
   → Forbidden

Authorization vs Business Logic

I learned that role authorization and business rules are different responsibilities.

Authorization asks:

Is this user allowed to perform this operation?

This can be enforced through a route dependency.

Business logic asks:

Even if the user is allowed, is this operation valid?

This belongs in the service layer.

For example:

Admin wants to delete film
        ↓
require_role("admin")
        ↓
Role allowed
        ↓
FilmService
        ↓
Check business rules
        ↓
Delete / Reject

A role check should not be buried inside the service when it is a route-level authorization rule.

/me Endpoint

The /me endpoint should be available to every authenticated user regardless of role.

@router.get("/me")
async def get_me(
    user = Depends(get_current_user)
):
    return user

There is no require_role() here because Admin, Critic, and Viewer should all be able to access their own profile.

Admin  → /me → Allowed
Critic → /me → Allowed
Viewer → /me → Allowed

Admin Statistics Endpoint

The statistics endpoint is restricted to Admin users.

It should return:

Total film count

Total review count

Overall average rating across all reviews

Username of the user who has submitted the most reviews

Conceptually:

@router.get(
    "/admin/stats",
    dependencies=[Depends(require_role("admin"))]
)
async def get_stats():
    return await stats_service.get_platform_stats()

Only an authenticated Admin should be able to access this endpoint.

Admin
   → /admin/stats
   → 200 OK

Critic
   → /admin/stats
   → 403 Forbidden

Viewer
   → /admin/stats
   → 403 Forbidden

Manual Verification

I learned that role boundaries should be tested manually through the interactive API documentation.

At least three requests should be made for each role.

Admin

Admin → permitted request
Admin → permitted request
Admin → permitted request

Expected result:

200 OK

Critic

Critic → create review
Critic → update own review
Critic → admin-only operation

Expected results:

200 / 201 → permitted
403       → forbidden

Viewer

Viewer → read films
Viewer → read reviews
Viewer → create/update/delete operation

Expected results:

200 → permitted
403 → forbidden

Exercise Requirements Completed

Created the concept of a reusable require_role() dependency.

Combined require_role() with get_current_user() using nested Depends().

Learned how route-level dependencies=[...] can enforce authorization.

Applied Admin, Critic, and Viewer role boundaries.

Added the /me endpoint for all authenticated users.

Added the concept of an Admin-only statistics endpoint.

Learned the difference between 401 Unauthorized and 403 Forbidden.

Used a custom AccessDeniedException for authorization failures.

Understood role fields versus separate roles and permissions tables.

Separated route-level authorization from service-level business rules.

Learned that Critic review updates and deletes also require ownership checks.

Verified role boundaries through interactive API documentation.

Final RBAC Flow

Client
   ↓
FastAPI Route
   ↓
require_role()
   ↓
get_current_user()
   ↓
OAuth2PasswordBearer
   ↓
Extract Access Token
   ↓
jwt.decode()
   ↓
Authenticated User
   ↓
Check Role
   ↓
┌───────────────┴───────────────┐
Allowed                         Denied
   ↓                              ↓
Handler                        403 Forbidden
   ↓
Service
   ↓
Business Rules
   ↓
Response

Final Role Flow

                    Authenticated User
                           ↓
                    Check User Role
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
      Admin              Critic             Viewer
        ↓                  ↓                  ↓
 Manage films       Create reviews       Read only
 Manage reviews     Own reviews
 Statistics         only

Final Architecture

Client
   ↓
FastAPI Route
   ↓
Authorization Dependency
   ↓
Authentication Dependency
   ↓
Current User
   ↓
Role Check
   ↓
Route Handler
   ↓
Service Layer
   ↓
Business Rules
   ↓
DAO
   ↓
Database