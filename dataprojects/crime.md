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

Assault offenses make up the majority of hate crimes, while destruction and vandalism of property makes up a huge chunk as well. Using this information, departments can focus on ensuring there are effective surveillance technologies in strategic areas where vandalism or intimidation may occur.

### Violent Crime

In addition to biased crimes, I decided to incorporate agency data and determine counties and communities with proportionally high violent crime rates. In this analysis, I considered incidents instead of offenses mainly because the general public is more likely to be concerned with an *instance* of criminal activity as opposed to how many offenses were committed in a given interaction. This also made inflation of the numbers less likely, and ensured that MySQL wouldn't take forever to run my queries.

Another important thing to note is what is meant by *agency*. Many (not all) law enforcement agencies in Texas opt in to the National Incident-Based Reporting System, which is run at the federal level (FBI). So, there are several counties and communities that are not represented in the data. Also, some agencies cover multiple counties instead of just one (i.e., cities that are on county borders). I decided to determine the incidents per capita by agency to account for differences in communities within the same county - for example, San Antonio PD has a per capita crime rate, but so does Windcrest PD. Both are in Bexar County. Bexar County also has an agency - this corresponds to areas in the county that are not in San Antonio OR Windcrest (e.g., unincorporated communities). So, there might be a really high per capita crime rate in the urban parts of San Antonio, but a much lower rate in Windcrest. Lumping both of these together in a county rate does not account for these differences. Finally, in my hate crime per capita analysis, I did use a county analysis for several reasons, so it made sense to use a different approach in this chart to compare (only as far as a comparison is logical).

I started by looking at all incidents, not just violent ones. My goal was to produce a scatterplot with population and incident number to see the correlation and pick out agencies that had proportionally high or low rates. I removed agencies that covered a population of zero to prevent skewing in the scatter plot:

```sql
SELECT 
    a.ucr_agency_name AS Agency,
    a.population AS Population,
    COUNT(ni.incident_id) AS Number_of_Incidents
FROM
    agencies AS a
        JOIN
    nibrs_incident AS ni ON a.agency_id = ni.agency_id
WHERE
    Population > 0
GROUP BY Agency, Population
ORDER BY Population DESC
```

<img alt="image" src="https://github.com/user-attachments/assets/27061479-e996-46df-9ceb-789e9cb203d5" />

I imported the table into Tableau and made a scatter plot. The main issue: cities like Houston and San Antonio have huge populations compared to the smaller agencies, so the scale was pretty off:

<img alt="image" src="https://github.com/user-attachments/assets/597b3116-4a98-447e-8dfb-011ee4c478d2" />

My solution was to add a population filter slider so that a viewer could switch between viewing plots for large cities and small cities. This is the scatterplot scaled for agencies with a maximum population of 100,000:

<img alt="image" src="https://github.com/user-attachments/assets/44d14f94-f9ff-4251-a5d3-c363aaf2f543" />

This plot is much more interesting. Communities like Humble, Weslaco, and San Angelo stick out as more dangerous. But what kinds of crimes are happening in those places? Is it mainly just bad checks and white collar crimes (bad check is an actual offense in this data)? I found out by only including violent crimes. I had to join the offense type table and add to my `WHERE` clause. I asked MySQL to include only offenses in categories including homicide, sex offenses, and assault:

```sql
SELECT 
    a.ucr_agency_name AS Agency,
    a.population AS Population,
    COUNT(offf.offense_id) AS Number_of_Crimes
FROM
    agencies AS a
        JOIN
    nibrs_incident AS ni ON a.agency_id = ni.agency_id
		JOIN
	nibrs_offense AS offf ON ni.incident_id = offf.incident_id
		JOIN
	nibrs_offense_type AS ot ON offf.offense_code = ot.offense_code
WHERE Population > 0
  AND (
      ot.offense_category_name = 'Homicide Offenses'
      OR ot.offense_category_name = 'Kidnapping/Abduction'
      OR ot.offense_category_name = 'Assault Offenses'
      OR ot.offense_category_name = 'Human Trafficking'
      OR ot.offense_category_name = 'Sex Offenses'
      OR ot.offense_category_name = 'Sex Offenses, Non-forcible'
  )
GROUP BY Agency, Population
ORDER BY Number_of_Crimes DESC
```

A very similar but slightly different chart resulted:

<img alt="image" src="https://github.com/user-attachments/assets/3248aed1-58e2-49f8-83b6-d21309f704bf" />

As the tooltip shows, Humble moved a bit closer to the trend line, while the other two aforementioned communities remained as relative outliers. I included the population slider for viewer use. A hover over the trend line shows an R squared value of about 0.718, which is a very strong correlation as expected (more people = more crimes). This chart is a very simple yet effective one at determining which counties and agencies struggle the most with violent crime. Federal agencies and neighboring/overlapping jurisdictions can assist accordingly and help bring the numbers down.

### Hate Crimes per Capita

This last analysis 
