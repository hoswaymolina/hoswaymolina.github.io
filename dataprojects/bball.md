# Sports Analytics: A Glance at the 2024-2025 NBA Season using Tableau

Recently, I watched Moneyball for the first time, and I wonder why I never watched it sooner. Baseball is not my favorite sport, but I knew that stats and analytics has transformed other sports as well, including basketball. It’s a dream of mine to work for my hometown team, the San Antonio Spurs, one day. While I never played basketball outside of recreational leagues, I know I can still apply my statistical and mathematical knowledge to be of value to any team.

In this project, I practiced my data visualization skills on the most recent NBA season’s data. While these aggregations and summaries are a far cry from the predictive models and sabermetrics that pro team data professionals use, they’re at least a solid stepping stone into that world. I had a lot of fun diving into the data, and I hope you will too!

Some highlights from this project:

- Jokić continues to dominate in the major offensive categories
- Denver and New York demonstrate big man shooting excellence, with center 3-point shooting percentage exceeding **40%**
- Memphis leads the youth movement, with **only 165** of the ~10,000 points they scored this season being scored by players **30 years of age and older**.

Keep reading to find out how I got there!

## The Dataset

The data set is Basketball Reference's [2024-2025 NBA Player Stats: Totals](https://www.basketball-reference.com/leagues/NBA_2025_totals.html) table. This trusted site provides excellent summary data for teams, players, and seasons. I had to copy it as table separated by commas, meaning I had to do some work in Microsoft Excel to put the values into separate rows and columns. To do this, I simply used the "Text to Table" function, listed commas as the delimiter, and the table was created.

## Visualization

### 3-point Percentage by Position/Team

Modern basketball is characterized as being "positionless" - since the 3-point shooting revolution, players of every position and size are expected to space the floor with their ability to shoot. As a result, it is rather normal (perhaps expected) for frontcourt players (forwards and centers) to have 3-point shooting ability. I created a heatmap to visualize how efficient each position was at shooting the 3-ball, and I also organized it by team to see which teams had more success in this regard.

With the position and team pills in the column and row shelves, I had to do some calculations in Tableau to get accurate average shooting percentages. Since volume is not accounted for when taking the "average of averages," I created a simple formula in Tableau which divided the sum of 3-pointers made by the sum of 3-pointers attempted (by each position):

`SUM([all_rows (nba_project)].[3P])/SUM([all_rows (nba_project)].[3PA])`

