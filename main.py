#%% LIBRARY
import streamlit as st
import numpy as np
import itertools
from openai import OpenAI
import time
 
#%% INTRO
st.title("MATH PROBLEM GENERATOR (POWERED BY AI BUDDY)")

#%% INPUT
option_api = st.sidebar.radio(
    label='Thầy/cô chọn chế độ sử dụng API', 
    options=['API mặc định', 'API cá nhân'],
    index=1
    )

if option_api == 'API cá nhân':
    api_key = st.sidebar.text_input(
        "Nhập API KEY của AI của thầy/cô",
        type="password"
        )
    max_token = None
    wait_time = 0
else:
    api_key = st.secrets["api"]["key"]
    max_token = 400
    st.sidebar.write(f"Số lượng từ tối đa cho câu trả lời: {max_token}")
    wait_time = 5
    st.sidebar.write(f"Thời gian chờ kết quả là {wait_time}s")

st.markdown("""
Xin chào thầy/cô đến với ứng dụng sinh câu hỏi toán tương tự bằng AI.

Trước khi tạo đề tương tự, thầy/cô lưu ý:
                
- Thầy/cô cần nhập nguyên lí hình thành số và đáp án vào phần mềm
                
- Phần mềm sẽ tạo ra các đề với bối cảnh mới, nhưng số sẽ tuân theo quy luật mà \
                    thầy/cô đã thiết lập.
                    
- Các biến và công thức tính toán trong bài cần để ở giữa dấu gạch dưới '_'. \
    *Ví dụ: Bạn A có \\_x\\_ quả cam, Bạn B có \\_y\\_ quả cam.*.

- Số mũ cấp số nhân không sử dụng ^ mà sử dụng kí hiệu \\*\\*. *Ví dụ: a mũ x sẽ viết là a \\*\\* x*
            """)
            
with st.expander("Click để xem đề mẫu"):
    st.markdown("""---""")
    st.write("**Đề khi input vào phần mềm:**")
    st.text("""Một người thả rơi một hòn bi từ trên cao xuống đất và đo được 
thời gian rơi là _t_ s. Bỏ qua sức cản không khí. Lấy g = _g_ $m/s^2$. 
Độ cao của nơi thả hòn bi so với mặt đất và vận tốc lúc chạm đất là: 
A. _1 / 2 * g * (t ** 2)_ 
B. _1 / 2 * g * t_ 
C. _g * (t ** 2)_ 
D. _2 * g * (t ** 2)_ 
Gợi ý công thức: $h = \\frac{1}{2} a t^2$ 
Đáp án: _1 / 2 * g * (t ** 2)_"""
    )
        
    st.markdown("""---""")    
    st.write("**Đề khi hiển thị với học sinh trên ứng dụng LMS:**")
    st.markdown("""Một người thả rơi một hòn bi từ trên cao xuống đất và đo được thời gian rơi \nlà  2.0  s. Bỏ qua sức cản không khí. Lấy g =  9.0  $m/s^2$. \n Độ cao của nơi thả hòn bi so với mặt đất và vận tốc lúc chạm đất là:\n
A.  18.0 \n
B.  9.0 \n
C.  36.0 \n
D.  72.0 \n
Gợi ý công thức: $h = \\frac{1}{2} a t^2$ \n
Đáp án:  18.0"""
                )
    
st.markdown("""
            ## Bước 1: Nhập đề nguyên lí
            """)
            
input_text = st.text_area("Nhập đề của thầy/cô tại đây:")
#%% PROCESS

if input_text:
    with st.expander("Click để xem lại đề nguyên lí"):
        st.markdown(input_text)
    
    word_list = input_text.split("_")

    # detect principal variable
    var_list = [word for word in word_list if len(word) == 1]
    
    value_list = dict()

    st.write("Nhập khoảng giá trị cho từng biến theo hướng dẫn.")
   
    min_val = dict()
    max_val = dict()
    step_val = dict()
   
   
    for i in range(len(var_list)):
        # Range for a variable
        col1, col2, col3, col4 = st.columns(4)
        col1.write(f"Khoảng giá trị của {var_list[i]}")
        min_val[i] = col2.number_input(
            "Giá trị nhỏ nhất", 
            key = var_list[i] + "min",
            value=0
            )
        max_val[i] = col3.number_input(
            "Giá trị lớn nhất", 
            key = var_list[i] + "max",
            value=1
            )
        step_val[i] = col4.number_input(
            "Khoảng cách",
            key = var_list[i] + "step",
            value=1
            )

        # Generate value from the range info
        var_range = np.arange(
            float(min_val[i]), 
            float(max_val[i])+1, 
            float(step_val[i])
            )
        
        # Place value in the value list dictionary
        value_list[var_list[i]] = var_range
        
    # Get all combination from the value ranges
    combinations = list(itertools.product(*value_list.values()))
    
    result = " "

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
        result += "\n" + output_text
        
    # %% USE AI TO GENERATE NEW CONTEXT FOR EACH PROBLEM
    
    if st.button("Tạo đề mới từ bộ tham số đã nhập"):
        
        if option_api == "API mặc định":
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.write("Loading")
            time.sleep(wait_time/5)
            col2.write(".")
            time.sleep(wait_time/5)
            col3.write(".")
            time.sleep(wait_time/5)
            col4.write(".")
            time.sleep(wait_time/5)
            col5.write(".")
            time.sleep(wait_time/5)
            col6.write(".")
            time.sleep(wait_time/5)
        
        
        user_message = "Tạo đề bài mới từ đề bài sau đây, sử dụng đa dạng phong phú \
            các loại bối cảnh nhưng phải giữ nguyên số liệu trong bài tập. \
                " + result
    
    
        client = OpenAI(api_key=api_key)
    
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages = [
                    {"role": "system", 
                     "content": "Bạn là giáo viên dạy toán ở Việt Nam, kiến thức của bạn \
                     là từ chương trình giáo dục phổ thông tại Việt Nam, sử dụng ngôn từ \
                         thân thiện, khoa học và phù hợp văn hoá Việt Nam. Công thức \
                             Toán học cần để ở giữa $ $"
                     },
                    {"role": "user", 
                     "content": user_message
                     }
                ],
            max_tokens = max_token
            )
            
        tab1, tab2 = st.tabs(["Văn bản đã xử lí", "Kí tự gốc"])
        
        with tab1:
            st.write(response.choices[0].message.content)
        with tab2:
            st.code(response.choices[0].message.content)
        
        

