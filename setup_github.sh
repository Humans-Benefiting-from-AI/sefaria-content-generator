#!/bin/bash

# Sefaria Content Generator - GitHub Setup Script
# This script initializes a git repository and pushes to GitHub

set -e

echo "🕎 Setting up Sefaria Content Generator GitHub Repository"
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [[ ! -f "main_working.py" ]]; then
    echo -e "${RED}❌ Error: Please run this script from the sefaria-content-generator directory${NC}"
    exit 1
fi

echo -e "${BLUE}📁 Current directory: $(pwd)${NC}"

# Initialize git repository if not already done
if [[ ! -d ".git" ]]; then
    echo -e "${BLUE}🔧 Initializing git repository...${NC}"
    git init
    echo -e "${GREEN}✅ Git repository initialized${NC}"
else
    echo -e "${YELLOW}⚠️  Git repository already exists${NC}"
fi

# Check if .gitignore exists
if [[ ! -f ".gitignore" ]]; then
    echo -e "${RED}❌ .gitignore file missing${NC}"
    exit 1
fi

# Add all files
echo -e "${BLUE}📄 Adding files to git...${NC}"
git add .

# Create initial commit
echo -e "${BLUE}💾 Creating initial commit...${NC}"
git commit -m "Initial commit: Sefaria Content Generator

🕎 Created comprehensive tool for Jewish educational content generation

Features:
- Sefaria API integration for Torah texts and sources
- Advanced content generation (study guides, commentary collections)  
- Jewish calendar integration and holiday content
- Web interface for content creation
- Template system for flexible formatting
- Comprehensive test suite and documentation

Fixed import issues and created working Flask application.

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>" || echo -e "${YELLOW}⚠️  Commit may already exist${NC}"

echo -e "${GREEN}✅ Git repository prepared${NC}"

# Check if gh CLI is available
if command -v gh &> /dev/null; then
    echo -e "${BLUE}🐙 GitHub CLI found. Creating repository...${NC}"
    
    # Create GitHub repository
    gh repo create sefaria-content-generator \
        --public \
        --description "🕎 Comprehensive tool for creating Jewish educational content using the Sefaria API. Features Torah text retrieval, study guide generation, Jewish calendar integration, and web interface for content creation." \
        --source=. \
        --push
    
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}🎉 Repository created and pushed to GitHub successfully!${NC}"
        echo -e "${BLUE}🔗 Repository URL: https://github.com/$(gh api user --jq .login)/sefaria-content-generator${NC}"
    else
        echo -e "${YELLOW}⚠️  GitHub repository creation failed. You can create it manually.${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  GitHub CLI (gh) not found.${NC}"
    echo -e "${BLUE}📝 Manual setup instructions:${NC}"
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: sefaria-content-generator"
    echo "3. Description: 🕎 Comprehensive tool for creating Jewish educational content using the Sefaria API"
    echo "4. Make it public"
    echo "5. Don't initialize with README (we already have one)"
    echo "6. Create repository"
    echo ""
    echo "Then run these commands:"
    echo "git branch -M main"
    echo "git remote add origin https://github.com/YOUR_USERNAME/sefaria-content-generator.git"
    echo "git push -u origin main"
fi

echo ""
echo -e "${GREEN}🚀 Setup complete!${NC}"
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Visit your GitHub repository"
echo "2. Add topics/tags: sefaria, jewish-texts, torah, education, content-generation"
echo "3. Enable GitHub Pages if desired"
echo "4. Add collaborators if needed"
echo ""
echo -e "${BLUE}💻 To run the application:${NC}"
echo "python3 main_working.py"
echo "# Then visit http://localhost:8080"