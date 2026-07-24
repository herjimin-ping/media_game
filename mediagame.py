import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import urllib.parse

# ---------------------------------------------------------
# 1. 페이지 기본 설정 및 디자인 (사이버/게임 스타일)
# ---------------------------------------------------------
st.set_page_config(
    page_title="요즘 뭐하템? - 미디어 알고리즘 & 윤리 퀴즈",
    page_icon="👾",
    layout="wide"
)

# Custom CSS 스타일링
st.markdown("""
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #4F46E5;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.1rem;
        text-align: center;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .monster-card {
        background-color: #F3F4F6;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .fact-box {
        background-color: #EEF2FF;
        border-left: 5px solid #6366F1;
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. 세션 상태 초기화 (비밀번호 및 응답 저장용)
# ---------------------------------------------------------
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'responses' not in st.session_state:
    # 예시용 초기 데이터 (실제 연동 시 구글 시트 데이터로 대체)
    st.session_state['responses'] = pd.DataFrame([
        {"시간": "2026-03-12 10:00", "이름": "김미디어", "학교급": "중등", "점수": 80, "유형": "밝은 빛나몬"},
        {"시간": "2026-03-12 10:05", "이름": "이알고", "학교급": "고등", "점수": 40, "유형": "어두운 다크알고몬"},
        {"시간": "2026-03-12 10:12", "이름": "박숏폼", "학교급": "초등", "점수": 60, "유형": "혼란의 멍하니몬"}
    ])

# ---------------------------------------------------------
# 3. 비밀 접속 코드 화면
# ---------------------------------------------------------
if not st.session_state['authenticated']:
    st.markdown("<h1 class='main-title'>🔐 요즘 뭐하템? - 비밀 접속</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>수업 시간에 안내받은 비밀 코드를 입력하세요!</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password_input = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
        if st.button("입장하기 🚀", use_container_width=True):
            if password_input == "media2026":  # 설정할 비밀번호
                st.session_state['authenticated'] = True
                st.success("접속 성공! 게임을 시작합니다.")
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다. 강사님께 문의하세요!")
    st.stop()

# ---------------------------------------------------------
# 4. 메인 앱 화면 (게임을 통한 몬스터 육성 + 퀴즈)
# ---------------------------------------------------------
st.markdown("<h1 class='main-title'>🎮 요즘 뭐하템? : 미디어 몬스터 키우기</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>나의 유튜브·숏츠 이용 습관과 미디어 윤리 지식으로 몬스터를 진화시켜 보세요!</p>", unsafe_allow_html=True)

# 탭 구성
tab1, tab2, tab3 = st.tabs(["👾 몬스터 육성 퀴즈", "🔍 팩트체크 & 어휘 탐정단", "📊 우리 반 데이터 분석"])

# ---------------------------------------------------------
# TAB 1: 몬스터 육성 퀴즈 (게임형)
# ---------------------------------------------------------
with tab1:
    st.subheader("📝 학생 정보 및 윤리 지침 퀴즈")
    
    with st.form("quiz_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            user_name = st.text_input("이름 또는 닉네임", placeholder="예: 미디어탐정")
        with col_b:
            school_level = st.selectbox("학교급 선택", ["초등", "중등", "고등"])
            
        st.markdown("---")
        st.markdown("### ❓ 미디어 윤리 & 알고리즘 탈출 퀴즈")
        
        q1 = st.radio(
            "Q1. 유튜브/숏츠를 보다가 너무 자극적이거나 신기한 정보가 나왔을 때 올바른 행동은?",
            [
                "1) 신기하니까 바로 친구들에게 공유하고 SNS에 올린다.",
                "2) 출처가 어디인지 확인하고, 진짜 사실인지 다른 뉴스나 팩트체크 사이트에서 검색해본다.",
                "3) 댓글의 반응만 보고 다들 진짜라고 하면 사실로 믿는다."
            ]
        )
        
        q2 = st.radio(
            "Q2. 숏츠 영상을 제작할 때 친구의 얼굴이 크게 나왔습니다. 올바른 영상 윤리는?",
            [
                "1) 재미있는 장면이니 친구 허락 없이 바로 업로드한다.",
                "2) 친구에게 동의를 구하거나, 얼굴을 스티커/모자이크로 가린 후 업로드한다.",
                "3) 칭찬하는 영상이니까 허락 없이 올려도 상관없다."
            ]
        )
        
        q3 = st.radio(
            "Q3. AI가 만든 딥페이크 영상이나 가짜 뉴스를 접했을 때 나의 태도는?",
            [
                "1) 정교하게 만들어졌다면 AI 기술이 대단하니 무조건 믿는다.",
                "2) 어색한 부분(손가락, 음성 억양 등)이 없는지 살피고 팩트체크 도구를 활용한다.",
                "3) 자극적일수록 조회수가 잘 나오므로 내 계정에 퍼나른다."
            ]
        )
        
        q4 = st.radio(
            "Q4. '알고리즘'이 나에게 계속 비슷한 숏폼 영상만 추천해 줄 때 드는 생각은?",
            [
                "1) 내 취향을 잘 알아주니 계속 추천 영상만 따라 본다.",
                "2) 내가 편향된 정보(필터 버블)에 갇힐 수 있음을 인지하고 다양한 분야의 영상도 찾아본다.",
                "3) 알고리즘이 주는 정보는 언제나 객관적이고 정확하다."
            ]
        )
        
        submit_btn = st.form_submit_button("몬스터 진화시키기 🧪", use_container_width=True)

    if submit_btn:
        if not user_name:
            st.warning("이름 또는 닉네임을 입력해주세요!")
        else:
            # 점수 계산
            score = 0
            if "2)" in q1: score += 25
            if "2)" in q2: score += 25
            if "2)" in q3: score += 25
            if "2)" in q4: score += 25
            
            # 몬스터 유형 판정
            if score >= 75:
                monster_type = "밝은 빛나몬"
                monster_img = "✨ 🌟 💖"
                monster_desc = "지혜롭고 건강한 미디어 습관을 가진 밝고 귀여운 몬스터!"
                bg_color = "#D1FAE5"
            elif score >= 50:
                monster_type = "혼란의 멍하니몬"
                monster_img = "🌀 📱 😳"
                monster_desc = "알고리즘의 유혹과 팩트체크 사이에서 고민 중인 몬스터!"
                bg_color = "#FEF3C7"
            else:
                monster_type = "어두운 다크알고몬"
                monster_img = "👾 ⬛ 🦇"
                monster_desc = "자극적인 숏폼과 가짜뉴스 피드에 갇혀 우울해하는 몬스터..."
                bg_color = "#FEE2E2"

            # 결과 데이터 누적
            new_data = {
                "시간": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "이름": user_name,
                "학교급": school_level,
                "점수": score,
                "유형": monster_type
            }
            st.session_state['responses'] = pd.concat([st.session_state['responses'], pd.DataFrame([new_data])], ignore_index=True)
            
            # 결과 출력
            st.markdown("---")
            st.balloons()
            st.markdown(f"### 🎉 {user_name}님의 미디어 몬스터 진화 완료!")
            
            col_m1, col_m2 = st.columns([1, 2])
            with col_m1:
                st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 30px; border-radius: 15px; text-align: center;">
                    <h1 style="font-size: 4rem; margin: 0;">{monster_img}</h1>
                    <h2 style="margin-top: 10px;">{monster_type}</h2>
                    <p style="font-weight: bold;">최종 점수: {score}점</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_m2:
                st.info(f"**몬스터 특징**: {monster_desc}")
                st.markdown("""
                **💡 오늘 얻는 미디어 통찰 (Insight):**
                * **알고리즘**은 내 기분을 좋게 만드는 영상을 계속 보여주지만, 때로는 **외눈박이 시야**를 만들어요.
                * 진짜 미디어 탐정은 숏츠 하나를 보더라도 **출처**와 **어휘의 정확한 뜻**을 짚고 넘어갑니다!
                """)

# ---------------------------------------------------------
# TAB 2: 팩트체크 & 국립국어원 표준사전 탐정단
# ---------------------------------------------------------
with tab2:
    st.subheader("🔍 유튜브·숏츠 의심 정보 교차검증 & 단어 뜻 사전")
    st.write("영상을 보다가 헷갈리는 단어가 있거나, 정보의 진위가 궁금할 때 바로 검색해보세요!")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.markdown("### 📖 1. 한국어표준대국어사전 (어휘 탐정)")
        st.caption("어휘 뜻을 모르면 맥락을 오해하기 쉽습니다! 정확한 단어 뜻을 찾아보세요.")
        search_word = st.text_input("뜻이 궁금한 단어를 입력하세요", placeholder="예: 편향, 알고리즘, 딥페이크")
        
        if search_word:
            encoded_word = urllib.parse.quote(search_word)
            dict_url = f"https://stdict.korean.go.kr/search/searchResult.do?searchKeyword={encoded_word}"
            st.markdown(f"👉 **[{search_word}]** 국립국어원 표준국어대사전에서 검색 결과 보기")
            st.link_button(f"📖 '{search_word}' 사전 뜻 확인하기", dict_url, use_container_width=True)
            
    with col_f2:
        st.markdown("### 🌐 2. 팩트체크 & 언론 교차검증")
        st.caption("소문이나 자극적인 뉴스의 사실 여부를 확인합니다.")
        fact_keyword = st.text_input("검증할 키워드를 입력하세요", placeholder="예: 백신 부작용, 독도, AI 생성물")
        
        if fact_keyword:
            encoded_fact = urllib.parse.quote(fact_keyword)
            
            # 교차검증 링크 모음
            google_fact_url = f"https://toolbox.google.com/factcheck/explorer/search/{encoded_fact}"
            naver_news_url = f"https://search.naver.com/search.naver?where=news&query={encoded_fact}"
            bigkinds_url = f"https://www.bigkinds.or.kr/v2/news/index.do"
            
            st.markdown("🔗 **교차검증 바로가기 버튼:**")
            st.link_button("🔎 Google Fact Check에서 확인", google_fact_url, use_container_width=True)
            st.link_button("📰 네이버 뉴스 검색결과 보기", naver_news_url, use_container_width=True)
            st.link_button("📊 빅카인즈(Big Kinds) 뉴스 분석 이동", bigkinds_url, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: 우리 반 데이터 분석 (실시간 시각화)
# ---------------------------------------------------------
with tab3:
    st.subheader("📊 우리 학생들의 미디어 몬스터 통계")
    st.write("오늘 참여한 학생들의 축적된 데이터가 실시간 시각화됩니다.")
    
    df = st.session_state['responses']
    
    if not df.empty:
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            # 몬스터 유형 분포 (파이 차트)
            fig_pie = px.pie(
                df, 
                names='유형', 
                title='👾 우리 반 몬스터 유형 분포',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_s2:
            # 학교급별 평균 점수 (막대 차트)
            avg_score = df.groupby('학교급')['점수'].mean().reset_index()
            fig_bar = px.bar(
                avg_score, 
                x='학교급', 
                y='점수', 
                title='🏫 학교급별 평균 윤리/리터러시 점수',
                color='학교급',
                text_auto=True
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        st.markdown("### 📋 최근 응답 기록")
        st.dataframe(df.sort_values(by="시간", ascending=False), use_container_width=True)
