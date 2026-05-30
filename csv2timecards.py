import pandas as pd
import math
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

import argparse
import os

MeetName = "Swim Meet"
MeetDate = "6/1/2026"
TeamName = "CCH Sharks"
PoolUnits = "SCM"


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
    
    # Process data in chunks of 6
    for i in range(0, len(records), cards_per_page):
        chunk = records[i:i + cards_per_page]

        # Format each record into a Paragraph flowable
        # formatted_cards = [format_record(r, card_style) for r in chunk]
        formatted_cards = []
        for p, r in enumerate(chunk):
            print(p)
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

def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Swimtopia Entry Report to NVSL time card format", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # csv input file
    parser.add_argument("in_csv_entries", type=str, help="Swimtopia Entry Report [Reports » Meet Entries by Event] exported as a csv.")

    # time card pdf output file
    parser.add_argument("-o", "--out", type=str, default=None, help="Time Card pdf format [6 cards per sheet] -- defaults to [meet]_[date]_[team].pdf if not defined")

    # pool units -- SCM by default
    parser.add_argument("-u", "--units", type=str, default="SCM", help="Pool length units [SCM|SCY|LCM]")
    
    # meet name
    parser.add_argument("-m", "--meet", type=str, default="Time Trials", help="Meet Name")

    # meet date
    parser.add_argument("-d", "--date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="Meet Date")

    # team name
    parser.add_argument("-t", "--team", type=str, default="CCH Sharks", help="Team Name")


    # Parse the arguments
    args = parser.parse_args()

    # Validate

    # in_csv_entries
    if not os.path.isfile(args.in_csv_entries):
        print(f"\n\033[1;31mERROR:\033[0m input file \033[1;33m{args.in_csv_entries}\033[0m does not exist. Check your file path.")
        print("exiting...\n")
        return
    
    # pool units
    if not args.units in ["SCM","LCM","SCY"]:
        print(f"\n\033[1;31mERROR:\033[0m pool units \033[1;33m{args.units}\033[0m invalid [SCM,SCY,LCM]. ")
        print("exiting...\n")
        return
    
    # rest of arguments are basically strings and can be whatever you want so no validation necessary

    global PoolUnits, MeetName, MeetDate, TeamName
    PoolUnits = args.units
    MeetName = args.meet
    MeetDate = args.date
    TeamName = args.team

    if not args.out:
        outfile = f"{MeetName}_{MeetDate}_{TeamName}.pdf".replace(" ", "").replace("-", "").replace("/", "").replace("\\", "")
        dir_name = os.path.dirname(args.in_csv_entries)
        args.out = os.path.join(dir_name, outfile)


    csv_to_pdf_cards(args.in_csv_entries, args.out)

if __name__ == "__main__":
    
    main()


    #csv_to_pdf_cards("cchsharks_entries.csv", "output4.pdf")