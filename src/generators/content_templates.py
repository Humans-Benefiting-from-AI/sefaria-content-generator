"""
Content Generation Templates for Sefaria Integration Tool

This module provides templates and utilities for generating various types
of content based on Sefaria sources.

Author: Manus AI Assistant
Date: September 2025
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
from datetime import datetime


@dataclass
class ContentTemplate:
    """Base class for content templates"""
    name: str
    description: str
    required_fields: List[str]
    optional_fields: List[str] = None
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate that required fields are present in data"""
        return all(field in data for field in self.required_fields)


class WeeklyParashaTemplate:
    """Template for generating weekly Torah portion content"""
    
    @staticmethod
    def generate(parasha_data: Dict[str, Any]) -> str:
        """Generate weekly parasha content"""
        template = f"""
# Weekly Torah Portion: {parasha_data.get('name', 'Unknown')}

## Torah Reading
**Reference:** {parasha_data.get('torah_ref', '')}

### Hebrew Text
{parasha_data.get('hebrew_text', '')}

### English Translation
{parasha_data.get('english_text', '')}

## Key Themes
{chr(10).join(f"- {theme}" for theme in parasha_data.get('themes', []))}

## Commentary Highlights
"""
        
        for commentary in parasha_data.get('commentaries', []):
            template += f"""
### {commentary.get('title', 'Commentary')}
{commentary.get('text', '')}

"""
        
        template += f"""
## Study Questions
{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(parasha_data.get('study_questions', [])))}

## Additional Resources
{chr(10).join(f"- [{res.get('title', 'Resource')}]({res.get('url', '#')})" for res in parasha_data.get('resources', []))}

---
*Generated on {datetime.now().strftime('%B %d, %Y')}*
"""
        return template


class DailyStudyTemplate:
    """Template for daily study content"""
    
    @staticmethod
    def generate(study_data: Dict[str, Any]) -> str:
        """Generate daily study content"""
        template = f"""
# Daily Study - {study_data.get('date', datetime.now().strftime('%B %d, %Y'))}

## Today's Text
**Reference:** {study_data.get('ref', '')}

### Original Text
{study_data.get('original_text', '')}

### Translation
{study_data.get('translation', '')}

## Reflection
{study_data.get('reflection', '')}

## Key Insight
{study_data.get('key_insight', '')}

## Connection to Daily Life
{study_data.get('daily_connection', '')}

## Related Sources
"""
        
        for source in study_data.get('related_sources', []):
            template += f"- **{source.get('ref', '')}:** {source.get('text', '')}\n"
        
        template += f"""
## Tomorrow's Preview
{study_data.get('tomorrow_preview', '')}

---
*Part of your daily Jewish learning journey*
"""
        return template


class CommentaryComparisonTemplate:
    """Template for comparing different commentaries"""
    
    @staticmethod
    def generate(comparison_data: Dict[str, Any]) -> str:
        """Generate commentary comparison content"""
        template = f"""
# Commentary Comparison: {comparison_data.get('ref', '')}

## Source Text
{comparison_data.get('source_text', '')}

## Commentary Analysis
"""
        
        for commentary in comparison_data.get('commentaries', []):
            template += f"""
### {commentary.get('author', 'Unknown Author')} ({commentary.get('period', 'Unknown Period')})

**Approach:** {commentary.get('approach', '')}

**Key Points:**
{chr(10).join(f"- {point}" for point in commentary.get('key_points', []))}

**Full Text:**
{commentary.get('full_text', '')}

**Unique Perspective:**
{commentary.get('unique_perspective', '')}

---
"""
        
        template += f"""
## Synthesis
{comparison_data.get('synthesis', '')}

## Modern Applications
{comparison_data.get('modern_applications', '')}

## Discussion Questions
{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(comparison_data.get('discussion_questions', [])))}
"""
        return template


class TopicalStudyTemplate:
    """Template for topical study guides"""
    
    @staticmethod
    def generate(topic_data: Dict[str, Any]) -> str:
        """Generate topical study content"""
        template = f"""
# Topical Study: {topic_data.get('topic', 'Unknown Topic')}

## Introduction
{topic_data.get('introduction', '')}

## Key Sources
"""
        
        for i, source in enumerate(topic_data.get('sources', []), 1):
            template += f"""
### Source {i}: {source.get('ref', '')}

**Text:**
{source.get('text', '')}

**Context:**
{source.get('context', '')}

**Relevance to Topic:**
{source.get('relevance', '')}

"""
        
        template += f"""
## Thematic Analysis
{topic_data.get('thematic_analysis', '')}

## Historical Development
{topic_data.get('historical_development', '')}

## Contemporary Relevance
{topic_data.get('contemporary_relevance', '')}

## Further Exploration
{chr(10).join(f"- {item}" for item in topic_data.get('further_exploration', []))}

## Bibliography
{chr(10).join(f"- {ref}" for ref in topic_data.get('bibliography', []))}
"""
        return template


class SourceSheetTemplate:
    """Template for creating source sheets"""
    
    @staticmethod
    def generate(sheet_data: Dict[str, Any]) -> str:
        """Generate source sheet content"""
        template = f"""
# {sheet_data.get('title', 'Source Sheet')}

**Created:** {sheet_data.get('date', datetime.now().strftime('%B %d, %Y'))}
**Topic:** {sheet_data.get('topic', '')}
**Audience:** {sheet_data.get('audience', 'General')}

## Introduction
{sheet_data.get('introduction', '')}

## Sources
"""
        
        for i, source in enumerate(sheet_data.get('sources', []), 1):
            template += f"""
### {i}. {source.get('ref', '')}

{source.get('text', '')}

**Commentary:**
{source.get('commentary', '')}

"""
        
        template += f"""
## Discussion Questions
{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(sheet_data.get('discussion_questions', [])))}

## Conclusion
{sheet_data.get('conclusion', '')}

## Additional Resources
{chr(10).join(f"- {resource}" for resource in sheet_data.get('additional_resources', []))}

---
*This source sheet was created using the Sefaria Integration Tool*
"""
        return template


class HolidayGuideTemplate:
    """Template for holiday study guides"""
    
    @staticmethod
    def generate(holiday_data: Dict[str, Any]) -> str:
        """Generate holiday guide content"""
        template = f"""
# {holiday_data.get('holiday_name', 'Holiday')} Study Guide

## Overview
**Date:** {holiday_data.get('date', '')}
**Duration:** {holiday_data.get('duration', '')}
**Significance:** {holiday_data.get('significance', '')}

## Historical Background
{holiday_data.get('historical_background', '')}

## Key Texts and Sources
"""
        
        for source in holiday_data.get('key_sources', []):
            template += f"""
### {source.get('title', 'Source')}
**Reference:** {source.get('ref', '')}

{source.get('text', '')}

**Explanation:**
{source.get('explanation', '')}

"""
        
        template += f"""
## Customs and Practices
{chr(10).join(f"- **{custom.get('name', '')}:** {custom.get('description', '')}" for custom in holiday_data.get('customs', []))}

## Liturgy and Prayers
{chr(10).join(f"- {prayer}" for prayer in holiday_data.get('liturgy', []))}

## Modern Observance
{holiday_data.get('modern_observance', '')}

## Family Activities
{chr(10).join(f"- {activity}" for activity in holiday_data.get('family_activities', []))}

## Reflection Questions
{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(holiday_data.get('reflection_questions', [])))}

## Additional Reading
{chr(10).join(f"- {reading}" for reading in holiday_data.get('additional_reading', []))}
"""
        return template


class ContentGenerator:
    """Main content generator using templates"""
    
    def __init__(self):
        self.templates = {
            'weekly_parasha': WeeklyParashaTemplate,
            'daily_study': DailyStudyTemplate,
            'commentary_comparison': CommentaryComparisonTemplate,
            'topical_study': TopicalStudyTemplate,
            'source_sheet': SourceSheetTemplate,
            'holiday_guide': HolidayGuideTemplate
        }
    
    def generate_content(self, template_type: str, data: Dict[str, Any]) -> str:
        """
        Generate content using specified template
        
        Args:
            template_type: Type of template to use
            data: Data to populate template with
            
        Returns:
            Generated content as string
        """
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")
        
        template_class = self.templates[template_type]
        return template_class.generate(data)
    
    def get_available_templates(self) -> List[str]:
        """Get list of available template types"""
        return list(self.templates.keys())
    
    def export_content(self, content: str, filename: str, format_type: str = 'markdown') -> str:
        """
        Export generated content to file
        
        Args:
            content: Generated content
            filename: Output filename
            format_type: Export format (markdown, html, json)
            
        Returns:
            Path to exported file
        """
        if format_type == 'markdown':
            filepath = f"{filename}.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        elif format_type == 'html':
            filepath = f"{filename}.html"
            html_content = self._markdown_to_html(content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
        elif format_type == 'json':
            filepath = f"{filename}.json"
            json_data = {
                'content': content,
                'generated_at': datetime.now().isoformat(),
                'format': 'markdown'
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
        
        return filepath
    
    def _markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown to basic HTML"""
        # Basic markdown to HTML conversion
        html = markdown_content
        
        # Headers
        html = html.replace('# ', '<h1>').replace('\n# ', '</h1>\n<h1>')
        html = html.replace('## ', '<h2>').replace('\n## ', '</h2>\n<h2>')
        html = html.replace('### ', '<h3>').replace('\n### ', '</h3>\n<h3>')
        
        # Bold and italic
        html = html.replace('**', '<strong>').replace('**', '</strong>')
        html = html.replace('*', '<em>').replace('*', '</em>')
        
        # Line breaks
        html = html.replace('\n\n', '</p>\n<p>')
        
        # Wrap in basic HTML structure
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Sefaria Content</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        .hebrew {{ direction: rtl; font-family: 'Times New Roman', serif; }}
    </style>
</head>
<body>
<p>{html}</p>
</body>
</html>"""
        
        return html


# Example usage
if __name__ == "__main__":
    generator = ContentGenerator()
    
    # Example data for testing
    sample_data = {
        'title': 'Sample Source Sheet',
        'topic': 'Creation',
        'introduction': 'This source sheet explores the theme of creation in Jewish texts.',
        'sources': [
            {
                'ref': 'Genesis 1:1',
                'text': 'In the beginning, God created the heavens and the earth.',
                'commentary': 'This opening verse establishes the fundamental principle of divine creation.'
            }
        ],
        'discussion_questions': [
            'What does this teach us about the nature of creation?',
            'How does this relate to our daily lives?'
        ],
        'conclusion': 'The theme of creation reminds us of our role as partners in ongoing creation.'
    }
    
    content = generator.generate_content('source_sheet', sample_data)
    print("Generated content preview:")
    print(content[:500] + "...")
    
    print(f"\nAvailable templates: {generator.get_available_templates()}")

