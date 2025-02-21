#%% LIBRARY
import streamlit as st
import numpy as np
import itertools
from openai import OpenAI
import time
 
#%% INTRO
# set page config
st.set_page_config(
    page_title = 'Problem Generator',
    page_icon = '🧮'
    )


st.title("SIMILAR PROBLEM GENERATOR (POWERED BY AI 🤖)")

#%% SIDE BAR INFOR - INPUT
option_api = st.sidebar.radio(
    label='Thầy/cô chọn chế độ sử dụng API', 
    options=['OPENAI API mặc định', 'OPENAI API cá nhân'],
    index=0
    )

if option_api == 'OPENAI API cá nhân':
    api_key = st.sidebar.text_input(
        "Nhập OPENAI API KEY của AI của thầy/cô",
        type="password"
        )
    max_token_out = None
    max_token_in = None
    wait_time = 0
else:
    api_key = st.secrets["api"]["key"]
    max_token_in = 1000
    max_token_out = 1000
    st.sidebar.write(f"Số lượng từ tối đa cho câu hỏi: {max_token_in}")
    st.sidebar.write(f"Số lượng từ tối đa cho câu trả lời: {max_token_out}")
    wait_time = 5
    st.sidebar.write(f"Thời gian chờ kết quả là {wait_time}s")
    
st.sidebar.markdown("""
---
Thầy/cô có thể trả phí và sử dụng OPENAI API tại 
[trang chủ của OPENAI](https://platform.openai.com/).
""")

# Credit
st.sidebar.markdown("""
---
**Credit**
- Idea by Ms. Trâm & Ms. Quỳnh Anh
- Developed by Neo
""")

#%% INTRODUCTION
st.markdown("""
            ## GIỚI THIỆU
            """) 

st.markdown("""
Xin chào thầy/cô đến với ứng dụng sinh câu hỏi toán tương tự bằng AI.
Dưới đây là nguyên lí hoạt động của hệ thống. Đảm bảo khắc phục được yếu điểm 
trong suy luận toán học của AI khi tạo đề mới.
""")


st.image("Principle.png")

st.markdown("""
Về cơ bản, thầy cô vẫn cần đảo bảo các con số trong bài là hợp lí và chính xác, AI 
chỉ hỗ trợ thầy cô tạo ra các bối cảnh mới với số liệu sẵn có.
            """)

#%% USER GUIDE
st.markdown("""
            ## HƯỚNG DẪN SỬ DỤNG
            """) 
            
st.video('https://youtu.be/9MUe0Fi8nao')

st.markdown("""
Trước tiên, thầy cô cần chuẩn bị đề nguyên lí, bao gồm các biến và nguyên lí tính 
toán của đáp án. 
- Các biến và công thức tính toán trong bài cần để ở giữa dấu gạch dưới '_'. 
- *Ví dụ: Bạn A có \\_x\\_ quả cam, Bạn B có \\_y\\_ quả cam.*, hai bạn có tổng 
\\_x+y\\_ quả cam => hệ thống tự động sẽ nhận diện x, y, và tính ra x+y
- Số mũ cấp số nhân không sử dụng ^ mà sử dụng kí hiệu \\*\\*. *Ví dụ: a mũ x sẽ viết là a \\*\\* x*
            """)

with st.expander("Click để xem đề mẫu - Đơn giản"):
    st.code("""
Nhà bạn An nuôi _a_ con gà. Nhà bạn Bình nuôi _b_ con gà. Hai bạn rủ nhau góp 
gà cùng nuôi. Sau 2 tuần, có thêm 1 con gà con.

Hai bạn đang có bao nhiêu con gà?   
    
    A. _a+b+1_ con gà
    
    B. _a*b+1_ con gà
    
    C. _a+b-1_ con gà
    
    D. _a*b-1_ con gà
    
Đáp án: _a+b+1_ con gà
    """
    )

with st.expander("Click để xem đề mẫu - Trung bình"):
    st.code("""
Một người thả rơi một hòn bi từ trên cao xuống đất và đo được 
thời gian rơi là _t_ s. Bỏ qua sức cản không khí. Lấy g = _g_ $m/s^2$. 
Độ cao của nơi thả hòn bi so với mặt đất và vận tốc lúc chạm đất là: 
    
    A. _1 / 2 * g * (t ** 2)_ 
    
    B. _1 / 2 * g * t_ 
    
    C. _g * (t ** 2)_ 
    
    D. _2 * g * (t ** 2)_    
             
Đáp án: _1 / 2 * g * (t ** 2)_"""
    )

        
with st.expander("Click để xem đề mẫu - Phức tạp"):
    st.code("""
Khu vườn nhà bác An có chiều dài gấp _k_ lần chiều rộng. Bác muốn mở rộng 
khu vườn bằng cách cùng tăng chiều dài và chiều rộng thêm _a_ m. Khi đó, 
khu vườn mới của bác có diện tích bằng _b_ m^2. Bác sử dụng dây thép gai 
để chắn xung quanh khu vườn của mình, cứ 1 m đường biên vườn cần sử dụng 
3 m dây thép gai. 
Vậy sau khi mở rộng diện tích khu vườn, số m dây thép gai bác cần dùng là … m.
    
Đáp án:
Số m dây thép gai cần dùng là: _(((-(a+a*k) + np.sqrt((a+a*k)**2 - 4*k*(a**2-b))) / (2*k))+k*((-(a+a*k) + np.sqrt((a+a*k)**2 - 4*k*(a**2-b))) / (2*k))+2*a)*2*3_
Số m dây thép gai cần dùng là: _(((-(a+a*k) - np.sqrt((a+a*k)**2 - 4*k*(a**2-b))) / (2*k))+k*((-(a+a*k) - np.sqrt((a+a*k)**2 - 4*k*(a**2-b))) / (2*k))+2*)*2*3_
    """
    )
        
st.markdown("""
Sau khi đã chuẩn bị đề nguyên lí, thầy cô chỉ việc nhập vào app vào làm theo các 
bước mà phần mềm yêu cầu để tạo các đề tương tự.
            """)
        
st.markdown("""---""") 
    
st.markdown("""
            ## Bước 1: Nhập đề nguyên lí
            """) 
            
input_text = st.text_input("Nhập đề của thầy/cô tại đây:").strip()
#%% PROCESS

if input_text:
    with st.expander("Click để xem lại đề nguyên lí"):
        st.markdown(input_text)
    
    word_list = input_text.split("_")

    # detect principal variable
    var_list = [word for word in list(set(word_list)) if len(word) == 1]
    
    value_list = dict()

    st.write("Nhập khoảng giá trị cho từng biến theo hướng dẫn.")
    nature_number = st.checkbox(label="Sử dụng số nguyên")
    if nature_number:
        default_value = 0
    else:
        default_value = 0.0
    
   
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
            value=default_value
            )
        max_val[i] = col3.number_input(
            "Giá trị lớn nhất", 
            key = var_list[i] + "max",
            value=default_value+1
            )
        step_val[i] = col4.number_input(
            "Khoảng cách",
            key = var_list[i] + "step",
            value=default_value+1
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
                if nature_number:
                    computation = int(computation)
                else:
                    computation = str(computation).replace('.', ',')
                
                word_list_temp[i] = str(computation)  
            except:
                pass
        output_text = " ".join(word_list_temp)
        print(output_text)
        result += "\n" + output_text
    

    type_message = 'Nếu câu hỏi có dạng multiple-choice/trắc nghiệm \
            một lựa chọn. Các phương án trong câu hỏi \
            cần sắp xếp theo thứ tự tăng dần. '
    
    
    guide_message = "Tạo đề bài mới từ đề bài sau đây, sử dụng đa dạng phong phú \
        các loại bối cảnh nhưng giữ nguyên số liệu trong bài tập. \
        Ngoài đề bài và đáp án, bổ sung thêm gợi ý cách làm cho từng câu hỏi nếu học sinh \
        làm sai. Giữ nguyên dạng câu hỏi."
        
    # %% USE AI TO GENERATE NEW CONTEXT FOR EACH PROBLEM
    st.markdown("""---""") 
    st.markdown("""
                ## Bước 2: Tạo bài tập tương tự
                """)
    
    if st.button("Tạo đề mới từ bộ tham số đã nhập"):
        
        if option_api == "OPENAI API mặc định":
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.write("Loading")
            time.sleep(wait_time/5)
            col2.write("...")
            time.sleep(wait_time/5)
            col3.write("...")
            time.sleep(wait_time/5)
            col4.write("...")
            time.sleep(wait_time/5)
            col5.write("...")
            time.sleep(wait_time/5)
            col6.write("...")
            time.sleep(wait_time/5)

    
        client = OpenAI(api_key=api_key)
    
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages = [
                    {"role": "system", 
                     "content": "Bạn là giáo viên dạy toán ở Việt Nam, kiến thức của bạn \
                    là từ chương trình giáo dục phổ thông tại Việt Nam, sử dụng ngôn từ \
                    thân thiện, khoa học và phù hợp văn hoá Việt Nam. Công thức \
                    Toán học cần để ở giữa $ $. " + type_message + guide_message
                     },
                    {"role": "user", 
                     "content": result[:max_token_in]
                     }
                ],
            max_tokens = max_token_out
            )
            
        tab1, tab2 = st.tabs(["Văn bản đã xử lí", "Kí tự gốc"])
        
        with tab1:
            st.write(response.choices[0].message.content)
        with tab2:
            st.code(response.choices[0].message.content)
            
        if option_api == "OPENAI API mặc định":
            st.markdown(f"""
                        **Thầy/cô đã đạt giới hạn {max_token_out} từ cho câu trả lời!**
                        """)