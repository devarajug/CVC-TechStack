from warnings import filterwarnings
from sys import argv
from os.path import dirname
from os.path import abspath
from sys import exit as sysexit
from requests import Session
from requests.auth import HTTPProxyAuth
from bs4 import BeautifulSoup
from zipfile import ZipFile
from io import BytesIO

class DCTDownload:

    def __init__(self, proxyname=None, proxyport=None, proxyuser=None, proxypass=None):
        self.dct_url = "https://owasp.org/www-project-dependency-check/"
        self.installation_path = dirname(dirname(abspath(__file__)))
        self.proxyname = proxyname
        self.proxyport = proxyport
        self.proxyuser = proxyuser
        self.proxypass = proxypass
    
    def getDCTDataFromWeb(self, url):
        try:
            request = Session()
            if self.proxypass and self.proxyuser:
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
            print("error in getDataFromWeb method.......")
            sysexit(e)
        return data
    
    def installDCT(self):
        try:
            print('[INFO] Installing Dependency Check Tool ....')
            dct_data = self.getDCTDataFromWeb(self.dct_url)
            parsed_dct_data = BeautifulSoup(dct_data.text, 'lxml')
            dct_download_url = parsed_dct_data.select("div[role=complementary] ul li a[href]")[0].get('href')
            dct_data = self.getDCTDataFromWeb(dct_download_url)
            if dct_data.ok:
                with ZipFile(BytesIO(dct_data.content), 'r') as zf:
                    zf.extractall(path=self.installation_path)
                print('[INFO] Installation Completed ......')
            else:
                sysexit("[INFO] Unable to download new version dct url may worng download it manually......")
        except Exception as e:
            sysexit("[INFO] Unable to download new version dct url may worng download it manually......"+str(e))

if __name__ == "__main__":

    filterwarnings("ignore")

    if len(argv[1:]):
        proxyname = argv[1]
        proxyport = argv[2]
        proxyuser = argv[3]
        proxypass = argv[4]
        dct = DCTDownload(proxyname, proxyport, proxyuser,proxypass)
    else:
        dct = DCTDownload()
    dct.installDCT()