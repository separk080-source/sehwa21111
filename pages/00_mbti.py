import streamlit as st
import streamlit.components.v1 as components

# -----------------------
#  설정
# -----------------------
st.set_page_config(
    page_title="🌈 MBTI 진로 추천소 ✨",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------
#  유틸: Lottie 임베드 HTML 생성 (안정적 폴백 포함)
# -----------------------
def lottie_html(lottie_url: str, height: int = 250):
    """
    Lottie 파일을 안전하게 임베드하는 HTML.
    네트워크 문제 또는 외부 로딩 실패 시에도 페이지가 깨지지 않도록 폴백 텍스트를 함께 넣음.
    """
    # lottiefiles 플레이어 사용 (unpkg)
    html = f"""
    <div style="display:flex;justify-content:center;align-items:center;">
      <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
      <lottie-player
        src="{lottie_url}"
        background="transparent"
        speed="1"
        style="width:100%; max-width:600px; height:{height}px;"
        loop
        autoplay>
      </lottie-player>
    </div>
    """
    return html

# -----------------------
#  데이터: MBTI별 테마 색 + 직업 및 설명
# -----------------------
mbti_colors = {
    "INTJ": "#8e44ad", "INTP": "#3498db", "ENTJ": "#c0392b", "ENTP": "#e67e22",
    "INFJ": "#9b59b6", "INFP": "#e84393", "ENFJ": "#f39c12", "ENFP": "#f78fb3",
    "ISTJ": "#2c3e50", "ISFJ": "#16a085", "ESTJ": "#d35400", "ESFJ": "#f1c40f",
    "ISTP": "#27ae60", "ISFP": "#1abc9c", "ESTP": "#2980b9", "ESFP": "#ff7675"
}

# 추천 직업 + 상세 설명 (원하시면 여기 더 추가/수정 가능)
mbti_jobs = {
    "INFP": ("감성 몽상가 🌷", {
        "작가 ✍️": "상상력과 감수성이 풍부한 INFP는 글로 깊은 공감과 메시지를 전달할 수 있어요. 문학, 시나리오, 카피라이팅 등 적합합니다.",
        "예술가 🎨": "시각·음악·퍼포먼스 등 예술 활동으로 내면을 표현하며 관객에게 울림을 줍니다.",
        "사회복지사 💕": "타인의 이야기와 감정에 공감하며 실질적 도움을 주는 자리에서 큰 보람을 느낍니다.",
        "콘텐츠 크리에이터 🎥": "자유로운 표현과 스토리텔링으로 사람들의 공감을 이끌어내는 콘텐츠를 제작합니다."
    }),
    "ENTP": ("혁신가 ⚡", {
        "창업가 🚀": "아이디어를 빠르게 시도하고 개선하는 것을 즐깁니다. 초기 스타트업 환경에 강합니다.",
        "광고 기획자 📢": "창의적인 콘셉트와 기획으로 사람들의 관심을 끌어내는 역할에 탁월합니다.",
        "크리에이터 🎬": "즉흥적 감각과 위트로 대중을 사로잡는 콘텐츠 제작에 적합합니다.",
        "방송인 🎤": "말솜씨와 유머로 사람들과 활발히 소통하는 무대에 어울립니다."
    }),
    "ISFP": ("감각적인 예술가 🎨", {
        "사진작가 📸": "섬세한 관찰력과 미적 감각으로 순간을 포착합니다.",
        "플로리스트 💐": "색과 형태의 조화로 공간을 아름답게 만드는 일을 즐깁니다.",
        "셰프 🍳": "맛과 시각을 통해 감성을 전달하는 창의적 직업에 적합합니다.",
        "디자이너 🖌️": "사용자 경험이나 시각 디자인 등에서 감각을 발휘합니다."
    }),
    "INTJ": ("전략가 🧠", {
        "데이터 과학자 📊": "논리적 분석과 모델링으로 복잡한 문제를 해결합니다.",
        "연구원 🔬": "깊이 있는 조사와 체계적 탐구로 새로운 지식을 만듭니다.",
        "정책 분석가 🏛️": "시스템/사회 구조를 개선하는 전략을 수립하는 데 강합니다.",
        "시스템 엔지니어 💻": "복잡한 시스템을 설계하고 최적화하는 역할이 잘 맞습니다."
    }),
    "ESFP": ("인생파 즐기는 자 🎉", {
        "배우 🎭": "표현력과 감정 전달력이 뛰어나 무대·스크린에서 빛납니다.",
        "댄서 💃": "움직임으로 감정을 전달하며 관객과 즉각적인 피드백을 즐깁니다.",
        "이벤트 기획자 🎈": "사람들을 즐겁게 하고 기억에 남는 경험을 만드는 데 적합합니다.",
        "엔터테이너 🎤": "무대 퍼포먼스와 대중 소통에 재능이 있습니다."
    }),
    # 기본 샘플 외 원하는 MBTI를 추가로 넣어드릴게요.
}

# -----------------------
#  헤더 (화려하게)
# -----------------------
st.markdown(
    """
    <div style="text-align:center; padding:18px 0;">
      <h1 style="font-size:52px; margin:6px 0; color:#ff66b3;">
        🌈✨ MBTI 진로 추천소 ✨🌈
      </h1>
      <p style="color:#555; font-size:18px;">
        💫 이모지 팡팡! 화려하고 예쁜 UI로 <b>당신에게 딱 맞는 직업</b>을 찾아드려요 💼🎉
      </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------
#  상단 애니메이션 시도 (폴백 텍스트 포함)
# -----------------------
lottie_url_header = "https://assets8.lottiefiles.com/packages/lf20_jcikwtux.json"
try:
    components.html(lottie_html(lottie_url_header, height=220), height=240)
except Exception:
    # 네트워크 차단 등으로 실패 시 간단한 이모지 표현
    st.markdown("<h3 style='text-align:center;'>🎬✨ 애니메이션 로드 불가 — 대신 이모지로 꾸며드렸어요! ✨🎬</h3>", unsafe_allow_html=True)

# -----------------------
#  사용자 입력 (MBTI 선택)
# -----------------------
mbti_keys = list(mbti_jobs.keys())
selected_mbti = st.selectbox(
    label="당신의 MBTI를 골라주세요 💭 (클릭하면 아래에 추천 직업이 뜹니다!)",
    options=mbti_keys,
    index=0,
    help="예: INFP, ENT P 등"
)

# -----------------------
#  결과 표시 영역 (컬러 테마 + 카드 + 팝업)
# -----------------------
if selected_mbti:
    # 안전하게 색상 가져오기 (만약 color가 없으면 기본색)
    theme_color = mbti_colors.get(selected_mbti, "#ff66b3")
    title, jobs_dict = mbti_jobs.get(selected_mbti, ("알 수 없는 타입", {}))

    # 테마 배너
    banner_html = f"""
    <div style="margin:12px 0; padding:22px; border-radius:16px;
                background: linear-gradient(90deg, {theme_color}22, #ffffff);
                border: 4px solid {theme_color};">
      <h2 style="color:{theme_color}; text-align:center; margin:2px 0; font-size:34px;">
        ✨ 당신은 <b>{selected_mbti}</b> — {title} ✨
      </h2>
      <p style="text-align:center; color:#444; font-size:16px; margin:6px 0;">
        아래 카드에서 마음에 드는 직업을 눌러 자세한 설명(팝업 느낌)을 확인해보세요! 💼💬
      </p>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)

    # 직업 카드 레이아웃: 컬럼으로 나눠서 예쁘게 보여주기
    job_items = list(jobs_dict.items())
    n = len(job_items)
    # 한 줄에 최대 3개 카드
    per_row = 3
    rows = (n + per_row - 1) // per_row

    idx = 0
    for r in range(rows):
        cols = st.columns(per_row)
        for c in range(per_row):
            if idx >= n:
                break
            job_name, job_desc = job_items[idx]
            idx += 1

            col = cols[c]
            with col:
                # 카드 스타일
                card_html = f"""
                <div style="background: linear-gradient(180deg, #fff 0%, {theme_color}11 100%);
                            border-radius:14px; padding:16px; box-shadow:0 6px 18px rgba(0,0,0,0.08);">
                  <h3 style="margin:6px 0; color:{theme_color}; font-size:20px;">{job_name}</h3>
                  <p style="color:#333; font-size:14px; margin:8px 0 12px 0;">
                    {job_desc if len(job_desc) < 120 else job_desc[:117] + '...'}
                  </p>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

                # "자세히 보기" expander -> 팝업처럼 동작
                with st.expander(f"🔍 {job_name} 자세히 보기"):
                    # 상세 설명 블록 (더 화려하게)
                    detail_html = f"""
                    <div style="padding:14px; border-radius:12px; background:{theme_color}10;">
                      <p style="font-size:15px; color:#222; line-height:1.6;">
                        {job_desc}
                      </p>
                      <hr style="border:none; border-top:1px solid {theme_color}22; margin:10px 0;">
                      <p style="text-align:right; color:{theme_color}; margin:0;">
                        💡 이 직업은 <b>{selected_mbti}</b> 유형의 특성을 잘 살릴 수 있어요!
                      </p>
                    </div>
                    """
                    st.markdown(detail_html, unsafe_allow_html=True)

    # 하단 애니메이션 + 효과
    lottie_url_footer = "https://assets1.lottiefiles.com/packages/lf20_bhw1ul4g.json"
    try:
        components.html(lottie_html(lottie_url_footer, height=220), height=240)
    except Exception:
        st.markdown("<p style='text-align:center;'>🎈 애니메이션 표시 불가 — 풍선 대신 축하 이모지 팡팡 🎉</p>", unsafe_allow_html=True)

    # 풍선 효과 (Streamlit 내장)
    st.balloons()

else:
    st.info("왼쪽 드롭다운에서 MBTI를 선택해 주세요 💫")

# -----------------------
#  사이드바 (꾸미기)
# -----------------------
with st.sidebar:
    st.markdown("<h2 style='color:#ff66b3;'>💖 MBTI Career Finder</h2>", unsafe_allow_html=True)
    st.markdown("✨ MBTI 유형에 맞춘 진로 추천 & 직업 설명 앱이에요.")
    st.markdown("---")
    st.markdown("📚 **제작자:** 시은")
    st.markdown("📧 **Contact:** seun_dev@example.com")
    st.markdown("🎯 팁: 직업명을 눌러 ‘자세히 보기’로 확장하면 팝업처럼 설명을 볼 수 있어요!")
    st.markdown("---")
    st.markdown("🔧 환경 설정")
    st.caption("streamlit이 설치되어 있어야 합니다. 설치: `pip install streamlit`")

# -----------------------
#  푸터
# -----------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#999;'>Made with 💖 by 시은 | MBTI Career Finder 🌟</p>", unsafe_allow_html=True)
