import sys
import glob
import subprocess
from termcolor import colored
from art import *

class Scraper:
    def __init__(self):
        print(text2art("FREF scraper"))  # ASCII Art
        self.python_files = glob.glob('./fref*.py')

    def run(self):
        for file in self.python_files:
            print(colored('Starting script: ', 'green') + colored(file, 'blue'))
            subprocess.run([sys.executable, file])
            print(colored('Finished running: ', 'green') + colored(file, 'blue'))

if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
