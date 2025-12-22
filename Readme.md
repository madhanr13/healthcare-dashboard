# Healthcare Data Format Guide

## 📋 CSV File Structure

Your CSV file must have these 8 columns in this exact order:

```
patient_id, timestamp, heart_rate, temperature, blood_pressure_systolic, blood_pressure_diastolic, respiratory_rate, oxygen_saturation
```

## 📊 Column Descriptions

| Column | Format | Example | Notes |
|--------|--------|---------|-------|
| **patient_id** | Text | P00007 | Unique patient identifier (P + 5 digits) |
| **timestamp** | ISO 8601 | 2025-12-28T14:30:45.123Z | Date & time of measurement |
| **heart_rate** | Number | 77 | Beats per minute (bpm) |
| **temperature** | Decimal | 37.5 | Degrees Celsius (°C) |
| **blood_pressure_systolic** | Number | 120 | Top number (mmHg) |
| **blood_pressure_diastolic** | Number | 80 | Bottom number (mmHg) |
| **respiratory_rate** | Number | 16 | Breaths per minute |
| **oxygen_saturation** | Number | 98 | Percentage (%) |

## ✅ Example Row

```csv
P00007,2025-12-28T14:30:45.123Z,77,37.5,120,80,16,98
```

**Translation:**
- Patient: P00007
- Date/Time: Dec 28, 2025 at 2:30 PM
- Heart Rate: 77 bpm
- Temperature: 37.5°C
- Blood Pressure: 120/80 mmHg
- Respiratory Rate: 16 breaths/min
- Oxygen: 98%

## 🎯 Normal Ranges (For Reference)

| Vital Sign | Low | Normal | High | Critical |
|-----------|-----|--------|------|----------|
| Heart Rate | <60 | 60-100 | 100-120 | >120 |
| Temperature | <36 | 36-37.5 | 37.5-38.5 | >38.5 |
| O2 Saturation | <90 | >95 | 90-95 | <90 |
| Resp. Rate | <12 | 12-20 | 20-24 | >24 |

## 📝 How to Create Your CSV File

### Option 1: Excel/Google Sheets
1. Create columns with headers (exact names!)
2. Enter your data row by row
3. Save as **CSV (Comma Separated Values)**
4. Upload to dashboard

### Option 2: Text Editor
1. Open Notepad or VS Code
2. Type data with commas between values
3. One row per line
4. Save as `filename.csv`

### Example (5 rows):
```csv
patient_id,timestamp,heart_rate,temperature,blood_pressure_systolic,blood_pressure_diastolic,respiratory_rate,oxygen_saturation
P00001,2025-12-28T08:00:00Z,72,36.8,118,76,14,99
P00001,2025-12-28T09:00:00Z,75,36.9,120,78,15,98
P00002,2025-12-28T08:15:00Z,68,37.0,118,78,14,99
P00002,2025-12-28T09:15:00Z,70,36.9,119,79,15,98
P00003,2025-12-28T08:30:00Z,110,38.5,135,85,18,92
```

## ⚠️ Important Rules

### Column Names MUST Match Exactly
❌ Wrong:
```csv
PatientID, HeartRate, Temp  (capitalization wrong)
id, hr, temp              (names too short)
```

✅ Correct:
```csv
patient_id,timestamp,heart_rate,temperature,blood_pressure_systolic,blood_pressure_diastolic,respiratory_rate,oxygen_saturation
```

### Data Requirements
- ✅ No empty rows
- ✅ No special characters in patient ID (except numbers)
- ✅ Timestamp in ISO 8601 format (2025-12-28T14:30:00Z)
- ✅ Numbers only (no units like "bpm" or "°C")
- ✅ Decimal numbers use period (.) not comma (,)

### File Size
- Small files: < 1MB upload instantly
- Large files: Up to 10MB supported
- More than 5000 records: May take longer to process

## 🔧 Common Issues & Fixes

### "Error: Missing columns"
**Fix:** Check exact column names match (case-sensitive)

### "Chart won't load"
**Fix:** Make sure at least 10 rows of data

### "Data looks wrong"
**Fix:** Open CSV in Excel to verify formatting

### "Upload fails"
**Fix:** Try smaller file (< 500 rows) first

## 📥 Ready-Made Sample Files

We provide 3 sample CSV files to test with:

1. **sample_data.csv** - 20 patients, clean data
2. **healthData2.csv** - 15 patients, varied values
3. **healthcare_data.csv** - 1 patient, 60 detailed records

**How to use:**
1. Visit: https://healthcare-analysis-qpds.netlify.app
2. Click "Load Sample Data" OR
3. Click "Upload CSV" and select any sample file

## 🎨 Dashboard Features by Data

Once uploaded, you can:

✅ **View Charts**
- Heart rate trends
- Temperature distribution
- Oxygen saturation ranges
- Patient statistics

✅ **Filter & Search**
- Find specific patients
- Filter by status (normal/critical)
- Search any vital sign

✅ **Generate Alerts**
- Automatic critical detection
- Color-coded warnings
- Real-time notifications

✅ **Export Results**
- Download filtered data
- Share with colleagues
- Use in reports

## 📱 Timestamp Format Explained

ISO 8601 Format: `YYYY-MM-DDTHH:MM:SS.mmmZ`

Breaking it down:
```
2025-12-28T14:30:45.123Z

2025     = Year
12       = Month (December)
28       = Day
T        = Separator (literal T)
14       = Hour (24-hour format)
30       = Minutes
45       = Seconds
.123     = Milliseconds (optional)
Z        = UTC timezone (required)
```

### Quick Timestamp Examples:
```
2025-12-28T08:00:00Z     = Dec 28, 2025 at 8:00 AM
2025-12-28T14:30:45.123Z = Dec 28, 2025 at 2:30 PM and 45 seconds
2025-01-15T23:59:59Z     = Jan 15, 2025 at 11:59 PM
```

## 💾 Quick Checklist Before Upload

- [ ] File is `.csv` format
- [ ] Column names are EXACTLY correct
- [ ] At least 5 rows of data
- [ ] No empty rows or columns
- [ ] Numbers only (no units)
- [ ] Timestamps in ISO 8601 format
- [ ] File size < 10MB
- [ ] No special characters in text

## ✨ That's It!

Your CSV is ready to upload! The dashboard will:
1. ✅ Validate data format
2. ✅ Clean any issues
3. ✅ Generate charts
4. ✅ Create alerts
5. ✅ Display results

**Questions?** Check the sample CSV files for reference!