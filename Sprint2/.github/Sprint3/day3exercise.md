Pagination, Filtering & Query Optimization — Implementation Plan
1. Film Pagination
Implement offset-based pagination for the film listing endpoint.
- Accept page and page_size query parameters.
- Return the requested films, total count, page, and page_size.
- Use database-level LIMIT and OFFSET so you don't fetch all films into memory.
2. Film Filtering
Allow users to combine these optional filters in the same request:
- genre — exact genre match.
- from_year and to_year — filter films by a release-year range. Either boundary can be optional.
- director — case-insensitive partial match.
Apply filters in the database query before pagination. Keep the total count consistent with the same filters.
3. Review Pagination and Filtering
For the endpoint that lists reviews for a specific film:
- Accept page and page_size.
- Return the paginated reviews and total review count.
- Apply any required review filters in the database before pagination.
Don't add extra review filters unless they're needed by the exercise or your existing API requirements.
4. Fix N+1 Queries
Identify the existing endpoint that causes repeated database queries when loading related data.
- Use SQLAlchemy eager loading, such as selectinload(), where appropriate.
- Load related data only when the response needs it.
- Avoid adding eager loading to every query unnecessarily.
5. Cursor Pagination
Implement cursor-based pagination as an alternative on one endpoint, preferably the film listing endpoint.
- Accept a cursor and a page-size limit.
- Use a stable ordering and fetch only the required records.
- Return the records and next_cursor.
- Return next_cursor: null when there are no more records.
- Keep the cursor opaque to API consumers.
6. Testing Checklist
- [ ] Film pagination returns the correct page and total count.
- [ ] Genre, year range, and director filters work individually and together.
- [ ] Review pagination works for a specific film.
- [ ] The identified N+1 query problem is resolved.
- [ ] Cursor pagination returns the next batch correctly and eventually returns next_cursor: null.
Recommended implementation order: Film pagination → film filters → review pagination → N+1 optimization → cursor pagination → tests.