# A Dive Into FBI Crime Data (Excel, SQL, Tableau)

<img width="426" height="438" alt="FBI_Badge_2" src="https://github.com/user-attachments/assets/ea0043fd-7696-4fdd-a42c-d1a1a8c2196c" />

***To interact with the dashboard on Tableau Public, go [here](https://public.tableau.com/shared/S3R9BHNFX?:display_count=n&:origin=viz_share_link)!***

Data is powerful. No one can deny the fact that analytics, statistics, and the scientific method have transformed the way we make decisions. It helps companies make more money. It helps sports teams win more. It can also help make the world a better place.

When I decided to dive into data analytics, I was worried because I didn't want to simply calculate profit, track KPIs, and look at sales numbers. I wanted to be in a field where I knew I was helping people. You can absolutely help people, directly or indirectly, by calculating profit, tracking KPIs, and looking at sales numbers, but doing analytics in certain industries allows for a more tangible way to impact lives. One of those fields is crime-fighting.

## Why this project?

In this project, I chose a topic in a field that interests me deeply - crime. There is a lot of crime data available for public use, but I decided to focus on violent and hate crimes since these are particularly appalling and terrible. I'm glad to know many friends across racial, ethnic, and national lines, so it hurts me to see groups of people discounted and dehumanized in the form of hate crimes. I hope this project can move the needle even just a little bit in raising awareness and fighting bias of every kind!

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

Loading the 40+ csv files into MySQL was a bit of a hassle. The load scripts were written for PostgreSQL, so the first thing I tried was to import each csv file using the import wizard. Some files were too big for this to work. They would start importing, but the progress bar would never fill up. So I would cancel the upload, but then see that the table showed up. I thought the issue was just a progress bar glitch, so I would import all these tables thinking that they loaded correctly. When I started querying the data, however, I realized that many were empty, and that things were not in fact loaded correctly.

At this point, I realized I had to upload the tables manually. I was able to copy the portion of the .sql files that created the tables just fine, but I had to comb through the errors and find out which parts of the script were PostgreSQL-only. That took forever, only for there to be more loading errors. I decided that maybe I would be better off downloading PostgreSQL and loading it that way. But I was absolutely unprepared for the amount of packages and options I had. There was no way for me to figure out what I needed and didn't need, not at the hour of night that it was.

I was very discouraged at this point, and almost changed topics or datasets. But I decided to take another crack at it the next day. With the help of ChatGPT, I was able to methodically diagnose the issues step by step. I ended up creating the tables just fine, but I would run the manual scripts for loading (`LOAD DATA INFILE`) and it would say it did not have the right permissions. I kept checking both the client and server side to make sure `LOAD DATA INFILE` was working, but it wouldn't budge. Finally, ChatGPT suggested that I run the load script I made from the terminal. I did this (as Administrator):

<img alt="Screenshot 2025-08-15 171013" src="https://github.com/user-attachments/assets/72921ecd-a901-4803-b44a-e4690459d582" />


...and what ensued were several minutes of waiting and suspense as the terminal executed each load command, some taking several minutes (these csv tables are HUGE!):

<img alt="image" src="https://github.com/user-attachments/assets/45e1a032-a520-4d38-b66e-3c160b3745a5" />

When the process finally ended, I wrote some queries, AND IT FINALLY WORKED!!! I was so happy that I didn't give up. I learned a lot about loading data and troubleshooting those few days - ask for help, start over with a clean slate (as many times as you need to), and never give up!

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

This last piece of analysis brings us back to hate crime. I love maps, especially choropleth maps (shaded maps), so since I was working with states and counties, I HAD to incorporate a map.

The last chart identified communities that struggled with violent crime, and I wanted this map to show which areas struggled with hate crime. There were a lot of issues and considerations when developing this map, and there weren't a lot of time- and effort-efficient ways to implement it (at my current level of Tableau expertise, at least!), but I think it ended up doing a decent job at showing trends.

### Considerations

The first thing to point out is that biased offenses, or hate crimes, are sometimes really easy to identify (e.g., vandalism with slurs), but are mostly not so easy. The FBI defines hate crimes as "criminal offenses that were motivated, in whole or in part, by the offender’s bias against the victim’s race/ethnicity/ancestry, gender, gender identity, religion, disability, or sexual orientation, and were committed against persons, property, or society" ([Hate Crime Methodology](/files/hate_crime_methodology.pdf)):

> Because motivation is subjective, it is sometimes difficult to know with certainty whether a crime resulted from the offender’s bias. Moreover, the presence of bias alone does not necessarily mean that a crime can be considered a hate crime. Only when a law enforcement investigation reveals sufficient evidence to lead a reasonable and prudent person to conclude that the offender’s actions were motivated, in whole or in part, by his or her bias, should an agency report an incident as a hate crime.

The point is that many hate crimes are not recorded because there is not sufficient evidence, or maybe no evidence at all. In the very first query I showed above, I found out that there were 479 hate crimes, while violent crimes alone in the state tower above 60,000. Statistical significance is much easier to achieve with 60,000 data points instead of 479. Considering some counties have a population under 2,000, a single hate crime occurrence will catapult its per capita rate extremely high compared to 100 hate crimes in a city like Houston.

The last major consideration has to do with agency data. As previously mentioned, some agencies cover multiple counties. This means that an agency covering two counties or more counties might record a hate crime. If organizing crimes by county, this leads to ambiguity - in which county was the crime committed? If organizing crimes by agency, however, we get even more "small number" issues, with many municipalities being small enclaves within large metropolitan areas.

### Methodology

My solution was to extract the biased offenses first by agency. Then, I grouped the counts by county and found the population. So I had a county, population (which was actually the population of the *agency*), and the number of biased offenses (hate crimes). To make this calculation easier (and prevent too many joins from happening), I used temporary tables (`WITH` function) to make sure I could have the population and offense count in the same place and produce a column with the calculation. Since I was dealing with very small numbers, I found the hate crime rate per 10,000 people. I rounded this number to 3 decimal places to make it cleaner. I was then able to execute a query and get a result:

```sql
WITH biased_offenses_by_county AS (

SELECT 
    COUNT(o.offense_id) AS biased_offenses,
    a.county_name AS county
FROM
    nibrs_offense AS o
        JOIN
    nibrs_incident AS ni ON o.incident_id = ni.incident_id
        JOIN
    agencies AS a ON ni.agency_id = a.agency_id
        JOIN
    nibrs_bias_motivation AS nb ON o.offense_id = nb.offense_id
WHERE
    nb.bias_id != '88'
        AND nb.bias_id != '99'
GROUP BY county
ORDER BY biased_offenses DESC
),

county_population AS (
    SELECT county_name, SUM(population) AS population
    FROM agencies
    GROUP BY county_name
)

SELECT
	bc.county,
    ROUND((bc.biased_offenses * 10000.0)/(cp.population), 3) AS biased_offenses_per_10000_people,
    bc.biased_offenses,
    cp.population
FROM biased_offenses_by_county AS bc
		JOIN
	county_population AS cp ON bc.county = cp.county_name
ORDER BY biased_offenses_per_10000_people DESC;
```

<img alt="image" src="https://github.com/user-attachments/assets/780c9289-5aff-48b7-9097-ce1ace04c627" />

This was pretty close to what I needed, but I hadn't accounted for the small numbers. Rather than deal with that in SQL, I decided to save this table and clean it up in Excel/Tableau - my goal was to have one map without a filter, and annother map with the population floor. Also, I could clean up the overlapping county issue in Excel much easier.

I exported this result into a csv and loaded it in Excel. My goal was to consolidate any overlapping counties into a single county group. There were already some "county groups" like I mentioned before - one had Atascosa, Bexar, and Medina counties all in one. My workflow was to find the largest county group, identify any counties that belonged to it, and add the hate crime count and population to that group. I used the Find and Replace function to execute this. As an example, one of the large county groups at one point was Collin, Dallas, Denton, and Rockwall (it ended up absorbing even more counties). I found any groups that contained only a subset of those counties, replaced the name with the bigger county group:

<img alt="Screenshot 2025-08-19 200624" src="https://github.com/user-attachments/assets/7f087bbc-de40-402f-a454-c04d0ed1c839" />

After this, I had a table with disjoint county groups (many "groups" only had one county), so that there was no overlap. I applied a filter to see only the multi-county groups (only cells with a comma). I made a column in which I used a `SUMIFS` formula - if it found the right county group in the county name column, it would add up the population (and, in the next cell, add up the crime count):

<img alt="Screenshot 2025-08-19 202949" src="https://github.com/user-attachments/assets/ff3d5419-80b5-4f74-aa77-c521a4d00e7b" />

Then I could delete all the duplicate rows and have a single county group with the correct aggregate numbers for population and crime count.

I wish that was the end of it, but I ran into more challenges.

It would have been very hard to use this table for a map in Tableau since I wasn't using individual counties, but rather county groups. It would be hard for Tableau to recognize them. So my friend ChatGPT told me I should make a helper column and break up the county groups by listing each county (by inserting new rows) in this column:

<img alt="image" src="https://github.com/user-attachments/assets/8a798cbd-9043-4177-9557-eea10eac453b" />

Now, while I couldn't have each county group as its own contiguous geographic feature, I could attribute to each county the population and offense count of its county group. In other words (and as you will see), counties in a group will be shaded the same color since they share a per capita hate crime rate, but they will still be shaded and show up as different counties.

I could finally import this table into Tableau:

<img alt="image" src="https://github.com/user-attachments/assets/ec2983c2-5347-4c24-9378-a2f1ed22773a" />

This map doesn't account for low populations or single offense counties. But I also wanted the filter to just have a filter option and a not filter option (not an "all counties", "excluded counties", and "included counties" option like the traditional filter method would have given). So I implemented a more unconventional method for the filter. First, I made a parameter with two string options: Filter Applied, and No Filter. I then showed the parameter control so that a viewer can toggle it. Next, I made a calculated field. This field is a Boolean, checking if the population and offense count meet the threshold if the filter applied parameter is on:

<img alt="image" src="https://github.com/user-attachments/assets/02d084f4-cd65-4f50-9a81-41aca3c697fb" />

If the filter is off, all the values are "True". If the filter is on, only the counties that meet the threshold are "True":

<img alt="Screenshot 2025-08-20 165100" src="https://github.com/user-attachments/assets/4149e0d6-19e1-4a42-80cc-f062679f2e2e" />

Now the choropleth highlights certain counties with the filter off (Armstrong County way up north, shown below), but the county doesn't even show up when the filter is on. The county has a population of less than 2,000 and only one hate crime, so it is put aside by the filter as not having enough data or a sample that is large enough. To make sure this issue is highlighted, I included the county group population and offense count in the tooltip, which is shown below for Armstrong County (filter off):

<img alt="image" src="https://github.com/user-attachments/assets/77e99c7f-e75e-49e6-89ff-1fba69c35668" />

I encourage you to check out my dashboard on Tableau Public (in full-screen mode) to play with the filter and explore the counties yourself!

### The Dashboard

My dashboard is [published on Tableau Public](https://public.tableau.com/shared/S3R9BHNFX?:display_count=n&:origin=viz_share_link), and I encourage you to look at it there on full-screen so you can use the population sliders and filters, but here's a screenshot of the dashboard:

<img alt="image" src="https://github.com/user-attachments/assets/bf9cda17-77da-405d-a240-b60b0fd9404f" />

## Takeaways

These charts and insights can directly assist law enforcement and are actionable. One of the main learning points for law enforcement in Texas is the prevalence of hate crimes in rural areas. This project identifies specific counties of interest. Even after accounting for low population, rural counties tend to take the lead in per capita hate crime counts. Law enforcement in these areas should work with locals and federal officials to ensure not only that education and community is fostered to prevent bias from happening in the first place, but also to explore preventative techniques like community patrols and installing up-to-date surveillance eqeuipment.

Similarly, the scatter plot shows several counties that struggle with violent crime rates. Cooperation between adjacent agencies (such as Humble and Houston/Harris County) is crucial to solving those issues.

I ran into many issues during this project, most of which happened before I was even able to write a query. I worked through the loading process over 3 days until I finally figured it out. Formatting the dashboard and figuring out how to navigate overlapping counties and agencies were also sources of headaches. But it wasn't anything that my brain, my community, the internet, or ChatGPT couldn't help me with. My skills in all three of SQL, Excel, and Tableau grew a great deal, and I am super pleased with how this project turned out. I'm excited to keep learning and refining my skills!

# Thanks for Reading!

Compared to my other projects up to this point, this one is a LONG read. If you read even only part of it, thanks for taking a look! I appreciate any and all feedback. Connect with me on [LinkedIn](https://hoswaymolina.github.io/) and let me know what you thought! Have a great day!
