Introduction to htmx — Film Search Exercise

The Film Review Platform API continues throughout Sprint 3. Each day adds a new capability or a test layer to the same codebase established in Sprint 2.

Exercise: Film Search — Server-Rendered UI Fragment

A product manager wants a lightweight internal page where staff can search the film catalogue and see results appear live, without building or deploying a separate frontend application for the search interface. A small server-rendered view added to the existing API is sufficient.

What You Must Build
1. Create a Separate UI Router

Add a new router to the existing FastAPI project specifically for server-rendered HTML pages.

Mount it under a distinct prefix, such as /ui.

Keep it separate from the existing JSON API routes.

Add a page endpoint at GET /ui/films.

2. Create the Film Search Page

Create a full HTML page at /ui/films that contains:

A text input for searching films.

An initially empty results area.

The htmx library loaded from a CDN in the document's <head>.

The page should load normally and allow staff to search the film catalogue without navigating away or reloading the entire page.

3. Create a Jinja2 Film-Card Fragment

Create a Jinja2 template that renders the matching films as HTML cards.

Each card must display:

Film title

Release year

Genre

Average rating

This template must return only the HTML fragment containing the film cards, not a complete HTML page.

4. Implement Live Search Using htmx

Configure the search input so that when its value changes, htmx sends a request to the film-search fragment endpoint.

The interaction should:

Detect a change in the search input.

Send a request containing the search term.

Receive the matching film cards as HTML.

Replace the content of the results area with the returned fragment.

There should be no submit button and no full-page reload.

5. Implement the Fragment Endpoint

Create a FastAPI endpoint that:

Accepts the search term.

Queries the existing DAO layer for matching films.

Passes the results to the Jinja2 fragment template.

Returns the rendered HTML fragment in every case, including when no films match.

The fragment endpoint must return HTML, never JSON.

6. Create a Minimal Next.js Application

Create a separate Next.js project alongside the existing API.

The Next.js application needs only one page that embeds the FastAPI /ui/films page inside an <iframe>.

This companion frontend will also serve as the integration target for later Sprint 3 exercises involving CORS, review submission, and full-stack Docker Compose.

Expected Request Flow
Film Search
User opens the Next.js page
          ↓
Next.js embeds /ui/films in an iframe
          ↓
FastAPI serves the full HTML page
          ↓
User types a search term
          ↓
htmx requests the fragment endpoint
          ↓
FastAPI queries the existing DAO
          ↓
Jinja2 generates the film-card HTML
          ↓
FastAPI returns the HTML fragment
          ↓
htmx replaces the results-area content
Suggested Project Structure
film-review-platform/
├── app/
│   ├── routes/
│   │   ├── film_routes.py       # Existing JSON API
│   │   └── ui_routes.py         # New HTML routes
│   ├── dao/                     # Existing DAO layer
│   └── main.py
├── templates/
│   ├── films.html               # Full search page
│   └── partials/
│       └── film_cards.html      # HTML fragment
└── ...

film-review-frontend/            # Separate Next.js project
└── app/
    └── page.tsx                 # Embeds the iframe

This is a suggested structure; adapt the paths to match your existing project organization.

Completion Checklist
Created the new /ui router.
Kept the HTML routes separate from the JSON API routes.
Created the full page at /ui/films.
Loaded htmx from a CDN.
Created a Jinja2 template for film-card fragments.
Displayed the title, release year, genre, and average rating.
Implemented live search without a submit button or full-page reload.
Connected the fragment endpoint to the existing DAO layer.
Returned HTML for both matching results and empty results.
Created a separate, minimal Next.js application.
Embedded /ui/films in an iframe.
What This Exercise Teaches You

The purpose is to practise building a lightweight, interactive UI using htmx, Jinja2, and FastAPI, while reusing your existing Film Review Platform backend. The Next.js application acts as a separate host for the server-rendered page.

You are not rebuilding the entire platform or replacing your backend. You are adding a new way to present and interact with the existing film catalogue.