@echo off

set /p input="Enter ThirdParty Components Location: "
set /p output="Enter Output Location: "
set /p proxycheck="Are You Running This Script Behind Proxy Y/N : "

set "condition=0"

if %proxycheck%==Y set "condition=1"
if %proxycheck%==y set "condition=1"

call python "Utils\clean-workspace.py" %output%

if %condition%==1 ( goto withproxy ) else ( goto withoutproxy )

goto end

:withproxy
    
    set /p proxyname="Enter Proxy Name: "
    set /p proxyport="Enter Proxy Port: "
    set /p proxyuser="Enter Proxy User: "
    set /p proxypass="Enter Proxy Password: "

    if exist "%cd%\venv" (
        call venv\Scripts\activate
        pip install -r requirements.txt
    ) else (
        pip install virtualenv
        python -m virtualenv venv
        call venv\Scripts\activate
        pip install -r requirements.txt
    )

    if exist "%cd%\dependency-check\bin\" (
        call python ".\Utils\dct-version-update.py" %proxyname% %proxyport% %proxyuser% %proxyport%
    ) else (
        call python ".\Utils\dct-download.py" %proxyname% %proxyport% %proxyuser% %proxyport%
    )
    
    call python "Utils\generate_cvc_command_bat_proxy.py" %input%

    call scan.bat

    call python "Utils\makeXl.py" %proxyname% %proxyport% %proxyuser% %proxypass% %input% %output%

    del scan.bat

:withoutproxy

    if exist "%cd%\venv" (
        call venv\Scripts\activate
        pip install -r requirements.txt
    ) else (
        pip install virtualenv
        python -m virtualenv venv
        call venv\Scripts\activate
        pip install -r requirements.txt
    )

    if exist "%cd%\dependency-check\bin\" (
        call python "Utils\dct-version-update.py"
    ) else (
        call python "Utils\dct-download.py"
    )
    
    call python "Utils\generate_cvc_command_bat_without_proxy.py" %input%

    call scan.bat
    
    call python "Utils\makeXl.py" %input% %output%

    del scan.bat

:end
    echo.
    echo [Info] Scan Finished Reports Generated...
    deactivate
    