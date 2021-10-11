from os.path import join
from os.path import dirname
from os.path import abspath
from os.path import isfile
from json import loads

class Comments:

    def __init__(self):
        self.developer_comments_file = join(dirname(abspath(__file__)), 'developer_comments.json')
    
    def readAuditorCommentsFile(self):
        if isfile(self.developer_comments_file):
            try:
                with open(self.developer_comments_file, 'r', encoding='utf8') as rb:
                    comments_data = loads(rb.read())
            except Exception as e:
                comments_data = {}
                print("[Error] Unable to read auditor comments file make sure file avaliable at Utils folder..", str(e))
        else:
            comments_data = {}
            print("[Error] Unable to read auditor comments file make sure file avaliable at Utils folder..")
        return comments_data