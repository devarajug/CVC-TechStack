from io import BytesIO
from re import compile
from sys import exit as sysexit
from sys import argv
from requests import Session
from requests.auth import HTTPProxyAuth
from warnings import filterwarnings
from shutil import rmtree
from subprocess import check_output
from packaging import version
from bs4 import BeautifulSoup
from zipfile import ZipFile
from os.path import join
from os.path import dirname
from os.path import abspath
from os.path import isdir


class CheckUpdateVersionOfDCT:
    def __init__(self, proxyname=None, proxyport=None, proxyuser=None, proxypass=None):
        self.dct_url = "https://owasp.org/www-project-dependency-check/"
        self.dct_system_path = join(dirname(dirname(abspath(__file__))), 'dependency-check', 'bin', 'dependency-check.bat')
        self.proxyusername = proxyuser
        self.proxypassword = proxypass
        self.proxyname = proxyname
        self.proxyport = proxyport
        self.local_dct_version = None
        self.web_dct_version = None
        self.status = False

    def getDCTDataFromWeb(self, url):
        try:
            request = Session()

            if self.proxyusername and self.proxypassword:
                proxies = {
                    "http": "http://"+str(self.proxyname)+":"+str(self.proxyport),
                    "https": "https://"+str(self.proxyname)+":"+str(self.proxyport)
                }
                auth = HTTPProxyAuth(self.proxyusername, self.proxypassword)
                request.proxies = proxies
                request.auth = auth
            request.verify = False
            data = request.get(url=url)
        except Exception as e:
            data = None
            print("error in getDataFromWeb method.......")
            sysexit(e)
        return data

    def updateDCT(self, parsed_dct_data):
        try:
            dct_path = dirname(dirname(self.dct_system_path))
            print('[INFO] Upgrading Dependency Check Tool ....')
            dct_download_url = parsed_dct_data.select("div[role=complementary] ul li a[href]")[0].get('href')
            dct_data = self.getDCTDataFromWeb(dct_download_url)
            if dct_data.ok:
                if isdir(dct_path):
                    rmtree(dct_path)
                    with ZipFile(BytesIO(dct_data.content), 'r') as zf:
                        zf.extractall(path=dirname(dct_path))
                        self.status = True
                print('[INFO] Uprade Completed ......')
            else:
                sysexit("[INFO] Unable to download new version dct url may worng download it manually......")

        except Exception as e:
            sysexit(e)
        return self.status

    def versionCheck(self):
        try:
            self.local_dct_version = check_output([self.dct_system_path, '--version'], universal_newlines=True).strip('\n').split(' ')[-1]
            dct_data = self.getDCTDataFromWeb(self.dct_url)
            parsed_dct_data = BeautifulSoup(dct_data.text, 'lxml')
            self.web_dct_version = parsed_dct_data.find(string=compile('''Version \\d+(?:\\.\\d+)+''')).split(" ")[-1]
            if version.parse(self.web_dct_version) > version.parse(self.local_dct_version):
                print()
                print("[Warn] Currently you are using lower version of Dependency Check Tool("+self.local_dct_version+").")
                print("[Warn] There is Higher version of Dependency Check Tool("+self.web_dct_version+") is avaliable in web.")
                print()
                self.updateDCT(parsed_dct_data)
            else:
                print()
                print("[Info] Checking Update for DCT is completed.")
                print("[Info] Already you are using higher version DCT.")
                print()
        except Exception as e:
            sysexit(e)

        return ""


if __name__ == "__main__":

    filterwarnings("ignore")

    if len(argv[1:]):
        proxyname = argv[1]
        proxyport = argv[2]
        proxyuser = argv[3]
        proxypass = argv[4]
        check = CheckUpdateVersionOfDCT(proxyname, proxyport, proxyuser,proxypass)
    else:
        check = CheckUpdateVersionOfDCT()
    check.versionCheck()