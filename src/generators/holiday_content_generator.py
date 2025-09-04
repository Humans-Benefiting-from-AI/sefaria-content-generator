"""
Jewish Holiday Content Generator

Generates specialized content for Jewish holidays, special Shabbatot,
and calendar events with automatic detection and content creation.

Author: Manus AI Assistant
Date: September 2025
"""

from jewish_calendar import JewishCalendarAPI, TorahCalendarManager, JewishHoliday
from typing import Dict, List, Optional, Any
from datetime import date, datetime, timedelta
import json


class HolidayContentGenerator:
    """Generates comprehensive content for Jewish holidays and special occasions"""
    
    def __init__(self, location: Optional[str] = None, israel: bool = False):
        """
        Initialize holiday content generator
        
        Args:
            location: Location for candle lighting times
            israel: Use Israel holiday schedule
        """
        self.calendar_manager = TorahCalendarManager(location, israel)
        self.holiday_database = self._initialize_holiday_database()
    
    def _initialize_holiday_database(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive holiday information database"""
        return {
            # High Holy Days
            'Rosh Hashana': {
                'category': 'High Holy Days',
                'duration_days': 2,
                'background': 'The Jewish New Year, marking the beginning of the Ten Days of Repentance. A time for reflection, renewal, and spiritual awakening.',
                'themes': ['Renewal', 'Judgment', 'Kingship', 'Repentance', 'Hope'],
                'customs': [
                    'Blowing the shofar',
                    'Eating apples and honey for a sweet new year',
                    'Tashlich ceremony by water',
                    'Special prayers and liturgy',
                    'Round challah symbolizing the cycle of the year'
                ],
                'special_foods': ['Apples and honey', 'Round challah', 'Pomegranates', 'Fish head', 'Sweet foods'],
                'torah_readings': ['Genesis 21:1-34', 'Numbers 29:1-6'],
                'haftarah': ['1 Samuel 1:1-2:10', 'Jeremiah 31:2-20'],
                'preparation': [
                    'Spiritual preparation through self-reflection',
                    'Seeking forgiveness from others',
                    'Preparing special foods',
                    'Learning about the holiday themes'
                ]
            },
            
            'Yom Kippur': {
                'category': 'High Holy Days',
                'duration_days': 1,
                'background': 'The Day of Atonement, the holiest day in the Jewish calendar. A day of fasting, prayer, and complete repentance.',
                'themes': ['Atonement', 'Forgiveness', 'Spiritual purification', 'Teshuvah', 'Divine mercy'],
                'customs': [
                    '25-hour fast',
                    'Five prayer services',
                    'Wearing white clothing',
                    'Kol Nidre service',
                    'Vidui (confessional prayers)'
                ],
                'special_foods': ['Pre-fast meal', 'Break-fast meal'],
                'torah_readings': ['Leviticus 16:1-34', 'Numbers 29:7-11'],
                'haftarah': ['Isaiah 57:14-58:14'],
                'preparation': [
                    'Seeking forgiveness from others',
                    'Spiritual preparation and reflection',
                    'Preparing pre-fast and break-fast meals',
                    'Charity and good deeds'
                ]
            },
            
            # Pilgrimage Festivals
            'Sukkot': {
                'category': 'Pilgrimage Festivals',
                'duration_days': 7,
                'background': 'The Festival of Booths, celebrating the harvest and commemorating the divine protection during the wilderness wandering.',
                'themes': ['Divine protection', 'Harvest celebration', 'Temporary dwellings', 'Joy', 'Unity'],
                'customs': [
                    'Building and dwelling in sukkah',
                    'Four species (lulav, etrog, myrtle, willow)',
                    'Eating meals in the sukkah',
                    'Welcoming guests (ushpizin)',
                    'Celebrating the harvest'
                ],
                'special_foods': ['Harvest fruits and vegetables', 'Traditional holiday foods'],
                'torah_readings': ['Leviticus 22:26-23:44', 'Numbers 29:12-16'],
                'haftarah': ['Zechariah 14:1-21'],
                'preparation': [
                    'Building the sukkah',
                    'Acquiring the four species',
                    'Preparing for outdoor meals',
                    'Learning about the holiday significance'
                ]
            },
            
            'Pesach': {
                'category': 'Pilgrimage Festivals',
                'duration_days': 8,
                'background': 'Passover, commemorating the Exodus from Egypt and the liberation from slavery. The festival of freedom.',
                'themes': ['Freedom', 'Liberation', 'Divine redemption', 'Remembrance', 'Renewal'],
                'customs': [
                    'Seder meals with Haggadah',
                    'Eating matzah',
                    'Avoiding chametz',
                    'Four cups of wine',
                    'Telling the Exodus story'
                ],
                'special_foods': ['Matzah', 'Maror (bitter herbs)', 'Charoset', 'Wine', 'Kosher for Passover foods'],
                'torah_readings': ['Exodus 12:21-51', 'Leviticus 22:26-23:44'],
                'haftarah': ['Joshua 5:2-6:1'],
                'preparation': [
                    'Cleaning and removing chametz',
                    'Preparing the seder',
                    'Shopping for Passover foods',
                    'Learning the Haggadah'
                ]
            },
            
            'Shavuot': {
                'category': 'Pilgrimage Festivals',
                'duration_days': 2,
                'background': 'The Festival of Weeks, commemorating the giving of the Torah at Mount Sinai. Also celebrates the harvest.',
                'themes': ['Torah giving', 'Divine revelation', 'Harvest celebration', 'Learning', 'Commitment'],
                'customs': [
                    'All-night Torah study',
                    'Reading the Book of Ruth',
                    'Eating dairy foods',
                    'Decorating with flowers and greenery',
                    'Confirmation ceremonies'
                ],
                'special_foods': ['Dairy foods', 'Cheesecake', 'Blintzes', 'Fresh fruits'],
                'torah_readings': ['Exodus 19:1-20:23', 'Numbers 28:26-31'],
                'haftarah': ['Ezekiel 1:1-28, 3:12'],
                'preparation': [
                    'Preparing for all-night study',
                    'Learning about Torah themes',
                    'Preparing dairy meals',
                    'Decorating the home'
                ]
            },
            
            # Other Major Holidays
            'Chanukah': {
                'category': 'Post-Biblical',
                'duration_days': 8,
                'background': 'The Festival of Lights, commemorating the rededication of the Temple and the miracle of oil that lasted eight days.',
                'themes': ['Religious freedom', 'Miracles', 'Light over darkness', 'Dedication', 'Perseverance'],
                'customs': [
                    'Lighting the chanukiah',
                    'Reciting Hallel',
                    'Eating foods fried in oil',
                    'Playing dreidel',
                    'Giving gifts or gelt'
                ],
                'special_foods': ['Latkes', 'Sufganiyot', 'Foods fried in oil'],
                'torah_readings': ['Numbers 7:1-89'],
                'haftarah': ['Zechariah 2:14-4:7'],
                'preparation': [
                    'Preparing the chanukiah',
                    'Learning the Chanukah story',
                    'Preparing traditional foods',
                    'Teaching children about the holiday'
                ]
            },
            
            'Purim': {
                'category': 'Post-Biblical',
                'duration_days': 1,
                'background': 'Commemorating the salvation of the Jewish people in ancient Persia, as recorded in the Book of Esther.',
                'themes': ['Divine providence', 'Hidden miracles', 'Courage', 'Community', 'Joy'],
                'customs': [
                    'Reading the Megillah',
                    'Wearing costumes',
                    'Giving gifts to friends (mishloach manot)',
                    'Charity to the poor',
                    'Festive meal'
                ],
                'special_foods': ['Hamantaschen', 'Festive meal foods'],
                'torah_readings': ['Exodus 17:8-16'],
                'haftarah': ['1 Samuel 15:2-34'],
                'preparation': [
                    'Preparing costumes',
                    'Preparing mishloach manot',
                    'Learning the Purim story',
                    'Planning charity giving'
                ]
            },
            
            # Fast Days
            'Tisha B\'Av': {
                'category': 'Fast Days',
                'duration_days': 1,
                'background': 'A day of mourning commemorating the destruction of both Temples and other tragedies in Jewish history.',
                'themes': ['Mourning', 'Remembrance', 'Hope for rebuilding', 'Historical consciousness', 'Resilience'],
                'customs': [
                    '25-hour fast',
                    'Reading Lamentations',
                    'Sitting on low stools',
                    'Avoiding leather shoes',
                    'Studying about the Temple'
                ],
                'special_foods': ['Pre-fast meal', 'Break-fast meal'],
                'torah_readings': ['Deuteronomy 4:25-40'],
                'haftarah': ['Jeremiah 8:13-9:23'],
                'preparation': [
                    'Learning about Temple history',
                    'Spiritual preparation',
                    'Preparing appropriate meals',
                    'Reflection on loss and hope'
                ]
            },
            
            # Modern Holidays
            'Yom HaShoah': {
                'category': 'Modern',
                'duration_days': 1,
                'background': 'Holocaust Remembrance Day, commemorating the six million Jews murdered during the Holocaust.',
                'themes': ['Remembrance', 'Never forget', 'Human dignity', 'Resistance', 'Education'],
                'customs': [
                    'Memorial ceremonies',
                    'Lighting memorial candles',
                    'Reading names of victims',
                    'Educational programs',
                    'Moment of silence'
                ],
                'special_foods': [],
                'torah_readings': [],
                'haftarah': [],
                'preparation': [
                    'Learning Holocaust history',
                    'Preparing memorial materials',
                    'Planning educational activities',
                    'Connecting with survivors'
                ]
            },
            
            'Yom HaAtzma\'ut': {
                'category': 'Modern',
                'duration_days': 1,
                'background': 'Israel Independence Day, celebrating the establishment of the State of Israel in 1948.',
                'themes': ['Independence', 'Homeland', 'Modern miracles', 'Zionism', 'Celebration'],
                'customs': [
                    'Festive celebrations',
                    'Israeli flag displays',
                    'Barbecues and picnics',
                    'Israeli music and dancing',
                    'Thanksgiving prayers'
                ],
                'special_foods': ['Israeli foods', 'Barbecue', 'Falafel', 'Hummus'],
                'torah_readings': [],
                'haftarah': [],
                'preparation': [
                    'Learning Israeli history',
                    'Preparing celebrations',
                    'Teaching about Israel',
                    'Planning festive meals'
                ]
            }
        }
    
    def generate_holiday_content(self, holiday_name: str, custom_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive content for a specific holiday
        
        Args:
            holiday_name: Name of the holiday
            custom_date: Optional custom date for the holiday
            
        Returns:
            Complete holiday content package
        """
        # Get holiday info from database
        holiday_info = self.holiday_database.get(holiday_name, {})
        
        if not holiday_info:
            return {
                'error': f'Holiday {holiday_name} not found in database',
                'available_holidays': list(self.holiday_database.keys())
            }
        
        # Get current holiday dates from calendar
        upcoming_holidays = self.calendar_manager.get_upcoming_holidays(90)
        holiday_dates = [h for h in upcoming_holidays if holiday_name.lower() in h.name.lower()]
        
        # Generate comprehensive content
        content = {
            'holiday_info': {
                'name': holiday_name,
                'category': holiday_info.get('category', ''),
                'duration_days': holiday_info.get('duration_days', 1),
                'dates': [{'date': h.date, 'hebrew_date': h.hebrew_date} for h in holiday_dates],
                'background': holiday_info.get('background', ''),
                'themes': holiday_info.get('themes', [])
            },
            'observance_guide': {
                'customs': holiday_info.get('customs', []),
                'special_foods': holiday_info.get('special_foods', []),
                'preparation': holiday_info.get('preparation', [])
            },
            'liturgy_and_readings': {
                'torah_readings': holiday_info.get('torah_readings', []),
                'haftarah': holiday_info.get('haftarah', []),
                'special_prayers': self._get_special_prayers(holiday_name)
            },
            'educational_content': {
                'historical_background': self._get_historical_background(holiday_name),
                'discussion_questions': self._generate_holiday_questions(holiday_name),
                'activities': self._get_holiday_activities(holiday_name),
                'learning_resources': self._get_learning_resources(holiday_name)
            },
            'practical_guide': {
                'preparation_timeline': self._get_preparation_timeline(holiday_name),
                'shopping_list': self._get_shopping_list(holiday_name),
                'family_activities': self._get_family_activities(holiday_name)
            },
            'generated_date': datetime.now().isoformat()
        }
        
        return content
    
    def generate_current_holiday_content(self) -> List[Dict[str, Any]]:
        """
        Generate content for all current and upcoming holidays
        
        Returns:
            List of holiday content for current period
        """
        upcoming_holidays = self.calendar_manager.get_upcoming_holidays(30)
        holiday_content = []
        
        for holiday in upcoming_holidays:
            # Try to match with our database
            for db_name in self.holiday_database.keys():
                if db_name.lower() in holiday.name.lower() or holiday.name.lower() in db_name.lower():
                    content = self.generate_holiday_content(db_name)
                    if 'error' not in content:
                        holiday_content.append(content)
                    break
        
        return holiday_content
    
    def generate_seasonal_content(self, season: str = 'current') -> Dict[str, Any]:
        """
        Generate content for seasonal Jewish observances
        
        Args:
            season: Season to generate content for ('current', 'high_holy_days', 'winter', etc.)
            
        Returns:
            Seasonal content package
        """
        current_month = date.today().month
        
        # Determine season based on Jewish calendar
        if season == 'current':
            if current_month in [9, 10]:  # September-October
                season = 'high_holy_days'
            elif current_month in [11, 12, 1]:  # November-January
                season = 'winter_holidays'
            elif current_month in [2, 3, 4]:  # February-April
                season = 'spring_festivals'
            elif current_month in [5, 6]:  # May-June
                season = 'late_spring'
            else:
                season = 'summer'
        
        seasonal_content = {
            'season_info': {
                'name': season,
                'description': self._get_seasonal_description(season),
                'themes': self._get_seasonal_themes(season)
            },
            'holidays': self._get_seasonal_holidays(season),
            'observances': self._get_seasonal_observances(season),
            'learning_focus': self._get_seasonal_learning(season),
            'generated_date': datetime.now().isoformat()
        }
        
        return seasonal_content
    
    def generate_weekly_holiday_alert(self) -> Dict[str, Any]:
        """
        Generate weekly alert for upcoming holidays and observances
        
        Returns:
            Weekly holiday alert with preparation reminders
        """
        upcoming_holidays = self.calendar_manager.get_upcoming_holidays(14)  # Next 2 weeks
        
        alerts = []
        for holiday in upcoming_holidays:
            days_until = (datetime.strptime(holiday.date, '%Y-%m-%d').date() - date.today()).days
            
            alert = {
                'holiday': holiday.name,
                'date': holiday.date,
                'hebrew_date': holiday.hebrew_date,
                'days_until': days_until,
                'urgency': 'high' if days_until <= 3 else 'medium' if days_until <= 7 else 'low',
                'preparation_needed': self._get_immediate_preparation(holiday.name, days_until)
            }
            alerts.append(alert)
        
        return {
            'week_info': {
                'start_date': date.today().strftime('%Y-%m-%d'),
                'hebrew_date': self.calendar_manager.calendar_api.get_jewish_date()
            },
            'holiday_alerts': alerts,
            'general_reminders': self._get_weekly_reminders(),
            'generated_date': datetime.now().isoformat()
        }
    
    def _get_special_prayers(self, holiday_name: str) -> List[str]:
        """Get special prayers for the holiday"""
        prayers = {
            'Rosh Hashana': ['Malchuyot', 'Zichronot', 'Shofarot', 'Avinu Malkeinu'],
            'Yom Kippur': ['Kol Nidre', 'Vidui', 'Avinu Malkeinu', 'Neilah'],
            'Sukkot': ['Hallel', 'Hoshanot'],
            'Chanukah': ['Hallel', 'Al HaNissim'],
            'Purim': ['Al HaNissim', 'Megillah reading']
        }
        return prayers.get(holiday_name, [])
    
    def _get_historical_background(self, holiday_name: str) -> str:
        """Get detailed historical background"""
        return f"Detailed historical background for {holiday_name} would be provided here, including origins, development, and significance throughout Jewish history."
    
    def _generate_holiday_questions(self, holiday_name: str) -> List[str]:
        """Generate discussion questions for the holiday"""
        general_questions = [
            f"What is the central message of {holiday_name}?",
            f"How do the customs of {holiday_name} reflect its themes?",
            f"What can we learn from {holiday_name} for our daily lives?",
            f"How has the observance of {holiday_name} evolved over time?"
        ]
        
        specific_questions = {
            'Rosh Hashana': [
                "How can we make this new year truly meaningful?",
                "What does it mean to be judged by God?",
                "How do we balance celebration with solemnity?"
            ],
            'Chanukah': [
                "What does religious freedom mean today?",
                "How do we find light in dark times?",
                "What miracles do we see in our own lives?"
            ]
        }
        
        questions = general_questions.copy()
        if holiday_name in specific_questions:
            questions.extend(specific_questions[holiday_name])
        
        return questions
    
    def _get_holiday_activities(self, holiday_name: str) -> List[str]:
        """Get activities for the holiday"""
        return [
            f"Family discussions about {holiday_name} themes",
            f"Creative projects related to {holiday_name}",
            f"Community service reflecting {holiday_name} values",
            f"Learning activities about {holiday_name} history"
        ]
    
    def _get_learning_resources(self, holiday_name: str) -> List[str]:
        """Get learning resources for the holiday"""
        return [
            f"Traditional texts about {holiday_name}",
            f"Modern commentaries on {holiday_name}",
            f"Historical sources about {holiday_name}",
            f"Educational videos and materials"
        ]
    
    def _get_preparation_timeline(self, holiday_name: str) -> List[Dict[str, str]]:
        """Get preparation timeline for the holiday"""
        return [
            {"timeframe": "2 weeks before", "tasks": "Begin learning and spiritual preparation"},
            {"timeframe": "1 week before", "tasks": "Complete shopping and major preparations"},
            {"timeframe": "Day before", "tasks": "Final preparations and spiritual readiness"},
            {"timeframe": "Day of", "tasks": "Focus on observance and celebration"}
        ]
    
    def _get_shopping_list(self, holiday_name: str) -> List[str]:
        """Get shopping list for the holiday"""
        holiday_info = self.holiday_database.get(holiday_name, {})
        foods = holiday_info.get('special_foods', [])
        
        general_items = ["Candles", "Wine/grape juice", "Special foods"]
        return general_items + foods
    
    def _get_family_activities(self, holiday_name: str) -> List[str]:
        """Get family activities for the holiday"""
        return [
            f"Tell the story of {holiday_name}",
            f"Prepare traditional {holiday_name} foods together",
            f"Create {holiday_name} decorations",
            f"Discuss {holiday_name} themes as a family"
        ]
    
    def _get_seasonal_description(self, season: str) -> str:
        """Get description of the season"""
        descriptions = {
            'high_holy_days': 'The period of Rosh Hashana and Yom Kippur, focusing on repentance and renewal',
            'winter_holidays': 'The joyous winter festivals of Chanukah and Tu BiShvat',
            'spring_festivals': 'The liberation celebration of Pesach and counting of the Omer',
            'late_spring': 'The culmination with Shavuot and the giving of the Torah'
        }
        return descriptions.get(season, f'The {season} period in the Jewish calendar')
    
    def _get_seasonal_themes(self, season: str) -> List[str]:
        """Get themes for the season"""
        themes = {
            'high_holy_days': ['Repentance', 'Renewal', 'Judgment', 'Forgiveness'],
            'winter_holidays': ['Light', 'Miracles', 'Perseverance', 'Growth'],
            'spring_festivals': ['Freedom', 'Liberation', 'Renewal', 'Growth'],
            'late_spring': ['Torah', 'Learning', 'Revelation', 'Commitment']
        }
        return themes.get(season, ['Spiritual growth', 'Community', 'Tradition'])
    
    def _get_seasonal_holidays(self, season: str) -> List[str]:
        """Get holidays for the season"""
        holidays = {
            'high_holy_days': ['Rosh Hashana', 'Yom Kippur', 'Sukkot'],
            'winter_holidays': ['Chanukah', 'Tu BiShvat'],
            'spring_festivals': ['Pesach', 'Yom HaShoah', 'Yom HaZikaron', 'Yom HaAtzma\'ut'],
            'late_spring': ['Lag B\'Omer', 'Shavuot']
        }
        return holidays.get(season, [])
    
    def _get_seasonal_observances(self, season: str) -> List[str]:
        """Get special observances for the season"""
        return [
            f"Special {season} customs and traditions",
            f"Seasonal learning and study",
            f"Community {season} events"
        ]
    
    def _get_seasonal_learning(self, season: str) -> List[str]:
        """Get learning focus for the season"""
        return [
            f"Study themes relevant to {season}",
            f"Traditional texts for {season}",
            f"Modern insights on {season} observances"
        ]
    
    def _get_immediate_preparation(self, holiday_name: str, days_until: int) -> List[str]:
        """Get immediate preparation tasks based on days until holiday"""
        if days_until <= 1:
            return ["Final preparations", "Spiritual readiness", "Last-minute shopping"]
        elif days_until <= 3:
            return ["Complete major preparations", "Begin spiritual preparation", "Confirm plans"]
        elif days_until <= 7:
            return ["Begin preparations", "Plan observance", "Learn about the holiday"]
        else:
            return ["Start thinking about the holiday", "Begin learning", "Mark calendar"]
    
    def _get_weekly_reminders(self) -> List[str]:
        """Get general weekly reminders"""
        return [
            "Check upcoming Jewish calendar events",
            "Prepare for Shabbat",
            "Consider weekly learning goals",
            "Plan family Jewish activities"
        ]


# Testing function
def test_holiday_content_generator():
    """Test the holiday content generator"""
    print("Testing Holiday Content Generator...")
    
    generator = HolidayContentGenerator()
    
    try:
        # Test specific holiday content
        print("\n1. Generating Rosh Hashana Content...")
        rosh_hashana_content = generator.generate_holiday_content('Rosh Hashana')
        print(f"Generated content for: {rosh_hashana_content['holiday_info']['name']}")
        print(f"Category: {rosh_hashana_content['holiday_info']['category']}")
        print(f"Number of themes: {len(rosh_hashana_content['holiday_info']['themes'])}")
        print(f"Number of customs: {len(rosh_hashana_content['observance_guide']['customs'])}")
        
        # Test current holiday content
        print("\n2. Generating Current Holiday Content...")
        current_holidays = generator.generate_current_holiday_content()
        print(f"Found {len(current_holidays)} upcoming holidays with content")
        
        # Test weekly holiday alert
        print("\n3. Generating Weekly Holiday Alert...")
        weekly_alert = generator.generate_weekly_holiday_alert()
        print(f"Hebrew date: {weekly_alert['week_info']['hebrew_date']}")
        print(f"Number of holiday alerts: {len(weekly_alert['holiday_alerts'])}")
        
        # Test seasonal content
        print("\n4. Generating Seasonal Content...")
        seasonal_content = generator.generate_seasonal_content()
        print(f"Season: {seasonal_content['season_info']['name']}")
        print(f"Description: {seasonal_content['season_info']['description']}")
        
        print("\nHoliday content generator test completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")


if __name__ == "__main__":
    test_holiday_content_generator()

