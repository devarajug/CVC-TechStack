from os.path import isfile
from re import search
from re import compile
from re import sub
from json import loads
import pandas as pd
from sys import exit as sysexit

class FetchCvcVulnerabilities:

    def __init__(self, cvc_json_file_path, comments={}, escaped_path=[]):
        self.json_file_path = cvc_json_file_path
        self.comments = comments
        self.remove_error = compile(''',"analysisExceptions":\[\{<exception>.*</exception>\}\]''')
        self.escaped_path = escaped_path
    
    def readCVCDataFromJsonFile(self):
        if isfile(self.json_file_path):
            try:
                with open(self.json_file_path, 'r', encoding='utf8') as f:
                    data = f.read()
                    if search(self.remove_error, data):
                        data = sub(self.remove_error, '', data)
                cvcJsonData = loads(data)
            except Exception as e:
                print("[Error] unable read dependency check json file....")
                sysexit(e)
        else:
            sysexit("[Error] unable read dependency check json file....")
        return cvcJsonData
    
    def cvcJsonDataToDataFrame(self):
        vuldependency, cve_id, severity, filePath, description, status, auditor_comments = [[] for i in range(7)]
        try:
            cvcJsonData = self.readCVCDataFromJsonFile()
            for dependency in cvcJsonData.get("dependencies", {}):
                if 'vulnerabilities' in dependency.keys():
                    for vulnerability in dependency.get('vulnerabilities', {}):
                        if 'relatedDependencies' in dependency.keys():
                            vuldependency.append(dependency.get('fileName').strip())
                            cve_id.append(vulnerability.get('name').strip())
                            severity.append(vulnerability.get('severity').upper().strip())
                            filePath.append('/'.join([x for x in dependency.get('filePath').split("\\") if x not in self.escaped_path]))
                            description.append(str(vulnerability.get('description')).replace('\n', ' '))
                            status.append(self.comments.get(vuldependency[-1], {}).get(cve_id[-1], {}).get("Status", "Open"))
                            auditor_comments.append(self.comments.get(vuldependency[-1], {}).get(cve_id[-1], {}).get("Comment", "need add in JsonFile"))

                            for relatedDependency in dependency.get('relatedDependencies', {}):
                                filename = relatedDependency.get('filePath').split('\\')[-1].strip()
                                filePath.append('/'.join([x for x in relatedDependency.get('filePath').split('\\') if x not in self.escaped_path]))
                                vuldependency.append(filename)
                                cve_id.append(vulnerability.get('name').strip())
                                description.append(str(vulnerability.get('description')).replace('\n', ' '))
                                severity.append(vulnerability.get('severity').upper().strip())
                                status.append(self.comments.get(vuldependency[-1], {}).get(cve_id[-1], {}).get("Status", "Open"))
                                auditor_comments.append(self.comments.get(vuldependency[-1], {}).get(cve_id[-1], {}).get("Comment", "need add in JsonFile"))
                        else:
                            vuldependency.append(dependency.get('fileName').strip())
                            cve_id.append(vulnerability.get('name').strip())
                            severity.append(vulnerability.get('severity').upper())
                            filePath.append('/'.join([x for x in dependency.get('filePath').split('\\') if x not in self.escaped_path]))
                            description.append(str(vulnerability.get('description')).replace('\n', ' '))
                            status.append(self.comments.get(vuldependency[-1], {}).get(cve_id[-1], {}).get("Status", "Open"))
                            auditor_comments.append(self.comments.get(vuldependency[-1], {}).get(cve_id[-1], {}).get("Comment", "need add in JsonFile"))
            
            result_data = zip(vuldependency, description, cve_id, severity,filePath, status, auditor_comments)
            df_cvc = pd.DataFrame(list(result_data),
                columns = [
                    "DependencyName",
                    "Description",
                    "CVE",
                    "Severity",
                    "FilePath",
                    "Status",
                    "Auditor Comment"
                ]
            )

        except Exception as e:
            print("[Error] unable to convert cvc data to data frame....")
            sysexit(e)
        return df_cvc