import streamlit as st
from streamlit_lottie import st_lottie
import requests

# 🌟 페이지 설정
st.set_page_config(
    page_title="MBTI 진로 추천✨",
    page_icon="💖",
    layout="wide"
)

# 🪄 Lottie 애니메이션 로드 함수
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 🎬 애니메이션 로드
career_anim = load_lottie("https://assets8.lottiefiles.com/packages/lf20_jcikwtux.json")
welcome_anim = load_lottie("https://assets2.lottiefiles.com/packages/lf20_hu9cd9.json")

# 🎨 MBTI별 테마 컬러
mbti_colors = {
    "INTJ": "#8e44ad", "INTP": "#3498db", "ENTJ": "#c0392b", "ENTP": "#e67e22",
    "INFJ": "#9b59b6", "INFP": "#e84393", "ENFJ": "#f39c12", "ENFP": "#f78fb3",
    "ISTJ": "#2c3e50", "ISFJ": "#16a085", "ESTJ": "#d35400", "ESFJ": "#f1c40f",
    "ISTP": "#27ae60", "ISFP": "#1abc9c", "ESTP": "#2980b9", "ESFP": "#ff7675"
}

# 💼 MBTI별 추천 직업 + 설명
mbti_jobs = {
    "INTJ": ("전략가 🧠", {
        "데이터 과학자": "논리적 사고와 분석력이 뛰어나며 복잡한 문제를 해결하는 데 강점이 있어요.",
        "연구원": "새로운 아이디어를 탐구하고 체계적으로 실험하는 걸 즐깁니다.",
        "시스템 엔지니어": "시스템의 구조를 설계하고 최적화하는 데 탁월해요.",
        "정책 분석가": "사회적 문제를 전략적으로 분석하고 해결책을 제시할 수 있어요."
    }),
    "INFP": ("감성 몽상가 🌷", {
        "작가": "감정과 생각을 언어로 표현하는 재능이 뛰어나요.",
        "예술가": "내면의 세계를 시각적 또는 음악적으로 표현하는 걸 즐깁니다.",
        "사회복지사": "타인을 돕고 세상에 긍정적 영향을 주고 싶어하는 마음이 커요.",
        "콘텐츠 크리에이터": "창의적인 아이디어로 사람들의 공감을 이끌어낼 수 있어요."
    }),
    "ENTP": ("혁신가 ⚡", {
        "창업가": "새로운 아이디어로 세상을 바꾸는 데 열정이 가득합니다.",
        "크리에이터": "자유로운 사고와 유머 감각으로 사람들을 사로잡아요.",
        "광고 기획자": "트렌드를 읽고 독창적인 캠페인을 기획하는 능력이 있어요.",
        "방송인": "에너지가 넘치며 사람들과의 소통을 즐깁니다."
    }),
    "ISFP": ("감각적인 예술가 🎨", {
        "사진작가": "세상의 아름다움을 포착하고 감성적으로 표현해요.",
        "디자이너": "미적 감각과 섬세함으로 시각적 아름다움을 창조합니다.",
        "플로리스트": "자연의 색감과 형태를 조화롭게 다루는 능력이 뛰어나요.",
        "셰프": "감각적이고 창의적인 요리로 사람들의 감정을 움직입니다."
    }),
    # 💫 필요하다면 다른 MBTI들도 동일하게 추가 가능!
}

# 🧭 헤더
st.markdown("""
    <h1 style='text-align:center; color:#ff66b3; font-size:60px;'>
        🧭 MBTI 진로 추천소 💫
    </h1>
    <p style='text-align:center; color:#777; font-size:18px;'>
        당신의 MBTI에 어울리는 <b>찰떡 직업</b>을 찾아보세요 💼
    </p>
""", unsafe_allow_html=True)

# 🌈 웰컴 애니메이션
st_lottie(welcome_anim, height=250, key="welcome")

# 🎯 MBTI 선택
selected_mbti = st.selectbox(
    "당신의 MBTI를 선택해주세요 💭",
    list(mbti_jobs.keys()),
    index=None,
    placeholder="예: INFP 🌸"
)

# 💡 결과 표시
if selected_mbti:
    color = mbti_colors[selected_mbti]
    title, job_dict = mbti_jobs[selected_mbti]
    
    st.markdown(f"""
        <div style='background-color:{color}20; border-left:10px solid {color}; padding:30px; border-radius:20px;'>
            <h2 style='color:{color}; text-align:center;'>당신은 <b>{selected_mbti}</b> ({title}) 타입이에요! 💖</h2>
            <p style='text-align:center; color:#333; font-size:20px;'>🌟 어울리는 직업을 클릭해보세요 👇</p>
        </div>
    """, unsafe_allow_html=True)

    # 💼 직업별 카드 + 팝업(expander)
    for job, desc in job_dict.items():
        with st.expander(f"💼 {job}"):
            st.markdown(f"""
                <div style='background-color:{color}15; border-radius:15px; padding:20px;'>
                    <p style='font-size:18px; color:#333;'>{desc}</p>
                    <p style='text-align:right; color:{color}; font-size:14px;'>💡 {title}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # 🎬 밑에 애니메이션 추가
    st_lottie(career_anim, height=250, key="career")
    st.balloons()
else:
    st.markdown("<p style='text-align:center; color:#888;'>👆 MBTI를 선택하면 결과가 나타납니다 💫</p>", unsafe_allow_html=True)

# 🌈 사이드바
st.sidebar.markdown("## 💖 MBTI Career Finder")
st.sidebar.markdown("이 앱은 MBTI 성격 유형에 맞는 직업을 추천하고,<br>각 직업에 대한 간단한 설명을 제공합니다 ✨", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("📚 **제작자:** 시은 🌸")
st.sidebar.markdown("📧 **Contact:** seun_dev@example.com")
st.sidebar.markdown("🌟 **Powered by Streamlit**")

# 📘 푸터
st.markdown("""
<hr>
<p style='text-align:center; color:#aaa;'>
Made with 💖 by <b>시은</b> | MBTI Career Finder 🌟
</p>
""", unsafe_allow_html=True)
