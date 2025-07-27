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

I then used this formula for color and text pills so that lower shooting percentages would be lighter, while higher percentages would be darker. The result was this:

HEATMAP

First, the blank space for Memphis' small forwards is there because there were simply no players listed as small forwards (according to basketball reference). This is further evidence of positionless basketball - the absence of a small forward was not the result of negligence by the general manager, but rather a consequence of the fact that there are multiple players who can fill the "wing" role on the court, even if they're primarily frontcourt of backcourt players.

Second, one of the main highlights for me is the high 3-point percentages of centers from the Nuggets and Knicks. They're shooting over 40 per cent, which is a really good mark - stretch bigs like Karl-Anthony Towns and Nikola Jokić are largely to blame, of course. Speaking of Jokić,

### Points/Rebounds/Assists Plot

These three statistics are the most important when making a glancing assessment of a player's production in the league, and Nikola Jokić is good at racking up all of them. The 3-time MVP and triple-double machine is one of the greatest players of all time, and probably the most skilled center of all time. The bubble chart I created does an excellent job of showing how much of a unicorn he is.

The chart is a scatterplot, but with four dimensions. The x and y axes denote total points and assists, respectively. To show rebounds, I added the TRB (total rebounds) stat to the size marker, meaning larger dots correspond to high rebound numbers. Lastly, I added a color dimension for position - each color refers to one of the 5 positions. What resulted was a dynamic chart that has a lot to say:

BUBBLE CHART
<img width="1657" height="801" alt="image" src="https://github.com/user-attachments/assets/47333c61-1bd9-44d6-844c-33b401088f62" />
