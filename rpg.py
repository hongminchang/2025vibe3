# game.py - 아르카디아 연대기: 통합 RPG 게임 (멀티엔딩, 스킬트리, 전투, 세이브 포함)

import streamlit as st
import random
import json

# 상태 초기화
def init_game():
    st.session_state.update({
        "page": "title",
        "player": {},
        "inventory": ["치유 물약"],
        "skills": [],
        "skill_points": 3,
        "map_unlocked": ["시작 마을"],
        "quest_log": [],
        "enemy": {},
        "boss_defeated": False,
        "ending": None
    })

# 직업 능력치
def get_class_stats(cls):
    stats = {
        "전사": {"HP": 120, "MP": 30, "공격력": 15, "방어력": 10},
        "마법사": {"HP": 80, "MP": 100, "공격력": 10, "방어력": 5},
        "암살자": {"HP": 100, "MP": 40, "공격력": 13, "방어력": 8}
    }
    return stats[cls]
# 전투 함수
def battle(enemy_name, enemy_hp, enemy_attack, next_page, boss=False):
    st.subheader(f"⚔️ 전투 - {enemy_name}")
    st.progress(st.session_state.player["HP"] / 120)
    st.write(f"👤 {st.session_state.player['이름']} (HP: {st.session_state.player['HP']})")
    st.write(f"👹 {enemy_name} (HP: {enemy_hp})")
    skill = st.selectbox("🌀 사용할 스킬", ["기본 공격"] + st.session_state.skills)
    if st.button("공격 실행"):
        dmg = st.session_state.player["공격력"] + random.randint(-2, 3)
        if "화염구" in skill:
            dmg += 10
            st.session_state.player["MP"] -= 10
        enemy_hp -= dmg
        st.success(f"{enemy_name}에게 {dmg} 피해!")

        if enemy_hp > 0:
            edmg = max(1, enemy_attack - st.session_state.player["방어력"] + random.randint(-1, 2))
            st.session_state.player["HP"] -= edmg
            st.error(f"{enemy_name}의 반격! {edmg} 피해")
        else:
            st.success("전투에서 승리했습니다!")
            st.session_state.page = next_page
            if boss:
                st.session_state.boss_defeated = True

        if st.session_state.player["HP"] <= 0:
            st.session_state.page = "gameover"

# 저장/불러오기
def save_game():
    with open("save.json", "w") as f:
        json.dump(st.session_state.player, f)

def load_game():
    with open("save.json", "r") as f:
        st.session_state.player = json.load(f)
# 페이지 구성
if "page" not in st.session_state:
    init_game()

st.set_page_config(page_title="RPG: 아르카디아 연대기", layout="centered")

# 타이틀
if st.session_state.page == "title":
    st.title("🎮 아르카디아 연대기")
    if st.button("🆕 새 게임"):
        st.session_state.page = "create"
    if st.button("📂 불러오기"):
        load_game()
        st.success("불러오기 완료!")
        st.session_state.page = "map"

# 캐릭터 생성
elif st.session_state.page == "create":
    st.header("👤 캐릭터 생성")
    name = st.text_input("이름:")
    cls = st.selectbox("직업:", ["전사", "마법사", "암살자"])
    if st.button("시작") and name:
        stats = get_class_stats(cls)
        st.session_state.player = {"이름": name, "직업": cls, "레벨": 1, **stats}
        st.session_state.page = "skills"

# 스킬트리
elif st.session_state.page == "skills":
    st.title("🌟 스킬트리 선택")
    st.markdown("스킬 포인트: " + str(st.session_state.skill_points))
    if st.checkbox("화염구 (MP 10 소모, +10 피해)", key="fireball") and st.session_state.skill_points > 0:
        if "화염구" not in st.session_state.skills:
            st.session_state.skills.append("화염구")
            st.session_state.skill_points -= 1
    if st.button("완료"):
        st.session_state.page = "map"
# 맵
elif st.session_state.page == "map":
    st.header("🗺️ 아르카디아 월드맵")
    region = st.radio("이동 지역", ["어둠의 숲", "마법사 탑", "고대 신전"], horizontal=True)
    if st.button("이동"):
        if region == "어둠의 숲":
            st.session_state.page = "battle1"
        elif region == "마법사 탑":
            st.session_state.page = "npc"
        elif region == "고대 신전":
            st.session_state.page = "boss"

# 전투 1
elif st.session_state.page == "battle1":
    battle("숲의 망령", 30, 10, "map")

# 보스 전투
elif st.session_state.page == "boss":
    battle("타락한 왕 네르자크", 100, 20, "ending", boss=True)

# NPC
elif st.session_state.page == "npc":
    st.subheader("🧙‍♂️ 마법사 탑")
    st.markdown("마법사: '보스를 물리치기 전에 스킬을 다듬고 회복을 준비하게.'")
    if st.button("HP/MP 회복"):
        st.session_state.player["HP"] = get_class_stats(st.session_state.player["직업"])["HP"]
        st.session_state.player["MP"] = get_class_stats(st.session_state.player["직업"])["MP"]
        st.success("회복 완료!")

# 엔딩
elif st.session_state.page == "ending":
    st.title("🏁 엔딩")
    if st.session_state.boss_defeated:
        st.success("🎉 진엔딩: 왕국에 평화가 찾아왔다!")
    else:
        st.error("😈 배드엔딩: 세계는 어둠에 잠겼다.")
    if st.button("🔁 다시 시작"):
        init_game()

# 게임 오버
elif st.session_state.page == "gameover":
    st.title("☠️ GAME OVER")
    if st.button("🔁 재시작"):
        init_game()
