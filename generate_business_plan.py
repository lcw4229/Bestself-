#!/usr/bin/env python3
"""Generate International Sport Business Plan as a Word document."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
CHART_PATH = os.path.join(OUTPUT_DIR, "budget_chart.png")
DOC_PATH = os.path.join(OUTPUT_DIR, "International_Sport_Business_Plan.docx")

# ── Color Palette ──
BRAND_ORANGE = RGBColor(0xE8, 0x6C, 0x00)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
MEDIUM_GRAY = RGBColor(0x66, 0x66, 0x66)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def set_cell_shading(cell, color_hex):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color_hex)
    shading.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge, val in kwargs.items():
        element = OxmlElement(f'w:{edge}')
        element.set(qn('w:val'), val.get('val', 'single'))
        element.set(qn('w:sz'), val.get('sz', '4'))
        element.set(qn('w:color'), val.get('color', '000000'))
        element.set(qn('w:space'), '0')
        tcBorders.append(element)
    tcPr.append(tcBorders)


def add_formatted_paragraph(doc, text, style='Normal', bold=False, size=11,
                             color=DARK_GRAY, alignment=WD_ALIGN_PARAGRAPH.LEFT,
                             space_after=6, space_before=0, first_line_indent=None):
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    if first_line_indent:
        p.paragraph_format.first_line_indent = Inches(first_line_indent)
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.name = 'Times New Roman'
    return p


def add_heading_styled(doc, text, level=1):
    if level == 1:
        p = add_formatted_paragraph(doc, text, bold=True, size=16,
                                     color=BRAND_ORANGE, space_before=18, space_after=8)
    elif level == 2:
        p = add_formatted_paragraph(doc, text, bold=True, size=13,
                                     color=DARK_GRAY, space_before=12, space_after=6)
    else:
        p = add_formatted_paragraph(doc, text, bold=True, size=11,
                                     color=DARK_GRAY, space_before=8, space_after=4)
    return p


def add_body(doc, text, indent=False):
    return add_formatted_paragraph(doc, text, size=12, space_after=6,
                                    first_line_indent=0.5 if indent else None)


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.clear()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.left_indent = Inches(0.5 + level * 0.25)
    run = p.add_run(text)
    run.font.size = Pt(12)
    run.font.color.rgb = DARK_GRAY
    run.font.name = 'Times New Roman'
    return p


def generate_budget_chart():
    categories = [
        'Facility Lease &\nRenovation',
        'Equipment &\nTechnology',
        'Staff Salaries\n& Training',
        'Digital Platform\nDevelopment',
        'Marketing &\nPromotion',
        'Operations &\nAdministration',
        'Contingency\nFund'
    ]
    year1 = [180000, 95000, 220000, 150000, 120000, 85000, 50000]
    year2 = [140000, 60000, 310000, 80000, 160000, 110000, 45000]
    year3 = [120000, 45000, 420000, 60000, 200000, 140000, 40000]

    revenue_years = ['Year 1', 'Year 2', 'Year 3']
    revenue = [320000, 780000, 1450000]
    expenses = [sum(year1), sum(year2), sum(year3)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

    # Chart 1: Grouped bar chart for expenses by category
    x = np.arange(len(categories))
    width = 0.25
    colors = ['#E86C00', '#2E86AB', '#A23B72']

    bars1 = axes[0].bar(x - width, [v/1000 for v in year1], width, label='Year 1', color=colors[0], edgecolor='white', linewidth=0.5)
    bars2 = axes[0].bar(x, [v/1000 for v in year2], width, label='Year 2', color=colors[1], edgecolor='white', linewidth=0.5)
    bars3 = axes[0].bar(x + width, [v/1000 for v in year3], width, label='Year 3', color=colors[2], edgecolor='white', linewidth=0.5)

    axes[0].set_ylabel('Amount (USD Thousands)', fontsize=10, fontweight='bold')
    axes[0].set_title('Projected Expenses by Category', fontsize=12, fontweight='bold', pad=12)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(categories, fontsize=7.5)
    axes[0].legend(fontsize=9)
    axes[0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f'${v:.0f}K'))
    axes[0].spines['top'].set_visible(False)
    axes[0].spines['right'].set_visible(False)
    axes[0].grid(axis='y', alpha=0.3)

    # Chart 2: Revenue vs Total Expenses
    x2 = np.arange(len(revenue_years))
    width2 = 0.35
    axes[1].bar(x2 - width2/2, [v/1000 for v in revenue], width2, label='Revenue', color='#2ECC71', edgecolor='white', linewidth=0.5)
    axes[1].bar(x2 + width2/2, [v/1000 for v in expenses], width2, label='Total Expenses', color='#E74C3C', edgecolor='white', linewidth=0.5)

    axes[1].set_ylabel('Amount (USD Thousands)', fontsize=10, fontweight='bold')
    axes[1].set_title('Revenue vs. Expenses Projection', fontsize=12, fontweight='bold', pad=12)
    axes[1].set_xticks(x2)
    axes[1].set_xticklabels(revenue_years, fontsize=10)
    axes[1].legend(fontsize=9)
    axes[1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f'${v:.0f}K'))
    axes[1].spines['top'].set_visible(False)
    axes[1].spines['right'].set_visible(False)
    axes[1].grid(axis='y', alpha=0.3)

    for bar_group in [bars1, bars2, bars3]:
        for bar in bar_group:
            h = bar.get_height()
            if h > 30:
                axes[0].annotate(f'${h:.0f}K', xy=(bar.get_x() + bar.get_width()/2, h),
                               xytext=(0, 3), textcoords='offset points',
                               ha='center', va='bottom', fontsize=6.5)

    plt.tight_layout(pad=2.0)
    plt.savefig(CHART_PATH, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def build_document():
    doc = Document()

    # ── Page Setup ──
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = DARK_GRAY

    # ════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════
    for _ in range(6):
        doc.add_paragraph()

    add_formatted_paragraph(doc, 'HoopRise Basketball Academy', bold=True, size=28,
                             color=BRAND_ORANGE, alignment=WD_ALIGN_PARAGRAPH.CENTER,
                             space_after=4)
    add_formatted_paragraph(doc, 'International Sport Business Plan', bold=True, size=18,
                             color=DARK_GRAY, alignment=WD_ALIGN_PARAGRAPH.CENTER,
                             space_after=4)

    # Decorative line
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('━' * 40)
    run.font.color.rgb = BRAND_ORANGE
    run.font.size = Pt(12)

    add_formatted_paragraph(doc, 'Expanding Youth Basketball Development in India',
                             size=14, color=MEDIUM_GRAY,
                             alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=30)

    add_formatted_paragraph(doc, 'Prepared for: International Sport Business',
                             size=12, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_formatted_paragraph(doc, 'June 2026',
                             size=12, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)

    doc.add_page_break()

    # ════════════════════════════════════════
    # TABLE OF CONTENTS
    # ════════════════════════════════════════
    add_formatted_paragraph(doc, 'Table of Contents', bold=True, size=16,
                             color=BRAND_ORANGE, space_after=12)

    toc_items = [
        ('Market Research Summary', '1'),
        ('The Concept', '2'),
        ('Mission Statement', '3'),
        ('Competitive Position', '3'),
        ('Cultural Considerations', '5'),
        ('Fundraising/Financing', '6'),
        ('Promotional Strategies', '7'),
        ('Anticipated Budget', '8'),
        ('Strategic Partnerships', '9'),
        ('References', '10'),
    ]
    for title, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(6), alignment=WD_ALIGN_PARAGRAPH.RIGHT, leader=1)
        run = p.add_run(title)
        run.font.size = Pt(12)
        run.font.name = 'Times New Roman'
        run.font.color.rgb = DARK_GRAY
        run2 = p.add_run(f'\t{page}')
        run2.font.size = Pt(12)
        run2.font.name = 'Times New Roman'
        run2.font.color.rgb = MEDIUM_GRAY

    doc.add_page_break()

    # ════════════════════════════════════════
    # MARKET RESEARCH SUMMARY (1 page)
    # ════════════════════════════════════════
    add_heading_styled(doc, 'Market Research Summary')

    add_heading_styled(doc, 'Key Demographics and Market Size', level=2)
    add_body(doc,
        'India represents one of the most compelling emerging markets for basketball development in the world. '
        'With a population exceeding 1.44 billion people, India is the world\'s most populous nation, and its '
        'demographic profile is exceptionally youth-oriented: approximately 65% of the population is under 35 years '
        'of age, and the median age stands at 28.4 years (United Nations, 2024). This positions India as a market '
        'with an enormous base of potential young athletes. The Indian sports industry is valued at approximately '
        '$2.7 billion and is projected to reach $10 billion by 2030, driven by rising disposable incomes, '
        'urbanization, and increased government investment in sports infrastructure (KPMG, 2023). Basketball '
        'specifically has seen rapid growth, with the NBA estimating over 300 million basketball fans in India '
        'as of 2024, making it the league\'s second-largest market outside the United States.',
        indent=True)

    add_heading_styled(doc, 'Consumer Behavior Trends', level=2)
    add_body(doc,
        'Indian consumers, particularly in the 15-30 age bracket, are increasingly health-conscious and drawn to '
        'fitness-oriented lifestyles. The rapid proliferation of affordable smartphones and low-cost mobile data '
        '(averaging $0.17 per GB, among the cheapest globally) has created a digitally connected generation that '
        'consumes sports content voraciously through platforms like YouTube, Instagram, and streaming services '
        '(Deloitte, 2024). Parents in India\'s growing middle class, now estimated at over 400 million people, '
        'are investing more in extracurricular activities for their children, viewing sports as a pathway to '
        'holistic development and potential scholarship opportunities. The rise of the Indian Premier League (IPL) '
        'has demonstrated that Indian consumers are willing to embrace and passionately support well-marketed '
        'sporting ventures, setting a precedent for other sports to follow.',
        indent=True)

    add_heading_styled(doc, 'Opportunities and Challenges', level=2)
    add_body(doc,
        'The opportunities for entering India\'s basketball market are substantial. The Indian government\'s '
        'Khelo India initiative has allocated over $350 million toward sports development, including basketball '
        'infrastructure. The NBA\'s establishment of the NBA Academy India in 2017 and the launch of the '
        'Basketball Africa League model provide proof of concept for structured basketball development programs. '
        'India\'s rapid urbanization, with 35% of the population now living in cities, creates concentrated demand '
        'centers. However, challenges exist: cricket\'s cultural dominance means basketball must compete for '
        'attention and participation; infrastructure gaps persist, with limited access to quality indoor courts; '
        'and price sensitivity remains a factor, as training programs must be accessible across income levels. '
        'Additionally, navigating India\'s diverse regulatory landscape across 28 states and 8 union territories '
        'requires localized strategies.',
        indent=True)

    doc.add_page_break()

    # ════════════════════════════════════════
    # THE CONCEPT
    # ════════════════════════════════════════
    add_heading_styled(doc, 'The Concept')
    add_body(doc,
        'HoopRise Basketball Academy is a hybrid basketball training and development enterprise that combines '
        'world-class physical training facilities with an integrated digital platform to deliver comprehensive '
        'basketball education to Indian youth. The academy will establish premium training centers in three of '
        'India\'s largest metropolitan areas—Mumbai, Delhi NCR, and Bangalore—while simultaneously launching '
        'a mobile application that extends training access to aspiring basketball players across the entire nation.',
        indent=True)

    add_body(doc,
        'The physical academies will feature regulation-size indoor courts, strength and conditioning facilities, '
        'sports science labs with motion capture technology, and classrooms for tactical instruction. Each location '
        'will be staffed by certified coaches with international playing or coaching experience, supplemented by '
        'local assistant coaches who understand regional dynamics. Training programs will be structured into tiered '
        'levels—Beginner, Intermediate, Advanced, and Elite—accommodating players from ages 8 to 22.',
        indent=True)

    add_body(doc,
        'The HoopRise digital platform will serve as both a training companion and a standalone product. It will '
        'feature AI-driven skill assessment tools, video-based drill libraries with demonstrations in multiple '
        'Indian languages, performance tracking dashboards, and virtual coaching sessions. This hybrid model '
        'addresses a critical gap in the Indian market: while interest in basketball is surging, structured and '
        'accessible training programs remain scarce, particularly outside major cities. HoopRise bridges this divide '
        'by making high-quality basketball development available to any young Indian with a smartphone, while '
        'offering an immersive in-person experience for those in proximity to academy locations.',
        indent=True)

    doc.add_page_break()

    # ════════════════════════════════════════
    # MISSION STATEMENT
    # ════════════════════════════════════════
    add_heading_styled(doc, 'Mission Statement')
    add_body(doc,
        'HoopRise Basketball Academy exists to democratize basketball excellence across India by providing '
        'world-class training infrastructure, expert coaching, and innovative digital tools that develop the '
        'next generation of Indian basketball talent. Our mission is to nurture athletic skill, physical fitness, '
        'teamwork, and personal character in every young player who enters our program, regardless of socioeconomic '
        'background or geographic location. We are committed to making basketball a mainstream pathway for youth '
        'development in India by combining global best practices with deep cultural understanding, creating an '
        'ecosystem where Indian basketball talent can be identified, cultivated, and elevated to compete on the '
        'world stage.',
        indent=True)

    add_body(doc,
        'Our core objectives are threefold: (1) to establish India\'s most recognized and respected basketball '
        'training brand within five years; (2) to develop a pipeline of players capable of competing in '
        'international leagues, collegiate programs, and national teams; and (3) to reach one million aspiring '
        'basketball players through our digital platform within three years of launch. We will achieve these '
        'objectives through relentless investment in coaching quality, technology-enabled training methodologies, '
        'and strategic partnerships that amplify our reach and credibility.',
        indent=True)

    # ════════════════════════════════════════
    # COMPETITIVE POSITION
    # ════════════════════════════════════════
    add_heading_styled(doc, 'Competitive Position')

    add_heading_styled(doc, 'Target Market Profile', level=2)
    add_body(doc,
        'HoopRise\'s primary target demographic consists of youth aged 8 to 22 from middle-class and upper-middle-class '
        'families in urban and semi-urban India. This segment is characterized by household incomes of $10,000 to '
        '$50,000 annually, parents who prioritize education and extracurricular development, and young people who '
        'are digitally native and influenced by global sports culture. Secondary targets include collegiate athletes '
        'seeking advanced training, corporate clients interested in team-building basketball programs, and recreational '
        'adult players in the 23-35 age range who participate in weekend leagues and fitness activities.',
        indent=True)

    add_body(doc,
        'The target demographic encompasses roughly 120 million youth across India\'s top 20 cities, with our '
        'initial focus on the combined metropolitan populations of Mumbai (21 million), Delhi NCR (32 million), '
        'and Bangalore (13 million). These cities were selected based on their high concentration of middle-class '
        'families, existing basketball interest, availability of commercial real estate suitable for academy '
        'facilities, and strong digital infrastructure. The lifestyle profile of our target consumer includes '
        'active engagement with social media, consumption of international sports content (particularly the NBA), '
        'participation in fitness trends, and openness to adopting new sporting activities as alternatives or '
        'complements to cricket.',
        indent=True)

    add_heading_styled(doc, 'Key Competitors', level=2)

    # Competitor table
    table = doc.add_table(rows=5, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    headers = ['Competitor', 'Strengths', 'Weaknesses', 'Market Position']
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = WHITE
        run.font.name = 'Times New Roman'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, 'E86C00')

    competitors = [
        ['NBA Academy India',
         'Global brand recognition; elite-level coaching; NBA pipeline',
         'Extremely selective (only top 24 players); single location; no mass-market access',
         'Niche/Elite'],
        ['Stepanova Basketball\nAcademy',
         'Established presence; affordable pricing; grassroots focus',
         'Limited facilities; no digital platform; inconsistent coaching quality',
         'Local/Grassroots'],
        ['Local Municipal\nPrograms',
         'Free or very low cost; government support; wide geographic spread',
         'Poor infrastructure; untrained coaches; no structured curriculum',
         'Mass/Basic'],
        ['International Online\nPlatforms (HomeCourt)',
         'Advanced technology; AI-driven analysis; global user base',
         'No local presence; English-only; not tailored to Indian context',
         'Digital/Global'],
    ]

    for row_idx, comp in enumerate(competitors, 1):
        for col_idx, val in enumerate(comp):
            cell = table.rows[row_idx].cells[col_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(9)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = DARK_GRAY
            if row_idx % 2 == 0:
                set_cell_shading(cell, 'FFF3E6')

    add_formatted_paragraph(doc, '', size=6, space_after=6)

    add_heading_styled(doc, 'Competitive Differentiation', level=2)
    add_body(doc,
        'HoopRise differentiates itself through its unique hybrid model that no current competitor in the Indian '
        'market offers. While the NBA Academy India serves only an elite few, and local programs lack quality and '
        'structure, HoopRise occupies the strategic middle ground—premium yet accessible. Our key differentiators '
        'include:',
        indent=True)

    add_bullet(doc, 'Hybrid Physical-Digital Model: In-person training complemented by a comprehensive mobile '
                    'app, ensuring continuity and accessibility beyond academy walls.')
    add_bullet(doc, 'Data-Driven Development: AI-powered performance tracking that provides personalized training '
                    'plans based on each player\'s strengths, weaknesses, and progress trajectory.')
    add_bullet(doc, 'Tiered Pricing Structure: Scholarship programs and subsidized digital access ensure that '
                    'economic barriers do not prevent talented players from accessing quality training.')
    add_bullet(doc, 'Multilingual Platform: Training content available in Hindi, English, Tamil, Kannada, and '
                    'Marathi, reflecting the linguistic diversity of our target cities.')
    add_bullet(doc, 'Pathway to Professional Play: Structured relationships with international collegiate programs '
                    'and professional leagues that offer players a visible pathway to competitive basketball careers.')

    doc.add_page_break()

    # ════════════════════════════════════════
    # CULTURAL CONSIDERATIONS
    # ════════════════════════════════════════
    add_heading_styled(doc, 'Cultural Considerations')

    add_heading_styled(doc, 'Family-Centric Decision Making', level=2)
    add_body(doc,
        'In Indian culture, decisions regarding children\'s extracurricular activities are predominantly made by '
        'parents, and often influenced by extended family. HoopRise\'s marketing and enrollment strategies will '
        'directly address parental concerns by emphasizing the academic and character-building benefits of basketball '
        'participation. All promotional materials will include messaging about discipline, time management, and '
        'teamwork—qualities that resonate with Indian parents. Open-house events, parent orientation sessions, and '
        'quarterly progress reports will build trust and maintain family engagement. The enrollment process will be '
        'designed to involve parents as partners, not merely as bill-payers.',
        indent=True)

    add_heading_styled(doc, 'Education-First Culture', level=2)
    add_body(doc,
        'India\'s deep cultural emphasis on academic achievement means that any sports program must position itself '
        'as complementary to education, not in competition with it. HoopRise will schedule training sessions around '
        'school hours and examination periods, offering flexible scheduling during board exam seasons (March-April '
        'and October-November). The academy will highlight success stories of basketball players who earned '
        'scholarships to international universities, directly linking athletic development to educational opportunity. '
        'A homework and study space within each academy facility will reinforce this message tangibly.',
        indent=True)

    add_heading_styled(doc, 'Language and Regional Diversity', level=2)
    add_body(doc,
        'India\'s linguistic landscape is extraordinarily diverse, with 22 officially recognized languages and '
        'hundreds of dialects. Coaching at each academy will be conducted bilingually—in English and the dominant '
        'regional language (Hindi in Delhi, Marathi in Mumbai, and Kannada in Bangalore). The digital platform will '
        'offer content in five languages at launch, with additional languages added based on user demand. Marketing '
        'campaigns will be localized not just linguistically but contextually, using region-specific sports analogies '
        'and cultural references to build resonance.',
        indent=True)

    add_heading_styled(doc, 'Religious and Festival Sensitivity', level=2)
    add_body(doc,
        'India\'s multifaith society observes numerous religious festivals throughout the year, including Diwali, '
        'Eid, Christmas, Pongal, Holi, and Navratri. HoopRise will develop an annual calendar that respects these '
        'observances by adjusting schedules, hosting themed basketball events during festival seasons, and '
        'incorporating inclusive celebrations that bring together players from diverse backgrounds. This approach '
        'not only demonstrates cultural respect but also positions the academy as a unifying space where diversity '
        'is celebrated through sport.',
        indent=True)

    add_heading_styled(doc, 'Gender Considerations', level=2)
    add_body(doc,
        'While urban India is progressively embracing women\'s participation in sports, cultural sensitivities remain, '
        'particularly regarding co-educational sports settings for adolescents. HoopRise will offer dedicated '
        'training sessions for girls and young women, staffed by female coaches, to encourage participation from '
        'families who may be hesitant about mixed-gender training environments. Promotional campaigns will '
        'prominently feature female basketball role models and highlight the empowerment benefits of athletic '
        'participation for young women, aligning with India\'s growing movement toward gender equity in sports.',
        indent=True)

    doc.add_page_break()

    # ════════════════════════════════════════
    # FUNDRAISING / FINANCING
    # ════════════════════════════════════════
    add_heading_styled(doc, 'Fundraising/Financing')

    add_body(doc,
        'HoopRise will pursue a diversified funding strategy to secure the estimated $900,000 required for '
        'initial launch and first-year operations. This multi-pronged approach reduces dependency on any single '
        'funding source and builds a resilient financial foundation.',
        indent=True)

    add_heading_styled(doc, 'Angel Investors and Venture Capital', level=2)
    add_body(doc,
        'India\'s sports-tech investment landscape has grown significantly, with firms such as Dream Sports, '
        'Blume Ventures, and Sequoia India actively seeking sports-related ventures. HoopRise will target a '
        'seed funding round of $400,000 from angel investors with demonstrated interest in sports, education, or '
        'youth development. The pitch will emphasize the scalable hybrid model, India\'s demographic advantage, '
        'and the growing global interest in Indian basketball as key value propositions.',
        indent=True)

    add_heading_styled(doc, 'Government Grants and Initiatives', level=2)
    add_body(doc,
        'The Indian government\'s Khelo India program and the Sports Authority of India (SAI) offer grants and '
        'subsidies to organizations that develop sports infrastructure and grassroots participation. HoopRise '
        'will apply for recognition as an accredited training center under these programs, potentially securing '
        '$100,000-$150,000 in grants and access to government sports facilities at subsidized rates. State-level '
        'sports departments in Maharashtra, Delhi, and Karnataka also offer complementary funding opportunities.',
        indent=True)

    add_heading_styled(doc, 'Corporate Sponsorships', level=2)
    add_body(doc,
        'India\'s Corporate Social Responsibility (CSR) mandate requires companies with net profits above a '
        'threshold to spend 2% on social initiatives. Sports development and youth empowerment qualify as CSR '
        'activities, opening avenues for sponsorship from major Indian corporations such as Tata Group, Reliance '
        'Industries, and Infosys. HoopRise will develop tiered sponsorship packages ranging from $25,000 to '
        '$200,000, offering brand visibility at academy facilities, on the digital platform, and at events.',
        indent=True)

    add_heading_styled(doc, 'Crowdfunding', level=2)
    add_body(doc,
        'A targeted crowdfunding campaign on platforms like Ketto (India\'s leading crowdfunding platform) and '
        'Kickstarter will aim to raise $50,000-$75,000 while simultaneously building brand awareness and community '
        'engagement. The campaign will highlight the social impact narrative of democratizing basketball access for '
        'Indian youth, offering rewards such as discounted academy memberships, branded merchandise, and exclusive '
        'content access.',
        indent=True)

    doc.add_page_break()

    # ════════════════════════════════════════
    # PROMOTIONAL STRATEGIES
    # ════════════════════════════════════════
    add_heading_styled(doc, 'Promotional Strategies')

    add_heading_styled(doc, 'Digital Marketing Campaigns', level=2)
    add_body(doc,
        'Given India\'s massive digital population of over 800 million internet users, digital marketing will serve '
        'as the primary promotional channel. HoopRise will execute targeted campaigns across Instagram, YouTube, '
        'and Facebook, leveraging video content that showcases training methodologies, player transformations, and '
        'behind-the-scenes academy life. YouTube pre-roll advertisements during NBA content will directly reach '
        'the target audience. Search engine optimization (SEO) and Google Ads campaigns targeting keywords such as '
        '"basketball training India," "basketball academy near me," and "learn basketball" will capture '
        'intent-driven traffic. A content marketing strategy will produce weekly blog posts and video tutorials '
        'that establish HoopRise as a thought leader in Indian basketball development.',
        indent=True)

    add_heading_styled(doc, 'Influencer and Ambassador Partnerships', level=2)
    add_body(doc,
        'HoopRise will partner with Indian basketball personalities, fitness influencers, and youth-oriented content '
        'creators to amplify brand awareness. Key targets include Satnam Singh (first Indian drafted by an NBA team), '
        'Prachi Tehlan (former Indian national team captain), and popular fitness YouTubers with audiences that '
        'overlap with the target demographic. Micro-influencers in each target city will be engaged to drive '
        'localized awareness and enrollment. Ambassador partnerships will include content creation agreements, '
        'appearance fees for academy events, and social media collaboration campaigns.',
        indent=True)

    add_heading_styled(doc, 'School and University Outreach', level=2)
    add_body(doc,
        'Direct partnerships with schools and universities in target cities will be a critical enrollment driver. '
        'HoopRise will offer free introductory basketball clinics at partner schools, donate equipment to schools '
        'that establish basketball programs, and sponsor inter-school basketball tournaments. University partnerships '
        'will focus on establishing HoopRise as the preferred training partner for collegiate basketball teams, '
        'offering subsidized group training packages and access to the digital platform for team performance analysis.',
        indent=True)

    add_heading_styled(doc, 'Event Sponsorships and Community Engagement', level=2)
    add_body(doc,
        'HoopRise will sponsor and organize community basketball events, including three-on-three street basketball '
        'tournaments, youth basketball camps during school holidays, and basketball viewing parties during major NBA '
        'events (NBA Finals, All-Star Weekend). These events will serve as experiential marketing touchpoints, '
        'allowing potential customers to interact with the brand, experience coaching quality firsthand, and '
        'engage with the HoopRise community. Annual events such as the "HoopRise Rising Stars Challenge" will '
        'generate media coverage and social media engagement, positioning the brand as central to India\'s '
        'basketball culture.',
        indent=True)

    doc.add_page_break()

    # ════════════════════════════════════════
    # ANTICIPATED BUDGET
    # ════════════════════════════════════════
    add_heading_styled(doc, 'Anticipated Budget')

    add_body(doc,
        'The following budget outlines projected expenses and revenue for HoopRise Basketball Academy over a '
        'three-year period. Year 1 focuses on establishment and launch, Year 2 on growth and market penetration, '
        'and Year 3 on scaling and profitability.',
        indent=True)

    # Budget table
    budget_table = doc.add_table(rows=9, cols=4)
    budget_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    budget_table.style = 'Table Grid'

    budget_headers = ['Category', 'Year 1 (USD)', 'Year 2 (USD)', 'Year 3 (USD)']
    for i, h in enumerate(budget_headers):
        cell = budget_table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = WHITE
        run.font.name = 'Times New Roman'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, 'E86C00')

    budget_data = [
        ['Facility Lease & Renovation', '$180,000', '$140,000', '$120,000'],
        ['Equipment & Technology', '$95,000', '$60,000', '$45,000'],
        ['Staff Salaries & Training', '$220,000', '$310,000', '$420,000'],
        ['Digital Platform Development', '$150,000', '$80,000', '$60,000'],
        ['Marketing & Promotion', '$120,000', '$160,000', '$200,000'],
        ['Operations & Administration', '$85,000', '$110,000', '$140,000'],
        ['Contingency Fund', '$50,000', '$45,000', '$40,000'],
        ['Total Expenses', '$900,000', '$905,000', '$1,025,000'],
    ]

    for row_idx, row_data in enumerate(budget_data, 1):
        for col_idx, val in enumerate(row_data):
            cell = budget_table.rows[row_idx].cells[col_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(10)
            run.font.name = 'Times New Roman'
            if row_idx == 8:  # Total row
                run.bold = True
                run.font.color.rgb = WHITE
                set_cell_shading(cell, '333333')
            else:
                run.font.color.rgb = DARK_GRAY
                if col_idx > 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                if row_idx % 2 == 0:
                    set_cell_shading(cell, 'FFF3E6')

    add_formatted_paragraph(doc, '', size=8, space_after=8)

    # Revenue projection
    add_heading_styled(doc, 'Projected Revenue', level=2)

    rev_table = doc.add_table(rows=5, cols=4)
    rev_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    rev_table.style = 'Table Grid'

    rev_headers = ['Revenue Stream', 'Year 1 (USD)', 'Year 2 (USD)', 'Year 3 (USD)']
    for i, h in enumerate(rev_headers):
        cell = rev_table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = WHITE
        run.font.name = 'Times New Roman'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, '2E86AB')

    rev_data = [
        ['Academy Memberships', '$180,000', '$420,000', '$720,000'],
        ['Digital Platform Subscriptions', '$40,000', '$150,000', '$380,000'],
        ['Corporate Programs & Events', '$60,000', '$130,000', '$230,000'],
        ['Sponsorship & Partnerships', '$40,000', '$80,000', '$120,000'],
    ]

    for row_idx, row_data in enumerate(rev_data, 1):
        for col_idx, val in enumerate(row_data):
            cell = rev_table.rows[row_idx].cells[col_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(10)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = DARK_GRAY
            if col_idx > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if row_idx % 2 == 0:
                set_cell_shading(cell, 'E6F4FA')

    add_formatted_paragraph(doc, '', size=6, space_after=4)

    add_body(doc,
        'Total projected revenue grows from $320,000 in Year 1 to $780,000 in Year 2 and $1,450,000 in Year 3, '
        'achieving profitability by the second half of Year 2. The break-even point is projected at approximately '
        '18 months post-launch, driven primarily by scaling academy memberships and rapid adoption of the digital '
        'platform.',
        indent=True)

    # Insert chart
    add_formatted_paragraph(doc, '', size=4, space_after=2)
    doc.add_picture(CHART_PATH, width=Inches(6.2))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # ════════════════════════════════════════
    # STRATEGIC PARTNERSHIPS
    # ════════════════════════════════════════
    add_heading_styled(doc, 'Strategic Partnerships')

    add_body(doc,
        'Strategic partnerships are essential to HoopRise\'s market entry strategy, providing credibility, '
        'resources, and access that would be difficult and costly to build independently. The following partnerships '
        'have been identified as high-priority targets, each aligned with specific business objectives.',
        indent=True)

    add_heading_styled(doc, 'NBA India', level=2)
    add_body(doc,
        'A partnership with NBA India is the cornerstone of HoopRise\'s credibility strategy. The NBA has invested '
        'heavily in growing basketball in India through initiatives like NBA Academy India, Jr. NBA programs, and '
        'broadcast partnerships. HoopRise will seek designation as an official NBA-affiliated training center, '
        'gaining access to NBA coaching methodologies, curriculum frameworks, and brand association. This partnership '
        'would also create pathways for HoopRise players to participate in NBA India events and potentially be '
        'scouted for the NBA Academy, adding significant value to the training proposition.',
        indent=True)

    add_heading_styled(doc, 'Nike India / Adidas India', level=2)
    add_body(doc,
        'An equipment and apparel partnership with a major sportswear brand will provide HoopRise with high-quality '
        'training gear, branded academy uniforms, and co-marketing opportunities. Nike, which has a strong '
        'basketball heritage and growing presence in India, is the preferred partner. The partnership would include '
        'equipment supply at preferential rates, co-branded marketing campaigns, and potential funding for '
        'scholarship programs. In return, the sportswear partner gains a dedicated channel for youth basketball '
        'engagement and product placement in a growing market segment.',
        indent=True)

    add_heading_styled(doc, 'Basketball Federation of India (BFI)', level=2)
    add_body(doc,
        'Alignment with the BFI provides institutional legitimacy and access to the national basketball ecosystem. '
        'HoopRise will seek recognition as an accredited training center, enabling academy players to be eligible '
        'for state and national team selection pathways. This partnership also opens doors to participation in '
        'BFI-organized tournaments, coaching certification programs, and access to government sports facilities. '
        'The BFI benefits from HoopRise\'s contribution to grassroots development and talent identification, '
        'strengthening the overall basketball pipeline in India.',
        indent=True)

    add_heading_styled(doc, 'Indian School and University Networks', level=2)
    add_body(doc,
        'Formal partnerships with school networks such as Delhi Public School (DPS), Amity International, and '
        'Ryan International will embed HoopRise within the education ecosystem. These partnerships will include '
        'after-school basketball programs conducted at school facilities, preferential enrollment rates for '
        'students of partner schools, and inter-school tournament sponsorship. University partnerships with '
        'institutions like Christ University (Bangalore), Shiv Nadar University (Delhi), and NMIMS (Mumbai) will '
        'focus on collegiate basketball development, internship opportunities, and sports management collaborations.',
        indent=True)

    add_heading_styled(doc, 'Technology Partners', level=2)
    add_body(doc,
        'Partnerships with Indian technology companies will support the development and scaling of the HoopRise '
        'digital platform. Collaborations with firms such as Infosys or Wipro for platform development, Amazon Web '
        'Services (AWS) India for cloud infrastructure (including startup credits programs), and sports technology '
        'companies like ShotTracker or Noah Basketball for performance analytics integration will ensure a '
        'world-class digital experience. These partnerships reduce development costs while providing access to '
        'cutting-edge technology that enhances the training experience.',
        indent=True)

    doc.add_page_break()

    # ════════════════════════════════════════
    # REFERENCES
    # ════════════════════════════════════════
    add_heading_styled(doc, 'References')

    references = [
        'Deloitte. (2024). India\'s digital sports consumption: Trends and opportunities in a mobile-first '
        'market. Deloitte Touche Tohmatsu India LLP.',

        'KPMG. (2023). The business of sports: A comprehensive analysis of India\'s evolving sports industry '
        'landscape. KPMG India.',

        'National Basketball Association. (2024). NBA global outreach report: Expanding basketball culture '
        'in emerging markets. NBA Communications.',

        'Sports Authority of India. (2023). Khelo India annual report 2022-2023: Building a sporting nation '
        'through grassroots development. Ministry of Youth Affairs and Sports, Government of India.',

        'United Nations Department of Economic and Social Affairs. (2024). World population prospects 2024: '
        'India demographic profile summary. United Nations Publications.',
    ]

    for ref in references:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        run = p.add_run(ref)
        run.font.size = Pt(12)
        run.font.name = 'Times New Roman'
        run.font.color.rgb = DARK_GRAY

    # ── Save ──
    doc.save(DOC_PATH)
    print(f"Document saved: {DOC_PATH}")


if __name__ == '__main__':
    generate_budget_chart()
    print(f"Chart saved: {CHART_PATH}")
    build_document()
