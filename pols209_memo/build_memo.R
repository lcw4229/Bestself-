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
 body_add_fpar(CTR("Landon Worrich  ·  lworrich@tamu.edu  ·  POLS 209, Fall 2026", TNR())) |>
 body_add_fpar(fpar(ftext(""), fp_p = fp_par(border.bottom = fp_border(color = "black", width = 0.75), padding.bottom = 6))) |>
 H("1. Research question") |>
 P("My project's Main Question is: in 2010, did communes in districts whose elected council was abolished have a different number of basic infrastructure services than communes in districts that kept their council? In 2009 Vietnam ran a pilot where it got rid of the elected District People's Councils in some districts. This let the central and provincial government run those districts more directly. The question is whether that change made a difference for basic services in the communes inside those districts.") |>
 P("X is treated_district, which equals 1 if the commune is in a district where the elected council was abolished and 0 if the district kept its council. Y is infrastructure_index, a count from 0 to 5 of how many basic infrastructure services the commune has. Since X is binary, the comparison is simple: communes in abolition districts (X = 1) versus communes in districts that kept their council (X = 0).") |>
 P("My prediction: I think communes in districts that lost their elected council will have slightly fewer basic infrastructure services than communes in districts that kept their council. My guess is about 0.25 fewer services, or about a quarter of one service per commune. The reason I expect this is that council members live in the district and know what the local communes need. They can speak up for a village that needs a road fixed or a new market when the district decides how to spend its money. Without the council, those decisions are made by officials who answer to the province instead of local people, and I think they will care more about the bigger or more visible projects than the needs of small rural communes. So I expect the communes to lose some of their voice, and that should show up as somewhat fewer services.") |>
 P("I am not very confident in this prediction. Vietnam is a one-party state, so the councils may not have had much real power in the first place, and getting rid of them might not change much. It is also possible that cutting out a layer of government makes things go faster. The article describes this same tradeoff: elected councils are supposed to make officials answer for services, but they can also become veto points captured by local elites (Malesky, Nguyen and Tran 2014, introduction). I picked a small number because of this, and I would honestly not be surprised if the difference turned out to be close to zero.") |>
 P("For this project, I would call a difference smaller than about 0.1 services (around one tenth of a standard deviation of Y) small, since it is less than a tenth of one service per commune. A difference of 0.5 services or more would be large, because it is like half of all communes losing a whole service. My prediction of 0.25 fewer services is in between, a modest but noticeable effect.") |>
 H("2. Data and measures") |>
 P("The data come from the commune module of the Vietnam Household Living Standards Survey (VHLSS), which Malesky, Nguyen and Tran (2014) use in their article in the American Political Science Review (108(1): 144-168). According to the project codebook, the file analysis.csv covers rural communes sampled in 58 provinces of Vietnam in two survey rounds: 2008 (2,081 communes) and 2010 (2,045 communes). It leaves out the five Central Highlands provinces and records missing the household-density measure (codebook, \"Choose the right dataset\"). The 2009 pilot abolished the elected District People's Councils in selected districts in 10 of these 58 provinces (codebook, treated_district; Malesky, Nguyen and Tran 2014, abstract, p. 144).") |>
 P("One row is one commune in one survey year (a commune-year). The file is a repeated cross-section, not a panel, because there is no ID that links the same commune across 2008 and 2010. So I treat each row as its own observation and do not claim to follow communes over time.") |>
 P("The file I imported has 4,126 rows covering both waves. The Main Question is only about 2010, so I kept the 2010 wave, which leaves 2,045 rows. Neither X nor Y has any missing values in 2010, so no rows were dropped for missing data. My final sample is 2,045 communes.") |>
 P("X (treated_district): 1 = the commune's district had its elected council abolished in the 2009 pilot, 0 = the district kept its council. This is the policy change the question asks about.") |>
 P("Y (infrastructure_index): number of basic infrastructure services in the commune, from 0 to 5. One point means one more service. The five services are a village road that can be used all year (year_round_road), any village road (village_road), public transport (public_transport), tap water as the main water source (tap_water), and a government socioeconomic-development and infrastructure project (socioeconomic_infrastructure_project). Each one is a 0/1 variable, and Y adds them up. This matches the \"basic infrastructure services\" in the question. I did not rescale either variable.") |>
 P("I also chose three variables to describe the communes:") |>
 B("households_in_commune", ": number of registered households in the commune (count). This tells me how big each commune is.") |>
 B("distance_to_nearest_town_km", ": distance from the commune to the nearest town, in kilometers. This measures how remote a commune is, which probably affects how easy it is to build and keep services.") |>
 B("program_135_commune", ": 1 = the commune is part of Program 135, the government's program for especially poor and disadvantaged communes, 0 = not. This measures economic disadvantage. I picked this instead of poverty_rate because the codebook says 2010 poverty was measured after abolition, so it could be affected by the treatment itself.") |>
 P("The typical commune in the sample is fairly large and somewhat rural. The average commune has about 2,129 households (median 1,966) and is about 11.7 km from the nearest town (median 8 km). About 19.5% of communes are Program 135 disadvantaged communes, and 13.3% are in districts that lost their council.") |>
 H("3. Descriptive statistics and distributions") |>
 IMG("X_distribution.png") |>
 P("Figure 1 shows that X is very uneven. Only 272 of the 2,045 communes (13.3%) are in districts where the council was abolished, and the other 1,773 are in districts that kept it. Because the treated group is small, its average will be estimated from fewer communes and will be noisier than the average for the comparison group.") |>
 IMG("Y_distribution.png") |>
 P("Figure 2 shows that Y is bunched in the middle and upper part of its range. Most communes have 3 or 4 of the 5 services (about 68% of communes), and only a few have 0 or 1. The mean is 3.34 and the median is 3, and the standard deviation is 1.09 services. Table 2 shows the middle half of communes (P25 to P75) falls between 3 and 4 services. There is also a ceiling: about 12% of communes already have all 5 services, so they cannot gain any more. This matters for my question, because if abolition helped services, the communes at 5 could not show it.") |>
 C("Table 1. ", "Summary statistics, retained sample (2,045 rural communes, 2010)") |>
 body_add_flextable(ft(t1, 2.9)) |>
N("Note: N counts recorded values. % observed = N / 2,045 x 100. For a 0/1 variable the mean is the share coded 1. Source: Malesky, Nguyen & Tran (2014).") |>
 C("Table 2. ", "Percentiles, retained sample (2,045 rural communes, 2010)") |>
 body_add_flextable(ft(t2, 2.4)) |>
 N("Note: P1 is the 1st percentile, P50 the median, and so on. Source: Malesky, Nguyen & Tran (2014).") |>
 P("The other variables have some features worth pointing out. Households has a long right tail. The median commune has 1,966 households, but the largest has 43,583, so the mean (2,129) is higher than the median. Distance to town also has a long tail: the median is 8 km, but the 99th percentile is 60.6 km and the maximum is 160 km. So a few very large or very remote communes pull the averages up, and the median is a better picture of a typical commune.") |>
 P("Putting my prediction in context: I predicted that communes in abolition districts would have about 0.25 fewer services. Since the SD of Y is 1.09, that is about 0.23 standard deviations, which is a modest effect. Another way to see it is that the middle half of communes goes from 3 services (P25) to 4 services (P75), so my prediction is about a quarter of that range. When I compare the raw averages, the difference is even smaller than I predicted and goes the other way: abolition communes average 3.39 services and communes that kept their council average 3.33, a gap of +0.06 services, or about 0.06 standard deviations. By my definition above, that is a small difference.") |>
 P("This simple 2010 comparison does not prove that my prediction is wrong. The districts in the pilot were not picked at random, so they could have been different from the others even before 2009. The article itself estimates the effect by comparing changes from before to after the reform (a difference-in-differences design) instead of looking at one year (Malesky, Nguyen and Tran 2014, abstract, p. 144). Since most communes already have 3 or 4 services, a drop of a quarter of a service would still be visible, but the ceiling at 5 means that if abolition actually helped, it would have limited room to show up. So far the numbers point toward a small effect, which makes my guess that councils mattered a lot for local services look less likely, but I will need the before-and-after comparison to really test it.")
print(doc, target="Memo_Vietnam_Councils.docx")
cat("ok\n")
