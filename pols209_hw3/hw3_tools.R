# hw3_tools.R: a function written for POLS 209 Homework 3.
# Your script loads it with source("hw3_tools.R"), near its top.
# binscatter() sorts the rows by x into groups of the same size, prints each
# group's averages, and draws them over the rows and the OLS line (block 7).

binscatter <- function(data, x, y, groups = 20) {
  # data: the data frame, one row per case
  # x, y: the names of the two columns, in quotes (for example "spend" and "sat")
  # groups: how many groups to make (20 unless you change it)
  n <- nrow(data)                                   # the number of rows
  place <- rank(data[[x]], ties.method = "first")   # 1 for the lowest x, n for the highest
  group <- ceiling(place * groups / n)              # group 1 holds the lowest x values, and so on
  fit <- lm(data[[y]] ~ data[[x]])                  # the OLS line, fit to every row
  a <- coef(fit)[1]                                 # its intercept
  b <- coef(fit)[2]                                 # its slope
  rows <- numeric(groups)     # a vector of zeros, one slot per group, for its number of rows
  x_low <- numeric(groups)    # the group's lowest x
  x_high <- numeric(groups)   # the group's highest x
  avg_x <- numeric(groups)    # the group's average x
  avg_y <- numeric(groups)    # the group's average y
  sd_y <- numeric(groups)     # the standard deviation of y within the group
  for (g in 1:groups) {       # repeat the lines inside the braces once for each group
    in_g <- group == g                  # TRUE for the rows in group g
    rows[g] <- sum(in_g)                # count them
    x_low[g] <- min(data[[x]][in_g])    # their lowest x
    x_high[g] <- max(data[[x]][in_g])   # their highest x
    avg_x[g] <- mean(data[[x]][in_g])   # their average x
    avg_y[g] <- mean(data[[y]][in_g])   # their average y
    sd_y[g] <- sd(data[[y]][in_g])      # the standard deviation of their y
  }
  line <- a + b * avg_x       # the line's height at each group's average x
  gap <- avg_y - line         # each group's average y minus the line's height there
  # the table: one row per group, with its numbers in columns
  table_out <- data.frame(group = 1:groups, rows, x_low, x_high, avg_x, avg_y, sd_y, line, gap)
  names(table_out)[3:7] <- c(paste0(x, "_low"), paste0(x, "_high"), paste0("avg_", x),
                             paste0("avg_", y), "sd_in_group")   # names for the table's columns
  print(round(table_out, 2), row.names = FALSE)   # show the table, rounded to two decimals
  plot_out <- ggplot(data, aes(x = .data[[x]], y = .data[[y]])) +               # x across, y up
    geom_point(color = "grey60", alpha = 0.4) +                                 # every row, faint
    geom_abline(intercept = a, slope = b, color = "#B8860B", linewidth = 1) +   # the OLS line, gold
    geom_point(data = data.frame(avg_x, avg_y), aes(x = avg_x, y = avg_y),
               color = "#6B2737", size = 3) +                                   # the group averages
    # the subtitle says what the dots and the line are
    labs(subtitle = paste0("Maroon dots: the averages of ", groups, " groups of ",
                           round(n / groups), ". Gold line: the OLS line, fit to all ", n, "."),
         x = x, y = y)   # axis labels: the two column names
  print(plot_out)             # draw it in the Plots pane
  invisible(plot_out)         # hand the plot back too, so you can store it and save it
}
