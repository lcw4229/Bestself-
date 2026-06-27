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
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
CHART_PATH = os.path.join(OUTPUT_DIR, "budget_chart.png")
DOC_PATH = os.path.join(OUTPUT_DIR, "International_Sport_Business_Plan.docx")

BRAND_ORANGE = RGBColor(0xE8, 0x6C, 0x00)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
MEDIUM_GRAY = RGBColor(0x66, 0x66, 0x66)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def set_cell_shading(cell, color_hex):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color_hex)
    shading.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading)


def add_formatted_paragraph(doc, text, bold=False, size=11,
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
        add_formatted_paragraph(doc, text, bold=True, size=16,
                                color=BRAND_ORANGE, space_before=18, space_after=8)
    elif level == 2:
        add_formatted_paragraph(doc, text, bold=True, size=13,
                                color=DARK_GRAY, space_before=12, space_after=6)
    else:
        add_formatted_paragraph(doc, text, bold=True, size=11,
                                color=DARK_GRAY, space_before=8, space_after=4)


def add_body(doc, text, indent=False):
    return add_formatted_paragraph(doc, text, size=12, space_after=6,
                                    first_line_indent=0.5 if indent else None)


def add_bullet(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    p.clear()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.left_indent = Inches(0.5)
    run = p.add_run(text)
    run.font.size = Pt(12)
    run.font.color.rgb = DARK_GRAY
    run.font.name = 'Times New Roman'


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

    # ── COVER PAGE ──
    for _ in range(6):
        doc.add_paragraph()

    add_formatted_paragraph(doc, 'HoopRise Basketball Academy', bold=True, size=28,
                             color=BRAND_ORANGE, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_formatted_paragraph(doc, 'International Sport Business Plan', bold=True, size=18,
                             color=DARK_GRAY, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)

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

    # ── TABLE OF CONTENTS ──
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

    # ── MARKET RESEARCH SUMMARY ──
    add_heading_styled(doc, 'Market Research Summary')

    add_heading_styled(doc, 'Key Demographics and Market Size', level=2)
    add_body(doc,
        'When looking at untapped basketball markets around the world, India stands out immediately. '
        'The country has over 1.44 billion people, making it the most populous nation on Earth, and the '
        'demographics skew incredibly young—roughly 65% of Indians are under the age of 35, with the '
        'median age sitting at just 28.4 years (United Nations, 2024). That is a massive pool of potential '
        'young athletes. On top of that, the Indian sports industry is currently valued at around $2.7 billion '
        'and is on track to hit $10 billion by 2030 thanks to rising incomes, urbanization, and a serious push '
        'from the government to invest in sports infrastructure (KPMG, 2023). What really caught our attention '
        'is the basketball-specific data: the NBA estimates that there are already over 300 million basketball '
        'fans in India, which makes it the NBA’s second-largest fan base outside of the United States. '
        'The demand is clearly there; the infrastructure just has not caught up yet.',
        indent=True)

    add_heading_styled(doc, 'Consumer Behavior Trends', level=2)
    add_body(doc,
        'Young Indian consumers, especially those in the 15–30 range, are more health-conscious than any '
        'previous generation. Gym memberships, fitness apps, and sports participation are all trending upward. '
        'A huge driver of this is India’s digital connectivity—mobile data costs an average of just '
        '$0.17 per GB, which is among the cheapest in the world, and smartphone penetration is through the '
        'roof (Deloitte, 2024). This means young Indians are consuming NBA highlights on YouTube, following '
        'basketball content on Instagram, and engaging with sports brands online at rates that would have been '
        'unthinkable ten years ago. Meanwhile, India’s middle class has grown to over 400 million people, '
        'and parents in this segment are increasingly willing to invest in extracurricular activities for their '
        'kids. They see sports not just as a hobby but as a real pathway to scholarships and personal development. '
        'The success of the Indian Premier League in cricket proved that Indian consumers will passionately '
        'support a well-marketed sporting product, and that blueprint can absolutely be applied to basketball.',
        indent=True)

    add_heading_styled(doc, 'Opportunities and Challenges', level=2)
    add_body(doc,
        'There are several strong tailwinds for entering this market right now. The Indian government’s '
        'Khelo India initiative has poured over $350 million into sports development, including basketball-specific '
        'infrastructure. The NBA already established its Academy India program back in 2017, which validates that '
        'there is international confidence in this market. With 35% of India’s population now living in '
        'cities, there are natural demand centers where a basketball academy can thrive. That said, we have to '
        'be realistic about the challenges. Cricket is king in India, and any sport entering that market is '
        'competing for attention and participation against a deeply entrenched cultural institution. Quality '
        'indoor basketball courts are hard to find outside major cities, and price sensitivity is real—'
        'training programs need to be priced in a way that middle-class families can actually afford. Finally, '
        'India’s regulatory environment varies significantly across its 28 states and 8 union territories, '
        'so a one-size-fits-all approach will not work.',
        indent=True)

    doc.add_page_break()

    # ── THE CONCEPT ──
    add_heading_styled(doc, 'The Concept')
    add_body(doc,
        'HoopRise Basketball Academy is a hybrid basketball training and development company that pairs '
        'high-quality physical training facilities with a digital platform to bring structured basketball '
        'education to young players across India. The plan is to open premium training centers in three major '
        'metro areas—Mumbai, Delhi NCR, and Bangalore—while also launching a mobile app that makes '
        'our training content accessible to players anywhere in the country, even if they are nowhere near one '
        'of our physical locations.',
        indent=True)

    add_body(doc,
        'Each physical academy will have regulation-size indoor courts, a strength and conditioning area, a '
        'sports science lab with motion capture technology, and classrooms for film study and tactical sessions. '
        'We plan to staff each location with certified coaches who have international playing or coaching '
        'experience, along with local assistant coaches who understand the regional dynamics and can connect with '
        'players on a personal level. Training will be split into four tiers—Beginner, Intermediate, '
        'Advanced, and Elite—so we can serve everyone from an 8-year-old picking up a basketball for the '
        'first time to a 22-year-old trying to break into professional play.',
        indent=True)

    add_body(doc,
        'The digital side of HoopRise is just as important. The app will feature AI-powered skill assessments, '
        'a video drill library with demonstrations in multiple Indian languages, performance tracking dashboards, '
        'and virtual coaching sessions. This is where the business really scales, because the biggest gap in '
        'India’s basketball landscape right now is not a lack of interest—it is a lack of structured, '
        'quality training that is actually accessible to most people. If you live in a Tier 2 or Tier 3 city, '
        'your options for basketball coaching are extremely limited. HoopRise solves that problem by putting '
        'world-class training content in the hands of any kid with a smartphone, while still offering the full '
        'in-person experience for those near our academy locations.',
        indent=True)

    doc.add_page_break()

    # ── MISSION STATEMENT ──
    add_heading_styled(doc, 'Mission Statement')
    add_body(doc,
        'HoopRise Basketball Academy exists to make high-level basketball development accessible to young '
        'athletes across India, regardless of where they live or what their family’s income looks like. '
        'Our mission is to build a training ecosystem that combines expert coaching, quality facilities, and '
        'smart technology to develop the next wave of Indian basketball talent. Beyond the sport itself, we '
        'want every player who comes through our program to walk away with stronger discipline, better teamwork '
        'skills, and a real sense of confidence—qualities that carry over into every part of life.',
        indent=True)

    add_body(doc,
        'We have three specific goals driving everything we do. First, we want to build the most recognized '
        'and trusted basketball training brand in India within five years. Second, we want to develop a '
        'legitimate pipeline of players who can compete at the collegiate, national, and international level. '
        'Third, we want to reach one million users on our digital platform within three years of launch. These '
        'are ambitious targets, but we believe they are achievable through a combination of relentless focus on '
        'coaching quality, smart use of technology, and strategic partnerships that give us credibility and '
        'reach from day one.',
        indent=True)

    # ── COMPETITIVE POSITION ──
    add_heading_styled(doc, 'Competitive Position')

    add_heading_styled(doc, 'Target Market Profile', level=2)
    add_body(doc,
        'Our primary target is youth aged 8 to 22 from middle-class and upper-middle-class families in urban '
        'India. We are talking about households with annual incomes between $10,000 and $50,000—families '
        'where parents prioritize education and are increasingly open to investing in structured extracurricular '
        'programs. The kids in this demographic are digitally native, heavily influenced by global sports culture, '
        'and many of them are already watching NBA content online. Our secondary targets include college athletes '
        'looking for advanced training, corporate clients who want basketball-based team-building programs, and '
        'recreational adult players aged 23–35 who play in weekend leagues or just want to stay active.',
        indent=True)

    add_body(doc,
        'Across India’s top 20 cities, there are roughly 120 million young people who fit this profile. '
        'We are starting with Mumbai (21 million metro population), Delhi NCR (32 million), and Bangalore '
        '(13 million) because these cities have the highest concentration of middle-class families, existing '
        'basketball interest, suitable commercial real estate, and strong digital infrastructure. The lifestyle '
        'of our target customer involves heavy social media use, regular consumption of NBA and international '
        'sports content, interest in fitness trends, and a growing openness to sports beyond cricket.',
        indent=True)

    add_heading_styled(doc, 'Key Competitors', level=2)

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
         'Incredible brand recognition; world-class coaching; direct pathway to the NBA',
         'Only takes about 24 players total; one location; not designed for the average player',
         'Niche/Elite'],
        ['Stepanova Basketball\nAcademy',
         'Has an established local presence; affordable pricing; focuses on grassroots',
         'Facilities are limited; no digital component; coaching quality varies a lot',
         'Local/Grassroots'],
        ['Local Municipal\nPrograms',
         'Free or almost free; backed by government; available in many cities',
         'Run-down facilities; coaches often have no formal training; no real curriculum',
         'Mass/Basic'],
        ['International Apps\n(HomeCourt, etc.)',
         'Cutting-edge tech; AI-driven feedback; large global user base',
         'No physical presence in India; English-only; not built for the Indian context',
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
        'The key thing that sets HoopRise apart is our hybrid model, which nobody else in the Indian market '
        'is doing right now. The NBA Academy is elite but inaccessible. Local programs are accessible but low '
        'quality. International apps have great tech but zero local relevance. We sit right in the sweet '
        'spot—premium quality that is still accessible to a wide audience. Here is what specifically '
        'sets us apart:',
        indent=True)

    add_bullet(doc, 'Hybrid Physical-Digital Model: Players get in-person training at our academies plus a '
                    'full mobile app experience, so their development does not stop when they leave the court.')
    add_bullet(doc, 'Data-Driven Development: Our AI-powered performance tracking creates personalized training '
                    'plans based on each player’s actual strengths and weaknesses, not a generic '
                    'one-size-fits-all program.')
    add_bullet(doc, 'Tiered Pricing: We are building in scholarship programs and subsidized digital access '
                    'from the start. Talent should not be gated by income.')
    add_bullet(doc, 'Multilingual Platform: All training content will be available in Hindi, English, Tamil, '
                    'Kannada, and Marathi at launch, because a kid in Bangalore should not have to train in '
                    'a language they are not comfortable in.')
    add_bullet(doc, 'Clear Pathway to Professional Play: We are establishing direct relationships with '
                    'international college programs and professional leagues so that players can see a real '
                    'future in basketball, not just a hobby.')

    doc.add_page_break()

    # ── CULTURAL CONSIDERATIONS ──
    add_heading_styled(doc, 'Cultural Considerations')

    add_heading_styled(doc, 'Family-Centric Decision Making', level=2)
    add_body(doc,
        'In India, parents and often even extended family are the decision makers when it comes to a child’s '
        'extracurricular activities. You cannot just market to the kid; you have to win over the family. That is '
        'why our marketing and enrollment strategies will speak directly to parental priorities. Every piece of '
        'promotional content will emphasize the character-building side of basketball—discipline, time '
        'management, teamwork, leadership—because those are the qualities that resonate with Indian parents. '
        'We will also hold regular open-house events, parent orientation sessions, and send out quarterly progress '
        'reports so families feel genuinely involved in their child’s development. The enrollment process '
        'will treat parents as partners in the journey, not just people writing checks.',
        indent=True)

    add_heading_styled(doc, 'Education-First Culture', level=2)
    add_body(doc,
        'Academics come first in Indian culture, and any sports venture that ignores that reality is going to '
        'fail. We are not fighting that; we are working with it. All training sessions will be scheduled around '
        'school hours, and during board exam seasons (March–April and October–November), we will '
        'offer flexible and reduced schedules so students are not forced to choose between studying and training. '
        'A big part of our pitch to families will be the scholarship angle—we will highlight players who '
        'earned spots at international universities through basketball, showing parents that this is actually '
        'complementary to their child’s education, not competing with it. We even plan to have study '
        'spaces inside each academy facility so that kids can get homework done before or after practice.',
        indent=True)

    add_heading_styled(doc, 'Language and Regional Diversity', level=2)
    add_body(doc,
        'India has 22 officially recognized languages and hundreds of dialects, which means operating in '
        'English alone is not going to cut it. At each academy, coaching will be bilingual—English paired '
        'with the dominant local language (Hindi in Delhi, Marathi in Mumbai, Kannada in Bangalore). The app '
        'will launch with content in five languages, and we will add more based on what users are asking for. '
        'Our marketing will also be localized beyond just language; we will use region-specific cultural '
        'references and sports analogies that actually connect with people in each city rather than running '
        'the same generic national campaign everywhere.',
        indent=True)

    add_heading_styled(doc, 'Religious and Festival Sensitivity', level=2)
    add_body(doc,
        'India is one of the most religiously diverse countries in the world, and the calendar is packed with '
        'festivals—Diwali, Eid, Christmas, Pongal, Holi, Navratri, and many more. Rather than treating '
        'these as scheduling headaches, we plan to use them as opportunities. We will adjust schedules around '
        'major festivals, host themed basketball events during holiday seasons, and use celebrations as moments '
        'to bring together players from different backgrounds. The goal is to make the academy feel like a '
        'space where everyone belongs, and where diversity is something that gets celebrated, not just tolerated.',
        indent=True)

    add_heading_styled(doc, 'Gender Considerations', level=2)
    add_body(doc,
        'Women’s sports participation in urban India is growing fast, but there are still cultural '
        'sensitivities, especially when it comes to mixed-gender athletic settings for teenagers. We are '
        'going to address this head-on by offering dedicated girls-only training sessions led by female '
        'coaches. This makes it much easier for more conservative families to feel comfortable enrolling their '
        'daughters. Our marketing will also prominently feature female basketball role models and lean into '
        'the empowerment narrative, because honestly, the growth potential on the women’s side is '
        'enormous, and we do not want to leave half the market on the table just because we did not think '
        'about these dynamics early enough.',
        indent=True)

    doc.add_page_break()

    # ── FUNDRAISING ──
    add_heading_styled(doc, 'Fundraising/Financing')

    add_body(doc,
        'We estimate that HoopRise needs approximately $900,000 to get through launch and the first year of '
        'operations. Rather than relying on one big investor or a single funding source, we are spreading the '
        'risk across multiple channels. Here is how we plan to raise the capital.',
        indent=True)

    add_heading_styled(doc, 'Angel Investors and Venture Capital', level=2)
    add_body(doc,
        'India’s sports-tech investment scene has been heating up, with firms like Dream Sports, Blume '
        'Ventures, and Sequoia India actively looking for sports-related plays. Our plan is to target a seed '
        'round of around $400,000 from angel investors who have a track record in sports, education, or youth '
        'development. The pitch is straightforward: India has the demographics, the digital infrastructure, and '
        'the growing demand, but nobody has built a scalable hybrid training model yet. HoopRise is that model.',
        indent=True)

    add_heading_styled(doc, 'Government Grants and Initiatives', level=2)
    add_body(doc,
        'The Indian government’s Khelo India program and the Sports Authority of India (SAI) both offer '
        'grants and subsidies to organizations that develop sports infrastructure and increase grassroots '
        'participation. We plan to apply for accreditation as an official training center under these programs, '
        'which could bring in $100,000–$150,000 in direct grants and give us access to government sports '
        'facilities at subsidized rates. Each state—Maharashtra, Delhi, and Karnataka—has its own '
        'sports department with additional funding opportunities, so we will be applying at both the national '
        'and state levels.',
        indent=True)

    add_heading_styled(doc, 'Corporate Sponsorships', level=2)
    add_body(doc,
        'Here is something a lot of people do not realize about India: companies with profits above a certain '
        'threshold are legally required to spend 2% of their net profits on Corporate Social Responsibility '
        '(CSR) initiatives. Sports development and youth empowerment both qualify, which opens the door to '
        'sponsorship from major Indian corporations like the Tata Group, Reliance Industries, and Infosys. '
        'We are going to build tiered sponsorship packages ranging from $25,000 to $200,000, offering brand '
        'visibility across our facilities, our app, and our events. It is a win-win—they need to spend '
        'the money anyway, and we can offer them meaningful brand exposure in a growing space.',
        indent=True)

    add_heading_styled(doc, 'Crowdfunding', level=2)
    add_body(doc,
        'To supplement the larger funding sources, we plan to run a crowdfunding campaign on Ketto (India’s '
        'biggest crowdfunding platform) and Kickstarter with a target of $50,000–$75,000. Beyond the money, '
        'this is really about building a community from day one. The campaign will lean into the social impact '
        'story—democratizing basketball access for kids who would never otherwise get quality coaching—'
        'and backers will get rewards like discounted memberships, exclusive merchandise, and early access to '
        'the app.',
        indent=True)

    doc.add_page_break()

    # ── PROMOTIONAL STRATEGIES ──
    add_heading_styled(doc, 'Promotional Strategies')

    add_heading_styled(doc, 'Digital Marketing Campaigns', level=2)
    add_body(doc,
        'With over 800 million internet users in India, digital is obviously the primary channel. We will run '
        'targeted ad campaigns on Instagram, YouTube, and Facebook built around video content—training '
        'highlights, player transformation stories, and behind-the-scenes looks at academy life. YouTube '
        'pre-roll ads placed before NBA content is a no-brainer since that is exactly where our target audience '
        'already is. On the search side, we will invest in SEO and Google Ads targeting high-intent keywords '
        'like “basketball training India,” “basketball academy near me,” and “learn '
        'basketball.” We will also publish weekly blog posts and video tutorials to build organic traffic '
        'and position HoopRise as the go-to authority on basketball development in India.',
        indent=True)

    add_heading_styled(doc, 'Influencer and Ambassador Partnerships', level=2)
    add_body(doc,
        'We are going to partner with a mix of Indian basketball figures, fitness influencers, and youth-oriented '
        'content creators to get the word out. Top targets include Satnam Singh (the first Indian player ever '
        'drafted by an NBA team), Prachi Tehlan (former national team captain), and some of the bigger fitness '
        'YouTubers whose audiences overlap with our demographic. In each target city, we will also work with '
        'local micro-influencers who have real credibility in their communities. These partnerships will involve '
        'content creation, appearances at academy events, and social media collaborations—all designed to '
        'give us authentic visibility rather than feeling like generic advertising.',
        indent=True)

    add_heading_styled(doc, 'School and University Outreach', level=2)
    add_body(doc,
        'Getting into schools is one of our biggest enrollment drivers. We plan to partner with major school '
        'networks to offer free introductory basketball clinics, donate equipment to schools that start '
        'basketball programs, and sponsor inter-school tournaments. On the university side, we want to become '
        'the preferred training partner for college basketball teams by offering group training packages and '
        'giving teams access to our digital platform for performance analysis. This approach puts us in front '
        'of our exact target audience in an environment where they are already open to learning new things.',
        indent=True)

    add_heading_styled(doc, 'Event Sponsorships and Community Engagement', level=2)
    add_body(doc,
        'Nothing builds a brand like real-world experiences. We will organize three-on-three street tournaments, '
        'holiday basketball camps, and viewing parties during major NBA events like the Finals and All-Star '
        'Weekend. These events let potential customers experience our coaching quality firsthand and get a feel '
        'for the HoopRise community. We also plan to host an annual “HoopRise Rising Stars Challenge” '
        'that will generate media coverage, drive social media engagement, and over time become a marquee event '
        'in India’s basketball calendar. The point is to make HoopRise synonymous with basketball culture '
        'in India, not just another training program.',
        indent=True)

    doc.add_page_break()

    # ── ANTICIPATED BUDGET ──
    add_heading_styled(doc, 'Anticipated Budget')

    add_body(doc,
        'Below is our three-year financial projection. Year 1 is all about getting set up and launching. '
        'Year 2 is focused on growth and gaining traction. By Year 3, we are scaling and hitting profitability.',
        indent=True)

    # Expenses table
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
            if row_idx == 8:
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

    # Revenue table
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
        'The numbers tell a clear story. Year 1 is a net loss as we invest heavily in setup, but revenue ramps '
        'quickly. By the second half of Year 2, we cross into profitability, with the break-even point coming '
        'at roughly 18 months post-launch. Year 3 revenue of $1.45 million against $1.025 million in expenses '
        'gives us a healthy margin, and that is before factoring in the potential for geographic expansion. The '
        'digital platform is the real growth engine here—it scales without the overhead of additional '
        'physical locations.',
        indent=True)

    add_formatted_paragraph(doc, '', size=4, space_after=2)
    doc.add_picture(CHART_PATH, width=Inches(6.2))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # ── STRATEGIC PARTNERSHIPS ──
    add_heading_styled(doc, 'Strategic Partnerships')

    add_body(doc,
        'No startup succeeds in a vacuum, and that is especially true when you are entering a market as '
        'complex as India. The right partnerships give us credibility, resources, and access that would take '
        'years and a lot more money to build on our own. Here are the key partnerships we are targeting and '
        'why each one matters.',
        indent=True)

    add_heading_styled(doc, 'NBA India', level=2)
    add_body(doc,
        'This is the partnership that changes everything. The NBA has already invested significantly in growing '
        'basketball in India through NBA Academy India, Jr. NBA programs, and broadcast deals. We want to '
        'position HoopRise as an official NBA-affiliated training center, which would give us access to their '
        'coaching curriculum, their brand halo, and their scouting network. For our players, this creates a '
        'visible pathway—train at HoopRise, get noticed, potentially earn a spot at the NBA Academy or '
        'get scouted for international opportunities. That is a recruiting pitch that no local competitor can match.',
        indent=True)

    add_heading_styled(doc, 'Nike India / Adidas India', level=2)
    add_body(doc,
        'A sportswear partnership is about more than just getting discounted gear (though that helps too). A '
        'brand like Nike, with its deep roots in basketball culture, would give us co-marketing opportunities, '
        'branded academy uniforms, and potential funding for scholarship programs. In return, Nike gets a '
        'dedicated channel for youth basketball engagement in one of the fastest-growing markets in the world. '
        'We would be putting their products on the next generation of Indian basketball players, which is exactly '
        'the kind of grassroots brand-building that sportswear companies love.',
        indent=True)

    add_heading_styled(doc, 'Basketball Federation of India (BFI)', level=2)
    add_body(doc,
        'Getting official recognition from the BFI gives us institutional legitimacy and connects our players '
        'to the national basketball ecosystem. If we are an accredited training center, our players become '
        'eligible for state and national team selection pathways. We also get access to BFI-organized '
        'tournaments, coaching certification programs, and government sports facilities. For the BFI, the '
        'value is clear—we are doing the grassroots development and talent identification work that '
        'strengthens the entire basketball pipeline in India.',
        indent=True)

    add_heading_styled(doc, 'Indian School and University Networks', level=2)
    add_body(doc,
        'Partnering with major school networks like Delhi Public School (DPS), Amity International, and Ryan '
        'International lets us embed HoopRise directly into the education ecosystem where our target customers '
        'already are. These partnerships would include after-school basketball programs at school facilities, '
        'discounted enrollment for partner school students, and sponsored inter-school tournaments. On the '
        'university side, we are targeting schools like Christ University in Bangalore, Shiv Nadar University '
        'in Delhi, and NMIMS in Mumbai for collegiate basketball development programs, internship pipelines, '
        'and sports management collaborations.',
        indent=True)

    add_heading_styled(doc, 'Technology Partners', level=2)
    add_body(doc,
        'Building and scaling a digital platform is expensive, but the right tech partnerships can cut those '
        'costs dramatically. We are looking at collaborations with Indian IT firms like Infosys or Wipro for '
        'platform development, AWS India for cloud infrastructure (they have a solid startup credits program), '
        'and sports tech companies like ShotTracker for performance analytics integration. These partnerships '
        'keep our development costs manageable while making sure the tech we deliver is genuinely world-class.',
        indent=True)

    doc.add_page_break()

    # ── REFERENCES ──
    add_heading_styled(doc, 'References')

    references = [
        'Deloitte. (2024). India’s digital sports consumption: Trends and opportunities in a '
        'mobile-first market. Deloitte Touche Tohmatsu India LLP.',

        'KPMG. (2023). The business of sports: A comprehensive analysis of India’s evolving sports '
        'industry landscape. KPMG India.',

        'National Basketball Association. (2024). NBA global outreach report: Expanding basketball culture '
        'in emerging markets. NBA Communications.',

        'Sports Authority of India. (2023). Khelo India annual report 2022–2023: Building a sporting '
        'nation through grassroots development. Ministry of Youth Affairs and Sports, Government of India.',

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

    doc.save(DOC_PATH)
    print(f"Document saved: {DOC_PATH}")


if __name__ == '__main__':
    generate_budget_chart()
    print(f"Chart saved: {CHART_PATH}")
    build_document()
