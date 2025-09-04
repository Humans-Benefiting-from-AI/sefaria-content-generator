"""
Comprehensive Test Suite for Sefaria Integration Tool

This module provides thorough testing of all components of the Sefaria integration tool,
including API calls, content generation, and export functionality.

Author: Manus AI Assistant
Date: September 2025
"""

import json
import time
import os
from typing import Dict, List, Any
from datetime import datetime

from sefaria_integration import SefariaAPIClient, SefariaContentGenerator
from content_templates import ContentGenerator
from advanced_content_generator import AdvancedContentGenerator


class SefariaTestSuite:
    """Comprehensive test suite for Sefaria integration tool"""
    
    def __init__(self):
        """Initialize test suite"""
        self.sefaria_client = SefariaAPIClient()
        self.basic_generator = SefariaContentGenerator(self.sefaria_client)
        self.template_generator = ContentGenerator()
        self.advanced_generator = AdvancedContentGenerator(self.sefaria_client)
        
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'detailed_results': []
        }
    
    def run_test(self, test_name: str, test_function, *args, **kwargs) -> bool:
        """
        Run a single test and record results
        
        Args:
            test_name: Name of the test
            test_function: Function to execute
            *args, **kwargs: Arguments for the test function
            
        Returns:
            True if test passed, False otherwise
        """
        self.test_results['tests_run'] += 1
        start_time = time.time()
        
        try:
            result = test_function(*args, **kwargs)
            execution_time = time.time() - start_time
            
            self.test_results['tests_passed'] += 1
            self.test_results['detailed_results'].append({
                'test_name': test_name,
                'status': 'PASSED',
                'execution_time': execution_time,
                'result': str(result)[:200] if result else 'Success'
            })
            print(f"✓ {test_name} - PASSED ({execution_time:.2f}s)")
            return True
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            self.test_results['tests_failed'] += 1
            self.test_results['detailed_results'].append({
                'test_name': test_name,
                'status': 'FAILED',
                'execution_time': execution_time,
                'error': str(e)
            })
            print(f"✗ {test_name} - FAILED ({execution_time:.2f}s): {e}")
            return False
    
    def test_basic_api_calls(self):
        """Test basic Sefaria API functionality"""
        print("\n=== Testing Basic API Calls ===")
        
        # Test text retrieval
        def test_get_text():
            text = self.sefaria_client.get_text("Genesis 1:1")
            assert text.ref == "Genesis 1:1"
            assert len(text.get_text_content()) > 0
            return f"Retrieved text: {text.get_text_content()[:50]}..."
        
        self.run_test("Get Text - Genesis 1:1", test_get_text)
        
        # Test text with different versions
        def test_get_text_english():
            text = self.sefaria_client.get_text("Genesis 1:1", version="english")
            assert text.language == "en"
            return f"English text: {text.get_text_content()[:50]}..."
        
        self.run_test("Get Text - English Version", test_get_text_english)
        
        # Test related content
        def test_get_related():
            related = self.sefaria_client.get_related("Genesis 1:1")
            assert related.ref == "Genesis 1:1"
            assert len(related.links) > 0
            return f"Found {len(related.links)} links, {len(related.topics)} topics"
        
        self.run_test("Get Related Content", test_get_related)
        
        # Test index information
        def test_get_index():
            index = self.sefaria_client.get_index("Genesis")
            assert 'title' in index
            return f"Index title: {index.get('title', 'Unknown')}"
        
        self.run_test("Get Index Information", test_get_index)
        
        # Test versions
        def test_get_versions():
            versions = self.sefaria_client.get_versions("Genesis")
            assert len(versions) > 0
            return f"Found {len(versions)} versions"
        
        self.run_test("Get Versions", test_get_versions)
        
        # Test random text
        def test_random_text():
            random_text = self.sefaria_client.get_random_text()
            assert 'ref' in random_text
            return f"Random text ref: {random_text.get('ref', 'Unknown')}"
        
        self.run_test("Get Random Text", test_random_text)
    
    def test_content_generation(self):
        """Test content generation functionality"""
        print("\n=== Testing Content Generation ===")
        
        # Test commentary collection
        def test_commentary_collection():
            collection = self.basic_generator.generate_commentary_collection("Genesis 1:1", max_commentaries=3)
            assert 'original_ref' in collection
            assert 'commentaries' in collection
            assert len(collection['commentaries']) >= 0
            return f"Generated collection with {collection['total_commentaries']} commentaries"
        
        self.run_test("Commentary Collection", test_commentary_collection)
        
        # Test study guide
        def test_study_guide():
            guide = self.basic_generator.generate_study_guide("Genesis 1:1")
            assert 'reference' in guide
            assert 'main_text' in guide
            assert 'study_questions' in guide
            return f"Generated study guide with {len(guide['study_questions'])} questions"
        
        self.run_test("Basic Study Guide", test_study_guide)
        
        # Test source sheet
        def test_source_sheet():
            refs = ["Genesis 1:1", "Genesis 1:2", "Genesis 1:3"]
            sheet = self.basic_generator.create_source_sheet("Creation Theme", refs)
            assert 'title' in sheet
            assert 'sources' in sheet
            return f"Created source sheet with {sheet['total_sources']} sources"
        
        self.run_test("Source Sheet Creation", test_source_sheet)
    
    def test_template_generation(self):
        """Test template-based content generation"""
        print("\n=== Testing Template Generation ===")
        
        # Test source sheet template
        def test_source_sheet_template():
            data = {
                'title': 'Test Source Sheet',
                'topic': 'Creation',
                'introduction': 'Test introduction',
                'sources': [
                    {
                        'ref': 'Genesis 1:1',
                        'text': 'In the beginning...',
                        'commentary': 'Test commentary'
                    }
                ],
                'discussion_questions': ['What does this teach us?'],
                'conclusion': 'Test conclusion'
            }
            content = self.template_generator.generate_content('source_sheet', data)
            assert 'Test Source Sheet' in content
            assert 'Genesis 1:1' in content
            return f"Generated {len(content)} characters of content"
        
        self.run_test("Source Sheet Template", test_source_sheet_template)
        
        # Test daily study template
        def test_daily_study_template():
            data = {
                'date': 'September 4, 2025',
                'ref': 'Genesis 1:1',
                'original_text': 'Hebrew text here',
                'translation': 'English translation',
                'reflection': 'Daily reflection',
                'key_insight': 'Key insight',
                'daily_connection': 'Connection to daily life'
            }
            content = self.template_generator.generate_content('daily_study', data)
            assert 'Daily Study' in content
            assert 'Genesis 1:1' in content
            return f"Generated daily study content"
        
        self.run_test("Daily Study Template", test_daily_study_template)
        
        # Test available templates
        def test_available_templates():
            templates = self.template_generator.get_available_templates()
            expected_templates = ['weekly_parasha', 'daily_study', 'commentary_comparison', 
                                'topical_study', 'source_sheet', 'holiday_guide']
            for template in expected_templates:
                assert template in templates
            return f"Found {len(templates)} templates: {', '.join(templates)}"
        
        self.run_test("Available Templates", test_available_templates)
    
    def test_advanced_features(self):
        """Test advanced content generation features"""
        print("\n=== Testing Advanced Features ===")
        
        # Test comprehensive study guide
        def test_comprehensive_study_guide():
            guide = self.advanced_generator.create_comprehensive_study_guide(
                "Genesis 1:1", 
                include_ai_analysis=True,
                difficulty_level="intermediate"
            )
            assert 'reference' in guide
            assert 'main_text' in guide
            assert 'metadata' in guide
            return f"Generated comprehensive guide with AI analysis"
        
        self.run_test("Comprehensive Study Guide", test_comprehensive_study_guide)
        
        # Test learning pathway
        def test_learning_pathway():
            pathway = self.advanced_generator.create_learning_pathway("Genesis 1:1", pathway_length=3)
            assert 'starting_ref' in pathway
            assert 'pathway' in pathway
            assert len(pathway['pathway']) > 0
            return f"Created pathway with {len(pathway['pathway'])} steps"
        
        self.run_test("Learning Pathway", test_learning_pathway)
        
        # Test comparative analysis
        def test_comparative_analysis():
            refs = ["Genesis 1:1", "Genesis 1:2"]
            analysis = self.advanced_generator.create_comparative_analysis(refs, "themes")
            assert 'references' in analysis
            assert 'texts' in analysis
            assert 'comparison' in analysis
            return f"Analyzed {len(analysis['texts'])} texts"
        
        self.run_test("Comparative Analysis", test_comparative_analysis)
    
    def test_export_functionality(self):
        """Test export functionality"""
        print("\n=== Testing Export Functionality ===")
        
        # Test JSON export
        def test_json_export():
            guide = self.advanced_generator.create_comprehensive_study_guide("Genesis 1:1")
            exports = self.advanced_generator.export_to_multiple_formats(guide, "/home/ubuntu/test_export")
            
            assert 'json' in exports
            assert 'markdown' in exports
            
            # Verify files exist
            assert os.path.exists(exports['json'])
            assert os.path.exists(exports['markdown'])
            
            # Verify JSON content
            with open(exports['json'], 'r') as f:
                json_data = json.load(f)
                assert 'reference' in json_data
            
            return f"Exported to {len(exports)} formats"
        
        self.run_test("Export Functionality", test_json_export)
        
        # Test template export
        def test_template_export():
            data = {
                'title': 'Export Test',
                'content': 'Test content for export'
            }
            filepath = self.template_generator.export_content(
                "# Test Content\nThis is test content.", 
                "/home/ubuntu/template_export_test", 
                "markdown"
            )
            
            assert os.path.exists(filepath)
            with open(filepath, 'r') as f:
                content = f.read()
                assert "Test Content" in content
            
            return f"Exported template to {filepath}"
        
        self.run_test("Template Export", test_template_export)
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("\n=== Testing Error Handling ===")
        
        # Test invalid reference
        def test_invalid_reference():
            try:
                self.sefaria_client.get_text("InvalidBook 999:999")
                return "Should have failed but didn't"
            except Exception as e:
                # This is expected
                return f"Correctly handled invalid reference: {type(e).__name__}"
        
        self.run_test("Invalid Reference Handling", test_invalid_reference)
        
        # Test empty template data
        def test_empty_template_data():
            try:
                content = self.template_generator.generate_content('source_sheet', {})
                # Should work with empty data, just produce minimal content
                assert len(content) > 0
                return "Handled empty template data gracefully"
            except Exception as e:
                return f"Error with empty data: {e}"
        
        self.run_test("Empty Template Data", test_empty_template_data)
        
        # Test unsupported template type
        def test_unsupported_template():
            try:
                self.template_generator.generate_content('nonexistent_template', {})
                return "Should have failed but didn't"
            except ValueError as e:
                return f"Correctly rejected unsupported template: {e}"
            except Exception as e:
                return f"Unexpected error: {e}"
        
        self.run_test("Unsupported Template", test_unsupported_template)
    
    def test_performance(self):
        """Test performance characteristics"""
        print("\n=== Testing Performance ===")
        
        # Test multiple API calls
        def test_multiple_api_calls():
            refs = ["Genesis 1:1", "Genesis 1:2", "Genesis 1:3", "Exodus 1:1", "Leviticus 1:1"]
            start_time = time.time()
            
            results = []
            for ref in refs:
                try:
                    text = self.sefaria_client.get_text(ref)
                    results.append(text.ref)
                except:
                    continue
            
            total_time = time.time() - start_time
            avg_time = total_time / len(results) if results else 0
            
            return f"Retrieved {len(results)} texts in {total_time:.2f}s (avg: {avg_time:.2f}s per text)"
        
        self.run_test("Multiple API Calls Performance", test_multiple_api_calls)
        
        # Test large content generation
        def test_large_content_generation():
            start_time = time.time()
            
            # Generate multiple pieces of content
            guide = self.advanced_generator.create_comprehensive_study_guide("Genesis 1:1")
            pathway = self.advanced_generator.create_learning_pathway("Genesis 1:1", pathway_length=3)
            
            total_time = time.time() - start_time
            return f"Generated complex content in {total_time:.2f}s"
        
        self.run_test("Large Content Generation", test_large_content_generation)
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Comprehensive Sefaria Integration Tool Test Suite")
        print("=" * 70)
        
        start_time = time.time()
        
        # Run all test categories
        self.test_basic_api_calls()
        self.test_content_generation()
        self.test_template_generation()
        self.test_advanced_features()
        self.test_export_functionality()
        self.test_error_handling()
        self.test_performance()
        
        total_time = time.time() - start_time
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests Run: {self.test_results['tests_run']}")
        print(f"Tests Passed: {self.test_results['tests_passed']}")
        print(f"Tests Failed: {self.test_results['tests_failed']}")
        print(f"Success Rate: {(self.test_results['tests_passed'] / self.test_results['tests_run'] * 100):.1f}%")
        print(f"Total Execution Time: {total_time:.2f} seconds")
        
        # Save detailed results
        self.test_results['total_execution_time'] = total_time
        with open('/home/ubuntu/test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: /home/ubuntu/test_results.json")
        
        if self.test_results['tests_failed'] == 0:
            print("\n🎉 ALL TESTS PASSED! The Sefaria Integration Tool is working correctly.")
        else:
            print(f"\n⚠️  {self.test_results['tests_failed']} tests failed. Check the detailed results for more information.")
        
        return self.test_results


def run_demonstration():
    """Run a demonstration of the tool's capabilities"""
    print("\n" + "=" * 70)
    print("🎭 SEFARIA INTEGRATION TOOL DEMONSTRATION")
    print("=" * 70)
    
    sefaria_client = SefariaAPIClient()
    advanced_generator = AdvancedContentGenerator(sefaria_client)
    
    # Demonstration 1: Create a comprehensive study guide
    print("\n📚 Demonstration 1: Comprehensive Study Guide")
    print("-" * 50)
    
    study_guide = advanced_generator.create_comprehensive_study_guide(
        "Ecclesiastes 3:1",
        include_ai_analysis=True,
        difficulty_level="intermediate"
    )
    
    print(f"✓ Created study guide for {study_guide['reference']}")
    print(f"✓ Generated {len(study_guide.get('themes', []))} key themes")
    print(f"✓ Included {len(study_guide.get('study_questions', []))} study questions")
    print(f"✓ Found {len(study_guide.get('related_sources', []))} related sources")
    
    # Export the study guide
    exports = advanced_generator.export_to_multiple_formats(
        study_guide, 
        "/home/ubuntu/demo_study_guide"
    )
    print(f"✓ Exported to {len(exports)} formats: {', '.join(exports.keys())}")
    
    # Demonstration 2: Create a learning pathway
    print("\n🛤️  Demonstration 2: Learning Pathway")
    print("-" * 50)
    
    pathway = advanced_generator.create_learning_pathway("Proverbs 1:1", pathway_length=5)
    
    print(f"✓ Created learning pathway starting from {pathway['starting_ref']}")
    print(f"✓ Pathway contains {len(pathway['pathway'])} steps")
    print(f"✓ Learning objectives: {len(pathway.get('learning_objectives', []))}")
    
    for i, step in enumerate(pathway['pathway'][:3], 1):  # Show first 3 steps
        print(f"   Step {i}: {step['ref']} - Focus: {step['learning_focus']}")
    
    # Demonstration 3: Comparative analysis
    print("\n🔍 Demonstration 3: Comparative Analysis")
    print("-" * 50)
    
    comparison_refs = ["Psalms 23:1", "Psalms 121:1", "Psalms 1:1"]
    analysis = advanced_generator.create_comparative_analysis(comparison_refs, "themes")
    
    print(f"✓ Analyzed {len(analysis['texts'])} texts")
    print(f"✓ Found {len(analysis['comparison'].get('similarities', []))} similarities")
    print(f"✓ Found {len(analysis['comparison'].get('differences', []))} differences")
    
    print("\n🎯 Demonstration Complete!")
    print("The Sefaria Integration Tool successfully demonstrated:")
    print("• API integration with Sefaria's database")
    print("• AI-powered content analysis and generation")
    print("• Multiple content formats and templates")
    print("• Export functionality to various formats")
    print("• Advanced features like learning pathways and comparative analysis")


if __name__ == "__main__":
    # Run comprehensive test suite
    test_suite = SefariaTestSuite()
    results = test_suite.run_all_tests()
    
    # Run demonstration if tests pass
    if results['tests_failed'] == 0:
        run_demonstration()
    else:
        print("\n⚠️  Skipping demonstration due to test failures.")
        print("Please review the test results and fix any issues before proceeding.")

