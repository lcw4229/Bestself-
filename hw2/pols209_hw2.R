# Homework 2, Part A. Your name here.
# setwd("...")   <- replace this line with the setwd() line the Console printed
# Build this script as you work through HW2_Part_A_Lab.html: add each block to
# the end of this script, copied or written as the page says, then run it.
library(ggplot2)                             # makes the figures
# source("hw2_tools.R")   # loads run_polls(); this script uses its own loops below
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

# Part A, block 5: 1,000 polls of each kind
draw_polls <- function(yes, n, reps = 1000) {
  replicate(reps, mean(yes[sample(length(yes), n)]))
}
set.seed(20261016)
polls_401 <- draw_polls(df_island$zoning, 401)
mean(polls_401)
sd(polls_401)                     # the standard error of a poll of 401
df_polls_401 <- data.frame(share = polls_401)
plot_polls_401 <- ggplot(df_polls_401, aes(x = share)) +
  geom_histogram(binwidth = 0.01, fill = "#6B2737", color = "white") +
  geom_vline(xintercept = island_share, linetype = "dashed") +
  labs(title = "1,000 random polls of 401 center on the island's 50.2% yes",
       subtitle = "Each bar counts polls whose yes share falls in a 1-point bin",
       x = "Yes share in the poll", y = "Number of polls")
plot_polls_401
ggsave("polls_401.png", plot = plot_polls_401, width = 7, height = 4.5,
       units = "in", dpi = 300, bg = "white")

gazette_401 <- draw_polls(df_owners$zoning, 401)
gazette_10000 <- draw_polls(df_owners$zoning, 10000)
mean(gazette_401)
mean(gazette_10000)
df_gazette_10000 <- data.frame(share = gazette_10000)
plot_gazette_10000 <- ggplot(df_gazette_10000, aes(x = share)) +
  geom_histogram(binwidth = 0.002, fill = "#6B2737", color = "white") +
  geom_vline(xintercept = island_share, linetype = "dashed") +
  labs(title = "Gazette polls of 10,000 homeowners all miss the island's 50.2%",
       subtitle = "1,000 polls drawn from the property-tax roll; dashed line: the island's share",
       x = "Yes share in the poll", y = "Number of polls")
plot_gazette_10000
ggsave("gazette_10000.png", plot = plot_gazette_10000, width = 7, height = 4.5,
       units = "in", dpi = 300, bg = "white")

# Part A, block 6: polls of 1,001
polls_1001 <- draw_polls(df_island$zoning, 1001)
sd(polls_1001)
sum(polls_1001 > 0.5)
se_1001 <- 0.5 / sqrt(1001)
below_50_1001 <- pnorm(0.5, mean = island_share, sd = se_1001)
below_50_1001

# Part A, block 7: how often does a 95% interval contain the island's share?
covers <- replicate(1000, {
  yes <- df_island$zoning[sample(nrow(df_island), 401)]
  se <- sd(yes) / sqrt(401)
  abs(mean(yes) - island_share) <= 1.96 * se
})
sum(covers)
