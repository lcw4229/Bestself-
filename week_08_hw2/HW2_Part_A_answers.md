# POLS 209 — Homework 2, Part A: answers

## Lab record

**Line 1 (block 3).** Seed 73519 · my_share 0.504 · my_lower 0.455 · my_upper 0.553 · contains 0.502: yes.

**Line 2.** `gazette_10000.png` is in this folder. Its title is "Gazette polls of homeowners all land far below the island's share".

---

## 1. Whose opinion each poll measures

**a.** The station's poll is meant to describe all 59,838 adults on Merrow. Its estimand is the share of those adults who voted yes on Proposition 1. The census puts that share at **50.2%**.

**b.** **THE HOMEOWNERS SPEAK: NO, 55 TO 45.** The cards were drawn from the property-tax roll, so they only measured adults who own their home. In the census, **44.8%** of homeowners voted yes.

## 2. The sampling distribution and the standard error

**a.** Each bar counts how many of the 1,000 random polls of 401 had a yes share inside that one-point-wide bin. The shares center on about 50.2%, the island's share, and nearly all of them fall between about 43% and 57%.

**b.** The 2.5 points does not say how far off our poll was. It describes how much polls of 401 scatter from one random sample to the next. Across 1,000 such polls, the yes shares had a standard deviation of 2.5 points (`sd_share_401` = 0.0250) around the island's share, so a typical poll lands about 2.5 points from the truth. Some land closer and some farther. Our actual poll found 49.1% against the census's 50.2%, so it was **1.1 percentage points** too low.

## 3. How often would a poll of 1,001 put "no" ahead?

The island's share is (50.22 − 50) / 1.58 ≈ **0.14 standard errors** above 50%. The normal curve gives `below_50_1001` = 0.445, so about **44.5%** of polls of 1,001 should put "no" ahead. In the simulation, 437 of 1,000 polls (**43.7%**) did, which is close to the prediction. Yes won by such a small margin that even a poll of 1,001 is not much better than a coin flip at naming the winner.

## 4. What "95%" promises

**a.** The 95% describes the method, not this one interval. The island's share is a fixed number, and any given interval either contains it or does not. The 95% means that if you drew many random samples and built an interval the same way from each, about 95% of those intervals would contain the island's share. My simulation backs this up: 948 of the 1,000 intervals from polls of 401 (**94.8%**) contained 50.2%.

**b.** About 5% of 280 is roughly **14 intervals** that would miss the island's share. Mine was not one of them: my interval, from 45.5% to 55.3%, contained 50.2%. Without a census, a student would have no way to tell that their interval missed. They only see their own sample, and a missed interval looks exactly like one that hit.

## 5. Ten thousand cards from the property-tax roll

**a.** Bias = E[Ȳ] − μ = 44.8% − 50.2% = **−5.4 percentage points**. With 20,000 cards:

- The standard error shrinks by a factor of √2, from about 0.5 to about **0.35 points**.
- The margin of error shrinks from about 1.0 to about **0.7 points**.
- The center of the sampling distribution stays at **44.8%**, the homeowners' share.
- The bias stays at **−5.4 points**.

The miss was not bad luck. It is built into the list the Gazette samples from: renters and other non-owners are left out, and they voted yes more often. More cards measure homeowners more precisely, but they never reach the rest of the island.

**b.** A Gazette interval stays centered near 44.8%, the homeowners' share, no matter how many cards are mailed. As the poll grows, the interval gets narrower around 44.8%. At 401 cards the margin is about ±4.9 points, wide enough to reach 50.2% fairly often (429 times in 1,000). At 1,001 cards it is about ±3.1 points and rarely reaches (76 times). At 10,000 cards it is about ±1.0 point, so it never reaches 50.2%, which is 5.4 points away (0 times). A bigger poll makes the Gazette more confident about the wrong number.

**c.** The Gazette's polls would have centered on **62%**, the homeowners' share. Their bias was 62% − 59.5% = **+2.5 points**. They named the winner: both 62% and 59.5% are above 50%, so the Gazette called yes, and yes won. A biased poll still names the winner when the bias does not push its share across 50%, so a lopsided race can hide a biased poll.

## 6. Planning Radio Merrow's next poll

**a.**

    1.96 × 0.5 / √n = 0.035
    0.98 / √n       = 0.035
    √n              = 0.98 / 0.035 = 28
    n               = 28² = 784

The station should interview **784 islanders**.

**b. Methods note.** Radio Merrow interviewed 784 adults chosen at random from the full census list of all 59,838 adults on Merrow, so every islander, whether they own, rent, or neither, had the same chance of being picked. The poll's margin of error is ±3.5 percentage points at 95% confidence. Even a properly random poll misses by more than its margin of error through chance alone, about once in every 20 polls. A poll can also miss when the list it draws from leaves out part of the population: the Gazette samples only homeowners from the property-tax roll, so its polls center on the homeowners' 44.8% yes rather than the island's 50.2%, and mailing more cards does not fix that.
