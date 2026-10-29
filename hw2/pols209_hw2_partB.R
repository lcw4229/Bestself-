# Homework 2, Part B. Your name here.
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

# Part A, block 1: the census
island_share <- mean(df_island$zoning)
island_share

# Part A, block 2: the station's poll of 401
set.seed(20261016)
poll_rows_401 <- sample(nrow(df_island), 401)
df_poll_401 <- df_island[poll_rows_401, ]
poll_share <- mean(df_poll_401$zoning)
poll_share
poll_se <- sd(df_poll_401$zoning) / sqrt(401)
poll_lower <- poll_share - 1.96 * poll_se
poll_upper <- poll_share + 1.96 * poll_se
poll_se
poll_lower
poll_upper

# Part A, block 3: my own poll of 401
set.seed(4229)
my_rows <- sample(nrow(df_island), 401)
my_share <- mean(df_island$zoning[my_rows])
my_se <- sd(df_island$zoning[my_rows]) / sqrt(401)
my_lower <- my_share - 1.96 * my_se
my_upper <- my_share + 1.96 * my_se
my_share
my_lower
my_upper

# Part A, block 4: the Gazette's list, the property-tax roll
df_owners <- df_island[df_island$tenure == "own", ]
nrow(df_owners)
owner_share <- mean(df_owners$zoning)
owner_share

# Part A, block 5: 1,000 polls of 401 from the census list
set.seed(20261016)
polls_401 <- run_polls(df_island, "zoning", 401, 1000)
mean(polls_401$share)
sd(polls_401$share)               # the standard error of a poll of 401
plot_polls_401 <- ggplot(polls_401, aes(x = share)) +
  geom_histogram(binwidth = 0.01, fill = "#6B2737", color = "white") +
  geom_vline(xintercept = island_share, linetype = "dashed") +
  labs(title = "1,000 random polls of 401 center on the island's 50.2% yes",
       subtitle = "Each bar counts polls whose yes share falls in a 1-point bin",
       x = "Yes share in the poll", y = "Number of polls")
plot_polls_401
ggsave("polls_401.png", plot = plot_polls_401, width = 7, height = 4.5,
       units = "in", dpi = 300, bg = "white")

# Part A, block 5D: 1,000 Gazette polls from the property-tax roll
set.seed(20261016)
gazette_401 <- run_polls(df_owners, "zoning", 401, 1000)
set.seed(20261016)
gazette_1001 <- run_polls(df_owners, "zoning", 1001, 1000)
set.seed(20261016)
gazette_10000 <- run_polls(df_owners, "zoning", 10000, 1000)
mean(gazette_401$share)
mean(gazette_1001$share)
mean(gazette_10000$share)

# Part A, block 5E: the Gazette's polls of 10,000
plot_gazette_10000 <- ggplot(gazette_10000, aes(x = share)) +
  geom_histogram(binwidth = 0.002, fill = "#6B2737", color = "white") +
  geom_vline(xintercept = island_share, linetype = "dashed") +
  labs(title = "Gazette polls of 10,000 homeowners all miss the island's 50.2%",
       subtitle = "1,000 polls drawn from the property-tax roll; dashed line: the island's share",
       x = "Yes share in the poll", y = "Number of polls")
plot_gazette_10000
ggsave("gazette_10000.png", plot = plot_gazette_10000, width = 7, height = 4.5,
       units = "in", dpi = 300, bg = "white")

# Part A, block 6: polls of 1,001
set.seed(20261016)
polls_1001 <- run_polls(df_island, "zoning", 1001, 1000)
sd(polls_1001$share)
sum(polls_1001$share > 0.5)
se_1001 <- sd(polls_1001$share)
below_50_1001 <- pnorm(0.5, mean = island_share, sd = se_1001)
below_50_1001

# Part A, block 7: how often does a 95% interval contain the island's share?
polls_401$lower <- polls_401$share - 1.96 * polls_401$se
polls_401$upper <- polls_401$share + 1.96 * polls_401$se
sum(polls_401$lower <= island_share & polls_401$upper >= island_share)

# Part A, block 7C: Gazette intervals, the homeowners' share and the island's
contains <- function(polls, value) {
  sum(polls$share - 1.96 * polls$se <= value & polls$share + 1.96 * polls$se >= value)
}
contains(gazette_401, owner_share)
contains(gazette_401, island_share)
contains(gazette_1001, island_share)
contains(gazette_10000, island_share)

# Part B, block 1: Radio Merrow's poll of 1,001
set.seed(20261016)
poll_rows_1001 <- sample(nrow(df_island), 1001)
df_poll_1001 <- df_island[poll_rows_1001, ]
nrow(df_poll_1001)

# Part B, block 2A: the vote by tenure, as a table
tenure_table <- table(df_poll_1001$zoning, df_poll_1001$tenure)
tenure_table

# Part B, block 2B: the yes share in each group, and the gap
poll_renter_share <- mean(df_poll_1001$zoning[df_poll_1001$tenure == "rent"])
poll_owner_share <- mean(df_poll_1001$zoning[df_poll_1001$tenure == "own"])
poll_other_share <- mean(df_poll_1001$zoning[df_poll_1001$tenure == "other"])
poll_gap <- poll_renter_share - poll_owner_share
poll_renter_share
poll_owner_share
poll_other_share
poll_gap

# Part B, block 3A: whose answers are missing
n_missing_acts <- sum(is.na(df_poll_1001$political_acts))
n_missing_acts
table(df_poll_1001$tenure, is.na(df_poll_1001$political_acts))
df_poll_acts <- df_poll_1001[!is.na(df_poll_1001$political_acts), ]
nrow(df_poll_acts)

# Part B, block 3B: each group's average and standard deviation, and the gap
acts_renters <- df_poll_acts$political_acts[df_poll_acts$tenure == "rent"]
acts_owners <- df_poll_acts$political_acts[df_poll_acts$tenure == "own"]
n_acts_renters <- length(acts_renters)
n_acts_owners <- length(acts_owners)
n_acts_renters
n_acts_owners
acts_mean_renters <- mean(acts_renters)
acts_mean_owners <- mean(acts_owners)
acts_sd_renters <- sd(acts_renters)
acts_sd_owners <- sd(acts_owners)
acts_sd_all <- sd(df_poll_acts$political_acts)
acts_mean_renters
acts_mean_owners
acts_sd_renters
acts_sd_owners
acts_sd_all
acts_gap <- acts_mean_renters - acts_mean_owners
acts_gap

# Part B, block 3C: the standard error of the gap, by hand
acts_se <- sqrt(acts_sd_renters^2 / n_acts_renters + acts_sd_owners^2 / n_acts_owners)
acts_se

# Part B, block 3D: t and the 95% interval
acts_t <- acts_gap / acts_se
acts_lower <- acts_gap - 1.96 * acts_se
acts_upper <- acts_gap + 1.96 * acts_se
acts_t
acts_lower
acts_upper

# Part B, block 3E: the p-value, by hand
acts_p_normal <- 2 * pnorm(-abs(acts_t))
acts_p_normal
# Block 3E: the same area under the t distribution.
acts_p_t <- 2 * pt(-abs(acts_t), df = 515.33)   # df for this test
acts_p_t

# Part B, block 3F: the same test with t.test().
# Renters first, so R tests renters minus owners.
t.test(acts_renters, acts_owners)

# Part B, block 3G: the census
df_island_acts <- df_island[!is.na(df_island$political_acts), ]
nrow(df_island_acts)
island_acts_renters <- mean(df_island_acts$political_acts[df_island_acts$tenure == "rent"])
island_acts_owners <- mean(df_island_acts$political_acts[df_island_acts$tenure == "own"])
island_acts_gap <- island_acts_renters - island_acts_owners
island_acts_renters
island_acts_owners
island_acts_gap

# Part B, block 4A: the station's two polls
vote_renters <- df_poll_1001$zoning[df_poll_1001$tenure == "rent"]
vote_owners <- df_poll_1001$zoning[df_poll_1001$tenure == "own"]
t.test(vote_renters, vote_owners)
vote_renters_401 <- df_poll_401$zoning[df_poll_401$tenure == "rent"]
vote_owners_401 <- df_poll_401$zoning[df_poll_401$tenure == "own"]
t.test(vote_renters_401, vote_owners_401)

# Part B, block 4B: the Gazette's September poll
set.seed(20261029)
sept_rows <- sample(nrow(df_island), 101)
df_sept_101 <- df_island[sept_rows, ]
table(df_sept_101$zoning, df_sept_101$tenure)
sept_renters <- df_sept_101$zoning[df_sept_101$tenure == "rent"]
sept_owners <- df_sept_101$zoning[df_sept_101$tenure == "own"]
t.test(sept_renters, sept_owners)

# Part B, block 5A: the district file
df_districts <- read.csv("merrow_districts.csv")
nrow(df_districts)

# Part B, block 5B: a scatterplot, one point per district.
# Renters across (x), the yes vote up (y).
plot_districts <- ggplot(df_districts, aes(x = renters_pct, y = yes_pct)) +
  # a dashed line at 50%: districts above it voted yes
  geom_hline(yintercept = 50, linetype = "dashed", color = "grey40") +
  # a label for the dashed line
  annotate("text", x = 84, y = 52, hjust = 1, color = "grey40",
           label = "Above this line: yes won") +
  labs(title = "Prop. 1 did better in districts where more adults rent",
       subtitle = "Each point is one of Merrow's 436 census districts. Source: Merrow Statistical Office",
       x = "Adults who rent (%)",
       y = "Voted yes on Proposition 1 (%)") +
  # one point per district, half see-through so overlapping points show
  geom_point(color = "#6B2737", alpha = 0.5)
plot_districts
ggsave("districts.png", plot = plot_districts, width = 7, height = 4.5,
       units = "in", dpi = 300, bg = "white")

# Part B, block 5C: the correlation and its test.
# r for the 436 districts, stored and then printed:
district_r <- cor(df_districts$renters_pct, df_districts$yes_pct)
district_r
# r again, with its t and its two-sided p-value:
cor.test(df_districts$renters_pct, df_districts$yes_pct)

# Part B, block 6B: my comparison, in the poll
# Progressive Alliance vs. Old Harbor Party on homes_tax_break
df_poll_choice <- df_poll_1001[!is.na(df_poll_1001$homes_tax_break) &
                                 !is.na(df_poll_1001$party), ]
choice_first <- df_poll_choice$homes_tax_break[df_poll_choice$party == "Progressive Alliance"]
choice_second <- df_poll_choice$homes_tax_break[df_poll_choice$party == "Old Harbor Party"]
length(choice_first)
length(choice_second)
t.test(choice_first, choice_second)

# Part B, block 6C: the census
df_island_choice <- df_island[!is.na(df_island$homes_tax_break) &
                                !is.na(df_island$party), ]
census_first <- mean(df_island_choice$homes_tax_break[df_island_choice$party == "Progressive Alliance"])
census_second <- mean(df_island_choice$homes_tax_break[df_island_choice$party == "Old Harbor Party"])
census_first
census_second
census_first - census_second
