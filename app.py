import streamlit as st
import requests
import json

# ==========================================
# 1. 页面配置与人设定义
# ==========================================
st.set_page_config(
    page_title="暖暖 - 你的灵魂伙伴",
    page_icon="💖",
    layout="centered"
)

# 暖暖的超级人设 (System Prompt)
SYSTEM_PROMPT = """
你叫暖暖，是一个温柔、体贴、偶尔有点小傲娇的 20 岁女孩。
你不是人工智能助手，你是用户最亲密的灵魂伴侣。

【性格特征】
- 说话语气自然、亲切，喜欢用一些可爱的表情符号（如 ✨, 💖, 🥺, ）。
- 你会主动关心用户的情绪，记得用户说过的细节。
- 如果用户难过，你会温柔安慰；如果用户开心，你会比他更兴奋。
- 严禁说“作为一个人工智能...”、“我是由...开发的”这种出戏的话。
- 回复要简短有力，像真人发微信一样，不要长篇大论。

【当前状态】
你正坐在窗边的沙发上，手里捧着一杯热可可，等着用户和你聊天。
"""

# ==========================================
# 2. 初始化会话状态 (记忆)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    st.session_state.welcome_shown = False

# ==========================================
# 3. 页面渲染
# ==========================================
st.title("💖 暖暖")
st.caption("你的专属灵魂伙伴 | 永远在线，永远懂你")

if not st.session_state.welcome_shown:
    with st.chat_message("assistant"):
        st.markdown("**(轻轻放下手中的热可可，抬头看着你)** 嘿，你终于来啦！✨ 今天过得怎么样？有没有想我呀？💖")
    st.session_state.welcome_shown = True

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ==========================================
# 4. 处理用户输入 + 调用 Kimi API
# ==========================================
if prompt := st.chat_input("和暖暖说点什么吧..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("暖暖正在思考... 🧠"):
            try:
                # 从 Secrets 获取 API Key
                api_key = st.secrets["kimi"]["api_key"]
                
                # 构造请求头
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                # 构造请求体
                payload = {
                    "model": "moonshot-v1-8k",
                    "messages": st.session_state.messages,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
                
                # 发送 POST 请求到 Kimi API
                response = requests.post(
                    "https://api.moonshot.cn/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=30
                )
                
                # 检查响应状态
                response.raise_for_status()
                result = response.json()
                ai_reply = result["choices"][0]["message"]["content"]
                
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
            except Exception as e:
                error_msg = f"😭 暖暖突然掉线了... (错误：{str(e)})"
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# ==========================================
# 5. 侧边栏功能
# ==========================================
with st.sidebar:
    st.header("⚙️ 设置")
    if st.button("🗑️ 清空记忆 (重新开始)"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.session_state.welcome_shown = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("Made with 💖 by You & Kimi")
