import streamlit as st
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 앱 설정
# -----------------------------
st.set_page_config(
    page_title="오늘의 소비, 내일의 나 💸✨",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 시각 스타일
sns.set_style("whitegrid")
plt.rcParams.update({"font.size": 11})

# -----------------------------
# 유틸 함수
# -----------------------------
def safe_parse_date(x):
    try:
        return pd.to_datetime(x)
    except Exception:
        return pd.NaT

# 간단 키워드 기반 카테고리 자동분류 함수
def categorize_description(desc: str):
    d = desc.lower()
    # 키워드 매핑 (필요하면 더 추가)
    mapping = {
        "coffee": "카페/음료 ☕",
        "starbucks": "카페/음료 ☕",
        "latte": "카페/음료 ☕",
        "bread": "식비 🍱",
        "market": "장보기 🛒",
        "grocery": "장보기 🛒",
        "cvs": "장보기 🛒",
        "uber": "교통/배달 🚗",
        "taxi": "교통/배달 🚗",
        "t map": "교통/배달 🚗",
        "gas": "자동차/유류 ⛽",
        "oil": "자동차/유류 ⛽",
        "netflix": "구독/엔터 🎬",
        "spotify": "구독/엔터 🎧",
        "gym": "건강/운동 🏋️",
        "hospital": "의료/건강 🩺",
        "book": "교육/도서 📚",
        "school": "교육/도서 📚",
        "flight": "여행 ✈️",
        "hotel": "여행 ✨",
        "delivery": "배달/식사 🍱",
        "food": "식비 🍱",
        "restaurant": "외식 🍽️",
        "clinic": "의료/건강 🩺",
    }
    for k, v in mapping.items():
        if k in d:
            return v
    # 숫자 포함 등으로 접근 불가 시 '기타'
    return "기타 🧾"

# CSV -> DataFrame 정리
def normalize_transactions(df: pd.DataFrame):
    df = df.copy()
    # 표준 컬럼: Date, Description, Amount, Category (선택)
    # 가능한 여러 이름을 허용
    col_map = {}
    lower_cols = [c.lower() for c in df.columns]
    for c in df.columns:
        lc = c.lower()
        if "date" in lc:
            col_map[c] = "Date"
        elif "time" in lc and "date" not in col_map.values():
            col_map[c] = "Date"
        elif "desc" in lc or "detail" in lc or "merchant" in lc or "store" in lc:
            col_map[c] = "Description"
        elif "amount" in lc or "price" in lc or "amt" in lc:
            col_map[c] = "Amount"
        elif "category" in lc:
            col_map[c] = "Category"
    df = df.rename(columns=col_map)
    # 필수 컬럼 체크
    if "Date" not in df.columns or "Amount" not in df.columns:
        raise ValueError("CSV 파일에 'Date' 와 'Amount' 컬럼이 필요합니다. (예: Date, Amount, Description, Category)")
    # parse date, clean amount
    df["Date"] = df["Date"].apply(safe_parse_date)
    # Amount 숫자 정리
    def clean_amount(x):
        try:
            if isinstance(x, str):
                x = x.replace(",", "").replace("₩", "").replace("KRW", "")
            return float(x)
        except Exception:
            return np.nan
    df["Amount"] = df["Amount"].apply(clean_amount)
    # Description
    if "Description" not in df.columns:
        df["Description"] = "알 수 없음"
    else:
        df["Description"] = df["Description"].fillna("알 수 없음").astype(str)
    # Category: fillna using heuristic
    if "Category" not in df.columns:
        df["Category"] = df["Description"].apply(categorize_description)
    else:
        df["Category"] = df["Category"].fillna("").apply(lambda x: x if x.strip() != "" else None)
        # 채워지지 않은 경우 자동 분류
        df["Category"] = df.apply(lambda r: r["Category"] if r["Category"] else categorize_description(r["Description"]), axis=1)
    # Drop rows with invalid amounts or dates
    df = df.dropna(subset=["Amount", "Date"])
    # Normalize Amount to absolute positive (지출으로 가정; 입금은 양수로 둠)
    # If Amount positive means expense; if data has negative expenses, convert to abs
    df["Amount"] = df["Amount"].abs()
    # Add Year-Month col
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
    return df.reset_index(drop=True)

# 예산 달성 예상: 간단 선형 예측으로 남은 기간 예산 소진 예측
def predict_budget_outcome(total_spent_month, budget):
    if budget <= 0:
        return {"status": "no_budget", "message": "예산이 설정되지 않았어요."}
    if total_spent_month <= budget:
        pct = total_spent_month / budget
        return {"status": "under", "pct": pct, "message": f"예산의 {pct*100:.1f}% 사용 중 — 좋아요! 🎉"}
    else:
        pct = total_spent_month / budget
        return {"status": "over", "pct": pct, "message": f"예산 초과! 현재 {pct*100:.1f}% 사용 중입니다. 🔥 절약 팁을 확인하세요."}

# 소액 절약 아이디어 생성 (간단 규칙 기반)
def generate_saving_tips(summary_by_cat, top_items, budget_analysis):
    tips = []
    # 1) 카페/음료 비중 높을 때
    cafe = None
    for cat in summary_by_cat.index:
        if "카페" in cat or "음료" in cat:
            cafe = summary_by_cat.get(cat, 0)
    total = summary_by_cat.sum()
    if cafe and cafe / total > 0.12:
        tips.append("☕ 카페비 12% 이상! 주 3회→주1회로 줄이면 한달에 큰 절약이 될 거예요. 직접 내려마시기 챌린지 추천!")
    # 2) 배달/외식
    deli = 0
    for cat in summary_by_cat.index:
        if "배달" in cat or "외식" in cat or "식비" in cat:
            deli += summary_by_cat.get(cat, 0)
    if deli / total > 0.25:
        tips.append("🍱 배달/외식 비중이 높아요. '배달 없는 월요일' 같은 주간 미션을 만들어보세요.")
    # 3) 구독
    sub = 0
    for cat in summary_by_cat.index:
        if "구독" in cat or "엔터" in cat:
            sub += summary_by_cat.get(cat, 0)
    if sub / total > 0.08:
        tips.append("🎬 구독 중복 의심! 사용하지 않는 구독을 확인하고 정리해보세요.")
    # 4) Top merchants
    if len(top_items) > 0:
        m, amt = top_items[0]
        tips.append(f"🏆 최다 지출: {m} — 다음 달엔 이 상점에서의 지출을 20% 줄여보는 건 어때요?")
    # 5) 예산 초과 시 빠른 팁
    if budget_analysis["status"] == "over":
        tips.append("⚠️ 예산 초과 상태입니다. 즉시 실행 가능한 미션: *커피 1잔 줄이기 / 배달 1회 줄이기 / 불필요 구독 취소*")
    # 기본 팁
    if len(tips) == 0:
        tips.append("✨ 축하! 큰 문제는 없어 보입니다. 작은 보너스 팁: 잔돈 자동저축 앱을 활용해보세요.")
    return tips

# DataFrame을 csv로 만들어 다운로드 링크 반환
def get_csv_download_link(df: pd.DataFrame, filename="report.csv"):
    csv = df.to_csv(index=False, encoding="utf-8-sig")
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 결과 CSV 다운로드</a>'
    return href

# -----------------------------
# UI: 헤더
# -----------------------------
st.markdown(
    """
    <div style="text-align:center; padding:12px 0;">
        <h1 style="color:#ff5c8a; font-size:42px; margin:6px;">💸 오늘의 소비, 내일의 나 — 스마트 절약 도우미 ✨</h1>
        <p style="color:#444; margin:0;">지출 내역을 업로드하면 자동으로 분석하고, 맞춤형 절약 미션과 팁을 드려요! 🎯</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")  # spacing

# -----------------------------
# 사이드바: 업로드 및 설정
# -----------------------------
with st.sidebar:
    st.header("업로드 & 설정 🛠️")
    st.markdown("CSV 파일 업로드 또는 예시 데이터 불러오기 후 분석을 시작하세요.")
    uploaded_file = st.file_uploader("📤 거래내역 CSV 업로드 (Date, Amount, Description 권장)", type=["csv", "txt"])
    st.markdown("---")
    use_sample = st.button("🔎 예시 데이터 불러오기 (테스트용)")
    st.markdown("---")
    budget_input = st.number_input("이번달 예산 설정 (원)", min_value=0, value=500000, step=10000, format="%d")
    st.markdown("**절약 목표**를 설정하면 미션과 예측이 더 정확해집니다.")
    st.markdown("---")
    st.caption("🔐 모든 분석은 로컬에서 실행됩니다. 데이터는 서버에 업로드되지 않습니다.")

# -----------------------------
# 데이터 로딩
# -----------------------------
df = None
if use_sample:
    # 간단한 예시 데이터 생성
    sample = {
        "Date": pd.date_range(end=datetime.today(), periods=30).tolist(),
        "Description": [
            "Starbucks", "Market", "Delivery - pizza", "Netflix", "Gym", "Taxi", "Restaurant",
            "Cafe", "Grocery mart", "Uber", "Bookstore", "Gas station", "Delivery - chicken",
            "Coffee shop", "Online store", "Restaurant", "Delivery - sushi", "Netflix", "Starbucks",
            "Market", "Grocery mart", "Taxi", "Gas station", "Cinema", "Hotel booking", "Delivery - pizza",
            "Cafe", "Online store", "Bookstore", "Gym"
        ],
        "Amount": [
            4500, 32000, 21000, 12800, 55000, 8500, 42000,
            5200, 46000, 12000, 18000, 40000, 23000,
            5400, 76000, 33000, 27000, 12800, 4500, 28000, 49000, 9000, 38000, 12000, 180000, 20000, 25000, 15000, 30000, 50000
        ]
    }
    df = pd.DataFrame(sample)
    st.success("예시 데이터가 불러와졌어요! 🎉")
elif uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("파일이 성공적으로 업로드 되었습니다 ✅")
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        st.stop()
else:
    st.info("왼쪽 사이드바에서 CSV를 업로드하거나 예시 데이터를 불러와 분석을 시작하세요 💡")
    st.stop()

# -----------------------------
# 데이터 정리
# -----------------------------
try:
    tx = normalize_transactions(df)
except Exception as e:
    st.error(f"데이터 정리 중 오류가 발생했습니다: {e}")
    st.stop()

# -----------------------------
# 상단 요약 카드
# -----------------------------
total_spent = tx["Amount"].sum()
this_month = datetime.now().strftime("%Y-%m")
month_mask = tx["YearMonth"] == this_month[:7]  # YearMonth 형식 'YYYY-MM'
spending_this_month = tx[tx["YearMonth"] == datetime.now().strftime("%Y-%m")]["Amount"].sum() if (tx["YearMonth"] == datetime.now().strftime("%Y-%m")).any() else 0.0

col1, col2, col3, col4 = st.columns([2,2,2,2])

with col1:
    st.markdown(f"**총 거래 건수** 🧾\n\n**{len(tx):,} 건**")
with col2:
    st.markdown(f"**총 지출 합계** 💳\n\n**{int(total_spent):,} 원**")
with col3:
    st.markdown(f"**이번달 지출(추정)** 🗓️\n\n**{int(spending_this_month):,} 원**")
with col4:
    budget_out = predict_budget_outcome(spending_this_month, budget_input)
    status_text = budget_out.get("message", "")
    st.markdown(f"**이번달 예산** 🎯\n\n**{int(budget_input):,} 원**\n\n{status_text}")

st.write("---")

# -----------------------------
# 카테고리별 분석 및 차트
# -----------------------------
st.subheader("카테고리별 소비 🔎")

summary_by_cat = tx.groupby("Category")["Amount"].sum().sort_values(ascending=False)
top_categories = summary_by_cat.head(6)

# 차트: 파이 차트 (matplotlib)
fig1, ax1 = plt.subplots(figsize=(6,4))
ax1.pie(top_categories, labels=top_categories.index, autopct="%1.1f%%", startangle=140, textprops={'fontsize':10})
ax1.axis("equal")
st.pyplot(fig1)

st.markdown("**상세 카테고리 금액 표**")
st.dataframe(summary_by_cat.to_frame("Amount").style.format("{:,.0f}"))

st.write("---")

# -----------------------------
# 월별 지출 추세
# -----------------------------
st.subheader("월별 지출 추세 📈")
trend = tx.groupby("YearMonth")["Amount"].sum().sort_index()
fig2, ax2 = plt.subplots(figsize=(8,3))
ax2.plot(trend.index, trend.values, marker="o")
ax2.set_title("월별 지출 합계")
ax2.set_xlabel("연-월")
ax2.set_ylabel("지출 (원)")
plt.xticks(rotation=45)
st.pyplot(fig2)

st.write("---")

# -----------------------------
# 상위 지출(가맹점) 및 세부 거래
# -----------------------------
st.subheader("상위 지출처 & 거래 내역 🔍")
# 상위 가맹점(Description 기준)
top_merchants = tx.groupby("Description")["Amount"].sum().sort_values(ascending=False).head(5)
st.table(top_merchants.to_frame("Amount").style.format("{:,.0f}"))

st.markdown("**원본 거래 일부 미리보기**")
st.dataframe(tx.sort_values(by="Date", ascending=False).head(20).style.format({"Amount":"{:,.0f}"}))

st.write("---")

# -----------------------------
# 절약 팁 & 미션 자동 생성
# -----------------------------
st.subheader("맞춤형 절약 팁 & 미션 🎯")
top_items = list(top_merchants.items()) if not top_merchants.empty else []
tips = generate_saving_tips(summary_by_cat, top_items, budget_out)

for t in tips:
    st.info(t)

st.markdown("### 절약 미션 생성기 🔥")
if st.button("🛡️ 지금 내 절약 미션 만들기"):
    missions = []
    # 간단한 규칙: 카페/음료 줄이기, 배달 줄이기, 구독 확인 등
    if any("카페" in c for c in summary_by_cat.index) and summary_by_cat[[c for c in summary_by_cat.index if "카페" in c]].sum() > 0:
        missions.append("주 3회 카페 → 주 1회로 줄이기 (한달 실천)")
    if any("배달" in c or "외식" in c for c in summary_by_cat.index) and summary_by_cat[[c for c in summary_by_cat.index if ("배달" in c or "외식" in c)]].sum() > 0:
        missions.append("이번 주 배달 0회 도전 (배달 대신 요리하기)")
    if any("구독" in c or "엔터" in c for c in summary_by_cat.index):
        missions.append("2주 내 사용하지 않은 구독 확인 후 정리하기")
    if not missions:
        missions.append("이번 달 지출 내역을 매주 한 번 점검하기 (지출 로그 습관화)")
    st.success("미션이 생성되었습니다! 아래에서 골라 실천해보세요 ✨")
    for m in missions:
        st.write(f"- ✅ {m}")

st.write("---")

# -----------------------------
# 예산 예측 및 시나리오
# -----------------------------
st.subheader("예산 시나리오 시뮬레이터 🧮")
st.markdown("간단 시뮬레이터로 지출을 조정했을 때 예산 달성 가능성을 확인해보세요.")

col_a, col_b = st.columns([2,3])
with col_a:
    reduction_percent = st.slider("월 지출을 몇 % 줄여볼까요?", min_value=0, max_value=50, value=10, step=5)
    hypothetical = spending_this_month * (1 - reduction_percent/100.0)
    st.markdown(f"예상 월 지출(감소 {reduction_percent}% 적용): **{int(hypothetical):,} 원**")
    result = predict_budget_outcome(hypothetical, budget_input)
    st.markdown("예산 시뮬레이션 결과:")
    st.write(result["message"])

with col_b:
    st.markdown("💡 실천 아이디어")
    st.markdown("- 커피 줄이기 챌린지 ☕\n- 배달 1회 줄이기 🍱\n- 잔돈 모으기 자동저축 앱 연결 💾")

st.write("---")

# -----------------------------
# 리포트 다운로드
# -----------------------------
st.subheader("리포트 생성 및 다운로드 📥")
report_df = tx.copy()
report_df["CategorySummary"] = report_df["Category"]

st.markdown(get_csv_download_link(report_df, filename="spending_report.csv"), unsafe_allow_html=True)
st.write("CSV 파일에는 거래내역과 자동 분류된 카테고리가 포함됩니다.")

# -----------------------------
# 뱃지 & 보상 UI
# -----------------------------
st.write("---")
st.subheader("달성 뱃지 🏅")
# 아주 간단한 뱃지 논리
badges = []
if spending_this_month <= budget_input * 0.8:
    badges.append(("절약 마스터", "이번 달 예산 80% 이하 사용 — 굿 잡! 🎉"))
if spending_this_month <= budget_input and spending_this_month > budget_input*0.8:
    badges.append(("균형 잡힌 소비", "예산 안에서 잘 유지 중이에요. 👏"))
if spending_this_month > budget_input:
    badges.append(("주의 요망", "예산 초과 — 작은 미션부터 시작해보세요! ⚠️"))
if not badges:
    badges.append(("시작 단계", "데이터가 충분치 않아요 — 더 많은 거래를 업로드 해보세요."))

for name, note in badges:
    st.markdown(f"**🏷️ {name}** — _{note}_")

st.write("---")

# -----------------------------
# 추가: 수동 거래 추가 UI (간단)
# -----------------------------
st.subheader("수동 거래 추가 ✍️")
with st.form("add_tx"):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        d = st.date_input("날짜", value=datetime.today())
    with c2:
        desc = st.text_input("설명", value="직접 입력")
    with c3:
        amt = st.number_input("금액", min_value=0, value=1000, step=100)
    with c4:
        cat = st.text_input("카테고리 (선택)", value="")
    submitted = st.form_submit_button("➕ 거래 추가")
    if submitted:
        new_row = {
            "Date": pd.to_datetime(d),
            "Description": desc,
            "Amount": float(amt),
            "Category": cat if cat.strip() != "" else categorize_description(desc),
            "YearMonth": pd.to_datetime(d).to_period("M").astype(str)
        }
        tx = pd.concat([tx, pd.DataFrame([new_row])], ignore_index=True)
        st.success("거래가
