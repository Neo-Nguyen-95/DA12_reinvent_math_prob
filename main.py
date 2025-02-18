#%% LIBRARY
import streamlit as st

#%% INTRO
st.title("MATH PROBLEM GENERATOR (POWERED BY AI BUDDY)")

#%% INPUT
option_api = st.sidebar.radio(
    label='Thầy/cô chọn chế độ sử dụng API', 
    options=['API mặc định', 'API cá nhân'],
    index=1
    )

if option_api == 'API cá nhân':
    api_key = st.sidebar.text_input("Nhập API KEY của AI của thầy/cô ")
else:
    api_key = st.secrets["api"]["key"]
    max_token = 400
    st.sidebar.write(f"Số lượng từ tối đa cho câu trả lời: {max_token}")

st.markdown("""
Xin chào thầy/cô đến với ứng dụng sinh câu hỏi toán tương tự bằng AI.

Trước khi tạo đề tương tự, thầy/cô lưu ý:
                
- Thầy/cô cần nhập nguyên lí hình thành số và đáp án vào phần mềm
                
- Phần mềm sẽ tạo ra các đề với bối cảnh mới, nhưng số sẽ tuân theo quy luật mà \
                    thầy/cô đã thiết lập.
                    
- Các biến và công thức tính toán trong bài cần để ở giữa dấu gạch dưới '_'.
            """)
st.text(r"Ví dụ: bạn A có _x_ quả ")
            
with st.expander("Click để xem đề mẫu"):
    st.markdown("""---""")
    st.write("**Đề khi input vào phần mềm:**")
    st.text(r"""Một người thả rơi một hòn bi từ trên cao xuống đất và đo được 
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
    st.markdown("""Một người thả rơi một hòn bi từ trên cao xuống đất và đo được thời gian rơi \nlà  1.0  s. Bỏ qua sức cản không khí. Lấy g =  9.0  $m/s^2$. \n Độ cao của nơi thả hòn bi so với mặt đất và vận tốc lúc chạm đất là:\n
A.  4.5 \n
B.  4.5 \n
C.  9.0 \n
D.  18.0 \n
Gợi ý công thức: $h = \\frac{1}{2} a t^2$ \n
Đáp án:  4.5"""
                )
#%% OUTPUT
