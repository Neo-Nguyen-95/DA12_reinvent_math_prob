#%% LIBRARY
import numpy as np
import itertools
from openai import OpenAI
import os
from dotenv import load_dotenv

#%% INPUT WITH RIGHT FORMAT
# So far, accept up to 3 variables

input_text = input("Nhập đề bài với mẫu chuẩn của phần mềm: ")

word_list = input_text.split("_")

# detect principal variable
var_list = [word for word in word_list if len(word) == 1]

print(f"Bài tập có {len(var_list)} tham số: {var_list}")  # confirm message

#%% CREAT RANGE
value_list = dict()

for i in range(len(var_list)):
    # Range for a variable
    var_range_input = input(f"Nhập giá trị min, max, step cho biến {var_list[i]}: ")
    var_range_input = var_range_input.split(" ")
    
    # Generate value from the range info
    var_range = np.arange(
        float(var_range_input[0]), 
        float(var_range_input[1])+1, 
        float(var_range_input[2])
        )
    
    # Place value in the value list dictionary
    value_list[var_list[i]] = var_range
    
# Get all combination from the value ranges
combinations = list(itertools.product(*value_list.values()))
# print(combinations)  # Test the result

#%% GET NEW PROBLEMS WITH GENERATED VALUES

result = []

for combination in combinations:
    for i in range(len(var_list)):
        globals()[var_list[i]] = combination[i] 
    
    word_list_temp = word_list.copy()
    for i in range(len(word_list_temp)):
        try:
            computation = eval(word_list_temp[i])
            word_list_temp[i] = str(computation)  
        except:
            pass
    output_text = " ".join(word_list_temp)
    print(output_text)
    result.append(output_text)

#%% USE AI TO GENERATE NEW CONTEXT FOR EACH PROBLEM

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages = [
            {"role": "system", "content": "You are a math tutor."},
            {"role": "user", "content": "Give me a tip to learn math"}
        ]
    )

response.choices[0].message.content
        