import streamlit as st
from streamlit_lottie import st_lottie
import requests

# 🌟 페이지 기본 설정
st.set_page_config(
    page_title="MBTI 진로 추천✨",
    page_icon="🌈",
    layout="wide"
)

# 🎬 Lottie 애니메이션 로드 함수
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 🎨 애니메이션 로드
welcome_anim = load_lottie("https://assets8.lottiefiles.com/packages/lf20_jcikwtux.json")
career_anim = load_lottie("https://assets1.lottiefiles.com/packages/lf20_bhw1ul4g.json")

# 🌈 MBTI별 테마 컬러
mbti_colors = {
    "INTJ": "#8e44ad", "INTP": "#3498db", "ENTJ": "#c0392b", "ENTP": "#e67e22",
    "INFJ": "#9b59b6", "INFP": "#e84393", "ENFJ": "#f39c12", "ENFP": "#f78fb3",
    "ISTJ": "#2c3e50", "ISFJ": "#16a085", "ESTJ": "#d35400", "ESFJ": "#f1c40f",
    "ISTP": "#27ae60", "ISFP": "#1abc9c", "ESTP": "#2980b9", "ESFP": "#ff7675"
}

# 💼 MBTI별 직업 + 설명
mbti_jobs = {
    "INFP": ("감성 몽상가 🌷", {
        "작가 ✍️": "상상력과 감수성이 풍부한 INFP는 글로 마음을 표현하는 걸 좋아해요.",
        "예술가 🎨": "감정과 아름다움을 작품으로 표현하며 사람들의 감성을 자극합니다.",
        "사회복지사 💕": "다른 사람을 돕고 세상을 따뜻하게 만드는 데 큰 행복을 느껴요.",
        "콘텐츠 크리에이터 🎥": "자유로운 감성으로 사람들에게 영감을 주는 콘텐츠를 만들어내요."
    }),
    "ENTP": ("혁신가 ⚡", {
        "창업가 🚀": "새로운 아이디어로 세상을 바꾸는 데 열정이 가득한 ENTP!",
        "광고 기획자 📢": "창의적이고 논리적인 사고로 사람들의 관심을 사로잡아요.",
        "크리에이터 🎬": "유머감각과 자유로운 사고로 대중과 소통합니다.",
        "방송인 🎤": "카리스마 넘치는 표현력으로 사람들을 즐겁게 해요!"
    }),
    "ISFP": ("감각적인 예술가 🎨", {
        "사진작가 📸": "섬세한 감각으로 세상의 아름다움을 포착해요.",
        "플로리스트 💐": "자연의 색감과 향기를 조화롭게 다루는 감각이 뛰어나요.",
        "셰프 🍳": "감각적인 요리로 사람들의 마음을 사로잡습니다.",
        "디자이너 🖌️": "색과 형태로 감정을 표현하는 시각적 마법사예요!"
    }),
    "INTJ": ("전략가 🧠", {
        "데이터 과학자 📊": "논리적이고 전략적인 사고로 복잡한 문제를 해결합니다.",
        "연구원 🔬": "새로운 지식을 탐구하고 체계적으로 정리하는 걸 즐겨요.",
        "정책 분석가 🏛️": "세상을 효율적으로 만들기 위한 전략을 세우는 데 능해요.",
        "시스템 엔지니어 💻": "구조적 사고로 완벽한 시스템을 설계합니다."
    }),
    "ESFP": ("인생파 즐기는 자 🎉", {
        "배우 🎭": "자신의 감정과 매력을 무대에서 마음껏 표현해요!",
        "댄서 💃": "움직임으로 감정을 전달하는 천부적인 표현자예요.",
        "이벤트 기획자 🎈": "즐거움과 흥을 만들어내는 파티의 마법사!",
        "엔터테이너 🎤": "에너지와 매력으로 사람들을 웃게 만듭니다."
    })
}

# 🌸 헤더
st.markdown("""
    <h1 style='text-align:center; color:#ff66b3; font-size:60px;'>
        🌈 MBTI 진로 추천소 💫
    </h1>
    <p style='text-align:center; color:#777; font-size:20px;'>
        당신의 MBTI에 어울리는 <b>완벽한 직업</b>을 찾아보세요 💕
    </p>
""", unsafe_allow_html=True)

# 🌟 상단 애니메이션
st_lottie(welcome_anim, height=250, key="welcome")

# 🧭 MBTI 선택
selected_mbti = st.selectbox(
    "당신의 MBTI를 선택해주세요 💭",
    list(mbti_jobs.keys()),
    index=None,
    placeholder="예: INFP 🌷"
)

# 💡 결과 표시
if selected_mbti:
    color = mbti_colors[selected_mbti]
    title, job_dict = mbti_jobs[selected_mbti]
    
    st.markdown(f"""
        <div style='background-color:{color}20; border-left:10px solid {color}; padding:30px; border-radius:20px;'>
            <h2 style='color:{color}; text-align:center;'>당신은 <b>{selected_mbti}</b> ({title}) 타입이에요! 💖</h2>
            <p style='text-align:center; color:#333; font-size:20px;'>✨ 아래의 직업을 클릭해 설명을 확인해보세요 💼</p>
        </div>
    """, unsafe_allow_html=True)

    # 💬 직업별 팝업(expander)
    for job, desc in job_dict.items():
        with st.expander(f"{job} 자세히 보기 🌟"):
            st.markdown(f"""
                <div style='background-color:{color}15; border-radius:15px; padding:20px;'>
                    <p style='font-size:18px; color:#333;'>{desc}</p>
                    <p style='text-align:right; color:{color}; font-size:14px;'>💡 {title}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st_lottie(career_anim, height=250, key="career")
    st.balloons()
else:
    st.markdown("<p style='text-align:center; color:#999;'>👆 MBTI를 선택하면 결과가 나타납니다 💫</p>", unsafe_allow_html=True)

# 🌈 사이드바 꾸미기
st.sidebar.markdown("## 💖 MBTI Career Finder")
st.sidebar.markdown("MBTI에 따라 <b>당신에게 어울리는 직업</b>과<br>각 직업의 특징을 알려주는 진로 탐색 앱이에요 🌟", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("📚 **제작자:** 시은 🌸")
st.sidebar.markdown("📧 **Contact:** seun_dev@example.com")
st.sidebar.markdown("🌈 **Powered by Streamlit**")

# 📘 푸터
st.markdown("""
<hr>
<p style='text-align:center; color:#aaa;'>
Made with 💖 by <b>시은</b> | MBTI Career Finder 🌸
</p>
""", unsafe_allow_html=True)
