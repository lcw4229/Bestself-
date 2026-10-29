# Homework 2, Part A. Landon Worrich.
# setwd("...")   <- replace this line with the setwd() line the Console printed
# Build this script as you work through HW2_Part_A_Lab.html: add each block to
# the end of this script, copied or written as the page says, then run it.
library(ggplot2)                             # makes the figures
source("hw2_tools.R")                        # loads run_polls()
df_island <- read.csv("merrow_census.csv")   # every adult on Merrow, one row each
# The look of every plot: fonts, title placement, and margins.
theme_set(theme_minimal(base_size = 12) +
  theme(plot.title = element_text(face = "bold", size = 14),
        plot.title.position = "plot",
        plot.caption = element_text(hjust = 0),
        plot.caption.position = "plot",
        panel.grid.minor = element_blank(),
        axis.title = element_text(size = 11),
        plot.margin = margin(12, 14, 10, 12)))

# Block 1: how the whole island voted
island_adults <- nrow(df_island)
island_adults
island_share <- mean(df_island$zoning)
island_share
island_sd <- sd(df_island$zoning)
island_sd

# Block 2B: choose 401 islanders at random.
set.seed(20261016)                          # start R's random draws at a fixed place
poll_rows <- sample(nrow(df_island), 401)   # 401 row numbers at random, none twice
head(poll_rows)                             # show the first six row numbers drawn

# Block 2C: keep those 401 rows: the station's poll.
df_poll_401 <- df_island[poll_rows, ]       # those rows, every column
nrow(df_poll_401)
poll_share <- mean(df_poll_401$zoning)
poll_share

# Block 2D: the station's margin of error
poll_se <- sd(df_poll_401$zoning) / sqrt(401)
poll_se
poll_margin <- 1.96 * poll_se
poll_margin
poll_lower <- poll_share - poll_margin
poll_lower
poll_upper <- poll_share + poll_margin
poll_upper

# Block 3: my own poll of 401
set.seed(4229)
my_rows <- sample(nrow(df_island), 401)
df_my_poll <- df_island[my_rows, ]
my_share <- mean(df_my_poll$zoning)
my_se <- sd(df_my_poll$zoning) / sqrt(401)
my_margin <- 1.96 * my_se
my_lower <- my_share - my_margin
my_upper <- my_share + my_margin
my_share
my_margin
my_lower
my_upper

# Block 4A: the property-tax roll
df_owners <- df_island[df_island$tenure == "own", ]
nrow(df_owners)

# Block 4B: the Gazette's poll
set.seed(20261016)
copy_rows <- sample(nrow(df_owners), 10000)
df_gazette_copy <- df_owners[copy_rows, ]
copy_share <- mean(df_gazette_copy$zoning)
copy_share
copy_se <- sd(df_gazette_copy$zoning) / sqrt(10000)
copy_se
copy_margin <- 1.96 * copy_se
copy_margin
copy_lower <- copy_share - copy_margin
copy_lower
copy_upper <- copy_share + copy_margin
copy_upper

# Block 4C: the homeowners' share
owner_share <- mean(df_owners$zoning)
owner_share

# Block 5A: a thousand random polls of 401 from the census list.
# 1,000 polls of 401, one row per poll: poll (1 to 1,000), share, and se.
# Restart R's random draws as in block 2B, so poll 1 is the station's poll.
set.seed(20261016)
df_polls_401 <- run_polls(df_island, "zoning", n = 401, polls = 1000)
head(df_polls_401, 3)                 # show the first three polls

# Block 5B: center and spread of the 1,000 shares
mean_share_401 <- mean(df_polls_401$share)
mean_share_401
sd_share_401 <- sd(df_polls_401$share)
sd_share_401

# Block 5C: picture the sampling distribution of the share in a poll of 401.
plot_401 <- ggplot(df_polls_401, aes(x = share)) +
  # bars one percentage point wide
  geom_histogram(binwidth = 0.01, fill = "#6B2737", color = "white") +
  # a gold reference line at the island's share
  geom_vline(xintercept = island_share, color = "#B8860B", linewidth = 1.2) +
  # a label for the gold line, at the top of the plot
  annotate("text", x = island_share, y = Inf, vjust = 1.5, hjust = -0.25,
           label = "All islanders: 0.502", color = "#B8860B") +
  # the same x-axis on every share picture
  coord_cartesian(xlim = c(0.35, 0.65)) +
  # the title and the axis labels
  labs(title = "Random polls of 401 islanders center on the island's share",
       subtitle = "1,000 polls, each a random sample of 401 adults on Merrow",
       x = "Share saying yes to Proposition 1",
       y = "Number of polls (out of 1,000)")
# Show the plot in the Plots pane, then save it as a file in your folder.
plot_401
ggsave("polls_401.png", plot = plot_401,
       width = 7, height = 4.5, units = "in", dpi = 300, bg = "white")

# Block 5D: 1,000 Gazette polls of 10,000
set.seed(20261016)
df_gazette_10000 <- run_polls(df_owners, "zoning", n = 10000, polls = 1000)
head(df_gazette_10000, 1)
mean_gazette_10000 <- mean(df_gazette_10000$share)
mean_gazette_10000

# Block 5E: picture the Gazette polls
plot_gazette_10000 <- ggplot(df_gazette_10000, aes(x = share)) +
  # bars one percentage point wide
  geom_histogram(binwidth = 0.01, fill = "#6B2737", color = "white") +
  # a gold reference line at the island's share
  geom_vline(xintercept = island_share, color = "#B8860B", linewidth = 1.2) +
  # a label for the gold line, at the top of the plot
  annotate("text", x = island_share, y = Inf, vjust = 1.5, hjust = -0.25,
           label = "All islanders: 0.502", color = "#B8860B") +
  # the same x-axis on every share picture
  coord_cartesian(xlim = c(0.35, 0.65)) +
  # the title and the axis labels
  labs(title = "Polls of 10,000 homeowners all land far below the island's share",
       subtitle = "1,000 polls, each a random sample of 10,000 adults on the property-tax roll",
       x = "Share saying yes to Proposition 1",
       y = "Number of polls (out of 1,000)")
# Show the plot in the Plots pane, then save it as a file in your folder.
plot_gazette_10000
ggsave("gazette_10000.png", plot = plot_gazette_10000,
       width = 7, height = 4.5, units = "in", dpi = 300, bg = "white")

# Block 6A: polls of 101, 1,001, and 10,001
set.seed(20261016)
df_polls_101 <- run_polls(df_island, "zoning", n = 101, polls = 1000)
set.seed(20261016)
df_polls_1001 <- run_polls(df_island, "zoning", n = 1001, polls = 1000)
set.seed(20261016)
df_polls_10001 <- run_polls(df_island, "zoning", n = 10001, polls = 1000)

# Block 6B: how much the shares scatter
sd_share_101 <- sd(df_polls_101$share)
sd_share_101
sd_share_1001 <- sd(df_polls_1001$share)
sd_share_1001

# Block 6C: how often yes is ahead
yes_ahead_401 <- sum(df_polls_401$share > 0.5)
yes_ahead_401
yes_ahead_101 <- sum(df_polls_101$share > 0.5)
yes_ahead_101
yes_ahead_1001 <- sum(df_polls_1001$share > 0.5)
yes_ahead_1001
yes_ahead_10001 <- sum(df_polls_10001$share > 0.5)
yes_ahead_10001

# Block 6C: the fraction of polls of 401 that should put "no" ahead.
# pnorm(): the area below 0.5 under a normal curve with this mean and sd.
below_50_401 <- pnorm(0.5, mean = island_share, sd = 0.5 / sqrt(401))
below_50_401   # print it
below_50_1001 <- pnorm(0.5, mean = island_share, sd = 0.5 / sqrt(1001))
below_50_1001

# Block 7A: does the station's interval contain the island's share
station_poll_contains <- abs(poll_share - island_share) <= poll_margin
station_poll_contains

# Block 7B: all 1,000 polls of 401, then 1,001
df_polls_401$miss <- abs(df_polls_401$share - island_share)
df_polls_401$margin <- 1.96 * df_polls_401$se
contains_401 <- sum(df_polls_401$miss <= df_polls_401$margin)
contains_401
contains_1001 <- sum(abs(df_polls_1001$share - island_share) <= 1.96 * df_polls_1001$se)
contains_1001

# Block 7C: the Gazette's intervals
set.seed(20261016)
df_gazette_401 <- run_polls(df_owners, "zoning", n = 401, polls = 1000)
set.seed(20261016)
df_gazette_1001 <- run_polls(df_owners, "zoning", n = 1001, polls = 1000)
mean_gazette_401 <- mean(df_gazette_401$share)
mean_gazette_401
mean_gazette_1001 <- mean(df_gazette_1001$share)
mean_gazette_1001
contains_gazette_401 <- sum(abs(df_gazette_401$share - island_share) <= 1.96 * df_gazette_401$se)
contains_gazette_401
contains_gazette_1001 <- sum(abs(df_gazette_1001$share - island_share) <= 1.96 * df_gazette_1001$se)
contains_gazette_1001
contains_gazette_10000 <- sum(abs(df_gazette_10000$share - island_share) <= 1.96 * df_gazette_10000$se)
contains_gazette_10000

# Block 7D: Gazette intervals vs. the homeowners' share
contains_owners_401 <- sum(abs(df_gazette_401$share - owner_share) <= 1.96 * df_gazette_401$se)
contains_owners_401
