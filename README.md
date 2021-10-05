# CVC & TECHSTACK SCAN

The use of this project is to automate the thirdparty compaonent check and also fetch the vulnerabilities of Technology Stack Used in Project.

# HOW IT WORKS

- Once you run the **cvc-scan** file 
- It asks for the following inputs:
    - Location of Thirdparty Components(Jar) used in application to scan.
    - Another location to store scan output files.
- After giving those inputs, It asks __Yes/No__ question wetaher you run the script behind corporate proxy or not.
- If you are running the script behind proxy then it asks for the following details.
    - Proxy Server Name.
    - Proxy Server Port.
    - Proxy Username.
    - Proxy Password.
- After giving those details the script checks weather python virtualenv present or not.
- If present it activates the envinorment and installs dependencies.
- If not present then, it create, activate and installs the dependencies.
- After installing dependencies, it checks weather dependecy check tool is present in the folder or not.
- If present it continues the scan, otherwise It installs the dependency check tool and continues the scan.
- Once scan is completed, then it took the [TechStack Details](https://github.com/devarajug/CVC-TechStack/blob/main/Utils/tech_stack_details.json) and check for the vulnerabilities.
- After techstack scan, script took the techstack and cvc data and make excel of two sheets one having cvc vulnerablities and another having techstack vulnerabilities.
- while creating excel file it updates the false postives using [auditor_comments.json](https://github.com/devarajug/CVC-TechStack/blob/main/Utils/auditor_comments.json).


# LICENSE

Copyright (c) 2021 Devaraju Garigapati

This repository is licensed under the [MIT](https://opensource.org/licenses/MIT) license.
See [LICENSE](https://opensource.org/licenses/MIT) for details.