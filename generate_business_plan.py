#!/usr/bin/env python3
"""Generate International Sport Business Plan as a Word document (academic paper format)."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
CHART_PATH = os.path.join(OUTPUT_DIR, "budget_chart.png")
DOC_PATH = os.path.join(OUTPUT_DIR, "International_Sport_Business_Plan.docx")

BLACK = RGBColor(0x00, 0x00, 0x00)


def set_cell_shading(cell, color_hex):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color_hex)
    shading.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading)


def set_line_spacing(paragraph, pt=24):
    pf = paragraph.paragraph_format
    pf.line_spacing = Pt(pt)


def add_body(doc, text, indent=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.5)
    set_line_spacing(p)
    run = p.add_run(text)
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'
    run.font.color.rgb = BLACK
    return p


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(12)
    set_line_spacing(p)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'
    run.font.color.rgb = BLACK
    return p


def add_subsection_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(12)
    set_line_spacing(p)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'
    run.font.color.rgb = BLACK
    return p


def add_bullet(doc, label, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.left_indent = Inches(0.5)
    set_line_spacing(p)
    run_b = p.add_run(label + ': ')
    run_b.bold = True
    run_b.font.size = Pt(12)
    run_b.font.name = 'Times New Roman'
    run_b.font.color.rgb = BLACK
    run_t = p.add_run(text)
    run_t.font.size = Pt(12)
    run_t.font.name = 'Times New Roman'
    run_t.font.color.rgb = BLACK


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
    colors = ['#333333', '#777777', '#AAAAAA']

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
    axes[1].bar(x2 - width2/2, [v/1000 for v in revenue], width2, label='Revenue', color='#555555', edgecolor='white', linewidth=0.5)
    axes[1].bar(x2 + width2/2, [v/1000 for v in expenses], width2, label='Total Expenses', color='#BBBBBB', edgecolor='white', linewidth=0.5)

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
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = BLACK

    # ── COVER PAGE ──
    for _ in range(6):
        p = doc.add_paragraph()
        set_line_spacing(p)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_line_spacing(p)
    run = p.add_run('HoopRise Basketball Academy')
    run.bold = True
    run.font.size = Pt(16)
    run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_line_spacing(p)
    run = p.add_run('International Sport Business Plan')
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_line_spacing(p)
    run = p.add_run('Expanding Youth Basketball Development in India')
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

    for _ in range(3):
        p = doc.add_paragraph()
        set_line_spacing(p)

    for line in ['Landon Worrich', 'SPMT 337: International Sport Business', 'June 2026']:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_line_spacing(p)
        run = p.add_run(line)
        run.font.size = Pt(12)
        run.font.name = 'Times New Roman'

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════
    # MARKET RESEARCH SUMMARY (1 page)
    # ══════════════════════════════════════════════════════════
    add_section_heading(doc, 'Market Research Summary')

    add_body(doc,
        'India stands out as the strongest target market for a basketball training venture. '
        'With 1.44 billion people and roughly 65% of the population under age 35, it\'s one of '
        'the youngest countries on earth (United Nations, 2024). The sports industry sits at '
        'about $2.7 billion and is projected to reach $10 billion by 2030 (KPMG, 2023). The NBA '
        'already counts over 300 million fans in India, making it their second-largest market '
        'outside the U.S., yet there\'s almost no structured training infrastructure to serve '
        'that demand.')

    add_body(doc,
        'Consumer behavior backs this up. Cheap mobile data at $0.17 per GB has put smartphones '
        'in nearly every hand, and young Indians are consuming NBA highlights, fitness content, '
        'and sports media constantly (Deloitte, 2024). India\'s middle class has grown past 400 '
        'million, and these families are increasingly open to investing in their kids\' athletic '
        'development alongside academics.')

    add_body(doc,
        'The opportunities are strong. The government\'s Khelo India program has invested over '
        '$350 million in grassroots sports, and the NBA opened its own academy in India in 2017. '
        'Urbanization is concentrating demand in major metros. The challenges are real too: '
        'cricket dominates the cultural landscape, quality indoor facilities are scarce, families '
        'are price-sensitive, and India\'s 28 states each have different regulations and norms. '
        'But the gap between basketball interest and basketball infrastructure creates a clear '
        'opening for a well-positioned training company.')

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════
    # BUSINESS PLAN (8-10 pages, sections flow continuously)
    # ══════════════════════════════════════════════════════════

    # ── THE CONCEPT ──
    add_section_heading(doc, 'The Concept')
    add_body(doc,
        'HoopRise is pretty simple at its core. I\'m building real basketball academies in '
        'three major Indian cities (Mumbai, Delhi NCR, Bangalore), and I\'m pairing those with '
        'a mobile app that brings my training to anyone with a phone and a Wi-Fi connection. '
        'Physical locations for the kids who can get there. A digital product for the millions '
        'who can\'t.')

    add_body(doc,
        'The academies will have full-size courts, weight rooms, sports science labs with motion '
        'capture, and film rooms for game breakdown. Coaches will be people who\'ve played or '
        'coached internationally, paired with local assistants who know the area and can actually '
        'relate to the kids. Training splits into four tiers: Beginner, Intermediate, Advanced, '
        'Elite. An 8-year-old who\'s never held a ball and a 21-year-old trying to go pro both '
        'need a place to train. I want to be that place for both of them.')

    add_body(doc,
        'The app is where things get exciting from a business standpoint. AI skill assessments, '
        'drill videos in multiple Indian languages, stat tracking, virtual coaching. If you\'re a '
        'kid in, say, Jaipur or Indore right now and you want real basketball coaching? Good '
        'luck. There\'s basically nothing. That\'s the gap I\'m filling. The app makes quality '
        'training available to anyone with a phone, while the physical academies give the full '
        'experience to players in my three launch cities. Nobody else in India is doing both.')

    # ── MISSION STATEMENT ──
    add_section_heading(doc, 'Mission Statement')
    add_body(doc,
        'Where you grow up shouldn\'t decide if you get a good coach. How much money your family '
        'has shouldn\'t either. That\'s the whole idea behind HoopRise. I want to build India\'s '
        'best basketball training program and then make it available to as many young players as '
        'I can, not just the ones in wealthy families or the right zip code. And it\'s not only '
        'about basketball. The discipline, the accountability, learning to work with people who '
        'are different from you, all of that matters just as much as getting your shot right.')

    add_body(doc,
        'I\'ve got three goals. One: become the name people think of when Indian basketball '
        'training comes up, within five years. Two: build a real pipeline of players who end up '
        'in college programs, national teams, or pro leagues. Three: get to a million app users '
        'in three years. Big numbers. I know. But India\'s young population is massive, the '
        'interest is there, and nobody\'s really going after this market with a serious plan yet. '
        'So I\'m going for it.')

    # ── COMPETITIVE POSITION ──
    add_section_heading(doc, 'Competitive Position')

    add_subsection_heading(doc, 'Target Market Profile')
    add_body(doc,
        'Main target is 8-to-22-year-olds from middle-class and upper-middle-class families in '
        'Indian cities. Households making $10,000 to $50,000 a year, give or take. Parents who '
        'value education but are starting to realize sports can be part of the picture too. The '
        'kids themselves grew up on the internet. They watch the NBA. A lot of them already want '
        'to play. They just don\'t have a good place to do it.')

    add_body(doc,
        'Beyond that, there\'s a secondary market: college athletes who want better coaching, '
        'companies interested in team-building stuff, and adults in their twenties and thirties '
        'who play pickup on weekends. About 120 million young people across India\'s top 20 '
        'cities fit my core profile. I\'m starting in Mumbai (21 million metro area), Delhi '
        'NCR (32 million), and Bangalore (13 million) because those three have the best overlap '
        'of middle-class population, basketball interest, and available real estate for facilities.')

    add_subsection_heading(doc, 'Key Competitors')

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
        run.font.size = Pt(11)
        run.font.name = 'Times New Roman'
        run.font.color.rgb = BLACK
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    competitors = [
        ['NBA Academy India',
         'Huge brand; world-class coaches; players can get scouted by the NBA directly',
         'Takes like 24 kids. Total. One single location. If you\'re not already elite, forget it.',
         'Niche/Elite'],
        ['Stepanova Basketball Academy',
         'Been around for a while; cheap; grassroots focused',
         'Tiny facilities; no app or tech; some coaches are great, others not so much',
         'Local/Grassroots'],
        ['Local Municipal Programs',
         'Free or close to it; government funded; available in lots of cities',
         'Courts in rough shape; coaches who often have zero formal training; no curriculum',
         'Mass/Basic'],
        ['International Apps (HomeCourt, etc.)',
         'Solid tech; AI feedback; big global user base',
         'No one on the ground in India; English only; designed for Americans, not Indians',
         'Digital/Global'],
    ]

    for row_idx, comp in enumerate(competitors, 1):
        for col_idx, val in enumerate(comp):
            cell = table.rows[row_idx].cells[col_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(10)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = BLACK

    add_body(doc, '', indent=False)

    add_subsection_heading(doc, 'Competitive Differentiation')
    add_body(doc,
        'Look at that table and the gap is pretty obvious. The NBA Academy? Amazing, but it '
        'serves a couple dozen kids. Municipal programs? Open to everyone, but the quality is '
        'rough. Apps like HomeCourt? Cool tech, zero connection to India. Nobody\'s doing both '
        'the physical and digital side in this market. That\'s the lane HoopRise is taking.')

    add_body(doc,
        'Premium enough to actually develop real players, but priced so a normal family can '
        'swing it. Specifically, here\'s what separates me:', indent=False)

    add_bullet(doc, 'Physical plus Digital', 'Train at the academy, keep working through the app '
                    'at home. The learning doesn\'t end when you walk out the door.')
    add_bullet(doc, 'Personalized Plans', 'AI tracks what each player\'s good at and what they\'re '
                    'struggling with, then adjusts. No one\'s running the same generic drills.')
    add_bullet(doc, 'Scholarships Built In', 'Financial aid was part of the model from the start. '
                    'If a kid\'s talented, money shouldn\'t be what stops them.')
    add_bullet(doc, 'Multilingual', 'App launches in Hindi, English, Tamil, Kannada, and Marathi. '
                    'Players should be able to train in a language they actually think in.')
    add_bullet(doc, 'A Real Path Forward', 'Direct connections to international college programs '
                    'and pro leagues. Not vague promises, actual relationships.')

    # ── CULTURAL CONSIDERATIONS ──
    add_section_heading(doc, 'Cultural Considerations')

    add_subsection_heading(doc, 'Family-Centric Decision Making')
    add_body(doc,
        'In India, the kid doesn\'t decide to join a basketball program. The family does. '
        'Sometimes it\'s mom and dad. Sometimes it\'s grandparents. Sometimes an uncle has '
        'opinions. That means my marketing can\'t just be highlight reels and cool branding '
        'aimed at teenagers. I have to answer the questions parents are actually asking: Will '
        'this help my kid\'s discipline? Will it teach them time management? Could this lead to '
        'a college scholarship?')

    add_body(doc,
        'So every piece of marketing hits those points. I\'ll run open-house days where '
        'families can walk through the facility, talk to coaches, ask whatever they want. Parents '
        'get quarterly progress reports. The whole signup process is designed to make them feel '
        'like they\'re part of this, not just the ones paying for it. If the parents aren\'t '
        'bought in, the kid isn\'t showing up. That\'s just how it works there.')

    add_subsection_heading(doc, 'Education-First Culture')
    add_body(doc,
        'School comes first. Always. If an Indian parent has to pick between a tutor and '
        'basketball practice, basketball loses ten out of ten times. I\'m not fighting that '
        'because I\'d lose. Instead, I built the schedule around it. Practice runs outside '
        'school hours. During board exam season, which hits in March-April and again in '
        'October-November, I cut back sessions and let families pick flexible times. Every '
        'academy has a study room where kids can do homework before or after they train, and '
        'that detail matters more than it might seem. It tells parents I\'m not pulling their '
        'kid away from academics.')

    add_body(doc,
        'The scholarship angle is big, too. I\'ll show families real stories of basketball '
        'players who got into international universities because of the sport. When a parent sees '
        'that basketball could actually help their kid\'s education rather than hurt it, the '
        'conversation changes completely.')

    add_subsection_heading(doc, 'Language and Regional Diversity')
    add_body(doc,
        'India has 22 official languages. Hundreds of dialects on top of that. Running everything '
        'in English only would be a huge mistake. Coaches at each academy will work bilingually: '
        'English and Hindi in Delhi, English and Marathi in Mumbai, English and Kannada in '
        'Bangalore. The app ships in five languages at launch, with more coming based on what '
        'people ask for. And I\'m localizing marketing, too. Not just translating it, but '
        'actually using cultural references that mean something in each city. A campaign that hits '
        'in Delhi might fall totally flat in Bangalore if you don\'t adjust the context.')

    add_subsection_heading(doc, 'Religious and Festival Sensitivity')
    add_body(doc,
        'Diwali. Eid. Christmas. Holi. Pongal. Navratri. The list goes on. India\'s festival '
        'calendar is packed, and these aren\'t just days off. They\'re deeply important to '
        'families. I\'m building my yearly schedule with those dates baked in from the start. '
        'Training adjusts around major holidays. During festival seasons, I\'ll host themed '
        'events that bring together kids from all different backgrounds. Making the academy a '
        'place where everyone feels welcome isn\'t optional. In a country this diverse, it\'s the '
        'only way to keep people coming back long-term.')

    add_subsection_heading(doc, 'Gender Considerations')
    add_body(doc,
        'Women\'s basketball is growing in urban India, but there\'s still real hesitation in '
        'some families about girls training alongside boys, especially once they\'re teenagers. '
        'I\'m offering dedicated girls-only sessions with female coaches. That one change '
        'removes the biggest barrier for families who\'d otherwise just say no.')

    add_body(doc,
        'I\'ll also make sure female players are front and center in my marketing. Not shoved '
        'into a sidebar, but actually featured as a core part of the brand. And if you look at '
        'it purely from a business perspective, ignoring the women\'s side means voluntarily '
        'cutting my addressable market in half. That just doesn\'t make sense.')

    # ── FUNDRAISING ──
    add_section_heading(doc, 'Fundraising/Financing')

    add_body(doc,
        'Total cost to launch and survive year one: roughly $900,000. That\'s facilities, staff, '
        'app development, marketing, and a buffer for things I didn\'t predict. I\'m pulling '
        'that from four different places so I\'m not dependent on any single source.')

    add_subsection_heading(doc, 'Angel Investors and Venture Capital')
    add_body(doc,
        'Sports-tech investing in India has gotten a lot more active. Dream Sports, Blume '
        'Ventures, Sequoia India, they\'re all looking for plays in this space. I\'m targeting '
        'a $400,000 seed round from angels with backgrounds in sports, education, or youth '
        'development. The pitch is pretty straightforward: India has the world\'s biggest young '
        'population, basketball interest is spiking, and nobody\'s built a scalable training '
        'model that mixes physical and digital. That\'s the gap. I\'m filling it.')

    add_subsection_heading(doc, 'Government Grants and Initiatives')
    add_body(doc,
        'India\'s Khelo India program and the Sports Authority of India hand out grants to '
        'organizations doing grassroots sports work. If I get accredited as an official training '
        'center, that could mean $100,000 to $150,000 in grant money plus cheap access to '
        'government sports facilities. Maharashtra, Delhi, and Karnataka all have their own '
        'state-level sports funds too, so I\'m applying at every level I can.')

    add_subsection_heading(doc, 'Corporate Sponsorships')
    add_body(doc,
        'Most people outside India don\'t know this, but Indian companies above a certain profit '
        'level are legally required to spend 2% of their net profits on corporate social '
        'responsibility. Youth sports qualifies. That means I can walk into a meeting with Tata, '
        'Reliance, or Infosys and present a sponsorship deal where they\'re spending money they '
        'have to spend anyway, but on something that actually gives them brand exposure with young '
        'consumers. I\'m putting together sponsorship tiers from $25,000 to $200,000, with '
        'visibility at academies, in the app, and at events.')

    add_subsection_heading(doc, 'Crowdfunding')
    add_body(doc,
        'I\'ll run a campaign on Ketto (India\'s biggest crowdfunding platform) and Kickstarter. '
        'Target is $50,000 to $75,000, but the money\'s almost secondary. What crowdfunding '
        'really does is build a base of early supporters who are personally invested before I\'ve '
        'even opened the doors. Backers get discounted memberships, merch, and early app access. '
        'It also forces me to tell my story publicly, and stories about giving kids access to '
        'sports they couldn\'t otherwise afford tend to travel fast online.')

    # ── PROMOTIONAL STRATEGIES ──
    add_section_heading(doc, 'Promotional Strategies')

    add_subsection_heading(doc, 'Digital Marketing Campaigns')
    add_body(doc,
        '800 million internet users. Digital\'s obviously the main channel. Targeted ads on '
        'Instagram, YouTube, and Facebook, heavy on video. Training clips, player progress '
        'stories, behind-the-scenes academy stuff. Placing YouTube pre-roll ads on NBA content '
        'is kind of a no-brainer since that\'s exactly where my audience already hangs out.')

    add_body(doc,
        'I\'ll also invest in SEO and Google Ads for search terms like "basketball training '
        'India" and "basketball academy near me." And I\'ll put out weekly blog posts and '
        'tutorial videos. The idea isn\'t just advertising, it\'s making HoopRise the name that '
        'keeps popping up whenever anyone in India searches for anything related to basketball '
        'development.')

    add_subsection_heading(doc, 'Influencer and Ambassador Partnerships')
    add_body(doc,
        'I want actual people attached to this brand. Satnam Singh was the first Indian ever '
        'drafted by an NBA team. Prachi Tehlan captained the national women\'s team. Those are '
        'the kinds of names I\'m going after. In each city, I\'ll also work with local '
        'micro-influencers, people with 50K to 200K followers who have real pull in their '
        'communities, not just big numbers. I want content collabs and event appearances that '
        'feel genuine, not stiff endorsement deals that everyone scrolls past.')

    add_subsection_heading(doc, 'School and University Outreach')
    add_body(doc,
        'My customers sit in classrooms five days a week. Getting into schools is a huge deal. '
        'Free intro clinics at partner schools, equipment donations for schools starting '
        'basketball programs, inter-school tournament sponsorships. On the college side, I want '
        'to be the training partner that university basketball teams turn to for group packages '
        'and performance analytics through the app. It\'s about being present in the places where '
        'young people already are, instead of trying to pull them somewhere new.')

    add_subsection_heading(doc, 'Event Sponsorships and Community Engagement')
    add_body(doc,
        'Online ads can only do so much. People need to experience the product. So I\'m doing '
        '3-on-3 street tournaments. Basketball camps during school breaks. Watch parties for the '
        'NBA Finals and All-Star Weekend. And once a year, a big event called the "HoopRise '
        'Rising Stars Challenge" that gets press, drives social media buzz, and gives the brand '
        'a signature moment. Long term, I want HoopRise to feel like the center of basketball '
        'culture in India. Not just a training academy, but the place where the basketball '
        'community actually gathers.')

    # ── ANTICIPATED BUDGET ──
    add_section_heading(doc, 'Anticipated Budget')

    add_body(doc,
        'Three-year financial picture. Year 1 I spend a lot and don\'t make it all back. Year 2 '
        'I grow into profitability. Year 3 I\'m making money.')

    add_subsection_heading(doc, 'Projected Expenses')

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
        run.font.size = Pt(11)
        run.font.name = 'Times New Roman'
        run.font.color.rgb = BLACK
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

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
            run.font.size = Pt(11)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = BLACK
            if row_idx == 8:
                run.bold = True
            if col_idx > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    add_body(doc, '', indent=False)

    add_subsection_heading(doc, 'Projected Revenue')

    rev_table = doc.add_table(rows=6, cols=4)
    rev_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    rev_table.style = 'Table Grid'

    rev_headers = ['Revenue Stream', 'Year 1 (USD)', 'Year 2 (USD)', 'Year 3 (USD)']
    for i, h in enumerate(rev_headers):
        cell = rev_table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = 'Times New Roman'
        run.font.color.rgb = BLACK
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    rev_data = [
        ['Academy Memberships', '$180,000', '$420,000', '$720,000'],
        ['Digital Platform Subscriptions', '$40,000', '$150,000', '$380,000'],
        ['Corporate Programs & Events', '$60,000', '$130,000', '$230,000'],
        ['Sponsorship & Partnerships', '$40,000', '$80,000', '$120,000'],
        ['Total Revenue', '$320,000', '$780,000', '$1,450,000'],
    ]

    for row_idx, row_data in enumerate(rev_data, 1):
        for col_idx, val in enumerate(row_data):
            cell = rev_table.rows[row_idx].cells[col_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(11)
            run.font.name = 'Times New Roman'
            run.font.color.rgb = BLACK
            if row_idx == 5:
                run.bold = True
            if col_idx > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    add_body(doc, '', indent=False)

    add_body(doc,
        'Year 1 loses money. I expected that. You can\'t open three academies and build an app '
        'without burning through cash. But revenue ramps up quick. Somewhere around month 18, I '
        'break even. By Year 3, I\'m pulling in $1.45 million against about $1 million in '
        'costs. That\'s solid margin, and it gets better as the app scales because digital users '
        'don\'t require more facilities or proportionally more coaches.')

    add_body(doc, '', indent=False)
    doc.add_picture(CHART_PATH, width=Inches(5.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ── STRATEGIC PARTNERSHIPS ──
    add_section_heading(doc, 'Strategic Partnerships')

    add_body(doc,
        'Trying to do everything myself would be slow, expensive, and kind of dumb when '
        'there are organizations out there that already have what I need. The smarter move is '
        'to partner up, trade value, and get to market faster. Five partnerships matter most.')

    add_subsection_heading(doc, 'NBA India')
    add_body(doc,
        'This is the big one. The NBA\'s already spending money in India through the Academy, '
        'Jr. NBA programs, and broadcast deals. Getting recognized as an official NBA-affiliated '
        'training center would give me their coaching resources, their credibility, and access to '
        'their scouting pipeline. For a kid training at HoopRise, that means a real ladder: '
        'perform well, get noticed, maybe get a shot at the Academy or catch a scout\'s eye. No '
        'other training program in India can dangle that kind of carrot.')

    add_subsection_heading(doc, 'Nike India / Adidas India')
    add_body(doc,
        'Sportswear partnership gives me better prices on gear, co-branded marketing, and '
        'possibly scholarship funding. Nike\'s my first pick because of their basketball roots, '
        'but Adidas works too. For the brand, they get their products on the next generation of '
        'Indian basketball players in a market that\'s only going to get bigger. They spend '
        'millions trying to build that kind of ground-level brand loyalty through other channels. '
        'I\'m offering it built in.')

    add_subsection_heading(doc, 'Basketball Federation of India (BFI)')
    add_body(doc,
        'BFI accreditation gives me institutional credibility you can\'t buy. My players become '
        'eligible for state and national team selection. I get into BFI tournaments and coaching '
        'certification programs. For the BFI, I\'m doing the grassroots scouting and '
        'development they don\'t have the infrastructure to do themselves. Both sides get '
        'something they need.')

    add_subsection_heading(doc, 'Indian School and University Networks')
    add_body(doc,
        'Delhi Public School, Amity International, Ryan International. These school networks '
        'have campuses everywhere. Partnering with them means after-school programs on their '
        'facilities, discounted enrollment for their students, and inter-school tournaments I '
        'sponsor. Universities like Christ (Bangalore), Shiv Nadar (Delhi), and NMIMS (Mumbai) '
        'give me access to the 18-22 age bracket and potential internship pipelines for sports '
        'management students. It puts me right where my customers spend most of their day.')

    add_subsection_heading(doc, 'Technology Partners')
    add_body(doc,
        'Good apps are expensive to build. Great apps even more so. Partnering with Indian IT '
        'companies like Infosys or Wipro for development, using AWS India\'s startup credits for '
        'hosting, and integrating tools from sports tech companies like ShotTracker keeps my '
        'costs manageable without sacrificing quality. When you\'re a startup trying to compete '
        'against polished international apps, you need the tech to be good. These partnerships '
        'make that possible without blowing through my budget.')

    # ── REFERENCES ──
    add_section_heading(doc, 'References')

    references = [
        'Deloitte. (2024). India\'s digital sports consumption: Trends and opportunities in a '
        'mobile-first market. Deloitte Touche Tohmatsu India LLP.',

        'KPMG. (2023). The business of sports: A comprehensive analysis of India\'s evolving '
        'sports industry landscape. KPMG India.',

        'National Basketball Association. (2024). NBA global outreach report: Expanding '
        'basketball culture in emerging markets. NBA Communications.',

        'Sports Authority of India. (2023). Khelo India annual report 2022-2023: Building a '
        'sporting nation through grassroots development. Ministry of Youth Affairs and Sports, '
        'Government of India.',

        'United Nations Department of Economic and Social Affairs. (2024). World population '
        'prospects 2024: India demographic profile summary. United Nations Publications.',
    ]

    for ref in references:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        set_line_spacing(p)
        run = p.add_run(ref)
        run.font.size = Pt(12)
        run.font.name = 'Times New Roman'
        run.font.color.rgb = BLACK

    doc.save(DOC_PATH)
    print(f"Document saved: {DOC_PATH}")


if __name__ == '__main__':
    generate_budget_chart()
    print(f"Chart saved: {CHART_PATH}")
    build_document()
