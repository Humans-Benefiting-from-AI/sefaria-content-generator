# Jewish Calendar API Research

## Hebcal API - Primary Source

### Overview
Hebcal.com provides a comprehensive REST API for Jewish calendar data in JSON format.

### Key Features
- **Torah Readings**: Parashat HaShavua (weekly Torah portion) with full leyning details
- **Jewish Holidays**: Major, minor, modern holidays, and special Shabbatot
- **Hebrew Dates**: Conversion between Gregorian and Hebrew calendar
- **Candle Lighting**: Shabbat and holiday times based on location
- **Daily Learning**: Daf Yomi, Mishna Yomi, and other study schedules

### API Endpoints

#### Base URL
```
https://www.hebcal.com/hebcal?v=1&cfg=json
```

#### Key Parameters
- `s=on` - Parashat ha-Shavuah (Torah readings)
- `maj=on` - Major holidays
- `min=on` - Minor holidays
- `mod=on` - Modern holidays (Yom HaShoah, etc.)
- `ss=on` - Special Shabbatot
- `year=now` - Current year or specific year
- `start=YYYY-MM-DD` - Date range start
- `end=YYYY-MM-DD` - Date range end

#### Torah Reading Details
When `s=on` is enabled, Torah readings include:
- Full parasha name (Hebrew and English)
- Aliyot breakdown (1-7, maftir)
- Haftarah reading
- Triennial cycle readings
- Links to Sefaria for full text

#### Example Response Structure
```json
{
  "title": "Parashat Bamidbar",
  "date": "2015-05-23",
  "hdate": "5 Sivan 5775",
  "category": "parashat",
  "hebrew": "פרשת במדבר",
  "leyning": {
    "1": "Numbers 1:1-1:19",
    "torah": "Numbers 1:1-4:20",
    "haftarah": "Hosea 2:1-22",
    "triennial": { ... }
  }
}
```

## Sefaria Calendar API

### Overview
Sefaria also provides calendar functionality for daily/weekly learning schedules.

### Features
- Daily learning schedules
- Torah portion information
- Integration with Sefaria text database

## JavaScript Libraries

### @hebcal/core
- Jewish holidays and calendar calculations
- Torah readings and Haftarah
- Candle lighting times
- Hebrew date conversions

### @hebcal/leyning
- Detailed Torah reading API
- Parashat HaShavua and holiday readings
- Aliyot and triennial cycle support

### @hebcal/learning
- Daily learning schedules
- Daf Yomi, Mishna Yomi, etc.

## Implementation Strategy

### For Torah Calendar Tool
1. **Use Hebcal REST API** as primary data source
2. **Integrate with Sefaria API** for full text content
3. **Combine both APIs** for comprehensive Torah portion content:
   - Hebcal: Calendar data, Torah reading schedule
   - Sefaria: Full text, commentaries, related sources

### Key Capabilities Needed
1. **Current Torah Portion Detection**
   - Get current week's parasha
   - Handle special cases (holidays, double portions)
   
2. **Holiday Detection**
   - Identify current/upcoming Jewish holidays
   - Generate holiday-specific content
   
3. **Automatic Content Generation**
   - Weekly Torah portion study guides
   - Holiday preparation materials
   - Seasonal Jewish content

### API Integration Plan
1. **Hebcal API**: Calendar events and Torah reading schedule
2. **Sefaria API**: Full text retrieval and commentary
3. **Combined Processing**: Generate comprehensive educational content

## Next Steps
1. Implement Hebcal API integration
2. Create Torah portion detection logic
3. Build automated content generation system
4. Add Jewish holiday content creation
5. Create specialized web interface

