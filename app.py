import streamlit as st
import anthropic
import base64
import io
import json
import re
from pathlib import Path
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Talent Intelligence · M.I.Tech",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
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
        # 확장자 기반으로 MIME 타입 직접 지정 (uploaded_file.type 신뢰 안 함)
        ext_mime = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".webp": "image/webp",
            ".gif": "image/gif"
        }
        mime = next((v for k, v in ext_mime.items() if name.endswith(k)), "image/jpeg")
        b64 = base64.standard_b64encode(content).decode()
        return f"__IMAGE__{name}__BASE64__{b64}__MIMETYPE__{mime}"
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
                # MIME 타입 유효성 검사
                valid_mimes = ["image/jpeg", "image/png", "image/webp", "image/gif"]
                if mime_type not in valid_mimes:
                    mime_type = "image/jpeg"
                # base64 유효성 간단 체크
                if len(b64_data) < 10:
                    continue
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

━━━━━━━━━━━━━━━━━━━━━━━━
번아웃 위험도 평가 기준 (Maslach Burnout Inventory 모델 기반)
━━━━━━━━━━━━━━━━━━━━━━━━
번아웃 위험도는 아래 3개 축을 종합하여 LOW / MEDIUM / HIGH / CRITICAL 4단계로 평가합니다:
- 정서적 고갈 (Emotional Exhaustion): 에너지 소진, 감정적 탈진 신호
- 비인격화 (Depersonalization): 냉소적 태도, 직무 의미 상실 신호
- 개인 성취감 저하 (Reduced Personal Accomplishment): 무력감, 자기 효능감 하락 신호
근거 자료: SNS 어조, 다면평가 결과, 기안서 문체, MBTI 스트레스 반응 패턴 등을 교차 분석

━━━━━━━━━━━━━━━━━━━━━━━━
이직 가능성 평가 기준 (Push-Pull 모델 기반)
━━━━━━━━━━━━━━━━━━━━━━━━
이직 가능성은 아래 Push(현조직 이탈 요인)와 Pull(외부 유인 요인)을 종합하여 LOW / MEDIUM / HIGH / CRITICAL 4단계로 평가합니다:
- Push 요인: 성장 정체감, 보상 불만족 신호, 관계 갈등, 번아웃 수준
- Pull 요인: 외부 네트워크 활동성, 스킬 시장가치, 업계 이동성
- 재직 의향 신호: 장기 프로젝트 참여도, 조직 애착 언어, 커리어 방향성
근거 자료: 이력서 재직 기간 패턴, SNS 활동, 다면평가 몰입도, 기안서 미래 지향성 등 교차 분석

반드시 아래 JSON 형식으로만 응답하세요. JSON 외 어떤 텍스트도 출력하지 마세요:
{
  "candidate_summary": "대상자 핵심 특성 한줄 평가 (50자 이내)",
  "personality_tags": ["태그1","태그2","태그3","태그4","태그5"],
  "dimensions": {
    "cognitive_ability": {
      "score": 75,
      "grade": "B+",
      "summary": "3문장 분석. 강점 발현 방식·조직 활용 가능성·잠재 한계 포함",
      "evidence": ["근거1","근거2"]
    },
    "job_expertise": {
      "score": 80,
      "grade": "A",
      "summary": "3문장 분석",
      "evidence": ["근거1","근거2"]
    },
    "proactiveness": {
      "score": 70,
      "grade": "B",
      "summary": "3문장 분석",
      "evidence": ["근거1","근거2"]
    },
    "leadership": {
      "score": 65,
      "grade": "B-",
      "summary": "3문장 분석",
      "evidence": ["근거1","근거2"]
    }
  },
  "burnout_risk": {
    "level": "MEDIUM",
    "score": 45,
    "emotional_exhaustion": "2문장",
    "depersonalization": "2문장",
    "personal_accomplishment": "2문장",
    "summary": "2문장 총평 및 관리 권고",
    "evidence": ["근거1","근거2"]
  },
  "turnover_risk": {
    "level": "LOW",
    "score": 25,
    "push_factors": "2문장",
    "pull_factors": "2문장",
    "retention_signals": "2문장",
    "summary": "2문장 총평 및 리텐션 전략",
    "evidence": ["근거1","근거2"]
  },
  "hiring_keywords": [
    {
      "rank": 1,
      "keyword": "10자 이내 키워드",
      "why": "2문장 선정 이유 (인재상 연결)",
      "how_to_check": "STAR 기반 질문 1개 + 평가 포인트"
    },
    {
      "rank": 2,
      "keyword": "10자 이내 키워드",
      "why": "2문장",
      "how_to_check": "STAR 기반 질문 1개 + 평가 포인트"
    },
    {
      "rank": 3,
      "keyword": "10자 이내 키워드",
      "why": "2문장",
      "how_to_check": "STAR 기반 질문 1개 + 평가 포인트"
    }
  ],
  "derailer": "2문장. 스트레스·장기 재직 시 부정적 행동 패턴",
  "development_suggestion": "2문장. 최고 성과를 위한 환경·관리 방식",
  "overall_insight": "4문장. 인재 유형 명명·최적 포지셔닝·채용 최종 권고"
}"""

    user_content = build_user_content(file_data, candidate_name, company_standard)
    if not user_content:
        raise ValueError("분석할 자료가 없습니다.")
    user_content.append({"type": "text", "text": "위 자료를 바탕으로 글로벌 탑티어 HR 컨설팅 펌 수준의 전문 인재 분석을 JSON 형식으로 수행해주세요. 모든 평가는 제공된 자료의 구체적 근거에 기반해야 하며, 표면적 관찰을 넘어 내재된 역량 패턴과 조직 적합도를 심층 분석해주세요."})

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}]
    )
    raw = response.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    # JSON 블록만 추출
    match = re.search(r'\{[\s\S]+\}', raw)
    if match:
        raw = match.group(0)
    # 잘린 JSON 자동 복구: 마지막 완성된 키까지만 살려서 닫기
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # 마지막 완전한 key-value 쌍 이후를 제거하고 닫기 시도
        repaired = raw
        for closing in ['"}', '"]', '}']:
            last = repaired.rfind(closing)
            if last != -1:
                candidate = repaired[:last + len(closing)]
                # 열린 괄호 수에 맞춰 닫기
                opens  = candidate.count('{') - candidate.count('}')
                opens2 = candidate.count('[') - candidate.count(']')
                candidate += ']' * max(0, opens2) + '}' * max(0, opens)
                try:
                    return json.loads(candidate)
                except Exception:
                    continue
        raise


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


# ─── 아카이브 함수 (Supabase 영구 저장 + 로컬 폴백) ─────────────────────────
ARCHIVE_FILE = "archive.json"
SUPABASE_TABLE = "talent_archive"

def _get_supabase():
    """Supabase 연결 정보 반환. 설정 안 됐으면 None."""
    try:
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "")
        if url and key:
            return url.rstrip("/"), key
    except Exception:
        pass
    return None, None

def _sb_headers(key):
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def load_archive() -> list:
    """Supabase → 로컬 파일 순으로 시도"""
    import requests as req
    url, key = _get_supabase()
    if url and key:
        try:
            r = req.get(
                f"{url}/rest/v1/{SUPABASE_TABLE}?order=created_at.desc&limit=200",
                headers=_sb_headers(key), timeout=5
            )
            if r.status_code == 200:
                rows = r.json()
                return [
                    {
                        "id":             row.get("id"),
                        "saved_at":       row.get("saved_at", ""),
                        "candidate_name": row.get("candidate_name", ""),
                        "dept":           row.get("dept", ""),
                        "result":         json.loads(row.get("result_json", "{}"))
                    }
                    for row in rows
                ]
        except Exception:
            pass

    # 로컬 폴백
    try:
        if Path(ARCHIVE_FILE).exists():
            with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []

def save_to_archive(record: dict):
    """Supabase → 로컬 파일 순으로 저장"""
    import requests as req
    url, key = _get_supabase()
    if url and key:
        try:
            payload = {
                "saved_at":       record.get("saved_at", ""),
                "candidate_name": record.get("candidate_name", ""),
                "dept":           record.get("dept", ""),
                "result_json":    json.dumps(record.get("result", {}), ensure_ascii=False)
            }
            r = req.post(
                f"{url}/rest/v1/{SUPABASE_TABLE}",
                headers=_sb_headers(key),
                json=payload, timeout=5
            )
            if r.status_code in (200, 201):
                return  # Supabase 저장 성공
        except Exception:
            pass

    # 로컬 폴백
    archive = load_archive()
    archive.insert(0, record)
    with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(archive, f, ensure_ascii=False, indent=2)

def delete_from_archive(record_id, idx: int):
    """Supabase row id로 삭제 → 없으면 로컬 인덱스 삭제"""
    import requests as req
    url, key = _get_supabase()
    if url and key and record_id:
        try:
            req.delete(
                f"{url}/rest/v1/{SUPABASE_TABLE}?id=eq.{record_id}",
                headers=_sb_headers(key), timeout=5
            )
            return
        except Exception:
            pass

    # 로컬 폴백
    archive = load_archive()
    if 0 <= idx < len(archive):
        archive.pop(idx)
    with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(archive, f, ensure_ascii=False, indent=2)


# ─── 결과 렌더링 함수 (신규 분석 & 아카이브 조회 공용) ──────────────────────
def render_result(R: dict, candidate_name: str):
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

    # ── 역량 차원 ──
    st.markdown("""
    <div class="section-header">
        <span class="section-num">04</span>
        <span class="section-title">역량 차원 분석</span>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    dims = R.get("dimensions", {})
    d_col1, d_col2 = st.columns(2)
    for idx, (key, info) in enumerate(dims.items()):
        score  = info.get("score", 0)
        grade  = info.get("grade", "-")
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

    # ── 채용 키워드 ──
    st.markdown("""
    <div class="section-header" style="margin-top:2.5rem;">
        <span class="section-num">05</span>
        <span class="section-title">채용 핵심 키워드 Top 3</span>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    rank_cls = ["rank-gold","rank-silver","rank-bronze"]
    rank_lbl = ["1st","2nd","3rd"]
    for kw in R.get("hiring_keywords", []):
        r  = kw.get("rank", 1) - 1
        rc = rank_cls[r] if r < 3 else "rank-bronze"
        rl = rank_lbl[r] if r < 3 else f"{r+1}th"
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

    # ── 번아웃 & 이직 가능성 ──
    st.markdown("""
    <div class="section-header" style="margin-top:2.5rem;">
        <span class="section-num">06</span>
        <span class="section-title">번아웃 위험도 & 이직 가능성</span>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    burnout  = R.get("burnout_risk", {})
    turnover = R.get("turnover_risk", {})

    def risk_color(level):
        return {"LOW":"#2D6A4F","MEDIUM":"#8B6914","HIGH":"#8B2635","CRITICAL":"#5C0011"}.get(level,"#7A7268")
    def risk_label(level):
        return {"LOW":"낮음","MEDIUM":"주의","HIGH":"높음","CRITICAL":"심각"}.get(level, level)
    def risk_bar_color(level):
        return {"LOW":"#2D6A4F","MEDIUM":"#D4AF72","HIGH":"#C0392B","CRITICAL":"#7B0000"}.get(level,"#B0A898")

    b_level  = burnout.get("level","MEDIUM")
    b_score  = burnout.get("score", 50)
    t_level  = turnover.get("level","LOW")
    t_score  = turnover.get("score", 30)

    b_col, t_col = st.columns(2)

    with b_col:
        bcolor = risk_color(b_level)
        st.markdown(f"""
        <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;
                    padding:1.4rem 1.6rem;border-left:3px solid {bcolor};">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.8rem;">
                <div style="font-size:0.65rem;font-weight:700;letter-spacing:3px;
                            text-transform:uppercase;color:{bcolor};">🔥 번아웃 위험도</div>
                <span style="background:{bcolor};color:white;border-radius:4px;
                             padding:0.2rem 0.7rem;font-size:0.7rem;font-weight:700;">
                    {risk_label(b_level)}
                </span>
            </div>
            <div style="background:#E2DDD4;border-radius:999px;height:5px;margin-bottom:1rem;overflow:hidden;">
                <div style="width:{b_score}%;height:100%;background:{risk_bar_color(b_level)};border-radius:999px;"></div>
            </div>
            <div style="font-size:0.8rem;color:#3D3830;line-height:1.75;margin-bottom:0.8rem;">
                {burnout.get('summary','자료 부족으로 분석 불가')}
            </div>
            <div style="border-top:1px solid #E2DDD4;padding-top:0.8rem;">
                <div style="font-size:0.68rem;color:#B0A898;font-weight:600;margin-bottom:0.4rem;letter-spacing:1px;">세부 분석</div>
                <div style="font-size:0.75rem;color:#7A7268;margin-bottom:0.3rem;">
                    <b style="color:#3D3830;">정서적 고갈</b> — {burnout.get('emotional_exhaustion','')}
                </div>
                <div style="font-size:0.75rem;color:#7A7268;margin-bottom:0.3rem;">
                    <b style="color:#3D3830;">비인격화</b> — {burnout.get('depersonalization','')}
                </div>
                <div style="font-size:0.75rem;color:#7A7268;">
                    <b style="color:#3D3830;">성취감</b> — {burnout.get('personal_accomplishment','')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t_col:
        tcolor = risk_color(t_level)
        st.markdown(f"""
        <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;
                    padding:1.4rem 1.6rem;border-left:3px solid {tcolor};">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.8rem;">
                <div style="font-size:0.65rem;font-weight:700;letter-spacing:3px;
                            text-transform:uppercase;color:{tcolor};">🚪 이직 가능성</div>
                <span style="background:{tcolor};color:white;border-radius:4px;
                             padding:0.2rem 0.7rem;font-size:0.7rem;font-weight:700;">
                    {risk_label(t_level)}
                </span>
            </div>
            <div style="background:#E2DDD4;border-radius:999px;height:5px;margin-bottom:1rem;overflow:hidden;">
                <div style="width:{t_score}%;height:100%;background:{risk_bar_color(t_level)};border-radius:999px;"></div>
            </div>
            <div style="font-size:0.8rem;color:#3D3830;line-height:1.75;margin-bottom:0.8rem;">
                {turnover.get('summary','자료 부족으로 분석 불가')}
            </div>
            <div style="border-top:1px solid #E2DDD4;padding-top:0.8rem;">
                <div style="font-size:0.68rem;color:#B0A898;font-weight:600;margin-bottom:0.4rem;letter-spacing:1px;">세부 분석</div>
                <div style="font-size:0.75rem;color:#7A7268;margin-bottom:0.3rem;">
                    <b style="color:#3D3830;">이탈 요인</b> — {turnover.get('push_factors','')}
                </div>
                <div style="font-size:0.75rem;color:#7A7268;margin-bottom:0.3rem;">
                    <b style="color:#3D3830;">외부 유인</b> — {turnover.get('pull_factors','')}
                </div>
                <div style="font-size:0.75rem;color:#7A7268;">
                    <b style="color:#3D3830;">재직 신호</b> — {turnover.get('retention_signals','')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Derailer & Development ──
    st.markdown("""
    <div class="section-header" style="margin-top:2.5rem;">
        <span class="section-num">07</span>
        <span class="section-title">리스크 & 개발 제언</span>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    dd1, dd2 = st.columns(2)
    with dd1:
        st.markdown(f"""
        <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;
                    padding:1.4rem 1.6rem;border-left:3px solid #8B2635;">
            <div style="font-size:0.65rem;font-weight:700;letter-spacing:3px;
                        text-transform:uppercase;color:#8B2635;margin-bottom:0.8rem;">
                ⚠ Derailer · 잠재적 위험 요인
            </div>
            <div style="font-size:0.85rem;color:#3D3830;line-height:1.85;">
                {R.get('derailer','자료 부족으로 분석 불가')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with dd2:
        st.markdown(f"""
        <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;
                    padding:1.4rem 1.6rem;border-left:3px solid #2D6A4F;">
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
        <span class="section-num">08</span>
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


# ─── 사이드바 아카이브 ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1rem;">
        <div style="font-family:'DM Serif Display',serif;font-size:1.2rem;
                    color:#1A1714;font-style:italic;margin-bottom:0.3rem;">
            Archive
        </div>
        <div style="font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;
                    color:#B0A898;">분석 기록 조회</div>
        <div style="height:1px;background:#D4CEC4;margin-top:0.8rem;"></div>
    </div>
    """, unsafe_allow_html=True)

    archive = load_archive()

    if not archive:
        st.markdown('<p style="font-size:0.8rem;color:#B0A898;text-align:center;padding:2rem 0;">저장된 분석 기록이 없습니다.</p>', unsafe_allow_html=True)
    else:
        # 전체 내보내기
        export_json = json.dumps(archive, ensure_ascii=False, indent=2)
        st.download_button(
            label="⬇ 전체 기록 내보내기 (JSON)",
            data=export_json.encode("utf-8"),
            file_name=f"talent_archive_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
        st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

        for i, rec in enumerate(archive):
            name    = rec.get("candidate_name", "이름 없음")
            dept    = rec.get("dept", "")
            saved   = rec.get("saved_at", "")
            rec_id  = rec.get("id", None)
            summary = rec.get("result", {}).get("candidate_summary", "")[:40]
            tags    = rec.get("result", {}).get("personality_tags", [])[:2]

            # 카드 클릭 = 해당 기록 조회
            with st.expander(f"**{name}** · {saved}", expanded=False):
                if dept:
                    st.caption(dept)
                st.markdown(f'<p style="font-size:0.75rem;color:#7A7268;line-height:1.6;">{summary}...</p>',
                            unsafe_allow_html=True)
                for t in tags:
                    st.markdown(f'<span style="display:inline-block;border:1px solid #D4AF72;color:#B8924A;'
                                f'border-radius:3px;padding:1px 7px;font-size:0.68rem;margin:1px;">{t}</span>',
                                unsafe_allow_html=True)
                col_v, col_d = st.columns(2)
                with col_v:
                    if st.button("조회", key=f"view_{i}", use_container_width=True):
                        st.session_state["archive_view"] = i
                        st.session_state["show_archive"] = True
                        st.rerun()
                with col_d:
                    if st.button("삭제", key=f"del_{i}", use_container_width=True):
                        delete_from_archive(rec_id, i)
                        if st.session_state.get("archive_view") == i:
                            st.session_state["show_archive"] = False
                        st.rerun()

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
    value="""1) 성장지향: 목표 의식이 뚜렷하며, 조직과 개인의 동반 성장을 위해 노력하는 분
2) 상호존중: 동료 간의 상호 존중과 팀워크의 가치를 소중히 여기는 분
3) 혁신과 도전: 지속적인 학습과 도전을 통해 끊임없이 혁신을 추구하는 분""",
    height=110
)

core_culture = st.text_area(
    "회사 5대 핵심문화 축",
    value="""1) 개방적 소통 탁월성 (Open communication excellence)
2) 몰입 기반 실행력 (Commitment-driven execution)
3) 성과 기반 인정 체계 (Performance-based recognition)
4) 협업 시너지 (Collaborative synergy)
5) 혁신 리더십 (Innovation leadership)""",
    height=140
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
if core_culture:
    file_data["회사 5대 핵심문화 축"] = core_culture

# ── Section 3: 분석 결과 안내 ──
st.markdown("""
<div class="section-header">
    <span class="section-num">03</span>
    <span class="section-title">분석 결과 안내</span>
    <div class="section-rule"></div>
</div>
""", unsafe_allow_html=True)

guide_items = [
    ("#B8924A", "01 · 대상자 프로필",       "종합 한줄 평가와 함께 대상자의 핵심 성향을 태그로 요약해드립니다."),
    ("#2B3D5C", "02 · 4개 역량 차원 분석",  "인지능력 · 잡 전문성 · 적극성 · 리더십을 100점 만점으로 점수화하고 근거를 제시합니다."),
    ("#B8924A", "03 · 채용 키워드 TOP 3",   "STAR 행동사건 면접법 기반의 구체적 질문과 평가 포인트를 순위별로 제공합니다."),
    ("#8B2635", "04 · Derailer 위험 요인",  "Hogan Assessment 기반으로 스트레스 상황에서 나타날 수 있는 부정적 행동 패턴을 사전 식별합니다."),
    ("#2D6A4F", "05 · 성과 극대화 조건",    "이 인재가 최고 성과를 낼 수 있는 환경·관리 방식·개발 과제를 제시합니다."),
    ("#2B3D5C", "06 · 종합 채용 권고",      "McKinsey·Korn Ferry 수준의 임원 평가 리포트 언어로 최종 채용 의사결정을 위한 권고를 제공합니다."),
]

g_col1, g_col2 = st.columns(2)
for i, (color, title, desc) in enumerate(guide_items):
    with (g_col1 if i % 2 == 0 else g_col2):
        st.markdown(f"""
        <div style="background:white;border:1px solid #D4CEC4;border-radius:8px;
                    padding:1.2rem 1.4rem;border-left:3px solid {color};margin-bottom:0.8rem;">
            <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;
                        text-transform:uppercase;color:{color};margin-bottom:0.5rem;">{title}</div>
            <div style="font-size:0.82rem;color:#3D3830;line-height:1.7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<p style="font-size:0.72rem;color:#B0A898;margin-bottom:0;">※ 업로드된 자료가 많을수록 분석 정확도가 높아집니다. 자료가 부족한 항목은 가용 정보를 바탕으로 추론합니다.</p>', unsafe_allow_html=True)

# ── Divider ──
st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── 아카이브 조회 모드 ──
if st.session_state.get("show_archive"):
    idx = st.session_state.get("archive_view", 0)
    archive_data = load_archive()
    if 0 <= idx < len(archive_data):
        rec = archive_data[idx]
        st.markdown(f"""
        <div style="background:#EDE8E0;border:1px solid #D4CEC4;border-radius:8px;
                    padding:0.8rem 1.2rem;margin-bottom:1.5rem;">
            <span style="font-size:0.8rem;color:#7A7268;">
                🗂 아카이브 조회 중 &nbsp;·&nbsp;
                <b style="color:#1A1714;">{rec.get('candidate_name','')}</b> &nbsp;·&nbsp;
                {rec.get('saved_at','')}
            </span>
        </div>
        """, unsafe_allow_html=True)
        render_result(rec["result"], rec.get("candidate_name",""))
    if st.button("← 새 분석으로 돌아가기", use_container_width=True):
        st.session_state["show_archive"] = False
        st.rerun()

else:
    # ── Run Button ──
    run = st.button("◈  분석 시작", use_container_width=True)

    if run:
        if not file_data and not candidate_name:
            st.error("자료를 최소 1개 이상 업로드하거나 성명을 입력해주세요.")
        else:
            with st.spinner("분석 중 — 업로드된 자료를 종합 검토하고 있습니다..."):
                try:
                    R = analyze_candidate(api_key, file_data, candidate_name, company_standard)

                    # 아카이브 저장
                    record = {
                        "saved_at":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "candidate_name": candidate_name or "이름 없음",
                        "dept":           candidate_dept,
                        "result":         R
                    }
                    save_to_archive(record)
                    st.success("✅ 분석 완료 — 왼쪽 아카이브에 자동 저장되었습니다.")

                    render_result(R, candidate_name)

                except json.JSONDecodeError as e:
                    st.error(f"결과 파싱 오류 — AI 응답을 해석하지 못했습니다. 잠시 후 다시 시도해주세요. (상세: {str(e)[:80]})")
                except anthropic.AuthenticationError:
                    st.error("API Key가 유효하지 않습니다. Streamlit Secrets를 확인해주세요.")
                except anthropic.APIStatusError as e:
                    st.error(f"API 오류 ({e.status_code}): {str(e.message)[:120]}")
                except Exception as e:
                    st.error(f"오류 발생: {e}")

# Footer
st.markdown("""
<div style="text-align:center;padding:3rem 0 1.5rem;font-size:0.65rem;
     letter-spacing:2px;text-transform:uppercase;color:#C8C0B4;border-top:1px solid #E2DDD4;margin-top:3rem;">
    Talent Intelligence Platform &nbsp;·&nbsp; M.I.Tech P&C Team &nbsp;·&nbsp; Powered by Claude AI
</div>
""", unsafe_allow_html=True)
