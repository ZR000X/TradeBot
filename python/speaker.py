import pprint, csv

class Speaker:
    def __init__(self, filename: str):
        self.filename = filename
        file = open(filename, 'w', newline='')
        self.csvWriter = csv.writer(file, delimiter=' ')
        self.pp = pprint.PrettyPrinter(indent=4)
    
    def say(self, msg):
        self.pp.pprint(msg)
        self.csvWriter.writerow([self.pp.pformat(msg)])