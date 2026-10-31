import logging
"""
Torah Calendar API Routes

Flask routes for the Torah calendar web interface providing
Torah readings, holiday information, and calendar events.

Author: Manus AI Assistant
Date: September 2025
"""

import sys
import os
sys.path.append('/home/ubuntu/torah-calendar-tool')

from flask import Blueprint, jsonify, request
from datetime import datetime, date
import json

# Import our Torah calendar modules
from src.jewish_calendar import TorahCalendarManager, JewishCalendarAPI
from src.torah_content_generator import TorahContentGenerator
from src.holiday_content_generator import HolidayContentGenerator

# Create blueprint
torah_api = Blueprint('torah_api', __name__, url_prefix='/api')

# Initialize generators
calendar_manager = TorahCalendarManager()
torah_generator = TorahContentGenerator()
holiday_generator = HolidayContentGenerator()


@torah_api.route('/current-torah-reading', methods=['GET'])
def get_current_torah_reading():
    """Get the current week's Torah reading"""
    try:
        torah_reading = calendar_manager.calendar_api.get_current_torah_reading()
        
        if torah_reading:
            return jsonify({
                'success': True,
                'torah_reading': {
                    'name': torah_reading.name,
                    'hebrew_name': torah_reading.hebrew_name,
                    'date': torah_reading.date,
                    'hebrew_date': torah_reading.hebrew_date,
                    'torah_portion': torah_reading.torah_portion,
                    'haftarah': torah_reading.haftarah,
                    'aliyot': torah_reading.aliyot,
                    'link': torah_reading.link
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No Torah reading found for current week'
            })
            
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/weekly-torah-guide', methods=['GET'])
def get_weekly_torah_guide():
    """Get comprehensive weekly Torah study guide"""
    try:
        weekly_guide = torah_generator.generate_weekly_torah_guide()
        
        if 'error' not in weekly_guide:
            return jsonify({
                'success': True,
                'guide': weekly_guide
            })
        else:
            return jsonify({
                'success': False,
                'error': weekly_guide['error']
            })
            
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/weekly-calendar-summary', methods=['GET'])
def get_weekly_calendar_summary():
    """Get comprehensive weekly calendar summary"""
    try:
        weekly_summary = torah_generator.generate_weekly_calendar_summary()
        
        return jsonify({
            'success': True,
            'summary': weekly_summary
        })
        
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/upcoming-holidays', methods=['GET'])
def get_upcoming_holidays():
    """Get upcoming Jewish holidays"""
    try:
        days_ahead = request.args.get('days', 60, type=int)
        holidays = calendar_manager.get_upcoming_holidays(days_ahead)
        
        holiday_list = []
        for holiday in holidays:
            holiday_list.append({
                'name': holiday.name,
                'hebrew_name': holiday.hebrew_name,
                'date': holiday.date,
                'hebrew_date': holiday.hebrew_date,
                'category': holiday.category,
                'subcategory': holiday.subcategory,
                'description': holiday.description,
                'is_yom_tov': holiday.is_yom_tov,
                'link': holiday.link
            })
        
        return jsonify({
            'success': True,
            'holidays': holiday_list
        })
        
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/holiday-content/<holiday_name>', methods=['GET'])
def get_holiday_content(holiday_name):
    """Get comprehensive content for a specific holiday"""
    try:
        holiday_content = holiday_generator.generate_holiday_content(holiday_name)
        
        if 'error' not in holiday_content:
            return jsonify({
                'success': True,
                'content': holiday_content
            })
        else:
            return jsonify({
                'success': False,
                'error': holiday_content['error'],
                'available_holidays': holiday_content.get('available_holidays', [])
            })
            
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/current-holiday-content', methods=['GET'])
def get_current_holiday_content():
    """Get content for all current and upcoming holidays"""
    try:
        holiday_content = holiday_generator.generate_current_holiday_content()
        
        return jsonify({
            'success': True,
            'holiday_content': holiday_content
        })
        
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/weekly-holiday-alert', methods=['GET'])
def get_weekly_holiday_alert():
    """Get weekly holiday alerts and reminders"""
    try:
        weekly_alert = holiday_generator.generate_weekly_holiday_alert()
        
        return jsonify({
            'success': True,
            'alert': weekly_alert
        })
        
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/seasonal-content', methods=['GET'])
def get_seasonal_content():
    """Get seasonal Jewish content"""
    try:
        season = request.args.get('season', 'current')
        seasonal_content = holiday_generator.generate_seasonal_content(season)
        
        return jsonify({
            'success': True,
            'content': seasonal_content
        })
        
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/hebrew-date', methods=['GET'])
def get_hebrew_date():
    """Get current Hebrew date"""
    try:
        gregorian_date = request.args.get('date')
        if gregorian_date:
            hebrew_date = calendar_manager.calendar_api.get_jewish_date(gregorian_date)
        else:
            hebrew_date = calendar_manager.calendar_api.get_jewish_date()
        
        return jsonify({
            'success': True,
            'hebrew_date': hebrew_date,
            'gregorian_date': gregorian_date or date.today().strftime('%Y-%m-%d')
        })
        
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/torah-reading-for-date', methods=['GET'])
def get_torah_reading_for_date():
    """Get Torah reading for a specific date"""
    try:
        target_date = request.args.get('date')
        if not target_date:
            return jsonify({
                'success': False,
                'error': 'Date parameter is required'
            }), 400
        
        torah_reading = calendar_manager.calendar_api.get_torah_reading_for_date(target_date)
        
        if torah_reading:
            return jsonify({
                'success': True,
                'torah_reading': {
                    'name': torah_reading.name,
                    'hebrew_name': torah_reading.hebrew_name,
                    'date': torah_reading.date,
                    'hebrew_date': torah_reading.hebrew_date,
                    'torah_portion': torah_reading.torah_portion,
                    'haftarah': torah_reading.haftarah,
                    'aliyot': torah_reading.aliyot,
                    'link': torah_reading.link
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'No Torah reading found for date {target_date}'
            })
            
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/upcoming-torah-readings', methods=['GET'])
def get_upcoming_torah_readings():
    """Get upcoming Torah readings"""
    try:
        weeks = request.args.get('weeks', 4, type=int)
        torah_readings = calendar_manager.calendar_api.get_upcoming_torah_readings(weeks)
        
        readings_list = []
        for reading in torah_readings:
            readings_list.append({
                'name': reading.name,
                'hebrew_name': reading.hebrew_name,
                'date': reading.date,
                'hebrew_date': reading.hebrew_date,
                'torah_portion': reading.torah_portion,
                'haftarah': reading.haftarah
            })
        
        return jsonify({
            'success': True,
            'torah_readings': readings_list
        })
        
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/available-holidays', methods=['GET'])
def get_available_holidays():
    """Get list of available holidays in the database"""
    try:
        available_holidays = list(holiday_generator.holiday_database.keys())
        
        return jsonify({
            'success': True,
            'holidays': available_holidays
        })
        
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@torah_api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'Torah Calendar API is running',
        'timestamp': datetime.now().isoformat()
    })

