from os.path import join
from os.path import dirname
from os.path import abspath
from os.path import isfile
from json import loads
from sys import exit as sysexit

class Comments:

    def __init__(self):
        self.auditor_comments_file = join(dirname(abspath(__file__)), 'auditor_comments.json')
    
    def readAuditorCommentsFile(self):
        if isfile(self.auditor_comments_file):
            try:
                with open(self.auditor_comments_file, 'r') as rb:
                    comments_data = loads(rb.read())
            except Exception as e:
                comments_data = {}
                print("[Error] Unable to read auditor comments file make sure file avaliable at Utils folder..")
                sysexit(e)
        else:
            comments_data = {}
            sysexit("[Error] Unable to read auditor comments file make sure file avaliable at Utils folder..")
        return comments_data