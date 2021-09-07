from requests import Session
from requests.auth import HTTPProxyAuth
from sys import exit as sysexit
from bs4 import BeautifulSoup
from os.path import join
from os.path import abspath
from os.path import dirname
from json import loads
import pandas as pd

class FetchTechStackVulnerabilities:

    def __init__(self, comments={}, proxy_name=None, proxy_port=None, proxy_user=None, proxy_pass=None):
        self.url = "https://nvd.nist.gov/vuln/search/results?adv_search=true&isCpeNameSearch=true&query={}&startIndex={}"
        self.proxyname = proxy_name
        self.proxyport = proxy_port
        self.proxyuser = proxy_user
        self.proxypass = proxy_pass
        self.startIndex = 0
        self.noOfIssuesCount = 0
        self.countFrom = 0
        self.countThrough = 0
        self.comments = comments
        
    def getDataFromWeb(self, url):
        try:
            request = Session()

            if self.proxyuser and self.proxypass:
                proxies = {
                    "http": "http://"+str(self.proxyname)+":"+str(self.proxyport),
                    "https": "https://"+str(self.proxyname)+":"+str(self.proxyport)
                }
                auth = HTTPProxyAuth(self.proxyuser, self.proxypass)
                request.proxies = proxies
                request.auth = auth
            request.verify = False
            data = request.get(url=url)
        except Exception as e:
            data = None
            print("[Error] unable connect to web to fecth techstack data..", str(e))
        return data
    
    def getTechStackDetails(self):

        try:
            with open(join(dirname(dirname(abspath(__file__))), 'tech_stack_details.json'), 'r') as rb:
                cpematchstrings = loads(rb.read())

        except Exception as e:
            print("[Error] Unable to read tech stack data from file, file may missed or deleted...", str(e))
        return cpematchstrings
    
    def scrapeTechStackData(self, cpe, startIndex=0):
        try:
            url = self.url.format(cpe, str(startIndex))
            data = self.getDataFromWeb(url=url)
            parsed_data = BeautifulSoup(data.text, 'lxml')
            self.noOfIssuesCount = int(parsed_data.select_one('strong[data-testid=vuln-matching-records-count]').text)
            self.countFrom = int(parsed_data.select_one('strong[data-testid=vuln-displaying-count-from]').text)
            self.countThrough = int(parsed_data.select_one('strong[data-testid=vuln-displaying-count-through]').text)
            TechStackData = parsed_data.select_one('table[data-testid=vuln-results-table]')
        except Exception as e:
            TechStackData = None
            print("[Error] unable to fecth details from parsed data ....", str(e))
        return TechStackData

    def techStackDataToDf(self):
        try:
            print()
            print("Analysis Started. It Takes Time to Complete, Please Wait Patiently....")
            productname, cve, severity, description, auditor_comment, status = [[] for i in range(6)]
            cpeMatchStrings=self.getTechStackDetails()
            for product, cpe in cpeMatchStrings.items():
                print()
                data = self.scrapeTechStackData(cpe=cpe)
                if self.noOfIssuesCount == 0:
                    productname.append(product.strip())
                    cve.append("No Vulnerability")
                    severity.append("No Vulnerability")
                    description.append("No Vulnerability")
                    auditor_comment.append('No Vulnerability')
                    status.append("No Vulnerability")
                    print(productname[-1]+ " : " + cve[-1] + " : " + severity[-1])
                elif self.noOfIssuesCount <= 20:
                    issues_table = self.scrapeTechStackData(cpe=cpe)
                    non_dispute_issues_count=0
                    for i in range(self.noOfIssuesCount):
                        description_data = issues_table.select_one('tr[data-testid=vuln-row-'+str(i)+'] td p[data-testid=vuln-summary-'+str(i)+']').text.strip()
                        if "unspecified vulnerability" in description_data.lower() or "disputed" in description_data.lower():
                            continue
                        else:
                            productname.append(product.strip())
                            cve.append(issues_table.select_one('tr[data-testid=vuln-row-'+str(i)+'] th strong a[href]').text.strip())
                            description.append(description_data)
                            cvss3 = issues_table.select_one('tr[data-testid=vuln-row-'+str(i)+'] td[nowrap=nowrap] span[id=cvss3-link]')
                            if cvss3:
                                cvss3_score_severity = cvss3.text.split(":")[-1]
                                cvss3_severity = cvss3_score_severity.split(" ")[-1]
                                severity.append(cvss3_severity.strip())
                            else:
                                cvss2 = issues_table.select_one('tr[data-testid=vuln-row-'+str(i)+'] td[nowrap=nowrap] span[id=cvss2-link]').text
                                cvss2_score_severity = cvss2.split(":")[-1]
                                cvss2_severity = cvss2_score_severity.split(" ")[-1]
                                severity.append(cvss2_severity.strip())
                            status.append(self.comments.get(productname[-1], {}).get(cve[-1], {}).get("Status", "Open"))
                            auditor_comment.append(self.comments.get(productname[-1], {}).get(cve[-1], {}).get("Comment", "need add in JsonFile"))
                            non_dispute_issues_count+=1
                        print(productname[-1]+ " : " + cve[-1] + " : " + severity[-1])
                    else:
                        if non_dispute_issues_count == 0:
                            productname.append(product)
                            cve.append("No Vulnerability")
                            severity.append("No Vulnerability")
                            description.append("No Vulnerability")
                            auditor_comment.append('No Vulnerability')
                            status.append("No Vulnerability")
                            print(productname[-1]+ " : " + cve[-1] + " : " + severity[-1])
                elif self.noOfIssuesCount > 20:
                    count_while = 0
                    while self.noOfIssuesCount - self.startIndex >= 0:
                        issues_table = self.scrapeTechStackData(cpe=cpe, startIndex=self.startIndex)
                        for i in range(self.countThrough+1 - self.countFrom):
                            description_data = issues_table.select_one('tr[data-testid=vuln-row-'+str(i)+'] td p[data-testid=vuln-summary-'+str(i)+']').text.strip()
                            if "unspecified vulnerability" in description_data.lower() or "disputed" in description_data.lower():
                                continue
                            else:
                                productname.append(product.strip())
                                cve.append(issues_table.select_one('tr[data-testid=vuln-row-'+str(i)+'] th strong a[href]').text.strip())
                                description.append(description_data)
                                cvss3 = issues_table.select_one('tr[data-testid=vuln-row-'+str(i)+'] td[nowrap=nowrap] span[id=cvss3-link]')
                                if cvss3:
                                    cvss3_score_severity = cvss3.text.split(":")[-1]
                                    cvss3_severity = cvss3_score_severity.split(" ")[-1]
                                    severity.append(cvss3_severity.strip())
                                else:
                                    cvss2 = issues_table.select_one('tr[data-testid=vuln-row-'+str(i)+'] td[nowrap=nowrap] span[id=cvss2-link]').text
                                    cvss2_score_severity = cvss2.split(":")[-1]
                                    cvss2_severity = cvss2_score_severity.split(" ")[-1]
                                    severity.append(cvss2_severity.strip())
                                status.append(self.comments.get(productname[-1], {}).get(cve[-1], {}).get("Status", "Open"))
                                auditor_comment.append(self.comments.get(productname[-1], {}).get(cve[-1], {}).get("Comment", "need add in JsonFile"))
                                count_while+=1
                            print(productname[-1]+ " : " + cve[-1] + " : " + severity[-1])
                        self.startIndex+=20
                    else:
                        if count_while == 0:
                            productname.append(product)
                            cve.append("No vulnerability")
                            severity.append("No vulnerability")
                            description.append("No vulnerability")
                            auditor_comment.append('No vulnerability')
                            status.append("No Vulnerability")
                            print(productname[-1]+ " : " + cve[-1] + " : " + severity[-1])
                else:
                    print("[Error] Unable to fetch no of issues please re run script...")
            result_data_tech_stack = zip(productname,description,cve,severity, status, auditor_comment)
            df_tech_stack = pd.DataFrame(
                list(result_data_tech_stack),
                columns = ['Product','Description','CVE','Severity', 'Status', 'Auditor Comment']
            )
        except Exception as e:
            df_tech_stack = None
            print("[Error] unable to convert techstack data to dataframe ....", str(e))
        return df_tech_stack