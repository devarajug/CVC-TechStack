import os
import colorama
from sys import argv
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter


cvcOutPutDir = argv[1]
files = os.listdir(cvcOutPutDir)
for file in files:
	conditions = [
		os.path.splitext(file)[-1] == '.xls',
		os.path.splitext(file)[-1] == '.xlsx',
	]
	if any(conditions):
		filename = os.path.join(cvcOutPutDir,file)

# filename = os.path.join(cvcOutPutDir,'dependency-check-report_Jile.xlsx') 

xl = pd.ExcelFile(filename)
dfxl = xl.parse(xl.sheet_names[0])

dfopen = dfxl[(dfxl['Status'] == 'Open') | (dfxl['Status'] == 'open')]

dfnotanissue = dfxl[(dfxl['Status'] == 'Not an Issue') | (dfxl['Status'] == 'Not an issue')]


dftotal = dfxl

OpenCritical       = len(dfopen[dfopen['Severity'] == "CRITICAL"])
OpenHigh           = len(dfopen[dfopen['Severity'] == "HIGH"])
OpenMedium         = len(dfopen[dfopen['Severity'] == "MEDIUM"])
OpenLow            = len(dfopen[(dfopen['Severity'] == "LOW") | (dfopen['Severity'] == "UNKNOWN") | (dfopen['Severity'] == "MODERATE")])

NotAnIssueCritical = len(dfnotanissue[dfnotanissue['Severity'] == "CRITICAL"])
NotAnIssueHigh     = len(dfnotanissue[dfnotanissue['Severity'] == "HIGH"])
NotAnIssueMedium   = len(dfnotanissue[dfnotanissue['Severity'] == "MEDIUM"])
NotAnIssueLow      = len(dfnotanissue[(dfnotanissue['Severity'] == "LOW") | (dfnotanissue['Severity'] == "UNKNOWN") | (dfnotanissue['Severity'] == "MODERATE")])

NotAnIssueTotal    = NotAnIssueCritical + NotAnIssueHigh + NotAnIssueMedium + NotAnIssueLow
OpenTotal          = OpenCritical + OpenHigh + OpenMedium + OpenLow

CriticalTotal      = OpenCritical + NotAnIssueCritical
HighToatl          = OpenHigh + NotAnIssueHigh
MediumTotal        = OpenMedium + NotAnIssueMedium
LowTotal           = OpenLow + NotAnIssueLow
GrandToatal        = NotAnIssueTotal + OpenTotal

print()

print(Fore.BLACK + Back.WHITE + Style.BRIGHT + "+---------------+------------+----------+-----------+-----------+-----------+")
print(Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" +Fore.BLUE + Style.BRIGHT + "  STATUS       " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.BLUE + Style.BRIGHT + "  CRITICAL  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.BLUE + Style.BRIGHT +"    HIGH  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.BLUE + Style.BRIGHT + "   MEDIUM  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.BLUE + Style.BRIGHT + "      LOW  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.BLUE + Style.BRIGHT + "    TOTAL  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+")

print(Fore.BLACK + Back.WHITE + Style.BRIGHT + "+---------------+------------+----------+-----------+-----------+-----------+")
print(Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.GREEN + Style.BRIGHT + "  NOT AN ISSUE " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.GREEN + Style.BRIGHT + "  " + "{:>8}".format(str(NotAnIssueCritical)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.GREEN + Style.BRIGHT +"  " + "{:>6}".format(str(NotAnIssueHigh)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT+ "+" + Fore.GREEN + Style.BRIGHT + "  " + "{:>7}".format(str(NotAnIssueMedium)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.GREEN + Style.BRIGHT + "  " + "{:>7}".format(str(NotAnIssueLow)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.GREEN + Style.BRIGHT + "  " + "{:>7}".format(str(NotAnIssueTotal)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+")

print(Fore.BLACK + Back.WHITE + Style.BRIGHT + "+---------------+------------+----------+-----------+-----------+-----------+")
print(Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.RED + Style.BRIGHT + "  OPEN         " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.RED + Style.BRIGHT + "  " + "{:>8}".format(str(OpenCritical)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.RED + Style.BRIGHT + "  " + "{:>6}".format(str(OpenHigh)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.RED + Style.BRIGHT + "  " + "{:>7}".format(str(OpenMedium)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.RED + Style.BRIGHT + "  " + "{:>7}".format(str(OpenLow)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.RED + Style.BRIGHT + "  "+ "{:>7}".format(str(OpenTotal)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+")

print(Fore.BLACK + Back.WHITE + Style.BRIGHT + "+---------------+------------+----------+-----------+-----------+-----------+")
print(Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.BLUE + Style.BRIGHT + "  GRAND TOTAL  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.BLUE + Style.BRIGHT + "  " + "{:>8}".format(str(CriticalTotal)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.BLUE + Style.BRIGHT + "  " + "{:>6}".format(str(HighToatl)) + "  "+Fore.BLACK + Back.WHITE + Style.BRIGHT+"+"+Fore.BLUE + Style.BRIGHT+"  " + "{:>7}".format(str(MediumTotal)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.BLUE + Style.BRIGHT + "  " + "{:>7}".format(str(LowTotal)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+" + Fore.BLUE + Style.BRIGHT + "  " + "{:>7}".format(str(GrandToatal)) + "  " + Fore.BLACK + Back.WHITE + Style.BRIGHT + "+")
print(Fore.BLACK + Back.WHITE + Style.BRIGHT + "+---------------+------------+----------+-----------+-----------+-----------+")

print()
print(len(dfopen) + len(dfnotanissue))