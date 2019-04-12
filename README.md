# Parsing USDA food database

This project loads the USDA food database in json format and parses the data into components that usable for analysis in a time and computation efficient manner.  
Finally food nutrient info can be displayed to users in a plot and tables (CSV files). 
Zinc content plot is displayed in the final result. The other nutrient content type would work similarly. 

[image1]: https://github.com/jiewwantan/nutrient_json_db/blob/master/zinc_content.png "Zinc Content"

## Program description
Function `get_data` loads the USDA nutrient database: nutrients.json into a Python
dataframe: df.

Most columns in the dataframe: “group”, “manufacturer”, “meta”, “name”,
“nutrients”, “portions” requires parsing except “group” and “manufacturer”.
“nutrients” column which contains most of the data we need for this project has data
nested in key/value pairs and goes as deep as two layers. As such “For” loops are
used to retrieve the data.
Function `preprocessing` parse the JSON file and extract value to build three
dataframes:

amino_df -> the dataframe with columns of 18 types of amino acids and the rows are
the food types that consist of the amino acids. The types of amino acids are identified
using reference from Amino acids’ Wikipedia page[3]. It turns out amino acids are
nutrient codes from 501 to 518. The strings of 18 amino acid names are manually
extracted from the json file in order to capture all amino acids correctly. Different
amino acids can spell or expresss differently from different sources.

zinc_df -> the dataframe zinc content value in mg and the food group where they are
found.

food_df -> the dataframe of food names, group, id (meta’s ndb_no), and
manufacturer.

The dataset consists of 8789 food types stored in 8789 lines. Within each line, there
are 6 main category of objects: “group”, “manufacturer”, “meta”, “name”, “nutrients”
and “portions”. Except “group” and “manufacturer” columns, within each column,
there are nested objects. For example nutrients column has objects on individual
nutrients. The number of nutrients depends on the food names/types itself. Within
each nutrient types, there are also nested objects to describe the nutrient’s
characteristics. It is only “name”, “meta” and “nutrients” we need to concern about
when it comes to parsing.

Parsing the data requires an understanding of how this json dataset is structured. This
is important because every json file can have its key/value pairs structured or nested
differently at different layers.

Depends how deep the required key/value are nested in the object, much thought has
to be taken into consideration about the algorithm to retrieve them. Obviously the
deeper it is, the more resource consuming it is. And this will add load into
computational resource. So users who may not have much computational resource to
spare has to be taken into consideration. When running the final version of the
program on a Linux machine with higher performance, the program took 1+ minute.
When running on a 5 years old Mac book, it took 6+minutes. So conservatively, the
longest runtime is considered instead.

To parse the data efficiently, I have considered flattening the entire dataset into a 2d
dataframe (instead of multiple layers of iterations) but that will produce a huge
dataframe with uncertain number of columns (due to varying nutrients types in each
food types). That may not lead to a good algorithmic design and could be unstable to
maintain. I then decided to flatten only the “nutrients” object every time a food types
is examined. However, this leads a 20+ mins total runtime on the faster Linux
machine. Evidently, not a good use of computation resource just to analyze a single
food database and display a couple of results. The flatten function tried is
pandas.io.json.json_normalize.

I later have the program iterate by amino acids first, followed by 8789 lines of food
names, followed by the individual nutrients within each food name. While the
building of zinc and food groups dataframes only needs to go through one amino acid
iteration since the remaining iterations are just the repeat of the same thing. I have
made zinc and food group dataframes construction with the amino acid dataframe
construction so that to utilize the 8789 lines of food names iteration and keep the
iterations as minimum as possible, by utilizing a flagging mechanism. The final
version consist of 18 ( 18 amino acids) iterations of 8789 lines of food names where
the first amino acid iteration will do zinc and food group as well. As such we don’t
need to have another 8789 lines of iteration for zinc and food group.

I also found that, instead of iterating by a range of numbers (18 and 8789), “for item
in items” would work much more efficiently. As such just two level of “for item in
items” loops combined with “item.get” will reduce the run time to 7+ mins, without
having to use the json flatten function. Further reduction is done when setting up a
flagging mechanism. Once the loop obtains the required amino acid and zinc values,
the loop stops screening the remaining individual nutrients. The runtime is then
reduced to 6 mins 40 seconds.

## Reflections
This is a comprehensive and beautiful dataset. Some useful application can be
developed out of this dataset. Such as diets for patients that requires specific nutrition
combinations. I suspect many have done so already. Though, if more food types can
be entered to cover Asian food or food from other cultures, the application can be
developed for users in countries beyond USA.
In this project I experienced the importance of designing programs that are
computationally cost effective. I have used depth first search in working out the
search algorithm. Zinc and the amino acids nutrients are located somewhere in the
middle of the 70 – 146 (max) lines of nutrients for each 8789 lines of food names.
Current search technique cut out the remaining, approximately a third of total
nutrients when the amino acid and zinc are found. Given much more thoughts on the
search algorithm design, I believe it is still possible to design an algorithm that reduces more processing time.

## Results
![Zinc Content][image1]


## Instructions

To execute the program, under command prompt, place USDA_FD.py, USDA_FD.py and nutrients.json under the same folder, run: 

`python USDA_FD.py`


## Prerequisites

Python 2.7 or Anaconda with Python 2.7 environment
Python packages: pandas, matplotlib, datetime

The code is written in a Linux Ubuntu machine and has been tested on three operating systems: 
Linux Ubuntu 16.04, Windows 10 Pro & Mac OS X 10.11.6. 
