import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="✊ 신박한 가위바위보", layout="centered")

st.title("🎮 신박한 가위바위보 게임")
st.markdown("가위✌️, 바위✊, 보✋ 중 하나를 골라 컴퓨터와 대결해보세요!")

# 선택 버튼
col1, col2, col3 = st.columns(3)
user_choice = None

with col1:
    if st.button("✌️ 가위"):
        user_choice = "가위"
with col2:
    if st.button("✊ 바위"):
        user_choice = "바위"
with col3:
    if st.button("✋ 보"):
        user_choice = "보"

# 선택된 경우 처리
if user_choice:
    computer_choice = random.choice(["가위", "바위", "보"])
    emojis = {"가위": "✌️", "바위": "✊", "보": "✋"}

    st.markdown("---")
    st.markdown("### 🌀 가위... 바위... 보!!")
    with st.spinner("결과를 확인 중..."):
        time.sleep(1.2)

    st.markdown(f"#### 🙋‍♂️ 당신: **{user_choice} {emojis[user_choice]}**")
    st.markdown(f"#### 🤖 컴퓨터: **{computer_choice} {emojis[computer_choice]}**")

    # 승패 판단
    if user_choice == computer_choice:
        result = "🤝 비겼어요!"
        comment = random.choice(["오! 서로 생각이 같았네요!", "다시 한번!", "무승부입니다!"])
    elif (user_choice == "가위" and computer_choice == "보") or \
         (user_choice == "바위" and computer_choice == "가위") or \
         (user_choice == "보" and computer_choice == "바위"):
        result = "🎉 승리!"
        comment = random.choice(["이겼어요! 멋져요!", "와우, 전략 성공!", "승리를 축하해요!"])
    else:
        result = "💥 패배..."
        comment = random.choice(["앗, 아쉽네요!", "다음엔 이겨봅시다!", "컴퓨터가 강하군요..."])

    st.markdown("## " + result)
    st.markdown(f"##### 💬 {comment}")


