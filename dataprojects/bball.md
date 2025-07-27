# Sports Analytics: A Glance at the 2024-2025 NBA Season using Tableau

<img width="2400" height="497" alt="Tableau_Logo" src="https://github.com/user-attachments/assets/8c362c2e-cafe-4f06-89fe-ec89a94a14d1" />

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

<img width="777" height="785" alt="Screenshot 2025-07-27 162304" src="https://github.com/user-attachments/assets/378f7009-98ee-41ef-8ead-ad0dbecdbaa2" />

First, the blank space for Memphis' small forwards is there because there were simply no players listed as small forwards (according to basketball reference). This is further evidence of positionless basketball - the absence of a small forward was not the result of negligence by the general manager, but rather a consequence of the fact that there are multiple players who can fill the "wing" role on the court, even if they're primarily frontcourt of backcourt players.

Second, one of the main highlights for me is the high 3-point percentages of centers from the Nuggets and Knicks. They're shooting over 40 per cent, which is a really good mark - stretch bigs like Karl-Anthony Towns and Nikola Jokić are largely to blame, of course. Speaking of Jokić,

### Points/Rebounds/Assists Plot

These three statistics are the most important when making a glancing assessment of a player's production in the league, and Nikola Jokić is good at racking up all of them. The 3-time MVP and triple-double machine is one of the greatest players of all time, and probably the most skilled center of all time. The bubble chart I created does an excellent job of showing how much of a unicorn he is.

The chart is a scatterplot, but with four dimensions. The x and y axes denote total points and assists, respectively. To show rebounds, I added the TRB (total rebounds) stat to the size marker, meaning larger dots correspond to high rebound numbers. Lastly, I added a color dimension for position - each color refers to one of the 5 positions. What resulted was a dynamic chart that has a lot to say:

<img width="1657" height="801" alt="image" src="https://github.com/user-attachments/assets/47333c61-1bd9-44d6-844c-33b401088f62" />

The Joker's dot is not only seated at the top right of the chart, but is also pretty big. Many players have similar or even better point and assist counts than Jokić, but none of them have quite the same output on the glass besides Giannis, who happens to only have a little over half of Jokić's assist count. In short: Jokić can do it all, and he is one-of-a-kind.

Another stand-out worth talking about is SGA. He led the league in scoring, and not by a little bit. His dot is at the far right of the chart. It's hard to argue against his case for MVP, which he happened to win, alongside the franchise's first championship in Oklahoma.

Lastly, if someone knew nothing about basketball, this chart could help them make a key inference about the center position - the blue circles tend to be bigger than the others. This means they get more rebounds, which one can guess means that those players are the ones typically concerned with rebounds. And this person would be right - the centers are usually the tallest on the floor, grabbing boards and protecting the rim. As mentioned, though, centers who can only do those two things (unless they're super, super good at them, like Rudy Gobert) have begun to struggle to find a place in this 3-point-crazed sport. This is an example of how data visualization can lead to key inferences about the world around us.

### Team Scoring Distribution

I created two charts that dealth with team scoring distribution - one showed the team's season total point count by player, and the other by age group. I used a stacked bar chart where height denoted points, columns represented teams, and section sof the bars denoted players. I added a text label to see some of the big contributors off the bar. Now, NBA rosters have around 15 people, so things got a bit crowded, and the result was a chart that is not really ideal for that reason, but it was still interesting to see:

<img width="1641" height="786" alt="image" src="https://github.com/user-attachments/assets/770a5f72-50c8-4f6d-8859-81a11e7b52f6" />

There are way too many colors and there's only room for like seven names. But there is still insight to be gained. Our unicorn Jokić is in the spotlight again, making up a large section on the Nuggets' bar. One team that stood out to me was my very own San Antonio Spurs - no single bar took up a huge area, like we see for SGA and the Thunder. The distribution was fairly even, which could mean that the team didn't really have a designated scorer or go-to-guy (could be fair - despite having cornerstone and Rookie-of-the-Year Victor Wembanyama, the team is really young and building an identity), or they are really good at sharing the ball. In my limited watching of Spurs games this past season, I am more inclined to believe the former is the true, although I know our ball movement has improved.

The other stacked bar chart is much easier to read, and much more effective. It is organized by age group:

<img width="1656" height="794" alt="image" src="https://github.com/user-attachments/assets/6ab8a304-f292-4c3d-9dd1-28affa341817" />

This chart, like the other one, is sorted by total team points in descending order. It's really good at showing which teams' scoring loads are carried by younger or older players. The Grizzlies, for example, have only about 1.6% of their scoring from players who aree at least 30. Compare that with the Bucks, over half of whose points came from that age bracket. The Clippers and Warriors have similar distributions. This chart is really useful as a way to visualize team age - typically, metrics like average team age are used, but this chart takes into account the scoring load of the age groups instead of just estimating age.

### Assist Treemap

The last chart I made was a treemap emphasizing assist counts for players. I assigned each position a color and each player a box. The size of each box denotes the relative number of assists the player completed. Here's the chart:

<img width="1652" height="800" alt="image" src="https://github.com/user-attachments/assets/ed571095-63e5-463f-9d82-4f62d9331e1b" />

