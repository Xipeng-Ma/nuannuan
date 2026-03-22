import streamlit as st
import time
import random

# ==========================================
# 1. 页面基础配置
# ==========================================
st.set_page_config(
    page_title="暖暖 - 你的情感伙伴",
    page_icon="💖",
    layout="centered"
)

# 自定义 CSS 样式（让气泡更好看）
st.markdown("""
<style>
    /* 隐藏默认的页脚和菜单 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 输入框样式优化 */
    .stChatInputContainer > div {
        background-color: #fff0f5;
        border-radius: 20px;
        padding: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 核心逻辑：暖暖的“大脑” (情感分析 + 回复生成)
# ==========================================
def get_nuan_response(user_text):
    """
    根据用户输入的情绪，生成温暖的回复。
    这里保留了你之前的逻辑核心，并做了一些润色。
    """
    text = user_text.lower()
    
    # --- 情绪关键词检测 ---
    sad_words = ["难过", "伤心", "累", "烦", "哭", "痛苦", "绝望", "孤单", "郁闷", "不开心", "bad", "sad", "tired"]
    happy_words = ["开心", "高兴", "棒", "好", "哈哈", "笑", "幸运", "美丽", "爱", "happy", "good", "love"]
    anxious_words = ["焦虑", "担心", "害怕", "紧张", "迷茫", "怎么办", "压力"]
    
    response = ""
    
    # --- 分支逻辑 ---
    if any(word in text for word in sad_words):
        responses = [
            "（轻轻抱住你）感觉到你现在很难过，没关系，我在呢。不用急着好起来，我会一直陪着你。",
            "抱抱～ 生活有时候确实挺累的。想哭就哭出来吧，我的肩膀借给你靠一会儿。",
            "虽然我不能替你承担痛苦，但我愿意做那个听你倾诉的人。你并不孤单，好吗？",
            "摸摸头。今天发生了什么事让你这么累？如果不介意的话，可以跟我说说。"
        ]
        response = random.choice(responses)
        
    elif any(word in text for word in happy_words):
        responses = [
            "哇！看到你这么开心，我也忍不住跟着笑了！✨ 发生了什么好事呀？",
            "太棒啦！你的笑容就是今天最温暖的阳光！☀️ 继续保持这份好心情哦！",
            "真好～ 感觉周围的空气都变甜了！快跟我分享一下，让我也沾沾喜气！",
            "耶！为你感到高兴！记得把这份快乐存进心里，下次难过的时候拿出来用哦。"
        ]
        response = random.choice(responses)
        
    elif any(word in text for word in anxious_words):
        responses = [
            "深呼吸～ 慢慢来。焦虑的时候，我们试着把大问题拆成小步骤，一步一步走，好吗？",
            "别怕，迷茫是成长的必经之路。无论结果如何，我都支持你的选择。",
            "（递给你一杯热茶🍵）先放松一下。天塌不下来，我们一起想办法。",
            "紧张是正常的，说明你在乎这件事。相信自己，你已经做得很好了。"
        ]
        response = random.choice(responses)
        
    else:
        # 默认闲聊/倾听模式
        default_responses = [
            "嗯嗯，我在听呢。然后呢？",
            "原来是这样呀... 你的想法很有趣，多跟我说说？",
            "（认真点头）我记下来了。这种感觉一定很特别吧？",
            "不管你说什么，我都觉得很有道理。毕竟是你嘛！😉",
            "今天天气不错/心情怎么样？想聊聊任何你想聊的话题。"
        ]
        response = random.choice(default_responses)
    
    return response

# ==========================================
# 3. 界面渲染：气泡聊天室
# ==========================================

# --- 顶部温馨标题区 (替代原来的图片) ---
st.markdown("""
<div style="text-align: center; margin-bottom: 25px; padding: 20px; background: linear-gradient(to bottom, #fff0f5, #ffffff); border-radius: 20px; box-shadow: 0 4px 10px rgba(255, 182, 193, 0.2);">
    <h1 style="color: #ff69b4; margin: 0; font-family: 'Segoe UI', sans-serif;">💖 暖暖</h1>
    <p style="font-size: 1.1em; color: #666; margin-top: 8px;">
        嘿，我是你的专属情感伙伴。<br>
        像老朋友一样，随便聊聊吧～
    </p>
    <div style="font-size: 2.5em; margin-top: 10px; letter-spacing: 10px;">👼 💘 🕊️</div>
</div>
""", unsafe_allow_html=True)

# --- 初始化会话状态 (存储聊天记录) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 添加一句开场白
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "嗨！我是暖暖。今天过得怎么样？有什么想跟我分享的吗？🌸"
    })

# --- 遍历并显示所有消息 (气泡形式) ---
for message in st.session_state.messages:
    if message["role"] == "user":
        # 👤 用户气泡 (右侧，粉色)
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin: 15px 0; animation: fadeIn 0.5s;">
            <div style="max-width: 75%; padding: 12px 18px; background: #ffb7c5; color: #fff; 
                        border-radius: 18px 18px 4px 18px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        font-size: 1.05em; line-height: 1.6; word-wrap: break-word;">
                {message["content"]}
            </div>
            <div style="width: 42px; height: 42px; margin-left: 10px; background: #ff9eb5; 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        font-size: 1.6em; flex-shrink: 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                😊
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 👼 暖暖气泡 (左侧，白色)
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 15px 0; animation: fadeIn 0.5s;">
            <div style="width: 42px; height: 42px; margin-right: 10px; background: #ffd1dc; 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        font-size: 1.6em; flex-shrink: 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                👼
            </div>
            <div style="max-width: 75%; padding: 12px 18px; background: #ffffff; color: #333; 
                        border-radius: 18px 18px 18px 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        font-size: 1.05em; line-height: 1.6; border: 1px solid #ffeef2; word-wrap: break-word;">
                {message["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 底部输入框 ---
user_input = st.chat_input("和暖暖说说话吧...")

if user_input:
    # 1. 显示用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. 模拟思考延迟 (增加真实感)
    with st.spinner("暖暖正在认真听..."):
        time.sleep(0.8) 
        # 3. 生成回复
        response_text = get_nuan_response(user_input)
    
    # 4. 显示暖暖回复
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    # 5. 刷新页面以显示新消息
    st.rerun()
