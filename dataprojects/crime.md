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

Crimes are organized by **incidents** at the hightest level. Each incident can have multiple **offenses**, which are essentially separate crimes that occurred in an incident. Each incident can be explored via tables that show administrative info (e.g., whether an offender was cleared exceptionally), property that was lost/damaged, the victims involved, offender demographics, and arrestee information. Everything from the date and hour the incident occurred to the victim's ethnicity to the measure of drugs possessed is contained in the files.

To help explain these relationships, [a very helpful diagram](/files/nibrs_diagram.pdf) was included in the zip file. There is so much detail included, so I had to pick a focus or else I would spend my entire life exploring it. I chose to focus on hate crime data because I 
