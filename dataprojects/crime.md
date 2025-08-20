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

I then grouped the query by bias. Since the bias motivation table only had the bias id (NOT the name of the bias), I decided to link a third table - the bias list table - so I could return the `bias_desc` column instead of a number. That way, anyone seeing the result could see the bias type without having to go back and forth between the bias list table and the query result:

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

