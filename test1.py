import streamlit as st
import random

st.set_page_config(page_title="✊ 가위바위보 게임", layout="centered")

st.title("✊ 가위바위보 게임")
st.markdown("### 버튼을 눌러 선택하세요!")

choices = {"가위 ✌️": "가위", "바위 ✊": "바위", "보 ✋": "보"}
emoji_choices = {"가위": "✌️", "바위": "✊", "보": "✋"}
user_choice = None

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("가위 ✌️"):
        user_choice = "가위"
with col2:
    if st.button("바위 ✊"):
        user_choice = "바위"
with col3:
    if st.button("보 ✋"):
        user_choice = "보"

if user_choice:
    computer_choice = random.choice(["가위", "바위", "보"])

    st.markdown("---")
    st.markdown(f"👤 당신의 선택: **{user_choice} {emoji_choices[user_choice]}**")
    st.markdown(f"💻 컴퓨터의 선택: **{computer_choice} {emoji_choices[computer_choice]}**")

    # 승패 결정
    if user_choice == computer_choice:
        result = "😐 비겼습니다!"
    elif (user_choice == "가위" and computer_choice == "보") or \
         (user_choice == "바위" and computer_choice == "가위") or \
         (user_choice == "보" and computer_choice == "바위"):
        result = "🎉 당신이 이겼습니다!"
    else:
        result = "💥 컴퓨터가 이겼습니다!"

    st.markdown(f"## {result}")

