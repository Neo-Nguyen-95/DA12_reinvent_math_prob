#%% LIBRARY
import numpy as np
from itertools import product

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
        float(var_range_input[1]), 
        float(var_range_input[2])
        )
    
    # Place value in the value list dictionary
    value_list[var_list[i]] = var_range
    
# HOW TO GET ALL COMBINATION FROM A DICTIONARY????


#%% PREVIOUS VERSION

#%% CALCULATE VALUES
# function to display 1 case
def generate_output():
    word_list_temp = word_list.copy()
    for i in range(len(word_list_temp)):
        try:
            computation = eval(word_list_temp[i])
            word_list_temp[i] = str(computation)  
        except:
            pass
    output_text = " ".join(word_list_temp)
    print(output_text)

# print all cases
for globals()[var_list[0]] in list_1:
    if len(list_2) > 0:
        for globals()[var_list[1]] in list_2:
            if len(list_3) > 0:
                for globals()[var_list[2]] in list_3:
                    generate_output()
            else:
                generate_output()
    else:
        generate_output()
        