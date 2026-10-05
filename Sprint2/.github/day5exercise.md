# Alembic Migrations + Data Seeding

## Exercise: Film Review Platform — Migration History & Seed Data

### 1. Exercise Goal

The goal of this exercise is to manage the Film Review Platform database using **Alembic migrations** instead of creating tables directly from SQLAlchemy models.

Every schema change should be tracked through a migration file so that the database can be upgraded or downgraded safely.

The exercise also includes a repeatable seed script that creates consistent baseline development data.

---

## 2. What Must Be Built

The exercise should include:

1. Alembic configured with the application's **async SQLAlchemy database setup**.
2. Alembic configured with `Base.metadata` so it can detect ORM model changes.
3. An **initial migration** creating:

   * Users
   * Films
   * Reviews
4. A **second migration** adding a `watchlist` table for the User ↔ Film many-to-many relationship.
5. The second migration must be created separately and must **not modify the first migration**.
6. A seed script containing:

   * At least 10 films
   * At least 3 genres
   * At least 3 users with different roles
   * At least 5 reviews
7. The seed script must be **idempotent** — running it multiple times must not create duplicate records.
8. A comment block at the top of the seed script explaining the complete setup process from an empty database.

---

# 3. Expected Project Structure

```text
app/
├── main.py
│
├── models/
│   ├── base.py
│   ├── user.py
│   ├── film.py
│   └── review.py
│
├── database/
│   ├── session.py
│   └── seed.py
│
└── ...

alembic/
├── env.py
├── script.py.mako
├── README
└── versions/
    ├── <revision>_initial_tables.py
    └── <revision>_add_watchlist.py

alembic.ini
```

---

# 4. Configure Alembic

Initialize Alembic:

```bash
alembic init alembic
```

This creates the Alembic structure:

```text
alembic/
├── env.py
├── versions/
├── script.py.mako
└── README
```

and:

```text
alembic.ini
```

The important configuration is in `env.py`.

Alembic needs to know:

* Which database to connect to.
* That the application uses an async SQLAlchemy engine.
* Which SQLAlchemy metadata contains the application's ORM models.

The important metadata configuration is:

```python
target_metadata = Base.metadata
```

This allows Alembic to compare the database schema with the SQLAlchemy models.

---

# 5. Initial Migration

The first migration should create the three existing tables:

```text
users
films
reviews
```

After the ORM models are ready, generate the migration:

```bash
alembic revision --autogenerate -m "create initial tables"
```

Alembic creates a migration file inside:

```text
alembic/versions/
```

For example:

```text
abc123_create_initial_tables.py
```

The migration should contain:

```python
def upgrade():
    ...


def downgrade():
    ...
```

The `upgrade()` function creates the required tables.

The `downgrade()` function removes them.

---

# 6. Review the Generated Migration

Do not immediately apply the generated migration.

First inspect the file and verify that it matches the intended schema.

Check:

* Table names
* Column names
* Data types
* Primary keys
* Foreign keys
* Nullable fields
* Unique constraints
* Relationships
* Required indexes or constraints

For example, if the model contains:

```python
title: Mapped[str]
```

the generated migration should contain a corresponding `title` column.

If something unexpected appears, correct the migration before applying it.

---

# 7. Apply the Initial Migration

Once the migration has been reviewed:

```bash
alembic upgrade head
```

This applies the migration to PostgreSQL.

The database should now contain:

```text
users
films
reviews
alembic_version
```

The `alembic_version` table is maintained by Alembic and records the currently applied migration revision.

---

# 8. Understand the Migration History

Each migration contains:

```python
revision = "abc123"
down_revision = None
```

The next migration may contain:

```python
revision = "def456"
down_revision = "abc123"
```

This creates the migration chain:

```text
abc123 → def456
```

`revision` identifies the current migration.

`down_revision` points to the previous migration.

Together they maintain the migration history.

The database separately stores its current migration revision in:

```text
alembic_version
```

---

# 9. Second Migration — Watchlist

The second migration should introduce a new `watchlist` table.

The watchlist represents a **many-to-many relationship**:

```text
User ←──── Watchlist ────→ Film
```

One user can have many films in their watchlist.

One film can appear in many users' watchlists.

A simple table could contain:

```text
watchlist
----------------
user_id
film_id
```

Both fields should reference their respective tables.

The migration should be created separately:

```bash
alembic revision --autogenerate -m "add watchlist"
```

Alembic should detect the new model/table and generate the second migration.

---

# 10. Do Not Modify the Initial Migration

After the first migration has already been applied, **do not go back and modify it** to add the watchlist.

Keep the history:

```text
Initial migration
      ↓
Create users
Create films
Create reviews
      ↓
Second migration
      ↓
Create watchlist
```

The migration history should remain:

```text
001_initial_tables
        ↓
002_add_watchlist
```

This demonstrates why migrations are useful: each schema change gets its own history.

---

# 11. Apply the Second Migration

After reviewing the generated migration:

```bash
alembic upgrade head
```

The database should now contain:

```text
users
films
reviews
watchlist
alembic_version
```

---

# 12. Seed Data

Create a separate seed script:

```text
app/
└── database/
    └── seed.py
```

The seed script should use the existing `AsyncSession` setup.

For example:

```python
async with AsyncSessionLocal() as db:
    ...
```

The script should insert baseline development data.

---

# 13. Required Seed Data

The seed script must create at least:

### Users

At least 3 users with distinct roles.

Example:

```text
Admin
Reviewer
Member
```

### Films

At least 10 films.

They must cover at least 3 genres.

Example:

```text
Sci-Fi
Drama
Action
```

### Reviews

At least 5 reviews connected to existing users and films.

Example relationship:

```text
User
  ↓
Review
  ↓
Film
```

---

# 14. Seed Data Must Be Idempotent

The most important requirement is:

> Running the seed script twice must produce the same final database state.

For example, after the first run:

```text
Users: 3
Films: 10
Reviews: 5
```

After running the seed again:

```text
Users: 3
Films: 10
Reviews: 5
```

It should **not** become:

```text
Users: 6
Films: 20
Reviews: 10
```

The seed script must check whether the records already exist before creating them, or otherwise use a safe approach that prevents duplicates.

---

# 15. Simple Seed Flow

The basic flow is:

```text
Start with empty database
        ↓
alembic upgrade head
        ↓
All tables created
        ↓
Run seed.py
        ↓
Initial records inserted
        ↓
Run seed.py again
        ↓
Existing records detected
        ↓
No duplicates created
```

---

# 16. Seed Script Setup Comment

At the very top of `seed.py`, document the complete setup flow.

Example:

```python
"""
Fresh database setup:

1. Start PostgreSQL.
2. Run migrations:
       alembic upgrade head

3. Run the seed script:
       python -m app.database.seed

The seed script can be run multiple times without
creating duplicate baseline records.
"""
```

This makes it clear to another developer how to reproduce the database from scratch.

---

# 17. Async Seed Example

A simplified structure can look like:

```python
from app.database.session import AsyncSessionLocal
from app.models.film import Film


async def seed_films():
    async with AsyncSessionLocal() as db:
        films = [
            Film(
                title="Inception",
                genre="Sci-Fi",
                release_year=2010,
            ),
            Film(
                title="Interstellar",
                genre="Sci-Fi",
                release_year=2014,
            ),
        ]

        db.add_all(films)
        await db.commit()
```

The final exercise should expand this idea to meet the required number of users, films, and reviews.

---

# 18. Migration vs Seeding

Keep these responsibilities separate.

### Alembic

Handles **database structure**:

```text
Tables
Columns
Foreign keys
Indexes
Constraints
```

### Seed Script

Handles **database data**:

```text
Users
Films
Reviews
Development records
```

The relationship is:

```text
SQLAlchemy Models
       ↓
Alembic
       ↓
Database Schema
       ↓
Seed Script
       ↓
Initial Database Data
```

---

# 19. Upgrade and Downgrade

The migration should support moving forward and backward.

Upgrade:

```bash
alembic upgrade head
```

Moves the database to the latest migration.

For example:

```text
001 → 002
```

Downgrade one migration:

```bash
alembic downgrade -1
```

Moves back one migration:

```text
002 → 001
```

Downgrade to a specific revision:

```bash
alembic downgrade <revision>
```

The `upgrade()` and `downgrade()` functions in each migration define the actual schema changes.

---

# 20. Final Expected Flow

Starting from an empty database:

```text
                    SQLAlchemy Models
                           ↓
                    Alembic Configuration
                           ↓
              alembic revision --autogenerate
                           ↓
                  Initial Migration
                           ↓
                    Review Migration
                           ↓
                 alembic upgrade head
                           ↓
              Users / Films / Reviews
                           ↓
              Add Watchlist Model
                           ↓
              Create Second Migration
                           ↓
                    Review Migration
                           ↓
                 alembic upgrade head
                           ↓
                     Watchlist
                           ↓
                    Run seed.py
                           ↓
       3 Users + 10 Films + 5 Reviews
                           ↓
             Run seed.py again
                           ↓
                No duplicate records
```

---

# 21. Exercise Checklist

### Alembic

* [ ] Initialize Alembic.
* [ ] Configure `env.py`.
* [ ] Connect Alembic to the async database setup.
* [ ] Set `target_metadata = Base.metadata`.
* [ ] Generate the initial migration.
* [ ] Review the generated migration manually.
* [ ] Apply the initial migration.
* [ ] Verify the `alembic_version` table.
* [ ] Create a second migration for `watchlist`.
* [ ] Do not modify the initial migration.
* [ ] Review the second migration.
* [ ] Apply the second migration.
* [ ] Test upgrade and downgrade.

### Seed Data

* [ ] Create a separate seed script.
* [ ] Add at least 3 users with different roles.
* [ ] Add at least 10 films.
* [ ] Use at least 3 genres.
* [ ] Add at least 5 reviews.
* [ ] Connect reviews to valid users and films.
* [ ] Make the seed process idempotent.
* [ ] Run the seed script twice.
* [ ] Verify that no duplicate records are created.
* [ ] Document the fresh database setup commands at the top of the seed script.

---

# 22. What This Exercise Demonstrates

After completing this exercise, the project should demonstrate the complete database workflow:

```text
SQLAlchemy Models
       ↓
Alembic detects schema changes
       ↓
Migration files
       ↓
Review migration
       ↓
Upgrade database
       ↓
Seed baseline data
       ↓
Repeatable development database
```

The main concept is that **migrations manage schema history, while seed scripts manage initial data**.
