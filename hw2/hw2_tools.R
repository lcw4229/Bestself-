# hw2_tools.R: one function written for POLS 209 Homework 2.
# Your script loads it with source("hw2_tools.R"), near its top.
# It draws many random polls from a population and keeps one row per poll.

run_polls <- function(population, column, n, polls) {
  # population: the data frame to draw from (everyone who could be interviewed)
  # column: the name of a 0/1 column, in quotes (for example "zoning")
  # n: how many people each poll interviews
  # polls: how many separate polls to draw
  share <- numeric(polls)   # a vector of zeros, one slot per poll, for each share
  se <- numeric(polls)      # another vector of zeros, for each poll's standard error
  for (i in 1:polls) {      # repeat the lines inside the braces once for each poll
    rows <- sample(nrow(population), n)   # pick n row numbers at random, none twice
    poll <- population[rows, ]            # keep those rows and every column: one poll
    share[i] <- mean(poll[, column])      # this poll's share of 1s, stored in slot i
    se[i] <- sd(poll[, column]) / sqrt(n) # this poll's s over the square root of n
  }
  data.frame(poll = 1:polls, share = share, se = se)   # hand back one row per poll
}
