# How Likely are you to win a game of "Highlow"?

My friends and I have a Discord server to make it easier to organize online gaming. But we also have some channels that are for fun - one of these is the "pancake" channel, where we collect, earn, and gamble a fake digital currency (pancakes). There are typical gambling games like blackjack and slots, for which much ink has been spilled concerning probability and statistics-informed strategies for winning. I have no more than a terribly basic understanding of those games. However, one of the pancake games is called with a command "p! highlow". I choose to just call the game "Highlow". There is no bet involved, so it's not gambling, but you do earn pancakes if you win.

It's pretty simple: a random integer from 1 to 100 is generated. The player must then decide whether the next randomly generated integer within the range will be higher or lower than the first one. After this, a new number is generated (if it is the same as the first number, a new random number is generated), and if the player is correct, they win the game (and 20 pancakes). Otherwise, they don't lose or gain any pancakes.

It's a straightfoward game. The best strategy for winning is intuitive - if our first number (let's call it n1) is 50 or below, we should select "high". Otherwise, we should select "low". Our chance of winning is also straightforward to see - if n1 is 34, then you have around a 66 percent chance of winning, while a draw of 82 yields around an 82 percent chance of winning (we'll be exact about it later). The further your number is from the middle, the better your chances.

This got me thinking - we know the chance of winning given our first draw, but what is the chance of winning the game *overall*, before we are given a number in the first place? This question was a bit harder to answer, but it was fun to figure out and also let me practice some of my data/programming skills, so I thought it would be cool to share!

## First... some Probability

### Probability of winning given first number

Earlier, I mentioned that finding the chance of winning given our first number (we'll call it n1) was straightforward. Let's go over the math. Once n1 is selected, the next number (we'll call it n2) MUST be distinct from n1. This means there are 99 possibilities for n2. If we guess "high", then the chance of winning is equal to the number of outcomes higher than n1 divided by 99. This will be greater than 50% as long as the number of outcomes higher than n1 is at least 50. From this, we see what our intuition told us: if n1 is 50, there are 50 outcomes above n1 versus 49 below. If n1 is 51, there are 50 outcomes below n1 versus 49 above. So we have a rule:

n1 < 51 --> guess "high"
otherwise --> guess "low"

Choosing this way guarantees a chance of winning of at least 50/99 = 50.5%, with the chance growing as n1 increases or decreases.

### Probability of winning overall

We understand how to find the chance of winning if we know n1. But how can we find out the probability of winning the game before we know n1? In other words, what percentage of attempts at this game should we *expect* to win? We can call this the *overall probability* or *average probability* of a win. To answer this, we will learn (or review) some probability theory and use the *law of total probability*.

In this game, there are 100 equally likely possibilities for n1. For each possibility, the player can choose either "high" or "low". Let's assume that the player **only** chooses the option which gives them the best chance at winning. In this case, *after* n1 is selected, there are two possible outcomes: a win or a loss. This means we have exactly 198 scenarios: for n1 = 1 or n1 = 100, we have a win. For n1 =
