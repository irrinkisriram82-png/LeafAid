"""Global CSS that gives LeafAid its dashboard look."""

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] { background: #F6F4EC; }
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 980px; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0F2A21 0%, #17402F 100%); }
[data-testid="stSidebar"] * { color: #E8F3EA; }
[data-testid="stSidebar"] .stButton > button {
  background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.16);
  border-radius: 10px; justify-content: flex-start; transition: all .15s ease;
}
[data-testid="stSidebar"] .stButton > button:hover { background: rgba(255,255,255,.16); border-color: #E9B44C; }
[data-testid="stSidebar"] .stButton > button p { color: inherit; font-size: .9rem; }
[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {
  background: #E9B44C; border-color: #E9B44C; color: #1B2A1B; font-weight: 600; justify-content: center;
}
[data-testid="stSidebar"] .stButton > button:disabled { opacity: .45; }

.la-brand { font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 700; margin-bottom: 14px; color: #fff; }
.la-brand span { color: #E9B44C; }
.la-profile { display: flex; gap: 12px; align-items: center; padding: 12px; border-radius: 14px;
  background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.12); margin-bottom: 18px; }
.la-avatar { width: 40px; height: 40px; flex: none; border-radius: 50%; background: #E9B44C; color: #1B2A1B !important;
  display: flex; align-items: center; justify-content: center; font-weight: 700; }
.la-profile-name { font-weight: 600; font-size: .95rem; }
.la-profile-email { font-size: .75rem; opacity: .75; word-break: break-all; }
.la-label { text-transform: uppercase; letter-spacing: .14em; font-size: .68rem; font-weight: 600; color: #8FB89A !important; margin: 14px 0 8px; }
.la-tip { margin-top: 16px; padding: 12px 14px; border-radius: 12px; font-size: .78rem; line-height: 1.45;
  background: rgba(233,180,76,.12); border: 1px dashed rgba(233,180,76,.55); }

/* ---------- hero + stats ---------- */
.la-hero { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 28px 32px;
  border-radius: 20px; margin-bottom: 16px; color: #fff;
  background: radial-gradient(circle at 88% 15%, #2E7D32 0%, #14352A 62%); box-shadow: 0 8px 24px rgba(20,53,42,.18); }
.la-hero h1.la-title { font-family: 'Fraunces', serif; font-size: 2rem; line-height: 1.15; margin: 4px 0 8px; padding: 0; color: #fff; }
.la-hero p { margin: 0; color: #CFE5D3; max-width: 520px; font-size: .95rem; }
.la-eyebrow { letter-spacing: .18em; font-size: .72rem; font-weight: 600; color: #E9B44C; }
.la-hero-badge { font-size: 3rem; background: rgba(255,255,255,.1); border-radius: 50%;
  width: 84px; height: 84px; flex: none; display: flex; align-items: center; justify-content: center; }

.la-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 18px; }
.la-stat { display: flex; gap: 12px; align-items: center; background: #fff; border: 1px solid #E3E8DC;
  border-radius: 14px; padding: 14px 16px; }
.la-stat-icon { font-size: 1.3rem; background: #E6F3E7; border-radius: 10px; width: 42px; height: 42px;
  display: flex; align-items: center; justify-content: center; }
.la-stat-value { font-family: 'Fraunces', serif; font-size: 1.5rem; font-weight: 700; color: #14352A; line-height: 1; }
.la-stat-label { font-size: .78rem; color: #6B7A6B; margin-top: 3px; }

/* ---------- chat ---------- */
[data-testid="stChatMessage"] { background: #fff; border: 1px solid #E3E8DC; border-radius: 16px;
  padding: 14px 16px; box-shadow: 0 1px 2px rgba(20,53,42,.05); }
[data-testid="stChatInput"] { border-radius: 14px; }

/* ---------- landing ---------- */
.la-landing h1.la-title { font-family: 'Fraunces', serif; font-size: 2.8rem; line-height: 1.1; margin: 8px 0 12px; padding: 0; color: #14352A; }
.la-landing h1.la-title em { color: #2E7D32; }
.la-landing > p { color: #4D5F4D; font-size: 1.02rem; max-width: 460px; }
.la-landing .la-eyebrow { color: #2E7D32; }
.la-features { display: grid; gap: 10px; margin-top: 22px; }
.la-feature { display: flex; gap: 12px; align-items: flex-start; background: #fff; border: 1px solid #E3E8DC; border-radius: 14px; padding: 12px 14px; }
.la-feature-icon { font-size: 1.3rem; background: #E6F3E7; border-radius: 10px; width: 40px; height: 40px; flex: none;
  display: flex; align-items: center; justify-content: center; }
.la-feature b { color: #14352A; font-size: .92rem; }
.la-feature div div { color: #6B7A6B; font-size: .8rem; }
[data-testid="stForm"] { background: #fff; border: 1px solid #E3E8DC; border-radius: 18px; padding: 24px;
  box-shadow: 0 8px 24px rgba(20,53,42,.08); }

@media (max-width: 640px) {
  .la-stats { grid-template-columns: 1fr; }
  .la-hero { flex-direction: column; align-items: flex-start; }
  .la-landing h1.la-title { font-size: 2.1rem; }
}
"""
