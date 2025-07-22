# Optimizing Hospitals with SQL

Have you ever stayed at a hospital? Maybe you have been a patient; maybe you knew someone who was a patient and were keeping them company. There is a wide range of reasons that someone may be admitted to a hospital - some are more serious than others. Either way, a decent experience at the hospital is important (given the tough situations of the people staying there), and unfortunately those can be hard to come by at hospitals.

To the end of improving hospital experiences and overall efficiency, data analysis is an incredible tool. Specifically, for hospitals with large amounts of data, specific tools like SQL work great. In this project, I dove deep into hospital data using SQL to help answer potential helathcare provider questions, including:

- What is the distribution of time spent in the hospital?
- 

Keep reading to see the answers and how I got them!

## The Dataset

The dataset comes from a research article concerning hospital readmission. The link can be found [here](https://www.kaggle.com/code/iabhishekofficial/prediction-on-hospital-readmission/data?select=diabetic_data.csv), and further information about the dataset can be found [here](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008).

## Cleaning

I performed some brief data cleaning for some of the columns - some of the data types for numbers ended up as varchars instead of integers, so I wrote some queries using ALTER and MODIFY: 

(line 88)

Now when I perform aggregations and order them later, it will do it numerically instead of alphabetically.

## Analysis

To answer the question about time spent distribution, I created a histogram organized by time spent at hospital in days. I did not notice any decimal places in the "time spent" column, but just in case, I added a ROUND function to ensure that only integers were used in the calculations. I assigned an asterisk to every 100 patients, and this is what I got:

HISTOGRAM QUERY
HISTOGRAM

We can see that the most common length of stay is 3 days. We can also see that most stays are within one week, which is not too bad. While data visualization tools like Tableau and Power BI have SQL beat, it's useful to know that I can pull a quick visualization with a short query.

The next question I answered was: What are the top procedures administered? I organized the procedures by medical specialty, which I had to narrow with the DISTINCT function (since it was showing each instance of the medical specialty in the column). In order to highlight only the top procedures, I used the HAVING function to list only procedures with an average number higher than 2.5 and with at least 50 instances (so as to have a large enough sample size). I got the following result:

NUM PROCEDURES QUERY
NUM PROCEDURES

Thoracic surgery, including of the cardiovascular variety, and radiologist procedures top out the list. Further, procedures by the cardiologists had the largest sample size, at over 5000.

The next inquiry by the hospital staff is whether patients of different races are being treated differently in terms of number of procedures done. In order to provide insight for this question, I had to use a JOIN since the health and demographics tables are separate. 
