import os
import zipfile
import subprocess
from imageAnalysers import nn
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Function to check the website with the mockup
def webCheck(mockUp,url):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-fullscreen")  # Fullscreen mode
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.save_screenshot('images/Screenshot.png')

    score = nn(mockUp,'images/Screenshot.png')

    if score > 0.7:
        print('Mockup is matched with the website')
        print('Score:',score)
    else:
        print('Mockup is not matched with the website')
        print('Score:',score)

def nonWebCheck(image1,image2):
    score = nn(image1,image2)

    if score > 0.7:
        print('Images matched')
        print('Score:',score)
    else:
        print('Images did not matched')
        print('Score:',score)

def handle_project_submission(zip_path):

    project_path = os.path.join('projects')

    # Step 1: Extract the project
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(project_path)
    
    # Step 2: Install dependencies
    result = subprocess.run(['npm.cmd', 'install'], cwd=project_path,capture_output=True,shell=True)

    if "npm audit fix" in str(result.stdout):
        subprocess.run(['npm.cmd', 'audit', 'fix'], cwd=project_path,shell=True) 

    # Step 3: Start the React appcl
    subprocess.Popen(['npm.cmd','run','dev'], cwd=project_path)

    # Step 4: Open in Chrome
    webCheck('images/Screenshot.png',"http://localhost:5174/")

handle_project_submission('project.zip')