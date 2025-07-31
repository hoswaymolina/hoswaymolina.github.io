# Modern Mining Processes: Examining Iron Refinement with Python

<img alt="Untitled" src="https://github.com/user-attachments/assets/4b9d02a5-9817-40c8-b662-fa210eed0e78" />

What do you think of when you hear the word "iron"? I usually think about strength, swords, and the medieval or classical eras. Of course, iron is a very important metal to us today - we use it in steel and various other products. As part of Avery Smith's Data Analytics Accelerator, I did some basic descriptive statistics and analysis on a real-life dataset from an iron plant. I have no knowledge of chemicals or manufacturing, so I was definitely out of my comfort zone for this project, but it helped that I was using Python, which is a really fascinating tool that I have gotten some experience with, particularly in a class I took in undergrad. In that course, I wrote short scripts to create algorithms that solved math problems - I wrote a program for Newton's method, a large prime number generator, and even made a caricature of myself using Tkinter.

In this project, however, I learned about the data anlaytics side of Python. I got to use packages like pandas and seaborn for the first time, which was exciting. I pretended that I was an iron manufacturing data analyst who was answering questions from my boss, including one about an interesting anomaly in June. Keep reading this to see my learning journey in Python!

## The Dataset

The dataset is from a real-world manufacturing plant; it can be found [here](https://www.kaggle.com/datasets/edumagalhaes/quality-prediction-in-a-mining-process?resource=download).

## Analysis

### Overview

I began the analysis by getting an overview of the data. I imported the appropriate packages and saved the table as "df". Then, I used the shape method to see how many rows and columns the data had:

<img alt="image" src="https://github.com/user-attachments/assets/7048ee30-329e-48a7-9c51-de7382981493" />

We have over 730,000 rows and 24 attributes. It's a good thing we're using python and not Microsoft Excel for this dataset (maybe it could work, but probably not as well!)

To take a look at some of the columns while practicing some other methods, I called a section of the table using the iloc method on five rows:

<img alt="image" src="https://github.com/user-attachments/assets/7307ad71-0ae4-46b8-89d6-faaa5886beff" />

### Cleaning

Since I was going to deal with dates, it was worth checking which variable type the date column was casted as. Since I'm new to Python, I also decided to see what happens when you check the data types for the data frame and the column:

<img alt="image" src="https://github.com/user-attachments/assets/514a0576-e103-435f-b1a0-9053e71c6ac5" />

We see that the dates were casted as strings. I fixed this with the to_datetime method:

<img alt="image" src="https://github.com/user-attachments/assets/6e2b43c7-7f50-4d1d-9324-62953dc317e0" />

Now we can see that the column is of the timestamp data type.

### Aggregations

It is useful to have some classic data aggregations, and I have learned that it is rather easy to do in python, with a simple describe method:

<img alt="image" src="https://github.com/user-attachments/assets/a7035b91-5fc9-40e4-a24f-b7b52565d81a" />

We get standard deviations, percentiles, means, mins, and maxes. It's a great table to get on overview on the effectiveness of the plant.

I wanted to get an overview for the date ranges. So, I used the max and min methods to get the latest and earliest dates represented in the dataset:

<img alt="image" src="https://github.com/user-attachments/assets/b6318307-8b7a-4e6b-8805-ee25ad77e670" />

Now, I was set up to answer the main question, which was to check on the "interesting" date that my boss mentioned. First, I wanted to create a table subset that only included the date of interest (June 1st, 2017) using a boolean mask. Then, I only wanted to include the important columns, which I was told were date, iron concentrate percentage, silica concentrate percentage, ore pulp pH, and the flotation level on column 5. I simply created a list with each of those column title names. I created a new dataframe, which was just the june dataframe with only the important columns, and then returned this new dataframe:

<img alt="image" src="https://github.com/user-attachments/assets/f7d3e63f-4c1a-4b41-bd46-338e069ebc13" />

Full transparency, I am not very familiar with iron refinement, so it's hard for me to tell if anything's off, BUT this table would be useful for anyone who DOES know what they're doing in terms of iron refinement. At aany rate, Python can be really useful for data visualization with packages like seaborn, which is exactly what I tried next.

### Visualization w/ Seaborn

To get a better feel for any "anomalies" that may be present, I simply used the effective and succinct pairplot method for our new important column June table:

<img alt="Untitled" src="https://github.com/user-attachments/assets/eab1db9b-e6b2-4a16-af63-baa755cdb67e" />

As far as the relationships go, there isn't much sticking out, and that's okay - it's usually just as helpful to know that two variables are not related as it is to know that they are related.

Last of all, I used the line chart feature in seaborn. The boss wanted to see how iron concentrate percentages changed throughout the day. He also wanted to see the same for other important columns. I uesd this opportunity to also practice for loops: I had python go through the important column list and provide a lineplot for each one. I actually recreated the list to exclude date, since that wasn't relevant here. Here are some of the plots that came out:

<img alt="Untitled" src="https://github.com/user-attachments/assets/7b3b8dd4-cf05-4368-ae4a-94ae0dff04db" />

<img alt="Untitled" src="https://github.com/user-attachments/assets/dc9571d9-f199-4e3b-90d1-e73bcd45bea4" />

In these charts, we can definitely see a huge dip at June 1st. It can help our boss and stakeholders to see this anomaly visually, and most importantly, now we know we weren't totally crazy not to see anything weird before. We just weren't looking at the right graph!

## Takeaways

Data analytics is really important for large, expensive, and potentially dangerous operations like mining for iron. It was a great experience to see how someone in a manufacturing analytics position would use a tool like python to get the job done. While this is a very surface-level introduction and exploration of Python's data analytics capabilities, I do understand Avery Smith's view that Python is like a jack-of-all-trades, master of none in data - SQL makes filtering columns and rows easier, while Tableau is much better for making and customizing visualizations. However, I know there are plenty of situations where Python shines.

## Thanks for Reading!

Thank you so much for going on this journey with me! Please connect with me on [LinkedIn](https://www.linkedin.com/in/hoswaymolina), and I'd be happy to hear any feedback you may have!
