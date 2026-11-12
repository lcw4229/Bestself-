import sys
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

out = sys.argv[1]
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(sec, m, Inches(1))

st = doc.styles["Normal"]
st.font.name = "Times New Roman"; st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
pf = st.paragraph_format
pf.line_spacing = 2.0; pf.space_before = Pt(0); pf.space_after = Pt(0)

# page number, top right
hp = sec.header.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
def field(par, code):
    r = par.add_run()
    for t, extra in (("begin", None), (None, code), ("end", None)):
        if t:
            e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), t); r._r.append(e)
        else:
            e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = extra; r._r.append(e)
field(hp, "PAGE")

def para(text="", align=None, indent=True, bold=False, italic=False, keep=False):
    p = doc.add_paragraph()
    if align == "c": p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if indent: p.paragraph_format.first_line_indent = Inches(0.5)
    if keep: p.paragraph_format.keep_with_next = True
    if text:
        r = p.add_run(text); r.bold = bold; r.italic = italic
    return p

def runs(parts, indent=True):
    """parts: list of (text, style) where style in '', 'b', 'i'"""
    p = doc.add_paragraph()
    if indent: p.paragraph_format.first_line_indent = Inches(0.5)
    for t, s in parts:
        r = p.add_run(t); r.bold = "b" in s; r.italic = "i" in s
    return p

def heading(text):
    p = para(text, align="c", indent=False, bold=True, keep=True)

def bullet(name, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.75)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    p.add_run("•\t")
    p.paragraph_format.tab_stops.add_tab_stop(Inches(0.75))
    r = p.add_run(name); r.italic = True
    p.add_run(text)

def page_break():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# ---------- Title page ----------
for _ in range(3): para(indent=False)
para("Abolishing Elected District Councils in Vietnam:", "c", False, bold=True)
para("Research Question, Data, and Descriptive Statistics", "c", False, bold=True)
para(indent=False)
for line in ["Landon Worrich", "lworrich@tamu.edu",
             "Department of Political Science, Texas A&M University",
             "POLS 209",
             "Professor Jares", "November 12, 2026"]:
    para(line, None, False)
page_break()

def figure(n, title, img, note):
    # same as the original memo: just the R chart, centered, no APA label or note
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0; p.paragraph_format.space_after = Pt(6)
    p.add_run().add_picture(img, width=Inches(5.8))

def set_borders(cell, top=None, bottom=None):
    tcPr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for side, val in (("top", top), ("bottom", bottom)):
        if val:
            e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(val)); e.set(qn("w:color"), "000000"); b.append(e)
    tcPr.append(b)

def table(n, title, header, rows, widths, note):
    para(f"Table {n}", indent=False, bold=True, keep=True).paragraph_format.space_before = Pt(12)
    para(title, indent=False, italic=True, keep=True)
    t = doc.add_table(rows=len(rows) + 1, cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    tblPr = t._tbl.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w * 1440)))
    for i, row in enumerate([header] + rows):
        for j, val in enumerate(row):
            c = t.cell(i, j); c.width = Inches(widths[j])
            p = c.paragraphs[0]; p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val); r.font.size = Pt(10)
            if i == 0 and val in ("N", "M", "SD"): r.italic = True
            if i == 0: set_borders(c, top=8, bottom=4)
            elif i == len(rows): set_borders(c, bottom=8)
    runs([("Note. ", "i"), (note, "")], indent=False)


# ---------- Body ----------
para("Abolishing Elected District Councils in Vietnam", "c", False, bold=True)
P = lambda t: para(t)
heading("1. Research Question")
P("The Main Question for my project is: in 2010, did rural communes in districts whose elected council was abolished have a different number of basic infrastructure services than communes in districts that kept their council? In 2009, Vietnam ran a pilot that got rid of the elected District People's Councils in some districts. That put those districts more directly under the control of the provincial and central government. I want to know whether losing the council changed the basic services that communes in those districts ended up with.")
runs([("My X variable is ", ""), ("treated_district", "i"), (", which is 1 if a commune is in a district that lost its council and 0 if the district kept it. My Y variable is ", ""), ("infrastructure_index", "i"), (", which counts how many of five basic infrastructure services a commune has, so it goes from 0 to 5. Since X only has two values, my comparison is simple: the average number of services in abolition communes (X = 1) compared to communes that kept their council (X = 0).", "")])
P("I predict that communes in abolition districts will have slightly fewer services, about 0.25 fewer per commune, or a quarter of one service. My reasoning is that council members actually live in the district. When the district decides where its money goes, they are the ones who can speak up for a specific village that needs its road fixed or wants a market. Once the council is gone, those decisions are made by officials who answer to the province, not to the people in the commune. I think those officials would focus more on big projects that look good to their bosses and less on small rural communes, so the communes lose some of their voice.")
P("I am not very confident in this, though. Vietnam is a one-party state, so these councils may not have had much power to begin with, and taking them away might not change anything. It is also possible that removing a whole layer of government makes things get done faster. The authors of the study talk about this same tradeoff: elected councils are supposed to make officials answer for services, but they can also turn into veto points that local elites control (Malesky et al., 2014, Introduction section). That is why I picked a small number, and I would not be shocked if the real difference were close to zero.")
P("To decide what counts as small or large, I think of it in terms of whole services. A difference under 0.1 services would be small, since that is less than a tenth of one service per commune. A difference of 0.5 services or more would be large, because that is like half of all communes losing an entire service. My prediction of 0.25 sits in the middle, so I would call it a modest effect.")

heading("2. Data and Measures")
runs([("The data come from the commune part of the Vietnam Household Living Standards Survey (VHLSS), which is the same data Malesky et al. (2014) use in their ", ""), ("American Political Science Review", "i"), (" article. The project file, ", ""), ("analysis.csv", "i"), (", covers rural communes in 58 provinces of Vietnam in two survey years, 2008 and 2010. It leaves out the five Central Highlands provinces and any records that were missing the household-density measure (POLS 209, 2026). The councils were abolished in selected districts in 10 of these provinces (Malesky et al., 2014, p. 144).", "")])
P("Each row in the file is one commune in one survey year. The same commune is not linked across 2008 and 2010, so the data are a repeated cross-section, not a panel. Because of that, I treat every row as its own observation and do not try to follow communes over time.")
P("The file I imported has 4,126 rows: 2,081 from 2008 and 2,045 from 2010. My question is only about 2010, so I kept the 2010 rows, which left 2,045. I then checked for missing values in X and Y and there were none, so no more rows were dropped. My final sample is 2,045 communes.")
runs([("For X, ", ""), ("treated_district", "i"), (" is coded 1 if the commune's district had its elected council abolished in the 2009 pilot and 0 if the district kept its council. This is the policy change the question is about. For Y, ", ""), ("infrastructure_index", "i"), (" adds up five yes/no services: a village road that can be used all year (", ""), ("year_round_road", "i"), ("), any village road (", ""), ("village_road", "i"), ("), public transport (", ""), ("public_transport", "i"), ("), tap water as the main water source (", ""), ("tap_water", "i"), ("), and a government development and infrastructure project (", ""), ("socioeconomic_infrastructure_project", "i"), ("). Each one is 0 or 1, so one point on Y means one more service. I used both variables as they are and did not rescale them.", "")])
P("I also picked three variables to describe the communes in my sample:")
bullet("households_in_commune", " is the number of registered households in the commune. It tells me how big each commune is.")
bullet("distance_to_nearest_town_km", " is the distance to the nearest town in kilometers. It shows how remote a commune is, which probably makes services harder and more expensive to build.")
bullet("program_135_commune", " is 1 if the commune is in Program 135, the government's program for especially poor and disadvantaged communes, and 0 if not. I used this to measure disadvantage instead of the poverty rate, because the codebook warns that 2010 poverty was measured after the councils were abolished and could have been affected by it.")
P("The typical commune in my sample is fairly large and somewhat out of the way. The average commune has about 2,129 households (the median is 1,966) and is about 11.7 km from the nearest town (median 8 km). About 19.5% of communes are Program 135 communes, and 13.3% are in districts that lost their council.")

heading("3. Descriptive Statistics and Distributions")
figure(1, "", "X_distribution.png", None)
P("Figure 1 shows how uneven X is. Only 272 of the 2,045 communes (13.3%) are in districts that lost their council, while 1,773 are in districts that kept it. Because the abolition group is so small, its average is based on a lot fewer communes, so it will be less precise than the average for the other group.")
figure(2, "", "Y_distribution.png", None)
P("Figure 2 shows that most communes already have a good number of services. About 68% have either 3 or 4 of the 5, and only about 6% have 0 or 1. The mean is 3.34, the median is 3, and the standard deviation is 1.09. Table 2 shows that the middle half of communes (P25 to P75) has between 3 and 4 services. About 12% have all 5, which creates a ceiling. Those communes cannot go any higher, so if abolition actually helped services, they would not be able to show it.")
# Insert Tables 1 and 2 exactly as exported by lab_part_B.R (Project_Tables.docx)
import copy
from docx import Document as _D
rdoc = _D("Project_Tables.docx")
body = doc.element.body
sect = body[-1]  # keep sectPr last
for el in list(rdoc.element.body):
    if el.tag.endswith("sectPr"): continue
    new = copy.deepcopy(el)
    if new.tag.endswith("tbl"):
        rows = new.findall(qn("w:tr"))
        for tr in rows:
            trPr = tr.find(qn("w:trPr"))
            if trPr is None:
                trPr = OxmlElement("w:trPr"); tr.insert(0, trPr)
            trPr.append(OxmlElement("w:cantSplit"))
        for tr in rows[:-1]:
            for pp in tr.iter(qn("w:p")):
                pPr = pp.find(qn("w:pPr"))
                if pPr is None:
                    pPr = OxmlElement("w:pPr"); pp.insert(0, pPr)
                pPr.append(OxmlElement("w:keepNext"))
    elif new.tag.endswith("}p") and "Table" in "".join(new.itertext()):
        pPr = new.find(qn("w:pPr"))
        if pPr is None:
            pPr = OxmlElement("w:pPr"); new.insert(0, pPr)
        pPr.append(OxmlElement("w:keepNext"))
    body.insert(list(body).index(sect), new)
P("The other variables have some long tails. The median commune has 1,966 households, but the biggest has 43,583, which pulls the mean up to 2,129. Distance to town works the same way: the median is 8 km, but the 99th percentile is 60.6 km and the farthest commune is 160 km away. For both of these, the median gives a better idea of a normal commune than the mean does.")
P("Looking at my prediction next to these numbers, a drop of 0.25 services is about 0.23 standard deviations of Y (0.25 divided by 1.09). It is also about a quarter of the gap between the 25th percentile (3 services) and the 75th percentile (4 services). So it would be noticeable but not huge. When I compare the raw 2010 averages, the difference is even smaller than what I predicted and goes the other way. Abolition communes average 3.39 services and the others average 3.33, a gap of +0.06 services, or about 0.06 standard deviations. By my own cutoff, that is a small difference.")
P("This one-year comparison does not prove my prediction wrong. The pilot districts were not picked at random, so they could have been different from other districts even before 2009. The article handles this with a difference-in-differences design that compares how services changed from 2006 to 2010 in the two groups, instead of just looking at one year (Malesky et al., 2014, p. 144). Since most communes have 3 or 4 services, a quarter-service drop would still have room to show up, while the ceiling at 5 limits how much an improvement could show. For now, the numbers point toward a small effect, which makes me think the councils may not have mattered as much for local services as I first expected. I would need the before-and-after comparison to really test it.")

# ---------- References ----------
page_break()
para("References", "c", False, bold=True)
def ref(parts):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.5); p.paragraph_format.first_line_indent = Inches(-0.5)
    for t, s in parts:
        r = p.add_run(t); r.italic = "i" in s
ref([("Malesky, E. J., Nguyen, C. V., & Tran, A. (2014). The impact of recentralization on public services: A difference-in-differences analysis of the abolition of elected councils in Vietnam. ", ""), ("American Political Science Review, 108", "i"), ("(1), 144–168. https://doi.org/10.1017/S0003055413000580", "")])
ref([("POLS 209. (2026). ", ""), ("Codebook: Abolishing elected district councils in Vietnam", "i"), (" [Unpublished course material]. Department of Political Science, Texas A&M University.", "")])

doc.save(out)
print("ok")
