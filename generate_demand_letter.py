#!/usr/bin/env python3
"""Generate demand letter PDF matching the Janicek Law Firm format exactly."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUTPUT = "/home/user/Bestself-/demand_letter_Lopez_v_Alvarez_Progressive.pdf"
LOGO  = "/tmp/logo/lor_logo.png"

# ── Page geometry ──────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter          # 612 x 792 pt
LEFT  = 1.0 * inch
RIGHT = 1.0 * inch
TOP   = 0.5 * inch
BOT   = 0.75 * inch

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN = colors.HexColor("#4a7c2f")

# ── Styles ─────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    """Create a named ParagraphStyle."""
    parent = kw.pop("parent", "Normal")
    return ParagraphStyle(name, parent=base[parent], **kw)

NORMAL = S("body",
           fontName="Times-Roman", fontSize=11, leading=15,
           spaceAfter=10, alignment=TA_JUSTIFY)

NORMAL_LEFT = S("body_left",
                fontName="Times-Roman", fontSize=11, leading=15,
                spaceAfter=10, alignment=TA_LEFT)

HDR_ADDR = S("hdr_addr",
             fontName="Times-Roman", fontSize=8.5, leading=11,
             alignment=TA_LEFT, textColor=colors.black)

HDR_CERT = S("hdr_cert",
             fontName="Times-Roman", fontSize=8.5, leading=11,
             alignment=TA_RIGHT, textColor=colors.black)

DATE_STYLE = S("date",
               fontName="Times-Roman", fontSize=11, leading=14,
               spaceAfter=14, alignment=TA_LEFT)

FAX_STYLE = S("fax",
              fontName="Times-BoldItalic", fontSize=11, leading=14,
              spaceAfter=0, alignment=TA_LEFT)

BOLD_STYLE = S("bold_line",
               fontName="Times-Bold", fontSize=11, leading=14,
               spaceAfter=0, alignment=TA_LEFT)

PLAIN_ADDR = S("plain_addr",
               fontName="Times-Roman", fontSize=11, leading=14,
               spaceAfter=0, alignment=TA_LEFT)

RE_LABEL = S("re_label",
             fontName="Times-Roman", fontSize=11, leading=15,
             alignment=TA_LEFT)

SALUTE = S("salute",
           fontName="Times-Roman", fontSize=11, leading=15,
           spaceBefore=12, spaceAfter=12, alignment=TA_LEFT)

CONF_HDR = S("conf_hdr",
             fontName="Times-Bold", fontSize=11, leading=14,
             spaceBefore=16, spaceAfter=14, alignment=TA_CENTER)

SECTION_HDR = S("sec_hdr",
                fontName="Times-Bold", fontSize=11, leading=14,
                spaceBefore=14, spaceAfter=6, alignment=TA_CENTER)

INDENT_BLOCK = S("indent",
                 fontName="Times-Roman", fontSize=10.5, leading=14,
                 leftIndent=36, rightIndent=36,
                 spaceBefore=8, spaceAfter=8,
                 alignment=TA_JUSTIFY)

NUMBERED = S("numbered",
             fontName="Times-Roman", fontSize=11, leading=15,
             leftIndent=18, firstLineIndent=-18,
             spaceBefore=6, spaceAfter=6, alignment=TA_JUSTIFY)

BILL_ITEM = S("bill_item",
              fontName="Times-Roman", fontSize=11, leading=15,
              leftIndent=54, spaceAfter=4, alignment=TA_LEFT)

BILL_TOTAL_LBL = S("bill_total_lbl",
                   fontName="Times-Bold", fontSize=11, leading=15,
                   leftIndent=54, spaceAfter=4, alignment=TA_LEFT)

SIGN_BLOCK = S("sign",
               fontName="Times-Roman", fontSize=11, leading=15,
               spaceAfter=4, alignment=TA_LEFT)

SIGN_ITALIC = S("sign_italic",
                fontName="Times-Italic", fontSize=11, leading=15,
                spaceAfter=4, alignment=TA_LEFT)

ENCLOSURE = S("encl",
              fontName="Times-Roman", fontSize=10.5, leading=14,
              leftIndent=54, spaceAfter=2, alignment=TA_LEFT)

# ── Helper: thin rule ──────────────────────────────────────────────────────────
def rule(width=None, thickness=0.75):
    return HRFlowable(width=width or "100%", thickness=thickness,
                      color=colors.black, spaceAfter=4, spaceBefore=4)

# ── Bill table helper ──────────────────────────────────────────────────────────
def bill_table():
    col_w = PAGE_W - LEFT - RIGHT - 54  # usable width after left indent
    data = [
        ["Christus Spohn Hospital Shoreline\n(Admission 06/20/2025 – 06/21/2025,\nAccount No. 6400000996012)",
         "$66,927.26"],
        ["", ""],
        ["Christus Spohn Hospital Shoreline\n(Admission 06/27/2025 – 07/01/2025,\nAccount No. 6400001013978)",
         "$335,567.56"],
    ]
    col_widths = [col_w * 0.72, col_w * 0.28]
    tbl = Table(data, colWidths=col_widths, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("FONTNAME",    (0, 0), (-1, -1), "Times-Roman"),
        ("FONTSIZE",    (0, 0), (-1, -1), 11),
        ("LEADING",     (0, 0), (-1, -1), 15),
        ("ALIGN",       (1, 0), (1, -1), "RIGHT"),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",  (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEBELOW",   (0, 2), (1, 2), 0.75, colors.black),
    ]))
    return tbl

def bill_total_table():
    col_w = PAGE_W - LEFT - RIGHT - 54
    data = [["TOTAL HOSPITAL BILLS:", "$402,494.82"]]
    col_widths = [col_w * 0.72, col_w * 0.28]
    tbl = Table(data, colWidths=col_widths, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("FONTNAME",    (0, 0), (0, 0), "Times-Bold"),
        ("FONTNAME",    (1, 0), (1, 0), "Times-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 11),
        ("LEADING",     (0, 0), (-1, -1), 15),
        ("ALIGN",       (1, 0), (1, 0), "RIGHT"),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",  (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return tbl

# ── Header builder (called on every page via a frame decorator) ─────────────────
def build_letterhead():
    """Return flowables that form the top-of-page letterhead."""
    items = []

    # Logo image — full usable width, proportional height
    usable_w = PAGE_W - LEFT - RIGHT
    logo_h = usable_w * (310 / 1339)
    items.append(Image(LOGO, width=usable_w, height=logo_h))
    items.append(Spacer(1, 4))

    # Two-column header text (address left | certifications right)
    addr_text = (
        "1100 NE Loop 410, Suite 600, San Antonio, Texas 78209"
        "      Telephone (210)366-4949      Fax (210)979-6804"
    )
    left_col = [
        Paragraph(addr_text, HDR_ADDR),
        Paragraph("Beth S. Janicek*", HDR_ADDR),
        Paragraph("Philip G. Bernal*", HDR_ADDR),
    ]
    right_col = [
        Paragraph("&nbsp;", HDR_CERT),
        Paragraph("*Board Certified-Personal Injury Trial Law", HDR_CERT),
        Paragraph("Texas Board of Legal Specialization", HDR_CERT),
    ]
    col_w = usable_w / 2
    hdr_tbl = Table(
        [[left_col, right_col]],
        colWidths=[col_w, col_w]
    )
    hdr_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
    ]))
    items.append(hdr_tbl)
    items.append(rule())
    items.append(Spacer(1, 10))
    return items


# ── Re: block ──────────────────────────────────────────────────────────────────
def re_block():
    """Tabular Re: block matching the original letter layout."""
    usable_w = PAGE_W - LEFT - RIGHT
    col1 = 0.45 * inch   # "Re:" label
    col2 = 1.10 * inch   # field label
    col3 = usable_w - col1 - col2  # value

    data = [
        [Paragraph("Re:", RE_LABEL),
         Paragraph("Your insured:", RE_LABEL),
         Paragraph("Keith Alvarez", RE_LABEL)],
        ["",
         Paragraph("Our Clients:", RE_LABEL),
         Paragraph(
             "Tavia Lemon and Samantha Romero, Individually and as "
             "Heirs and Wrongful Death Beneficiaries of Elda Marisol "
             "Lopez, Deceased",
             RE_LABEL)],
        ["",
         Paragraph("Claim No.:", RE_LABEL),
         Paragraph("25-503488295", RE_LABEL)],
        ["",
         Paragraph("Date of Loss:", RE_LABEL),
         Paragraph("June 20, 2025", RE_LABEL)],
    ]
    tbl = Table(data, colWidths=[col1, col2, col3])
    tbl.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return tbl


# ── Main document builder ──────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=LEFT, rightMargin=RIGHT,
        topMargin=TOP, bottomMargin=BOT,
        title="Demand Letter – Lopez v. Alvarez/Progressive",
        author="Janicek Law Firm, P.C.",
    )

    story = []

    # ── Letterhead ──
    story += build_letterhead()

    # ── Date ──
    story.append(Paragraph("June 3, 2026", DATE_STYLE))

    # ── Addressee block ──
    story.append(Paragraph("<i><b>Via Facsimile: (833) 958-1221</b></i>", FAX_STYLE))
    story.append(Paragraph("Progressive Casualty Insurance Company", PLAIN_ADDR))
    story.append(Paragraph("<b>ATTN: Dana Perkins</b>", BOLD_STYLE))
    story.append(Paragraph("P.O. Box 94639", PLAIN_ADDR))
    story.append(Paragraph("Cleveland, OH 44101-9908", PLAIN_ADDR))
    story.append(Spacer(1, 12))

    # ── CONFIDENTIAL header ──
    story.append(Paragraph(
        "<u>CONFIDENTIAL SETTLEMENT DEMAND PURSUANT TO TEX. R. EVID. 408</u>",
        CONF_HDR))

    # ── Re: block ──
    story.append(re_block())
    story.append(Spacer(1, 12))

    # ── Salutation ──
    story.append(Paragraph("Dear Ms. Perkins:", SALUTE))

    # ── Opening paragraph ──
    story.append(Paragraph(
        "I am writing this letter on behalf of Tavia Lemon and Samantha Romero, the daughters "
        "and surviving wrongful death beneficiaries of Elda Marisol Lopez, Deceased, for the "
        "catastrophic injuries and wrongful death she suffered as the result of a motor vehicle "
        "collision which occurred on June 20, 2025. We hereby send a demand for policy limits "
        "pursuant to the Stowers’ Doctrine, such offer remaining open until June 24, 2026.",
        NORMAL))

    # ── Facts of the collision ──
    story.append(Paragraph(
        "On June 20, 2025, Elda Marisol Lopez, a 53-year-old woman, was a passenger in a 2020 "
        "Gray Honda Civic driven by your insured, Keith N. Alvarez, traveling south on the 100 "
        "block of North Port Avenue in Corpus Christi, Nueces County, Texas. While proceeding "
        "through the intersection at Agnes Street, your insured’s vehicle was struck by a "
        "2020 White Toyota Tundra driven by Eusebia Abdelrahim, who was traveling north on the "
        "400 block of South Port Avenue and attempted to execute a left turn onto the 2800 block "
        "of Agnes Street directly in front of your insured’s oncoming vehicle. The violent "
        "collision resulted in severe damage to both vehicles and the catastrophic injury of Ms. "
        "Lopez. Officer Lenortavage, Badge No. 12204, of the Corpus Christi Police Department "
        "responded to the scene and completed a Texas Peace Officer’s Crash Report (Case "
        "No. C2503621). Please see the certified crash report attached hereto.",
        NORMAL))

    story.append(Paragraph(
        "Investigator’s Narrative Opinion of What Happened:",
        NORMAL_LEFT))

    story.append(Paragraph(
        "DRIVER OF UNIT 1 TRAVELING NORTH ON THE 400 BLOCK OF S PORT AVE STATED SHE "
        "HAD A GREEN ARROW AND WAS ATTEMPTING TO TURN LEFT ONTO THE 2800 BLOCK OF "
        "AGNES ST, AND WAS STRUCK BY UNIT 2. DRIVER OF UNIT 2 TRAVELING SOUTH ON THE "
        "100 BLOCK OF N PORT AVE STATED HE HAD A GREEN LIGHT AND STRUCK UNIT 1, AS IT "
        "TURNED LEFT IN FRONT OF HIM. DUE TO CONFLICTING STATEMENTS FROM BOTH PARTIES "
        "AND NO INDEPENDENT WITNESSES, AN AT FAULT DRIVER WAS UNABLE TO BE DETERMINED.",
        INDENT_BLOCK))

    story.append(Paragraph(
        "As a direct and proximate result of the collision, Elda Marisol Lopez suffered traumatic "
        "internal injuries, including a splenic laceration, whose delayed rupture triggered "
        "hemorrhagic shock, multi-organ failure, and ultimately her death. Despite emergency "
        "surgical intervention and intensive critical care at Christus Spohn Hospital Shoreline "
        "in Corpus Christi, Texas, Elda Marisol Lopez died on July 1, 2025, at 5:16 PM — "
        "eleven days after the collision.",
        NORMAL))

    # ── Medical Treatment section ──
    story.append(Paragraph("Medical Treatment", SECTION_HDR))

    story.append(Paragraph(
        "On June 20, 2025, emergency medical personnel transported Ms. Lopez from the scene of "
        "the collision to Christus Spohn Hospital Shoreline, where she was admitted and placed "
        "on cardiac telemetry. During this initial hospitalization, Ms. Lopez underwent CT "
        "imaging of the brain, cervical spine, and thoracic spine; echocardiogram; nuclear "
        "stress test; chest X-ray; chest ultrasound; and comprehensive laboratory studies. She "
        "was evaluated by emergency medicine, cardiology, nephrology, and internal medicine. "
        "Ms. Lopez was discharged on June 21, 2025, in stable condition, with the principal "
        "diagnosis of NSTEMI (non-ST-elevated myocardial infarction) attributable to the "
        "traumatic stress of the collision.",
        NORMAL))

    story.append(Paragraph(
        "Although Ms. Lopez was discharged, her internal injuries from the collision were far "
        "from resolved. On June 27, 2025, Ms. Lopez presented to the Christus Spohn Beeville "
        "Emergency Department in acute distress, complaining of severe epigastric and left upper "
        "quadrant abdominal pain, nausea, and hemodynamic instability. Her blood pressure on "
        "arrival was 79/49. Laboratory results revealed a critical hemoglobin of 5.5 g/dL, "
        "consistent with severe hemorrhagic anemia. She was emergently transferred via HALO "
        "transport to the Christus Spohn Shoreline ICU for further critical care.",
        NORMAL))

    story.append(Paragraph(
        "Upon arrival at the ICU, Ms. Lopez was administered two units of packed red blood cells "
        "and placed on vasopressor support. Her condition rapidly deteriorated — she became "
        "acutely obtunded and hypertensive, and a code stroke was called. She was emergently "
        "intubated for airway protection. CT imaging of the abdomen was ordered and her abdomen "
        "was noted to be significantly more distended throughout the day. Surgery was urgently "
        "consulted.",
        NORMAL))

    story.append(Paragraph(
        "On June 28, 2025, Ms. Lopez underwent an emergency exploratory laparotomy performed by "
        "Dr. Pearce. Surgical findings were devastating: a large laceration of the spleen with "
        "approximately 4 liters of blood already pooled in her abdominal cavity. Dr. Pearce "
        "performed an emergency splenectomy and evacuation of the hemoperitoneum. As directly "
        "documented in the operative and medical records:",
        NORMAL))

    story.append(Paragraph(
        "“Postoperative findings were consistent with hemorrhagic shock secondary to a "
        "ruptured spleen. It was later reported that the patient had been involved in a motor "
        "vehicle accident several days prior to admission.”",
        INDENT_BLOCK))

    story.append(Paragraph(
        "The estimated blood loss from the surgery alone was at least 4 liters. Following the "
        "splenectomy, Ms. Lopez’s condition remained critical. She developed severe "
        "metabolic acidosis requiring sodium bicarbonate therapy, and was initiated on continuous "
        "renal replacement therapy (CRRT) via TABLO for acute kidney failure superimposed on her "
        "pre-existing end-stage renal disease. She required maximum-dose vasopressor support with "
        "norepinephrine (levophed) at quadruple concentration running at 2 mcg/kg/min, "
        "vasopressin at maximum dose, and phenylephrine. She remained intubated on mechanical "
        "ventilation, with a PF ratio of 114 by June 30, 2025 — indicating severe acute "
        "respiratory distress syndrome (ARDS). She was positive 15 liters of fluid since "
        "admission, a marker of the catastrophic failure of her circulatory system. Her liver "
        "enzymes remained markedly elevated, consistent with shock liver (hepatic ischemia "
        "secondary to hypoperfusion). She was also diagnosed with suspected disseminated "
        "intravascular coagulation (DIC) and acute encephalopathy.",
        NORMAL))

    story.append(Paragraph(
        "On July 1, 2025, Ms. Lopez’s daughters, Tavia Lemon and Samantha Romero, were at "
        "their mother’s bedside when the medical team updated them on her grave clinical "
        "status. As documented in the discharge summary:",
        NORMAL))

    story.append(Paragraph(
        "“On day of discharge both daughters updated at bedside regarding clinical status. "
        "They understood her grave clinical condition given her multi organ failure. They "
        "admitted she had been in poor health even prior to this hospitalization. They state "
        "that their mother would not want to have her life prolonged in this way and wish to "
        "transition her to hospice care.”",
        INDENT_BLOCK))

    story.append(Paragraph(
        "Elda Marisol Lopez passed away on July 1, 2025, at 5:16 PM after being "
        "transitioned to comfort care. Her death was the direct and proximate result of the "
        "traumatic splenic laceration she sustained in the June 20, 2025 motor vehicle "
        "collision.",
        NORMAL))

    story.append(Paragraph(
        "Enclosed please find copies of the complete medical records and Affidavit of Records "
        "Custodian from Christus Spohn Hospital Shoreline, including documentation of both "
        "hospitalizations.",
        NORMAL))

    # ── Current Costs ──
    story.append(Paragraph("Current Costs", SECTION_HDR))

    story.append(Spacer(1, 4))
    # Indent wrapper table
    usable_w = PAGE_W - LEFT - RIGHT
    indent_w = 54
    inner_w  = usable_w - indent_w

    bill_data = [
        ["Christus Spohn Hospital Shoreline\n"
         "(Admission 06/20/2025 – 06/21/2025,\n"
         "Account No. 6400000996012)",
         "$66,927.26"],
        [" ", ""],
        ["Christus Spohn Hospital Shoreline\n"
         "(Admission 06/27/2025 – 07/01/2025,\n"
         "Account No. 6400001013978)",
         "$335,567.56"],
    ]
    bill_tbl = Table(bill_data, colWidths=[inner_w * 0.72, inner_w * 0.28], hAlign="LEFT")
    bill_tbl.setStyle(TableStyle([
        ("FONTNAME",      (0, 0), (-1, -1), "Times-Roman"),
        ("FONTSIZE",      (0, 0), (-1, -1), 11),
        ("LEADING",       (0, 0), (-1, -1), 15),
        ("ALIGN",         (1, 0), (1, -1), "RIGHT"),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEBELOW",     (0, 2), (1, 2), 0.75, colors.black),
    ]))

    total_data = [["TOTAL HOSPITAL BILLS:", "$402,494.82"]]
    total_tbl = Table(total_data, colWidths=[inner_w * 0.72, inner_w * 0.28], hAlign="LEFT")
    total_tbl.setStyle(TableStyle([
        ("FONTNAME",      (0, 0), (-1, -1), "Times-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 11),
        ("LEADING",       (0, 0), (-1, -1), 15),
        ("ALIGN",         (1, 0), (1, 0),  "RIGHT"),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    wrapper = Table(
        [[bill_tbl], [total_tbl]],
        colWidths=[usable_w],
        hAlign="LEFT"
    )
    wrapper.setStyle(TableStyle([
        ("LEFTPADDING",   (0, 0), (-1, -1), indent_w),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(wrapper)
    story.append(Spacer(1, 10))

    # ── Damages section ──
    story.append(Paragraph("Damages", SECTION_HDR))

    story.append(Paragraph(
        "Elda Marisol Lopez was 53 years old at the time of the collision. She was the beloved "
        "mother of Tavia Lemon and Samantha Romero, both of whom were present at her bedside "
        "during the final moments of her life. Ms. Lopez was a woman of deep family devotion, "
        "and her sudden and tragic death has left an irreparable void in the lives of her "
        "daughters and all those who loved and depended upon her.",
        NORMAL))

    story.append(Paragraph(
        "Prior to her death, Elda Marisol Lopez endured eleven days of immense and escalating "
        "physical pain, suffering, and mental anguish. She was subjected to invasive emergency "
        "surgery, repeated blood transfusions, mechanical ventilation, continuous dialysis, and "
        "maximum-dose vasopressor infusions. She experienced the terror of acute hemorrhagic "
        "shock, the trauma of emergency intubation, and the indignity of total dependence on "
        "life-sustaining technology in her final days. The physical pain and emotional suffering "
        "that Ms. Lopez endured from the moment of the collision through the moment of her death "
        "constitutes the basis of the Survival Action brought on behalf of her estate.",
        NORMAL))

    story.append(Paragraph(
        "Tavia Lemon and Samantha Romero, as the wrongful death beneficiaries of Elda Marisol "
        "Lopez, have suffered and will continue to suffer the devastating loss of their mother’s "
        "love, companionship, comfort, guidance, and society. They witnessed their mother’s "
        "prolonged and painful decline, stood at her bedside as she died, and will carry that "
        "grief for the remainder of their lives. The mental anguish endured by Ms. Lopez’s "
        "daughters is profound and ongoing.",
        NORMAL))

    story.append(Paragraph(
        "It is reasonably foreseeable that the wrongful death beneficiaries will continue to "
        "endure significant emotional hardship and grief for the remainder of their lives. Their "
        "non-economic damages are substantial and ongoing.",
        NORMAL))

    story.append(Paragraph(
        "Liability in this matter is clear. The collision occurred because a vehicle turned left "
        "directly in the path of your insured’s oncoming vehicle, causing a violent impact "
        "that inflicted life-ending internal injuries upon Elda Marisol Lopez, who was an "
        "entirely innocent passenger. The resulting injuries — including a traumatic "
        "splenic laceration leading to delayed rupture, hemorrhagic shock, multi-organ failure, "
        "and death — are severe, well-documented, and irrefutably connected to the "
        "collision. Should this matter proceed to litigation, a jury would likely return a "
        "verdict well in excess of policy limits, awarding damages for both economic and "
        "non-economic losses, including the survival damages of Ms. Lopez for her pre-death "
        "pain and suffering, as well as the wrongful death damages of her daughters for loss "
        "of companionship, grief, mental anguish, and the loss of the love and support of "
        "their mother.",
        NORMAL))

    # ── Stowers Demand section ──
    story.append(Paragraph(
        "<u>STOWER’S DEMAND</u>",
        SECTION_HDR))

    story.append(Paragraph(
        "To be clear, the intent of this offer is to place Progressive Casualty Insurance "
        "Company in a Stowers situation as that term is commonly known within the insurance "
        "and litigation industry. Your insured should be made aware of the following:",
        NORMAL))

    stowers = [
        ("1.", "TEXAS RECOGNIZES A CAUSE OF ACTION ON THE PART OF AN INSURED AGAINST THE "
         "INSURED’S LIABILITY INSURANCE CARRIER (in this case Progressive Casualty "
         "Insurance Company) IF THE INSURED IS DAMAGED BECAUSE OF THE CARRIER’S "
         "NEGLIGENCE IN REFUSING TO SETTLE CLAIMS AGAINST THE INSURED WITHIN POLICY LIMITS. "
         "<i>G.A. Stowers Furniture Co. v. American Indemnity Co.</i>, 15 S.W.2d 544, 547 "
         "(Tex. Comm’n App. 1929, holding approved)."),
        ("2.", "The Stowers duty shifts the risk of an excess judgment (i.e., a judgment for "
         "more than the policy limits) from the insured to the insurer (i.e., Progressive "
         "Casualty Insurance Company)."),
        ("3.", "An insured suffers an injury for Stowers’ purposes if an excess judgment "
         "is awarded in this litigation."),
        ("4.", "If Progressive Casualty Insurance Company fails to settle with the Plaintiffs "
         "(i.e., if Progressive Casualty Insurance Company fails to accept the demand stated "
         "in this letter), and if an excess judgment is awarded, Plaintiffs may be entitled "
         "to recovery of actual damages, exemplary damages, interest, court costs, and "
         "attorney fees against Progressive Casualty Insurance Company."),
        ("5.", "Whether the insurer acted in “good faith” in deciding whether to "
         "accept or reject a demand such as the one stated in this letter is of no consequence "
         "to Stowers liability. The only consideration for Stowers liability is whether the "
         "insurer accepted a reasonable settlement offer within policy limits. Otherwise, the "
         "insurer will risk liability for an excess judgment against the insured."),
        ("6.", "Again, the insured, Keith N. Alvarez, is being given a chance to protect his "
         "financial assets. If insured should demand that Progressive Casualty Insurance "
         "Company settle for our offer, and Progressive Casualty Insurance Company refuses "
         "to do so, then the insured, Keith N. Alvarez, will be able to shift the risk of "
         "any excess judgment to the insurance company. Thus, by the insured Keith N. Alvarez "
         "demanding his insurance company immediately settle for the offer made herein, the "
         "insured, Keith N. Alvarez, can ensure that the insurance company will be responsible "
         "for paying any excess judgment. By making this offer, our clients have given the "
         "insured, Keith N. Alvarez, an opportunity to protect his individual assets. To "
         "protect these assets, he need only demand that the insurance company settle for "
         "our policy limits offer stated herein. Thereafter, any failure on the part of "
         "Progressive Casualty Insurance Company to do so would clearly be unreasonable "
         "given the gravity of the liability and damage facts stated above."),
    ]

    for num, text in stowers:
        story.append(Paragraph(f"<b>{num}</b>&nbsp;&nbsp;&nbsp;{text}", NUMBERED))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Again, I trust that the insured, Keith N. Alvarez, will be explained the dangers "
        "of this case and the role he can play in protecting his personal assets from excess "
        "judgment. Certainly, insured would probably be best served by Progressive Casualty "
        "Insurance Company forwarding this letter directly to him for review with a "
        "recommendation that he seek the advice of an attorney of his own choosing. In "
        "exchange for the payment of the policy limits held by insured, Keith N. Alvarez, "
        "Plaintiffs will agree to provide an executed full and final release of all claims "
        "against the insured, Keith N. Alvarez, arising out of the incident which is the "
        "basis of this claim.",
        NORMAL))

    story.append(Paragraph(
        "If there is anything you feel you need to finalize your evaluation, please let me "
        "know immediately. We can certainly accommodate any reasonable request for "
        "information within the time in which you have to respond to this offer.",
        NORMAL))

    story.append(Paragraph(
        "This demand expires at 5:00 p.m. (CST) June 24, 2026.",
        NORMAL))

    # ── Closing / signature ──
    story.append(Spacer(1, 14))
    story.append(Paragraph("Yours very truly,", SIGN_BLOCK))
    story.append(Spacer(1, 10))
    story.append(Paragraph("JANICEK LAW FIRM, P.C.", SIGN_BLOCK))
    story.append(Spacer(1, 18))
    story.append(Paragraph("<i>/s/ Philip G. Bernal</i>", SIGN_ITALIC))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Philip G. Bernal", SIGN_BLOCK))
    story.append(Paragraph("PGB/cm", SIGN_BLOCK))
    story.append(Spacer(1, 14))

    # ── Enclosures ──
    story.append(Paragraph("Enclosures:", SIGN_BLOCK))
    enclosures = [
        "Certified Texas Peace Officer’s Crash Report (Case No. C2503621)",
        "Christus Spohn Hospital Shoreline Medical Records and Affidavit\n"
        "(Account No. 6400000996012, Admission 06/20/2025 – 06/21/2025)",
        "Christus Spohn Hospital Shoreline Medical Records and Affidavit\n"
        "(Account No. 6400001013978, Admission 06/27/2025 – 07/01/2025)",
    ]
    for e in enclosures:
        story.append(Paragraph(e, ENCLOSURE))

    doc.build(story)
    print(f"PDF written to: {OUTPUT}")


if __name__ == "__main__":
    build()
