@echo off

set /p xls_file="Enter Location of updated xls file: "

call python "Utils\update_auditor_comments_file.py" %xls_file%