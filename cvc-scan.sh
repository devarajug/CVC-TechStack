#!/bin/bash

read -p "Enter ThirdParty Components Location: " input
read -p "Enter Output Location: " output
read -p "Are You Running This Script Behind Proxy Y/N : " proxycheck
echo ""

if [[ "$proxycheck" == "Y" || "$proxycheck" == "y" ]]; then
    python3 "$(pwd)/Utils/clean-workspace.py" $output
    
    read -p "Enter Proxy Server Name: " proxyserver
    read -p "Enter Proxy Server port: " proxyport
    read -p "Enter Proxy Username: " proxyuser
    read -sp "Enter Proxy Password: " proxypass
    echo ""
    if [[ -d "$(pwd)/venv" ]]; then
        source venv/bin/activate
        python3 -m pip install -r requirements.txt 
    else
        python3 -m pip install virtualenv
        python3 -m virtualenv venv
        source venv/bin/activate
        python3 -m pip install -r requirements.txt
    fi

    if [[ -d "$(pwd)/dependency-check" ]]; then
        python3 "$(pwd)/Utils/dct-version-update.py" $proxyserver $proxyport $proxyuser $proxypass
    else
        python3 "$(pwd)/Utils/dct-download.py" $proxyserver $proxyport $proxyuser $proxypass
    fi

    source "$(pwd)/dependency-check/bin/dependency-check.sh" \
        --project "Jile" \
        -f "JSON" -f "HTML" \
        --enableExperimental \
        --enableRetired \
        --disableAssembly \
        --prettyPrint \
        --disableYarnAudit \
        --proxyserver "$proxyserver" \
        --proxyport "$proxyport" \
        --proxyuser "$proxyuser" \
        --proxypass "$proxypass" \
        --scan "$input" \
        --out "$output"

    python3 "$(pwd)/Utils/makeXl.py" $proxyserver $proxyport $proxyuser $proxypass $input $output
else
    if [[ -d "$(pwd)/venv" ]]; then
        source venv/bin/activate
        python3 -m pip install -r requirements.txt 
    else
        python3 -m pip install virtualenv
        python3 -m virtualenv venv
        source venv/bin/activate
        python3 -m pip install -r requirements.txt
    fi

    if [[ -d "$(pwd)/dependency-check" ]]; then
        python3 "$(pwd)/Utils/dct-version-update.py" $proxyserver $proxyport $proxyuser $proxypass
    else
        python3 "$(pwd)/Utils/dct-download.py" $proxyserver $proxyport $proxyuser $proxypass
    fi

    source "$(pwd)/dependency-check/bin/dependency-check.sh" \
        --project "Jile" \
        -f "JSON" -f "HTML" \
        --enableExperimental \
        --enableRetired \
        --disableAssembly \
        --prettyPrint \
        --disableYarnAudit \
        --scan "$input" \
        --out "$output"

    python3 "$(pwd)/Utils/makeXl.py" $input $output
fi