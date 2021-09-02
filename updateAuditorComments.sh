#!/bin/bash

echo "Enter Location of updated xls file: "
read xls_file

python3 "Utils\update_auditor_comments_file.py" $xls_file