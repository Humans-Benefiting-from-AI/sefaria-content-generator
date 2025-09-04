# Sefaria API Research

## Overview
The Sefaria API provides live access to Sefaria's structured database of Jewish texts and their interconnections. It's designed to make getting a new web or mobile app up-and-running as simple as possible.

## Key Features
- No API keys, tokens, or authorization required for documented endpoints
- Open-source database of Jewish texts
- Structured interconnections between texts
- OpenAPI specification available

## Main API Categories

### Text Access
- **Texts (v3)**: Retrieve text editions with metadata
- **Versions**: See all available editions of a given book
- **Index (v2)**: Get metadata for specific books
- **Table of Contents**: See all available books

### Text Relationships
- **Related API**: Retrieve related commentaries, parallel passages, and connections
- **Links**: Access interconnections between texts

### Study Resources
- **Calendars**: Data about study schedules tracked on Sefaria
- **Topic Graph**: Retrieve interrelated topics
- **Ref-Topic-Links**: Get topics associated with specific texts

### Language Support
- **Languages**: See all available languages on Sefaria
- **Translations**: Query text editions by language
- **Lexicon**: Dictionary functionality
- **Word Completion**: Text completion features

### Media and Images
- **Social Media Image**: Generate graphics from text segments
- **Manuscripts**: Retrieve manuscript pages for texts

### Utility
- **Random Text**: Get random text passages
- **Random By Topic**: Random texts by topic

## Documentation Status
- Work-in-progress reference documentation
- Interactive playgrounds available
- Additional technical docs available
- OpenAPI specification provided

## Next Steps
1. Explore specific API endpoints in detail
2. Test API calls with real data
3. Understand data formats and structures
4. Design integration patterns for content generation



## API Response Structure (Texts v3)

Based on testing the Texts v3 API with "Rashi on Genesis", the response includes:

### Version Information
- `status`: "locked" (indicates text status)
- `priority`: 4 (version priority)
- `license`: "Public Domain"
- `versionNotes`: Additional notes about the version
- `formatAsPoetry`: Boolean for formatting
- `digitizedBySefaria`: Boolean indicating if digitized by Sefaria
- `method`: Method used for digitization
- `versionSource`: Source URL for the version
- `versionUrl`: URL for the specific version
- `versionTitleInHebrew`: Hebrew title of the version
- `versionNotesInHebrew`: Hebrew version notes
- `shortVersionTitle`: Abbreviated version title
- `extendedNotes`: Extended notes about the version
- `extendedNotesHebrew`: Extended notes in Hebrew
- `purchaseInformationImage`: Purchase information
- `purchaseInformationURL`: Purchase URL
- `hasManuallyWrappedRefs`: Boolean for manual wrapping
- `language`: Language code (e.g., "he" for Hebrew)
- `languageFamilyName`: Language family (e.g., "hebrew")
- `actualLanguage`: Actual language code
- `versionSource`: Source information
- `versionTitle`: Full version title
- `actualLanguage`: Language specification

### Text Content Structure
The API provides structured access to:
- Hebrew text with proper formatting
- Commentary structure for texts like Rashi
- Metadata about text versions and sources
- Language and translation information

### Key Capabilities Confirmed
1. **Multi-language support**: Hebrew, English, and other languages
2. **Version management**: Multiple versions of the same text
3. **Commentary access**: Structured access to commentaries like Rashi
4. **Metadata richness**: Extensive metadata about sources and versions
5. **Public domain content**: Much content is in public domain

