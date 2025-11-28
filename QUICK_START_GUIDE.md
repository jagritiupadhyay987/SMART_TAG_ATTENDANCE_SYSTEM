# Quick Start Guide - Attendance Management System

## 🚀 Getting Started

### Prerequisites
- Windows 10/11
- Internet connection for downloading dependencies

### Step 1: Install Python (if not already installed)
1. Double-click `python-3.11.6-amd64.exe` in the project root
2. Follow the installation wizard
3. **Important**: Check "Add Python to PATH" during installation

### Step 2: Install MongoDB
1. Double-click `mongodb-windows-x86_64-6.0.8-signed.msi`
2. Follow the installation wizard
3. Start MongoDB service:
   - Press `Win + R`, type `services.msc`
   - Find "MongoDB" service and start it
   - Or run `mongod` in command prompt

### Step 3: Start the Backend
1. Double-click `start_backend.bat`
2. Wait for the server to start (you'll see "Backend will be available at: http://localhost:8080")
3. Keep this window open

### Step 4: Seed the Database
1. Open a new command prompt
2. Double-click `seed_database.bat`
3. Wait for "Database seeded successfully!" message

### Step 5: Start the Frontend
1. Open a new command prompt
2. Navigate to the frontend directory:
   ```cmd
   cd vivid-learner-portal
   ```
3. Install dependencies:
   ```cmd
   npm install
   ```
4. Start the frontend:
   ```cmd
   npm run dev
   ```

### Step 6: Access the Application
1. Open your browser and go to `http://localhost:5173`
2. Use these credentials to login:
   - **Student**: `student@demo.com` / `password123`
   - **HOD**: `hod@demo.com` / `password123`

## 🔧 Troubleshooting

### Backend Issues
- **"Python not found"**: Make sure Python is installed and added to PATH
- **"MongoDB connection failed"**: Start MongoDB service or install MongoDB
- **Port 8080 in use**: Close other applications using port 8080

### Frontend Issues
- **"Cannot connect to server"**: Make sure backend is running on port 8080
- **Login fails**: Make sure database is seeded with sample data
- **Build errors**: Delete `node_modules` folder and run `npm install` again

### Database Issues
- **Empty collections**: Run `seed_database.bat` to populate sample data
- **Connection timeout**: Check if MongoDB service is running

## 📱 Features Available

### For HOD/Staff Users:
- **Dashboard**: Real-time statistics and overview
- **Attendance Tracking**: Mark and view attendance
- **Student Management**: Add, view, and manage students
- **Reports**: Generate attendance reports and analytics

### For Students:
- **Student Portal**: View personal attendance records

## 🛠️ Development

### Backend API Documentation
- Visit `http://localhost:8080/docs` for interactive API documentation
- All endpoints are properly documented with examples

### Frontend Development
- Built with React 18, TypeScript, and Vite
- Hot reload enabled for development
- Console logs available for debugging

## 📞 Support

If you encounter any issues:
1. Check the console logs in your browser (F12)
2. Check the backend terminal for error messages
3. Ensure all services are running (MongoDB, Backend, Frontend)
4. Try restarting all services in the correct order

## 🎯 Next Steps

Once everything is running:
1. Explore the different user roles and their capabilities
2. Try adding new students through the Student Management page
3. Mark attendance and view reports
4. Customize the system for your specific needs

The system is now fully functional with MongoDB integration!
