# roulette

In the first few months of 2016 I visited several South American countries. There were casinos everywhere, 
and I found that I could quickly and consistently win money playing roulette using a simple strategy.

The strategy is to bet on a color, either red or black, and if you lose, double your bet on the opposite color. If you lose again,
double down again and keep your bet on the same color. The laws of probability say that the longer a streak of a certain color continues,
the more improbable a continued streak of that color will be.

Since I was able to win so consistently, I was wondering if I had stumbled onto a sure-fire way to win money when I gambled. It didn't
add up.

So, as any good developer would do, I decided to put this to the test and roll my own roulette simulation.

Over the course of a few days, I built this simulator to test my chosen roulette strategy. It will automatically play with a given
roulette strategy until its bankroll hits 0. I quickly discovered that the bankroll always dropped to zero, and that my hot streak
was simply the result of luck. I had bought into the Gambler's Fallacy...the idea that I was 'owed' a certain color after several
spins.

While the probability of a set of 4 or 5 spins landing on a certain color is low, the probability of each spin is only 50%. The roulette
table has no memory, and you're not betting on 4 or 5 spins in a row...you're betting on the outcome of a particular spin.

What can I say? Humans are bad at statistics.
