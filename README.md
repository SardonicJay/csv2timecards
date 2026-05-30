# csv2timecards
Utility to convert Entry Reports to Printable Time Cards


# python libraries
`uv` may be necessary to install in Windows
```
pip install numpy
pip install pandas
pip install reportlab
pip install pyinstaller
```
# create an executable from python script
`pyinstaller --onefile .\csv2timecards.py`


# argument list
```
.\dist\csv2timecards.exe --help
usage: csv2timecards.exe [-h] [-o OUT] [-u UNITS] [-m MEET] [-d DATE] [-t TEAM] in_csv_entries

Swimtopia Entry Report to NVSL time card format

positional arguments:
  in_csv_entries     Swimtopia Entry Report [Reports » Meet Entries by Event] exported as a csv.

options:
  -h, --help         show this help message and exit
  -o, --out OUT      Time Card pdf format [6 cards per sheet] -- defaults to [meet]_[date]_[team].pdf if not defined (default: None)
  -u, --units UNITS  Pool length units [SCM|SCY|LCM] (default: SCM)
  -m, --meet MEET    Meet Name (default: Time Trials)
  -d, --date DATE    Meet Date (default: 2026-05-30)
  -t, --team TEAM    Team Name (default: CCH Sharks)
```