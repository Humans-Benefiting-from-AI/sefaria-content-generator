"""
Advanced Content Generator for Sefaria Integration Tool

This module provides sophisticated content generation capabilities
using Sefaria sources, including AI-powered analysis and multiple output formats.

Author: Manus AI Assistant
Date: September 2025
"""

import openai
from typing import Dict, List, Any, Optional, Tuple
import json
import re
from datetime import datetime, timedelta
import random
from sefaria_integration import SefariaAPIClient, SefariaContentGenerator
from content_templates import ContentGenerator


class AIContentAnalyzer:
    """AI-powered content analysis using OpenAI"""
    
    def __init__(self):
        """Initialize the AI content analyzer"""
        # OpenAI client is already configured via environment variables
        self.client = openai.OpenAI()
    
    def analyze_text_themes(self, text: str, context: str = "") -> List[str]:
        """
        Analyze text to extract key themes using AI
        
        Args:
            text: Text to analyze
            context: Additional context about the text
            
        Returns:
            List of identified themes
        """
        prompt = f"""
        Analyze the following Jewish text and identify the key themes and concepts:
        
        Text: {text}
        Context: {context}
        
        Please provide a list of 3-5 key themes, focusing on:
        - Theological concepts
        - Ethical teachings
        - Historical significance
        - Literary elements
        - Practical applications
        
        Return only the themes as a simple list, one per line.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )
            
            themes = response.choices[0].message.content.strip().split('\n')
            return [theme.strip('- ').strip() for theme in themes if theme.strip()]
            
        except Exception as e:
            print(f"Error in AI theme analysis: {e}")
            return ["Divine providence", "Human responsibility", "Textual interpretation"]
    
    def generate_commentary(self, text: str, style: str = "modern") -> str:
        """
        Generate AI commentary on a text
        
        Args:
            text: Text to comment on
            style: Commentary style (modern, traditional, academic)
            
        Returns:
            Generated commentary
        """
        style_prompts = {
            "modern": "Provide a modern, accessible commentary that relates to contemporary life",
            "traditional": "Provide commentary in the style of classical Jewish commentators",
            "academic": "Provide scholarly, academic analysis with historical context"
        }
        
        prompt = f"""
        {style_prompts.get(style, style_prompts['modern'])}:
        
        Text: {text}
        
        Please provide insightful commentary that:
        - Explains difficult concepts
        - Provides historical context
        - Draws practical lessons
        - Connects to broader Jewish thought
        
        Keep the commentary concise but meaningful (2-3 paragraphs).
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.4
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error in AI commentary generation: {e}")
            return "This text invites deep reflection on its meaning and application to our lives."
    
    def create_study_questions(self, text: str, level: str = "intermediate") -> List[str]:
        """
        Generate study questions using AI
        
        Args:
            text: Text to create questions for
            level: Difficulty level (beginner, intermediate, advanced)
            
        Returns:
            List of study questions
        """
        level_descriptions = {
            "beginner": "basic comprehension and simple application",
            "intermediate": "analysis, interpretation, and connections",
            "advanced": "critical thinking, synthesis, and complex applications"
        }
        
        prompt = f"""
        Create 5-7 study questions for the following Jewish text, appropriate for {level} level students.
        Focus on {level_descriptions.get(level, level_descriptions['intermediate'])}.
        
        Text: {text}
        
        Questions should encourage:
        - Deep thinking about the text's meaning
        - Personal reflection and application
        - Connection to broader Jewish concepts
        - Discussion and debate
        
        Return only the questions, numbered 1-7.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.5
            )
            
            questions = response.choices[0].message.content.strip().split('\n')
            return [q.strip() for q in questions if q.strip() and any(c.isdigit() for c in q[:3])]
            
        except Exception as e:
            print(f"Error in AI question generation: {e}")
            return [
                "What is the main message of this text?",
                "How does this relate to your personal experience?",
                "What questions does this text raise for you?"
            ]


class AdvancedContentGenerator:
    """Advanced content generator with AI capabilities"""
    
    def __init__(self, sefaria_client: SefariaAPIClient):
        """
        Initialize advanced content generator
        
        Args:
            sefaria_client: Sefaria API client instance
        """
        self.sefaria = sefaria_client
        self.basic_generator = SefariaContentGenerator(sefaria_client)
        self.template_generator = ContentGenerator()
        self.ai_analyzer = AIContentAnalyzer()
    
    def create_comprehensive_study_guide(self, ref: str, 
                                       include_ai_analysis: bool = True,
                                       difficulty_level: str = "intermediate") -> Dict[str, Any]:
        """
        Create a comprehensive study guide with AI enhancements
        
        Args:
            ref: Text reference
            include_ai_analysis: Whether to include AI-generated content
            difficulty_level: Target difficulty level
            
        Returns:
            Comprehensive study guide data
        """
        # Get basic text and related content
        main_text = self.sefaria.get_text(ref)
        related = self.sefaria.get_related(ref)
        
        # Build comprehensive guide
        guide_data = {
            'reference': ref,
            'main_text': {
                'content': main_text.get_text_content(),
                'language': main_text.language,
                'version': main_text.version_title,
                'source': main_text.version_source
            },
            'metadata': {
                'created_date': datetime.now().isoformat(),
                'difficulty_level': difficulty_level,
                'ai_enhanced': include_ai_analysis
            }
        }
        
        if include_ai_analysis:
            # AI-generated themes
            guide_data['themes'] = self.ai_analyzer.analyze_text_themes(
                main_text.get_text_content(), 
                f"This is from {ref}"
            )
            
            # AI-generated commentary
            guide_data['ai_commentary'] = self.ai_analyzer.generate_commentary(
                main_text.get_text_content(), 
                "modern"
            )
            
            # AI-generated study questions
            guide_data['study_questions'] = self.ai_analyzer.create_study_questions(
                main_text.get_text_content(), 
                difficulty_level
            )
        
        # Add related sources
        guide_data['related_sources'] = []
        for link in related.links[:5]:
            if 'sourceRef' in link:
                try:
                    related_text = self.sefaria.get_text(link['sourceRef'])
                    guide_data['related_sources'].append({
                        'ref': link['sourceRef'],
                        'text': related_text.get_text_content()[:200] + "...",
                        'relationship': link.get('type', 'related'),
                        'category': link.get('category', 'Unknown')
                    })
                except:
                    continue
        
        # Add topics
        guide_data['topics'] = []
        for topic in related.topics[:3]:
            guide_data['topics'].append({
                'name': topic.get('topic', ''),
                'description': topic.get('description', ''),
                'slug': topic.get('slug', '')
            })
        
        return guide_data
    
    def create_thematic_collection(self, theme: str, max_sources: int = 10) -> Dict[str, Any]:
        """
        Create a thematic collection of sources
        
        Args:
            theme: Theme to search for
            max_sources: Maximum number of sources to include
            
        Returns:
            Thematic collection data
        """
        # Search for sources related to the theme
        search_results = self.sefaria.search_texts(theme)
        
        collection_data = {
            'theme': theme,
            'created_date': datetime.now().isoformat(),
            'sources': [],
            'ai_analysis': {}
        }
        
        # Process search results
        if 'hits' in search_results:
            for hit in search_results['hits'][:max_sources]:
                try:
                    ref = hit.get('ref', '')
                    if ref:
                        text = self.sefaria.get_text(ref)
                        collection_data['sources'].append({
                            'ref': ref,
                            'text': text.get_text_content(),
                            'language': text.language,
                            'relevance_score': hit.get('score', 0)
                        })
                except:
                    continue
        
        # AI analysis of the collection
        if collection_data['sources']:
            combined_text = " ".join([s['text'][:100] for s in collection_data['sources']])
            collection_data['ai_analysis'] = {
                'themes': self.ai_analyzer.analyze_text_themes(combined_text, f"Collection about {theme}"),
                'overview': self.ai_analyzer.generate_commentary(combined_text, "academic")
            }
        
        return collection_data
    
    def create_comparative_analysis(self, refs: List[str], 
                                  analysis_focus: str = "themes") -> Dict[str, Any]:
        """
        Create comparative analysis of multiple texts
        
        Args:
            refs: List of text references to compare
            analysis_focus: Focus of analysis (themes, style, content)
            
        Returns:
            Comparative analysis data
        """
        analysis_data = {
            'references': refs,
            'focus': analysis_focus,
            'created_date': datetime.now().isoformat(),
            'texts': [],
            'comparison': {}
        }
        
        # Gather texts
        for ref in refs:
            try:
                text = self.sefaria.get_text(ref)
                analysis_data['texts'].append({
                    'ref': ref,
                    'content': text.get_text_content(),
                    'language': text.language,
                    'version': text.version_title
                })
            except:
                continue
        
        # AI-powered comparison
        if len(analysis_data['texts']) >= 2:
            combined_prompt = f"Compare these Jewish texts focusing on {analysis_focus}:\n\n"
            for i, text_data in enumerate(analysis_data['texts'], 1):
                combined_prompt += f"Text {i} ({text_data['ref']}): {text_data['content'][:200]}...\n\n"
            
            analysis_data['comparison'] = {
                'similarities': self._extract_similarities(analysis_data['texts']),
                'differences': self._extract_differences(analysis_data['texts']),
                'ai_synthesis': self.ai_analyzer.generate_commentary(combined_prompt, "academic")
            }
        
        return analysis_data
    
    def create_learning_pathway(self, starting_ref: str, 
                              pathway_length: int = 7) -> Dict[str, Any]:
        """
        Create a progressive learning pathway
        
        Args:
            starting_ref: Starting text reference
            pathway_length: Number of texts in pathway
            
        Returns:
            Learning pathway data
        """
        pathway_data = {
            'starting_ref': starting_ref,
            'pathway_length': pathway_length,
            'created_date': datetime.now().isoformat(),
            'pathway': [],
            'learning_objectives': []
        }
        
        current_ref = starting_ref
        visited_refs = set()
        
        for step in range(pathway_length):
            if current_ref in visited_refs:
                break
            
            visited_refs.add(current_ref)
            
            try:
                # Get current text
                text = self.sefaria.get_text(current_ref)
                related = self.sefaria.get_related(current_ref)
                
                # Add to pathway
                step_data = {
                    'step': step + 1,
                    'ref': current_ref,
                    'text': text.get_text_content(),
                    'learning_focus': self._determine_learning_focus(text.get_text_content()),
                    'key_concepts': self.ai_analyzer.analyze_text_themes(text.get_text_content())[:3]
                }
                
                pathway_data['pathway'].append(step_data)
                
                # Find next text in pathway
                if related.links:
                    # Choose next text based on relevance and progression
                    next_candidates = [link['sourceRef'] for link in related.links 
                                     if 'sourceRef' in link and link['sourceRef'] not in visited_refs]
                    if next_candidates:
                        current_ref = next_candidates[0]  # Take first available
                    else:
                        break
                else:
                    break
                    
            except:
                break
        
        # Generate learning objectives
        if pathway_data['pathway']:
            all_concepts = []
            for step in pathway_data['pathway']:
                all_concepts.extend(step['key_concepts'])
            
            pathway_data['learning_objectives'] = list(set(all_concepts))[:5]
        
        return pathway_data
    
    def _extract_similarities(self, texts: List[Dict[str, Any]]) -> List[str]:
        """Extract similarities between texts"""
        # Simple keyword-based similarity detection
        similarities = []
        
        # Common themes
        common_words = ['God', 'Torah', 'Israel', 'commandment', 'righteousness']
        for word in common_words:
            if all(word.lower() in text['content'].lower() for text in texts):
                similarities.append(f"All texts mention {word}")
        
        return similarities[:3]
    
    def _extract_differences(self, texts: List[Dict[str, Any]]) -> List[str]:
        """Extract differences between texts"""
        differences = []
        
        # Language differences
        languages = set(text['language'] for text in texts)
        if len(languages) > 1:
            differences.append(f"Texts are in different languages: {', '.join(languages)}")
        
        # Length differences
        lengths = [len(text['content']) for text in texts]
        if max(lengths) > 2 * min(lengths):
            differences.append("Texts vary significantly in length")
        
        return differences[:3]
    
    def _determine_learning_focus(self, text: str) -> str:
        """Determine the learning focus for a text"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['law', 'commandment', 'statute']):
            return "Legal/Halakhic"
        elif any(word in text_lower for word in ['story', 'narrative', 'said']):
            return "Narrative/Aggadic"
        elif any(word in text_lower for word in ['prayer', 'blessing', 'praise']):
            return "Liturgical"
        elif any(word in text_lower for word in ['wisdom', 'understanding', 'knowledge']):
            return "Wisdom Literature"
        else:
            return "General Study"
    
    def export_to_multiple_formats(self, content_data: Dict[str, Any], 
                                 base_filename: str) -> Dict[str, str]:
        """
        Export content to multiple formats
        
        Args:
            content_data: Content data to export
            base_filename: Base filename for exports
            
        Returns:
            Dictionary mapping format to filepath
        """
        exports = {}
        
        # JSON export
        json_path = f"{base_filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(content_data, f, indent=2, ensure_ascii=False)
        exports['json'] = json_path
        
        # Markdown export
        if 'reference' in content_data:  # Study guide format
            markdown_content = self._convert_study_guide_to_markdown(content_data)
        elif 'theme' in content_data:  # Thematic collection format
            markdown_content = self._convert_collection_to_markdown(content_data)
        else:
            markdown_content = self._convert_generic_to_markdown(content_data)
        
        md_path = f"{base_filename}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        exports['markdown'] = md_path
        
        return exports
    
    def _convert_study_guide_to_markdown(self, data: Dict[str, Any]) -> str:
        """Convert study guide data to markdown"""
        md = f"# Study Guide: {data['reference']}\n\n"
        
        if 'main_text' in data:
            md += f"## Text\n{data['main_text']['content']}\n\n"
        
        if 'themes' in data:
            md += "## Key Themes\n"
            for theme in data['themes']:
                md += f"- {theme}\n"
            md += "\n"
        
        if 'ai_commentary' in data:
            md += f"## Commentary\n{data['ai_commentary']}\n\n"
        
        if 'study_questions' in data:
            md += "## Study Questions\n"
            for i, question in enumerate(data['study_questions'], 1):
                md += f"{i}. {question}\n"
            md += "\n"
        
        return md
    
    def _convert_collection_to_markdown(self, data: Dict[str, Any]) -> str:
        """Convert thematic collection to markdown"""
        md = f"# Thematic Collection: {data['theme']}\n\n"
        
        if 'ai_analysis' in data and 'overview' in data['ai_analysis']:
            md += f"## Overview\n{data['ai_analysis']['overview']}\n\n"
        
        md += "## Sources\n"
        for i, source in enumerate(data['sources'], 1):
            md += f"### {i}. {source['ref']}\n{source['text'][:300]}...\n\n"
        
        return md
    
    def _convert_generic_to_markdown(self, data: Dict[str, Any]) -> str:
        """Convert generic data to markdown"""
        md = "# Generated Content\n\n"
        md += f"Generated on: {data.get('created_date', 'Unknown')}\n\n"
        
        for key, value in data.items():
            if key != 'created_date':
                md += f"## {key.replace('_', ' ').title()}\n"
                if isinstance(value, list):
                    for item in value:
                        md += f"- {item}\n"
                elif isinstance(value, dict):
                    md += f"{json.dumps(value, indent=2)}\n"
                else:
                    md += f"{value}\n"
                md += "\n"
        
        return md


# Example usage and testing
def test_advanced_content_generation():
    """Test advanced content generation features"""
    print("Testing Advanced Content Generation...")
    
    # Initialize components
    sefaria_client = SefariaAPIClient()
    advanced_generator = AdvancedContentGenerator(sefaria_client)
    
    try:
        # Test comprehensive study guide
        print("\n1. Testing comprehensive study guide generation...")
        study_guide = advanced_generator.create_comprehensive_study_guide(
            "Genesis 1:1", 
            include_ai_analysis=True,
            difficulty_level="intermediate"
        )
        print(f"Generated study guide with {len(study_guide.get('themes', []))} themes")
        
        # Test thematic collection
        print("\n2. Testing thematic collection...")
        collection = advanced_generator.create_thematic_collection("creation", max_sources=3)
        print(f"Created collection with {len(collection['sources'])} sources")
        
        # Test learning pathway
        print("\n3. Testing learning pathway...")
        pathway = advanced_generator.create_learning_pathway("Genesis 1:1", pathway_length=3)
        print(f"Created pathway with {len(pathway['pathway'])} steps")
        
        # Test export functionality
        print("\n4. Testing export functionality...")
        exports = advanced_generator.export_to_multiple_formats(
            study_guide, 
            "/home/ubuntu/test_study_guide"
        )
        print(f"Exported to formats: {list(exports.keys())}")
        
        print("\nAll advanced content generation tests completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")


if __name__ == "__main__":
    test_advanced_content_generation()

