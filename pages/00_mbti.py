import streamlit as st

# 🌟 페이지 기본 설정
st.set_page_config(
    page_title="MBTI 진로 추천✨",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 🌈 예쁜 헤더
st.markdown("""
    <h1 style='text-align: center; color: #ff66b3; font-size: 60px;'>🧭 MBTI 진로 추천소 💫</h1>
    <p style='text-align: center; color: #666; font-size: 18px;'>당신의 MBTI에 어울리는 찰떡 직업을 찾아보세요 💼💖</p>
""", unsafe_allow_html=True)

# 🎨 MBTI별 직업 추천 데이터
mbti_jobs = {
    "INTJ": ("전략가 🧠", "데이터 과학자, 연구원, 시스템 엔지니어, 정책 분석가"),
    "INTP": ("아이디어 천재 💡", "프로그래머, 발명가, UX 디자이너, 철학자"),
    "ENTJ": ("리더형 보스 🦁", "경영 컨설턴트, CEO, 변호사, 기획자"),
    "ENTP": ("혁신가 ⚡", "창업가, 크리에이터, 광고 기획자, 방송인"),
    "INFJ": ("통찰형 조언자 🌌", "상담가, 작가, 심리학자, 교육자"),
    "INFP": ("감성 몽상가 🌷", "작가, 예술가, 사회복지사, 콘텐츠 크리에이터"),
    "ENFJ": ("따뜻한 리더 🌞", "교사, 강사, 마케터, 인사 담당자"),
    "ENFP": ("열정 폭발 엔터테이너 🎆", "방송인, 디자이너, 홍보 전문가, 여행 가이드"),
    "ISTJ": ("철저한 관리자 🧾", "회계사, 행정공무원, 군인, 품질관리자"),
    "ISFJ": ("헌신적인 조력자 🌼", "간호사, 교사, 사회복지사, 상담사"),
    "ESTJ": ("현실주의 리더 🧩", "경영자, 관리자, 프로젝트 매니저, 판사"),
    "ESFJ": ("친절한 사회인 🎀", "간호사, 이벤트 플래너, 인사 담당자, 교사"),
    "ISTP": ("문제 해결사 🛠️", "기계공, 프로그래머, 파일럿, 엔지니어"),
    "ISFP": ("감각적인 예술가 🎨", "사진작가, 디자이너, 플로리스트, 셰프"),
    "ESTP": ("모험가 🏎️", "세일즈맨, 스포츠 코치, 기획자, 경찰"),
    "ESFP": ("인생파 즐기는 자 🎉", "배우, 댄서, 엔터테이너, 이벤트 기획자"),
}

# 🎯 MBTI 선택
selected_mbti = st.selectbox(
    "당신의 MBTI를 선택해주세요 💭",
    list(mbti_jobs.keys()),
    index=None,
    placeholder="예: INFP 🌸"
)

# 🎁 결과 출력
if selected_mbti:
    title, jobs = mbti_jobs[selected_mbti]
    st.markdown(f"""
        <div style='text-align:center; background-color:#ffe6f7; padding:40px; border-radius:20px; margin-top:20px;'>
            <h2 style='color:#ff3399;'>당신은 <b>{selected_mbti}</b> ({title}) 타입이에요! 💖</h2>
            <p style='font-size:20px; color:#333;'>🌟 추천 직업: <b>{jobs}</b></p>
            <p style='font-size:18px; color:#555;'>당신의 강점을 살릴 수 있는 진로를 탐색해보세요 🌈</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 🎉 애니메이션 효과 (balloons)
    st.balloons()
else:
    st.markdown("<p style='text-align:center; color:#888;'>👆 MBTI를 선택하면 결과가 나타납니다 💫</p>", unsafe_allow_html=True)

# 📘 하단 푸터
st.markdown("""
<hr>
<p style='text-align:center; color:#aaa;'>
Made with 💖 by <b>시은</b> | MBTI Career Finder 🌟
</p>
""", unsafe_allow_html=True)
