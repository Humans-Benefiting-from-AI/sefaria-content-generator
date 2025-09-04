"""
Jewish Calendar Integration Module

Integrates with Hebcal API to provide Jewish calendar functionality,
Torah reading detection, and holiday information.

Author: Manus AI Assistant
Date: September 2025
"""

import requests
import json
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import time


@dataclass
class TorahReading:
    """Represents a Torah reading (Parashat HaShavua)"""
    name: str
    hebrew_name: str
    date: str
    hebrew_date: str
    torah_portion: str
    haftarah: str
    aliyot: Dict[str, str]
    triennial: Optional[Dict[str, str]] = None
    link: Optional[str] = None


@dataclass
class JewishHoliday:
    """Represents a Jewish holiday or observance"""
    name: str
    hebrew_name: str
    date: str
    hebrew_date: str
    category: str
    subcategory: Optional[str] = None
    description: Optional[str] = None
    is_yom_tov: bool = False
    link: Optional[str] = None


@dataclass
class JewishCalendarEvent:
    """Represents any Jewish calendar event"""
    title: str
    hebrew_title: str
    date: str
    hebrew_date: str
    category: str
    event_type: str
    details: Optional[Dict[str, Any]] = None


class JewishCalendarAPI:
    """Client for Hebcal Jewish calendar API"""
    
    BASE_URL = "https://www.hebcal.com/hebcal"
    
    def __init__(self, location: Optional[str] = None, israel: bool = False):
        """
        Initialize the Jewish calendar API client
        
        Args:
            location: Location for candle lighting times (optional)
            israel: Use Israel holiday schedule (default: Diaspora)
        """
        self.location = location
        self.israel = israel
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Torah-Calendar-Tool/1.0',
            'Accept': 'application/json'
        })
    
    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the Hebcal API
        
        Args:
            params: Query parameters
            
        Returns:
            JSON response as dictionary
        """
        # Base parameters
        base_params = {
            'v': '1',
            'cfg': 'json',
            'i': 'on' if self.israel else 'off'
        }
        
        # Merge with provided parameters
        all_params = {**base_params, **params}
        
        try:
            response = self.session.get(self.BASE_URL, params=all_params)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            print(f"Error making request to Hebcal API: {e}")
            raise
    
    def get_current_torah_reading(self) -> Optional[TorahReading]:
        """
        Get the current week's Torah reading (Parashat HaShavua)
        
        Returns:
            TorahReading object for current week, or None if not found
        """
        # Get current week's events
        today = date.today()
        
        # Find the most recent Saturday (or today if it's Saturday)
        days_since_saturday = (today.weekday() + 2) % 7
        saturday = today - timedelta(days=days_since_saturday)
        
        params = {
            's': 'on',  # Torah readings
            'start': saturday.strftime('%Y-%m-%d'),
            'end': saturday.strftime('%Y-%m-%d')
        }
        
        data = self._make_request(params)
        
        # Find Torah reading in the response
        for item in data.get('items', []):
            if item.get('category') == 'parashat':
                return self._parse_torah_reading(item)
        
        return None
    
    def get_torah_reading_for_date(self, target_date: Union[str, date]) -> Optional[TorahReading]:
        """
        Get Torah reading for a specific date
        
        Args:
            target_date: Date as string (YYYY-MM-DD) or date object
            
        Returns:
            TorahReading object or None if not found
        """
        if isinstance(target_date, str):
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        
        # Find the Saturday of that week
        days_since_saturday = (target_date.weekday() + 2) % 7
        saturday = target_date - timedelta(days=days_since_saturday)
        
        params = {
            's': 'on',
            'start': saturday.strftime('%Y-%m-%d'),
            'end': saturday.strftime('%Y-%m-%d')
        }
        
        data = self._make_request(params)
        
        for item in data.get('items', []):
            if item.get('category') == 'parashat':
                return self._parse_torah_reading(item)
        
        return None
    
    def get_upcoming_torah_readings(self, weeks: int = 4) -> List[TorahReading]:
        """
        Get upcoming Torah readings for the next several weeks
        
        Args:
            weeks: Number of weeks to look ahead
            
        Returns:
            List of TorahReading objects
        """
        today = date.today()
        end_date = today + timedelta(weeks=weeks)
        
        params = {
            's': 'on',
            'start': today.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        }
        
        data = self._make_request(params)
        readings = []
        
        for item in data.get('items', []):
            if item.get('category') == 'parashat':
                reading = self._parse_torah_reading(item)
                if reading:
                    readings.append(reading)
        
        return readings
    
    def get_current_jewish_holidays(self, days_ahead: int = 30) -> List[JewishHoliday]:
        """
        Get current and upcoming Jewish holidays
        
        Args:
            days_ahead: Number of days to look ahead
            
        Returns:
            List of JewishHoliday objects
        """
        today = date.today()
        end_date = today + timedelta(days=days_ahead)
        
        params = {
            'maj': 'on',  # Major holidays
            'min': 'on',  # Minor holidays
            'mod': 'on',  # Modern holidays
            'mf': 'on',   # Minor fasts
            'ss': 'on',   # Special Shabbatot
            'start': today.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        }
        
        data = self._make_request(params)
        holidays = []
        
        for item in data.get('items', []):
            if item.get('category') == 'holiday':
                holiday = self._parse_holiday(item)
                if holiday:
                    holidays.append(holiday)
        
        return holidays
    
    def get_jewish_date(self, gregorian_date: Union[str, date] = None) -> str:
        """
        Get Hebrew date for a given Gregorian date
        
        Args:
            gregorian_date: Date to convert (default: today)
            
        Returns:
            Hebrew date string
        """
        if gregorian_date is None:
            gregorian_date = date.today()
        elif isinstance(gregorian_date, str):
            gregorian_date = datetime.strptime(gregorian_date, '%Y-%m-%d').date()
        
        params = {
            'd': 'on',  # Hebrew dates
            'start': gregorian_date.strftime('%Y-%m-%d'),
            'end': gregorian_date.strftime('%Y-%m-%d')
        }
        
        data = self._make_request(params)
        
        # Look for any item with Hebrew date
        for item in data.get('items', []):
            if 'hdate' in item:
                return item['hdate']
        
        return ""
    
    def get_weekly_calendar_events(self, start_date: Union[str, date] = None) -> List[JewishCalendarEvent]:
        """
        Get all Jewish calendar events for a week
        
        Args:
            start_date: Start of week (default: current week)
            
        Returns:
            List of JewishCalendarEvent objects
        """
        if start_date is None:
            start_date = date.today()
        elif isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        
        # Get week range (Sunday to Saturday)
        days_since_sunday = start_date.weekday() + 1
        if days_since_sunday == 7:
            days_since_sunday = 0
        
        week_start = start_date - timedelta(days=days_since_sunday)
        week_end = week_start + timedelta(days=6)
        
        params = {
            'maj': 'on',
            'min': 'on',
            'mod': 'on',
            'mf': 'on',
            'ss': 'on',
            's': 'on',
            'nx': 'on',  # Rosh Chodesh
            'o': 'on',   # Omer
            'd': 'on',   # Hebrew dates
            'start': week_start.strftime('%Y-%m-%d'),
            'end': week_end.strftime('%Y-%m-%d')
        }
        
        data = self._make_request(params)
        events = []
        
        for item in data.get('items', []):
            event = self._parse_calendar_event(item)
            if event:
                events.append(event)
        
        return events
    
    def _parse_torah_reading(self, item: Dict[str, Any]) -> Optional[TorahReading]:
        """Parse Torah reading from API response"""
        try:
            leyning = item.get('leyning', {})
            
            return TorahReading(
                name=item.get('title', ''),
                hebrew_name=item.get('hebrew', ''),
                date=item.get('date', ''),
                hebrew_date=item.get('hdate', ''),
                torah_portion=leyning.get('torah', ''),
                haftarah=leyning.get('haftarah', ''),
                aliyot={
                    '1': leyning.get('1', ''),
                    '2': leyning.get('2', ''),
                    '3': leyning.get('3', ''),
                    '4': leyning.get('4', ''),
                    '5': leyning.get('5', ''),
                    '6': leyning.get('6', ''),
                    '7': leyning.get('7', ''),
                    'maftir': leyning.get('maftir', '')
                },
                triennial=leyning.get('triennial'),
                link=item.get('link')
            )
        except Exception as e:
            print(f"Error parsing Torah reading: {e}")
            return None
    
    def _parse_holiday(self, item: Dict[str, Any]) -> Optional[JewishHoliday]:
        """Parse holiday from API response"""
        try:
            return JewishHoliday(
                name=item.get('title', ''),
                hebrew_name=item.get('hebrew', ''),
                date=item.get('date', ''),
                hebrew_date=item.get('hdate', ''),
                category=item.get('category', ''),
                subcategory=item.get('subcat'),
                description=item.get('memo'),
                is_yom_tov=item.get('yomtov', False),
                link=item.get('link')
            )
        except Exception as e:
            print(f"Error parsing holiday: {e}")
            return None
    
    def _parse_calendar_event(self, item: Dict[str, Any]) -> Optional[JewishCalendarEvent]:
        """Parse general calendar event from API response"""
        try:
            return JewishCalendarEvent(
                title=item.get('title', ''),
                hebrew_title=item.get('hebrew', ''),
                date=item.get('date', ''),
                hebrew_date=item.get('hdate', ''),
                category=item.get('category', ''),
                event_type=item.get('subcat', item.get('category', '')),
                details=item
            )
        except Exception as e:
            print(f"Error parsing calendar event: {e}")
            return None


class TorahCalendarManager:
    """High-level manager for Torah and Jewish calendar functionality"""
    
    def __init__(self, location: Optional[str] = None, israel: bool = False):
        """
        Initialize Torah calendar manager
        
        Args:
            location: Location for candle lighting times
            israel: Use Israel holiday schedule
        """
        self.calendar_api = JewishCalendarAPI(location, israel)
    
    def get_current_week_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive summary of current week's Jewish calendar events
        
        Returns:
            Dictionary with Torah reading, holidays, and other events
        """
        torah_reading = self.calendar_api.get_current_torah_reading()
        holidays = self.calendar_api.get_current_jewish_holidays(7)  # Next 7 days
        weekly_events = self.calendar_api.get_weekly_calendar_events()
        hebrew_date = self.calendar_api.get_jewish_date()
        
        return {
            'torah_reading': torah_reading,
            'holidays': holidays,
            'weekly_events': weekly_events,
            'hebrew_date': hebrew_date,
            'gregorian_date': date.today().strftime('%Y-%m-%d')
        }
    
    def is_special_shabbat(self) -> Optional[str]:
        """
        Check if current/upcoming Shabbat is a special Shabbat
        
        Returns:
            Name of special Shabbat or None
        """
        events = self.calendar_api.get_weekly_calendar_events()
        
        for event in events:
            if 'shabbat' in event.title.lower() and event.category != 'parashat':
                return event.title
        
        return None
    
    def get_upcoming_holidays(self, days: int = 60) -> List[JewishHoliday]:
        """
        Get upcoming holidays with descriptions
        
        Args:
            days: Number of days to look ahead
            
        Returns:
            List of upcoming holidays
        """
        return self.calendar_api.get_current_jewish_holidays(days)


# Example usage and testing
def test_jewish_calendar():
    """Test the Jewish calendar functionality"""
    print("Testing Jewish Calendar Integration...")
    
    # Initialize calendar manager
    calendar = TorahCalendarManager()
    
    try:
        # Test current Torah reading
        print("\n1. Current Torah Reading:")
        torah_reading = calendar.calendar_api.get_current_torah_reading()
        if torah_reading:
            print(f"Parasha: {torah_reading.name} ({torah_reading.hebrew_name})")
            print(f"Date: {torah_reading.date} ({torah_reading.hebrew_date})")
            print(f"Torah: {torah_reading.torah_portion}")
            print(f"Haftarah: {torah_reading.haftarah}")
        
        # Test current week summary
        print("\n2. Current Week Summary:")
        summary = calendar.get_current_week_summary()
        print(f"Hebrew Date: {summary['hebrew_date']}")
        print(f"Holidays this week: {len(summary['holidays'])}")
        print(f"Total events: {len(summary['weekly_events'])}")
        
        # Test upcoming holidays
        print("\n3. Upcoming Holidays:")
        holidays = calendar.get_upcoming_holidays(30)
        for holiday in holidays[:5]:  # Show first 5
            print(f"- {holiday.name} ({holiday.date})")
        
        print("\nJewish calendar integration test completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")


if __name__ == "__main__":
    test_jewish_calendar()

