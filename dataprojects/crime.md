# Violent and Hate Crime in Texas

Oh yeah

## Why this project?

## The Data

The FBI's [Crime Data Explorer](https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/home) has a wealth of real-life crime data avaialable for the public. I highly recommend it as a data source for anyone interested in doing projects with crime data. They make it easy to access with a [Documents and Downloads](https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads) button from which one can download excel worksheets (for the smaller datasets) or zip files (for the bigger data dumps). I wanted to have the freedom to explore the data in as much or as little detail as I wished but also work with a manageable dataset size. So, I opted to download the Crime Incident-Based Data for Texas in 2024, which at the time of writing was the most recent data:

<img alt="image" src="https://github.com/user-attachments/assets/e333e4ee-259d-4df0-b4a4-9142a1b18957" />

I downloaded a zip file containing over 40 csv files, a readme, and 2 SQL scripts to load the data with. They were written for PostgreSQL, which gave me a huge headache at the beginning of the project that I will explain later. That said, these scripts had much of what I needed, and even though I had to edit them to work for MySQL, they still saved me a huge amount of time.

### Further Notes

