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

/* ── 좌우 여백 ── */
.block-container {
    max-width: 960px !important;
    padding-left: 6rem !important;
    padding-right: 6rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
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
    system_prompt = """당신은 글로벌 탑티어 HR 컨설팅 펌(McKinsey People & Organization, Korn Ferry, Spencer Stuart 수준)의 수석 어세스먼트 컨설턴트입니다. 조직심리학 박사 학위와 15년 이상의 임원 평가 및 인재 어세스먼트 경험을 보유하고 있습니다.

당신의 분석은 다음 프레임워크를 통합적으로 적용합니다:
- Korn Ferry의 Leadership Architect (역량 모델 67개 팩터)
- SHL의 OPQ32 (성격 및 행동 선호도 측정)
- Hogan Assessment의 HPI/HDS/MVPI (명시적 성격 / 암묵적 위험 요소 / 동기 가치 체계)
- DDI의 Targeted Selection (행동사건 면접법 기반 역량 평가)
- MBTI 및 Big Five(OCEAN) 모델과의 교차 검증

━━━━━━━━━━━━━━━━━━━━━━━━
분석 원칙
━━━━━━━━━━━━━━━━━━━━━━━━
1. 근거 기반 추론: 모든 평가는 제공된 자료에서 직접 인용 가능한 구체적 근거를 바탕으로 합니다. 추측성 표현("~할 것 같다") 대신 행동 증거 기반 표현("~한 이력이 확인된다")을 사용합니다.
2. 다층적 교차 검증: 단일 자료가 아닌 복수 자료 간 일관성·불일치를 분석하여 표면 행동과 내재 동기를 구분합니다.
3. 조직 적합도 연계: 개인 역량 분석을 회사 인재상 및 직무 요구사항과 명시적으로 연결합니다.
4. 위험 요인 식별: 강점 이면의 잠재적 취약점(Derailer)을 전문가 시각으로 도출합니다.
5. 실용적 채용 전환: 분석 결과를 실제 채용 현장에서 즉시 활용 가능한 행동 지표로 전환합니다.

━━━━━━━━━━━━━━━━━━━━━━━━
각 차원별 평가 기준
━━━━━━━━━━━━━━━━━━━━━━━━
[인지 능력 - Cognitive Ability]
- 개념적 사고력: 복잡한 정보를 구조화하고 패턴을 도출하는 능력
- 분석적 추론: 데이터/상황에서 핵심 변수를 식별하고 인과관계를 파악하는 능력
- 학습 민첩성 (Learning Agility): 새로운 환경과 정보에 빠르게 적응하는 능력
- 의사결정 질: 불확실한 상황에서 논리적이고 신속한 판단을 내리는 능력

[잡 전문성 - Job Expertise]
- 직무 지식 깊이: 해당 산업/직무의 핵심 지식 및 기술 수준
- 실행 역량: 지식을 실제 성과로 전환하는 능력 (KPI 달성 이력 포함)
- 도메인 네트워크: 업계 내 관계망과 시장 이해도
- 글로벌 역량: 크로스컬처 환경에서의 협업·소통 능력

[적극성 - Proactiveness]
- 주도성 (Initiative): 지시 없이 과제를 발굴하고 선제적으로 행동하는 성향
- 결과 지향성 (Achievement Drive): 목표 달성에 대한 내적 동기 강도
- 변화 주도: 현상 유지보다 개선과 혁신을 추구하는 성향
- 역경 극복 (Resilience): 실패와 장애 상황에서의 회복탄력성

[리더십 - Leadership]
- 영향력 행사: 공식 권한 없이도 타인을 설득하고 이끄는 능력
- 팀 개발: 구성원의 성장을 지원하고 동기를 부여하는 능력
- 전략적 방향 설정: 조직의 장기 비전을 수립하고 전달하는 능력
- 이해관계자 관리: 내외부 이해관계자와의 관계를 전략적으로 구축하는 능력

━━━━━━━━━━━━━━━━━━━━━━━━
점수 산출 기준 (100점 만점)
━━━━━━━━━━━━━━━━━━━━━━━━
90-100 (S): 동종업계 상위 5% 수준. 해당 역량의 롤모델.
80-89 (A): 상위 15% 수준. 명확한 강점으로 조직에 즉각적 기여 가능.
70-79 (B+): 상위 30% 수준. 강점이 있으나 일부 개발 영역 존재.
60-69 (B): 평균 수준. 기본 역량은 갖추었으나 차별화 요소 미흡.
50-59 (B-): 평균 이하. 해당 역량에서 주의 깊은 관찰과 개발 지원 필요.
49 이하 (C): 유의미한 약점. 해당 역량이 직무 핵심 요건이라면 채용 리스크.

반드시 아래 JSON 형식으로만 응답하세요. JSON 외 어떤 텍스트도 출력하지 마세요:
{
  "candidate_summary": "대상자 핵심 특성을 컨설팅 언어로 표현한 한줄 평가 (70자 내외, 구체적 강점과 포지셔닝 포함)",
  "personality_tags": ["핵심역량태그1","핵심역량태그2","성향태그3","리스크태그4","포지셔닝태그5"],
  "dimensions": {
    "cognitive_ability": {
      "score": 75,
      "grade": "B+",
      "summary": "4-5문장의 전문 컨설팅 수준 분석. 강점의 구체적 발현 방식, 내재된 인지 패턴, 조직 내 활용 가능성, 잠재적 한계까지 포함",
      "evidence": ["자료에서 직접 확인된 구체적 행동 근거 1", "수치나 사례가 포함된 근거 2", "복수 자료 교차 확인된 근거 3"]
    },
    "job_expertise": {
      "score": 80,
      "grade": "A",
      "summary": "4-5문장의 전문 컨설팅 수준 분석",
      "evidence": ["근거1", "근거2", "근거3"]
    },
    "proactiveness": {
      "score": 70,
      "grade": "B",
      "summary": "4-5문장의 전문 컨설팅 수준 분석",
      "evidence": ["근거1", "근거2", "근거3"]
    },
    "leadership": {
      "score": 65,
      "grade": "B-",
      "summary": "4-5문장의 전문 컨설팅 수준 분석",
      "evidence": ["근거1", "근거2", "근거3"]
    }
  },
  "hiring_keywords": [
    {
      "rank": 1,
      "keyword": "10자 이내 핵심 역량 키워드",
      "why": "이 키워드가 1순위인 이유를 회사 인재상·직무 요건과 연결하여 3-4문장으로 설명. 해당 인재 유형의 본질적 특성과 연결",
      "how_to_check": "면접관이 실제로 사용할 수 있는 구체적 질문 2가지와 평가 포인트 포함. 행동사건 면접법(STAR: Situation-Task-Action-Result) 기반으로 작성"
    },
    {
      "rank": 2,
      "keyword": "10자 이내 핵심 역량 키워드",
      "why": "3-4문장 설명",
      "how_to_check": "구체적 질문과 평가 포인트"
    },
    {
      "rank": 3,
      "keyword": "10자 이내 핵심 역량 키워드",
      "why": "3-4문장 설명",
      "how_to_check": "구체적 질문과 평가 포인트"
    }
  ],
  "derailer": "이 인재 유형의 잠재적 위험 요소(Derailer) — 스트레스 상황이나 장기 재직 시 나타날 수 있는 부정적 행동 패턴과 조직 내 주의사항을 2-3문장으로 기술",
  "development_suggestion": "이 인재가 조직에서 최고 성과를 내기 위해 필요한 환경 조건·관리 방식·개발 과제를 2-3문장으로 제시",
  "overall_insight": "McKinsey, Korn Ferry 수준의 임원 평가 리포트 언어로 작성한 종합 인사이트. 대상자의 인재 유형 명명, 조직 내 최적 포지셔닝, 단기·중장기 기여 가능성, 채용 의사결정을 위한 최종 권고를 5-6문장으로 기술"
}"""

    user_content = build_user_content(file_data, candidate_name, company_standard)
    if not user_content:
        raise ValueError("분석할 자료가 없습니다.")
    user_content.append({"type": "text", "text": "위 자료를 바탕으로 글로벌 탑티어 HR 컨설팅 펌 수준의 전문 인재 분석을 JSON 형식으로 수행해주세요. 모든 평가는 제공된 자료의 구체적 근거에 기반해야 하며, 표면적 관찰을 넘어 내재된 역량 패턴과 조직 적합도를 심층 분석해주세요."})

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=6000,
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

# ── API Key: Streamlit Secrets에서 자동 로드 ──
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    st.error("⚠️ 서버 설정 오류입니다. 관리자에게 문의해주세요.")
    st.stop()

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

# ── Section 2: Upload ──
st.markdown("""
<div class="section-header">
    <span class="section-num">02</span>
    <span class="section-title">자료 업로드</span>
    <div class="section-rule"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:white;border:1px solid #D4CEC4;border-radius:8px;padding:1.2rem 1.5rem;margin-bottom:1rem;">
    <p style="font-size:0.8rem;font-weight:600;color:#1A1714;margin-bottom:0.6rem;">📎 아래 자료를 한꺼번에 선택해서 업로드하세요</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.3rem 2rem;">
        <div style="font-size:0.75rem;color:#7A7268;">✦ 이력서 / 자기소개서</div>
        <div style="font-size:0.75rem;color:#7A7268;">✦ 다면평가 결과</div>
        <div style="font-size:0.75rem;color:#7A7268;">✦ 대상자 작성 기안서</div>
        <div style="font-size:0.75rem;color:#7A7268;">✦ MBTI 결과 (스크린샷 가능)</div>
        <div style="font-size:0.75rem;color:#7A7268;">✦ 인적성 검사 결과표</div>
        <div style="font-size:0.75rem;color:#7A7268;">✦ SNS / 포트폴리오</div>
        <div style="font-size:0.75rem;color:#7A7268;">✦ 소속 부서 자료</div>
        <div style="font-size:0.75rem;color:#7A7268;">✦ 회사 인재상 파일</div>
    </div>
    <p style="font-size:0.7rem;color:#B0A898;margin-top:0.8rem;margin-bottom:0;">
        PDF · DOCX · JPG · PNG · TXT 지원 &nbsp;|&nbsp; 없는 자료는 건너뛰어도 됩니다
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "파일을 여기에 끌어다 놓거나 클릭해서 선택하세요 (여러 파일 동시 선택 가능)",
    type=["pdf","docx","jpg","jpeg","png","webp","txt","md"],
    accept_multiple_files=True,
    label_visibility="visible"
)

file_data = {}
if uploaded_files:
    st.markdown(f'<p style="font-size:0.78rem;color:#2D6A4F;margin:0.5rem 0;">✅ {len(uploaded_files)}개 파일 업로드 완료</p>', unsafe_allow_html=True)
    for uploaded in uploaded_files:
        content = read_file_content(uploaded)
        file_data[uploaded.name] = content

if candidate_dept:
    file_data["소속 부서"] = candidate_dept
if company_standard:
    file_data["회사 인재상"] = company_standard

# ── Section 3: 분석 결과 안내 ──
st.markdown("""
<div class="section-header">
    <span class="section-num">03</span>
    <span class="section-title">분석 결과 안내</span>
    <div class="section-rule"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-bottom:1rem;">

    <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;padding:1.2rem 1.4rem;border-left:3px solid #B8924A;">
        <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#B8924A;margin-bottom:0.5rem;">01 · 대상자 프로필</div>
        <div style="font-size:0.82rem;color:#3D3830;line-height:1.7;">
            종합 한줄 평가와 함께 대상자의 핵심 성향을 <b>태그</b>로 요약해드립니다.
        </div>
    </div>

    <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;padding:1.2rem 1.4rem;border-left:3px solid #2B3D5C;">
        <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#2B3D5C;margin-bottom:0.5rem;">02 · 4개 역량 차원 분석</div>
        <div style="font-size:0.82rem;color:#3D3830;line-height:1.7;">
            <b>인지능력 · 잡 전문성 · 적극성 · 리더십</b>을 100점 만점으로 점수화하고 근거를 제시합니다.
        </div>
    </div>

    <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;padding:1.2rem 1.4rem;border-left:3px solid #B8924A;">
        <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#B8924A;margin-bottom:0.5rem;">03 · 채용 키워드 TOP 3</div>
        <div style="font-size:0.82rem;color:#3D3830;line-height:1.7;">
            STAR 행동사건 면접법 기반의 <b>구체적 질문과 평가 포인트</b>를 순위별로 제공합니다.
        </div>
    </div>

    <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;padding:1.2rem 1.4rem;border-left:3px solid #8B2635;">
        <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#8B2635;margin-bottom:0.5rem;">04 · Derailer 위험 요인</div>
        <div style="font-size:0.82rem;color:#3D3830;line-height:1.7;">
            Hogan Assessment 기반으로 <b>스트레스 상황에서 나타날 수 있는 부정적 행동 패턴</b>을 사전 식별합니다.
        </div>
    </div>

    <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;padding:1.2rem 1.4rem;border-left:3px solid #2D6A4F;">
        <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#2D6A4F;margin-bottom:0.5rem;">05 · 성과 극대화 조건</div>
        <div style="font-size:0.82rem;color:#3D3830;line-height:1.7;">
            이 인재가 <b>최고 성과를 낼 수 있는 환경·관리 방식·개발 과제</b>를 제시합니다.
        </div>
    </div>

    <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;padding:1.2rem 1.4rem;border-left:3px solid #2B3D5C;">
        <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#2B3D5C;margin-bottom:0.5rem;">06 · 종합 채용 권고</div>
        <div style="font-size:0.82rem;color:#3D3830;line-height:1.7;">
            McKinsey·Korn Ferry 수준의 <b>임원 평가 리포트 언어</b>로 최종 채용 의사결정을 위한 권고를 제공합니다.
        </div>
    </div>

</div>
<p style="font-size:0.72rem;color:#B0A898;margin-bottom:0;">
    ※ 업로드된 자료가 많을수록 분석 정확도가 높아집니다. 자료가 부족한 항목은 가용 정보를 바탕으로 추론합니다.
</p>
""", unsafe_allow_html=True)

# ── Divider ──
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Run Button ──
run = st.button("◈  분석 시작", use_container_width=True)

if run:
    if not file_data and not candidate_name:
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

                # ── Derailer & Development ──
                st.markdown("""
                <div class="section-header" style="margin-top:2.5rem;">
                    <span class="section-num">05</span>
                    <span class="section-title">리스크 & 개발 제언</span>
                    <div class="section-rule"></div>
                </div>
                """, unsafe_allow_html=True)

                d1, d2 = st.columns(2)
                with d1:
                    st.markdown(f"""
                    <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;
                                padding:1.4rem 1.6rem;height:100%;border-left:3px solid #8B2635;">
                        <div style="font-size:0.65rem;font-weight:700;letter-spacing:3px;
                                    text-transform:uppercase;color:#8B2635;margin-bottom:0.8rem;">
                            ⚠ Derailer · 잠재적 위험 요인
                        </div>
                        <div style="font-size:0.85rem;color:#3D3830;line-height:1.85;">
                            {R.get('derailer','자료 부족으로 분석 불가')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with d2:
                    st.markdown(f"""
                    <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;
                                padding:1.4rem 1.6rem;height:100%;border-left:3px solid #2D6A4F;">
                        <div style="font-size:0.65rem;font-weight:700;letter-spacing:3px;
                                    text-transform:uppercase;color:#2D6A4F;margin-bottom:0.8rem;">
                            ◆ Development · 성과 극대화 조건
                        </div>
                        <div style="font-size:0.85rem;color:#3D3830;line-height:1.85;">
                            {R.get('development_suggestion','자료 부족으로 분석 불가')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # ── Overall Insight ──
                st.markdown("""
                <div class="section-header" style="margin-top:2.5rem;">
                    <span class="section-num">06</span>
                    <span class="section-title">종합 인사이트 & 채용 권고</span>
                    <div class="section-rule"></div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="insight-box">
                    <div class="insight-label">◈ Executive Assessment Summary</div>
                    <div class="insight-text">{R.get('overall_insight','')}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div style="text-align:center;padding:2.5rem 0 1rem;font-size:0.65rem;
                     letter-spacing:3px;text-transform:uppercase;color:#B0A898;">
                    Assessment Complete &nbsp;·&nbsp; M.I.Tech Talent Intelligence &nbsp;·&nbsp; Confidential
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
