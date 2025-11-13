# NutriLift - All Available Pages Quick Reference

## Public/System Pages

| URL | Method | Auth Required | Description |
|-----|--------|---------------|-------------|
| `/health/` | GET | No | Health check endpoint - returns `{"ok": true}` |
| `/admin/` | GET/POST | Staff/Superuser | Django admin interface |

## API Endpoints

| URL | Method | Auth Required | Roles | Description |
|-----|--------|---------------|-------|-------------|
| `/whoami/` | GET | Yes | SAPA_ADMIN, ORG_ADMIN, Superuser | Returns user info (email, roles, active_org) |

## Screening Application Pages

| URL | Method | Auth Required | Roles | Org Context | Description |
|-----|--------|---------------|-------|-------------|-------------|
| `/screening/teacher/` | GET | Yes | TEACHER, ORG_ADMIN, Superuser | Required | Teacher portal - list students with filters |
| `/screening/teacher/screen/<student_id>/` | GET/POST | Yes | TEACHER, ORG_ADMIN, Superuser | Required | Create new screening form |
| `/screening/teacher/result/<screening_id>/` | GET | Yes | TEACHER, ORG_ADMIN, Superuser | Required | View screening result with WhatsApp links |
| `/screening/admin/export/screenings.csv` | GET | Yes | ORG_ADMIN, INDITECH, Superuser | Required | Export screenings as CSV |

## Django Admin Pages

All admin pages require staff/superuser authentication and are accessible at `/admin/`:

### Accounts App
- `/admin/accounts/user/` - User management
- `/admin/accounts/organization/` - Organization management
- `/admin/accounts/orgmembership/` - Organization membership management

### Roster App
- `/admin/roster/classroom/` - Classroom management
- `/admin/roster/guardian/` - Guardian management
- `/admin/roster/student/` - Student management
- `/admin/roster/studentguardian/` - Student-Guardian relationship management

### Screening App
- `/admin/screening/screening/` - Screening management

### Audit App
- `/admin/audit/auditlog/` - Audit log management

## Query Parameters

### Teacher Portal (`/screening/teacher/`)
- `classroom` - Filter by classroom ID (integer)
- `risk` - Filter by risk level: `GREEN`, `AMBER`, or `RED`
- `q` - Search by student name (string)

### Export CSV (`/screening/admin/export/screenings.csv`)
- `since` - ISO date format (e.g., `2024-01-01T00:00:00`) - defaults to last 6 months

## Role Definitions

- **SAPA_ADMIN**: System administrator
- **ORG_ADMIN**: Organization administrator
- **TEACHER**: Teacher role
- **INDITECH**: Inditech role
- **Superuser**: Django superuser (bypasses role checks)

## Organization Context

Many endpoints require organization context, which is set via the `CurrentOrganizationMiddleware`. Users must have an active organization membership to access organization-scoped endpoints.

## Total Count

- **Public/System**: 2 pages
- **API Endpoints**: 1 endpoint
- **Screening Application**: 4 pages
- **Admin Pages**: 9 model admin pages
- **Total**: 16+ unique pages/endpoints



