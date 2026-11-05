# Homework 3. Your name here.
# setwd("...")   <- replace this line with the setwd() line the Console printed
# Build this script as you work through HW3_Lab.html: add each block to
# the end of this script, copied or written as the page says, then run it.
library(ggplot2)                               # makes the figures
source("hw3_tools.R")                          # loads binscatter(), used in block 7
df_texas <- read.csv("texas_districts.csv")    # 460 Texas school districts, one row each
# The look of every plot: fonts, title placement, and margins.
theme_set(theme_minimal(base_size = 12) +
  theme(plot.title = element_text(face = "bold", size = 14),
        plot.title.position = "plot",
        plot.caption = element_text(hjust = 0),
        plot.caption.position = "plot",
        panel.grid.minor = element_blank(),
        axis.title = element_text(size = 11),
        plot.margin = margin(12, 14, 10, 12)))

# Block 1: describe the districts
print(nrow(df_texas))                          # number of districts
spend_mean <- mean(df_texas$spend)             # mean spending per student (thousands of $)
spend_sd <- sd(df_texas$spend)                 # its standard deviation
print(spend_mean)
print(spend_sd)
sat_mean <- mean(df_texas$sat)                 # mean SAT average
sat_sd <- sd(df_texas$sat)                     # its standard deviation
print(sat_mean)
print(sat_sd)
print(quantile(df_texas$spend, probs = c(0, .25, .50, .75, 1)))
print(quantile(df_texas$sat, probs = c(0, .25, .50, .75, 1)))

# Block 2: draw Mr. Fenske's chart
plot_texas <- ggplot(df_texas, aes(x = spend, y = sat)) +
  labs(title = "Texas districts that spend more per student post lower SAT averages",
       subtitle = "Each point is one of 460 Texas school districts, 2023-24. Data: TEA.",
       x = "Operating spending per student (thousands of dollars)",
       y = "Average SAT score, class of 2024") +
  geom_point(color = "#6B2737", alpha = 0.5)   # one point per district
plot_texas

# Block 3A: the slope and the intercept, from the covariance and the variance
slope <- cov(df_texas$spend, df_texas$sat) / var(df_texas$spend)
intercept <- sat_mean - slope * spend_mean
print(slope)
print(intercept)

# Block 3B: the same line with lm().
line_fit <- lm(sat ~ spend, data = df_texas)   # least squares: sat on spend
coef(line_fit)                                 # the intercept and the slope

# Block 3C: Mr. Fenske's chart, with its line.
plot_line <- plot_texas +
  # the OLS line from your intercept and slope, in gold
  geom_abline(intercept = intercept, slope = slope, color = "#B8860B", linewidth = 1)
plot_line
ggsave("texas_line.png", plot = plot_line, width = 7, height = 4.5, units = "in",
       dpi = 300, bg = "white")

# Block 4A: every district's predicted value and residual
df_texas$pred <- intercept + slope * df_texas$spend   # predicted SAT average
df_texas$resid <- df_texas$sat - df_texas$pred        # actual minus predicted
print(head(df_texas, 3))

# Block 4B: my district, and the dot farthest to the right
print(df_texas[df_texas$district == "College Station ISD", ])
print(df_texas[df_texas$district == "Karnes City ISD", ])

# Block 5A: the slope's standard error, t-statistic, and p-value from R.
summary(line_fit)   # estimates, standard errors, t-statistics, and p-values

# Block 5B: the critical value for a 95% confidence interval (458 degrees of freedom).
crit <- qt(0.975, df = 458)   # 97.5% of the area under the t curve lies to its left
crit                          # show it
slope_lower <- slope - crit * 2.184
slope_upper <- slope + crit * 2.184
print(slope_lower)
print(slope_upper)

# Block 5C: R's 95% confidence interval for each estimate.
confint(line_fit)   # a 95% confidence interval for each estimate

# Block 6A: R-squared from the two sums of squared misses
ssr_line <- sum(df_texas$resid^2)                  # RSS
df_texas$flat_miss <- df_texas$sat - sat_mean      # misses from the flat line
ssr_flat <- sum(df_texas$flat_miss^2)              # TSS
r_squared <- 1 - ssr_line / ssr_flat
print(ssr_line)
print(ssr_flat)
print(r_squared)

# Block 6B: the root mean-squared error and R-squared from summary().
summary(line_fit)$sigma       # the root mean-squared error
summary(line_fit)$r.squared   # R-squared

# Block 7: a binscatter of SAT averages on spending, 20 groups of 23 districts.
binscatter(df_texas, "spend", "sat")   # prints the table, then draws the plot

# Block 8A: the districts farthest below and above the line
df_sorted <- df_texas[order(df_texas$resid),
                      c("district", "spend", "sat", "pred", "resid", "pct_disadv", "pct_sat")]
print(head(df_sorted, 8))
print(tail(df_sorted, 8))
print(median(df_texas$pct_disadv))
print(median(df_texas$pct_sat))

# Block 8B: spending and SAT averages against the low-income share and SAT participation
fit_spend_disadv <- lm(spend ~ pct_disadv, data = df_texas)
fit_sat_disadv <- lm(sat ~ pct_disadv, data = df_texas)
fit_spend_pctsat <- lm(spend ~ pct_sat, data = df_texas)
fit_sat_pctsat <- lm(sat ~ pct_sat, data = df_texas)
print(coef(fit_spend_disadv))
print(coef(fit_sat_disadv))
print(coef(fit_spend_pctsat))
print(coef(fit_sat_pctsat))
print(sd(df_texas$pct_disadv))
print(sd(df_texas$pct_sat))
