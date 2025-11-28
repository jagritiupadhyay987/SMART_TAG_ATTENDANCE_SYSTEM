# Attendance Management System

A comprehensive attendance management system with role-based access control, credit-based manual marking, and table views matching the provided design images.

## Features

### 🎯 Role-Based Access
- **Student View**: Students can only view their own attendance records (read-only)
- **Staff View**: Staff can view and edit attendance with credit limitations
- **HOD/Principal View**: Full access to all students in their class/section

### 📊 Table Views (Matching Design Images)
1. **Student Portal**: Personal attendance summary with date, morning/evening status
2. **Staff Portal**: Class-wide view with manual marking capabilities and credit tracking
3. **HOD/Principal Portal**: Complete class overview with all student data

### 💳 Credit System
- Each student has 4 manual marking credits per month
- Credits are consumed when staff manually marks attendance
- Automatic attendance (card scan) doesn't consume credits
- Credit exhaustion prevents further manual marking

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (local or cloud)

### Installation

1. **Clone and setup backend:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Setup frontend:**
```bash
cd vivid-learner-portal
npm install
```

3. **Start MongoDB** (if running locally)

### Running the System

1. **Start Backend (Port 8080):**
```bash
cd backend
python run.py
```

2. **Start Frontend (Port 8080):**
```bash
cd vivid-learner-portal
npm run dev
```

3. **Visit the application:**
```
http://localhost:8080
```

## 🧪 Testing

Run the test script to verify everything is working:

```bash
python test_connection.py
```

This will:
- Check backend health
- Seed sample data
- Test all API endpoints
- Verify table format matches design images

## 📡 API Endpoints

### Student Management
- `POST /students/` - Create new student
- `GET /students/` - Get all students
- `GET /students/{admission_no}` - Get specific student

### Attendance Management
- `POST /auto_attendance` - Mark automatic attendance (card scan)
- `POST /manual_attendance` - Mark manual attendance (credit-based)
- `GET /view_attendance/{admission_no}` - Student view of attendance
- `GET /staff_dashboard/{class_name}` - Staff class dashboard
- `GET /hod_dashboard/{class_name}` - HOD class dashboard
- `GET /staff_actions/{admission_no}` - Staff actions for specific student

### Utility
- `POST /seed_data` - Seed sample data for testing
- `GET /health` - Health check

## 👥 Sample Users

The system comes with pre-configured users:

| Username | Role | Access |
|----------|------|--------|
| `student1` | Student | View own records only |
| `staff1` | Staff | View/edit with credit limits |
| `hod1` | HOD | Full class access |
| `principal1` | Principal | Full class access |

## 📊 Database Structure

### Collections

1. **students**: Student information
```json
{
  "admission_no": "ADM123",
  "name": "Rahul Sharma",
  "class_name": "10-A",
  "section": "A"
}
```

2. **attendance**: Attendance records
```json
{
  "admission_no": "ADM123",
  "year": 2025,
  "month": 9,
  "date": 18,
  "attendance": {
    "morning": "Present",
    "evening": "Present"
  },
  "is_manual": false
}
```

3. **credits**: Manual marking credits
```json
{
  "admission_no": "ADM123",
  "year": 2025,
  "month": 9,
  "used": 1,
  "limit": 4
}
```

## 🎨 Frontend Integration

The frontend API service (`src/services/api.ts`) is configured to connect to the backend on port 8080 and includes methods for all the table views shown in the design images.

### Key API Methods:
- `attendanceApi.viewAttendance()` - Student portal view
- `attendanceApi.getStaffDashboard()` - Staff class dashboard
- `attendanceApi.getHodDashboard()` - HOD class dashboard
- `attendanceApi.getStaffActions()` - Staff actions view

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```
MONGO_URL=mongodb://localhost:27017/
MONGO_DB=attendance_system
```

### Port Configuration
- Backend: Port 8080 (configured in `run.py`)
- Frontend: Port 8080 (configured in `vite.config.ts`)
- API Base URL: `http://localhost:8080` (configured in `api.ts`)

## 📝 Usage Examples

### Mark Automatic Attendance
```bash
curl -X POST "http://localhost:8080/auto_attendance?admission_no=ADM123&username=staff1"
```

### Mark Manual Attendance
```bash
curl -X POST "http://localhost:8080/manual_attendance?username=staff1" \
  -H "Content-Type: application/json" \
  -d '{
    "admission_no": "ADM123",
    "date": "2025-09-21",
    "session": "morning",
    "status": "Present"
  }'
```

### Get Student View
```bash
curl "http://localhost:8080/view_attendance/ADM123?username=student1"
```

### Get Staff Dashboard
```bash
curl "http://localhost:8080/staff_dashboard/10-A?username=staff1"
```

## 🎯 Table Format Matching

The API responses are structured to match the table formats shown in the design images:

1. **Student View**: Returns student info + attendance records array
2. **Staff Dashboard**: Returns class info + students array with attendance + credits
3. **HOD Dashboard**: Same as staff but with full access
4. **Staff Actions**: Returns student info + attendance records + credit status

Each response includes the exact data structure needed to render the tables as shown in the images.
