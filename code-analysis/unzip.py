import zipfile
import os

def extract_coding_files(zip_path):
    # List of common coding file extensions
    CODING_EXTENSIONS = [
    '.py', '.java', '.cpp', '.c', '.cs', '.js', '.ts', '.html', '.css', '.php', '.rb',
    '.go', '.rs', '.swift', '.kt', '.sql', '.xml', '.json', '.yml', '.yaml'
        ]
    
    extract_to = './unzipped_files'
    # Check if the zip file exists
    if not os.path.exists(zip_path):
        print(f"The file {zip_path} does not exist.")
        return

    # Create the extraction directory if it doesn't exist
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    # Extract only coding files
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if any(file.endswith(ext) for ext in CODING_EXTENSIONS):
                zip_ref.extract(file, extract_to)
                print(f"Extracted: {file}")
    
    return extract_to
    


