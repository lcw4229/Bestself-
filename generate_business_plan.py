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
        'India jumped out at us right away. We spent weeks looking at markets in Southeast Asia, '
        'parts of Africa, and even Eastern Europe, but the numbers in India were impossible to ignore. '
        'The country has 1.44 billion people. That alone is wild. But what makes it truly special for '
        'basketball is the age breakdown: about 65% of the population falls under 35, and the median '
        'age is just 28.4 (United Nations, 2024). So you have this enormous young population that is '
        'growing up in a more connected, more globally influenced world than any Indian generation '
        'before them.',
        indent=True)

    add_body(doc,
        'The broader sports industry in India sits at roughly $2.7 billion right now and analysts '
        'expect it to crack $10 billion by 2030 (KPMG, 2023). Rising incomes, more people moving to '
        'cities, and a government that is finally putting real money behind sports are all feeding that '
        'growth. But here is the stat that got us most excited: the NBA says it has over 300 million '
        'fans in India, making it their second biggest market outside the U.S. Three hundred million '
        'fans, and barely any structured training infrastructure to serve them. That gap is exactly '
        'where HoopRise fits in.',
        indent=True)

    add_heading_styled(doc, 'Consumer Behavior Trends', level=2)
    add_body(doc,
        'Indian kids between 15 and 30 are not the same consumers their parents were. They work out '
        'more. They follow NBA players on Instagram. They watch highlight reels at 2 a.m. A huge reason '
        'for this shift is how cheap mobile data has gotten in India, averaging around $0.17 per GB, '
        'which is basically nothing (Deloitte, 2024). Smartphones are everywhere, and that means sports '
        'content consumption has gone through the roof in the last five or six years.',
        indent=True)

    add_body(doc,
        'On the family side, India\'s middle class has ballooned to over 400 million people. Parents '
        'in this bracket are spending more on their kids\' activities outside of school. They want their '
        'children doing something productive after classes, and they are increasingly open to sports, '
        'not just tutoring. The Indian Premier League showed everyone that Indians will throw their '
        'full passion behind a well-packaged sport product. Cricket did it first. Basketball can be next.',
        indent=True)

    add_heading_styled(doc, 'Opportunities and Challenges', level=2)
    add_body(doc,
        'The timing for this kind of venture is genuinely good. The government\'s Khelo India program '
        'has funneled over $350 million into sports development. The NBA opened its own academy in India '
        'back in 2017, which tells you that serious institutional money already believes in this market. '
        'And with 35% of the country now living in cities, you have dense pockets of demand ready to '
        'be tapped.',
        indent=True)

    add_body(doc,
        'But we are not naive about the obstacles. Cricket runs deep in Indian culture. It is not just '
        'a sport there; it is almost a religion. Any basketball venture is fighting for attention against '
        'that. Quality indoor courts are rare outside major metros. Price sensitivity matters a lot '
        'because even middle-class families watch their budgets carefully. And India\'s regulatory setup '
        'varies wildly across 28 states and 8 union territories, so what works in Mumbai might not fly '
        'in Chennai without adjustments. We have thought about all of this, and the plan accounts for it.',
        indent=True)

    doc.add_page_break()

    # ── THE CONCEPT ──
    add_heading_styled(doc, 'The Concept')
    add_body(doc,
        'HoopRise is a basketball training company built around one core idea: pair real, physical '
        'academy locations with a strong digital platform so that quality coaching reaches as many young '
        'players as possible. We are opening training centers in Mumbai, Delhi NCR, and Bangalore. At '
        'the same time, we are building a mobile app that brings our training methods to kids in any '
        'city, any town, anywhere in India.',
        indent=True)

    add_body(doc,
        'The academies themselves will have full-size indoor courts, weight rooms, sports science labs '
        'with motion capture tech, and film rooms for breaking down game footage. We plan on hiring '
        'coaches with international backgrounds (playing or coaching overseas) and pairing them with '
        'local assistants who actually know the community and can relate to the kids. Training runs on '
        'four levels: Beginner, Intermediate, Advanced, and Elite. That way an 8-year-old just learning '
        'to dribble and a 21-year-old gunning for a pro tryout can both find a program that fits.',
        indent=True)

    add_body(doc,
        'The app is honestly where this business gets really interesting from a growth perspective. It '
        'will have AI skill assessments, a video drill library filmed in multiple Indian languages, stat '
        'tracking, and virtual coaching sessions. Right now, if you are a kid in a Tier 2 or Tier 3 '
        'Indian city and you want serious basketball coaching, your options are basically zero. HoopRise '
        'changes that. A smartphone and an internet connection become your access point to training '
        'content that used to only exist in a handful of elite programs. Meanwhile, players near our '
        'academy cities still get the full in-person experience. That combination is something nobody '
        'else in India is offering.',
        indent=True)

    doc.add_page_break()

    # ── MISSION STATEMENT ──
    add_heading_styled(doc, 'Mission Statement')
    add_body(doc,
        'We started HoopRise because we believe that where you grow up or how much your family makes '
        'should not decide whether you get good basketball coaching. Our mission is straightforward: '
        'build the best basketball training program in India by combining great coaches, solid '
        'facilities, and smart technology, then make it accessible to as many young players as we '
        'possibly can. We also care about what basketball teaches beyond the court. Discipline. '
        'Accountability. How to work with people who are different from you. Those things matter just '
        'as much as a jump shot.',
        indent=True)

    add_body(doc,
        'Three goals sit at the center of everything. First, we want HoopRise to be the name people '
        'think of when they think of basketball training in India, and we want that within five years. '
        'Second, we want to build a real pipeline of players who go on to compete in college programs, '
        'national teams, and professional leagues. Third, we want one million users on the app within '
        'three years. Those are big numbers. We know that. But the market is big, the demand is real, '
        'and we have a plan for each one.',
        indent=True)

    # ── COMPETITIVE POSITION ──
    add_heading_styled(doc, 'Competitive Position')

    add_heading_styled(doc, 'Target Market Profile', level=2)
    add_body(doc,
        'We are going after kids and young adults between 8 and 22, mostly from middle-class and '
        'upper-middle-class families in Indian cities. These are households pulling in roughly $10,000 '
        'to $50,000 a year, where parents care a lot about education but are starting to see sports as '
        'part of the picture too. The young people in this group grew up online. They watch the NBA. '
        'They follow basketball culture. A lot of them already want to play; they just do not have '
        'anywhere good to train.',
        indent=True)

    add_body(doc,
        'Our secondary market includes college athletes who need better coaching, companies looking for '
        'team-building activities, and adults in their twenties and thirties who play recreational '
        'basketball on weekends. Across India\'s 20 biggest cities, about 120 million young people fit '
        'our target profile. We are launching in Mumbai (21 million metro), Delhi NCR (32 million), and '
        'Bangalore (13 million) because that is where middle-class density, basketball interest, and '
        'commercial infrastructure overlap the most.',
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
         'Massive brand power; elite coaches; direct NBA scouting pipeline',
         'Accepts maybe 24 kids total; single location; completely unreachable for the average player',
         'Niche/Elite'],
        ['Stepanova Basketball\nAcademy',
         'Been around a while; priced low; focused on grassroots',
         'Small, cramped facilities; no app or digital tools; coaching quality is inconsistent',
         'Local/Grassroots'],
        ['Local Municipal\nPrograms',
         'Free or nearly free; government backed; exist in many cities',
         'Courts are falling apart; coaches rarely have real credentials; no structured program at all',
         'Mass/Basic'],
        ['International Apps\n(HomeCourt, etc.)',
         'Strong tech; AI analysis; big global user numbers',
         'Nobody on the ground in India; English only; built for American and European users, not Indians',
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
        'The reason HoopRise works where others fall short comes down to one thing: nobody else is '
        'combining physical academies with a full digital training product in the Indian market. The '
        'NBA Academy is world-class but only serves a tiny handful of kids. Local programs are open to '
        'everyone but the quality is awful. International apps have great technology but they were not '
        'designed with India in mind at all.',
        indent=True)

    add_body(doc,
        'We sit right between all of those. Premium enough to actually develop real talent. Accessible '
        'enough that a regular middle-class family can afford it. Our specific advantages break down '
        'like this:',
        indent=True)

    add_bullet(doc, 'Physical plus Digital: Train at the academy, then keep working at home through the '
                    'app. Development does not stop when practice ends.')
    add_bullet(doc, 'Personalized Training Plans: The AI tracks what each player is good at and where '
                    'they struggle, then adjusts their program accordingly. No cookie-cutter drills.')
    add_bullet(doc, 'Tiered Pricing with Scholarships: We built financial aid into the model from day '
                    'one. A talented kid should not get shut out because of money.')
    add_bullet(doc, 'Multilingual Content: The app launches in Hindi, English, Tamil, Kannada, and '
                    'Marathi. A kid in Bangalore deserves to train in a language that feels natural to them.')
    add_bullet(doc, 'A Real Path Forward: We are building direct connections with international college '
                    'programs and pro leagues so players can actually see where basketball might take them.')

    doc.add_page_break()

    # ── CULTURAL CONSIDERATIONS ──
    add_heading_styled(doc, 'Cultural Considerations')

    add_heading_styled(doc, 'Family-Centric Decision Making', level=2)
    add_body(doc,
        'Indian families make decisions together. Period. If a kid wants to join a basketball program, '
        'the parents need to be convinced, and sometimes grandparents weigh in too. So our marketing '
        'cannot just be cool dunk videos targeting teenagers. We have to speak directly to what parents '
        'care about: will this make my child more disciplined? Will it teach them to manage their time? '
        'Will it help with college?',
        indent=True)

    add_body(doc,
        'Every promotional piece we put out will hit those points hard. We will also run open-house days '
        'where families can come see the facility, meet the coaches, and ask questions. Quarterly '
        'progress reports go home to parents. The whole enrollment process treats the family as a '
        'partner. If the parents do not feel like they are part of this, the kid does not sign up. '
        'Simple as that.',
        indent=True)

    add_heading_styled(doc, 'Education-First Culture', level=2)
    add_body(doc,
        'Academics are sacred in India. If a parent has to choose between tutoring and basketball, '
        'basketball loses every single time. We are not trying to fight that. Instead, we work around '
        'it. Practice times run outside of school hours. During board exam season (March through April, '
        'and again in October and November), we scale back sessions and offer flexible scheduling. We '
        'will also push the scholarship angle constantly, showing families real examples of basketball '
        'players who got into international universities on athletic scholarships. And every academy '
        'will have a study area where kids can do homework before or after practice, because that small '
        'detail sends a message: we take their education seriously too.',
        indent=True)

    add_heading_styled(doc, 'Language and Regional Diversity', level=2)
    add_body(doc,
        'Twenty-two official languages. Hundreds of dialects. India is not one market; it is dozens of '
        'markets stitched together. Running an English-only operation would cut us off from a huge '
        'number of potential players and families. Our coaches will work bilingually at each location: '
        'English plus Hindi in Delhi, English plus Marathi in Mumbai, English plus Kannada in Bangalore. '
        'The app launches in five languages with more added based on user demand. Marketing gets '
        'localized too, not just translated. We will use references and cultural touchpoints that '
        'actually mean something in each city instead of running one national campaign and hoping it '
        'lands everywhere.',
        indent=True)

    add_heading_styled(doc, 'Religious and Festival Sensitivity', level=2)
    add_body(doc,
        'Diwali. Eid. Christmas. Holi. Pongal. Navratri. The festival calendar in India is packed, and '
        'these celebrations are deeply important to families. We are building our yearly schedule around '
        'them, not in spite of them. When a major festival hits, we adjust training schedules. During '
        'holiday seasons, we will host themed basketball events that bring together players from '
        'different communities. Honestly, festivals are an opportunity to make the academy feel like a '
        'place where every kid belongs, regardless of their background. That sense of inclusion is not '
        'just nice to have; it is essential for long-term retention in a country this diverse.',
        indent=True)

    add_heading_styled(doc, 'Gender Considerations', level=2)
    add_body(doc,
        'Women\'s sports in urban India are growing, but cultural hesitation around mixed-gender '
        'athletics (especially for teenagers) is still very real. Some families will not enroll their '
        'daughters in a program where they train alongside boys. We are going to offer dedicated '
        'sessions for girls, coached by women. That removes the barrier for families who would '
        'otherwise say no.',
        indent=True)

    add_body(doc,
        'Our marketing will feature female players prominently, not as an afterthought but as a central '
        'part of the brand. Frankly, the business case is obvious too. If we ignore this, we are '
        'voluntarily giving up access to half the market. We would rather get it right from the start.',
        indent=True)

    doc.add_page_break()

    # ── FUNDRAISING ──
    add_heading_styled(doc, 'Fundraising/Financing')

    add_body(doc,
        'Getting HoopRise off the ground and through year one will cost about $900,000. That covers '
        'facilities, staff, tech development, marketing, and a contingency buffer. We are not putting '
        'all our eggs in one basket with funding. The plan spreads across four sources.',
        indent=True)

    add_heading_styled(doc, 'Angel Investors and Venture Capital', level=2)
    add_body(doc,
        'The sports-tech investment scene in India has picked up real momentum lately. Firms like Dream '
        'Sports, Blume Ventures, and Sequoia India have all been putting money into sports-related '
        'startups. We are targeting a seed round of roughly $400,000 from angels who have a background '
        'in sports, education, or youth programs. The pitch writes itself: India has the biggest young '
        'population on the planet, basketball fandom is exploding, and nobody has built a scalable '
        'hybrid training model there yet. That is the opening we are walking through.',
        indent=True)

    add_heading_styled(doc, 'Government Grants and Initiatives', level=2)
    add_body(doc,
        'India\'s Khelo India program and the Sports Authority of India both hand out grants to '
        'organizations that build sports infrastructure and grow participation at the grassroots level. '
        'We are applying for accreditation as an official training center, which could unlock $100,000 '
        'to $150,000 in grants and get us discounted access to government-owned sports facilities. '
        'Maharashtra, Delhi, and Karnataka each have their own state-level sports funding too, so we '
        'will be applying at multiple levels simultaneously.',
        indent=True)

    add_heading_styled(doc, 'Corporate Sponsorships', level=2)
    add_body(doc,
        'This is one of those details about India that most people outside the country do not know. '
        'Indian companies above a certain profit threshold are legally required to spend 2% of net '
        'profits on social responsibility initiatives. Youth sports and empowerment programs qualify. '
        'That opens the door to sponsorship conversations with the Tata Group, Reliance, Infosys, and '
        'others who need to spend that money somewhere. We are building tiered sponsorship packages '
        'from $25,000 to $200,000 that give brands visibility at our academies, on the app, and at '
        'events. They get genuine exposure in a growing space. We get funded. It works for both sides.',
        indent=True)

    add_heading_styled(doc, 'Crowdfunding', level=2)
    add_body(doc,
        'We are also planning a crowdfunding campaign on Ketto (India\'s largest platform for this) and '
        'Kickstarter, aiming for $50,000 to $75,000. Honestly, the crowdfunding piece is about more '
        'than just money. It builds a community of early supporters who feel personally invested in '
        'HoopRise before we even open the doors. Backers get discounted memberships, exclusive merch, '
        'and early app access. The campaign tells the story of what we are trying to do for kids who '
        'would never otherwise get real basketball coaching, and that kind of narrative travels well '
        'on social media.',
        indent=True)

    doc.add_page_break()

    # ── PROMOTIONAL STRATEGIES ──
    add_heading_styled(doc, 'Promotional Strategies')

    add_heading_styled(doc, 'Digital Marketing Campaigns', level=2)
    add_body(doc,
        'India has over 800 million internet users, so digital is the obvious primary channel. We will '
        'run targeted ads on Instagram, YouTube, and Facebook, all built around video. Training clips, '
        'player progress stories, behind-the-scenes content from the academy. YouTube pre-roll ads '
        'placed before NBA videos make a lot of sense because that is literally where our audience is '
        'already spending their time.',
        indent=True)

    add_body(doc,
        'On the search side, we will invest in SEO and Google Ads around high-intent terms like '
        '"basketball training India" and "basketball academy near me." Weekly blog posts and tutorial '
        'videos will build organic reach over time and make HoopRise the name that keeps showing up '
        'whenever someone searches for basketball development content in India.',
        indent=True)

    add_heading_styled(doc, 'Influencer and Ambassador Partnerships', level=2)
    add_body(doc,
        'We want real faces attached to this brand, not just a logo. Top targets include Satnam Singh '
        '(first Indian ever drafted by an NBA team), Prachi Tehlan (former national team captain), and '
        'several fitness-focused YouTubers whose audiences line up with our demographic. In each city '
        'we are also going to work with local micro-influencers, people with maybe 50,000 to 200,000 '
        'followers who have genuine credibility in their communities. These are not going to be stiff '
        'endorsement deals. We want content collaborations, appearances at our events, and social media '
        'partnerships that feel authentic rather than forced.',
        indent=True)

    add_heading_styled(doc, 'School and University Outreach', level=2)
    add_body(doc,
        'Schools are where our customers already are, five days a week. We plan to partner with school '
        'networks to run free introductory basketball clinics, give away equipment to schools that start '
        'basketball programs, and sponsor inter-school tournaments. On the college side, we want to be '
        'the go-to training partner for university basketball teams, offering group packages and access '
        'to the app\'s analytics tools. This puts us directly in front of the exact kids we are trying '
        'to reach, in a setting where they are already open to trying something new.',
        indent=True)

    add_heading_styled(doc, 'Event Sponsorships and Community Engagement', level=2)
    add_body(doc,
        'You can run all the online ads you want, but there is no substitute for people actually '
        'experiencing your product. We are going to organize 3-on-3 street tournaments, basketball '
        'camps during school breaks, and watch parties for the NBA Finals and All-Star Weekend. Once a '
        'year, we will run a "HoopRise Rising Stars Challenge" that becomes the big annual event, gets '
        'press coverage, and gives the brand a signature moment on the calendar. The goal is to make '
        'HoopRise feel like the center of basketball culture in India, not just another place to take '
        'lessons.',
        indent=True)

    doc.add_page_break()

    # ── ANTICIPATED BUDGET ──
    add_heading_styled(doc, 'Anticipated Budget')

    add_body(doc,
        'Here is the financial picture across three years. Year 1 is setup and launch. Year 2 is '
        'growth. Year 3 is when we start making real money.',
        indent=True)

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
        'Year 1 is a loss. We knew that going in. Heavy upfront investment in facilities, tech, and '
        'staffing means we are spending far more than we are bringing in. But revenue climbs fast. By '
        'the back half of Year 2, we cross into the black, with a break-even point at about 18 months. '
        'Year 3 brings in $1.45 million against $1.025 million in costs, which gives us room to breathe '
        'and reinvest. The app is the real engine here because it scales without requiring us to lease '
        'more buildings or hire proportionally more staff for every new user.',
        indent=True)

    add_formatted_paragraph(doc, '', size=4, space_after=2)
    doc.add_picture(CHART_PATH, width=Inches(6.2))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # ── STRATEGIC PARTNERSHIPS ──
    add_heading_styled(doc, 'Strategic Partnerships')

    add_body(doc,
        'We could try to build everything from scratch. But honestly, that would be slow, expensive, '
        'and unnecessary. The smarter play is to partner with organizations that already have what we '
        'need (credibility, infrastructure, reach) and offer them something valuable in return. Here '
        'are the five partnerships we are going after.',
        indent=True)

    add_heading_styled(doc, 'NBA India', level=2)
    add_body(doc,
        'This one is the biggest. If we can get affiliated with the NBA, everything else becomes '
        'easier. They have already put real money into Indian basketball through the NBA Academy, '
        'Jr. NBA programs, and broadcast deals. What we want is recognition as an official '
        'NBA-affiliated training center. That gives us access to their coaching playbooks, their brand '
        'credibility, and their scouting network. For our players, it means a visible ladder: train at '
        'HoopRise, perform well, get noticed by NBA scouts or earn a look from the Academy. No local '
        'competitor can offer anything close to that.',
        indent=True)

    add_heading_styled(doc, 'Nike India / Adidas India', level=2)
    add_body(doc,
        'A partnership with a major sportswear brand does a few things at once. We get quality gear at '
        'better prices. We get co-branded marketing campaigns. And we potentially unlock funding for '
        'scholarship programs. Nike is our first choice because of their history with basketball, but '
        'Adidas would work too. From their perspective, they get a direct channel into India\'s next '
        'generation of basketball players. They get their products on kids in a market that is only '
        'getting bigger. That is the kind of grassroots brand-building that these companies spend '
        'millions trying to create organically.',
        indent=True)

    add_heading_styled(doc, 'Basketball Federation of India (BFI)', level=2)
    add_body(doc,
        'BFI recognition gives us something money cannot buy: institutional credibility. If we are an '
        'accredited center, our players can be eligible for state and national team selection. We get '
        'access to BFI tournaments, coaching certifications, and government sports venues. And for the '
        'BFI, we are basically doing their grassroots work for them, finding talent and developing '
        'players who feed into the national pipeline. It is a relationship that makes both sides '
        'stronger.',
        indent=True)

    add_heading_styled(doc, 'Indian School and University Networks', level=2)
    add_body(doc,
        'We want to be inside the schools. Partnering with networks like Delhi Public School, Amity '
        'International, and Ryan International lets us run after-school basketball programs on their '
        'campuses, offer discounted enrollment to their students, and sponsor inter-school tournaments. '
        'For universities, we are targeting Christ University in Bangalore, Shiv Nadar in Delhi, and '
        'NMIMS in Mumbai. These partnerships give us access to the exact age group we want, in the '
        'exact places where they spend most of their time. It does not get much more targeted than that.',
        indent=True)

    add_heading_styled(doc, 'Technology Partners', level=2)
    add_body(doc,
        'Building a good app costs a lot of money. Building a great app costs even more. Tech '
        'partnerships help close that gap. We are looking at Indian IT firms like Infosys or Wipro for '
        'platform development work, AWS India for cloud hosting (their startup credits program is '
        'genuinely helpful for early-stage companies), and sports tech outfits like ShotTracker for '
        'performance analytics features. These partnerships bring our development costs down while '
        'keeping the product quality high, which matters a lot when you are trying to compete with '
        'polished international apps on a startup budget.',
        indent=True)

    doc.add_page_break()

    # ── REFERENCES ──
    add_heading_styled(doc, 'References')

    references = [
        'Deloitte. (2024). India\'s digital sports consumption: Trends and opportunities in a '
        'mobile-first market. Deloitte Touche Tohmatsu India LLP.',

        'KPMG. (2023). The business of sports: A comprehensive analysis of India\'s evolving sports '
        'industry landscape. KPMG India.',

        'National Basketball Association. (2024). NBA global outreach report: Expanding basketball '
        'culture in emerging markets. NBA Communications.',

        'Sports Authority of India. (2023). Khelo India annual report 2022-2023: Building a sporting '
        'nation through grassroots development. Ministry of Youth Affairs and Sports, Government of '
        'India.',

        'United Nations Department of Economic and Social Affairs. (2024). World population prospects '
        '2024: India demographic profile summary. United Nations Publications.',
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
