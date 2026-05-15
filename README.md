# Medical Ethics Sharing Platform

A Django web application where users can share and discover materials related to Medical Ethics — including films, theatre plays, literary texts, clinical ethics cases, and ethics-related news. Posts go through an editor approval workflow before being published publicly.

---

## Project Overview

This platform allows registered users to submit posts in five categories. Editors (staff users) review submitted content and approve or reject it before it becomes publicly visible. The site features a dark academia aesthetic with photo backgrounds, floating particles, animated post cards, dark mode support, and a fully responsive layout.

---

## Screenshots

### Home Page
![Home Page](screenshotshome.png)

### Browse Posts Page
![Browse Posts](screenshotsbrowse.png)

### Login Page
![Login Page](screenshotslogin.png)

---

## Features

- **User registration, login, and logout**
- **Post creation** — title, content (text), external link, and category
- **5 categories** — Films, Theatre Plays, Literary Texts, Clinical Ethics Cases, Ethics News
- **Editor approval system** — posts are saved as *pending* until an editor approves or rejects them
- **Public post list and detail pages** — only approved posts are shown publicly
- **Search** — search posts by title or content
- **Filter by category** — filter posts on the Browse page
- **User profile page** — update username, email, bio; view submitted posts with statuses
- **Dark/light mode toggle** — saved to localStorage
- **Responsive design** — works on all screen sizes

---

## How to Run the Project

### 1. Prerequisites

- Python 3.10 or higher
- pip

### 2. Clone / Extract the Project

```bash
unzip <project_folder>.zip
cd medethics
```

### 3. Create and Activate a Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install django django-crispy-forms crispy-bootstrap5 pillow
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Editor Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password. This account will have editor privileges.

### 7. Load Initial Categories (Optional)

```bash
python manage.py shell -c "
from blog.models import Category
cats = [
  ('Films','films'),
  ('Theatre Plays','theatre-plays'),
  ('Literary Texts','literary-texts'),
  ('Clinical Ethics Cases','clinical-ethics-cases'),
  ('Ethics News','ethics-news'),
]
for name, slug in cats:
    Category.objects.get_or_create(name=name, slug=slug)
print('Categories created.')
"
```

Or use the setup script if present:

```bash
python setup_data.py
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open your browser at: **http://127.0.0.1:8000/**

---

## Application Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Latest approved posts + hero (for guests) |
| Register | `/register/` | Create a new account |
| Login | `/login/` | Sign in |
| Logout | `/logout/` (POST) | Sign out |
| Browse Posts | `/posts/` | All approved posts with category filter |
| Post Detail | `/posts/<id>/` | Full post content |
| Create Post | `/posts/create/` | Submit a new post (login required) |
| Edit Post | `/posts/<id>/edit/` | Edit your post |
| Delete Post | `/posts/<id>/delete/` | Delete your post |
| Category | `/category/<slug>/` | Posts in a specific category |
| Editor Panel | `/editor/` | Approve/reject pending posts (staff only) |
| My Profile | `/profile/` | Edit profile and view submission history |

---

## Editor / Admin Access

- Log in with a superuser account created in step 6.
- The **Editor Panel** link appears in the navbar for staff/superuser accounts.
- In the editor panel you can **Approve** or **Reject** pending posts.
- You can also manage everything via Django Admin at `/admin/`.

---

## Project Structure

```
medethics/
├── blog/                   # Main app (posts, categories)
│   ├── migrations/
│   ├── static/blog/
│   │   └── main.css        # All custom styles (dark academia theme)
│   ├── templates/blog/
│   │   ├── base.html       # Base template with navbar, footer, particles
│   │   ├── home.html
│   │   ├── approved_posts.html
│   │   ├── post_detail.html
│   │   ├── create_post.html
│   │   ├── delete_post.html
│   │   ├── editor_panel.html
│   │   └── category_posts.html
│   ├── models.py           # Post, Category
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── users/                  # User auth and profiles app
│   ├── migrations/
│   ├── templates/users/
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── logout.html
│   │   └── profile.html
│   ├── models.py           # Profile (extends User)
│   ├── forms.py
│   ├── views.py
│   └── signals.py          # Auto-create Profile on user save
├── ethics_project/
│   ├── settings.py
│   └── urls.py
├── db.sqlite3
├── manage.py
├── setup_data.py
└── README.md
```

---

## Database Models

### Category
| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | e.g. "Films" |
| `slug` | SlugField | e.g. "films" (used in URLs) |

### Post
| Field | Type | Description |
|-------|------|-------------|
| `title` | CharField | Post title |
| `content` | TextField | Body text (optional if link provided) |
| `link` | URLField | External link (optional) |
| `category` | ForeignKey → Category | Post category |
| `author` | ForeignKey → User | Submitting user |
| `created_at` | DateTimeField | Submission timestamp |
| `status` | CharField | `pending` / `approved` / `rejected` |
| `reviewed_by` | ForeignKey → User | Editor who reviewed |
| `reviewed_at` | DateTimeField | Review timestamp |

### Profile
| Field | Type | Description |
|-------|------|-------------|
| `user` | OneToOneField → User | Linked user |
| `bio` | TextField | Optional biography |

---

## Technology Stack

| Technology | Usage |
|------------|-------|
| Python 3.x | Backend language |
| Django 4.x / 5.x | Web framework |
| SQLite | Database |
| HTML5 / CSS3 | Templates and styling |
| JavaScript (Vanilla) | Dark mode, particles, toast init |
| Bootstrap 5.3 | Layout and UI components |
| Bootstrap Icons | Icon set |
| Google Fonts | Playfair Display + DM Sans |
| Unsplash (CDN) | Background photography |

---

## Bonus Features Implemented

- **Search** — full-text search by title and content
- **Filter by category** — on the Browse Posts page
- **User profile page** — edit info, view post history with approval statuses
- **Dark mode** — toggleable, saved to localStorage, respects system preference
- **Editor panel** — shows pending, approved, and rejected posts

---

## Notes

- The database file (`db.sqlite3`) is included. It may or may not contain test data.
- If the database is empty, run the setup steps above to create categories and a superuser.
- Static files are served by Django's development server (`DEBUG=True`). For production, `collectstatic` would be required.
