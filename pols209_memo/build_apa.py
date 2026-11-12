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

# ---------- Body ----------
para("Abolishing Elected District Councils in Vietnam", "c", False, bold=True)
heading("1. Research Question")
P = lambda t: para(t)
P("My main question is whether communes in districts that had their elected council abolished had a different number of basic infrastructure services in 2010 than communes in districts that kept their council. In 2009 Vietnam ran a pilot that removed the elected District People's Councils in some districts, giving the central and provincial governments more direct control there. I want to know if that changed basic services in the communes inside those districts.")
runs([("X is ", ""), ("treated_district", "i"), (". It equals 1 if the commune is in a district where the council was abolished and 0 if the district kept its council. Y is ", ""), ("infrastructure_index", "i"), (", which counts how many of five basic infrastructure services a commune has (0 to 5). X is binary, so I am comparing communes in abolition districts (X = 1) to communes in districts that kept their council (X = 0).", "")])
P("I expect communes in districts that lost their council to have slightly fewer services, about 0.25 fewer per commune. Council members live in the district and know what the communes there need. When the district decides how to spend its budget, they can argue for a road repair or a new market for a specific village. Once the council is gone, officials who report to the province make those decisions instead, and I think they would put more weight on large or visible projects than on small rural communes. That should lead to slightly fewer services.")
P("I am not very confident about this prediction. Vietnam is a one-party state and the councils may not have had much real power, in which case removing them would not change much. Removing a layer of government could also make decisions happen faster. Malesky et al. (2014, Introduction section) describe this tradeoff, since elected councils are meant to hold officials accountable for services but can also become veto points captured by local elites. I picked a small number for that reason and would not be surprised by a difference near zero.")
P("I would consider anything under about 0.1 services small. That is less than a tenth of a service per commune and roughly a tenth of a standard deviation of Y. A difference of 0.5 services or more would be large, because it would be like half the communes losing a whole service. My prediction of 0.25 is between those two.")

heading("2. Data and Measures")
runs([("The data are from the commune module of the Vietnam Household Living Standards Survey (VHLSS), the same data Malesky et al. (2014) use in their ", ""), ("American Political Science Review", "i"), (" article. The project codebook says ", ""), ("analysis.csv", "i"), (" includes rural communes sampled in 58 provinces in two rounds, 2008 (2,081 communes) and 2010 (2,045 communes). The five Central Highlands provinces are excluded, as are records missing the household-density measure (POLS 209, 2026, “Choose the Right Dataset” section). The 2009 pilot abolished the elected District People's Councils in selected districts in 10 of the 58 provinces (Malesky et al., 2014, p. 144; POLS 209, 2026).", "")])
P("Each row is a commune in one survey year. There is no ID linking the same commune across 2008 and 2010, so the file is a repeated cross-section and not a panel. I treat each row as a separate observation and do not track communes over time.")
P("The file has 4,126 rows across both years. My question is only about 2010, so I kept the 2010 rows, which leaves 2,045. Neither X nor Y has missing values in 2010, so I did not drop anything, and the final sample is 2,045 communes.")
runs([("X (", ""), ("treated_district", "i"), ("): 1 if the commune's district had its elected council abolished in the 2009 pilot, 0 if the district kept its council. This is the policy change I am asking about.", "")])
runs([("Y (", ""), ("infrastructure_index", "i"), ("): the number of basic infrastructure services in the commune, from 0 to 5. The five services are a village road usable all year (", ""), ("year_round_road", "i"), ("), any village road (", ""), ("village_road", "i"), ("), public transport (", ""), ("public_transport", "i"), ("), tap water as the main water source (", ""), ("tap_water", "i"), ("), and a government socioeconomic-development and infrastructure project (", ""), ("socioeconomic_infrastructure_project", "i"), ("). Each one is coded 0/1 and Y is the sum. Neither variable was rescaled.", "")])
P("I also used three variables to describe the communes:")
bullet("households_in_commune", ": number of registered households in the commune. This is a measure of commune size.")
bullet("distance_to_nearest_town_km", ": distance to the nearest town in kilometers. This measures how remote a commune is, which probably affects how hard it is to build and maintain services.")
bullet("program_135_commune", ": 1 if the commune is in Program 135, the government program for especially poor and disadvantaged communes, 0 if not. I used this as my measure of disadvantage instead of poverty_rate because the codebook says 2010 poverty was measured after abolition and could be affected by the treatment.")
P("The average commune has about 2,129 households (median 1,966) and is about 11.7 km from the nearest town (median 8 km). About 19.5% are Program 135 communes and 13.3% are in districts that lost their council.")

heading("3. Descriptive Statistics and Distributions")

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

figure(1, "Number of Communes by District Council Status, 2010", "X_distribution.png",
       None)
runs([("Figure 1 shows that X is very uneven. Only 272 of the 2,045 communes (13.3%) are in districts where the council was abolished, compared to 1,773 in districts that kept it. With a treated group that small, its average will be less precise than the comparison group's.", "")])
figure(2, "Number of Basic Infrastructure Services per Commune, 2010", "Y_distribution.png",
       "Services counted: year-round village road, any village road, public transport, tap water as the main source, and a government infrastructure project.")
P("Figure 2 shows most communes near the middle and top of Y's range. About 68% have 3 or 4 of the 5 services and only about 6% have 0 or 1. The mean is 3.34, the median is 3, and the standard deviation is 1.09. According to Table 2 the middle half of communes (P25 to P75) has between 3 and 4 services. About 12% of communes already have all 5, so they cannot go any higher. If abolition improved services, those communes would not be able to show it.")

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
P("Households and distance to town are both right-skewed. The median commune has 1,966 households but the largest has 43,583, which pulls the mean up to 2,129. Distance has a median of 8 km, a 99th percentile of 60.6 km, and a maximum of 160 km. Because of these outliers the median is a better description of a typical commune than the mean.")
P("With an SD of 1.09 for Y, my predicted difference of 0.25 services is about 0.23 standard deviations. It is also about a quarter of the distance between P25 (3 services) and P75 (4 services). The actual raw difference is smaller and in the other direction. Abolition communes average 3.39 services and communes that kept their council average 3.33, a gap of +0.06 services or about 0.06 standard deviations. By the cutoff I set earlier, that is small.")
P("The 2010 comparison alone does not show my prediction is wrong. Pilot districts were not chosen randomly and could have been different from other districts before 2009. The article estimates the effect with a difference-in-differences design, comparing changes before and after the reform rather than one year (Malesky et al., 2014, p. 144). A quarter-service drop would still be visible since most communes have 3 or 4 services, but the ceiling at 5 limits how much a positive effect could appear. For now the data point to a small effect, which makes it less likely that the councils mattered much for local services. I will need the before-and-after comparison to test that properly.")

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
