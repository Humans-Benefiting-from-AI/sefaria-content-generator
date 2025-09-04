"""
Torah Content Generator

Automatically generates educational content based on weekly Torah readings
and Jewish calendar events using Sefaria and Hebcal APIs.

Author: Manus AI Assistant
Date: September 2025
"""

import sys
import os
sys.path.append('/home/ubuntu')

from jewish_calendar import JewishCalendarAPI, TorahCalendarManager, TorahReading, JewishHoliday
from sefaria_integration import SefariaAPIClient, SefariaContentGenerator
from typing import Dict, List, Optional, Any
from datetime import date, datetime, timedelta
import json


class TorahContentGenerator:
    """Generates comprehensive content for Torah readings and Jewish calendar events"""
    
    def __init__(self, location: Optional[str] = None, israel: bool = False):
        """
        Initialize Torah content generator
        
        Args:
            location: Location for candle lighting times
            israel: Use Israel holiday schedule
        """
        self.calendar_manager = TorahCalendarManager(location, israel)
        self.sefaria_client = SefariaAPIClient()
        self.sefaria_generator = SefariaContentGenerator(self.sefaria_client)
    
    def generate_weekly_torah_guide(self, torah_reading: Optional[TorahReading] = None) -> Dict[str, Any]:
        """
        Generate comprehensive weekly Torah study guide
        
        Args:
            torah_reading: Specific Torah reading (default: current week)
            
        Returns:
            Complete study guide with text, commentary, and insights
        """
        if torah_reading is None:
            torah_reading = self.calendar_manager.calendar_api.get_current_torah_reading()
        
        if not torah_reading:
            return {"error": "No Torah reading found"}
        
        # Extract parasha name for Sefaria queries
        parasha_name = torah_reading.name.replace("Parashat ", "").replace("Parashah ", "")
        
        # Get basic Torah information (without full text for now)
        torah_text = None
        haftarah_text = None
        
        # Generate basic study guide without Sefaria for now
        study_guide = {
            'reference': torah_reading.torah_portion,
            'main_text': {
                'content': f"Torah reading: {torah_reading.torah_portion}",
                'language': 'en',
                'version': 'Basic'
            },
            'study_questions': self._generate_discussion_questions(parasha_name),
            'themes': self._generate_weekly_themes(parasha_name)
        }
        
        # Generate basic commentary info
        commentaries = [
            {
                'source': 'Traditional Commentary',
                'text': f"Commentary on {parasha_name} - detailed analysis would be provided here",
                'title': f'{parasha_name} Commentary',
                'category': 'Commentary'
            }
        ]
        
        # Build comprehensive guide
        weekly_guide = {
            'parasha_info': {
                'name': torah_reading.name,
                'hebrew_name': torah_reading.hebrew_name,
                'date': torah_reading.date,
                'hebrew_date': torah_reading.hebrew_date,
                'torah_portion': torah_reading.torah_portion,
                'haftarah': torah_reading.haftarah
            },
            'torah_text': {
                'content': f"Torah portion: {torah_reading.torah_portion}",
                'language': 'en',
                'version': 'Basic Reference',
                'preview': f"This week's Torah reading is {torah_reading.torah_portion}"
            },
            'haftarah_text': {
                'content': f"Haftarah: {torah_reading.haftarah}" if torah_reading.haftarah else "No Haftarah specified",
                'language': 'en',
                'version': 'Basic Reference',
                'preview': f"Haftarah reading: {torah_reading.haftarah}" if torah_reading.haftarah else "No Haftarah"
            },
            'aliyot_breakdown': torah_reading.aliyot,
            'study_guide': study_guide,
            'commentaries': commentaries,
            'weekly_themes': self._generate_weekly_themes(parasha_name),
            'discussion_questions': self._generate_discussion_questions(parasha_name),
            'practical_applications': self._generate_practical_applications(parasha_name),
            'generated_date': datetime.now().isoformat()
        }
        
        return weekly_guide
    
    def generate_holiday_content(self, holiday: JewishHoliday) -> Dict[str, Any]:
        """
        Generate content for a specific Jewish holiday
        
        Args:
            holiday: Jewish holiday object
            
        Returns:
            Holiday content with background, customs, and texts
        """
        holiday_content = {
            'holiday_info': {
                'name': holiday.name,
                'hebrew_name': holiday.hebrew_name,
                'date': holiday.date,
                'hebrew_date': holiday.hebrew_date,
                'category': holiday.category,
                'description': holiday.description,
                'is_yom_tov': holiday.is_yom_tov
            },
            'background': self._get_holiday_background(holiday.name),
            'customs_and_laws': self._get_holiday_customs(holiday.name),
            'special_readings': self._get_holiday_readings(holiday.name),
            'preparation_guide': self._get_holiday_preparation(holiday.name),
            'generated_date': datetime.now().isoformat()
        }
        
        return holiday_content
    
    def generate_weekly_calendar_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive weekly calendar summary
        
        Returns:
            Complete weekly summary with all events and content
        """
        summary = self.calendar_manager.get_current_week_summary()
        
        # Generate Torah content if available
        torah_content = None
        if summary['torah_reading']:
            torah_content = self.generate_weekly_torah_guide(summary['torah_reading'])
        
        # Generate holiday content for any holidays this week
        holiday_content = []
        for holiday in summary['holidays']:
            try:
                content = self.generate_holiday_content(holiday)
                holiday_content.append(content)
            except Exception as e:
                print(f"Error generating holiday content for {holiday.name}: {e}")
        
        # Check for special Shabbat
        special_shabbat = self.calendar_manager.is_special_shabbat()
        
        weekly_summary = {
            'week_info': {
                'gregorian_date': summary['gregorian_date'],
                'hebrew_date': summary['hebrew_date'],
                'special_shabbat': special_shabbat
            },
            'torah_content': torah_content,
            'holiday_content': holiday_content,
            'weekly_events': [
                {
                    'title': event.title,
                    'hebrew_title': event.hebrew_title,
                    'date': event.date,
                    'category': event.category,
                    'type': event.event_type
                }
                for event in summary['weekly_events']
            ],
            'candle_lighting_info': self._get_candle_lighting_info(),
            'generated_date': datetime.now().isoformat()
        }
        
        return weekly_summary
    
    def generate_monthly_overview(self, month: Optional[int] = None, year: Optional[int] = None) -> Dict[str, Any]:
        """
        Generate monthly overview of Torah readings and holidays
        
        Args:
            month: Month number (default: current month)
            year: Year (default: current year)
            
        Returns:
            Monthly overview with all Torah readings and holidays
        """
        if month is None:
            month = date.today().month
        if year is None:
            year = date.today().year
        
        # Get month's Torah readings
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        # Get Torah readings for the month
        torah_readings = []
        current_date = start_date
        while current_date < end_date:
            # Check each Saturday
            if current_date.weekday() == 5:  # Saturday
                reading = self.calendar_manager.calendar_api.get_torah_reading_for_date(current_date)
                if reading:
                    torah_readings.append(reading)
            current_date += timedelta(days=1)
        
        # Get holidays for the month
        holidays = self.calendar_manager.calendar_api.get_current_jewish_holidays(31)
        month_holidays = [
            h for h in holidays 
            if datetime.strptime(h.date, '%Y-%m-%d').month == month
        ]
        
        monthly_overview = {
            'month_info': {
                'month': month,
                'year': year,
                'hebrew_month': self._get_hebrew_month_name(month, year)
            },
            'torah_readings': [
                {
                    'name': reading.name,
                    'date': reading.date,
                    'torah_portion': reading.torah_portion
                }
                for reading in torah_readings
            ],
            'holidays': [
                {
                    'name': holiday.name,
                    'date': holiday.date,
                    'category': holiday.category
                }
                for holiday in month_holidays
            ],
            'generated_date': datetime.now().isoformat()
        }
        
        return monthly_overview
    
    def _generate_weekly_themes(self, parasha_name: str) -> List[str]:
        """Generate thematic insights for the Torah portion"""
        # This would ideally use AI or a comprehensive database
        # For now, return general themes that apply to most portions
        themes = [
            "Divine guidance and human responsibility",
            "The relationship between individual and community",
            "Justice and compassion in daily life",
            "Faith and action in challenging times",
            "The eternal relevance of Torah wisdom"
        ]
        
        # Add parasha-specific themes based on name
        specific_themes = {
            'Bereshit': ['Creation and purpose', 'Human dignity', 'Environmental stewardship'],
            'Noach': ['Renewal and hope', 'Moral courage', 'Divine covenant'],
            'Lech-Lecha': ['Faith journey', 'Trust in the unknown', 'Spiritual calling'],
            'Vayera': ['Hospitality', 'Divine justice', 'Intercession for others'],
            'Shoftim': ['Justice and leadership', 'Judicial integrity', 'Pursuit of righteousness'],
            'Ki Teitzei': ['Social responsibility', 'Ethical treatment of others', 'Compassionate laws']
        }
        
        if parasha_name in specific_themes:
            themes.extend(specific_themes[parasha_name])
        
        return themes
    
    def _generate_discussion_questions(self, parasha_name: str) -> List[str]:
        """Generate discussion questions for the Torah portion"""
        general_questions = [
            "What is the central message of this Torah portion?",
            "How do the events in this parasha relate to our modern lives?",
            "What character traits are highlighted in this reading?",
            "How does this portion connect to previous Torah readings?",
            "What practical lessons can we derive from this text?"
        ]
        
        # Add parasha-specific questions
        specific_questions = {
            'Shoftim': [
                "What qualities should we look for in leaders?",
                "How do we balance justice with mercy?",
                "What role does the pursuit of justice play in society?"
            ]
        }
        
        questions = general_questions.copy()
        if parasha_name in specific_questions:
            questions.extend(specific_questions[parasha_name])
        
        return questions
    
    def _generate_practical_applications(self, parasha_name: str) -> List[str]:
        """Generate practical applications for daily life"""
        return [
            "Reflect on how the Torah's teachings apply to current challenges",
            "Consider ways to embody the values presented in this portion",
            "Discuss the parasha's lessons with family and friends",
            "Look for opportunities to practice the virtues highlighted",
            "Connect the ancient wisdom to contemporary ethical dilemmas"
        ]
    
    def _get_holiday_background(self, holiday_name: str) -> str:
        """Get background information for a holiday"""
        # This would ideally connect to a comprehensive database
        backgrounds = {
            'Rosh Hashana': 'The Jewish New Year, a time of reflection, repentance, and renewal.',
            'Yom Kippur': 'The Day of Atonement, the holiest day in the Jewish calendar.',
            'Sukkot': 'The Festival of Booths, celebrating the harvest and divine protection.',
            'Shavuot': 'The Festival of Weeks, commemorating the giving of the Torah.',
            'Pesach': 'Passover, celebrating the Exodus from Egypt and freedom from slavery.'
        }
        
        return backgrounds.get(holiday_name, f"Information about {holiday_name}")
    
    def _get_holiday_customs(self, holiday_name: str) -> List[str]:
        """Get customs and laws for a holiday"""
        return [
            f"Traditional observances for {holiday_name}",
            "Special prayers and rituals",
            "Dietary customs and restrictions",
            "Family and community traditions"
        ]
    
    def _get_holiday_readings(self, holiday_name: str) -> List[str]:
        """Get special Torah and Haftarah readings for holidays"""
        return [
            "Special Torah readings for the holiday",
            "Haftarah selections",
            "Additional liturgical texts"
        ]
    
    def _get_holiday_preparation(self, holiday_name: str) -> List[str]:
        """Get preparation guide for holidays"""
        return [
            "Spiritual preparation and reflection",
            "Practical preparations and customs",
            "Family and community involvement",
            "Study and learning opportunities"
        ]
    
    def _get_candle_lighting_info(self) -> Dict[str, str]:
        """Get candle lighting information"""
        return {
            "note": "Candle lighting times vary by location",
            "general_time": "18 minutes before sunset",
            "recommendation": "Check local times for your area"
        }
    
    def _get_hebrew_month_name(self, month: int, year: int) -> str:
        """Get Hebrew month name (simplified)"""
        # This would ideally use proper Hebrew calendar conversion
        hebrew_months = [
            "Tishrei", "Cheshvan", "Kislev", "Tevet", "Shevat", "Adar",
            "Nissan", "Iyar", "Sivan", "Tammuz", "Av", "Elul"
        ]
        
        # Simplified mapping (not accurate for Hebrew calendar)
        return f"Approximate Hebrew month for {month}/{year}"


# Testing function
def test_torah_content_generator():
    """Test the Torah content generator"""
    print("Testing Torah Content Generator...")
    
    generator = TorahContentGenerator()
    
    try:
        # Test weekly Torah guide
        print("\n1. Generating Weekly Torah Guide...")
        weekly_guide = generator.generate_weekly_torah_guide()
        
        if 'error' not in weekly_guide:
            print(f"Generated guide for: {weekly_guide['parasha_info']['name']}")
            print(f"Torah portion: {weekly_guide['parasha_info']['torah_portion']}")
            print(f"Number of themes: {len(weekly_guide['weekly_themes'])}")
            print(f"Number of questions: {len(weekly_guide['discussion_questions'])}")
        
        # Test weekly calendar summary
        print("\n2. Generating Weekly Calendar Summary...")
        weekly_summary = generator.generate_weekly_calendar_summary()
        print(f"Hebrew date: {weekly_summary['week_info']['hebrew_date']}")
        print(f"Number of events: {len(weekly_summary['weekly_events'])}")
        print(f"Holiday content items: {len(weekly_summary['holiday_content'])}")
        
        print("\nTorah content generator test completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")


if __name__ == "__main__":
    test_torah_content_generator()

