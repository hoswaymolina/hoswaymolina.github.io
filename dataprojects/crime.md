# Violent and Hate Crime in Texas

Oh yeah

## Why this project?

## The Data

The FBI's [Crime Data Explorer](https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/home) has a wealth of real-life crime data avaialable for the public. I highly recommend it as a data source for anyone interested in doing projects with crime data. They make it easy to access with a [Documents and Downloads](https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads) button from which one can download excel worksheets (for the smaller datasets) or zip files (for the bigger data dumps). I wanted to have the freedom to explore the data in as much or as little detail as I wished but also work with a manageable dataset size. So, I opted to download the Crime Incident-Based Data for Texas in 2024, which at the time of writing was the most recent data:

<img alt="image" src="https://github.com/user-attachments/assets/e333e4ee-259d-4df0-b4a4-9142a1b18957" />

I downloaded a zip file containing over 40 csv files, a readme, a very helpful data diagram explaining the tables and their relationships, and 2 SQL scripts to load the data with. They were written for PostgreSQL, which gave me a huge headache at the beginning of the project that I will explain later. That said, these scripts had much of what I needed, and even though I had to edit them to work for MySQL, they still saved me a huge amount of time.

### Data Structure

Here's a brief description of the data in the FBI's own words (from the readme):

> This download contains a year's worth of incident and arrestee data for a single state that participates in the National Incident-Based Reporting System (NIBRS) system. NIBRS is the successor to the Summary Reporting System (SRS) previously used by the UCR program since the 1930s, and it offers incident-level data with more detailed information about offenders, victims, relationships between offenders and victims, and offenses affecting victims. It also removes the the "hierarchy rule" that meant only a single offense was counted as part of SRS summary reports.
>
> For detailed information about all the fields provided in NIBRS and how they are collected and presented, please refer to the [official NIBRS documentation](https://ucr.fbi.gov/nibrs/nibrs-user-manual).

Crimes are organized by **incidents** at the hightest level, each with a unique id. Each incident can have multiple **offenses**, which are essentially separate crimes that occurred in an incident. They also have unique ids. So, there may be multiple offense ids associated with a particular incident. Each incident can be explored via tables that show administrative info (e.g., whether an offender was cleared exceptionally), property that was lost/damaged, the victims involved, offender demographics, and arrestee information. Everything from the date and hour the incident occurred to the victim's ethnicity to the measure of drugs possessed is contained in the files.

To help explain these relationships, [a very helpful diagram](/files/nibrs_diagram.pdf) was included in the zip file. I suggest reviewing it briefly before diving into my analysis - it helps explain why I had to juggle primary and foreign keys a lot in my analysis.

### Data Dictionary

In case you want more detail about the tables and columns that I access in the queries below, here is an [NIBRS Data Dictionary](/files/NIBRS_DataDictionary.pdf) that is available on the website!

### Loading the Data

## Analysis

### Number of hate crimes by bias

One of the first things I did was to organize the crimes by bias type. First, I wrote a query returning the total number of biased offenses that occurred in total. I linked the offenses table with the bias motivation table and counted offenses ids where the bias was not "unknown" or "none":

```sql
SELECT 
    COUNT(o.offense_id) AS num_biased_offenses
FROM
    nibrs_offense AS o
        JOIN
    nibrs_bias_motivation AS nb ON o.offense_id = nb.offense_id
WHERE
    nb.bias_id != '88'
        AND nb.bias_id != '99';
```

A single cell was returned showing 479 hate crimes in Texas for 2024. I verified this number with the hate crime table spreadsheet available on the CDE website, which also showed 479 offenses.

I then grouped the query by bias. Since the bias motivation table only had the bias id (NOT the name of the bias), I decided to link a third table - the bias list table - so I could return the `bias_desc` column (bias name) instead of a number. That way, anyone seeing the result could see the bias type without having to go back and forth between the bias list table and the query result:

```sql
SELECT 
    COUNT(ni.offense_id) AS num_biased_offenses,
    nl.bias_desc AS bias
FROM
    nibrs_offense AS ni
        JOIN
    nibrs_bias_motivation AS nb ON ni.offense_id = nb.offense_id
        JOIN
    nibrs_bias_list AS nl ON nb.bias_id = nl.bias_id
WHERE
    nb.bias_id != '88'
        AND nb.bias_id != '99'
GROUP BY bias
ORDER BY num_biased_offenses DESC;
```

<img alt="image" src="https://github.com/user-attachments/assets/41ad0dc3-e951-415b-bacc-779b93af0546" />

The result showed that Anti-Black or African American bias was by far the most common type. Texas is a state where the majority of the population is non-white - almost 40% are Hispanic, and about 11% are black ([RHCA](https://regionalhca.org/hispanic-demographics/)), so seeing these rates is important for understanding biases and the nature of these crimes. Leaders and officials can use this information to adjust their education efforts and prevent bias early on in schools and elsewhere. They can direct resources to focus on particularly vulnerable areas for crime prevention and monitoring.

As with my other charts and graphs, I exported the result table in SQL as a csv file to make the data visualizations easier. I decided to make a straightforward bar chart showing the frequency of each bias. I chose to highlight the very high Anti-Black figure by making it a dark orange and lightening the other bars (by dragging bias to the color square). This is how the chart ended up:

<img alt="image" src="https://github.com/user-attachments/assets/59635c3d-679d-48ff-bc79-8b7ca7874b60" />

I wrote one more query to break down biased offenses by the race of the offender. I had to join the `nibrs_offender` table as well as the `ref_race` table to access this information:

```sql
SELECT 
    COUNT(ni.offense_id) AS num_biased_offenses,
    nl.bias_desc AS bias,
    race.race_desc AS race_of_offender
FROM
    nibrs_offense AS ni
        JOIN
    nibrs_bias_motivation AS nb ON ni.offense_id = nb.offense_id
        JOIN
    nibrs_bias_list AS nl ON nb.bias_id = nl.bias_id
        JOIN
    nibrs_offender AS offf ON ni.incident_id = offf.incident_id
        JOIN
    ref_race AS race ON offf.race_id = race.race_id
WHERE
    nb.bias_id != '88'
        AND nb.bias_id != '99'
GROUP BY bias , race_of_offender
ORDER BY race_of_offender ASC , num_biased_offenses DESC
```

<img alt="image" src="https://github.com/user-attachments/assets/6931c1b7-a48d-449d-b6bb-bc4e4ea2846b" />

I didn't end up including this in my visualizations, but it was interesting to see that 8 Anti-Black or African American offenses were committed by black offenders. There were also 12 Anti-White offenses by white offenders.

### Hate crimes organized by offense type

In order to help officials fight biased crime, it helps to know the most common types of crime - are they violent? Do they focus on property damage, or something else perhaps? This way, departments can know whether particular kinds of surveillance or preventive measures are effective or not and reallocate resources accordingly. Maybe a civilian patrol is more effective if vandalism is more common in an area.

First, I found out the breakdown for offense categories across all crimes. The offense and offense type tables proved sufficient:

```sql
SELECT 
    COUNT(o.offense_id) AS num_offenses,
    ot.offense_category_name AS offense_category
FROM
    nibrs_offense AS o
        JOIN
    nibrs_offense_type AS ot ON o.offense_code = ot.offense_code
GROUP BY offense_category
ORDER BY num_offenses DESC;
```

<img alt="image" src="https://github.com/user-attachments/assets/326cec54-745b-4198-a7db-04c785d2cd24" />

Larceny and assault topped the list. I adjusted the query to return the category, specific offense, and bias, filtering out cases without a bias:

```sql
SELECT 
    COUNT(o.offense_id) AS num_offenses,
    ot.offense_category_name AS offense_category,
    ot.offense_name AS Offense
FROM
    nibrs_offense AS o
        JOIN
    nibrs_offense_type AS ot ON o.offense_code = ot.offense_code
		JOIN
	nibrs_bias_motivation AS nb ON o.offense_id = nb.offense_id
WHERE
	nb.bias_id != '88'
        AND nb.bias_id != '99'
GROUP BY offense_category , Offense
ORDER BY offense_category, num_offenses DESC;
```

<img alt="image" src="https://github.com/user-attachments/assets/3229ccd3-7be9-4a1e-97a8-e60c80b79556" />

I exported this result as a csv and loaded it into Tableau. Since I was dealing with a part-whole relationship, I opted for a treemap to show the proportion of hate crimes that were a particular offense type. Larger rectangles correspond to greater frequency, and each shade of orange corresponds to an offense category (e.g., Assault, Larceny/Theft). Since there were many categories with only one offense, I decided to group these smaller ones as "Other" using Tableau's group feature. That way I only had to deal with five shades of orange instead of 14 or so (which would make it harder to distinguish):

<img alt="image" src="https://github.com/user-attachments/assets/2d426f95-380a-48f1-a325-1f274f648445" />

Here's the final chart:

<img alt="image" src="https://github.com/user-attachments/assets/a46742a1-d88d-45cc-9ec1-4faf63f97a45" />

