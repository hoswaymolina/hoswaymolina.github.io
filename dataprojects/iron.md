# Iron

## The Dataset

The dataset is from a real-world manufacturing plant; it can be found [here](https://www.kaggle.com/datasets/edumagalhaes/quality-prediction-in-a-mining-process?resource=download).

## Analysis

### Overview

I began the analysis by getting an overview of the data. I imported the appropriate packages and saved the table as "df". Then, I used the shape method to see how many rows and columns the data had:

<img width="791" height="346" alt="image" src="https://github.com/user-attachments/assets/7048ee30-329e-48a7-9c51-de7382981493" />

We have over 730,000 rows and 24 attributes. It's a good thing we're using python and not Microsoft Excel for this dataset (maybe it could work, but probably not as well!)

To take a look at some of the columns while practicing some other methods, I called a section of the table using the iloc method on five rows:

<img width="861" height="337" alt="image" src="https://github.com/user-attachments/assets/7307ad71-0ae4-46b8-89d6-faaa5886beff" />

### Cleaning

Since I was going to deal with dates, it was worth checking which variable type the date column was casted as. Since I'm new to Python, I also decided to see what happens when you check the data types for the data frame and the column:

<img width="397" height="239" alt="image" src="https://github.com/user-attachments/assets/514a0576-e103-435f-b1a0-9053e71c6ac5" />

We see that the dates were casted as strings. I fixed this with the to_datetime method:

<img width="488" height="175" alt="image" src="https://github.com/user-attachments/assets/6e2b43c7-7f50-4d1d-9324-62953dc317e0" />

Now we can see that the column is of the timestamp data type.

### Aggregations

It is useful to have some classic data aggregations, and I have learned that it is rather easy to do in python, with a simple describe method:

<img width="715" height="420" alt="image" src="https://github.com/user-attachments/assets/a7035b91-5fc9-40e4-a24f-b7b52565d81a" />

We get standard deviations, percentiles, means, mins, and maxes. 
