## Falling Rain Parser

This code parses data from fallingrain.com and saves it into a csv file.

---

## Language used

Python

---

## Concept behind the code

Assumption:

Based on the pattern of the links

1. The states, union territories and the capital have been numbered between 0 to 39.
2. The cities in a state can be accessed using the lexicographic order.

The code generates the basic 40 links and the function **generateURLs** generates the further links by appending characters to them 
in lexicographical order.

As the dataset is huge so the code uses multithreading. All the links are put into a synchronized queue which are then parsed with 
the help of multiple threads.

On each link **crawl** function is called which checks whether the page contains a table or not. If the page contains a table the 
data is then parsed and saved using the **saveData** function in the following format

**City, State, Latitude, Longitude, Elevation, Estimated Population**

---

## Libraries used

1. bs4
2. urllib3

---

## How to run

1. Run pip3 install -r requirements.txt in the console for python ver 3
2. Run pip install requirements.txt in the console for python ver 2
3. Run parse_falling_rain.py by typing **python parse_falling_rain.py** in the console