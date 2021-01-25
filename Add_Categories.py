# Import Libraries
import random
import csv
import pandas as pd
import numpy as np
import re
import nltk
import os
import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

#csv file to be read in
read_filename = 'wine_with_type.csv'

#csv to write data to
write_filename = 'wine_with_flavors.csv'


# ========== Flavors (4) ============ #
# Sweet
sweet = ["sweet", "sweetness", "sugary", "sugars", "sugar"]

# dry
dry = ["dry", "brut", "sec", "demi-sec", "off-dry"]


# Fruity
fruit_forward_red = ["Berry", 'black-cherry', "Raspberry", "Cherry", "Coconut", "Cassis", 'red-berry', "Blackberry", "Blueberry", "Jam", "Prune", "Candied", "Bergamot", "Olive", "Bramble", "Cranberry", "Fig" , "Jammy", "Juniper" , "Kirsch", "Loganberry" , "Plum", "Raisin", "Raspberry" , "Strawberry", "Fruit", "Fruity"]
fruit_forward_white = ["Lemon", "Apple", "Peach", "Mango", "Pear", "Berry", "Cantaloupe", "Creme Brulee", "Crème Brûlée", "Caramel", "Vanilla", "Apricot", "Banana", "Candied", "Citrus", "Honey", "Gooseberry", "Kiwi", "Lychee", "Marmalade", "Melon", "Orange", "Papaya", "Passion Fruit", "Pineapple", "Prune", "Sherbet", "Fruit", "Fruity"]

# Savory
savory_red = ["Savory", "Cranberry", "Soy", "Onion", "Rhubarb"," Black Currant", "Cassis", "Pepper", 'lemon-zest', "Peppercorn", "Olive", "Mulberry", "Bilberry", "Dried Herbs", "Game", "Sage", "Leather", "Tobacco", "Charcoal", "Tar", "Underbrush", "Garrigue", "Gravel", "Torrefaction", "Mineral", "Woodsmoke"]
savory_white = ["Savory", "Lime", "Pith", "Quince", "Almond", "Gooseberry", "Jalapeno", "Grapefruit", "Papaya", "Thyme", "Chervil", "Grass", "Flint", "Chalk", "Chalky", "Petrichor", "Minerally", "Mineral", "biscuit", "brioche", "buttery", "butter", "caramel", "cereal", "cream", "marzipan", "croissant", "pastry"]

# Earthy
earthy_red = ["Earthy", "Rough", "Tannic", "Rusty", "Rustic", 'lead', "Earthy", "Balsamic", 'herbal', 'woody','spicy', 'clove', "Eucalyptus", "Pepper", "Leafy", "Medicinal", "Mint", "Mushroom", "Rhubarb", "Tomato", "beetroot", "tea", "meat", "tobacco", "cardboard", "iodine", "charcoal", "chocolate", "coffee", "leather","tar", "smoke", "wood", "vinyl", "velvet", "velvety", "Pepper", "Spice", "Spices", "Cedar", "Cinnamon", "Clove", "Cola", "Cumin", "Licorice"]
earthy_white = ["Earthy", "Asparagus", "Cabbage", "Fennel", "Grass", "Hay", "Hedgerow", "Lemongrass", 'herbal', 'woody','spicy', 'clove', "Vegetal", "Chalky", "flint", "chalk", "graphite", "mineral", "oyster", "salt", "slate", "steely", "wool", "almond", "beeswax", "petrol", "gasoline", "smoky", "Rough", "Tannic", "Rusty", "Rustic", "Earthy", "smoke", "toffee", "vanilla", "walnut", "wax", "match", "Pepper", "Spice", "Spices", "Cedar", "Cinnamon"]

# Floral
floral_red = ["Floral", "Blossom", "Rosy", "Rose", 'fragrant', "Lavender", "Peony", "Flower", "Flowery", "Rose", "Turkish Delight", "Violet"]
floral_white = ["Floral", "Blossom", 'Camomile', "Geranium", "Elderflower", 'fragrant', "Honeysuckle", "Jasmine", "Ginger", "Flower", "Flowery", "Rosy", "Rose"]

# Bitter
bitter_red = ["Chewy", "Muscular", "Structured", "Firm", "Rigid", "Closed", "Dried Herbs", "Herby", "Oregano", "Bay Leaf", "Bitter Chocolate", "Baker’s Chocolate", "Bitter Herbs", "Austere", "Angular", "Grippy", "Harsh", "Coarse", "Dense"]
bitter_white = ["Austere", "Citrus Pith", "Quince", "Bitter", "Almond", "Green", "Almond", "Chalk", "Chalky"]

# ========== Body Profile ============ #
# Light-Bodied
light_bodied_red = ["Light-bodied", "Light Bodied", 'summer', "Light Body", "Light", "fresh:, ""Subtle", "Delicate", "Elegant", "Crisp", "Thin", "Finesse", "Bright", "Floral"]
light_bodied_white = ["Light-bodied", "Light Bodied", 'summer', "Light Body", "Light","Zesty", "Airy", "Lean", "fresh", "Racy", "Crisp", "Zippy", "Austere", "Long Tingly Finish", "Brilliant", "Lively"]

# Full-Bodied
full_bodied_red = ["Full-bodied", "Full Bodied", "Full Body", "Rich", "Lush", "Opulent", 'richness', 'syrah', "Rigid", "Intense", "Extracted", "High Alcohol", "High Tannin", "Firm", "Structured", "Muscular", "Concentrated", "Hot",'ripe', 'luscious','heft', 'bold', 'lavish']
full_bodied_white = ["Full-bodied", "Full Bodied", "Full Body", "Rich", "Lush", "Oily", "Buttery", 'richness', "biscuit", "brioche", "buttery", "butter", "caramel", "shortcake", "cereal", "cream", "marzipan", "croissant", "pastry",'ripe', 'luscious','heft', 'bold', 'lavish']
# In[106]:


# Put in lowercase:
sweet = [x.lower() for x in sweet]
dry = [x.lower() for x in dry]

fruit_forward_red = [x.lower() for x in fruit_forward_red]
fruit_forward_white = [x.lower() for x in fruit_forward_white]

savory_red = [x.lower() for x in savory_red]
savory_white = [x.lower() for x in savory_white]

earthy_red = [x.lower() for x in earthy_red]
earthy_white = [x.lower() for x in earthy_white]

floral_red = [x.lower() for x in floral_red]
floral_white = [x.lower() for x in floral_white]

light_bodied_red = [x.lower() for x in light_bodied_red]
light_bodied_white = [x.lower() for x in light_bodied_white]

full_bodied_red = [x.lower() for x in full_bodied_red]
full_bodied_white = [x.lower() for x in full_bodied_white]

bitter_red = [x.lower() for x in bitter_red]
bitter_white = [x.lower() for x in bitter_white]

from nltk.corpus import stopwords
a = set(stopwords.words("english"))

#get the number of lines of the csv file to be read
number_lines = sum(1 for row in (open(read_filename)))

#size of chunks of data to write to the csv
chunksize = 100

cols = pd.read_csv('wine.csv', nrows=1).columns

#start looping through data writing it to a new file for each chunk
for i in range(1,number_lines,chunksize):
    data = pd.read_csv(read_filename,
        names=cols,
        nrows = chunksize,#number of rows to read at each loop
        skiprows = i)#skip rows that have been read

    # Create new box, "category"
    data['category'] = np.empty((len(data), 0)).tolist()

    # ### Part 2: Tokenize description boxes.

    # Break up the sentences into lists of individual words
    for i in range(len(data)):
        text = data['description'][i]
        data['description'][i] = word_tokenize(re.sub(r'^A-Za-z ', '', text.lower()))

        data['description'][i] = [x for x in data['description'][i] if x not in a]

        words = []
        for token in data['description'][i]:
            words.append(nltk.pos_tag([token]))
            data['description'][i] = words

        new_list = []
        final_set = []
        for tag in range(len(data['description'][i])):
            if data['description'][i][tag][0][1] == 'NN' or data['description'][i][tag][0][1] == 'JJ':
                final_set.append(data['description'][i][tag][0][0])
        data['description'][i] = final_set

    # Sweet
        sum1 = 0
        for j in range(len(data["description"][i])):
            if data["description"][i][j] in sweet:
                sum1 += 1
    # =====================================================
    # Dry
        sum2 = 0
        for j in range(len(data["description"][i])):
            if data["description"][i][j] in dry:
                sum2 += 1

        try:
            sums = [sum1,sum2]
            ns = [index for index, value in enumerate(sums) if value == max(sums)]
            n = random.choice(ns)
            if sum1 & (0 == n):
                data["category"][i].append("Sweet")
            if sum2 & (1 == n):
                data["category"][i].append("Dry")
        except:
            pass
        # ======================== Red Wines ================================================================
        if 'Red' in data["type"][i].split(' '):
        # =====================================================
        # Fruity Reds
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in fruit_forward_red:
                    sum += 1
            if sum >= 3:
                data["category"][i].append("Fruity")
        # =====================================================
        # Savory Reds
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in savory_red:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Savory")

        # =====================================================
        # Earthy Reds
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in earthy_red:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Earthy")
        # =====================================================
        # Floral Reds
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in floral_red:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Floral")

        # =====================================================
        # Bitter Reds
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in bitter_red:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Bitter")

        # =====================================================
        # Light-Bodied Red
            sum1 = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in light_bodied_red:
                    sum1 += 1
        # =====================================================
        # Full-Bodied Red
            sum2 = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in full_bodied_red:
                    sum2 += 1
            try:
                sums = [sum1,sum2]
                ns = [index for index, value in enumerate(sums) if value == max(sums)]
                n = random.choice(ns)
                if sum1 & (0 == n):
                    data["category"][i].append("Light-Bodied")
                if sum2 & (1 == n):
                    data["category"][i].append("Full-Bodied")
            except:
                pass

    # ======================== White Wines ================================================================
        elif 'White' in data["type"][i].split(' '):
        # =====================================================
        # Fruity Whites
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in fruit_forward_white:
                    sum += 1
            if sum >= 3:
                data["category"][i].append("Fruity")

        # =====================================================
        # Savory Whites
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in savory_white:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Savory")
        # =====================================================
        # Earthy Whites
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in earthy_white:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Earthy")
        # =====================================================
        # Floral Whites
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in floral_white:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Floral")

        # =====================================================
        # Bitter Whites
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in bitter_white:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Bitter")


        # =====================================================
        # Light-Bodied White
            sum1 = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in light_bodied_white:
                    sum += 1
            if sum1 >= 1:
                data["category"][i].append("Light-Bodied")
        # =====================================================
        # Full-Bodied White
            sum2 = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in full_bodied_white:
                    sum2 += 1

            try:
                sums = [sum1,sum2]
                ns = [index for index, value in enumerate(sums) if value == max(sums)]
                n = random.choice(ns)
                if sum1 & (0 == n):
                    data["category"][i].append("Light-Bodied")
                if sum2 & (1 == n):
                    data["category"][i].append("Full-Bodied")
            except:
                pass

    # ======================== Rosé Wines ================================================================
        else:
            # Fruity
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in fruit_forward_red or data["description"][i][j] in fruit_forward_white:
                    sum += 1
            if sum >= 3:
                data["category"][i].append("Fruity")

            # Savory
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in savory_red or data["description"][i][j] in savory_white:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Savory")

        # Earthy
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in earthy_red or data["description"][i][j] in earthy_white:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Earthy")

            # Floral
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in floral_red or data["description"][i][j] in floral_white:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Floral")

            # Bitter
            sum = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in bitter_red or data["description"][i][j] in bitter_white:
                    sum += 1
            if sum >= 2:
                data["category"][i].append("Bitter")

            # Light-Bodied
            sum1 = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in light_bodied_red or data["description"][i][j] in light_bodied_white:
                    sum1 += 1

            # Full-Bodied
            sum2 = 0
            for j in range(len(data["description"][i])):
                if data["description"][i][j] in full_bodied_red or data["description"][i][j] in full_bodied_white:
                    sum2 += 1

            try:
                sums = [sum1,sum2]
                ns = [index for index, value in enumerate(sums) if value == max(sums)]
                n = random.choice(ns)
                if sum1 & (0 == n):
                    data["category"][i].append("Light-Bodied")
                if sum2 & (1 == n):
                    data["category"][i].append("Full-Bodied")
            except:
                pass

        data['description'][i] = text


    data.to_csv(write_filename,
        index=False,
        header=False,
        mode='a',#append data to csv file
        chunksize=chunksize)


