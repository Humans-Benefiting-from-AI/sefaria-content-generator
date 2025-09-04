# Torah Calendar Tool

A specialized web application that integrates with Sefaria and Hebcal APIs to automatically generate content based on the weekly Torah reading and Jewish calendar events.

## Features

### 🔯 Torah Reading Integration
- **Current Torah Reading**: Displays the current week's Parashat HaShavua with Hebrew names, dates, and Torah portions
- **Aliyot Breakdown**: Complete breakdown of all seven aliyot plus Maftir with specific verse references
- **Haftarah Information**: Prophetic reading that accompanies the Torah portion
- **Sefaria Integration**: Direct links to read the full text on Sefaria

### 📅 Jewish Calendar Features
- **Hebrew Date Display**: Shows current Hebrew date in the header
- **Holiday Detection**: Automatically detects and displays current and upcoming Jewish holidays
- **Holiday Content**: Comprehensive information about holidays including:
  - Background and historical significance
  - Themes and spiritual meanings
  - Customs and observances
  - Special foods and preparations
  - Torah readings and liturgy

### 📚 Automated Content Generation
- **Weekly Study Guides**: Automatically generated study materials for each Torah portion including:
  - Key themes and lessons
  - Discussion questions for families and study groups
  - Practical applications for daily life
  - Commentary insights
- **Holiday Alerts**: Preparation reminders and timelines for upcoming holidays
- **Seasonal Content**: Content tailored to Jewish seasons and special periods

### 🌐 Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Tabbed Navigation**: Easy access to different content areas:
  - Torah Reading
  - Holidays
  - Weekly Summary
  - Upcoming Events
- **Modern UI**: Clean, professional interface with Jewish-themed styling
- **Real-time Updates**: Content automatically updates based on the current date

## Technology Stack

### Backend
- **Flask**: Python web framework
- **Flask-CORS**: Cross-origin resource sharing support
- **Requests**: HTTP library for API calls
- **SQLAlchemy**: Database ORM (optional)

### Frontend
- **HTML5**: Modern semantic markup
- **CSS3**: Responsive design with Flexbox and Grid
- **JavaScript**: Interactive functionality and API communication
- **Font Awesome**: Icons for enhanced UI

### APIs
- **Sefaria API**: Jewish text database and Torah readings
- **Hebcal API**: Jewish calendar, holidays, and Hebrew dates

## Installation and Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Local Development

1. **Clone or download the project**
   ```bash
   cd torah-calendar-tool/torah-calendar-web
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the development server**
   ```bash
   python src/main.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5001`

### Production Deployment

The application is designed to be deployed on cloud platforms. It includes:
- CORS configuration for cross-origin requests
- Host binding to `0.0.0.0` for external access
- Production-ready Flask configuration

## API Endpoints

### Torah Reading Endpoints
- `GET /api/current-torah-reading` - Current week's Torah reading
- `GET /api/weekly-torah-guide` - Comprehensive study guide
- `GET /api/torah-reading-for-date?date=YYYY-MM-DD` - Torah reading for specific date
- `GET /api/upcoming-torah-readings?weeks=N` - Upcoming Torah readings

### Holiday Endpoints
- `GET /api/upcoming-holidays?days=N` - Upcoming holidays
- `GET /api/holiday-content/{holiday_name}` - Detailed holiday information
- `GET /api/current-holiday-content` - Current holiday content
- `GET /api/weekly-holiday-alert` - Holiday preparation alerts

### Calendar Endpoints
- `GET /api/hebrew-date?date=YYYY-MM-DD` - Hebrew date conversion
- `GET /api/weekly-calendar-summary` - Weekly calendar overview
- `GET /api/seasonal-content?season=current` - Seasonal Jewish content

### Utility Endpoints
- `GET /api/available-holidays` - List of supported holidays
- `GET /api/health` - Health check endpoint

## Content Generation Features

### Torah Study Guides
Each weekly Torah guide includes:
- **Parasha Information**: Name, date, Torah portion, and Haftarah
- **Torah Text Preview**: Key verses and themes
- **Weekly Themes**: 5-8 major themes from the portion
- **Discussion Questions**: 8-10 thought-provoking questions
- **Practical Applications**: Real-world applications of Torah teachings

### Holiday Content
Comprehensive holiday information includes:
- **Holiday Information**: Name, category, duration, and dates
- **Background**: Historical and religious significance
- **Themes**: Spiritual and ethical themes
- **Observance Guide**: Customs, special foods, and preparation
- **Liturgy**: Torah readings, Haftarah, and special prayers
- **Educational Content**: Discussion questions and activities
- **Practical Guide**: Preparation timeline and shopping lists

### Calendar Integration
- **Automatic Updates**: Content updates based on current date
- **Hebrew Calendar**: Full integration with Hebrew dates and years
- **Holiday Detection**: Automatic detection of current and upcoming holidays
- **Seasonal Awareness**: Content adapts to Jewish seasons and periods

## Supported Holidays

The system includes comprehensive content for:

### High Holy Days
- Rosh Hashana
- Yom Kippur

### Pilgrimage Festivals
- Sukkot
- Pesach (Passover)
- Shavuot

### Other Major Holidays
- Chanukah
- Purim

### Fast Days
- Tisha B'Av
- Other traditional fast days

### Modern Holidays
- Yom HaShoah (Holocaust Remembrance Day)
- Yom HaAtzma'ut (Israel Independence Day)

## Customization

### Location Settings
The system can be configured for different locations to provide:
- Accurate candle lighting times
- Local holiday observances
- Israel vs. Diaspora holiday schedules

### Content Customization
- Holiday database can be extended with additional holidays
- Content templates can be modified for different audiences
- API endpoints can be customized for specific needs

## Development

### Project Structure
```
torah-calendar-web/
├── src/
│   ├── main.py              # Flask application entry point
│   ├── routes/
│   │   ├── torah_api.py     # Torah and calendar API routes
│   │   └── user.py          # User management routes
│   ├── models/
│   │   └── user.py          # Database models
│   ├── static/
│   │   ├── index.html       # Main web interface
│   │   ├── style.css        # Styling and responsive design
│   │   └── script.js        # Frontend JavaScript
│   └── database/
│       └── app.db           # SQLite database
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Core Modules
- `jewish_calendar.py` - Hebrew calendar and API integration
- `torah_content_generator.py` - Torah study guide generation
- `holiday_content_generator.py` - Holiday content creation

### Adding New Features
1. **New API Endpoints**: Add routes to `torah_api.py`
2. **Frontend Features**: Modify `script.js` and `style.css`
3. **Content Generators**: Extend the generator classes
4. **Holiday Support**: Add entries to the holiday database

## Contributing

This project is designed to be extensible and customizable. Areas for potential enhancement:

- Additional holiday support
- Multi-language content
- Advanced study features
- Community content sharing
- Mobile app development
- Integration with other Jewish learning platforms

## License

This project integrates with and relies on:
- **Sefaria**: Open source Jewish text platform
- **Hebcal**: Jewish calendar API service

Please respect the terms of service for these APIs when using this tool.

## Support

For questions, issues, or feature requests, please refer to the documentation or contact the development team.

---

**Torah Calendar Tool** - Bringing the richness of Jewish learning and calendar awareness to the digital age.

