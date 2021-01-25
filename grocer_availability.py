import pandas as pd
from csv import writer
from csv import reader
import re
from collections import Counter

# Function to see if any searchTerm from list equals any whole word in the searchTarget string
def partialMatchPhrase(searchTarget, searchTerm):
    return len(re.findall(r'\b' + re.escape(searchTerm) + r'\b', searchTarget)) > 0

def filter_fn(grocer_title, wine_title):
    grocer_title = re.sub(r'[^a-zA-Z ]+', '', grocer_title.lower())
    wine_title = re.sub(r'[^a-zA-Z ]+', '', wine_title.lower())
    return partialMatchPhrase(grocer_title, wine_title) | partialMatchPhrase(wine_title, grocer_title)

# Function to populate type column in data file
def addAvailabilityData(wine_read_filename, wine_write_filename, grocery_list_filename):
    print('>>> Starting')
    
    with open(wine_read_filename, 'r') as read_obj, \
        open(out_filename, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        
        # Open grocery list
        grocery_list = pd.read_csv(grocery_list_filename)

        # Read each row of the input csv file as list
        i = 0
        for row in csv_reader:
            # Append wineType, or if first row, append column header
            if (i > 0):
                matches = grocery_list[grocery_list.apply(lambda x: filter_fn(x['Title'], row[11]), axis=1)]
                availability = True if len(matches) else False
                grocer_title = matches.loc[matches.index[0], 'Title'] if len(matches) else None
                grocer_price = matches.loc[matches.index[0], 'Price'] if len(matches) else None
                grocer_aisle = matches.loc[matches.index[0], 'Aisle']  if len(matches) else None
            else:
                availability = 'availabile'
                grocer_title = 'grocer_title'
                grocer_price = 'grocer_price'
                grocer_aisle = 'grocer_aisle'
            row.append(availability)
            row.append(grocer_title)
            row.append(grocer_price)
            row.append(grocer_aisle)
            # Add the updated row / list to the output file
            csv_writer.writerow(row)
            i += 1

    # Display count of rows matched to each wine type
    wine_list = pd.read_csv('wine_with_availability.csv')
    print(wine_list.groupby('availabile').count())

    print('>>> Finished')

# Uncomment lines below to run the function to add availability column
grocery_list_filename = 'grocery_list.csv'
wine_read_filename = 'wine_with_flavors.csv'
wine_write_filename = 'wine_availability.csv'

addAvailabilityData(wine_read_filename, wine_write_filename, grocery_list_filename)