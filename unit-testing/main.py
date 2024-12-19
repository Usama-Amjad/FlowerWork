import subprocess
from helpers import detect_language,test_file_copy

def running_test_file(mode,project_path,test_file_path):
    # detect language
    language = detect_language(project_path)
    
    # For client the test file will be added to the project folder
    if mode == True :
        test_file_copy(project_path,test_file_path)
        
    # Running test depending on language
    if language == 'Python':
        print('running python tests')
        result = subprocess.run(['pytest'],capture_output=True,shell=True,cwd=project_path)
        if result.returncode != 0:
            print('Error/Failed to run tests')
        else:
            print("Passed all tests")

    elif language == 'JavaScript':
        print('running javascript tests')
        print("running npm test")
        result = subprocess.run(['npm', 'test'], capture_output=True, shell=True,cwd=project_path) 
        if result.returncode != 0:
            print("running jest")
            result = subprocess.run(['npx', 'jest','--passWithNoTests'], capture_output=True, shell=True,cwd=project_path)
            if "FAIL" in str(result.stderr):
                print(result.stderr.decode())

    elif language == 'Java':
        result = subprocess.run(['mvn','test'],capture_output=True,shell=True,cwd=project_path)
        if result.returncode != 0:
            print('Error/Failed to run tests')
        else:
            print("Passed all tests")
    
    elif language == 'C#':
        print('Running C# tests...')
        result = subprocess.run(['dotnet', 'test'], capture_output=True, shell=True, cwd=project_path)
        if result.returncode != 0:
            print('Error/Failed to run tests')
        else:
            print("Passed all tests")
    
    elif language == 'Rust':
        print('Running Rust tests...')
        result = subprocess.run(['cargo', 'test'], capture_output=True, shell=True, cwd=project_path)
        if result.returncode != 0:
            print('Error/Failed to run tests')
        else:
            print("Passed all tests")

    else:
        print('Language not supported for testing')

# Contractor==False,Client==True
running_test_file(False,'test-project','')  

# We have to make sure to automatically run test the test file should follow the nameing convention and the inside code should also be written in 
# the test terminology
# if in new system pip install commands for every langiuage should be added
# Make output like cmd