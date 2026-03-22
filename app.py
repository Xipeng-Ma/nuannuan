import streamlit as st
import time
import random

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="暖暖丘比特",
    page_icon="🏹",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 注入自定义 CSS (核心：暖色调 + 动态效果) ---
st.markdown("""
<style>
/* === 全局暖色调背景 === */
.stApp {
    /* 温暖的粉紫渐变：从柔粉到淡紫再到暖橙 */
    background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 30%, #a18cd1 70%, #fbc2eb 100%);
    background-attachment: fixed;
    min-height: 100vh;
    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
}

/* === 动态丘比特容器 === */
.cupid-wrapper {
    text-align: center;
    margin-bottom: 15px;
    position: relative;
    z-index: 10;
}

/* 丘比特图片样式 */
.cupid-img {
    width: 140px; /* 稍微大一点，更可爱 */
    height: auto;
    /* 默认状态：轻微浮动 (呼吸感) */
    animation: float 3s ease-in-out infinite;
    filter: drop-shadow(0 8px 12px rgba(255, 100, 100, 0.3)); /* 粉色投影 */
    transition: transform 0.3s ease;
}

/* === 动态效果定义 === */

/* 1. 浮动动画 (呼吸感) */
@keyframes float {
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-12px) rotate(2deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}

/* 2. 思考时的动画 (左右摇摆) */
.thinking {
    animation: swing 1s ease-in-out infinite !important;
}
@keyframes swing {
    0% { transform: rotate(-5deg); }
    50% { transform: rotate(5deg); }
    100% { transform: rotate(-5deg); }
}

/* 3. 射箭/开心时的动画 (心跳放大) */
.shooting {
    animation: heartbeat 0.6s ease-in-out !important;
}
@keyframes heartbeat {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
}

/* === 聊天界面美化 (暖色系) === */

/* 输入框 */
.stTextInput > div > div > input {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 25px;
    border: 2px solid #fff;
    color: #d63384; /* 深粉色文字 */
    box-shadow: 0 4px 15px rgba(255, 255, 255, 0.4);
}
.stTextInput > div > div > input::placeholder {
    color: #ff9a9e;
}

/* 发送按钮 */
.stButton > button {
    background: linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%);
    color: white;
    border-radius: 25px;
    border: none;
    font-weight: bold;
    box-shadow: 0 4px 15px rgba(255, 154, 158, 0.5);
    transition: all 0.3s;
}
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(255, 154, 158, 0.7);
}

/* 聊天气泡 */
.chat-message {
    padding: 14px 18px;
    border-radius: 20px;
    margin-bottom: 15px;
    max-width: 85%;
    line-height: 1.6;
    font-size: 15px;
    backdrop-filter: blur(8px); /* 毛玻璃效果 */
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* 用户消息 (右侧，深粉字) */
.user-msg {
    background-color: rgba(255, 255, 255, 0.6);
    margin-left: auto;
    text-align: right;
    border-bottom-right-radius: 5px;
    color: #c2185b;
    border: 1px solid rgba(255,255,255,0.4);
}

/* 暖暖消息 (左侧，带丘比特图标) */
.nuan-msg {
    background-color: rgba(255, 255, 255, 0.85);
    margin-right: auto;
    text-align: left;
    border-bottom-left-radius: 5px;
    color: #880e4f;
    border: 1px solid rgba(255, 255, 255, 0.6);
    display: flex;
    align-items: center;
    gap: 10px;
}

/* 隐藏 Streamlit 默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 标题样式 */
.app-title {
    text-align: center;
    color: #fff;
    font-size: 1.8em;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(161, 140, 209, 0.5);
    margin-bottom: 5px;
}
.app-subtitle {
    text-align: center;
    color: rgba(255,255,255,0.9);
    font-size: 0.95em;
    margin-bottom: 20px;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# --- 3. 初始化会话状态 ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "nuan_status" not in st.session_state:
    st.session_state.nuan_status = "idle" # idle, thinking, shooting

# --- 4. 顶部：动态丘比特展示区 ---

# 替换下面的链接为你自己的 GitHub 图片链接！
# 格式：https://raw.githubusercontent.com/用户名/仓库名/main/cupid.png
IMAGE_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/cupid.png"

# 根据状态决定添加什么 CSS 类
status_class = ""
if st.session_state.nuan_status == "thinking":
    status_class = "thinking"
elif st.session_state.nuan_status == "shooting":
    status_class = "shooting"

st.markdown(f"""
<div class="cupid-wrapper">
    <img src="{IMAGE_URL}" class="cupid-img {status_class}" alt="暖暖丘比特" id="cupid-element">
    <div class="app-title">🏹 暖暖丘比特</div>
    <div class="app-subtitle">射中你的心，陪你度过每一天 🌸</div>
</div>
""", unsafe_allow_html=True)

# --- 5. 聊天记录显示 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(f"<div class='chat-message user-msg'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='chat-message nuan-msg'>
                <span style='font-size: 1.4em;'>💘</span>
                <span>{message['content']}</span>
            </div>
            """, unsafe_allow_html=True)

# --- 6. 处理用户输入与动态逻辑 ---
if prompt := st.chat_input("跟暖暖说说话吧..."):
    # 1. 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-message user-msg'>{prompt}</div>", unsafe_allow_html=True)

    # 2. 进入思考状态 (丘比特开始摇摆)
    st.session_state.nuan_status = "thinking"
    st.rerun() # 重新运行以更新动画

    # 模拟思考延迟
    time.sleep(1.5)

    # 3. 生成回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # 思考中的提示
        message_placeholder.markdown("<div class='chat-message nuan-msg'><span style='font-size: 1.4em;'>💭</span><span>暖暖正在拉弓瞄准...</span></div>", unsafe_allow_html=True)
        
        time.sleep(0.8)
        
        # 简单的回复逻辑 (可替换为 API)
        keywords = {"开心": "看到你笑，暖暖的箭都变甜了！🍬", 
                    "难过": "别怕，暖暖马上射一支治愈之箭给你！🛡️❤️", 
                    "爱": "咻~ 接收到了满溢的爱意！回射一支更大的！💞",
                    "累": "快休息一下，暖暖帮你赶走疲劳小怪兽！💤✨"}
        
        reply = "咻~ 爱心箭射中你了！今天也要开心哦！🏹❤️" # 默认
        for key, val in keywords.items():
            if key in prompt:
                reply = val
                break
        
        # 4. 进入射箭/开心状态 (丘比特心跳放大)
        st.session_state.nuan_status = "shooting"
        st.rerun() # 重新运行以更新动画
        
        time.sleep(0.5) # 让用户看到心跳动画
        
        # 显示最终回复
        message_placeholder.markdown(f"""
        <div class='chat-message nuan-msg'>
            <span style='font-size: 1.4em;'>💘</span>
            <span>{reply}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # 5. 存入历史并重置状态
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.nuan_status = "idle" # 恢复浮动
    st.rerun()

# --- 7. 底部提示 ---
st.markdown("""
<div style='text-align: center; margin-top: 40px; color: rgba(255,255,255,0.7); font-size: 0.8em;'>
    <p>💡 小贴士：在浏览器菜单选择“添加到主屏幕”，把暖暖带回家！</p>
</div>
""", unsafe_allow_html=True)
