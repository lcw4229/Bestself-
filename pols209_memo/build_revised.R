suppressMessages({library(ggplot2); library(flextable); library(officer)})
theme_set(theme_minimal(base_size = 12))
# Figures rebuilt from walkthrough counts (X exact; Y counts read off the walkthrough chart,
# matched to mean 3.335 / SD 1.085). Replace with the PNGs from lab_part_B.R.
dx <- data.frame(g = factor(c("Kept council","Council abolished"), levels=c("Kept council","Council abolished")), n = c(1773, 272))
px <- ggplot(dx, aes(g, n)) + geom_col(fill="#500000", width=.6) +
  geom_text(aes(label=format(n, big.mark=",")), vjust=-.4) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.08))) +
  labs(title = "Figure 1. Most communes kept their district council",
       subtitle="Rural communes in Vietnam, 2010 survey wave",
       x="District council status in 2010", y="Number of communes",
       caption="N = 2,045 communes. Source: Malesky, Nguyen & Tran (2014).")
dy <- data.frame(v = factor(0:5), n = c(21,106,284,637,750,247))
py <- ggplot(dy, aes(v, n)) + geom_col(fill="#500000", width=.6) +
  geom_text(aes(label=n), vjust=-.4) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.08))) +
  labs(title = "Figure 2. Most communes have 3 or 4 of 5 basic services",
       subtitle="Rural communes in Vietnam, 2010 survey wave",
       x="Basic infrastructure services in the commune (count, 0-5)", y="Number of communes",
       caption="N = 2,045 communes. Source: Malesky, Nguyen & Tran (2014).")



lab <- c("In council-abolition district (X; 1 = yes)","Basic infrastructure services (Y; count, 0-5)",
         "Households in commune (count)","Distance to nearest town (km)","Program 135 commune (1 = yes)")
t1 <- data.frame(Variable=lab, N=rep("2,045",5), Mean=c("0.133","3.335","2,128.8","11.67","0.195"),
                 SD=c("0.340","1.085","1,457.6","12.86","0.396"), `% observed`=rep("100%",5), check.names=FALSE)
t2 <- data.frame(Variable=lab, Min=c("0","0","155","0","0"), P1=c("0","0","336","0","0"),
  P10=c("0","2","755","0.64","0"), P25=c("0","3","1,295","4","0"), P50=c("0","3","1,966","8","0"),
  P75=c("0","4","2,743","15","0"), P90=c("1","5","3,539","25","1"), P99=c("1","5","5,362","60.6","1"),
  Max=c("1","5","43,583","160","1"))
ft <- function(d, w1) { f <- flextable(d); f <- theme_booktabs(f); f <- fontsize(f, size=10, part="all")
  f <- font(f, fontname="Times New Roman", part="all"); f <- bold(f, part="header")
  f <- align(f, j=2:ncol(d), align="right", part="all"); f <- width(f, j=1, width=w1)
  f <- width(f, j=2:ncol(d), width=(6.5-w1)/(ncol(d)-1)); f <- padding(f, padding=3, part="all"); f <- align(f, align="center", part="all"); f <- align(f, j=1, align="left", part="all"); set_table_properties(f, layout="fixed", align="center") }

doc <- read_docx()
doc <- body_set_default_section(doc, prop_section(page_size = page_size(width = 8.5, height = 11),
  page_mar = page_mar(top = 1, bottom = 1, left = 1, right = 1, header = 0.5, footer = 0.5, gutter = 0)))
TNR <- function(...) fp_text(font.family = "Times New Roman", font.size = 12, ...)
body_par <- fp_par(text.align = "left", line_spacing = 1.15, padding.bottom = 8)
P <- function(doc, txt) body_add_fpar(doc, fpar(ftext(txt, TNR()), fp_p = body_par))
B <- function(doc, name, txt) body_add_fpar(doc, fpar(ftext("•  ", TNR()), ftext(name, TNR(bold = TRUE)), ftext(txt, TNR()),
  fp_p = fp_par(line_spacing = 1.15, padding.bottom = 4, padding.left = 18)))
H <- function(doc, txt) body_add_fpar(doc, fpar(ftext(txt, fp_text(font.family = "Times New Roman", font.size = 14, bold = TRUE)),
  fp_p = fp_par(padding.top = 14, padding.bottom = 6, keep_with_next = TRUE)))
C <- function(doc, label, txt) body_add_fpar(doc, fpar(ftext(label, TNR(bold = TRUE)), ftext(txt, TNR(italic = TRUE)),
  fp_p = fp_par(padding.top = 10, padding.bottom = 4, keep_with_next = TRUE)))
N <- function(doc, txt) body_add_fpar(doc, fpar(ftext(txt, fp_text(font.family = "Times New Roman", font.size = 10, italic = TRUE)),
  fp_p = fp_par(padding.top = 3, padding.bottom = 10)))
IMG <- function(doc, f) body_add_img(doc, f, width = 5.8, height = 3.73, style = "centered")
CTR <- function(txt, prop) fpar(ftext(txt, prop), fp_p = fp_par(text.align = "center", padding.bottom = 2))
doc <- doc |>
 body_add_fpar(CTR("Abolishing Elected District Councils in Vietnam", fp_text(font.family="Times New Roman", font.size=16, bold=TRUE))) |>
 body_add_fpar(CTR("Project Memo: Research Question, Data, and Descriptive Statistics", TNR(italic=TRUE))) |>
 body_add_fpar(CTR("Landon Worrich, lworrich@tamu.edu", TNR())) |>
 body_add_fpar(CTR("POLS 209, Fall 2026", TNR())) |>
 body_add_fpar(fpar(ftext(""), fp_p = fp_par(border.bottom = fp_border(color = "black", width = 0.75), padding.bottom = 6))) |>
 H("1. Research question") |>
 P("My main question is whether communes in districts that had their elected council abolished had a different number of basic infrastructure services in 2010 than communes in districts that kept their council. In 2009 Vietnam ran a pilot that removed the elected District People's Councils in some districts, giving the central and provincial governments more direct control there. I want to know if that changed basic services in the communes inside those districts.") |>
 P("X is treated_district. It equals 1 if the commune is in a district where the council was abolished and 0 if the district kept its council. Y is infrastructure_index, which counts how many of five basic infrastructure services a commune has (0 to 5). X is binary, so I am comparing communes in abolition districts (X = 1) to communes in districts that kept their council (X = 0).") |>
 P("I expect communes in districts that lost their council to have slightly fewer services, about 0.25 fewer per commune. Council members live in the district and know what the communes there need. When the district decides how to spend its budget, they can argue for a road repair or a new market for a specific village. Once the council is gone, officials who report to the province make those decisions instead, and I think they would put more weight on large or visible projects than on small rural communes. That should lead to slightly fewer services.") |>
 P("I am not very confident about this prediction. Vietnam is a one-party state and the councils may not have had much real power, in which case removing them would not change much. Removing a layer of government could also make decisions happen faster. Malesky, Nguyen and Tran (2014, introduction) describe this tradeoff, since elected councils are meant to hold officials accountable for services but can also become veto points captured by local elites. I picked a small number for that reason and would not be surprised by a difference near zero.") |>
 P("I would consider anything under about 0.1 services small. That is less than a tenth of a service per commune and roughly a tenth of a standard deviation of Y. A difference of 0.5 services or more would be large, because it would be like half the communes losing a whole service. My prediction of 0.25 is between those two.") |>
 H("2. Data and measures") |>
 P("The data are from the commune module of the Vietnam Household Living Standards Survey (VHLSS), the same data Malesky, Nguyen and Tran (2014) use in their American Political Science Review article (108(1): 144-168). The project codebook says analysis.csv includes rural communes sampled in 58 provinces in two rounds, 2008 (2,081 communes) and 2010 (2,045 communes). The five Central Highlands provinces are excluded, as are records missing the household-density measure (codebook, \"Choose the right dataset\"). The 2009 pilot abolished the elected District People's Councils in selected districts in 10 of the 58 provinces (codebook, treated_district; Malesky, Nguyen and Tran 2014, abstract, p. 144).") |>
 P("Each row is a commune in one survey year. There is no ID linking the same commune across 2008 and 2010, so the file is a repeated cross-section and not a panel. I treat each row as a separate observation and do not track communes over time.") |>
 P("The file has 4,126 rows across both years. My question is only about 2010, so I kept the 2010 rows, which leaves 2,045. Neither X nor Y has missing values in 2010, so I did not drop anything, and the final sample is 2,045 communes.") |>
 P("X (treated_district): 1 if the commune's district had its elected council abolished in the 2009 pilot, 0 if the district kept its council. This is the policy change I am asking about.") |>
 P("Y (infrastructure_index): the number of basic infrastructure services in the commune, from 0 to 5. The five services are a village road usable all year (year_round_road), any village road (village_road), public transport (public_transport), tap water as the main water source (tap_water), and a government socioeconomic-development and infrastructure project (socioeconomic_infrastructure_project). Each one is coded 0/1 and Y is the sum. Neither variable was rescaled.") |>
 P("I also used three variables to describe the communes:") |>
 B("households_in_commune", ": number of registered households in the commune. This is a measure of commune size.") |>
 B("distance_to_nearest_town_km", ": distance to the nearest town in kilometers. This measures how remote a commune is, which probably affects how hard it is to build and maintain services.") |>
 B("program_135_commune", ": 1 if the commune is in Program 135, the government program for especially poor and disadvantaged communes, 0 if not. I used this as my measure of disadvantage instead of poverty_rate because the codebook says 2010 poverty was measured after abolition and could be affected by the treatment.") |>
 P("The average commune has about 2,129 households (median 1,966) and is about 11.7 km from the nearest town (median 8 km). About 19.5% are Program 135 communes and 13.3% are in districts that lost their council.") |>
 H("3. Descriptive statistics and distributions") |>
 IMG("X_distribution.png") |>
 P("Figure 1 shows that X is very uneven. Only 272 of the 2,045 communes (13.3%) are in districts where the council was abolished, compared to 1,773 in districts that kept it. With a treated group that small, its average will be less precise than the comparison group's.") |>
 IMG("Y_distribution.png") |>
 P("Figure 2 shows most communes near the middle and top of Y's range. About 68% have 3 or 4 of the 5 services and only about 6% have 0 or 1. The mean is 3.34, the median is 3, and the standard deviation is 1.09. According to Table 2 the middle half of communes (P25 to P75) has between 3 and 4 services. About 12% of communes already have all 5, so they cannot go any higher. If abolition improved services, those communes would not be able to show it.") |>
 C("Table 1. ", "Summary statistics, retained sample (2,045 rural communes, 2010)") |>
 body_add_flextable(ft(t1, 2.9)) |>
 N("Note: N counts recorded values. % observed = N / 2,045 x 100. For a 0/1 variable the mean is the share coded 1. Source: Malesky, Nguyen & Tran (2014).") |>
 C("Table 2. ", "Percentiles, retained sample (2,045 rural communes, 2010)") |>
 body_add_flextable(ft(t2, 1.95)) |>
 N("Note: P1 is the 1st percentile, P50 the median, and so on. Source: Malesky, Nguyen & Tran (2014).") |>
 P("Households and distance to town are both right-skewed. The median commune has 1,966 households but the largest has 43,583, which pulls the mean up to 2,129. Distance has a median of 8 km, a 99th percentile of 60.6 km, and a maximum of 160 km. Because of these outliers the median is a better description of a typical commune than the mean.") |>
 P("With an SD of 1.09 for Y, my predicted difference of 0.25 services is about 0.23 standard deviations. It is also about a quarter of the distance between P25 (3 services) and P75 (4 services). The actual raw difference is smaller and in the other direction. Abolition communes average 3.39 services and communes that kept their council average 3.33, a gap of +0.06 services or about 0.06 standard deviations. By the cutoff I set earlier, that is small.") |>
 P("The 2010 comparison alone does not show my prediction is wrong. Pilot districts were not chosen randomly and could have been different from other districts before 2009. The article estimates the effect with a difference-in-differences design, comparing changes before and after the reform rather than one year (Malesky, Nguyen and Tran 2014, abstract, p. 144). A quarter-service drop would still be visible since most communes have 3 or 4 services, but the ceiling at 5 limits how much a positive effect could appear. For now the data point to a small effect, which makes it less likely that the councils mattered much for local services. I will need the before-and-after comparison to test that properly.")
print(doc, target="Memo_Vietnam_Councils_revised.docx")
cat("ok\n")
