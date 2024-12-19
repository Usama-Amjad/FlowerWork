import os
import shutil
def find_required_file(root_dir,file_ext):
    found=False
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(file_ext):
                found=True
    return found

def find_required_folder(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for dir in dirs:
            if dir.lower().endswith(".tests")  or dir.lower().endswith(".unittests"):
                return dir
    return "Project.UnitTests"

def detect_language(project_path):
    if os.path.isfile(os.path.join(project_path, 'requirements.txt')):
        return 'Python'
    elif os.path.isfile(os.path.join(project_path, 'package.json')):
        return 'JavaScript'
    elif os.path.isfile(os.path.join(project_path, 'pom.xml')):
        return 'Java'
    elif os.path.isfile(os.path.join(project_path, 'Cargo.toml')):
        return 'Rust'
    elif find_required_file(project_path,".csproj"):
        return 'C#'
    else:
        return None
    
def test_file_copy(project_path,test_file_path):
    if language == 'Java':
        shutil.copy(test_file_path, project_path+'/src/test/java')
    elif language == 'Rust':
        shutil.copy(test_file_path, project_path+'/src')
    elif language == 'C#':
        project_path_edit=find_required_folder(project_path)
        shutil.copy(test_file_path, project_path_edit)
    else:
        shutil.copy(test_file_path, project_path)