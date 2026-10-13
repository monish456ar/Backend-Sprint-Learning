Middleware, Background Tasks & CORS — Exercise
Project: Film Review Platform
Stack: FastAPI + existing Next.js companion app
Goal
Update the existing project to trace requests, measure response time, allow browser access from Next.js, and recalculate film review statistics in the background after a review is created.
What to Build
1. Middleware
- Generate or reuse a request ID for each request.
- Include the same ID in request logs and the X-Request-ID response header.
- Measure request duration and return it in the X-Process-Time-Ms header.
2. CORS
- Allow only http://localhost:3000.
- Allow only the methods and headers the frontend needs, including Authorization and Content-Type if used.
- Do not use wildcard origins.
3. Login and Review UI
Reuse the existing Next.js app and FastAPI login route; do not build a new authentication system if one already exists.
- Log in and use the access token for authenticated API requests.
- Admin/Critic: show the film list and Create Review form.
- Viewer: show the film list only.
- The form needs a film dropdown, rating input, review text field, and submit button.
- Do not add a user dropdown. FastAPI should get the reviewer ID from the authenticated user.
- Protect review creation on the backend with the existing authentication and require_role dependency. Hiding the form in the UI is not enough.
Submit the review to POST /films/{film_id}/reviews, sending the access token and the review fields required by the existing API.
4. Background Task and Film Statistics
- After the review is saved, use FastAPI BackgroundTasks to recalculate the film's review_count and average_rating, then update the Film record.
- The review_count field has already been added to the existing Film table using an Alembic migration; do not add it again.
- Return the created-review response without waiting for this recalculation. The task should manage its own database session if needed.
Verify
- [ ] API responses include X-Request-ID and X-Process-Time-Ms.
- [ ] Server logs for a request share the same request ID.
- [ ] Next.js at http://localhost:3000 can call the API in the browser; an unapproved origin is blocked by browser CORS enforcement.
- [ ] Admin/Critic can see and submit the review form; Viewer cannot create a review, even when calling the API directly.
- [ ] The review is saved and returned, then the film's review count and average rating are updated by the background task.
Note: Bruno and curl do not enforce browser CORS, so test CORS from the browser. BackgroundTasks is suitable for this lightweight exercise, but it does not provide durable retries if the process crashes.