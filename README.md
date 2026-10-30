# Scrumptious

Scrumptious is a Kanban project management web application built for FIT2101 (Software Process and Management) at Monash University during Semester 2, 2026. The application allows software teams to plan sprints, track tasks across customizable columns, manage roles and permissions, and monitor velocity with burndown charts.

## Overview

The application was developed by Team 09 (Thursday 5:00 PM tutorial) to demonstrate agile software engineering practices, test-driven development, and continuous integration.

Key capabilities include:
* Interactive Kanban boards with drag-and-drop task movements and quick transition controls
* Role-based access control distinguishing between Scrum Masters, Project Leaders, and Developers
* Task details supporting Fibonacci story points, due dates, priority tags, subtask checklists, and multi-assignee allocations
* Sprint tracking with task completion timestamps, velocity metrics, and burndown chart visualization
* Task audit trails with an activity log and discussion comment threads
* Authentication with email verification, password reset, and optional TOTP two-factor authentication
* In-app notification center for project events, invitations, and task assignments
* User interface supporting high-contrast light and dark themes complying with WCAG AA guidelines

## Architecture

The system uses a decoupled client-server architecture:

```
scrumptious/
├── app.py                     # Flask entry point and blueprint registrations
├── config.py                  # Supabase client setup (service role and anon keys)
├── auth_utils.py              # Authentication decorators (@login_required, @require_role)
├── activity.py                # Activity log recorder and query helpers
├── notifications_utils.py     # Notification event dispatcher
├── routes/
│   ├── auth.py                # Registration, login, 2FA, password recovery
│   ├── projects.py            # Project CRUD, memberships, and role assignments
│   ├── columns.py             # Column creation, reordering, and deletion
│   ├── tasks.py               # Task management, assignees, and completion state
│   └── notifications.py       # In-app notifications retrieval and updates
├── static/
│   ├── css/                   # Stylesheets (style.css, notifications.css)
│   └── js/                    # Client logic (api.js, board.js, notification.js, toast.js)
├── supabase/
│   └── schema.sql             # PostgreSQL schema and table definitions
├── tests/                     # Automated test suites
├── index.html                 # Login and registration view
├── board.html                 # Main Kanban workspace view
└── reset-password.html        # Password reset handler view
```

### Backend design and security
The backend is built in Python using Flask and structured into modular blueprints. Data storage and authentication are handled through Supabase (PostgreSQL).

Rather than querying the database directly from client-side JavaScript, all client requests are mediated through Flask API endpoints. The backend connects to Supabase using the service role key and explicitly validates user identities and role permissions on every request using custom decorators (`@login_required` and `@require_role`). This keeps database credentials server-side and prevents client bypass of business rules.

### Frontend design
The frontend is written in vanilla JavaScript (ES6+) and standard CSS, without third-party frameworks or bundlers. This keeps the asset payload small and allows the project to run directly from the Flask static file server without a Node.js build step.

## Setup and Installation

### Prerequisites
* Python 3.11 or newer
* A Supabase project instance

### 1. Clone the repository
```bash
git clone https://github.com/nav6x/scrumptious.git
cd scrumptious
```

### 2. Set up a virtual environment
On macOS and Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Environment variables
Create a `.env` file in the project root:
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
SUPABASE_ANON_KEY=your-supabase-anon-key
FLASK_ENV=development
```
You can obtain your project URL and keys from the **Project Settings -> API** section of your Supabase dashboard.

### 4. Database initialization
In your Supabase project SQL Editor, run the script provided in `supabase/schema.sql`. This creates the required tables:
* `profiles` (user accounts and preferences)
* `projects` and `project_members` (workspaces and assigned roles)
* `columns` (board swimlanes)
* `tasks` and `task_assignees` (work items and assignments)
* `activity_logs` (audit history)
* `notifications` (system and user alerts)

### 5. Run the application
```bash
python app.py
```
The server starts locally at `http://127.0.0.1:5000`.

## Testing

Automated tests are written with `pytest` and execute integration assertions against Flask route handlers and test database fixtures:

```bash
# Run all tests
pytest -v

# Run with coverage report
pytest -v --cov=. --cov-report=term-missing
```

The test suite covers route authorization, role verification, task validation boundaries, activity logging, and password reset flows, maintaining 92% statement coverage.

## API Reference

Endpoints (except `/api/auth/signup` and `/api/auth/login`) require a Bearer token in the request header:
```
Authorization: Bearer <jwt-token>
```

| Method | Route | Description |
| :--- | :--- | :--- |
| POST | `/api/auth/signup` | Register a new account |
| POST | `/api/auth/login` | Authenticate user and return session token |
| POST | `/api/auth/logout` | Terminate user session |
| POST | `/api/auth/forgot-password` | Request password recovery email |
| POST | `/api/auth/reset-password` | Set new password with recovery token |
| POST | `/api/auth/2fa/setup` | Generate TOTP secret and QR payload |
| POST | `/api/auth/2fa/verify` | Confirm and enable TOTP authentication |
| GET / POST | `/api/projects` | List joined projects or create a new project |
| GET / POST | `/api/projects/<id>/members` | List or invite members to a project |
| GET / POST | `/api/projects/<id>/columns` | Retrieve columns or add a new column |
| PATCH / DELETE | `/api/projects/<id>/columns/<col_id>` | Rename or remove a column |
| GET / POST | `/api/projects/<id>/tasks` | List project tasks or create a task |
| PATCH / DELETE | `/api/projects/<id>/tasks/<task_id>` | Update task state, assignees, or delete task |
| GET | `/api/projects/<id>/activity` | Retrieve task activity history |
| GET / PATCH | `/api/notifications` | List user notifications or mark as read |

## Team and Credits

### Development Team (Monash FIT2101 Team 09)
* **Navadarshanth Shanmugasundaram** (Student ID: 31091367, Authcate: `nsha0146`, GitHub: [@nav6x](https://github.com/nav6x))
* **Ayden Lim** (`alim0124`)
* **Nilay Kashid** (`nkas0015`)
* **Kaveen Silva** (`ksil0005`)
* **Yahye Qani** (`yqan0001`)

### Academic Accreditation
* **Institution**: Faculty of Information Technology, Monash University
* **Course**: FIT2101 Software Process and Management (Semester 2, 2026)
* **Teaching Team**: Zhiming Deng (Teaching Associate / Tutor) and the FIT2101 unit staff for course design, project specifications, and initial repository scaffolding.

### Third-Party Technologies
* [Flask](https://flask.palletsprojects.com/) by the Pallets Projects (Python web framework)
* [Supabase](https://supabase.com/) (Managed PostgreSQL database and authentication engine)
* [pytest](https://docs.pytest.org/) (Python testing framework)
* [Render](https://render.com/) (Cloud hosting and deployment infrastructure)

## License

This project was developed for academic coursework at Monash University.
