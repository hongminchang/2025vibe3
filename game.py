import streamlit as st
import random
import time

st.set_page_config(page_title="🐹 두더지 타임 어택", layout="wide")

# 제목 및 설명
st.title("🐹 두더지 타임 어택!")
st.markdown("🧠 **두더지를 빠르게 클릭해 점수를 얻고, 리더보드에 이름을 올려보세요!**")
st.markdown("---")

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.start_time = None
    st.session_state.hits = []
    st.session_state.duration = 20  # 게임 시간(초)
    st.session_state.game_over = False
    st.session_state.nickname = ""
    st.session_state.playing = False
    st.session_state.leaderboard = []

# 닉네임 입력
if not st.session_state.playing:
    st.session_state.nickname = st.text_input("🎮 닉네임을 입력하세요", "Player")
    if st.button("🚀 게임 시작하기"):
        st.session_state.score = 0
        st.session_state.hits = []
        st.session_state.start_time = time.time()
        st.session_state.game_over = False
        st.session_state.playing = True

# 게임 중
if st.session_state.playing and not st.session_state.game_over:
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, int(st.session_state.duration - elapsed))

    if remaining <= 0:
        st.session_state.game_over = True
        st.session_state.playing = False

    st.markdown(f"⏱️ 남은 시간: **{remaining}초**")
    st.markdown(f"🏆 현재 점수: **{st.session_state.score}점**")
    st.markdown("---")

    # 두더지 UI
    cols = st.columns(5)
    target_index = random.randint(0, 4)

    for i, col in enumerate(cols):
        if i == target_index:
            if col.button("🐹"):
                st.session_state.score += 1
                st.session_state.hits.append(time.time() - st.session_state.start_time)
        else:
            col.markdown(" ")

# 게임 종료 화면
if st.session_state.game_over:
    st.subheader("🎉 게임 종료!")
    st.markdown(f"🔢 최종 점수: `{st.session_state.score}`")

    avg_reaction = (
        sum(st.session_state.hits) / len(st.session_state.hits)
        if st.session_state.hits else 0
    )
    st.markdown(f"⚡ 평균 반응 속도: `{avg_reaction:.2f}초`")

    # 리더보드 업데이트
    st.session_state.leaderboard.append({
        "nickname": st.session_state.nickname,
        "score": st.session_state.score,
        "reaction": avg_reaction
    })

    # 리더보드 출력
    st.markdown("---")
    st.markdown("## 🏅 리더보드 (Top 5)")
    sorted_board = sorted(
        st.session_state.leaderboard,
        key=lambda x: (-x["score"], x["reaction"])
    )
    for i, record in enumerate(sorted_board[:5], 1):
        st.markdown(
            f"**{i}. {record['nickname']}** - 점수: `{record['score']}`, 반응속도: `{record['reaction']:.2f}초`"
        )

    # 재시작 버튼
    if st.button("🔁 다시하기"):
        st.session_state.playing = False
        st.session_state.game_over = False
        st.session_state.start_time = None
        st.session_state.hits = []
        st.session_state.score = 0
