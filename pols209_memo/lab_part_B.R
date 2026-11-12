# POLS 209 | Project Memo 1: Abolishing Elected District Councils in Vietnam
# Name: Landon Worrich (lworrich@tamu.edu)
#
# Put this script in the same folder as the project_files folder, then click Session -> Set Working Directory ->
# To Source File Location before you run it.

# 1. Load the data and keep the rows the Main Question asks about --------
df_project <- read.csv("project_files/malesky_vietnam_recentralization/analysis.csv")
nrow(df_project)        # 4,126 rows imported (2008 and 2010 waves)
table(df_project$survey_year)   # 2008: 2,081   2010: 2,045

# The Main Question is about 2010, so keep only the 2010 wave
df_project <- df_project[df_project$survey_year == 2010, ]
nrow(df_project)        # 2,045 rows after keeping 2010

# Y (infrastructure_index) adds up five 0/1 services from the codebook.
# This checks that the five pieces really add up to Y (should print TRUE)
five_services <- c("year_round_road", "village_road", "public_transport",
                   "tap_water", "socioeconomic_infrastructure_project")
all(rowSums(df_project[, five_services]) == df_project$infrastructure_index)

# Check for missing X and Y
sum(is.na(df_project$treated_district))       # 0 missing X
sum(is.na(df_project$infrastructure_index))   # 0 missing Y

# Drop rows missing X or Y (none get dropped, but this keeps it safe)
df_project <- df_project[!is.na(df_project$treated_district) &
                         !is.na(df_project$infrastructure_index), ]
nrow(df_project)        # 2,045 rows retained

# 2. Packages ---------------------------------------
library(ggplot2)
library(flextable)
library(officer)

theme_set(theme_minimal(base_size = 12))

# 3. Figures: distributions of X and Y -----------------------------------
# X is 0/1, so I use a labeled bar chart
df_project$x_label <- factor(df_project$treated_district,
                             levels = c(0, 1),
                             labels = c("Kept council", "Council abolished"))

plot_x <- ggplot(df_project, aes(x = x_label)) +
  geom_bar(fill = "#500000", width = 0.6) +
  geom_text(stat = "count", aes(label = after_stat(count)), vjust = -0.4) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.08))) +
  labs(title = "Most communes are in districts that kept their council",
       subtitle = "Rural communes in Vietnam, 2010 survey wave",
       x = "District council status in 2010",
       y = "Number of communes",
       caption = "N = 2,045 communes. Source: Malesky, Nguyen & Tran (2014).")
plot_x

# Y is a count from 0 to 5 (only 6 values), so a bar chart works better
# than a histogram
df_project$y_label <- factor(df_project$infrastructure_index, levels = 0:5)

plot_y <- ggplot(df_project, aes(x = y_label)) +
  geom_bar(fill = "#500000", width = 0.6) +
  geom_text(stat = "count", aes(label = after_stat(count)), vjust = -0.4) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.08))) +
  labs(title = "Most communes have 3 or 4 of the 5 basic services",
       subtitle = "Rural communes in Vietnam, 2010 survey wave",
       x = "Basic infrastructure services in the commune (count, 0-5)",
       y = "Number of communes",
       caption = "N = 2,045 communes. Source: Malesky, Nguyen & Tran (2014).")
plot_y

ggsave("X_distribution.png", plot = plot_x, width = 7, height = 4.5,
       units = "in", dpi = 300, bg = "white")
ggsave("Y_distribution.png", plot = plot_y, width = 7, height = 4.5,
       units = "in", dpi = 300, bg = "white")

# 4. Put my prediction next to the spread of Y ---------------------------
mean(df_project$infrastructure_index)          # about 3.34
median(df_project$infrastructure_index)        # 3
y_sd <- sd(df_project$infrastructure_index)
y_sd                                           # about 1.09

# Share of communes at each value of Y
round(100 * prop.table(table(df_project$infrastructure_index)), 1)

# Group averages (X is binary, so just compare the two groups)
mean_abolished <- mean(df_project$infrastructure_index[df_project$treated_district == 1])
mean_kept      <- mean(df_project$infrastructure_index[df_project$treated_district == 0])
mean_abolished                                 # about 3.39
mean_kept                                      # about 3.33
mean_abolished - mean_kept                     # about +0.06

# My predicted difference: abolition communes have 0.25 FEWER services
predicted_change <- -0.25
abs(predicted_change) / y_sd                   # about 0.23 SD of Y
abs(mean_abolished - mean_kept) / y_sd         # raw gap is about 0.06 SD

# 5. Tables 1 and 2 ------------------------------------------------------
# I make the tables with basic R code instead of the course helper.
# Each table uses the retained sample (2,045 communes).

table_vars <- c("treated_district", "infrastructure_index",
                "households_in_commune", "distance_to_nearest_town_km",
                "program_135_commune")
table_labels <- c("In council-abolition district (X; 1 = yes, 0 = no)",
                  "Basic infrastructure services (Y; count, 0-5)",
                  "Households in commune (count)",
                  "Distance to nearest town (km)",
                  "Program 135 disadvantaged commune (1 = yes, 0 = no)")

# Table 1: N, mean, SD, percent observed
table1 <- data.frame(
  Variable     = table_labels,
  N            = sapply(table_vars, function(v) sum(!is.na(df_project[[v]]))),
  Mean         = sapply(table_vars, function(v) mean(df_project[[v]], na.rm = TRUE)),
  SD           = sapply(table_vars, function(v) sd(df_project[[v]], na.rm = TRUE)),
  Pct_observed = sapply(table_vars, function(v) 100 * mean(!is.na(df_project[[v]])))
)
table1

# Table 2: percentiles
pcts <- c(0, .01, .10, .25, .50, .75, .90, .99, 1)
table2 <- t(sapply(table_vars, function(v)
  quantile(df_project[[v]], probs = pcts, na.rm = TRUE)))
colnames(table2) <- c("Min", "P1", "P10", "P25", "P50", "P75", "P90", "P99", "Max")
table2 <- data.frame(Variable = table_labels, table2, check.names = FALSE)
table2

# 6. Save the tables as a Word file --------------------------------------
t1_print <- table1
t1_print$N <- format(t1_print$N, big.mark = ",")
t1_print$Mean <- formatC(t1_print$Mean, format = "f", digits = 3, big.mark = ",")
t1_print$SD <- formatC(t1_print$SD, format = "f", digits = 3, big.mark = ",")
t1_print$Pct_observed <- paste0(round(t1_print$Pct_observed), "%")
names(t1_print) <- c("Variable", "N", "Mean", "SD", "% observed")

t2_print <- table2
for (col in names(t2_print)[-1]) {
  t2_print[[col]] <- format(round(t2_print[[col]], 2), big.mark = ",",
                            drop0trailing = TRUE, trim = TRUE)
}

ft1 <- autofit(theme_booktabs(flextable(t1_print)))
ft2 <- autofit(theme_booktabs(flextable(t2_print)))

tables_doc <- read_docx()
tables_doc <- body_add_par(tables_doc, "Table 1. Summary statistics (2,045 communes, 2010)")
tables_doc <- body_add_flextable(tables_doc, ft1)
tables_doc <- body_add_par(tables_doc, "")
tables_doc <- body_add_par(tables_doc, "Table 2. Percentiles (2,045 communes, 2010)")
tables_doc <- body_add_flextable(tables_doc, ft2)
tables_doc <- body_add_par(tables_doc, "Source: Malesky, Nguyen & Tran (2014), APSR 108(1): 144-168.")
print(tables_doc, target = "Project_Tables.docx")

list.files()
