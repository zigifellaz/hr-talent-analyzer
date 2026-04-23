import streamlit as st
import anthropic
import base64
import io
import json
import re
from pathlib import Path

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Talent Intelligence · M.I.Tech",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS — Editorial Luxury ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=Noto+Serif+KR:wght@300;400;600;700&family=Noto+Sans+KR:wght@300;400;500;600&display=swap');

:root {
    --ink:       #1A1714;
    --ink-2:     #3D3830;
    --ink-3:     #7A7268;
    --ink-4:     #B0A898;
    --paper:     #F7F3ED;
    --paper-2:   #EDE8E0;
    --paper-3:   #E2DDD4;
    --gold:      #B8924A;
    --gold-lt:   #D4AF72;
    --slate:     #2B3D5C;
    --slate-lt:  #4A6080;
    --red:       #8B2635;
    --green:     #2D6A4F;
    --rule:      #D4CEC4;
}

/* ── Reset & Base ── */
html, body, .stApp {
    background-color: var(--paper) !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', 'Noto Sans KR', sans-serif !important;
}

/* Grain overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
    opacity: 0.6;
}

/* ── Masthead ── */
.masthead {
    border-bottom: 2px solid var(--ink);
    padding: 1.8rem 0 1.2rem 0;
    margin-bottom: 0;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
}
.masthead-brand {
    font-family: 'DM Serif Display', 'Noto Serif KR', serif;
    font-size: 2.6rem;
    font-weight: 400;
    color: var(--ink);
    letter-spacing: -1px;
    line-height: 1;
}
.masthead-brand em {
    font-style: italic;
    color: var(--gold);
}
.masthead-meta {
    font-size: 0.7rem;
    color: var(--ink-3);
    text-align: right;
    letter-spacing: 2px;
    text-transform: uppercase;
    line-height: 1.8;
}
.masthead-rule {
    height: 1px;
    background: var(--ink);
    margin: 0.3rem 0 2rem 0;
}
.masthead-thin {
    height: 1px;
    background: var(--rule);
    margin: 0.4rem 0 0 0;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2.2rem 0 1.2rem 0;
}
.section-num {
    font-family: 'DM Serif Display', serif;
    font-size: 0.75rem;
    color: var(--gold);
    letter-spacing: 3px;
    font-style: italic;
    min-width: 24px;
}
.section-title {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--ink-2);
    border-bottom: none;
    padding: 0;
    margin: 0;
}
.section-rule {
    flex: 1;
    height: 1px;
    background: var(--rule);
}

/* ── Input Fields ── */
.stTextInput > div > div {
    background: white !important;
    border: 1px solid var(--rule) !important;
    border-radius: 4px !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div:focus-within {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(184,146,74,0.1) !important;
}
.stTextArea > div > div {
    background: white !important;
    border: 1px solid var(--rule) !important;
    border-radius: 4px !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
.stTextArea > div > div:focus-within {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(184,146,74,0.1) !important;
}
label, .stTextInput label, .stTextArea label {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--ink-3) !important;
}

/* ── Upload Cards ── */
.upload-item {
    background: white;
    border: 1px solid var(--rule);
    border-radius: 6px;
    padding: 1rem 1.2rem 0.6rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.upload-item:hover {
    border-color: var(--gold);
    box-shadow: 0 2px 12px rgba(184,146,74,0.08);
}
.upload-item-title {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--ink);
    letter-spacing: 0.5px;
    margin-bottom: 0.15rem;
}
.upload-item-desc {
    font-size: 0.7rem;
    color: var(--ink-4);
    margin-bottom: 0.5rem;
}

/* ── File Uploader ── */
.stFileUploader > div {
    background: var(--paper-2) !important;
    border: 1.5px dashed var(--rule) !important;
    border-radius: 6px !important;
    transition: border-color 0.2s !important;
}
.stFileUploader > div:hover {
    border-color: var(--gold) !important;
}
.stFileUploader label { display: none !important; }

/* ── Analyze Button ── */
.stButton > button {
    background: var(--ink) !important;
    color: var(--paper) !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.85rem 2.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    transition: all 0.25s !important;
    width: 100% !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, var(--gold) 0%, var(--slate) 100%);
    opacity: 0;
    transition: opacity 0.3s;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(26,23,20,0.25) !important;
    letter-spacing: 4px !important;
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: white !important;
    border: 1px solid var(--rule) !important;
    border-radius: 6px !important;
}
.streamlit-expanderHeader {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    color: var(--ink-2) !important;
    text-transform: uppercase !important;
}

/* ── Result: Report Cover ── */
.report-cover {
    background: var(--ink);
    border-radius: 8px;
    padding: 3rem 3.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.report-cover::after {
    content: '◈';
    position: absolute;
    right: 3rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 8rem;
    color: rgba(255,255,255,0.04);
    line-height: 1;
    pointer-events: none;
}
.report-cover-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1rem;
}
.report-cover-name {
    font-family: 'DM Serif Display', 'Noto Serif KR', serif;
    font-size: 3rem;
    font-weight: 400;
    color: var(--paper);
    line-height: 1.1;
    margin-bottom: 0.8rem;
    letter-spacing: -1px;
}
.report-cover-summary {
    font-size: 0.95rem;
    color: rgba(247,243,237,0.65);
    line-height: 1.7;
    font-weight: 300;
    max-width: 580px;
    margin-bottom: 1.5rem;
}
.tag-chip {
    display: inline-block;
    border: 1px solid rgba(184,146,74,0.5);
    color: var(--gold-lt);
    border-radius: 3px;
    padding: 0.25rem 0.7rem;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 1px;
    margin: 0.2rem 0.2rem 0 0;
    text-transform: uppercase;
}

/* ── Dimension Cards ── */
.dim-card {
    background: white;
    border: 1px solid var(--rule);
    border-radius: 6px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s;
}
.dim-card:hover {
    box-shadow: 0 4px 20px rgba(26,23,20,0.08);
}
.dim-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--gold);
}
.dim-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1rem;
}
.dim-icon-title {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.dim-icon {
    width: 32px;
    height: 32px;
    background: var(--paper-2);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
}
.dim-name {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--ink);
    letter-spacing: 0.5px;
}
.dim-sub {
    font-size: 0.65rem;
    color: var(--ink-4);
    letter-spacing: 1px;
    text-transform: uppercase;
}
.dim-score-block {
    text-align: right;
}
.dim-score {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: var(--ink);
    line-height: 1;
    font-style: italic;
}
.dim-score span {
    font-size: 0.9rem;
    color: var(--ink-4);
    font-style: normal;
    font-family: 'DM Sans', sans-serif;
}
.dim-grade {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2px;
    margin-top: 0.2rem;
    text-transform: uppercase;
}
.progress-track {
    height: 3px;
    background: var(--paper-3);
    border-radius: 999px;
    margin: 0.8rem 0 1rem 0;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--gold), var(--slate));
}
.dim-summary {
    font-size: 0.83rem;
    color: var(--ink-2);
    line-height: 1.75;
    margin-bottom: 0.8rem;
}
.evidence-list {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
    padding-top: 0.8rem;
    border-top: 1px solid var(--paper-3);
}
.evidence-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: var(--ink-3);
    line-height: 1.5;
}
.evidence-dot {
    width: 4px;
    height: 4px;
    background: var(--gold);
    border-radius: 50%;
    margin-top: 0.45rem;
    flex-shrink: 0;
}

/* ── Keyword Cards ── */
.kw-card {
    background: white;
    border: 1px solid var(--rule);
    border-radius: 6px;
    padding: 1.8rem 2rem;
    margin-bottom: 1rem;
    display: grid;
    grid-template-columns: 56px 1fr;
    gap: 1.5rem;
    align-items: start;
    transition: box-shadow 0.2s;
}
.kw-card:hover {
    box-shadow: 0 4px 20px rgba(26,23,20,0.08);
}
.kw-rank-col {
    text-align: center;
    padding-top: 0.2rem;
}
.kw-rank-num {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    font-style: italic;
    line-height: 1;
}
.rank-gold { color: #B8924A; }
.rank-silver { color: #8A9BA8; }
.rank-bronze { color: #9B7B5A; }
.kw-rank-label {
    font-size: 0.6rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--ink-4);
    display: block;
    margin-top: 0.2rem;
}
.kw-title {
    font-family: 'DM Serif Display', 'Noto Serif KR', serif;
    font-size: 1.35rem;
    color: var(--ink);
    margin-bottom: 0.5rem;
    line-height: 1.2;
}
.kw-why {
    font-size: 0.82rem;
    color: var(--ink-2);
    line-height: 1.75;
    margin-bottom: 0.9rem;
}
.kw-how {
    background: var(--paper-2);
    border-radius: 4px;
    padding: 0.8rem 1rem;
    border-left: 2px solid var(--gold);
}
.kw-how-label {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.4rem;
}
.kw-how-text {
    font-size: 0.8rem;
    color: var(--ink-2);
    line-height: 1.65;
}

/* ── Insight Box ── */
.insight-box {
    background: var(--slate);
    border-radius: 8px;
    padding: 2.5rem 3rem;
    position: relative;
    overflow: hidden;
}
.insight-box::before {
    content: '"';
    position: absolute;
    left: 2rem;
    top: -1rem;
    font-family: 'DM Serif Display', serif;
    font-size: 10rem;
    color: rgba(255,255,255,0.06);
    line-height: 1;
    pointer-events: none;
}
.insight-label {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: rgba(212,175,114,0.8);
    margin-bottom: 1rem;
}
.insight-text {
    font-family: 'DM Sans', 'Noto Sans KR', sans-serif;
    font-size: 0.95rem;
    color: rgba(247,243,237,0.85);
    line-height: 2;
    font-weight: 300;
}

/* ── Horizontal Rule ── */
.hr {
    height: 1px;
    background: var(--rule);
    border: none;
    margin: 2.5rem 0;
}

/* ── Success / Error ── */
.stSuccess { background: #EAF4EE !important; border-color: var(--green) !important; }
.stError { background: #FAEAEC !important; border-color: var(--red) !important; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ────────────────────────────────────────────────────────────────
def read_file_content(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    content = uploaded_file.read()
    if name.endswith(".pdf"):
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                return "\n".join(p.extract_text() or "" for p in pdf.pages)
        except Exception:
            pass
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        except Exception:
            return "[PDF — 텍스트 추출 실패]"
    if name.endswith(".docx"):
        try:
            import docx
            doc = docx.Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            return "[DOCX — 텍스트 추출 실패]"
    if any(name.endswith(e) for e in [".jpg", ".jpeg", ".png", ".webp", ".gif"]):
        b64 = base64.standard_b64encode(content).decode()
        return f"__IMAGE__{name}__BASE64__{b64}__MIMETYPE__{uploaded_file.type}"
    try:
        return content.decode("utf-8")
    except Exception:
        try:
            return content.decode("cp949")
        except Exception:
            return "[파일 읽기 실패]"


def build_user_content(file_data, candidate_name, company_standard):
    user_content = []
    text_parts = []
    if candidate_name:
        text_parts.append(f"[대상자 이름] {candidate_name}")
    if company_standard:
        text_parts.append(f"[회사 인재상]\n{company_standard}")
    for label, content in file_data.items():
        if content and not content.startswith("__IMAGE__"):
            text_parts.append(f"[{label}]\n{content}")
    if text_parts:
        user_content.append({"type": "text", "text": "\n\n".join(text_parts)})
    for label, content in file_data.items():
        if content and content.startswith("__IMAGE__"):
            try:
                parts = content.split("__")
                b64_data = parts[4]
                mime_type = parts[6] if len(parts) > 6 else "image/jpeg"
                user_content.append({"type": "image", "source": {"type": "base64", "media_type": mime_type, "data": b64_data}})
                user_content.append({"type": "text", "text": f"위 이미지는 [{label}] 자료입니다."})
            except Exception:
                pass
    return user_content


def analyze_candidate(api_key, file_data, candidate_name, company_standard):
    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = """당신은 기업 HR 전문가이자 조직심리학자입니다.
제공된 자료를 바탕으로 해당 인원을 4개 차원에서 전문 분석하고, 동일 유형 인재 채용 키워드를 순위별로 제시하세요.

반드시 아래 JSON 형식으로만 응답하세요:
{
  "candidate_summary": "대상자 종합 한줄 평가 (60자 내외)",
  "personality_tags": ["태그1","태그2","태그3","태그4","태그5"],
  "dimensions": {
    "cognitive_ability": {"score":75,"grade":"B+","summary":"3-4문장 분석","evidence":["근거1","근거2","근거3"]},
    "job_expertise":     {"score":80,"grade":"A", "summary":"3-4문장 분석","evidence":["근거1","근거2","근거3"]},
    "proactiveness":     {"score":70,"grade":"B", "summary":"3-4문장 분석","evidence":["근거1","근거2","근거3"]},
    "leadership":        {"score":65,"grade":"B-","summary":"3-4문장 분석","evidence":["근거1","근거2","근거3"]}
  },
  "hiring_keywords": [
    {"rank":1,"keyword":"키워드","why":"2-3문장 선정 이유","how_to_check":"구체적 확인 방법"},
    {"rank":2,"keyword":"키워드","why":"2-3문장 선정 이유","how_to_check":"구체적 확인 방법"},
    {"rank":3,"keyword":"키워드","why":"2-3문장 선정 이유","how_to_check":"구체적 확인 방법"}
  ],
  "overall_insight": "전체 인재 유형 심층 인사이트 및 조직 내 예상 역할 (4-5문장)"
}
점수 100점 만점. 자료 없는 항목은 가용 정보로 추론 후 표기."""

    user_content = build_user_content(file_data, candidate_name, company_standard)
    if not user_content:
        raise ValueError("분석할 자료가 없습니다.")
    user_content.append({"type": "text", "text": "위 자료를 바탕으로 JSON 형식으로 인재 분석을 수행해주세요."})

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}]
    )
    raw = response.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def grade_color(grade):
    return {"A+":"#2D6A4F","A":"#2D6A4F","B+":"#2B3D5C","B":"#2B3D5C",
            "B-":"#8B6914","C+":"#8B2635","C":"#8B2635"}.get(grade, "#7A7268")

def dim_label(k):
    return {"cognitive_ability":"인지 능력","job_expertise":"잡 전문성",
            "proactiveness":"적극성","leadership":"리더십"}.get(k, k)

def dim_sublabel(k):
    return {"cognitive_ability":"Cognitive Ability","job_expertise":"Job Expertise",
            "proactiveness":"Proactiveness","leadership":"Leadership"}.get(k, k)

def dim_icon(k):
    return {"cognitive_ability":"🧠","job_expertise":"⚙️",
            "proactiveness":"🔥","leadership":"👑"}.get(k,"◈")


# ─── UI ─────────────────────────────────────────────────────────────────────

# Masthead
st.markdown("""
<div class="masthead">
    <div>
        <div class="masthead-brand">Talent <em>Intelligence</em></div>
    </div>
    <div class="masthead-meta">
        M.I.TECH · P&C TEAM<br>
        인재 심층 분석 플랫폼<br>
        INTERNAL USE ONLY
    </div>
</div>
<div class="masthead-rule"></div>
<div class="masthead-thin"></div>
""", unsafe_allow_html=True)

# ── Section 1: API ──
with st.expander("⚙  API KEY 설정", expanded=False):
    api_key = st.text_input("Anthropic API Key", type="password",
                             placeholder="sk-ant-api03-...",
                             help="console.anthropic.com에서 발급")

# ── Section 2: Candidate Info ──
st.markdown("""
<div class="section-header">
    <span class="section-num">01</span>
    <span class="section-title">대상자 기본 정보</span>
    <div class="section-rule"></div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    candidate_name = st.text_input("성명", placeholder="홍길동")
with c2:
    candidate_dept = st.text_input("소속 부서", placeholder="Sales & Marketing Division")

company_standard = st.text_area(
    "회사 인재상",
    placeholder="예: 도전정신, 전문성, 협업능력, 고객 중심 사고, 글로벌 역량...",
    height=72
)

# ── Section 3: Upload ──
st.markdown("""
<div class="section-header">
    <span class="section-num">02</span>
    <span class="section-title">자료 업로드</span>
    <div class="section-rule"></div>
</div>
<p style="font-size:0.75rem;color:#B0A898;margin:-0.5rem 0 1.2rem 0;">
PDF · DOCX · JPG · PNG · TXT 지원 &nbsp;|&nbsp; 없는 항목은 건너뜁니다
</p>
""", unsafe_allow_html=True)

upload_items = [
    ("이력서 / 자기소개서",  "resume",    "학력·경력·수상·자격증"),
    ("다면평가 결과",        "peer_eval", "상사·동료·부하 다방향 평가"),
    ("대상자 작성 기안서",   "proposal",  "품의서·기획안·보고서"),
    ("MBTI 결과",           "mbti",      "유형지 또는 스크린샷"),
    ("인적성 검사 결과표",   "aptitude",  "인지·성격 검사 점수"),
    ("SNS / 포트폴리오",    "sns",       "LinkedIn·블로그·GitHub"),
    ("소속 부서 자료",       "dept_info", "팀 미션·조직도"),
    ("회사 인재상 파일",     "talent_std","별도 파일 제출 시"),
]

file_data = {}
col_a, col_b = st.columns(2)
for i, (label, key, desc) in enumerate(upload_items):
    with (col_a if i % 2 == 0 else col_b):
        st.markdown(f"""
        <div class="upload-item">
            <div class="upload-item-title">{label}</div>
            <div class="upload-item-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        uploaded = st.file_uploader(
            f"_{key}", key=key, label_visibility="collapsed",
            type=["pdf","docx","jpg","jpeg","png","webp","txt","md"]
        )
        if uploaded:
            file_data[label] = read_file_content(uploaded)
            st.caption(f"✓ {uploaded.name}")

if candidate_dept:
    file_data["소속 부서"] = candidate_dept
if company_standard:
    file_data["회사 인재상"] = company_standard

# ── Divider ──
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Run Button ──
run = st.button("◈  분석 시작", use_container_width=True)

if run:
    if not api_key:
        st.error("API Key를 먼저 입력해주세요.")
    elif not file_data and not candidate_name:
        st.error("자료를 최소 1개 이상 업로드하거나 성명을 입력해주세요.")
    else:
        with st.spinner("분석 중 — 업로드된 자료를 종합 검토하고 있습니다..."):
            try:
                R = analyze_candidate(api_key, file_data, candidate_name, company_standard)

                # ── Report Cover ──
                name_d = candidate_name or "대상자"
                tags_html = "".join(
                    f'<span class="tag-chip">{t}</span>'
                    for t in R.get("personality_tags", [])
                )
                st.markdown(f"""
                <div class="report-cover">
                    <div class="report-cover-label">◈ Talent Analysis Report</div>
                    <div class="report-cover-name">{name_d}</div>
                    <div class="report-cover-summary">{R.get('candidate_summary','')}</div>
                    <div>{tags_html}</div>
                </div>
                """, unsafe_allow_html=True)

                # ── Dimensions ──
                st.markdown("""
                <div class="section-header">
                    <span class="section-num">03</span>
                    <span class="section-title">역량 차원 분석</span>
                    <div class="section-rule"></div>
                </div>
                """, unsafe_allow_html=True)

                dims = R.get("dimensions", {})
                d_col1, d_col2 = st.columns(2)
                for idx, (key, info) in enumerate(dims.items()):
                    score = info.get("score", 0)
                    grade = info.get("grade", "-")
                    gcolor = grade_color(grade)
                    ev_html = "".join(
                        f'<div class="evidence-item"><div class="evidence-dot"></div><span>{e}</span></div>'
                        for e in info.get("evidence", [])
                    )
                    with (d_col1 if idx % 2 == 0 else d_col2):
                        st.markdown(f"""
                        <div class="dim-card">
                            <div class="dim-header">
                                <div class="dim-icon-title">
                                    <div class="dim-icon">{dim_icon(key)}</div>
                                    <div>
                                        <div class="dim-name">{dim_label(key)}</div>
                                        <div class="dim-sub">{dim_sublabel(key)}</div>
                                    </div>
                                </div>
                                <div class="dim-score-block">
                                    <div class="dim-score">{score}<span>/100</span></div>
                                    <div class="dim-grade" style="color:{gcolor};">{grade}</div>
                                </div>
                            </div>
                            <div class="progress-track">
                                <div class="progress-fill" style="width:{score}%;"></div>
                            </div>
                            <div class="dim-summary">{info.get('summary','')}</div>
                            <div class="evidence-list">{ev_html}</div>
                        </div>
                        """, unsafe_allow_html=True)

                # ── Keywords ──
                st.markdown("""
                <div class="section-header" style="margin-top:2.5rem;">
                    <span class="section-num">04</span>
                    <span class="section-title">채용 핵심 키워드 Top 3</span>
                    <div class="section-rule"></div>
                </div>
                <p style="font-size:0.75rem;color:#B0A898;margin:-0.5rem 0 1.5rem 0;">
                동일 유형 인재 채용 시 면접·서류에서 중점 확인해야 할 체크포인트
                </p>
                """, unsafe_allow_html=True)

                rank_classes = ["rank-gold", "rank-silver", "rank-bronze"]
                rank_labels  = ["1st", "2nd", "3rd"]
                for kw in R.get("hiring_keywords", []):
                    r = kw.get("rank", 1) - 1
                    rc = rank_classes[r] if r < 3 else "rank-bronze"
                    rl = rank_labels[r] if r < 3 else f"{r+1}th"
                    st.markdown(f"""
                    <div class="kw-card">
                        <div class="kw-rank-col">
                            <div class="kw-rank-num {rc}">{r+1}</div>
                            <span class="kw-rank-label">{rl}</span>
                        </div>
                        <div>
                            <div class="kw-title">{kw.get('keyword','')}</div>
                            <div class="kw-why">{kw.get('why','')}</div>
                            <div class="kw-how">
                                <div class="kw-how-label">확인 방법</div>
                                <div class="kw-how-text">{kw.get('how_to_check','')}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # ── Insight ──
                st.markdown("""
                <div class="section-header" style="margin-top:2.5rem;">
                    <span class="section-num">05</span>
                    <span class="section-title">종합 인사이트</span>
                    <div class="section-rule"></div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="insight-box">
                    <div class="insight-label">◈ Overall Insight</div>
                    <div class="insight-text">{R.get('overall_insight','')}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div style="text-align:center;padding:2.5rem 0 1rem;font-size:0.65rem;
                     letter-spacing:3px;text-transform:uppercase;color:#B0A898;">
                    Analysis Complete &nbsp;·&nbsp; M.I.Tech Talent Intelligence &nbsp;·&nbsp; Internal Use Only
                </div>
                """, unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("결과 파싱 오류 — 업로드 자료 확인 후 재시도해주세요.")
            except anthropic.AuthenticationError:
                st.error("API Key가 유효하지 않습니다.")
            except Exception as e:
                st.error(f"오류 발생: {e}")

# Footer
st.markdown("""
<div style="text-align:center;padding:3rem 0 1.5rem;font-size:0.65rem;
     letter-spacing:2px;text-transform:uppercase;color:#C8C0B4;border-top:1px solid #E2DDD4;margin-top:3rem;">
    Talent Intelligence Platform &nbsp;·&nbsp; M.I.Tech P&C Team &nbsp;·&nbsp; Powered by Claude AI
</div>
""", unsafe_allow_html=True)
