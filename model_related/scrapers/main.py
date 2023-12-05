import glob
import subprocess
import os
import concurrent.futures

python_files = glob.glob('./fref*.py')
for file in python_files:
    subprocess.run(['python', file])


# files = glob.glob('./data/*/*.csv')
# for file in files:
#     if "_summary.csv" not in file:
#         os.remove(file)import glob
