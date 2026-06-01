# csv2timecards
Utility to convert Entry Reports to Printable Time Cards

Export from Swimtopia...

*[Reports » Meet Entries by Event]* exported as a csv.

Outputs a pdf file that is printable on standard card stock (6 per page).  Any incomplete page will be filled with blank cards to be used at the meet for scratches and late adds.


# python libraries
`uv` may be necessary to install in Windows
```
pip install numpy
pip install pandas
pip install reportlab
pip install pyinstaller
```

# run as python script
`python .\csv2timecards.py`

# create a standalone executable from python script
`pyinstaller --onefile .\csv2timecards.py`

# Executing

## guided input
Drop the Swimtopia Entry report on the executable to start a guided user input process to generate your time cards.

## config file
`csv2timecards.cfg` -- must reside in same directory as executable
json configuration to set defaults
Bypass repetitive user prompting for unchanging values like team and pool length (units).

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

# argument list
Can define arguments on command line and bypass user input prompting.

```
 .\dist\csv2timecards.exe --help

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
