import pandas as pd
from csv import writer
from csv import reader
import re
from collections import Counter

# Removes parenthesis or brackets and their contents
def removeComments(string):
    s = re.sub(r"[\(\[].*?[\)\]]", "", string)
    return s.strip()

# Function to see if any searchTerm from list equals any whole word in the searchTarget string
def partialMatchPhrase(searchTarget, searchTerms):
    for term in searchTerms:
        matches = re.findall(r'\b' + re.escape(term) + r'\b', searchTarget)
        if len(matches) > 0:
            return True
    return False

# Function to find wine color based on common words for that color
# Certain matches are given more weight to reduce matching errors
def findColors(searchTarget, weighDefinitive=True, weighAll=False):
    colors = []
    if partialMatchPhrase(searchTarget, ['rosé', 'rosato', 'rosado', 'rosat', 'roséwein', 'roséfine']):
        colors.append('Rosé')
        if weighAll | weighDefinitive:
            # Add weight to this match very heavily since these words are
            # very indicative of wine type
            colors.append('Rosé')
            colors.append('Rosé')
            colors.append('Rosé')
            colors.append('Rosé')
    if partialMatchPhrase(searchTarget, ['blanc','bianco','bianca','weißwein', 'weis']):
        colors.append('White')
        if weighAll | weighDefinitive:
            colors.append('White')
            colors.append('White')
            colors.append('White')
    if partialMatchPhrase(searchTarget, ['white']):
        colors.append('White')
        if weighAll:
            colors.append('White')
            colors.append('White')
    if partialMatchPhrase(searchTarget, ['noir','rotwein','rosso','rouge']):
        colors.append('Red')
        if weighAll | weighDefinitive:
            # We add extra weight to matches on varity
            colors.append('Red')
            colors.append('Red')
            colors.append('Red')
    if partialMatchPhrase(searchTarget, ['red']):
        colors.append('Red')
        if weighAll:
            # We add extra weight to matches on varity
            colors.append('Red')
            colors.append('Red')
    return colors

# Function to find if the wine is sparkling based on common words for sparkling
def findPrefix(searchTarget):
    prefix = None
    if partialMatchPhrase(searchTarget, ['sparkling','champagne','bubbles', 'bubbly','brut','bruto', 'sekt', \
        'Schaumwein','effervescent', 'spumante','scintillante']):
        prefix = 'Sparkling'
    return prefix

def findSuffix(searchTarget):
    suffix = None
    if partialMatchPhrase(searchTarget, ['blend']):
        suffix = 'Blend'
    return suffix

def chooseMostCommon(searchList, breakTies = False):
    searchSet = set(searchList)
    if len(searchSet) == 1:
        return (searchList[0], searchList)
    elif len(searchSet) == 0:
        return (None, searchList)
    else:
        sorted = Counter(searchList).most_common() # list of tuples with (value, count) in sorted order
        mostCommon = [(value, count) for (value, count) in sorted if sorted[0][1] == count]
        if len(mostCommon) == 1 | breakTies:
            return (mostCommon[0][0], searchList)
        else:
            return (None, searchList)

# Algorithm to guess wine type (Red, White, Rose, Sparkling, or Blend)
# We build a list of color matches based on several criteria
# Then we take the most frequent color in that list
def determineWineType(variety, designation, title, description):
    # Check if a sparkling wine
    prefix = findPrefix(variety)
    if not prefix:
        prefix = findPrefix(designation)

    # Check if a blend
    suffix = findSuffix(variety)
    if not suffix:
        suffix = findSuffix(designation)

    # First take color from wine variety name
    colors = findColors(variety, weighAll=True, weighDefinitive=True)
    (color, colors) = chooseMostCommon(colors)

    # Next try to match wine variety to grape list from Wikipedia
    full_matches = grape_list[grape_list['Name'].apply(lambda x: x == variety)]['Type'].tolist()

    # Handle hyphenated blends
    if len(full_matches) == 0 and ('-' in variety):
        for varietyPart in variety.split('-'):
            full_matches += grape_list[grape_list['Name'].apply(lambda x: x == varietyPart)]['Type'].tolist()

    # Handle multi-word
    if len(full_matches) == 0 and (' ' in variety):
        for varietyPart in variety.split(' '):
            full_matches += grape_list[grape_list['Name'].apply(lambda x: x == varietyPart)]['Type'].tolist()

    # Check for full grape matches
    if len(full_matches):
        colors += full_matches

    # Next take color from wine designation
    colors += findColors(designation, weighDefinitive=True)

    # Next take color from wine title
    colors += findColors(title, weighDefinitive=True)

    (color, colors) = chooseMostCommon(colors)

    if color is None:

        # Check for partial grape matchese
        partial_matches = grape_list[grape_list['Name'].apply(lambda x: partialMatchPhrase(x, [variety]))]

        # Handle hyphenated blends
        if len(partial_matches) == 0 and ('-' in variety):
            for varietyPart in variety.split('-'):
                partial_matches += grape_list[grape_list['Name'].apply(lambda x: x == varietyPart)]
        colors += partial_matches['Type'].tolist()

        (color, colors) = chooseMostCommon(colors)

    # This is where we make some best guesses since no match was found...
    # Try this lookup list for white wines either not in our grape list or in multiple lists
    # but known usually white
    if color is None and variety in ['chardonnay', 'riesling', 'pinot gris', 'muskat', \
        'muscadine', 'malvasia fina', 'malvasia', 'gros plant', 'cercial', 'cerceal']:
        colors.append('White')
        colors.append('White')
        (color, colors) = chooseMostCommon(colors)

    # Almost all sparkling wines are white
    if color is None and prefix == 'Sparkling':
        colors.append('White')
        (color, colors) = chooseMostCommon(colors)

    # If we still have no color match, look in description
    if color is None:
        colors += findColors(description)
        (color, colors) = chooseMostCommon(colors, True)

    # If still no match, assume Red
    if color is None:
        color = 'Red'

    return (" ".join(filter(None, (prefix, color, suffix))))

# Function to populate type column in data file
def addTypeColumnToData(read_filename, write_filename):
    print('>>> Starting')

    with open(read_filename, 'r') as read_obj, \
        open(write_filename, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)

        # Read each row of the input csv file as list
        i = 0
        for row in csv_reader:
            # Skip rows with null in important columns
            if row[1] and row[4] and row[5] and row[9] and row[12]:
                # Append wineType, or if first row, append column header
                if (i > 0):
                    wineType = determineWineType(row[12].lower(), row[3].lower(), row[11].lower(), row[2].lower())
                else:
                    wineType = 'type'
                row[11] = removeComments(row[11])
                row.append(wineType)
                # Add the updated row / list to the output file
                csv_writer.writerow(row)
                i += 1

    # Display count of rows matched to each wine type
    wine_list = pd.read_csv(write_filename)
    print(wine_list.groupby('type').count())

    print('>>> Finished')

# Uncomment line below to run the function to add type column


grape_list = pd.read_csv('grape_list_parsed.csv')
read_filename = 'winemag-data-130k-v2.csv'
write_filename = 'wine_with_type.csv'
addTypeColumnToData(read_filename, write_filename)
