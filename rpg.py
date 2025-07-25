import streamlit as st
import random

# 게임 상태 초기화
def init_game():
    st.session_state.update({
        "page": "title",
        "player": {},
        "inventory": ["치유 물약"],
        "quest_items": [],
        "chapter": 1,
        "enemy": {},
        "boss_defeated": False
    })

# 기본 능력치
def get_class_stats(cls):
    stats = {
        "전사": {"HP": 120, "MP": 30, "공격력": 15, "방어력": 10},
        "마법사": {"HP": 80, "MP": 100, "공격력": 10, "방어력": 5},
        "도적": {"HP": 100, "MP": 40, "공격력": 13, "방어력": 8}
    }
    return stats[cls]

# 전투 처리
def battle(enemy_name, enemy_hp, enemy_attack, next_page):
    st.session_state.enemy.setdefault("name", enemy_name)
    st.session_state.enemy.setdefault("hp", enemy_hp)
    st.session_state.enemy.setdefault("attack", enemy_attack)

    st.subheader(f"⚔️ 전투 - {enemy_name}")
    st.write(f"👤 {st.session_state.player['이름']} (HP: {st.session_state.player['HP']})")
    st.write(f"👹 {enemy_name} (HP: {st.session_state.enemy['hp']})")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗡️ 공격"):
            dmg = st.session_state.player["공격력"] + random.randint(-2, 3)
            st.session_state.enemy["hp"] -= dmg
            st.success(f"{enemy_name}에게 {dmg}의 피해를 입혔습니다!")
    with col2:
        if st.button("🧪 치유 물약 사용"):
            if "치유 물약" in st.session_state.inventory:
                st.session_state.player["HP"] += 20
                st.session_state.inventory.remove("치유 물약")
                st.success("HP 20 회복!")
            else:
                st.warning("치유 물약이 없습니다!")

    if st.session_state.enemy["hp"] > 0:
        dmg = max(1, enemy_attack - st.session_state.player["방어력"] + random.randint(-1, 2))
        st.session_state.player["HP"] -= dmg
        st.error(f"{enemy_name}의 공격! {dmg} 피해를 입었습니다.")

    if st.session_state.player["HP"] <= 0:
        st.session_state.page = "gameover"
    elif st.session_state.enemy["hp"] <= 0:
        st.success(f"{enemy_name}를 물리쳤습니다!")
        st.session_state.enemy = {}
        if enemy_name == "네르자크":
            st.session_state.boss_defeated = True
            st.session_state.page = "ending"
        else:
            st.session_state.page = next_page

# 엔딩 분기 처리
def show_ending():
    st.title("🏁 운명의 결말")
    if st.session_state.boss_defeated:
        st.markdown("당신은 '네르자크'를 쓰러뜨리고 아르카디아에 빛을 되찾았습니다.")
        st.balloons()
        st.success("🎉 진엔딩 달성!")
    else:
        st.markdown("세 개의 보석을 모두 모으지 못한 당신은 신전을 들어가지 못한 채 모래 속에 잠식됩니다.")
        st.error("💀 배드엔딩: 어둠의 소용돌이")
    if st.button("🔁 다시 시작"):
        init_game()

# 초기 설정
if "page" not in st.session_state:
    init_game()

# 페이지 설정
st.set_page_config(page_title="아르카디아 연대기", layout="centered")

# 타이틀 화면
if st.session_state.page == "title":
    st.title("🌟 아르카디아 연대기: 잊힌 빛의 전설")
    st.markdown("고대의 왕국이 타락의 그림자에 휩싸였다...\n당신이 전설의 시작이 될 수 있을까?")
    if st.button("▶️ 게임 시작"):
        st.session_state.page = "create"

# 캐릭터 생성
elif st.session_state.page == "create":
    st.subheader("🧝 캐릭터 생성")
    name = st.text_input("이름:")
    cls = st.selectbox("직업:", ["전사", "마법사", "도적"])
    if st.button("모험 시작") and name:
        stats = get_class_stats(cls)
        st.session_state.player = {"이름": name, "직업": cls, "레벨": 1, **stats}
        st.session_state.page = "chapter1"

# 챕터 1
elif st.session_state.page == "chapter1":
    st.title("🌲 [챕터 1] 어둠의 숲")
    st.write("당신은 짙은 안개가 낀 숲에서 깨어납니다. 어딘가 낯설고 불길합니다.")
    if st.button("길을 따라가 본다"):
        st.session_state.page = "battle1"

elif st.session_state.page == "battle1":
    battle("그림자 늑대", 30, 10, "chapter2")

# 챕터 2
elif st.session_state.page == "chapter2":
    st.title("🏘️ [챕터 2] 봉인된 마을")
    st.write("당신은 리엔 마을에 도착했고, 고대 마법사가 말합니다:")
    st.info("“봉인을 풀려면 세 개의 원소 보석이 필요하네. 먼저 불의 사원으로 가게.”")
    if st.button("불의 사원으로 향한다"):
        st.session_state.page = "battle2"

elif st.session_state.page == "battle2":
    battle("불의 정령", 40, 12, "chapter3")
    if st.session_state.page == "chapter3":
        st.session_state.quest_items.append("불의 보석")

# 챕터 3
elif st.session_state.page == "chapter3":
    st.title("❄️ [챕터 3] 얼음 협곡")
    st.write("당신은 북쪽의 얼음 협곡에서 냉기의 정령을 마주칩니다.")
    if st.button("정령과 전투"):
        st.session_state.page = "battle3"

elif st.session_state.page == "battle3":
    battle("냉기의 정령", 50, 15, "chapter4")
    if st.session_state.page == "chapter4":
        st.session_state.quest_items.append("얼음의 보석")

# 챕터 4
elif st.session_state.page == "chapter4":
    st.title("🌪️ [챕터 4] 황혼 사막")
    st.write("사막의 중심에는 시간을 지키는 수호자가 기다립니다.")
    if st.button("수호자에게 도전"):
        st.session_state.page = "battle4"

elif st.session_state.page == "battle4":
    battle("사막의 수호자", 60, 17, "chapter5")
    if st.session_state.page == "chapter5":
        st.session_state.quest_items.append("바람의 보석")

# 챕터 5
elif st.session_state.page == "chapter5":
    st.title("🏛️ [챕터 5] 고대 신전")
    if all(item in st.session_state.quest_items for item in ["불의 보석", "얼음의 보석", "바람의 보석"]):
        st.success("세 개의 보석이 반응하며 신전의 봉인이 풀립니다!")
        if st.button("네르자크와 결전"):
            st.session_state.page = "boss"
    else:
        st.warning("보석이 부족합니다... 봉인은 풀리지 않습니다.")
        if st.button("끝내기"):
            st.session_state.page = "ending"

elif st.session_state.page == "boss":
    battle("네르자크", 100, 20, "ending")

# 엔딩
elif st.session_state.page == "ending":
    show_ending()

# 게임오버
elif st.session_state.page == "gameover":
    st.title("☠️ GAME OVER")
    st.markdown("당신의 여정은 여기서 끝났습니다...")
    if st.button("🔄 다시 도전"):
        init_game()
