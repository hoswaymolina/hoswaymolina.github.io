# Debt and Development in the Levant: Jordan and the World Bank

In June 2025, I went on a transformative and impactful trip to Jordan. I loved immersing myself in the language, food, and people of a nation quite different than any other I had visited.

The country of Jordan will always hold a special place in my heart. Naturally, when I started the first SQL project in Avery Smith's Data Career Jumpstart, I knew that I would focus on Jordanian data. Among Middle Eastern nations, Jordan is quite stable. Historically, they have also had much support and influence from the West. All this considered, I knew it would be interesting to see how Jordan matched up relative to other countries in the region (and across the world). Have they borrowed more or less than others? What kinds of projects have they directed those loans to?

I discovered that:

- Among Middle Eastern and North African countries, **Jordan ranks 5th out of 10** in number of loans.
- Globally, **Jordan ranks 80th out of 130** in amount owed to the IDA.
- **Education and highways** are **among the top 10 project types** pursued in Jordan.

Keep reading to see how I found out!

## The Dataset

This dataset is a .csv file containing historical data from the [IDA Statement Of Credits, Grants and Guarantees](https://financesone.worldbank.org/ida-statement-of-credits-grants-and-guarantees-historical-data/DS00976), which is available on the World Bank Group website. The data used for this project was updated on June 30, 2025. There are 1.4 million rows, making SQL a much better choice for analysis than Excel. I used CSVFiddle to write queries. I enjoyed how simple and straightforward the environment is - it's perfect for learning SQL, while hosts like BigQuery can be more confusing for beginners.

It is worth noting that, as a historical database, the sums used in this project are "cumulative" sums, not regular sums. That is, when the amount owed is listed, it does not represent the amount owed in that instance. The choice to use cumulative sums versus regular sums was for simplicity's sake.

## Analysis

I decided to begin by seeing how the Middle East and North Africa (MENA) region compared to the other regions. I summed the amount owed to the IDA, grouped by region, and then placed the rows in descending order:

<img src="images/bank/q_region_rankings.png?raw=true"/>
<img src="images/bank/r_region_rankings.png?raw=true"/>

So, MENA ranks 9th out of 12. I then turned my attention to Jordan's ranking global ranking in amount owed:

<img src="images/bank/q_total_owed_global.png?raw=true"/>
<img src="images/bank/r_total_owed_global.png?raw=true"/>

This shows a ranking of 80th out of 130. So, in terms of amount owed, Jordan is in the **40th percentile** in amount owed to the IDA. It's safe to say that Jordan is roughly middle-of-the-road.

I was mainly curious about how Jordan compared to other MENA countries, so I dove deeper into trends within the region. I looked at the number of loans taken out and placed the countries in order:

<img src="images/bank/q_numloans.png?raw=true"/>
<img src="images/bank/r_numloans.png?raw=true"/>
