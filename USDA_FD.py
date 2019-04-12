# ------------------------- IMPORT LIBRARIES --------------------
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# ------------------------- GLOBAL PARAMETERS -------------------------

# The list of Amino Acid types
# The types in this array is built by comparing the nutrient types in the json file with the amino acids list here:
# https://en.wikipedia.org/wiki/Amino_acid. Turns out amino acids are nutrient codes from 501 to 518.
# The names are however extracted from the json file, so that the right string is captured.
AMINO_LIST = ["Tryptophan", "Threonine", "Isoleucine", "Leucine", "Lysine", "Methionine", "Cystine",
              "Phenylalanine", "Tyrosine", "Valine", "Arginine", "Histidine", "Alanine", "Aspartic acid",
              "Glutamic acid", "Glycine", "Proline", "Serine"]

# The string that refers Zinc
Z = "Zinc, Zn"

# ------------------------------ CLASSES ---------------------------------


class ExternalDataRetrieval:
    """
    This class is dedicated to load the nutrient data from the directory this program resides

    """

    def get_data(self):
        """
        This function import the json file into a dataframe

        return:
            df: a dataframe of USDA nutrient database
        """

        # Import json data into a pandas dataframe
        df = pd.read_json("./nutrients.json", lines=True)

        return df

    def preprocessing(self):
        """

        This function preprocesses the nutrient.json file, parsing the nested data into usable dataframes.

        Returns:
            amino_df: a table with amino acids types as columns & food types that contains the amino acid type as rows
            zinc_df: a table with zinc content and the food groups.
            food_df: a table with foog groups, manufacturer and IDs (using ndb_no in meta)


        """
        print("This may take a while, please grab a coffee. Average wait time: 2 - 6 mins.")
        print("Loading data... ")
        df = ExternalDataRetrieval().get_data()

        print("Preprocessing data... ")

        amino_df = pd.DataFrame()
        # Set column names for zinc content dataframe
        zcolumns = ['value', 'group']
        # Set column names for food groups dataframe
        fcolumns = ['ID', 'food', 'group', 'manufacturer']
        # Declare zinc content dataframe
        zinc_df = pd.DataFrame(columns=zcolumns)
        # Declare food group dataframe
        food_df = pd.DataFrame(columns=fcolumns)
        # Doing this one amino acids type at a time.
        for n in AMINO_LIST:
            food = []
            # nutrients components of the food type is further  nested in 'nutrients', which its components are further
            # nested
            for i, items in enumerate(df['nutrients']):
                # Iterate through the nutrient type to obtain necessary info.
                # For this project, there are many redundant data in there.
                f_flag = False
                # Only need to set the flag to activate the zinc check for one amino acid loop
                if n == AMINO_LIST[0]:
                    z_flag = False
                for item in items:
                    # Check to see if this nutrient type is one of the amino acids
                    if item.get("name") == n and item.get("value") > 0:
                        # If so, add the food type to the amino acid type array
                        food.append(df['name'][i]['long'])
                        f_flag = True
                    # Check to see if this nutrient type is Zinc, only need to do this for one amino acid loop.
                    if item.get("name") == Z and n == AMINO_LIST[0]:
                        # If so, gets its zinc content value and the food group it is in.
                        zinc_df.loc[i] = [item.get("value"), df['group'][i]]
                        z_flag = True
                    if f_flag and z_flag:
                        break

                # Build the food group data dataframe one food at a time, only need to do this for one amino acid loop.
                if n == AMINO_LIST[0]:
                    food_df.loc[i] = [df['meta'][i]['ndb_no'], df['name']
                                      [i]['long'], df['group'][i], df['manufacturer'][i]]

            # Assemble the amino acid type array in to nutrient dataframe
            fd = pd.DataFrame({n: food})
            # Since the length of each columns varies (amino acid food types appearance in food types varies),
            # there are many NaN in the dataframe as a result. We need to drop the NaN
            fd = fd.dropna()
            amino_df = pd.concat([amino_df, fd], axis=1, ignore_index=True)
        # Add column names to the nutrient dataframe
        amino_df.columns = AMINO_LIST
        print("Good news, preprocessing completed successfully! ")
        return amino_df, zinc_df, food_df


class UserInterfaceDisplay:
    """
    The class to display output to users by plotting a bar chart on Zinc content
    as well as output the relevant dataframes into CSV tables

    """

    def print_tables(self, amino_df, zinc_df, food_df):
        """
        This functions output the dataframs into table for later analysis

        """

        # Output amino acid nutrients dataframe to a csv file
        amino_df.to_csv('amino_acid_food.csv', sep=',')
        print "A table of amino acids found in different food is saved as amino_acid_food.csv "
        # Output zinc content of food groups dataframe to a csv file
        zinc_df.to_csv('zinc_FoodGroup.csv', sep=',')
        print "The zinc value in food belongs to different food groups is saved as zinc_FoodGroup.csv "
        # Output food group dataframe to a csv file
        food_df.to_csv('FoodGroup.csv', sep=',')
        print "A table of food names categorized to different food groups is saved as FoodGroup.csv "

    def plot_zinc_bar(self, zinc_df):
        """
        Function to plot correlation trend of the selected index with other indices over the years

        Args:
            zinc_df: the zinc content in mg extracted from food types of food groups

        """

        print("Now plotting bar chart ...")

        # Arrange the zinc content by food group
        zinc_grp = zinc_df.groupby(['group'])['value'].median()

        # Plot bar chart
        xlabels = zinc_grp.index.get_level_values(0)
        fig = plt.figure(figsize=(16, 10))
        ax = fig.add_subplot(111)
        zinc_grp.plot(kind='bar', rot=80, fontsize=14)
        ax.set_xticklabels(xlabels, rotation=40, ha='right')
        ax.set_title("Median Zinc content by Food Groups", fontsize=15)
        ax.set_xlabel("USDA Food Groups", fontsize=14)
        ax.set_ylabel("Zinc Content in mg", fontsize=14)
        ax.yaxis.grid(color='maroon', linestyle='--', linewidth=1)
        plt.tight_layout()
        plt.savefig('zinc_content.png')
        print "Ends at:", datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        plt.show()


# ----------------------------- MAIN PROGRAM ---------------------------------

def main():
    """
    The main program

    """
    print ("\n")
    print ("####### Welcome to USDA Food Database-Nutrient Information Analysis  #######")
    print ("\n")
    print "Starts at:", datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Preprocess data first

    try:
        amino_df, zinc_df, food_df = ExternalDataRetrieval().preprocessing()
    except ValueError:
        print('No valid file found. Please place nutrients.json into the same folder this program resides')

    # Output data to plot and tables
    UserInterfaceDisplay().print_tables(amino_df, zinc_df, food_df)
    UserInterfaceDisplay().plot_zinc_bar(zinc_df)

    # Officially end of program

    print ("\n")
    print (
        "#################### End of program, Thank you for using! ####################")
    print ("\n")


if __name__ == '__main__':
    main()

    # -------------------------------- END  ---------------------------------------
