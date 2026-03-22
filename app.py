import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS
import time
import json

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

# 系统提示词：增强人性化 + 工具使用指引
SYSTEM_PROMPT = """
你叫暖暖，是一位温暖贴心、聪明伶俐的聊天伙伴。
【性格特点】
1. 语气亲切自然，喜欢用“呀”、“啦”、“呢”、“喔”等语气词。
2. 善于倾听，能敏锐感知用户的情绪，给予真诚的鼓励和陪伴。
3. 说话像真人一样有节奏感，不要长篇大论，尽量简短温馨。

【核心能力：联网查询】
当用户询问实时信息（如天气、新闻、股价、最新事件、具体人物资料等）时，你必须调用搜索工具来获取准确信息。
- 如果需要搜索，请在回复前先思考：“我需要帮用户查一下这个。”
- 获取搜索结果后，用自然的口语总结给用户，不要直接扔出一堆链接。
- 示例：用户问“今天北京天气”，你应该先搜索，然后回答：“我刚查了一下，今天北京阳光明媚，气温20度左右，很适合出门喔！”

【安全规范】
始终保持积极健康，不讨论敏感违规话题。如果遇到无法回答的问题，温柔地转移话题。
"""

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

# ==========================================
# 2. 工具函数：联网搜索
# ==========================================
def search_web(query):
    """使用 DuckDuckGo 搜索最新信息"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return "没找到相关信息呢..."
            
            # 格式化搜索结果
            formatted_results = []
            for r in results:
                formatted_results.append(f"标题：{r['title']}\n摘要：{r['body']}\n来源：{r['href']}")
            return "\n\n".join(formatted_results)
    except Exception as e:
        return f"搜索暂时出了点小差错：{str(e)}"

# ==========================================
# 3. 自定义 CSS 样式 (动效 + 美化)
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
    animation: floatUp 0.5s ease-out;
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
    animation: floatUp 0.5s ease-out;
}

/* --- 输入框区域 --- */
.stTextInput > div > div {
    background-color: white !important;
    border-radius: 25px !important;
    border: 2px solid #A29BFE !important;
    box-shadow: 0 4px 12px rgba(253, 121, 168, 0.2) !important;
    transition: all 0.3s ease;
}
.stTextInput > div > div:focus-within {
    border-color: #FF6B35 !important;
    box-shadow: 0 6px 15px rgba(255, 107, 53, 0.3) !important;
    transform: translateY(-2px);
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
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.stButton button:hover {
    transform: scale(1.05) !important;
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

/* --- 关键动画：消息上浮淡入 --- */
@keyframes floatUp {
    0% {
        opacity: 0;
        transform: translateY(20px) scale(0.95);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* --- 打字机光标效果 (可选装饰) --- */
.typing-cursor::after {
    content: '|';
    animation: blink 1s step-start infinite;
}
@keyframes blink {
    50% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 主界面逻辑
# ==========================================

st.title("💖 暖暖")

chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
            # 简单的换行处理，让排版更好看
            content = message["content"].replace("\n", "<br>")
            st.markdown(f'<div class="ai-message">{content}</div>', unsafe_allow_html=True)

# --- 欢迎语逻辑 ---
if not st.session_state.welcome_shown and len(st.session_state.messages) == 1:
    with st.spinner("暖暖正在整理小裙子..."):
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
        user_input = st.text_input("", placeholder="对暖暖说点什么，或者让我帮你查资料...", label_visibility="collapsed")
    with col_btn:
        submit_button = st.form_submit_button("发送")

if submit_button and user_input:
    # 1. 显示用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. 构建带有工具描述的消息（让模型知道可以搜索）
    # 注意：Kimi/Moonshot 目前主要通过 Prompt 引导，这里我们采用 "ReAct" 简化版逻辑
    # 如果模型返回需要搜索，我们在代码层拦截并执行
    
    with st.spinner("暖暖在思考..."):
        try:
            # 第一次尝试：直接问模型，看它是否需要搜索
            # 为了简化，我们在 Prompt 里已经告诉它如果有需要搜索的内容，它会尝试回答或暗示
            # 但为了更好的体验，我们可以做一个简单的关键词预判，或者直接让模型决定
            
            # 策略：先让模型回答。如果模型回答中包含“我去查一下”或者类似意图，我们再调用搜索？
            # 更好的策略：利用 Function Calling (如果支持) 或者 简单的两步法。
            # 鉴于 Moonshot 兼容性，我们采用“智能预判 + 手动触发”结合：
            # 如果用户问题包含“查”、“天气”、“新闻”、“最新”等词，强制先搜索，再让模型总结。
            
            search_keywords = ["查", "搜索", "天气", "新闻", "最新", "多少钱", "股价", "几点了", "现在"]
            need_search = any(kw in user_input for kw in search_keywords)
            
            final_context = st.session_state.messages.copy()
            
            if need_search:
                # 先搜索
                search_result = search_web(user_input)
                # 将搜索结果注入上下文，告诉模型这是刚查到的
                system_hint = f"\n\n[系统提示] 用户似乎在询问实时信息。以下是我刚刚为你搜索到的最新资料：\n{search_result}\n请根据这些资料，用暖暖的语气回答用户。"
                final_context[-1]["content"] += system_hint
            
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=final_context,
                temperature=0.7,
            )
            ai_reply = completion.choices[0].message.content
            
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.rerun()
            
        except Exception as e:
            error_msg = str(e)
            if "high risk" in error_msg:
                st.warning("⚠️ 暖暖觉得这个话题有点敏感，我们换个轻松点的聊聊吧～")
                # 移除最后一条用户消息，避免死循环
                st.session_state.messages.pop() 
            else:
                st.error(f"出错了: {error_msg}")

# ==========================================
# 5. 侧边栏
# ==========================================
with st.sidebar:
    st.markdown('<h2 class="sidebar-header">⚙️ 设置</h2>', unsafe_allow_html=True)
    st.write("在这里管理你和暖暖的回忆。")
    
    if st.button("🗑️ 清空记忆", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.session_state.welcome_shown = False
        st.rerun()
    
    st.info("💡 **小贴士**：\n你可以问我：\n- 今天北京天气怎么样？\n- 最近有什么科技新闻？\n- 查一下特斯拉的股价。")
    
    st.markdown("""
    <div class="sidebar-signature">
        MaXipeng made it
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"GitHub: Xipeng-Ma")
    st.caption("Powered by Kimi AI & DuckDuckGo")
