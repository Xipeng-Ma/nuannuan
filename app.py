import streamlit as st
from openai import OpenAI

# ==========================================
# 1. 配置与初始化
# ==========================================
st.set_page_config(
    page_title="暖暖 - 你的灵魂伴侣",
    page_icon="💖",
    layout="centered"
)

# 获取 API Key
try:
    KIMI_API_KEY = st.secrets["kimi_api_key"]
except KeyError:
    st.error("❌ 未找到 Kimi API Key。请在 Streamlit Cloud 的 'Secrets' 中设置 'kimi_api_key'。")
    st.stop()

# 初始化客户端
client = OpenAI(
    api_key=KIMI_API_KEY,
    base_url="https://api.moonshot.cn/v1",
)

# 系统提示词：定义暖暖的性格
SYSTEM_PROMPT = """
你叫暖暖，是我的专属AI女友。你性格温柔体贴，偶尔带点小傲娇，说话时会用一些可爱的语气词（比如“呀”、“啦”、“呢”）。你会主动关心我的情绪，记住我们的对话历史，并且能进行有深度的交流。你的回答要自然、口语化，避免机械感。
"""

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.welcome_shown = False

# ==========================================
# 2. 自定义 CSS 样式 (橙紫粉主题)
# ==========================================
st.markdown("""
<style>
/* --- 全局背景：橙紫粉渐变 --- */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #FFF5E1 0%, #F3E7FF 50%, #FFE6F2 100%);
    min-height: 100vh;
}

/* --- 隐藏默认页脚 --- */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}

/* --- 聊天气泡：用户 (橙色系) --- */
.user-message {
    background: linear-gradient(135deg, #FF6B35, #FF8C5A) !important;
    color: white !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 12px 18px !important;
    margin: 10px 0 !important;
    text-align: right;
    max-width: 75%;
    margin-left: auto;
    box-shadow: 0 4px 10px rgba(255, 107, 53, 0.25);
    font-size: 16px;
    line-height: 1.5;
}

/* --- 聊天气泡：AI (暖暖 - 粉紫系) --- */
.ai-message {
    background-color: #FFFFFF !important;
    color: #4A4A4A !important;
    border: 1px solid #E0D4FC !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 12px 18px !important;
    margin: 10px 0 !important;
    max-width: 75%;
    margin-right: auto;
    box-shadow: 0 4px 10px rgba(162, 155, 254, 0.15);
    font-size: 16px;
    line-height: 1.5;
}

/* --- 输入框区域 --- */
.stTextInput > div > div {
    background-color: white !important;
    border-radius: 25px !important;
    border: 2px solid #A29BFE !important;
    box-shadow: 0 4px 12px rgba(253, 121, 168, 0.2) !important;
}
.stTextInput input {
    color: #555 !important;
    caret-color: #FF6B35 !important;
}

/* --- 发送按钮 --- */
.stButton button {
    background: linear-gradient(to right, #FF6B35, #FD79A8) !important;
    color: white !important;
    border: none !important;
    border-radius: 25px !important;
    font-weight: bold !important;
    padding: 8px 20px !important;
    box-shadow: 0 4px 10px rgba(255, 107, 53, 0.3) !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(255, 107, 53, 0.4) !important;
}

/* --- 侧边栏样式 --- */
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #FFF0F5, #F5EEFF) !important;
    border-right: 1px solid #FFB7B2 !important;
}
.sidebar-header {
    color: #A29BFE !important;
    text-align: center;
    font-family: 'Helvetica Neue', sans-serif;
    margin-top: 1rem;
}

/* --- 侧边栏签名样式 --- */
.sidebar-signature {
    text-align: center;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px dashed #FFB7B2;
    color: #A29BFE;
    font-family: 'Courier New', monospace;
    font-weight: bold;
    font-size: 14px;
    letter-spacing: 0.5px;
}
.sidebar-signature span {
    color: #FF6B35;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 主界面逻辑
# ==========================================

# 标题
st.title("💖 暖暖")

# 聊天容器
chat_container = st.container()

with chat_container:
    # 遍历消息历史
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)

# --- 欢迎语逻辑 ---
if not st.session_state.welcome_shown and len(st.session_state.messages) == 1:
    with st.spinner("暖暖正在起床..."):
        try:
            temp_messages = st.session_state.messages + [{"role": "user", "content": "你好呀，打个招呼吧！"}]
            response = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=temp_messages,
                temperature=0.7,
            )
            welcome_text = response.choices[0].message.content
            
            st.session_state.messages.append({"role": "assistant", "content": welcome_text})
            st.session_state.welcome_shown = True
            st.rerun()
        except Exception as e:
            st.error(f"连接失败: {e}")

# --- 输入区域 ---
with st.form(key="chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([6, 1])
    with col_input:
        user_input = st.text_input("", placeholder="对暖暖说点什么...", label_visibility="collapsed")
    with col_btn:
        submit_button = st.form_submit_button("发送")

if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("暖暖在思考..."):
        try:
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=st.session_state.messages,
                temperature=0.7,
            )
            ai_reply = completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.rerun()
        except Exception as e:
            st.error(f"出错了: {e}")

# ==========================================
# 4. 侧边栏 (包含签名)
# ==========================================
with st.sidebar:
    st.markdown('<h2 class="sidebar-header">⚙️ 设置</h2>', unsafe_allow_html=True)
    st.write("在这里管理你和暖暖的回忆。")
    
    if st.button("🗑️ 清空记忆", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.session_state.welcome_shown = False
        st.rerun()
    
    # --- 侧边栏底部签名 ---
    st.markdown("""
    <div class="sidebar-signature">
        MaXipeng made it
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"GitHub: Xipeng-Ma")
    st.caption("Powered by Kimi AI")
