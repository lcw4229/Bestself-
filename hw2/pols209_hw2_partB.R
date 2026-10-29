# Homework 2, Part B. Landon Worrich.
setwd("~/Desktop/Texas A&M/POLS 209/week_08_hw2")
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

#block 1
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

#block 2d
poll_se <- sd(df_poll_401$zoning) / sqrt(401)
poll_se

poll_margin <- 1.96 * poll_se
poll_margin

poll_lower <- poll_share - poll_margin
poll_lower

poll_upper <- poll_share + poll_margin
poll_upper

#block 3
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

#block 4a
df_owners <- df_island[df_island$tenure=="own", ]
nrow(df_owners)

#block 4b
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

#block 4c
owner_share <- mean(df_owners$zoning)
owner_share

# Block 5A: a thousand random polls of 401 from the census list.
# 1,000 polls of 401, one row per poll: poll (1 to 1,000), share, and se.
# Restart R's random draws as in block 2B, so poll 1 is the station's poll.
set.seed(20261016)
df_polls_401 <- run_polls(df_island, "zoning", n = 401, polls = 1000)
head(df_polls_401, 3)                 # show the first three polls

#block 5b
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

#block 5d
set.seed(20261016)
df_gazette_10000 <- run_polls(df_owners, "zoning", n = 10000, polls = 1000)
head(df_gazette_10000, 1)

mean_gazette_10000 <- mean(df_gazette_10000$share)
mean_gazette_10000

#block 5e
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

#block 6a
set.seed(20261016)
df_polls_101 <- run_polls(df_island, "zoning", n = 101, polls = 1000)
set.seed(20261016)
df_polls_1001 <- run_polls(df_island, "zoning", n = 1001, polls = 1000)
set.seed(20261016)
df_polls_10001 <- run_polls(df_island, "zoning", n = 10001, polls = 1000)

#block 6b
sd_share_101 <- sd(df_polls_101$share)
sd_share_101

sd_share_1001 <- sd(df_polls_1001$share)
sd_share_1001

#block 6c
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

#block 7a
station_poll_contains <- abs(poll_share - island_share) <= poll_margin
station_poll_contains

#block 7b
df_polls_401$miss <- abs(df_polls_401$share - island_share)
df_polls_401$margin <- 1.96 * df_polls_401$se
contains_401 <- sum(df_polls_401$miss <= df_polls_401$margin)
contains_401

contains_1001 <- sum(abs(df_polls_1001$share - island_share) <= 1.96 * df_polls_1001$se)
contains_1001

#block 7c
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

#block 7d
contains_owners_401 <- sum(abs(df_gazette_401$share - owner_share) <= 1.96 * df_gazette_401$se)
contains_owners_401

#part b block 1
set.seed(20261016)
poll_rows_1001 <- sample(nrow(df_island), 1001)
df_poll_1001 <- df_island[poll_rows_1001, ]
nrow(df_poll_1001)

#part b block 2a
tenure_table <- table(df_poll_1001$zoning, df_poll_1001$tenure)
tenure_table

#part b block 2b
poll_renter_share <- mean(df_poll_1001$zoning[df_poll_1001$tenure=="rent"])
poll_renter_share

poll_owner_share <- mean(df_poll_1001$zoning[df_poll_1001$tenure=="own"])
poll_owner_share

poll_other_share <- mean(df_poll_1001$zoning[df_poll_1001$tenure=="other"])
poll_other_share

poll_gap <- poll_renter_share - poll_owner_share
poll_gap

#part b block 3a
n_missing_acts <- sum(is.na(df_poll_1001$political_acts))
n_missing_acts

table(df_poll_1001$tenure, is.na(df_poll_1001$political_acts))

df_poll_acts <- df_poll_1001[!is.na(df_poll_1001$political_acts), ]
nrow(df_poll_acts)

#part b block 3b
acts_renters <- df_poll_acts$political_acts[df_poll_acts$tenure=="rent"]
acts_owners <- df_poll_acts$political_acts[df_poll_acts$tenure=="own"]
n_acts_renters <- length(acts_renters)
n_acts_renters

n_acts_owners <- length(acts_owners)
n_acts_owners

acts_mean_renters <- mean(acts_renters)
acts_mean_renters

acts_mean_owners <- mean(acts_owners)
acts_mean_owners

acts_sd_renters <- sd(acts_renters)
acts_sd_renters

acts_sd_owners <- sd(acts_owners)
acts_sd_owners

acts_sd_all <- sd(df_poll_acts$political_acts)
acts_sd_all

acts_gap <- acts_mean_renters - acts_mean_owners
acts_gap

#part b block 3c
acts_se <- sqrt(acts_sd_renters^2 / n_acts_renters + acts_sd_owners^2 / n_acts_owners)
acts_se

#part b block 3d
acts_t <- acts_gap / acts_se
acts_t

acts_lower <- acts_gap - 1.96 * acts_se
acts_lower

acts_upper <- acts_gap + 1.96 * acts_se
acts_upper

#part b block 3e
acts_p_normal <- 2 * pnorm(-abs(acts_t))
acts_p_normal

# Block 3E: the same area under the t distribution.
acts_p_t <- 2 * pt(-abs(acts_t), df = 515.33)   # df for this test
acts_p_t

# Block 3F: the same test with t.test().
# Renters first, so R tests renters minus owners.
t.test(acts_renters, acts_owners)

#part b block 3g
df_island_acts <- df_island[!is.na(df_island$political_acts), ]
nrow(df_island_acts)

island_acts_renters <- mean(df_island_acts$political_acts[df_island_acts$tenure=="rent"])
island_acts_renters

island_acts_owners <- mean(df_island_acts$political_acts[df_island_acts$tenure=="own"])
island_acts_owners

island_acts_gap <- island_acts_renters - island_acts_owners
island_acts_gap

#part b block 4a
vote_renters <- df_poll_1001$zoning[df_poll_1001$tenure=="rent"]
vote_owners <- df_poll_1001$zoning[df_poll_1001$tenure=="own"]
t.test(vote_renters, vote_owners)

vote_renters_401 <- df_poll_401$zoning[df_poll_401$tenure=="rent"]
vote_owners_401 <- df_poll_401$zoning[df_poll_401$tenure=="own"]
t.test(vote_renters_401, vote_owners_401)

#part b block 4b
set.seed(20261029)
sept_rows <- sample(nrow(df_island), 101)
df_sept_101 <- df_island[sept_rows, ]
table(df_sept_101$zoning, df_sept_101$tenure)

sept_renters <- df_sept_101$zoning[df_sept_101$tenure=="rent"]
sept_owners <- df_sept_101$zoning[df_sept_101$tenure=="own"]
t.test(sept_renters, sept_owners)

#part b block 5a
df_districts <- read.csv("merrow_districts.csv")
nrow(df_districts)

# Block 5B: a scatterplot, one point per district.
# Renters across (x), the yes vote up (y).
plot_districts <- ggplot(df_districts, aes(x = renters_pct, y = yes_pct)) +
  # a dashed line at 50%: districts above it voted yes
  geom_hline(yintercept = 50, linetype = "dashed", color = "grey40") +
  # a label for the dashed line
  annotate("text", x = 84, y = 52, hjust = 1, color = "grey40",
           label = "Above this line: yes won") +
  # YOUR LINES: labs() with your title, a subtitle, and both axis labels
  labs(title = "Prop. 1 did better in districts where more adults rent",
       subtitle = "Each point is one of Merrow's 436 districts (Merrow Statistical Office)",
       x = "Adults who rent (%)",
       y = "Voted yes on Proposition 1 (%)") +
  # one point per district, half see-through so overlapping points show
  geom_point(color = "#6B2737", alpha = 0.5)
# YOUR LINES: show the plot, then save it as districts.png with ggsave()
plot_districts
ggsave("districts.png", plot = plot_districts,
       width = 7, height = 4.5, units = "in", dpi = 300, bg = "white")

# Block 5C: the correlation and its test.
# r for the 436 districts, stored and then printed:
district_r <- cor(df_districts$renters_pct, df_districts$yes_pct)
district_r
# r again, with its t and its two-sided p-value:
cor.test(df_districts$renters_pct, df_districts$yes_pct)

#part b block 6b
#party: progressive alliance vs old harbor party, outcome homes_tax_break
df_poll_choice <- df_poll_1001[!is.na(df_poll_1001$homes_tax_break) & !is.na(df_poll_1001$party), ]
choice_first <- df_poll_choice$homes_tax_break[df_poll_choice$party=="Progressive Alliance"]
choice_second <- df_poll_choice$homes_tax_break[df_poll_choice$party=="Old Harbor Party"]
length(choice_first)

length(choice_second)

t.test(choice_first, choice_second)

#part b block 6c
df_island_choice <- df_island[!is.na(df_island$homes_tax_break) & !is.na(df_island$party), ]
census_first <- mean(df_island_choice$homes_tax_break[df_island_choice$party=="Progressive Alliance"])
census_first

census_second <- mean(df_island_choice$homes_tax_break[df_island_choice$party=="Old Harbor Party"])
census_second

census_first - census_second
