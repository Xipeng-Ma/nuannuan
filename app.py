import streamlit as st
import time
import random

# ==========================================
# 1. 页面配置 & 样式
# ==========================================
st.set_page_config(page_title="暖暖 - 你的灵魂伙伴", page_icon="💖", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stChatInputContainer > div {background-color: #fff0f5; border-radius: 20px;}
    /* 增加一点打字机效果的动画 */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .message-box { animation: fadeIn 0.4s ease-out; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 暖暖的“大脑”：人格化核心逻辑
# ==========================================

def get_nuan_response(user_text, history):
    """
    模拟具有人格、记忆和情绪的回复逻辑。
    user_text: 用户当前输入
    history: 最近的聊天记录（用于模拟记忆）
    """
    text = user_text.lower()
    
    # --- 1. 记忆提取 (简单模拟) ---
    # 检查最近是否提到过特定话题
    recent_context = " ".join([m["content"] for m in history[-3:]]) if history else ""
    
    has_mentioned_food = "饿" in text or "吃" in text or "饭" in recent_context
    has_mentioned_sleep = "困" in text or "睡" in text or "累" in recent_context
    has_mentioned_work = "工作" in text or "学习" in text or "忙" in text
    
    # --- 2. 情绪检测 (加权) ---
    mood_score = 0 # -10 (极度低落) 到 10 (极度开心)
    
    sad_triggers = ["难过", "伤心", "哭", "烦", "累", "痛苦", "绝望", "孤单", "郁闷", "讨厌", "bad", "sad"]
    happy_triggers = ["开心", "哈哈", "棒", "好", "幸运", "爱", "喜欢", "美", "happy", "love", "笑"]
    anxious_triggers = ["焦虑", "担心", "怕", "紧张", "迷茫", "怎么办", "压力"]
    
    if any(w in text for w in sad_triggers): mood_score -= 5
    if any(w in text for w in happy_triggers): mood_score += 5
    if any(w in text for w in anxious_triggers): mood_score -= 3
    
    # --- 3. 人格化回复生成 ---
    response = ""
    action = "" # 动作描写
    
    # 【场景 A：用户很低落】-> 温柔陪伴型
    if mood_score <= -4:
        actions = ["*轻轻抱住你*", "*摸摸你的头*", "*递给你一张纸巾*", "*安静地坐在你身边*"]
        templates = [
            f"{random.choice(actions)} 感觉到你现在心里沉甸甸的。没关系，不用急着好起来，我会一直陪着你，直到雨停。",
            f"{random.choice(actions)} 抱抱～ 这个世界有时候真的很讨厌。如果你想哭就大声哭出来，我的肩膀借给你，弄湿了也没关系。",
            f"{random.choice(actions)} 我在听呢。不管发生什么，都不是你的错。你已經很努力了，真的。"
        ]
        response = random.choice(templates)
        
    # 【场景 B：用户很开心】-> 热情分享型
    elif mood_score >= 4:
        actions = ["*眼睛亮晶晶地看着你*", "*开心地转了个圈*", "*为你鼓掌*", "*笑得合不拢嘴*"]
        templates = [
            f"{random.choice(actions)} 哇！听到你这么开心，我感觉周围的空气都变甜了！✨ 快跟我说说，到底是什么好事呀？",
            f"{random.choice(actions)} 太棒啦！你的笑容就是今天最棒的风景！☀️ 这种好心情要牢牢抓住哦！",
            f"{random.choice(actions)} 耶！真为你高兴！看来今天是个幸运日呢，要不要许个愿？😉"
        ]
        response = random.choice(templates)
        
    # 【场景 C：用户焦虑/迷茫】-> 理性安抚型
    elif any(w in text for w in anxious_triggers):
        actions = ["*递给你一杯温热的茶*", "*拉着你的手*", "*认真地看着你的眼睛*"]
        templates = [
            f"{random.choice(actions)} 深呼吸～ 来，跟着我做：吸气... 呼气... 别怕，天塌不下来。我们一步一步来，好吗？",
            f"{random.choice(actions)} 迷茫是因为你想变得更好呀。不用现在就看清整条路，只要看清脚下的这一步就够了。我会陪着你走的。",
            f"{random.choice(actions)} 紧张是正常的，说明你在乎这件事。但别忘了，你比你自己想象的更强大哦！"
        ]
        response = random.choice(templates)
        
    # 【场景 D：日常闲聊 + 记忆联动】-> 像朋友一样聊天
    else:
        # 尝试结合“记忆”进行回复
        if has_mentioned_food and "饿" not in text:
            response = f"*关切地看着你* 对了，刚才你说有点饿，现在去吃点好吃的了吗？🍜 别饿坏了肚子，我会心疼的。"
        elif has_mentioned_sleep and "困" not in text:
            response = f"*轻声细语* 刚才听你说有点累，今晚要不要早点休息？🌙 把烦恼都关在门外，睡个美美的觉吧。"
        elif has_mentioned_work:
            response = f"*拍拍你的背* 工作或学习辛苦啦！要不要歇五分钟？喝口水，眺望远方，我陪你发会儿呆～ ☕"
        elif "名字" in text or "叫啥" in text:
            response = "*歪头一笑* 我叫暖暖呀！是你专属的情感小卫士，也是你随时可以打扰的好朋友。你呢？想让我怎么称呼你？"
        elif "谢谢" in text:
            response = "*脸红了一下* 哎呀，跟我这么客气干嘛！能帮到你，我也超级开心的！💖"
        else:
            # 纯闲聊库（加入更多语气词和动作）
            chat_pool = [
                "*托着下巴* 嗯嗯，我在听呢。然后呢？我想多了解一点你的想法。",
                "*点点头* 原来是这样呀... 你的视角好独特，我之前都没想过！",
                "*笑着看你* 不管你说什么，我都觉得很有道理。毕竟是你嘛！😉",
                "今天天气好像不错/有点阴郁（看向窗外），你的心情有没有受它影响呀？",
                "*突然想到什么* 对了，最近有听到什么好听的歌吗？求推荐！🎵",
                "感觉你今天说话的声音（文字）里带着一丝特别的情绪，是有什么心事吗？"
            ]
            response = random.choice(chat_pool)

    return response

# ==========================================
# 3. 界面渲染
# ==========================================

# --- 顶部人设展示 ---
st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="color: #ff69b4; font-family: 'Segoe UI', sans-serif;">💖 暖暖</h1>
    <p style="color: #666; font-size: 0.9em;">
        “嘿，我是暖暖。不只是机器人，更是想懂你的朋友。”<br>
        👼 会倾听 · 会记忆 · 会心疼 · 会撒娇
    </p>
</div>
""", unsafe_allow_html=True)

# --- 初始化会话 ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 开场白更具人格化
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "*微笑着向你招手* 嗨！终于等到你了。我是暖暖。今天过得怎么样？有没有发生什么想跟我分享的小事？🌸"
    })

# --- 显示历史消息 (气泡) ---
for i, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f"""
        <div class="message-box" style="display: flex; justify-content: flex-end; margin: 15px 0;">
            <div style="max-width: 75%; padding: 12px 18px; background: #ffb7c5; color: #fff; 
                        border-radius: 18px 18px 4px 18px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        font-size: 1.05em; line-height: 1.6;">
                {message["content"]}
            </div>
            <div style="width: 40px; height: 40px; margin-left: 10px; background: #ff9eb5; 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        font-size: 1.5em;">😊</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-box" style="display: flex; justify-content: flex-start; margin: 15px 0;">
            <div style="width: 40px; height: 40px; margin-right: 10px; background: #ffd1dc; 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        font-size: 1.5em;">👼</div>
            <div style="max-width: 75%; padding: 12px 18px; background: #ffffff; color: #333; 
                        border-radius: 18px 18px 18px 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        font-size: 1.05em; line-height: 1.6; border: 1px solid #ffeef2;">
                {message["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 输入处理 ---
user_input = st.chat_input("和暖暖说说心里话...")

if user_input:
    # 1. 添加用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. 模拟思考 (稍微长一点，显得在认真思考)
    with st.spinner("暖暖正在认真思考怎么回应你..."):
        time.sleep(1.2) 
        # 传入历史记录，让回复更有上下文感
        reply = get_nuan_response(user_input, st.session_state.messages)
    
    # 3. 添加暖暖回复
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
