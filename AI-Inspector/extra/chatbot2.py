# import openai
# import os
# import json

# TOGETHER_API_KEY = '7e97ff7f3faff372d7495d30944efed8c1e4da93d93e5f100a1e42d51bb31ca9'

# client = openai.OpenAI(
#     api_key=TOGETHER_API_KEY,
#     base_url="https://api.together.xyz/v1",
# )

# def get_code_completion(messages, max_tokens=512, model="codellama/CodeLlama-70b-Instruct-hf"):
#     chat_completion = client.chat.completions.create(
#         messages=messages,
#         model=model,
#         max_tokens=max_tokens,
#         stop=[
#             "<step>"
#         ],
#         frequency_penalty=1,
#         presence_penalty=1,
#         top_p=0.7,
#         n=10,
#         temperature=0.7,
#     )
 
#     return chat_completion

# messages = [
#       {
#             "role": "system",
#             "content": "You are an expert programmer that helps to write Python code based on the user request, with concise explanations. Don't be too verbose.",
#       },
#       {
#             "role": "user",
#             "content": "Write a python function to add two numbers.",
#       }
# ]
 
# chat_completion = get_code_completion(messages)
            
# print(chat_completion.choices[0].message.content)

# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# @app.route('/square/<int:n>')
# def square(n):
#     return str(n**2)

# if __name__=="__main__":
#     app.run(debug=True)