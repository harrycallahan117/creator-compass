import streamlit as st
import pandas as pd
import re
import time
from datetime import date
import instaloader
import requests
import os

# --- API Setup ---
OPENROUTER_API_KEY = "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"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- AI Function (FREE TIER) - FIXED ---
@st.cache_data(ttl=600)
def generate_ai_insights(system_prompt, user_prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Creator Compass"
    }
    data = {
        "model": "openrouter/free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1200
    }
    try:
        response = requests.post(OPENROUTER_BASE_URL, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        st.success("✅ AI insights loaded!")
        return content
    except Exception as e:
        error_msg = f"💔 AI temp unavailable: {str(e)[:100]}"
        st.error(error_msg)
        return error_msg

# --- FIXED Pastel CSS - Ultra Soft + Times New Roman for AI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&family=Great+Vibes&family=Satisfy&family=Pacifico&family=Poppins:wght@300;400&family=Times+New+Roman&display=swap');

* { font-feature-settings: "liga" 1, "rlig" 1, "calt" 1; }

body, .main, .reportview-container, .appview-container {
    background: linear-gradient(135deg, #FDF6E3 0%, #F8F1E9 50%, #FFF8F0 100%) !important;
    color: #5F4B44 !important;
    font-family: 'Poppins', 'Segoe UI', sans-serif !important;
    line-height: 1.6 !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Dancing Script', 'Great Vibes', cursive !important;
    color: #8B7D6B !important;
    text-align: center !important;
    text-shadow: 1px 1px 2px rgba(255,248,240,0.6) !important;
    letter-spacing: 0.5px !important;
}

h1 { font-size: 3.5rem; font-weight: 700; margin-bottom: 0.5rem; }
h2 { font-size: 2.5rem; margin-bottom: 1rem; }
h3 { font-size: 2rem; margin-bottom: 1.2rem; }

input, textarea, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background: linear-gradient(145deg, #FFE4E1, #FFF5F5) !important;
    color: #5F4B44 !important;
    border-radius: 15px !important;
    border: 2px solid #F0E68C !important;
    box-shadow: 0 4px 12px rgba(255,248,240,0.4), inset 0 1px 0 rgba(255,255,255,0.9) !important;
    font-family: 'Satisfy', cursive !important;
    font-size: 1.1rem !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
    font-feature-settings: "liga" 0 !important;
}

input:focus, textarea:focus {
    border-color: #E6E6FA !important;
    box-shadow: 0 0 20px rgba(230,230,250,0.4), 0 0 0 3px rgba(255,248,240,0.3) !important;
    transform: translateY(-2px) !important;
}

.stButton > button {
    font-family: 'Pacifico', 'Dancing Script', cursive !important;
    background: linear-gradient(145deg, #FFE4E1, #E6E6FA) !important;
    color: #5F4B44 !important;
    border: none !important;
    border-radius: 20px !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    padding: 14px 28px !important;
    box-shadow: 0 6px 20px rgba(255,248,240,0.4), 0 2px 8px rgba(230,230,250,0.3) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8) !important;
    font-feature-settings: "liga" 1 !important;
    position: relative;
    overflow: hidden;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 35px rgba(230,230,250,0.5) !important;
    background: linear-gradient(145deg, #E6E6FA, #FFE4E1) !important;
}

.stButton > button:active { transform: translateY(-1px) scale(1) !important; }

.idea-card, div[class*="idea-card"] {
    background: linear-gradient(145deg, #FFF5F5, #F8F8FF) !important;
    color: #5F4B44 !important;
    padding: 25px !important;
    margin: 15px auto !important;
    border-radius: 25px !important;
    box-shadow: 0 8px 25px rgba(255,248,240,0.4), inset 0 1px 0 rgba(255,255,255,0.95) !important;
    max-width: 650px !important;
    text-align: left !important;
    font-family: 'Satisfy', cursive !important;
    font-size: 1rem !important;
    border: 2px solid rgba(230,230,250,0.6) !important;
    line-height: 1.6 !important;
    font-feature-settings: "liga" 1 !important;
}

.motivation-card, div[class*="motivation-card"] {
    background: linear-gradient(145deg, #FFF0F5, #F5F5F5) !important;
    font-family: 'Great Vibes', 'Dancing Script', cursive !important;
    font-size: 1.8rem !important;
    color: #8B7D6B !important;
    padding: 35px !important;
    margin: 30px auto !important;
    border-radius: 30px !important;
    box-shadow: 0 15px 45px rgba(230,230,250,0.4) !important;
    max-width: 700px !important;
    text-align: center !important;
    line-height: 1.7 !important;
    text-shadow: 1px 1px 3px rgba(255,255,255,0.95) !important;
    font-feature-settings: "liga" 1 !important;
    border: 3px solid rgba(255,248,240,0.6) !important;
}

.error-card, div[class*="error-card"] {
    background: linear-gradient(145deg, #FFF5F5, #FAF0F0) !important;
    color: #A07D5F !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    border-radius: 15px !important;
    border-left: 6px solid #E6E6FA !important;
    box-shadow: 0 6px 20px rgba(230,230,250,0.3) !important;
    font-family: 'Poppins', sans-serif !important;
    line-height: 1.5 !important;
}

.stTextArea > div > div > textarea {
    font-family: 'Times New Roman', serif !important;
    font-size: 1rem !important;
    line-height: 1.5 !important;
}

.stExpander {
    background: linear-gradient(145deg, #FDF6E3, #F8F1E9) !important;
    border-radius: 20px !important;
    border: 2px solid rgba(230,230,250,0.5) !important;
    margin: 15px 0 !important;
    box-shadow: 0 4px 15px rgba(255,248,240,0.3) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Dancing Script', cursive !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

img.emoji {
    height: 1.2em !important;
    vertical-align: middle !important;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Creator Compass 💖", layout="wide", page_icon="🌸")

# Header
st.markdown("""
<div style='text-align:center; padding: 2rem 0;'>
    <h1 style='font-size: 4rem; margin: 0;'>🌸 Creator Compass 🌸</h1>
    <h3 style='font-size: 2.2rem; margin: 0.5rem 0 1rem 0; color: #8B7D6B;'>For my future beauty icon 💗</h3>
    <div style='font-size: 1.5rem; color: #FFE4E1; font-family: Pacifico, cursive;'>✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨</div>
</div>
""", unsafe_allow_html=True)

# Daily motivation
daily_messages = [
    "You don't have to fix your whole life today. Just get through today",
    "Progress isn't always visible. Sometimes it's just choosing to move forward 💐",
    "“It's okay if your best today looks different than it used to 💎",
    "Resting doesn't mean you're failing. It means you're human 🌷",
    "You're allowed to outgrow the version of you that only survived 🌟",
    "Some days the win is simply not giving up ✨",
    "Healing is rarely loud. Most of it happens quietly 💕",
    "Even if you can't see progress, the fact that you're trying matters 🌺"
]

# --- Reel Inputs ---
st.markdown("<h2 style='font-size: 2.6rem;'>💗 Paste Your Reels</h2>", unsafe_allow_html=True)
reel_links = []
for i in range(5):
    col1, col2 = st.columns([8, 1])
    with col1:
        link = st.text_input(f"Reel {i+1}", key=f"link_{i}",
                            help="instagram.com/reel/ABC123...",
                            placeholder="https://www.instagram.com/reel/...")
    with col2:
        st.markdown("🌸")
    if link.strip():
        reel_links.append(link.strip())

# --- Analyze Button ---
if st.button("🪄 Analyze Trends ✨", use_container_width=True):
    L = instaloader.Instaloader()
   
    try:
        username = st.secrets.get("INSTA_USERNAME", os.getenv("INSTA_USERNAME"))
        password = st.secrets.get("INSTA_PASSWORD", os.getenv("INSTA_PASSWORD"))
        
        if not (username and password):
            st.error("🌹 Add login to `.streamlit/secrets.toml`:")
            st.code('INSTA_USERNAME = "your_username"\nINSTA_PASSWORD = "your_password"', language="toml")
            st.stop()
        
        L.login(username, password)
        st.success(f"🌸 Logged in as @{username} 💕")
    except Exception as e:
        st.markdown(f"<div class='error-card'>💔 Login failed: {str(e)}</div>", unsafe_allow_html=True)
        st.stop()
   
    results = []
    failed_urls = []
   
    @st.cache_data(show_spinner=False)
    def fetch_reel_data(url):
        try:
            if '/reel/' in url:
                shortcode = url.split('/reel/')[1].split('?')[0].split('/')[0]
            elif '/p/' in url:
                shortcode = url.split('/p/')[1].split('?')[0].split('/')[0]
            else:
                return {"error": "Invalid URL"}
            
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            return {
                "caption": (post.caption or "")[:300],
                "likes": post.likes,
                "comments": post.comments,
                "views": getattr(post, 'video_view_count', 0) or 0,
                "shortcode": shortcode,
                "url": url
            }
        except Exception as e:
            return {"error": str(e)[:100]}
   
    with st.spinner(f"🌟 Analyzing {len(reel_links)} reels..."):
        for i, url in enumerate(reel_links):
            st.info(f"💖 Reel {i+1}/{len(reel_links)}")
            data = fetch_reel_data(url)
            if "error" not in data:
                results.append(data)
            else:
                failed_urls.append((url, data["error"]))
            time.sleep(2)
   
    if results:
        df = pd.DataFrame(results)
        df["hashtags"] = df["caption"].apply(lambda c: re.findall(r"#(\w+)", c or ""))
        
        def detect_hook(caption):
            cap = (caption or "").lower()
            if "pov" in cap: return "POV ✨"
            if re.search(r"\b(?:3|5|7|10)\s*(?:ways|tips|steps)", cap): return "Tutorial 📝"
            if any(x in cap for x in ["grwm", "get ready"]): return "GRWM 🌅"
            return "Other 🌸"
        
        df["hook_type"] = df["caption"].apply(detect_hook)
        df["engagement_rate"] = (df["likes"] + df["comments"]) / df["views"].replace(0, 1) * 100
        
        st.session_state.failed_urls = failed_urls
        
        # AI Insights - FULL DISPLAY (Times New Roman) - FIXED
        st.markdown("<h3 style='font-size: 2.1rem;'>🧚 AI Insights 💖</h3>", unsafe_allow_html=True)
        st.info("✨ Loading AI analysis...")
        
        prompt = f"Beauty reels data: {df[['caption','hook_type','likes','views','engagement_rate']].to_dict('records')}\n\nAnalyze trends, what works best, top 3 specific reel ideas + posting schedule tips."
        insights = generate_ai_insights(
            "Instagram beauty reels expert. Analyze performance data, engagement rates, content patterns. Give actionable insights + 3 specific next reel ideas.", 
            prompt
        )
        st.markdown(f'<div class="idea-card"><strong>🎯 Main Analysis:</strong><br>{insights}</div>', unsafe_allow_html=True)
        
        # Hook Types AI Summary - FIXED
        st.markdown("### 🌸 Hook Types Analysis")
        hook_summary_prompt = f"Hook types: {df['hook_type'].value_counts().to_dict()}. Avg engagement by type: {df.groupby('hook_type')['engagement_rate'].mean().round(2).to_dict()}. Analyze for beauty reels."
        hook_insights = generate_ai_insights(
            "Instagram expert. Analyze hook types data (POV, Tutorial, GRWM, Other) for beauty content: what dominates, best performer, 1 optimization tip.", 
            hook_summary_prompt
        )
        st.markdown(f'<div class="idea-card">{hook_insights}</div>', unsafe_allow_html=True)
        
        # 📊 Your Stats 💖
        st.markdown("### 📊 Your Stats 💖")
        display_df = df[["hook_type","likes","comments","views","engagement_rate"]].copy()
        display_df["engagement_rate"] = display_df["engagement_rate"].round(2).astype(str) + "%"
        display_df["caption_preview"] = df["caption"].str[:80] + "..."
        st.table(display_df.style.format({"likes": "{:,.0f}", "views": "{:,.0f}"}))
        
        # Downloads
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("💾 Download Data", df.to_csv(index=False).encode(), "reels.csv")
        with col2:
            if df["hashtags"].str.len().sum() > 0:
                tags_df = pd.DataFrame({"hashtag": [t for tags in df["hashtags"] for t in tags], "count": 1}).groupby("hashtag").sum().sort_values("count", ascending=False)
                st.download_button("🏷️ Top Hashtags", tags_df.to_csv().encode(), "hashtags.csv")
        
        # *** NEW *** Top 3 Specific Reel Ideas - Fixed format, no overflow
        st.markdown("<h3 style='font-size: 1.9rem;'>🌺 Top 3 Specific Reel Ideas</h3>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="idea-card">
        <strong>1. "Before & After: 5-Minute Glow Up" (Hook: Other ✨)</strong><br>
        • <strong>Concept:</strong> Quick makeup/skincare showing dramatic results in 5 min<br>
        • <strong>Why it works:</strong> High-value transformation content<br>
        • <strong>Hashtags:</strong> #glowup #makeuphacks #explore #skincare
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="idea-card">
        <strong>2. "1 Product That Changed My Routine" (Hook: Tutorial 💡)</strong><br>
        • <strong>Concept:</strong> Demo 1 cult-favorite product in action<br>
        • <strong>Why it works:</strong> Immediate value + visual appeal<br>
        • <strong>Hashtags:</strong> #beautytip #skincare #viral #makeup
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="idea-card">
        <strong>3. "GRWM: 3 Mistakes I Stopped Making" (Hook: GRWM 🌅)</strong><br>
        • <strong>Concept:</strong> Show routine + 3 beauty mistakes to avoid<br>
        • <strong>Why it works:</strong> Relatable + educational content<br>
        • <strong>Hashtags:</strong> #GRWM #beautymistakes #makeup #skincare
        </div>
        """, unsafe_allow_html=True)
   
    else:
        st.markdown("<div class='error-card'>🌸 No valid reels. Check links! 💕</div>", unsafe_allow_html=True)

# Quick tips
with st.expander("💗 Quick Tips 🌸"):
    st.markdown("""
    - ✨ Post 3-5x weekly consistently  
    - 🎵 Use trending audio fast
    - ⏱️ Hook in first 3 seconds
    - 🏷️ Mix popular + niche hashtags (10-15)
    - 💬 Reply to all comments ASAP
    - 📱 Best times: 8AM, 12PM, 7PM your timezone
    """)

# Motivation
today_msg = daily_messages[date.today().timetuple().tm_yday % len(daily_messages)]
st.markdown(f'<div class="motivation-card">{today_msg}</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align:center;padding:3rem;color:#8B7D6B;font-family:"Great Vibes",cursive;font-size:1.8rem;border-top:3px solid #FFE4E1;margin-top:3rem;background:linear-gradient(145deg,#FDF6E3,#FFF5F5);border-radius:25px;'>
🌸 Made for my beauty icon 💕 | Feb 2026 ✨</div>
""", unsafe_allow_html=True)
