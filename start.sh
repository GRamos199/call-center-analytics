#!/bin/bash

# Call Center Analytics - Startup Script

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Call Center Analytics Dashboard${NC}"
echo -e "${GREEN}================================${NC}\n"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if requirements are installed
echo -e "${YELLOW}Checking dependencies...${NC}"
pip install -q -r requirements.txt

# Start Streamlit
echo -e "${GREEN}Starting Streamlit dashboard...${NC}"
echo -e "${GREEN}Open your browser at: http://localhost:8501${NC}\n"
cd analytics && streamlit run app.py
