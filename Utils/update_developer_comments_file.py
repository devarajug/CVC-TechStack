import json
from os import sep
from sys import argv
import pandas as pd
from os.path import join
from os.path import dirname
from os.path import abspath
from os.path import isfile


class UpdateJsonFile:
	def __init__(self, xls_file_path):
		self.jar_template = '''{{
            "{jarName}": {{
                "{CVEID}" : {{
                    "Status" : "{Status}",
                    "Comment" : "{Comment}"
                }}
            }}
        }}'''
		self.cve_template = '''{{
            "{CVEID}" : {{
                "Status" : "{Status}",
                "Comment" : "{Comment}"
            }}
        }}'''
		self.xls_path = join(*xls_file_path)
		self.developer_comments_file = join(dirname(abspath(__file__)), 'developer_comments.json')
	def updateAuditorComments(self):
		xl = pd.ExcelFile(self.xls_path)
		no_of_sheets = len(xl.sheet_names)

		xl_data = [pd.read_excel(self.xls_path, sheet_name=i) for i in range(no_of_sheets)]
		if isfile(self.developer_comments_file):
			with open(self.developer_comments_file, 'r') as ac:
				developer_comments = json.loads(ac.read())
				vulnerable_jars = developer_comments.keys()
		else:
			vulnerable_jars, developer_comments = [], {}
		for sheet_data in xl_data:
			for i in range(len(sheet_data)):
				jar = sheet_data.loc[i, 'DependencyName']
				if jar not in vulnerable_jars:
					if sheet_data.loc[i, 'CVE'].lower() != "no vulnerability":
						issue = self.jar_template.format(
							jarName=jar,
							CVEID=sheet_data.loc[i, 'CVE'],
							Status=sheet_data.loc[i, 'Status'],
							Comment=sheet_data.loc[i, 'Developer Comment']
						)
						developer_comments.update(json.loads(issue))
						print(issue)
				else:
					jar_data = developer_comments.get(jar)
					cve = sheet_data.loc[i, 'CVE']
					if cve.lower() != "no vulnerability":
						if cve not in jar_data.keys():
							issue = self.cve_template.format(
								CVEID=cve,
								Status=sheet_data.loc[i, 'Status'],
								Comment=sheet_data.loc[i, 'Developer Comment']
							)
							print(issue)
						else:
							issue = self.cve_template.format(
								CVEID=cve,
								Status=sheet_data.loc[i, 'Status'],
								Comment=sheet_data.loc[i, 'Developer Comment']
							)
						jar_data.update(json.loads(issue))
						developer_comments[jar] = jar_data
			with open(self.developer_comments_file, 'w') as acb:
				acb.write(json.dumps(developer_comments, indent=4))

if __name__ == "__main__":
	xls_file_list = argv[1].split("\\")
	xls_file_list.insert(1, sep)
	UpdateJsonFile(xls_file_path=xls_file_list).updateAuditorComments()
