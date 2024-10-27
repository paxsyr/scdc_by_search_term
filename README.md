# scdc_by_search_term
Allows you to navigate the Drexel SCDC system by search terms

## Motivation
The SCDC system (somehow) doesn't let you use search terms to filter jobs.

It only supports "Level of Experience", "Major", "Employer Name Phrase", "Job Location", "Non-Profit Employers Only", "Research Position", and "Accessible by public transportation from Drexel"

## Overview
The first python script, scdc_scraper.py, will use your Drexel account to log into the SCDC system and create a .json file of all the job postings for the majors (and other search criteria SCDC already supports) that you select.

In the second python script, search_scdc_dump.py, you can search this .json file by the search terms of your choice.

The system is designed in two parts because otherwise you would have to do the whole web scraping operation every time you only wanted to change your search terms.

## Instructions
1. Run scdc_scraper.py via the terminal
2. Follow the instructions displayed in the terminal
3. Run search_scdc_dump.py via the terminal, with the name of the newly generated .json file and your search term(s) as arguments
