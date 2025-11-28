# Attendance Management System - Setup Instructions

This project consists of a FastAPI backend with MongoDB and a React frontend. All components are now fully connected and working with MongoDB.

## Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB (local installation or MongoDB Atlas)
- Git

## Backend Setup (FastAPI + MongoDB)

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the backend directory:
```env
MONGO_URL=mongodb://localhost:27017/
MONGO_DB=attendance_system
JWT_SECRET=your_super_secret_key_change_this_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Start MongoDB
Make sure MongoDB is running on your system:
- **Windows**: Start MongoDB service or run `mongod`
- **macOS**: `brew services start mongodb-community`
- **Linux**: `sudo systemctl start mongod`

### 5. Run the Backend Server
```bash
python run.py
```

The backend will be available at `http://localhost:8080`

### 6. Seed Sample Data (Optional)
Once the backend is running, you can seed sample data by making a POST request to:
```
POST http://localhost:8080/seed_data
```

Or use the frontend to seed data through the API.

## Frontend Setup (React + Vite)

### 1. Navigate to Frontend Directory
```bash
cd vivid-learner-portal
```

### 2. Install Node Dependencies
```bash
npm install
```

### 3. Set Up Environment Variables
Create a `.env` file in the vivid-learner-portal directory:
```env
VITE_FASTAPI_BASE_URL=http://localhost:8080
```

### 4. Start the Frontend Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Database Schema

The MongoDB database uses the following collections:

### 1. `users` - User authentication
```json
{
  "_id": "ObjectId",
  "email": "string",
  "hashed_password": "string",
  "user_type": "student|staff|hod|principal",
  "admission_no": "string (optional)",
  "disabled": "boolean",
  "created_at": "datetime"
}
```

### 2. `students` - Student records
```json
{
  "_id": "ObjectId",
  "admission_no": "string",
  "name": "string",
  "student_id": "string",
  "class_name": "string",
  "section": "string",
  "created_at": "datetime"
}
```

### 3. `attendance` - Attendance records
```json
{
  "_id": "ObjectId",
  "admission_no": "string",
  "year": "number",
  "month": "number",
  "date": "number",
  "attendance": {
    "morning": "Present|Absent|NA",
    "evening": "Present|Absent|NA"
  },
  "updatedBy": "string",
  "lastUpdatedAt": "datetime",
  "is_manual": "boolean"
}
```

### 4. `credits` - Manual attendance credits
```json
{
  "_id": "ObjectId",
  "admission_no": "string",
  "year": "number",
  "month": "number",
  "used": "number",
  "limit": "number"
}
```

## API Endpoints

### Authentication
- `POST /token` - Login and get JWT token
- `POST /users/` - Create new user account

### Student Management
- `GET /students/` - Get all students
- `GET /students/{admission_no}` - Get student by admission number
- `POST /students/` - Create new student

### Attendance
- `POST /auto_attendance` - Mark automatic attendance
- `POST /manual_attendance` - Mark manual attendance
- `GET /view_attendance/{admission_no}` - View student attendance records

### Dashboards
- `GET /staff_dashboard/{class_name}` - Staff dashboard for class
- `GET /hod_dashboard/{class_name}` - HOD dashboard for class
- `GET /staff_actions/{admission_no}` - Staff actions for student

### Utilities
- `GET /health` - Health check
- `POST /seed_data` - Seed sample data

## Frontend Features

### 1. Dashboard
- Real-time statistics from MongoDB
- Recent activity feed
- Quick actions with refresh functionality
- Responsive design with animations

### 2. Attendance Tracking
- Mark automatic and manual attendance
- View real-time attendance data
- Filter by class and date
- Integration with MongoDB backend

### 3. Student Management
- Add new students
- View all students in a table
- Search and filter functionality
- View individual student attendance

### 4. Reports
- Real-time analytics from MongoDB
- Class performance reports
- Attendance trends
- Export functionality

### 5. Authentication
- JWT-based authentication
- Role-based access control
- Secure token management

## Default Login Credentials

After seeding data, you can use these credentials:

- **Student**: `student@demo.com` / `password123`
- **HOD**: `hod@demo.com` / `password123`

## Troubleshooting

### Backend Issues
1. **MongoDB Connection Error**: Ensure MongoDB is running and the connection string is correct
2. **Port Already in Use**: Change the port in `run.py` or kill the process using port 8080
3. **Module Not Found**: Ensure all dependencies are installed with `pip install -r requirements.txt`

### Frontend Issues
1. **API Connection Error**: Check if the backend is running and the API URL is correct
2. **Build Errors**: Clear node_modules and reinstall with `rm -rf node_modules && npm install`
3. **CORS Issues**: The backend is configured to allow CORS from the frontend URL

### Database Issues
1. **Empty Collections**: Run the seed data endpoint to populate sample data
2. **Connection Timeout**: Check MongoDB service status and network connectivity

## Development

### Backend Development
- The backend uses FastAPI with automatic API documentation
- Visit `http://localhost:8080/docs` for interactive API documentation
- All endpoints are properly typed with Pydantic models

### Frontend Development
- Built with React 18, TypeScript, and Vite
- Uses Tailwind CSS for styling
- Components are built with Radix UI primitives
- State management with React Context

## Production Deployment

### Backend
1. Set production environment variables
2. Use a production WSGI server like Gunicorn
3. Set up proper MongoDB authentication
4. Use a reverse proxy like Nginx

### Frontend
1. Build the production bundle: `npm run build`
2. Serve static files with a web server
3. Configure environment variables for production API URL

## Security Considerations

1. Change default JWT secret in production
2. Use HTTPS in production
3. Implement proper MongoDB authentication
4. Add rate limiting to API endpoints
5. Validate all input data
6. Use environment variables for sensitive data

## Support

For issues or questions:
1. Check the console logs for error messages
2. Verify all services are running
3. Check network connectivity between frontend and backend
4. Ensure MongoDB is accessible

The system is now fully functional with MongoDB integration and all features working as expected!
