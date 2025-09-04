"""
Sefaria API Integration Tool

A comprehensive Python module for integrating with the Sefaria API
to fetch Jewish texts, sources, and generate content based on them.

Author: Manus AI Assistant
Date: September 2025
"""

import requests
import json
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from urllib.parse import quote
import time


@dataclass
class SefariaText:
    """Represents a text from Sefaria with metadata"""
    ref: str
    text: Union[str, List[str]]
    language: str
    version_title: str
    version_source: str
    license: str
    priority: int
    status: str
    format_as_poetry: bool = False
    
    def get_text_content(self) -> str:
        """Get the text content as a single string"""
        if isinstance(self.text, list):
            return " ".join(self.text)
        return self.text


@dataclass
class SefariaRelated:
    """Represents related content for a text reference"""
    ref: str
    links: List[Dict[str, Any]]
    sheets: List[Dict[str, Any]]
    notes: List[Dict[str, Any]]
    media: List[Dict[str, Any]]
    topics: List[Dict[str, Any]]


class SefariaAPIClient:
    """Main client for interacting with the Sefaria API"""
    
    BASE_URL = "https://www.sefaria.org/api"
    
    def __init__(self, rate_limit_delay: float = 0.1):
        """
        Initialize the Sefaria API client
        
        Args:
            rate_limit_delay: Delay between API calls to respect rate limits
        """
        self.rate_limit_delay = rate_limit_delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Sefaria-Integration-Tool/1.0',
            'Accept': 'application/json'
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a request to the Sefaria API with error handling
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.RequestException: If the API request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"Error making request to {url}: {e}")
            raise
    
    def get_text(self, ref: str, version: Optional[str] = None, 
                 fill_missing: bool = False, return_format: str = "default") -> SefariaText:
        """
        Get text content for a specific reference
        
        Args:
            ref: Sefaria text reference (e.g., "Genesis 1:1")
            version: Version specification (language or language|versionTitle)
            fill_missing: Whether to fill missing segments
            return_format: Format of returned text
            
        Returns:
            SefariaText object with text and metadata
        """
        endpoint = f"v3/texts/{quote(ref)}"
        params = {}
        
        if version:
            params['version'] = version
        if fill_missing:
            params['fill_in_missing_segments'] = '1'
        if return_format != "default":
            params['return_format'] = return_format
        
        data = self._make_request(endpoint, params)
        
        # Extract the first version for simplicity
        if 'versions' in data and data['versions']:
            version_data = data['versions'][0]
            return SefariaText(
                ref=ref,
                text=version_data.get('text', ''),
                language=version_data.get('language', ''),
                version_title=version_data.get('versionTitle', ''),
                version_source=version_data.get('versionSource', ''),
                license=version_data.get('license', ''),
                priority=version_data.get('priority', 0),
                status=version_data.get('status', ''),
                format_as_poetry=version_data.get('formatAsPoetry', False)
            )
        else:
            raise ValueError(f"No text found for reference: {ref}")
    
    def get_related(self, ref: str) -> SefariaRelated:
        """
        Get all related content for a text reference
        
        Args:
            ref: Sefaria text reference
            
        Returns:
            SefariaRelated object with related content
        """
        endpoint = f"related/{quote(ref)}"
        data = self._make_request(endpoint)
        
        return SefariaRelated(
            ref=ref,
            links=data.get('links', []),
            sheets=data.get('sheets', []),
            notes=data.get('notes', []),
            media=data.get('media', []),
            topics=data.get('topics', [])
        )
    
    def get_links(self, ref: str) -> List[Dict[str, Any]]:
        """
        Get links for a specific text reference
        
        Args:
            ref: Sefaria text reference
            
        Returns:
            List of link objects
        """
        endpoint = f"links/{quote(ref)}"
        return self._make_request(endpoint)
    
    def get_index(self, title: str) -> Dict[str, Any]:
        """
        Get index information for a text
        
        Args:
            title: Title of the text
            
        Returns:
            Index information dictionary
        """
        endpoint = f"v2/index/{quote(title)}"
        return self._make_request(endpoint)
    
    def get_versions(self, title: str) -> List[Dict[str, Any]]:
        """
        Get all versions of a text
        
        Args:
            title: Title of the text
            
        Returns:
            List of version objects
        """
        endpoint = f"texts/versions/{quote(title)}"
        return self._make_request(endpoint)
    
    def get_random_text(self) -> Dict[str, Any]:
        """
        Get a random text from Sefaria
        
        Returns:
            Random text information
        """
        endpoint = "texts/random"
        return self._make_request(endpoint)
    
    def get_topic_graph(self, topic: str) -> Dict[str, Any]:
        """
        Get topic graph information
        
        Args:
            topic: Topic name
            
        Returns:
            Topic graph data
        """
        endpoint = f"topic-graph/{quote(topic)}"
        return self._make_request(endpoint)
    
    def search_texts(self, query: str, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Search for texts in Sefaria
        
        Args:
            query: Search query
            filters: Additional search filters
            
        Returns:
            Search results
        """
        endpoint = "search-wrapper"
        params = {'q': query}
        
        if filters:
            params.update(filters)
        
        return self._make_request(endpoint, params)


class SefariaContentGenerator:
    """Generate content based on Sefaria sources"""
    
    def __init__(self, api_client: SefariaAPIClient):
        """
        Initialize content generator
        
        Args:
            api_client: Sefaria API client instance
        """
        self.api = api_client
    
    def generate_commentary_collection(self, ref: str, max_commentaries: int = 5) -> Dict[str, Any]:
        """
        Generate a collection of commentaries for a text reference
        
        Args:
            ref: Text reference to get commentaries for
            max_commentaries: Maximum number of commentaries to include
            
        Returns:
            Dictionary with original text and commentaries
        """
        # Get the original text
        original_text = self.api.get_text(ref)
        
        # Get related content to find commentaries
        related = self.api.get_related(ref)
        
        commentaries = []
        for link in related.links[:max_commentaries]:
            if 'anchorRef' in link and 'sourceRef' in link:
                try:
                    commentary_text = self.api.get_text(link['sourceRef'])
                    commentaries.append({
                        'source': link['sourceRef'],
                        'text': commentary_text.get_text_content(),
                        'title': link.get('sourceHeRef', link['sourceRef']),
                        'category': link.get('category', 'Commentary')
                    })
                except Exception as e:
                    print(f"Error fetching commentary {link['sourceRef']}: {e}")
                    continue
        
        return {
            'original_ref': ref,
            'original_text': original_text.get_text_content(),
            'original_language': original_text.language,
            'commentaries': commentaries,
            'total_commentaries': len(commentaries)
        }
    
    def generate_study_guide(self, ref: str) -> Dict[str, Any]:
        """
        Generate a study guide for a text reference
        
        Args:
            ref: Text reference to create study guide for
            
        Returns:
            Study guide with text, context, and questions
        """
        # Get the main text
        main_text = self.api.get_text(ref)
        
        # Get related content
        related = self.api.get_related(ref)
        
        # Generate study guide structure
        study_guide = {
            'reference': ref,
            'main_text': {
                'content': main_text.get_text_content(),
                'language': main_text.language,
                'version': main_text.version_title,
                'source': main_text.version_source
            },
            'context': {
                'related_passages': [],
                'topics': [],
                'historical_context': []
            },
            'study_questions': self._generate_study_questions(main_text.get_text_content()),
            'additional_resources': []
        }
        
        # Add related passages
        for link in related.links[:3]:
            if 'sourceRef' in link:
                study_guide['context']['related_passages'].append({
                    'ref': link['sourceRef'],
                    'relationship': link.get('type', 'related'),
                    'category': link.get('category', 'Unknown')
                })
        
        # Add topics
        for topic in related.topics[:5]:
            study_guide['context']['topics'].append({
                'name': topic.get('topic', ''),
                'description': topic.get('description', ''),
                'slug': topic.get('slug', '')
            })
        
        return study_guide
    
    def _generate_study_questions(self, text: str) -> List[str]:
        """
        Generate study questions based on text content
        
        Args:
            text: Text content to generate questions for
            
        Returns:
            List of study questions
        """
        # Basic question templates - in a real implementation,
        # this could use AI/NLP to generate more sophisticated questions
        questions = [
            "What is the main theme or message of this passage?",
            "How does this text relate to its historical context?",
            "What literary devices or techniques are used here?",
            "How might different commentators interpret this passage?",
            "What practical lessons can be drawn from this text?"
        ]
        
        # Add text-specific questions based on content analysis
        if len(text.split()) > 50:
            questions.append("What are the key arguments or points made in this longer passage?")
        
        if any(word in text.lower() for word in ['said', 'spoke', 'commanded']):
            questions.append("Who is speaking in this passage and to whom?")
        
        if any(word in text.lower() for word in ['law', 'commandment', 'statute']):
            questions.append("What legal or ethical principles are established here?")
        
        return questions
    
    def create_source_sheet(self, title: str, refs: List[str], 
                           commentary: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a source sheet with multiple text references
        
        Args:
            title: Title for the source sheet
            refs: List of text references to include
            commentary: Optional commentary to include
            
        Returns:
            Source sheet structure
        """
        sources = []
        
        for ref in refs:
            try:
                text = self.api.get_text(ref)
                sources.append({
                    'ref': ref,
                    'text': text.get_text_content(),
                    'language': text.language,
                    'version': text.version_title,
                    'heRef': ref  # In a real implementation, get Hebrew reference
                })
            except Exception as e:
                print(f"Error fetching text for {ref}: {e}")
                continue
        
        source_sheet = {
            'title': title,
            'sources': sources,
            'commentary': commentary or "",
            'created_date': time.strftime('%Y-%m-%d'),
            'total_sources': len(sources)
        }
        
        return source_sheet


# Example usage and testing functions
def test_sefaria_integration():
    """Test the Sefaria integration functionality"""
    print("Testing Sefaria API Integration...")
    
    # Initialize client
    client = SefariaAPIClient()
    
    try:
        # Test basic text retrieval
        print("\n1. Testing text retrieval...")
        text = client.get_text("Genesis 1:1")
        print(f"Retrieved text: {text.ref}")
        print(f"Content preview: {text.get_text_content()[:100]}...")
        
        # Test related content
        print("\n2. Testing related content...")
        related = client.get_related("Genesis 1:1")
        print(f"Found {len(related.links)} links, {len(related.topics)} topics")
        
        # Test content generation
        print("\n3. Testing content generation...")
        generator = SefariaContentGenerator(client)
        
        commentary_collection = generator.generate_commentary_collection("Genesis 1:1", max_commentaries=3)
        print(f"Generated commentary collection with {commentary_collection['total_commentaries']} commentaries")
        
        study_guide = generator.generate_study_guide("Genesis 1:1")
        print(f"Generated study guide with {len(study_guide['study_questions'])} questions")
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")


if __name__ == "__main__":
    test_sefaria_integration()

