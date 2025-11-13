# NutriLift Project - All Pages & Testing Plan

## Project Overview
This is a Django-based nutrition screening application for schools. The system allows teachers to screen students for nutritional risk and manage the data.

---

## All Available Pages/Endpoints

### 1. System/Public Endpoints

#### `/health/`
- **Type**: JSON API endpoint
- **Method**: GET
- **Authentication**: None required
- **Description**: Health check endpoint
- **Expected Response**: `{"ok": true}`

#### `/admin/` (Django Admin Interface)
- **Type**: Web interface
- **Method**: GET/POST
- **Authentication**: Staff/Superuser required
- **Description**: Django admin panel for managing all models
- **Sub-pages**:
  - `/admin/accounts/user/` - User management
  - `/admin/accounts/organization/` - Organization management
  - `/admin/accounts/orgmembership/` - Organization membership management
  - `/admin/roster/classroom/` - Classroom management
  - `/admin/roster/guardian/` - Guardian management
  - `/admin/roster/student/` - Student management
  - `/admin/roster/studentguardian/` - Student-Guardian relationship management
  - `/admin/screening/screening/` - Screening management
  - `/admin/audit/auditlog/` - Audit log management

### 2. Authentication & User Info

#### `/whoami/`
- **Type**: JSON API endpoint
- **Method**: GET
- **Authentication**: Required (SAPA_ADMIN, ORG_ADMIN, or superuser)
- **Description**: Returns current user information
- **Expected Response**: 
  ```json
  {
    "email": "user@example.com",
    "roles": ["TEACHER"],
    "active_org": "School Name"
  }
  ```

### 3. Screening Application Pages

#### `/screening/teacher/`
- **Type**: Web page (HTML)
- **Method**: GET
- **Authentication**: Required (TEACHER, ORG_ADMIN, or superuser)
- **Organization Context**: Required
- **Description**: Teacher portal showing list of students with filtering options
- **Query Parameters**:
  - `classroom` - Filter by classroom ID
  - `risk` - Filter by risk level (GREEN, AMBER, RED)
  - `q` - Search by student name
- **Features**:
  - Lists all students in the organization
  - Shows last risk level for each student
  - Filter by classroom, risk level, or search by name
  - Link to create screening for each student

#### `/screening/teacher/screen/<student_id>/`
- **Type**: Web form (HTML)
- **Method**: GET (form) / POST (submit)
- **Authentication**: Required (TEACHER, ORG_ADMIN, or superuser)
- **Organization Context**: Required
- **Description**: Screening form to create a new screening for a student
- **Form Fields**:
  - Height (cm)
  - Weight (kg)
  - Age (years)
  - Gender (M/F/O)
  - Low income status (checkbox)
  - Parent WhatsApp Number (optional)
  - MCQ Questions (5 checkboxes):
    - Diet diversity low
    - Symptom: weight loss
    - Symptom: fatigue
    - Symptom: recurrent illness
    - Symptom: hair/skin issues
- **On Submit**: Creates screening, computes risk level, redirects to result page

#### `/screening/teacher/result/<screening_id>/`
- **Type**: Web page (HTML)
- **Method**: GET
- **Authentication**: Required (TEACHER, ORG_ADMIN, or superuser)
- **Organization Context**: Required
- **Description**: Displays screening result with risk level and action links
- **Features**:
  - Shows screening details (risk level, red flags)
  - Provides WhatsApp links for:
    - Education message (always available if guardian phone exists)
    - Assistance message (only if low income)

#### `/screening/admin/export/screenings.csv`
- **Type**: CSV file download
- **Method**: GET
- **Authentication**: Required (ORG_ADMIN, INDITECH, or superuser)
- **Organization Context**: Required
- **Description**: Exports screenings data as CSV
- **Query Parameters**:
  - `since` - ISO date format (default: last 6 months)
- **CSV Columns**:
  - Screened At, Student Name, Gender, Age, Classroom, Parent Phone, Height, Weight, BMI, Risk, Red Flags

---

## Step-by-Step Testing Plan

### Prerequisites Setup

1. **Start the Django development server**
   ```bash
   cd backend
   python manage.py runserver
   ```
   Server should be running at `http://127.0.0.1:8000/` (or configured port)

2. **Create test data** (if not already exists):
   - Create a superuser: `python manage.py createsuperuser`
   - Create an Organization via admin
   - Create a User and assign OrgMembership with TEACHER or ORG_ADMIN role
   - Create a Classroom
   - Create a Student
   - Optionally create a Guardian

---

### Phase 1: System Health & Admin Access

#### Test 1.1: Health Check Endpoint
1. **URL**: `http://127.0.0.1:8000/health/`
2. **Method**: GET
3. **Expected**: 
   - Status: 200 OK
   - Response: `{"ok": true}`
4. **Notes**: No authentication required

#### Test 1.2: Admin Login
1. **URL**: `http://127.0.0.1:8000/admin/`
2. **Action**: Login with superuser credentials
3. **Expected**: 
   - Admin dashboard loads
   - All model sections visible in sidebar

#### Test 1.3: Admin - User Management
1. **URL**: `http://127.0.0.1:8000/admin/accounts/user/`
2. **Actions**:
   - View list of users
   - Click "Add user" to create new user
   - Test search functionality
3. **Expected**: Users list displays, can create/edit users

#### Test 1.4: Admin - Organization Management
1. **URL**: `http://127.0.0.1:8000/admin/accounts/organization/`
2. **Actions**:
   - View organizations
   - Create new organization (name, org_type, city, state, country)
   - Edit existing organization
3. **Expected**: Organizations can be created and managed

#### Test 1.5: Admin - OrgMembership Management
1. **URL**: `http://127.0.0.1:8000/admin/accounts/orgmembership/`
2. **Actions**:
   - Create membership linking user to organization with role
   - Test roles: TEACHER, ORG_ADMIN, SAPA_ADMIN, INDITECH
3. **Expected**: Memberships can be created and assigned roles

#### Test 1.6: Admin - Classroom Management
1. **URL**: `http://127.0.0.1:8000/admin/roster/classroom/`
2. **Actions**:
   - Create classroom (organization, grade, division)
   - Test unique constraint (same org, grade, division)
3. **Expected**: Classrooms can be created per organization

#### Test 1.7: Admin - Guardian Management
1. **URL**: `http://127.0.0.1:8000/admin/roster/guardian/`
2. **Actions**:
   - Create guardian (organization, full_name, phone_e164, whatsapp_opt_in)
   - Test unique constraint (same org, phone)
3. **Expected**: Guardians can be created

#### Test 1.8: Admin - Student Management
1. **URL**: `http://127.0.0.1:8000/admin/roster/student/`
2. **Actions**:
   - Create student (organization, classroom, first_name, last_name, gender, dob, student_code, is_low_income, primary_guardian)
   - Test search by name or student_code
3. **Expected**: Students can be created and linked to classrooms/guardians

#### Test 1.9: Admin - StudentGuardian Management
1. **URL**: `http://127.0.0.1:8000/admin/roster/studentguardian/`
2. **Actions**:
   - Create relationship (student, guardian, relationship type)
3. **Expected**: Relationships can be created

#### Test 1.10: Admin - Screening Management
1. **URL**: `http://127.0.0.1:8000/admin/screening/screening/`
2. **Actions**:
   - View existing screenings
   - Filter by organization, risk_level, screened_at
   - Search by student name
3. **Expected**: Screenings list with filters work

#### Test 1.11: Admin - AuditLog Management
1. **URL**: `http://127.0.0.1:8000/admin/audit/auditlog/`
2. **Actions**:
   - View audit logs
   - Filter by organization, action
   - Search by target_id, actor email, organization name
3. **Expected**: Audit logs display correctly

---

### Phase 2: Authentication & API Endpoints

#### Test 2.1: Whoami Endpoint (Unauthenticated)
1. **URL**: `http://127.0.0.1:8000/whoami/`
2. **Method**: GET (without login)
3. **Expected**: 
   - Status: 403 Forbidden or redirect to login
   - Error message about authentication

#### Test 2.2: Whoami Endpoint (Authenticated - Teacher)
1. **URL**: `http://127.0.0.1:8000/whoami/`
2. **Method**: GET (logged in as user with TEACHER role)
3. **Expected**: 
   - Status: 200 OK
   - JSON response with email, roles array, active_org
4. **Note**: Requires organization context (set via middleware)

#### Test 2.3: Whoami Endpoint (Authenticated - Org Admin)
1. **URL**: `http://127.0.0.1:8000/whoami/`
2. **Method**: GET (logged in as user with ORG_ADMIN role)
3. **Expected**: Same as Test 2.2

---

### Phase 3: Screening Application - Teacher Portal

#### Test 3.1: Teacher Portal (Unauthenticated)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/`
2. **Method**: GET (not logged in)
3. **Expected**: 
   - Status: 403 Forbidden or redirect to login
   - Error about authentication/role

#### Test 3.2: Teacher Portal (Authenticated - No Org Context)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/`
2. **Method**: GET (logged in but no organization context)
3. **Expected**: 
   - Status: 403 Forbidden
   - Error: "Organization context required."

#### Test 3.3: Teacher Portal (Authenticated - With Org Context)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/`
2. **Method**: GET (logged in as TEACHER with organization context)
3. **Expected**: 
   - Status: 200 OK
   - Page displays:
     - Filter form (classroom dropdown, risk dropdown, search box)
     - Table with students (Name, Class, Last risk, Action column)
     - "Fill a Screening" link for each student

#### Test 3.4: Teacher Portal - Filter by Classroom
1. **URL**: `http://127.0.0.1:8000/screening/teacher/?classroom=<classroom_id>`
2. **Method**: GET
3. **Expected**: 
   - Only students from selected classroom displayed
   - Selected classroom highlighted in dropdown

#### Test 3.5: Teacher Portal - Filter by Risk Level
1. **URL**: `http://127.0.0.1:8000/screening/teacher/?risk=RED`
2. **Method**: GET
3. **Test variations**: `risk=GREEN`, `risk=AMBER`, `risk=RED`
4. **Expected**: 
   - Only students with selected risk level displayed
   - Selected risk highlighted in dropdown

#### Test 3.6: Teacher Portal - Search by Name
1. **URL**: `http://127.0.0.1:8000/screening/teacher/?q=John`
2. **Method**: GET
3. **Expected**: 
   - Only students with "John" in first_name or last_name displayed
   - Search box retains query value

#### Test 3.7: Teacher Portal - Combined Filters
1. **URL**: `http://127.0.0.1:8000/screening/teacher/?classroom=<id>&risk=AMBER&q=test`
2. **Method**: GET
3. **Expected**: 
   - Filters combine correctly (AND logic)
   - All filter values retained in form

#### Test 3.8: Teacher Portal - Empty Results
1. **URL**: `http://127.0.0.1:8000/screening/teacher/?q=NonexistentStudent`
2. **Method**: GET
3. **Expected**: 
   - Message: "No students yet" in table
   - Page still loads correctly

---

### Phase 4: Screening Application - Create Screening

#### Test 4.1: Screening Form (Unauthenticated)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/screen/<student_id>/`
2. **Method**: GET (not logged in)
3. **Expected**: 403 Forbidden or redirect to login

#### Test 4.2: Screening Form (Wrong Organization)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/screen/<student_id>/`
2. **Method**: GET (student belongs to different org)
3. **Expected**: 404 Not Found (student not found in user's org)

#### Test 4.3: Screening Form (Valid Access)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/screen/<student_id>/`
2. **Method**: GET (logged in, student in same org)
3. **Expected**: 
   - Status: 200 OK
   - Form displays with fields:
     - Height (cm)
     - Weight (kg)
     - Age (years)
     - Gender (pre-filled from student)
     - Low income checkbox (pre-filled from student)
     - Parent WhatsApp Number
     - 5 MCQ checkboxes
   - Student name visible on page

#### Test 4.4: Screening Form - Submit Valid Data (GREEN Risk)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/screen/<student_id>/`
2. **Method**: POST
3. **Data**:
   - height_cm: 120
   - weight_kg: 25
   - age_years: 8
   - gender: M
   - is_low_income_at_screen: false
   - parent_phone_e164: +911234567890 (optional)
   - All MCQ checkboxes: unchecked
4. **Expected**: 
   - Status: 302 Redirect
   - Redirects to `/screening/teacher/result/<screening_id>/`
   - Screening created with risk_level = GREEN
   - Audit log entry created

#### Test 4.5: Screening Form - Submit Valid Data (AMBER Risk)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/screen/<student_id>/`
2. **Method**: POST
3. **Data**: Similar to Test 4.4, but with some MCQ checkboxes checked
4. **Expected**: 
   - Risk level computed as AMBER
   - Red flags populated based on answers

#### Test 4.6: Screening Form - Submit Valid Data (RED Risk)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/screen/<student_id>/`
2. **Method**: POST
3. **Data**: Multiple red flags checked, extreme measurements
4. **Expected**: 
   - Risk level computed as RED
   - Multiple red flags in red_flags array

#### Test 4.7: Screening Form - Create Guardian from Phone
1. **URL**: `http://127.0.0.1:8000/screening/teacher/screen/<student_id>/`
2. **Method**: POST
3. **Data**: Include `parent_phone_e164: +911234567890`
4. **Expected**: 
   - Guardian created or linked if phone exists
   - Student's primary_guardian set if not already set

#### Test 4.8: Screening Form - Invalid Data
1. **URL**: `http://127.0.0.1:8000/screening/teacher/screen/<student_id>/`
2. **Method**: POST
3. **Data**: Missing required fields or invalid values
4. **Expected**: 
   - Form displays with validation errors
   - No screening created

---

### Phase 5: Screening Application - View Result

#### Test 5.1: Screening Result (Unauthenticated)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/result/<screening_id>/`
2. **Method**: GET (not logged in)
3. **Expected**: 403 Forbidden

#### Test 5.2: Screening Result (Wrong Organization)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/result/<screening_id>/`
2. **Method**: GET (screening from different org)
3. **Expected**: 404 Not Found

#### Test 5.3: Screening Result (Valid Access - With Guardian)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/result/<screening_id>/`
2. **Method**: GET
3. **Expected**: 
   - Status: 200 OK
   - Displays:
     - Student name
     - Risk level (GREEN/AMBER/RED)
     - Red flags list
     - Education WhatsApp link (if guardian phone exists)
     - Assistance WhatsApp link (if low income AND guardian phone exists)

#### Test 5.4: Screening Result (No Guardian)
1. **URL**: `http://127.0.0.1:8000/screening/teacher/result/<screening_id>/`
2. **Method**: GET (screening for student without guardian)
3. **Expected**: 
   - WhatsApp links are empty/not displayed
   - Other information still displays

#### Test 5.5: Screening Result - WhatsApp Link Format
1. **URL**: `http://127.0.0.1:8000/screening/teacher/result/<screening_id>/`
2. **Method**: GET
3. **Expected**: 
   - Education link format: `https://wa.me/911234567890/?text=...`
   - Assistance link format: `https://wa.me/911234567890/?text=...`
   - Links contain pre-filled messages with screening details

---

### Phase 6: Screening Application - Export CSV

#### Test 6.1: Export CSV (Unauthenticated)
1. **URL**: `http://127.0.0.1:8000/screening/admin/export/screenings.csv`
2. **Method**: GET (not logged in)
3. **Expected**: 403 Forbidden

#### Test 6.2: Export CSV (Wrong Role - Teacher)
1. **URL**: `http://127.0.0.1:8000/screening/admin/export/screenings.csv`
2. **Method**: GET (logged in as TEACHER)
3. **Expected**: 403 Forbidden (requires ORG_ADMIN, INDITECH, or superuser)

#### Test 6.3: Export CSV (Valid Access - Default)
1. **URL**: `http://127.0.0.1:8000/screening/admin/export/screenings.csv`
2. **Method**: GET (logged in as ORG_ADMIN)
3. **Expected**: 
   - Status: 200 OK
   - Content-Type: text/csv
   - Content-Disposition: attachment; filename="screenings.csv"
   - CSV contains last 6 months of screenings
   - Headers: Screened At, Student Name, Gender, Age, Classroom, Parent Phone, Height, Weight, BMI, Risk, Red Flags

#### Test 6.4: Export CSV - With Date Filter
1. **URL**: `http://127.0.0.1:8000/screening/admin/export/screenings.csv?since=2024-01-01T00:00:00`
2. **Method**: GET
3. **Expected**: 
   - Only screenings from 2024-01-01 onwards included
   - CSV format correct

#### Test 6.5: Export CSV - Invalid Date Format
1. **URL**: `http://127.0.0.1:8000/screening/admin/export/screenings.csv?since=invalid-date`
2. **Method**: GET
3. **Expected**: 
   - Falls back to default (last 6 months)
   - No error, CSV still generated

#### Test 6.6: Export CSV - Empty Results
1. **URL**: `http://127.0.0.1:8000/screening/admin/export/screenings.csv?since=2099-01-01T00:00:00`
2. **Method**: GET (no future screenings)
3. **Expected**: 
   - CSV with headers only
   - No data rows

#### Test 6.7: Export CSV - BMI Calculation
1. **URL**: `http://127.0.0.1:8000/screening/admin/export/screenings.csv`
2. **Method**: GET
3. **Expected**: 
   - BMI calculated correctly: weight_kg / (height_cm/100)²
   - BMI rounded to 1 decimal place
   - Empty BMI if height/weight missing

#### Test 6.8: Export CSV - Audit Log
1. **URL**: `http://127.0.0.1:8000/screening/admin/export/screenings.csv`
2. **Method**: GET
3. **Expected**: 
   - Audit log entry created with action "CSV_EXPORTED"
   - Payload includes count of exported screenings

---

### Phase 7: Integration & Edge Cases

#### Test 7.1: Complete Screening Workflow
1. Login as TEACHER
2. Navigate to `/screening/teacher/`
3. Filter/search for a student
4. Click "Fill a Screening" link
5. Fill out screening form with all fields
6. Submit form
7. Verify redirect to result page
8. Verify result page displays correctly
9. Verify WhatsApp links work (if guardian exists)
10. Return to teacher portal and verify student's last risk updated

#### Test 7.2: Multiple Screenings for Same Student
1. Create first screening for a student (GREEN)
2. Create second screening for same student (RED)
3. Verify teacher portal shows latest risk (RED)
4. Verify both screenings exist in admin

#### Test 7.3: Organization Isolation
1. Create two organizations (Org A, Org B)
2. Create students in each org
3. Login as user with access to Org A only
4. Verify cannot access Org B's students/screenings
5. Verify admin filters by organization correctly

#### Test 7.4: Role-Based Access Control
1. Test TEACHER role:
   - Can access teacher portal ✓
   - Can create screenings ✓
   - Cannot export CSV ✗
2. Test ORG_ADMIN role:
   - Can access teacher portal ✓
   - Can create screenings ✓
   - Can export CSV ✓
3. Test SAPA_ADMIN role:
   - Can access whoami ✓
   - Can access admin ✓
4. Test INDITECH role:
   - Can export CSV ✓

#### Test 7.5: Data Validation
1. Test screening form with:
   - Negative height/weight
   - Extremely large values
   - Invalid phone format
   - Missing required fields
2. Verify appropriate validation errors

#### Test 7.6: Search Functionality
1. Test teacher portal search with:
   - First name only
   - Last name only
   - Full name
   - Partial match
   - Case insensitive
   - Special characters
2. Verify all work correctly

---

## Testing Checklist Summary

### ✅ System Endpoints
- [ ] Health check endpoint
- [ ] Admin login and all admin pages
- [ ] Whoami endpoint (various roles)

### ✅ Screening Application
- [ ] Teacher portal (list, filters, search)
- [ ] Create screening form (GET and POST)
- [ ] View screening result
- [ ] Export CSV

### ✅ Data Management
- [ ] Create organizations
- [ ] Create users and memberships
- [ ] Create classrooms
- [ ] Create students
- [ ] Create guardians
- [ ] Create screenings

### ✅ Security & Access Control
- [ ] Authentication required
- [ ] Role-based access
- [ ] Organization isolation
- [ ] CSRF protection

### ✅ Edge Cases
- [ ] Empty results
- [ ] Invalid data
- [ ] Missing relationships
- [ ] Multiple screenings
- [ ] Date filtering

---

## Notes for Testing

1. **Base URL**: Default is `http://127.0.0.1:8000/` - adjust if using different port
2. **Admin URL**: Default is `/admin/` - can be changed via `ADMIN_URL` environment variable
3. **Organization Context**: Many endpoints require organization context set via middleware
4. **Authentication**: Use Django's session-based authentication (login via admin or custom login)
5. **Test Data**: Ensure sufficient test data exists before testing filtering/search features
6. **CSRF**: Forms require CSRF tokens - ensure cookies are enabled in browser/testing tool

---

## Quick Test Commands

```bash
# Health check
curl http://127.0.0.1:8000/health/

# Whoami (requires authentication)
curl -b cookies.txt -c cookies.txt http://127.0.0.1:8000/whoami/

# Export CSV (requires authentication and role)
curl -b cookies.txt http://127.0.0.1:8000/screening/admin/export/screenings.csv -o screenings.csv
```

---

**Last Updated**: Based on current codebase analysis
**Total Pages Identified**: 20+ unique endpoints/pages



