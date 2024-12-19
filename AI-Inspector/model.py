from langchain_community.llms import Ollama
from Dataloader import loader as ld

def model(filePath,project_description,user_guidlines):
    print("model is called")
    # Model
    model = Ollama(model='codechecker')

    # Extracting code from a file
    code = ld(filePath)

    # Projext Describtion
    project_description=project_description

    # User Guidlines
    user_guidlines=user_guidlines

    # Prompt
    prompt = """
        You are an AI code checker that Reviews and check whether the submitted code is according to the project description and matches the details.For correcteness you will Run unit test by yourself with real examples and verify results.User may also provide specific code guidelines and principles so you have to check whether the provided code meet the principles and guidelines.Respond as yes or no if the program is correct or incorrect,respectively,and if it is wrong then only then give all the fixes once.
        Keep it simple,short and concise.
    """

    # Complete Template COntaing all informations
    template = f"""
    # prompt:
    # {prompt}

    Project Description:
    {project_description}

    Principles:
    {user_guidlines}

    Provided Code:
    {code}
        """
    # Passing Template and waiting for response
    print(template)
    print("Generating response")
    response = model(template)

    print(response)

    return response

model('./files/app.cpp','python Program to find the area of triangle','')