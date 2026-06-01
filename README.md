# csv2timecards
Utility to convert Entry Reports to Printable Time Cards

Export from Swimtopia...

*[Reports » Meet Entries by Event]* exported as a csv.

Outputs a pdf file to same directory as the input csv that is printable on standard card stock (6 per page).  Any incomplete page will be filled with blank cards to be used at the meet for scratches and late adds.

# Quick Start Guide
1. Create a directory
2. Download `csv2timecards.exe` and `csv2timecards.cfg` into the directory
3. Edit `csv2timecards.cfg` and set your team name and pool units (SCM, SCY, or LCM)
4. Run your desired entry report from Swimtopia *[Reports » Meet Entries by Event]*
5. Click *Download Meet Entry Data (CSV)* and move the csv file into the directory.
6. Open the directory and drag the csv entry file on top of csv2timecards.exe
7. Follow the prompts to export your csv file to a timecard formatted pdf file.

# Executing

<font color=green>For easiest results keep all your files (executable, configs, and csv entries) in the same directory</font>

## guided input
Drag & Drop the Swimtopia Entry report on the executable to start a guided user input process to generate your time cards.

## config file
`csv2timecards.cfg` 
* json configuration to set defaults
* Bypass repetitive user prompting for unchanging values like team and pool length (units).

NOTE: due to the way in which the python is packaged into the executable, the config file must reside the the same directory as your csv entries when dragging & dropping.

example: 
```
{
    "team": "Your Team",
    "units": "SCM"
}
```
Can also set meet and date.  Example found here: `examples\csv2timecards.cfg.full`
```
{
    "meet": "Time Trials",
    "date": "2026-06-13",

    "team": "Your Team",
    "units": "SCM"
}
```

## argument list
Can define arguments on command line and bypass user input prompting.

```
 .\csv2timecards.exe --help

usage: csv2timecards.exe [-h] [-o OUT] [-u UNITS] [-m MEET] [-d DATE] [-t TEAM] in_csv_entries

Swimtopia Entry Report to NVSL time card format

positional arguments:
  in_csv_entries     Swimtopia Entry Report [Reports » Meet Entries by Event] exported as a csv.

options:
  -h, --help         show this help message and exit
  -o, --out OUT      Time Card pdf format [6 cards per sheet] -- defaults to [meet]_[date]_[team].pdf if not defined (default: None)
  -u, --units UNITS  Pool length units [SCM|SCY|LCM] (default: None)
  -m, --meet MEET    Meet Name (default: None)
  -d, --date DATE    Meet Date (default: None)
  -t, --team TEAM    Team Name (default: None)
```

# Building Guide
Only needed if you want to make your own modifications to the code.  Otherwise you can just download from the release page.

## python libraries
`uv` may be necessary to install on Windows
```
pip install numpy
pip install pandas
pip install reportlab
pip install pyinstaller
```

## run as python script
`python .\csv2timecards.py`

## create a standalone executable from python script
-- writes to the `dist` subdirectory

```
pyinstaller --onefile .\csv2timecards.py
dist\csv2timecards.exe
```
