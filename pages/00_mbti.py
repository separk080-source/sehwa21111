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
    html = f"""
    <div style="display:flex;justify-content:center;align-items:center;">
      <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
      <lottie-player
        src="{lottie_url}"
        background="transparent"
        speed="1"
        style="width:100%; max-width:700px; height:{height}px;"
        loop
        autoplay>
      </lottie-player>
    </div>
    """
    return html

# -----------------------
#  데이터: MBTI별 테마 색 + 직업 및 설명 (16가지 전부)
# -----------------------
mbti_colors = {
    "INTJ": "#8e44ad", "INTP": "#3498db", "ENTJ": "#c0392b", "ENTP": "#e67e22",
    "INFJ": "#9b59b6", "INFP": "#e84393", "ENFJ": "#f39c12", "ENFP": "#f78fb3",
    "ISTJ": "#2c3e50", "ISFJ": "#16a085", "ESTJ": "#d35400", "ESFJ": "#f1c40f",
    "ISTP": "#27ae60", "ISFP": "#1abc9c", "ESTP": "#2980b9", "ESFP": "#ff7675"
}

mbti_jobs = {
    "INTJ": ("전략가 🧠", {
        "데이터 과학자 📊": "복잡한 정보를 분석하고 패턴을 찾아 최적의 해결책을 만듭니다. 논리·계획 수립에 강합니다.",
        "연구원 🔬": "깊이 있는 탐구와 체계적 실험으로 새로운 지식을 만들며 독립적으로 일하는 걸 즐깁니다.",
        "시스템 엔지니어 💻": "전체 구조를 설계하고 안정적인 시스템을 구축하는 데 탁월합니다.",
        "정책 분석가 🏛️": "사회·조직 문제를 구조적으로 분석해 합리적 개선책을 제안합니다."
    }),
    "INTP": ("아이디어 천재 💡", {
        "AI 개발자 🤖": "논리적 모델링과 문제분해 능력으로 알고리즘을 설계하고 구현합니다.",
        "학자/연구원 📚": "이론적 호기심이 많아 새로운 개념을 탐구하고 정교하게 다듬습니다.",
        "시스템 설계자 🧩": "추상적 구조를 설계하며 복잡한 문제를 단순화하는 능력이 탁월합니다.",
        "UI/UX 리서처 🔎": "사용자 행동을 분석해 제품 개선에 기여합니다."
    }),
    "ENTJ": ("리더형 보스 🦁", {
        "경영자/CEO 👔": "비전을 제시하고 조직을 이끄는 리더십이 빛납니다.",
        "경영 컨설턴트 📈": "문제 해결과 전략 수립으로 조직의 성과를 개선합니다.",
        "프로덕트 매니저 🧭": "목표 지향적 사고로 제품의 방향을 결정하고 팀을 조율합니다.",
        "변호사 ⚖️": "논리적 설득과 전략으로 복잡한 사안을 해결합니다."
    }),
    "ENTP": ("혁신가 ⚡", {
        "창업가 🚀": "새로운 아이디어로 시장에 도전하고 빠르게 학습하며 성장합니다.",
        "광고 기획자 📢": "크리에이티브한 콘셉트로 사람들의 관심을 끌어냅니다.",
        "크리에이터 🎬": "즉흥적이고 유머러스한 콘텐츠로 대중의 공감을 이끌어냅니다.",
        "제품 혁신가 🧪": "실험과 개선을 반복해 새로운 시도를 하는 환경에서 가장 빛납니다."
    }),
    "INFJ": ("통찰형 조언자 🌌", {
        "상담가/심리치료사 🧡": "타인의 감정을 깊이 이해하고 돕는 데 천부적입니다.",
        "작가 ✍️": "내면의 메시지를 섬세하게 전달하는 스토리텔러로서 강점이 있습니다.",
        "교육자/교수 🎓": "깊은 통찰로 학생들의 성장에 영감을 줍니다.",
        "NGO/사회운동가 ✨": "가치 있는 목표를 위해 사람들을 조직하고 이끌어갑니다."
    }),
    "INFP": ("감성 몽상가 🌷", {
        "작가/시인 🖋️": "감수성과 상상력을 글로 표현해 사람들의 마음을 움직입니다.",
        "예술가 🎨": "시각·음악·퍼포먼스를 통해 감정을 전달하는 데 재능이 있습니다.",
        "사회복지사 💕": "타인을 돕고 사회적 의미를 실현하는 데 큰 보람을 느낍니다.",
        "콘텐츠 크리에이터 🎥": "개성 있는 스토리로 사람들과 공감대를 형성합니다."
    }),
    "ENFJ": ("따뜻한 리더 🌞", {
        "교사/강사 🍎": "사람들의 잠재력을 끌어내고 동기를 부여하는 능력이 탁월합니다.",
        "HR/조직관리자 🤝": "팀 케어와 조직문화를 형성하는 역할에서 강점을 발휘합니다.",
        "마케터/브랜드 매니저 📣": "사람의 마음을 읽고 소통전략을 기획합니다.",
        "사회적 기업가 🌍": "사람과 가치를 잇는 프로젝트를 이끌어갑니다."
    }),
    "ENFP": ("열정 폭발 엔터테이너 🎉", {
        "프로듀서/기획자 🎭": "창의적인 아이디어로 다양한 프로젝트를 기획합니다.",
        "홍보/PR 전문가 📣": "사교성과 에너지로 사람들과 관계를 맺는 데 능숙합니다.",
        "여행가이드/체험 디자이너 🌏": "새로운 경험을 기획하고 사람들에게 즐거움을 제공합니다.",
        "광고 크리에이터 🧨": "발랄한 상상력으로 주목받는 캠페인을 만듭니다."
    }),
    "ISTJ": ("철저한 관리자 🧾", {
        "회계사/감사원 🧮": "세부사항을 정확히 다루며 규칙과 절차를 잘 지킵니다.",
        "공무원/행정가 🏢": "책임감과 신뢰도로 안정적인 운영을 이끌어갑니다.",
        "품질관리자 🛠️": "시스템의 신뢰성 확보에 필요한 역할을 수행합니다.",
        "프로젝트 매니저 📅": "계획과 실행을 꼼꼼히 관리하는 데 강점이 있습니다."
    }),
    "ISFJ": ("헌신적인 조력자 🌼", {
        "간호사/의료지원 🩺": "타인을 돌보는 데 헌신적이며 세심한 배려가 장점입니다.",
        "교사/보육교사 🧸": "학생의 성장과 안정된 환경을 만드는 데 능합니다.",
        "사회복지사 🤲": "실질적 도움과 지속적 지원을 통해 사람들을 돕습니다.",
        "행정/사무관리 🗂️": "조직의 운영을 차근차근 돕는 역할에 적합합니다."
    }),
    "ESTJ": ("현실주의 리더 🧩", {
        "관리자/운영책임자 🏷️": "조직을 체계적으로 운영하고 성과를 창출합니다.",
        "판사/검사 ⚖️": "규칙과 공정성에 기반한 판단을 내리는 데 적합합니다.",
        "군/경찰 등 공공안전 🛡️": "규율과 책임을 중시하는 환경에서 강합니다.",
        "프로젝트 매니저 🚦": "일정·자원·리스크를 조율해 프로젝트를 완수합니다."
    }),
    "ESFJ": ("친절한 사회인 🎀", {
        "이벤트 플래너 🎉": "사람들이 즐거워하는 경험을 만드는 데 재능이 있습니다.",
        "간호사/헬스케어 🫶": "타인을 보살피며 신뢰를 얻는 역할에 잘 맞습니다.",
        "HR/채용담당자 🧾": "사람을 연결하고 조직을 운영하는 데 능숙합니다.",
        "고객 서비스/매장 관리자 🛍️": "서비스 마인드로 고객 만족을 이끌어냅니다."
    }),
    "ISTP": ("문제 해결사 🛠️", {
        "엔지니어/기술자 ⚙️": "실무적 문제를 빠르게 해결하는 데 강합니다.",
        "파일럿/운송직 ✈️": "냉정한 판단과 기술적 숙련을 요구하는 직무에 적합합니다.",
        "데이터 엔지니어 🧱": "시스템과 도구를 만들어 효율을 높이는 일을 선호합니다.",
        "응급 구조대/기술직 🚑": "즉각적 판단과 손기술이 중요한 환경에서 빛납니다."
    }),
    "ISFP": ("감각적인 예술가 🎨", {
        "디자이너/일러스트레이터 🖌️": "시각적 감각으로 아름다움을 만들어냅니다.",
        "사진작가 📸": "순간을 포착해 감정을 전달하는 데 재능이 있습니다.",
        "셰프/베이커 🍰": "감각적 표현을 음식으로 구현하며 창의력을 발휘합니다.",
        "플로리스트/무대미술 🌺": "색채와 구성으로 감성을 자극하는 일을 즐깁니다."
    }),
    "ESTP": ("모험가 🏎️", {
        "세일즈/비즈니스 개발 📞": "순발력과 설득력으로 기회를 포착합니다.",
        "이벤트/스포츠 매니저 🏟️": "현장 중심의 활동적 역할에서 에너지를 발산합니다.",
        "응급의료/현장직 🚨": "위기 상황에서 빠르게 행동하는 데 능숙합니다.",
        "리테일/프랜차이즈 운영 🛒": "즉흥적 판단과 실행력으로 성과를 만듭니다."
    }),
    "ESFP": ("인생파 즐기는 자 🎉", {
        "배우/퍼포머 🎭": "표현력과 카리스마로 무대·스크린에서 빛납니다.",
        "댄서/퍼포먼스 아티스트 💃": "움직임으로 감정을 전달하며 관객과 소통합니다.",
        "이벤트 코디네이터 🎈": "사람들이 즐길 순간을 기획하고 실행합니다.",
        "호스피탈리티/서비스업 🍸": "사람들과의 상호작용에서 큰 만족을 얻습니다."
    })
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
    theme_color = mbti_colors.get(selected_mbti, "#ff66b3")
    title, jobs_dict = mbti_jobs.get(selected_mbti, ("알 수 없는 타입", {}))

    # 배너
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

    # 직업 카드: 한 줄에 최대 3개
    job_items = list(jobs_dict.items())
    n = len(job_items)
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

                with st.expander(f"🔍 {job_name} 자세히 보기"):
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

    # 하단 애니메이션 + 풍선
    lottie_url_footer = "https://assets1.lottiefiles.com/packages/lf20_bhw1ul4g.json"
    try:
        components.html(lottie_html(lottie_url_footer, height=220), height=240)
    except Exception:
        st.markdown("<p style='text-align:center;'>🎈 애니메이션 표시 불가 — 풍선 대신 축하 이모지 팡팡 🎉</p>", unsafe_allow_html=True)

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
