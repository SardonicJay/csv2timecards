import pandas as pd
import math
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

import argparse
import os
import json

MeetName = "Swim Meet"
MeetDate = "6/1/2026"
TeamName = "Team Name"
PoolUnits = "SCM"

#text coloring
RESET = "\033[0m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

BOLD = "\033[1;"
BOLD_RED = "\033[1;31m"
BOLD_GREEN = "\033[1;32m"
BOLD_YELLOW = "\033[1;33m"

EmptyCard = {'EventNumber': '___', 
             'Heat': math.nan, 'Lane': math.nan, 
             'AgeGroupName': 'Grp:___________',
             'Distance': 'Dst:___', 'Stroke': 'Strk:________', 
             'AthleteName': 'Name:________________', 'AthleteAge': '', 
             'SeedTimeConverted': '______', 'SeedTimeUnconverted': '_____', 
             'IsExhibition': False, 'IndOrRelay': 'I'}


def format_record(pos, row_dict, style):
    card_text = ""
    entry = {}
    #print(row_dict.items())
    for key, value in row_dict.items():
        entry[key] = value
        
    if math.isnan(entry['Heat']):
        entry['Heat'] = "____"
    if math.isnan(entry['Lane']):
        entry['Lane'] = "____"
    
    # center each card accounting for page margining
    if pos in [2,3]:
        card_text += "<br/>"*2
    elif pos in [4,5]:
        card_text += "<br/>"*4

    # font style centering doesnt appear to work so I just add some spaces for the meet name and date
    card_text += f"<b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{MeetName} - {MeetDate}</b><br/><br/>"

    card_text += f"Event {entry['EventNumber']}<br/>"
    card_text += f"{entry['AgeGroupName']} &nbsp;{entry['Distance']} {PoolUnits} {entry['Stroke']} <br/>"
    card_text += f"Heat: {entry['Heat']} &nbsp; Lane: {entry['Lane']} &nbsp; Seed Time: {entry['SeedTimeConverted']}<br/><br/>"
    card_text += f"{entry['AthleteName']} &nbsp; {entry['AthleteAge']} <br/>"
    card_text += f"Team: {TeamName} <br/> <br/>"
    card_text += f"<b>T1</b> ___.___.___  <b>T2</b> ___.___.___  <b>T3</b> ___.___.___<br/><br/>"
    card_text += f"<b>Official Time</b> ___.___.___"  
    return Paragraph(card_text, style)

def csv_to_pdf_cards(csv_file, pdf_file):
    # Load data
    df = pd.read_csv(csv_file)
    records = df.to_dict(orient='records')
    
    # PDF Setup (Letter size: 612 x 792 points)
    # 0.5 inch margins = 36 points
    doc = SimpleDocTemplate(
        pdf_file, 
        pagesize=letter,
        leftMargin=12, rightMargin=12, 
        topMargin=12, bottomMargin=12
    )
    
    # Calculate exact card dimensions
    # Width: (612 - 72) / 2 = 270 points per card
    # Height: (792 - 72) / 3 = 240 points per card
    col_widths = [270, 270]
    row_heights = [240, 240, 240]
    
    # Styles for card text
    styles = getSampleStyleSheet()
    card_style = ParagraphStyle(
        'CardStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#333333')
    )
    
    # Card Border and Padding Styling
    grid_style = TableStyle([
        # ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#A0A0A0')),
        # ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAFAFA')),
        ('GRID', (0, 0), (-1, -1), 1, colors.transparent),
        ('BACKGROUND', (0, 0), (-1, -1), colors.transparent),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 18),
        ('LEFTPADDING', (0, 0), (-1, -1), 18),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ])
    
    story = []
    cards_per_page = 6
    empty_cards = 0
    
    # Process data in chunks of 6
    for i in range(0, len(records), cards_per_page):
        chunk = records[i:i + cards_per_page]

        # this avoids wasting card stock by filling out the rest of the last sheet with an empty card to fill out by hand
        while len(chunk) < cards_per_page:
            chunk.append(EmptyCard)
            empty_cards+=1

        # Format each record into a Paragraph flowable
        # formatted_cards = [format_record(r, card_style) for r in chunk]
        formatted_cards = []
        for p, r in enumerate(chunk):
            formatted_cards.append(format_record(p, r, card_style))
        
        # Pad the chunk with empty paragraphs if it has fewer than 6 records
        while len(formatted_cards) < cards_per_page:
            formatted_cards.append(Paragraph("", card_style))
            
        # Structure into a 2 columns x 3 rows matrix
        grid_data = [
            [formatted_cards[0], formatted_cards[1]],
            [formatted_cards[2], formatted_cards[3]],
            [formatted_cards[4], formatted_cards[5]]
        ]
        
        # Build page grid
        page_table = Table(grid_data, colWidths=col_widths, rowHeights=row_heights)
        page_table.setStyle(grid_style)
        story.append(page_table)
        
        # Add page break if more records remain
        if i + cards_per_page < len(records):
            story.append(PageBreak())
            
    doc.build(story)

    print(f"\n{BOLD_YELLOW}Processing Complete...{RESET}\n\n {MAGENTA}{len(records)+empty_cards} total {CYAN}({empty_cards} empty){RESET} time cards generated to {BOLD_GREEN}{pdf_file}{RESET}\n")
    
    input("Press Enter to exit...")

def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Swimtopia Entry Report to NVSL time card format", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # csv input file
    parser.add_argument("in_csv_entries", type=str, help="Swimtopia Entry Report [Reports » Meet Entries by Event] exported as a csv.")

    # time card pdf output file
    parser.add_argument("-o", "--out", type=str, default=None, help="Time Card pdf format [6 cards per sheet] -- defaults to [meet]_[date]_[team].pdf if not defined")

    # pool units -- SCM by default
    parser.add_argument("-u", "--units", type=str, default=None, help="Pool length units [SCM|SCY|LCM]")
    
    # meet name
    parser.add_argument("-m", "--meet", type=str, default=None, help="Meet Name")

    # meet date
    #parser.add_argument("-d", "--date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="Meet Date")
    parser.add_argument("-d", "--date", type=str, default=None, help="Meet Date")

    # team name
    parser.add_argument("-t", "--team", type=str, default=None, help="Team Name")


    # apply config file values if it exists
    config = None
    #cfg_file = os.path.splitext(os.path.abspath(__file__))[0]+".cfg"
    cfg_file = "csv2timecards.cfg"
    try:
        if os.path.isfile(cfg_file):
            with open(cfg_file, 'r') as cfg:
                config = json.load(cfg)
    except:
        print(f"\n{BOLD_RED}ERROR:{RESET} with loading cfg file {YELLOW}{cfg_file}{RESET} check formatting.  bypassing config....")
        config = None

    if config:
        parser.set_defaults(**config)

    # Parse the arguments
    args = parser.parse_args()

    # Validate

    # in_csv_entries
    if not os.path.isfile(args.in_csv_entries):
        print(f"\n{BOLD_RED}ERROR:{RESET} input file {BOLD}{YELLOW}{args.in_csv_entries}{RESET} does not exist. Check your file path.")
        input("Press Enter to exit...")
        return
    
    # team name
    if not args.team:
        args.team = input(f"\nEnter Team Name [default: {GREEN}Team{RESET}]: ") or "Team"

    # meet name
    if not args.meet:
        args.meet = input(f"\nEnter Meet Name [default: {GREEN}Meet{RESET}]: ") or "Meet"

    # meet date
    if not args.date:
        args.date = input(f"\nEnter Meet Date [default: {GREEN}{datetime.now().strftime("%Y-%m-%d")}{RESET}]: ") or datetime.now().strftime("%Y-%m-%d")
    
    # pool units
    if not args.units:
        args.units = input(f"\nEnter Pool Units [valid: {GREEN}SCM|SCY|LCM{RESET} default: {GREEN}SCM{RESET}]: ") or "SCM"
    if not args.units in ["SCM","LCM","SCY"]:
        print(f"\n{BOLD_RED}ERROR:{RESET} pool units {RED}{args.units}{RESET} invalid. [valid: {GREEN}SCM|SCY|LCM{RESET}]. ")
        input("Press Enter to exit...")
        return
    
    global PoolUnits, MeetName, MeetDate, TeamName
    PoolUnits = args.units
    MeetName = args.meet
    MeetDate = args.date
    TeamName = args.team

    print(f"\n{BOLD_YELLOW}Team Name: {RESET}{CYAN}{TeamName}{RESET}")
    print(f"{BOLD_YELLOW}Meet Name: {RESET}{CYAN}{MeetName}{RESET}")
    print(f"{BOLD_YELLOW}Meet Date: {RESET}{CYAN}{MeetDate}{RESET}")
    print(f"{BOLD_YELLOW}Pool Units: {RESET}{CYAN}{PoolUnits}{RESET}")

    if not args.out:
        outfile = f"{MeetName}_{MeetDate}_{TeamName}.pdf".replace(" ", "").replace("-", "").replace("/", "").replace("\\", "")
        dir_name = os.path.dirname(args.in_csv_entries)
        outfileFullPath = os.path.join(dir_name, outfile)

        args.out = input(f"\nEnter Time Card Output File [default: {GREEN}{outfileFullPath}{RESET}]: ") or outfileFullPath


    csv_to_pdf_cards(args.in_csv_entries, args.out)

if __name__ == "__main__":
    
    main()