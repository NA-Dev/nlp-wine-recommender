# Python Wine Recommender



### Executive Summary

Using a publicly available list of wines and taster reviews, we used a series of Natural Language Processing steps to enrich the data set to include wine type and flavor profiles. Next, a terminal app will take your answers to a series of questions and return wine recommendations. Additional steps were taken to scrape a local grocery store's inventory to see which of these wines were available locally.



**See recommender.gif for a screen capture of the terminal app, ProjectPresentation.pdf for presentation, and Write_Up.pdf for full report.**



## How to Run the Recommender Terminal App

- Download Repo 
- Run Application Script: filters.py
- Follow CLI prompts
- Sample Output: recommendations.txt



## Data Sources
Original dataset: winemag-data-130k-v2.csv
Source: https://www.kaggle.com/christopheiv/winemagdata130k

Original grape Variety list : grape_list.csv
Source: https://en.wikipedia.org/wiki/List_of_grape_varieties



## Data Pre-Processing

### Step 1: Parsing the grape list

- Parser script: grape_list_parser.py
- Output: grape_list_parsed.csv
- Unit test: grape_list_parser_test.py

### Step 2: Match wines with wine type (Red, White, Rosé, Sparkling, Blend)

- Matching script: grape_id.py
- Unit test: grape_id_test.py
- Output: wine_with_type.csv

### Step 3: Add Flavor Profile Tags

- Definitions: 3. NLP Definitions.pdf
- NLP Test on Subset: Desc_Test_1_Box.ipynb
- Chunked Categorizer Script: Add_Categories.py
- Output: wine_with_flavors.csv



## Optional Steps

### Step 5: Scrape wine list from my local grocer

- Scraper: grocer_scraper.py (modify for your grocer's website)
- Output: grocery_list.csv

### Step 6: Compare lists to mark locally available wines

- Comparer Script: grocer_availability.py
- Output: wine_with_availability.csv

### Step 7: Look into wine taster details

- Notebook: reviewer_analysis.ipynb



This a continuation of a group final project for CS 5010: Python for Data Analysis with contributors Nikki Aaron, Bev Dobrenz, Joseph Wysocki, and Amanda West.