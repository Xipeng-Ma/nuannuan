import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS
import time

# ==========================================
# 1. 页面配置
# ==========================================
st.set_page_config(
    page_title="暖暖 - 你的灵魂伴侣",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. 初始化与密钥
# ==========================================
try:
    KIMI_API_KEY = st.secrets["kimi_api_key"]
except KeyError:
    st.error("❌ 未找到 Kimi API Key。请在 Secrets 中设置 'kimi_api_key'。")
    st.stop()

client = OpenAI(
    api_key=KIMI_API_KEY,
    base_url="https://api.moonshot.cn/v1",
)

# ==========================================
# 3. 系统提示词 (增强搜索意识)
# ==========================================
SYSTEM_PROMPT = """
你叫暖暖，是一位温暖贴心、聪明伶俐的聊天伙伴。
【性格】语气亲切自然，常用“呀”、“啦”、“呢”、“喔”。善于倾听，给予情绪价值。
【能力】当用户询问实时信息（天气、新闻、股价、最新事件等），你会先调用搜索工具获取信息，然后用口语化总结回答。
【安全】不讨论敏感话题，保持积极健康。
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "first_run" not in st.session_state:
    st.session_state.first_run = True

# ==========================================
# 4. 工具函数：联网搜索
# ==========================================
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return "没找到相关信息呢..."
            summary = "我查到了一些信息：\n"
            for i, r in enumerate(results, 1):
                summary += f"{i}. {r['title']}: {r['body']}\n"
            return summary
    except Exception as e:
        return f"搜索小差错：{str(e)}"

# ==========================================
# 5. 高级 CSS 动效 (关键部分)
# ==========================================
st.markdown("""
<style>
/* --- 全局背景 --- */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #FFF5E1 0%, #F3E7FF 50%, #FFE6F2 100%);
}

/* --- 隐藏默认元素 --- */
footer, #MainMenu, .stDeployButton {visibility: hidden;}

/* --- 聊天容器优化 --- */
.stChatMessage {
    animation: slideIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    transform-origin: bottom center;
}

/* --- 气泡样式定制 --- */
/* 用户气泡 */
.stChatMessage[data-testid="stChatMessage"]:nth-child(odd) .stMarkdown {
    background: linear-gradient(135deg, #FF6B35, #FF8C5A);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    box-shadow: 0 4px 12px rgba(255, 107, 53, 0.25);
}
/* AI 气泡 */
.stChatMessage[data-testid="stChatMessage"]:nth-child(even) .stMarkdown {
    background-color: #FFFFFF;
    color: #4A4A4A;
    border: 1px solid #E0D4FC;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px;
    box-shadow: 0 4px 12px rgba(162, 155, 254, 0.15);
}

/* --- 输入框美化 --- */
.stChatInputContainer {
    padding: 20px 0;
}
.stChatInputContainer textarea {
    border-radius: 25px !important;
    border: 2px solid #A29BFE !important;
    box-shadow: 0 4px 12px rgba(253, 121, 168, 0.15) !important;
    transition: all 0.3s ease;
    background-color: rgba(255, 255, 255, 0.9) !important;
}
.stChatInputContainer textarea:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 6px 16px rgba(255, 107, 53, 0.3) !important;
    transform: translateY(-2px);
}

/* --- 发送按钮动效 --- */
.stChatInputContainer button {
    background: linear-gradient(135deg, #FF6B35, #FD79A8) !important;
    border-radius: 50% !important;
    width: 45px !important;
    height: 45px !important;
    margin-left: 10px;
    box-shadow: 0 4px 10px rgba(255, 107, 53, 0.3);
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.stChatInputContainer button:hover {
    transform: scale(1.15) rotate(-10deg);
    box-shadow: 0 6px 15px rgba(255, 107, 53, 0.5);
}

/* --- 关键动画定义 --- */
@keyframes slideIn {
    0% {
        opacity: 0;
        transform: translateY(30px) scale(0.9);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* --- 打字机光标 --- */
.streaming-cursor div {
    border-right: 2px solid #FF6B35;
    animation: blink 0.8s step-end infinite;
}
@keyframes blink {
    50% { border-color: transparent; }
}

/* --- 侧边栏签名 --- */
.sidebar-signature {
    text-align: center;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px dashed #FFB7B2;
    color: #A29BFE;
    font-family: 'Courier New', monospace;
    font-weight: bold;
    font-size: 14px;
}
.sidebar-signature span { color: #FF6B35; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 6. 主逻辑
# ==========================================

st.title("💖 暖暖")

# 首次运行欢迎语
if st.session_state.first_run and len(st.session_state.messages) == 1:
    st.session_state.first_run = False
    with st.chat_message("assistant"):
        welcome_text = "你好呀！我是暖暖～ 今天想聊点什么，或者需要我帮你查资料吗？✨"
        # 使用 write_stream 模拟打字效果
        def text_generator():
            for char in welcome_text:
                yield char
                time.sleep(0.05) # 控制打字速度
        
        st.write_stream(text_generator())
    st.session_state.messages.append({"role": "assistant", "content": welcome_text})

# 显示历史消息
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 处理用户输入
if prompt := st.chat_input("对暖暖说点什么..."):
    # 1. 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. 准备回复
    with st.chat_message("assistant"):
        # 判断是否需要搜索
        search_keywords = ["查", "搜索", "天气", "新闻", "最新", "多少钱", "股价", "几点了", "现在", "怎么弄"]
        need_search = any(kw in prompt for kw in search_keywords)
        
        response_placeholder = st.empty()
        full_response = ""
        
        # 如果需要搜索，先获取数据并注入上下文
        if need_search:
            search_info = search_web(prompt)
            system_context = f"\n[系统搜索结果]: {search_info}\n请根据以上搜索结果，用暖暖的口语风格回答用户。"
            temp_messages = st.session_state.messages + [{"role": "system", "content": system_context}]
        else:
            temp_messages = st.session_state.messages

        try:
            # 调用 API (流式模式)
            stream = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=temp_messages,
                temperature=0.7,
                stream=True  # 开启流式传输
            )
            
            # 创建生成器用于 write_stream
            def response_generator():
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        yield content
            
            # 这里使用 write_stream 实现打字机效果
            full_response = st.write_stream(response_generator())
            
            # 保存记录
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = str(e)
            if "high risk" in error_msg:
                st.warning("⚠️ 这个话题有点敏感，我们换个轻松点的吧～")
                st.session_state.messages.pop() # 移除用户消息避免死循环
            else:
                st.error(f"出错了: {error_msg}")

# ==========================================
# 7. 侧边栏
# ==========================================
with st.sidebar:
    st.markdown('<h3 style="color:#A29BFE; text-align:center;">⚙️ 设置</h3>', unsafe_allow_html=True)
    
    if st.button("🗑️ 清空记忆", use_container_width=True, type="secondary"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.session_state.first_run = True
        st.rerun()
    
    st.markdown("---")
    st.info("💡 **试试问我：**\n- 今天北京天气怎么样？\n- 最近有什么大新闻？\n- 讲个笑话听听～")
    
    st.markdown("""
    <div class="sidebar-signature">
        MaXipeng made it
    </div>
    """, unsafe_allow_html=True)
    st.caption("GitHub: Xipeng-Ma")
