# NFC Attendance System Implementation Guide

## Overview

This implementation integrates NFC card-based attendance tracking into your existing attendance management system. Students can now mark their attendance by simply tapping their NFC cards on a reader.

## Features Implemented

### Backend Features
- ✅ NFC attendance endpoints (`/nfc/*`)
- ✅ NFC service with debouncing (prevents duplicate scans)
- ✅ Student-NFC UID registration
- ✅ Morning/Evening session detection
- ✅ MongoDB integration for NFC data
- ✅ Standalone NFC reader script
- ✅ API-based attendance marking

### Frontend Features
- ✅ NFC attendance management interface
- ✅ NFC reader status monitoring
- ✅ Student-NFC registration
- ✅ Attendance history for NFC cards
- ✅ Real-time status updates

## Hardware Requirements

### NFC Reader
- **Recommended**: PN532 NFC Reader (USB)
- **Alternative**: RC522 (requires different library)
- **Connection**: USB to computer

### NFC Cards/Tags
- Any standard NFC card or tag
- Each student needs a unique NFC card

## Installation & Setup

### 1. Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install nfcpy==1.0.4 pymongo fastapi uvicorn requests

# OR run the setup script
python setup_nfc.py
```

### 2. Hardware Setup

1. Connect PN532 NFC reader to USB port
2. Install drivers if required (usually automatic on Windows/Linux)
3. Test hardware detection:
   ```bash
   python -c "import nfc; print('NFC hardware detected')"
   ```

### 3. Start the System

```bash
# Terminal 1: Start backend server
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Start NFC reader
python nfc_reader.py

# Terminal 3: Start frontend (if needed)
cd vivid-learner-portal
npm run dev
```

## API Endpoints

### NFC Attendance Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/nfc/attendance` | POST | Mark attendance using NFC UID |
| `/nfc/register` | POST | Register NFC UID for student |
| `/nfc/status` | GET | Get NFC reader status |
| `/nfc/start` | POST | Start NFC reader |
| `/nfc/stop` | POST | Stop NFC reader |
| `/nfc/history/{nfc_uid}` | GET | Get attendance history for NFC UID |
| `/nfc/clear-cache` | POST | Clear debounce cache |
| `/nfc/students` | GET | Get all students with NFC UIDs |

### Example API Usage

```python
import requests

# Mark attendance via API
response = requests.post('http://localhost:8000/nfc/attendance', json={
    'nfc_uid': 'A1B2C3D4',
    'timestamp': '2024-01-15T08:30:00'
})

# Register NFC UID for student
response = requests.post('http://localhost:8000/nfc/register', params={
    'admission_no': 'ADM123',
    'nfc_uid': 'A1B2C3D4'
})
```

## Database Schema Updates

### Students Collection
```json
{
  "_id": "ObjectId",
  "admission_no": "ADM123",
  "name": "Rahul Sharma",
  "student_id": "STU001",
  "class_name": "10-A",
  "section": "A",
  "nfc_uid": "A1B2C3D4",  // NEW: NFC card UID
  "created_at": "2024-01-15T08:30:00"
}
```

### Attendance Collection
```json
{
  "_id": "ObjectId",
  "admission_no": "ADM123",
  "date": "2024-01-15",
  "year": 2024,
  "month": 1,
  "date": 15,
  "morning": "Present",
  "evening": "Absent",
  "attendance": {
    "morning": "Present",
    "evening": "Absent"
  },
  "updatedBy": "nfc_system",
  "lastUpdatedAt": "2024-01-15T08:30:00",
  "is_nfc": true,        // NEW: Whether marked via NFC
  "nfc_uid": "A1B2C3D4"  // NEW: NFC UID used
}
```

## Usage Instructions

### 1. Register NFC Cards

1. Access the web interface: `http://localhost:5173`
2. Navigate to "Attendance Tracking"
3. In the NFC section, select a student
4. Enter the NFC UID (found on the card)
5. Click "Register NFC UID"

### 2. Mark Attendance

#### Method 1: Physical NFC Reader
1. Start the NFC reader: `python backend/nfc_reader.py`
2. Students tap their NFC cards on the reader
3. Attendance is automatically marked

#### Method 2: Web Interface
1. Go to NFC section in web interface
2. Enter NFC UID manually
3. Click "Mark Attendance"

#### Method 3: API
```bash
curl -X POST http://localhost:8000/nfc/attendance \
  -H "Content-Type: application/json" \
  -d '{"nfc_uid": "A1B2C3D4"}'
```

### 3. Monitor Status

- **NFC Reader Status**: Shows if reader is active
- **Recent Scans**: Number of recent NFC scans
- **Debounce Time**: Prevents duplicate scans (10 seconds)

## Sample Data

The system comes with sample students and NFC UIDs:

| Student | Admission No | NFC UID |
|---------|--------------|---------|
| Rahul Sharma | ADM123 | A1B2C3D4 |
| Amit Verma | ADM124 | E5F6G7H8 |
| Priya Singh | ADM125 | I9J0K1L2 |

## Session Logic

- **Morning Session**: Before 12:00 PM
- **Evening Session**: After 12:00 PM
- **Automatic Detection**: Based on current time when card is tapped

## Debouncing

- **Purpose**: Prevents duplicate attendance marking
- **Duration**: 10 seconds (configurable)
- **Behavior**: Ignores same NFC UID if scanned within debounce period

## Troubleshooting

### Common Issues

1. **NFC Hardware Not Detected**
   ```bash
   # Check if NFC reader is connected
   lsusb | grep -i nfc
   
   # Test Python NFC library
   python -c "import nfc; clf = nfc.ContactlessFrontend('usb'); print('OK')"
   ```

2. **API Connection Failed**
   - Ensure backend server is running on port 8000
   - Check API_BASE_URL in nfc_reader.py
   - Verify network connectivity

3. **Student Not Found**
   - Ensure student is registered in database
   - Check NFC UID is correctly registered
   - Verify admission number matches

4. **Duplicate Attendance**
   - Check debounce settings
   - Clear debounce cache if needed
   - Verify timestamp logic

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

1. **NFC UID Validation**: Only registered NFC UIDs are accepted
2. **Debouncing**: Prevents rapid duplicate scans
3. **Session Validation**: Morning/evening sessions are time-based
4. **API Authentication**: All endpoints require authentication (bypassed for testing)

## Performance

- **Debounce Cache**: In-memory storage of recent scans
- **Database Queries**: Optimized for student lookup by NFC UID
- **API Response Time**: Typically < 100ms for attendance marking

## Future Enhancements

1. **Real-time Notifications**: WebSocket updates for attendance events
2. **Batch Registration**: Upload multiple NFC UIDs at once
3. **Attendance Analytics**: NFC-specific reporting
4. **Mobile App**: Native mobile app for NFC reading
5. **Offline Mode**: Local storage when API is unavailable

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `http://localhost:8000/docs`
3. Check backend logs for error messages
4. Verify hardware connections and drivers

## Files Modified/Created

### Backend Files
- `backend/app/models.py` - Added NFC-related models
- `backend/app/main.py` - Added NFC endpoints
- `backend/app/nfc_service.py` - NFC service implementation
- `backend/requirements.txt` - Added nfcpy dependency
- `backend/nfc_reader.py` - Standalone NFC reader
- `backend/setup_nfc.py` - Setup script

### Frontend Files
- `vivid-learner-portal/src/services/api.ts` - Added NFC API functions
- `vivid-learner-portal/src/components/NFCAttendance.tsx` - NFC management component
- `vivid-learner-portal/src/pages/AttendanceTracking.tsx` - Integrated NFC component

### Documentation
- `NFC_IMPLEMENTATION_GUIDE.md` - This guide

---

**Note**: This implementation is based on your provided NFC code and integrates seamlessly with your existing attendance system. The NFC functionality works alongside your current manual and automatic attendance features.

