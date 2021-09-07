from os import sep
from sys import argv
from os.path import join
from os.path import abspath
from os.path import dirname


class CvcScanCommand:

    def __init__(self, input_locations):
        self.cvc_command_file = join(dirname(dirname(abspath(__file__))), 'scan.bat')
        self.input_locations = input_locations
        self.scan_template = '''call ".\\dependency-check\\bin\\dependency-check.bat"^
        --project "Jile"^
        -f "JSON" -f "HTML"^
        --enableExperimental^
        --enableRetired^
        --disableAssembly^
        --prettyPrint^
        --disableYarnAudit^
        --out "%output%"^
        '''

    def generate(self):
        try:
            locations = self.input_locations.split(",")
            for i in range(len(locations)):
                location = locations[i].split("\\")
                location.insert(1, sep)
                if i != len(locations)-1:
                    self.scan_template+="--scan "+join(*location)+"^\n\t\t"
                else:
                    self.scan_template+="--scan "+join(*location)
            with open(self.cvc_command_file, 'w') as w:
                w.write(self.scan_template)
        except Exception as e:
            print("[Error] Unable to generate cvc scan bat file using inputs pls rerun script", str(e))
        return True


if __name__ == "__main__":
    input_locations = argv[1]
    command = CvcScanCommand(input_locations)
    command.generate()