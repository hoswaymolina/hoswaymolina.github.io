# How Likely are you to win a game of "Highlow"?

My friends and I have a Discord server to make it easier to organize online gaming. But we also have some channels that are for fun - one of these is the "pancake" channel, where we collect, earn, and gamble a fake digital currency (pancakes). There are typical gambling games like blackjack and slots, for which much ink has been spilled concerning probability and statistics-informed strategies for winning. I have no more than a terribly basic understanding of those games. However, one of the pancake games is called with a command "p! highlow". I choose to just call the game "Highlow". There is no bet involved, so it's not gambling, but you do earn pancakes if you win.

It's pretty simple: a random integer from 1 to 100 is generated. The player must then decide whether the next randomly generated integer within the range will be higher or lower than the first one. After this, a new number is generated (if it is the same as the first number, a new random number is generated), and if the player is correct, they win the game (and 20 pancakes). Otherwise, they don't lose or gain any pancakes.

It's a straightfoward game. The best strategy for winning is intuitive - if our first number (let's call it $n_1$) is 50 or below, we should select "high". Otherwise, we should select "low". Our chance of winning is also straightforward to see - if $n_1$ is 34, then you have around a 66 percent chance of winning, while a draw of 82 yields around an 82 percent chance of winning (we'll be exact about it later). The further your number is from the middle, the better your chances.

This got me thinking - we know the chance of winning given our first draw, but what is the chance of winning the game *overall*, before we are given a number in the first place? This question was a bit harder to answer, but it was fun to figure out and also let me practice some of my data/programming skills, so I thought it would be cool to share!

## First... some Probability

### Probability of winning given first number

Earlier, I mentioned that finding the chance of winning given our first number (we'll call it $n_1$) was straightforward. Let's go over the math. Once $n_1$ is selected, the next number (we'll call it $n_2$) MUST be distinct from $n_1$. This means there are 99 possibilities for $n_2$. If we guess "high", then the chance of winning is equal to the number of outcomes higher than $n_1$ divided by 99. This will be greater than 50% as long as the number of outcomes higher than $n_1$ is at least 50. From this, we see what our intuition told us: if $n_1$ is 50, there are 50 outcomes above $n_1$ versus 49 below. If $n_1$ is 51, there are 50 outcomes below $n_1$ versus 49 above. So we have a rule:

$n_1$ < 51 --> guess "high"

otherwise --> guess "low"

Choosing this way guarantees a chance of winning of at least 50/99 = 50.5%, with the chance growing as $n_1$ increases or decreases.

### Probability of winning overall

We understand how to find the chance of winning if we know $n_1$. But how can we find out the probability of winning the game before we know $n_1$? In other words, what percentage of attempts at this game should we *expect* to win? We can call this the *overall probability* or *average probability* of a win. To answer this, we will learn (or review) some probability theory and use the *law of total probability*.

In this game, there are 100 equally likely possibilities for $n_1$. For each possibility, the player can choose either "high" or "low". Let's assume that the player **only** chooses the option which gives them the best chance at winning. In this case, *after* $n_1$ is selected, there are two possible outcomes: a win or a loss. This means we have exactly 198 scenarios: 2 for $n_1$ = 1 or $n_1$ = 100, where we have a win. For $2 \leq n_1 \leq 99$, we have either a win or a loss, so for 98 numbers, each with 2 possible outcomes, we have $98 \cdot 2 = 196$ outcomes. In statistics, we call the set of all possible outcomes the *sample space*, which we can call $S$.

We can break this space $S$ up into groups, or *subsets*; for example, let's group together outcomes with a common $n_1$. In other words, the outcomes \{$`n_1`$ and win\} and \{$`n_1`$ and loss\} would be in the same subset, and they actually constitute the entire subset, since these are the only possible outcomes given $n_1$. Let's call these sets $B_n$, of which there are 100 for each possible $n_1$. These sets do not overlap, ***and*** they constitute the entire sample space $S$ - this means they form a *partition* of the sample space. We might also group together all of the winning outcomes in $S$ - let's call this subset $W$. This would include the outcomes \{2 and win\}, \{3 and win\}, \{4 and win\}, and so on.

Using this information, we can use the *law of total probability*. In English, it states that if we have a partition with $k$ elements of a sample space $S$ (where each subset in the partition has a nonzero probability), and we have some event A that is a subset of $S$, then the probability of A happening is equal to the sum of joint probabilities $A$ **AND** $B_i$ (for each element $B_i$ of the partition). In symbols, we have

```math
P(A) = \sum_{i=1}^{k} P(A|B_i)P(B_i)
```

$P(A)$ represents the probability of event A, while $P(A|B_i)$ represents the probability of $A$ given the event $B_i$ has occurred.

In our problem, we have a partition of $S$, namely \{$`B_1`$, $`B_2`$, ... , $`B_{100}`$\}, and a subset $W \subset S$. Plugging these in to the equation gives us

```math
P(W) = \sum_{i=1}^{100} P(W|B_i)P(B_i)
```

In other words: To find the probability of winning the game, we must find **(for every possible $n_1$)** the probability of winning *given a draw of* $n_1$ AND drawing $n_1$ in the first place, then summing all 100 of these probabilities. For example, consider $n_1 = 1$. The probability of winning given a draw of 1 is 100%, while the probability of drawing a 1 is 1%. So, the probability of the outcome \{1 and win\} is 1%. Now consider $n_1 = 25$. The probability of winning given a draw of 25 is $\frac{100-25}{99} = 75.76\\%$, while the probability of drawing a 25 is 1%. Thus, the probability of the outcome \{25 and win\} is approximately 0.76%. One can see how adding up these probabilities gives us the total probability of a win: We are simply finding the probability of \{$`n_1`$ and win\} for all $n_1$, which constitutes all of the winning events without overlap (since more than one $n_1$ cannot be drawn).
