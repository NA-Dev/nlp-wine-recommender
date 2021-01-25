# Class to hold wine recommendation query functions
import pandas as pd
import json

class WineRecommender:

    # construct the class
    def __init__(self, name, wine_type=None, flavor=None, country=None, price_min=0, price_max=9999999, \
      points_min=0, points_max=100):
        self.name = name
        self.wine_type = wine_type
        self.flavor = flavor
        self.country = country
        self.price_min = price_min
        self.price_max = price_max
        self.points_min = points_min
        self.points_max = points_max
        self.wine_list = pd.read_csv('wine2.csv')
        # Replace single quotes with double then convert string to array
        self.wine_list['flavors'] = self.wine_list['flavors'].apply(lambda x: json.loads(x.replace("'", '"')))
        self.results = self.wine_list
        self.price_range_options = [
            {'name': 'Everyday', 'price_min': 1, 'price_max': 25},
            {'name': 'Occasional', 'price_min': 26, 'price_max': 75},
            {'name': 'Premium', 'price_min': 76, 'price_max': 100},
            {'name': 'Luxury', 'price_min': 101, 'price_max': 200},
            {'name': 'Iconic', 'price_min': 201, 'price_max': 3300}
        ]
        self.points_range_options = [
            {'name': 'Excellent', 'points_min': 90, 'points_max': 100},
            {'name': 'Pretty Good', 'points_min': 86, 'points_max': 90},
            {'name': 'Not My Style', 'points_min': 0, 'points_max': 85}
        ]
        self.flavor_options = ['Sweet','Dry','Fruity','Savory','Earthy','Floral', 'Bitter','Light-Bodied','Full-Bodied']
        self.filter_options = ['Wine Type', 'Flavor Profile', 'Taster Rating', 'Country of Origin', 'Price Range']
        self.filters_applied = []

    def __str__(self):
        return "Your Name: " + self.name + "\n" + \
        "Preferred type: " + self.wine_type + "\n" + \
        "Preferred Flavor: " + self.flavor + "\n" + \
        "Country of Origin: " + self.country

    def countries(self):
        string = ''
        options = self.results['country'].unique()
        for i in range(len(options)):
            string += f"{str(i+1)}: {options[i]} ({len(self.results[self.results['country'] == options[i]])} wines)\n"
        return string

    def flavors(self):
        string = ''
        options = self.flavor_options
        for i in range(len(options)):
            # string += f"{str(i+1)}: {options[i]} ({len(self.results[self.results['flavors'].str.contains(options[i])])} wines)\n"
            string += f"{str(i+1)}: {options[i]} ({len(self.results[self.results['flavors'].apply(lambda x: options[i] in x)])} wines)\n"
        return string

    def filters(self):
        string = ''
        options = self.filter_options
        for i in range(len(options)):
            if options[i] not in self.filters_applied:
                string += f"{str(i+1)}: {options[i]}\n"
        return string

    def wine_types(self):
        string = ''
        options = self.results['type'].unique()
        for i in range(len(options)):
            string += f"{str(i+1)}: {options[i]} ({len(self.results[self.results['type'] == options[i]])} wines)\n"
        return string

    def price_ranges(self):
        string = ''
        options = self.price_range_options
        for i in range(len(options)):
            string += f"{str(i+1)}: {options[i]['name']} ${options[i]['price_min']}-${options[i]['price_max']}"\
              f"  ({len(self.results[(options[i]['price_min'] <= self.results['price']) & (self.results['price'] <= options[i]['price_max'])])} wines)\n"
        return string

    def set_price_range(self, index):
        self.price_min = self.price_range_options[index]['price_min']
        self.price_max = self.price_range_options[index]['price_max']

    def points_ranges(self):
        string = ''
        options = self.points_range_options
        for i in range(len(options)):
            string += f"{str(i+1)}: {options[i]['name']} {options[i]['points_min']}-{options[i]['points_max']} points  "\
              f"({len(self.results[(options[i]['points_min'] <= self.results['points']) & (self.results['points'] <= options[i]['points_max'])])} wines)\n"
        return string

    def set_points_range(self, index):
        self.points_min = self.points_range_options[index]['points_min']
        self.points_max = self.points_range_options[index]['points_max']

    def set_recommendations(self):
        results = self.wine_list
        if self.wine_type:
            results = results[self.wine_type == results['type']]
        if self.flavor:
            # results = results[results['flavors'].str.contains(self.flavor)]
            results = results[results['flavors'].apply(lambda x: self.flavor in x)]
        if self.country:
            results = results[self.country == results['country']]
        results = results[(self.price_min <= results['price']) & (results['price'] <= self.price_max)]
        results = results[(self.points_min <= results['points']) & (results['points'] <= self.points_max)]
        self.results = results

    def get_recommendations(self):
        if len(self.results) == 0:
            string = 'No Results'
        else:
            # Shuffle randomly and choose 5
            self.results = self.results.sample(frac=1).reset_index(drop=True)
            string = f"\n{self.name}'s Top 5 Wine Recommendations"\
              f"\n--------------------------------------"\
              f"\n--------------------------------------\n\n"
            for index, result in self.results.head(5).iterrows():
                string += f"{result['title']}"\
                  f"\n--------------------------------------\n"\
                  f"{result['type']} ({result['country']})\n"\
                  f"${result['price']}  |  {result['points']} points  |  {', '.join(result['flavors'])}\n"\
                  f"{result['description']}\n\n"
        return string


def recommend():
    # Get user's name
    name = input('\nSo you are interested in selecting a new wine to try? '
        + 'You can apply various filters, then select 0 to see your recommendations.\n'
        + 'What should I call you during this process?\n')
    recommender = WineRecommender(name)

    filter_id = 99
    try:
        # Can end the loop by entering 0.
        # Or running out of results
        # Or applying an option for each filter
        while (len(recommender.results) > 5) & (filter_id > 0) & (len(recommender.filters_applied) < len(recommender.filter_options)):
            # Choose a filter
            filter_id = int(input('\nWhat type of filter would you like to apply? '
                + 'Enter the number for one of these options:\n'  \
                + f'0: None, just show my recommendations\n{recommender.filters()}'))

            if filter_id == 1:
                # Filter based on wine type/color
                wine_type_id = int(input(f'\nAlright {recommender.name}, we have a several types of wine to choose from. '
                    + 'Enter the number for one of these options:\n'  \
                    + f'0: None, just show my recommendations\n{recommender.wine_types()}'))
                if wine_type_id:
                    recommender.wine_type = recommender.results['type'].unique()[wine_type_id - 1]

            elif filter_id == 2:
                # Filter based on flavors
                flavor_id = int(input('\nWhich flavor are you in the mood for? '
                    + 'Enter the number for one of these options:\n'  \
                    + f'0: None, just show my recommendations\n{recommender.flavors()}'))

                if flavor_id:
                    recommender.flavor = recommender.flavor_options[flavor_id - 1]

            elif filter_id == 3:
                # Filter based on points range
                points_range_id = int(input('\nWhat rating level would you like to limit this search to? '
                    + 'Enter the number for one of these options:\n'  \
                    + f'0: None, just show my recommendations\n{recommender.points_ranges()}'))
                if points_range_id:
                    recommender.set_points_range(points_range_id - 1)

            elif filter_id == 4:
                # Filter based on origin country
                country_id = int(input('\nIs there a particular country of origin you are interested in? '
                    + 'Enter the number for one of these options:\n'  \
                    + f'0: None, just show my recommendations\n{recommender.countries()}'))
                if country_id:
                    recommender.country = recommender.results['country'].unique()[country_id - 1]

            elif filter_id == 5:
                # Filter based on price range
                price_range_id = int(input('\nWhat price range would you like to limit this search to? '
                    + 'Enter the number for one of these options:\n'  \
                    + f'0: None, just show my recommendations\n{recommender.price_ranges()}'))
                if price_range_id:
                    recommender.set_price_range(price_range_id - 1)

            if filter_id in range(1,len(recommender.filter_options) + 1):
                recommender.filters_applied.append(recommender.filter_options[filter_id - 1])

            recommender.set_recommendations()

    except:
        pass

    return recommender



# Uncomment this and run file in command line interface to run the recommender script
recommender = recommend()
print(recommender.get_recommendations())

