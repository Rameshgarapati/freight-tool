import requests
import time
import json
import os

token = ''
filename = ''   
payload1 = "grant_type=client_credentials&client_id=l7bd8b1643115b499198691fcc2ccd5edd&client_secret=535b361d-7625-4757-832e-8a7498b9eef9"
url1 = "https://apis.fedex.com/oauth/token"

headers1 = {
    'Content-Type': "application/x-www-form-urlencoded"
    }

def read_token_file(filename):
    """
    Reads the token from the specified file.

    Args:
        filename (str): Path to the token file.

    Returns:
         str: The token read from the file.
    """
        
    try:
        with open(filename, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
        

def update_token_file(filename, token):
    """
    Updates the token in the specified file.

    Args:
        filename (str): Path to the token file.
        token (str): The new token to write to the file.
    """
    try:
        with open(filename, "w") as file:
            file.write(token)
        print(f"Token updated in '{filename}'.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

import os

def check_folder_and_set_variable():
    folder_path = os.getcwd()
   
    tkn = "token"
    

    """
    Checks if a folder is empty. If not empty, compares file names with the provided token.
    If a file name starts with the token, sets the variable to 1. Otherwise, sets it to 0.

    Args:
        folder_path (str): Path to the folder to check.
        tkn (str): The token to compare with file names.

    Returns:
        int: The variable value (1 or 0).
    """
    if os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        if not files:
            print("The folder is empty.")
            return 0
        else:
            for file in files:
                if file.startswith(tkn):
                    return 1
            return 0
    else:
        print("The provided path is not a valid directory.")
        return 0

    # Example usage




def check_folder_and_run_code(file_check):

    folder_path = os.getcwd()
   
    tkn = "token"

    """
    Checks if a folder is empty. If not empty, compares file names with the provided token.
    If a file name starts with the token, it skips the file. Otherwise, it runs the provided Python code.

    Args:
        folder_path (str): Path to the folder to check.
        token (str): The token to compare with file names.
        code_to_run (str): Python code to run if the folder is not empty and no file name starts with the token.
    """
    if os.path.isdir(folder_path):


        if file_check == 1:


            for file in os.listdir(folder_path):
                if file.startswith(tkn):
                    timestamp = int(file.split("_")[1].split(".")[0])
                    current_time = int(time.time())
                    elapsed_time = current_time - timestamp
                    print(elapsed_time)
                    if elapsed_time >= 3600:
                        new_timestamp = int(time.time())
                        response1 = requests.request("POST", url1, data=payload1, headers=headers1)
                        token = json.loads(response1.text)['access_token']
                        new_filename = f"token_{new_timestamp}.txt"
                        update_token_file(new_filename, token)
                        os.remove(file)
                        return token
                    else:
                        print(file)
                        token = read_token_file(file)
                        return token
                        print(token)


        else:
            response1 = requests.request("POST", url1, data=payload1, headers=headers1)
            token = json.loads(response1.text)['access_token']
            timestamp = int(time.time())
            filename = f"token_{timestamp}.txt"
            with open(filename, "w") as file:
                file.write(token)
            return token
                 
