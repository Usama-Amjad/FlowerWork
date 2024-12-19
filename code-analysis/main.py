from unzip import extract_coding_files
from linters import code_analysis


zipped_folder='file.zip'

unzipped_folder=extract_coding_files(zipped_folder)

code_analysis(unzipped_folder)