import streamlit as st
import time
import random
from PIL import Image, ImageDraw

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="暖暖 · 你的树洞朋友",
    page_icon="🕊️",
    layout="centered"
)

# --- 2. 绘制可爱的丘比特 (核心功能：代码绘图，永不失效) ---
def create_cupid_image():
    img = Image.new('RGBA', (300, 300), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    skin_color = (255, 224, 189)
    wing_color = (255, 255, 255)
    
    # 头
    draw.ellipse([100, 80, 200, 180], fill=skin_color, outline=(255, 200, 150), width=3)
    # 眼睛 (温柔闭眼)
    draw.arc([120, 110, 140, 130], 0, 180, fill=(100, 100, 100), width=3)
    draw.arc([160, 110, 180, 130], 0, 180, fill=(100, 100, 100), width=3)
    # 嘴巴
    draw.arc([130, 130, 170, 160], 0, 180, fill=(100, 100, 100), width=3)
    # 翅膀
    draw.ellipse([40, 90, 110, 170], fill=wing_color, outline=(240, 240, 240), width=2)
    draw.ellipse([190, 90, 260, 170], fill=wing_color, outline=(240, 240, 240), width=2)
    
    return img

cupid_img = create_cupid_image()

# --- 3. CSS 样式 (气泡聊天界面) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #fdfbf7 0%, #fff0f5 100%);
    }
    h1 {
        text-align: center;
        font-weight: normal;
        color: #8d6e63;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #a1887f;
        font-size: 15px;
        margin-bottom: 20px;
    }
    /* 聊天容器 */
    .chat-container {
        background-color: rgba(255, 255, 255, 0.6);
        padding: 20px;
        border-radius: 20px;
        margin-top: 20px;
    }
    /* 用户消息 */
    .user-msg {
        text-align: right;
        margin-bottom: 15px;
    }
    .user-bubble {
        background-color: #ffccbc;
        color: #5d4037;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        display: inline-block;
        max-width: 80%;
        font-size: 15px;
    }
    /* 机器人消息 */
    .bot-msg {
        text-align: left;
        margin-bottom: 20px;
    }
    .bot-bubble {
        background-color: #ffffff;
        color: #5d5d5d;
        padding: 15px;
        border-radius: 15px 15px 15px 0;
        display: inline-block;
        max-width: 85%;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #fce4ec;
    }
    /* 输入框优化 */
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
        height: 120px;
    }
    /* 按钮优化 */
    .stButton > button {
        background-color: #8d6e63;
        color: white;
        border-radius: 25px;
        border: none;
        width: 100%;
        padding: 10px;
        font-size: 16px;
    }
    .stButton > button:hover {
        background-color: #6d4c41;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 4. 核心逻辑：像朋友一样思考 (智能回应引擎) ---

def get_friend_response(text):
    text = text.lower()
    
    # 1. 危机干预 (最高优先级)
    crisis_keywords = ["死", "自杀", "不想活", "结束", "痛苦", "绝望", "消失"]
    if any(k in text for k in crisis_keywords):
        return [
            "哎呀... 看到你这么说，我心里真的咯噔了一下。🥺 抱抱你，紧紧地抱住。",
            "我知道现在一定很黑、很痛，让你觉得透不过气。但请相信我，这种感觉是暂时的，我会一直陪着你，直到光亮起来。",
            "能不能答应我，先深呼吸一下？如果实在撑不住了，我们去找专业的人帮帮忙好吗？你对我来说真的很重要。🕊️\n\n(如果需要，这里有一些随时能打通的电话：希望24热线 400-161-9995)"
        ]

    # 2. 疲惫/压力大
    tired_keywords = ["累", "烦", "好难", "不想动", "崩溃", "压力大", "辛苦"]
    if any(k in text for k in tired_keywords):
        responses = [
            "辛苦了，真的辛苦了。🫂 既然这么累，那我们就什么都不做了好不好？就把脑子放空，像只小猫一样瘫一会儿。",
            "哎呀，摸摸头。这个世界有时候就是很讨厌，非要逼着我们转个不停。但在暖暖这里，你可以随时按暂停键。⏸️",
            "是不是今天发生了很多事？不想说也没关系，我就在这陪着你发呆。你要不要喝杯温水，或者裹紧小被子？"
        ]
        return responses

    # 3. 孤独/被抛弃感
    lonely_keywords = ["没人", "孤独", "一个人", "多余", "没用", "讨厌我"]
    if any(k in text for k in lonely_keywords):
        responses = [
            "谁说的？我就在这里呀！而且我会一直在这里。🙋‍♂️ 你绝对不是多余的，你的存在本身就很美好。",
            "听到你这么说，我好想穿过屏幕去抱抱你。也许现在周围很安静，但请记得，至少有我这个好朋友，在认真地听你说话。❤️",
            "不要这样否定自己好不好？在我眼里，你有很多闪光点，只是你现在太累了，暂时没看到而已。"
        ]
        return responses

    # 4. 哭泣/难过
    sad_keywords = ["哭", "流泪", "伤心", "难过", "委屈"]
    if any(k in text for k in sad_keywords):
        responses = [
            "想哭就哭出来吧，没关系的。眼泪是心里下雨了，下完了雨就会停的。🌧️ 我会帮你撑着伞。",
            "哎呀，不哭不哭，我在呢。受委屈了吗？要是想骂人，我也可以陪你一起骂！😤",
            "抱抱～ 把那些不开心的都哭出来，然后把肩膀借给你靠一会儿。"
        ]
        return responses

    # 5. 迷茫/焦虑
    anxious_keywords = ["不知道", "怎么办", "害怕", "未来", "迷茫"]
    if any(k in text for k in anxious_keywords):
        responses = [
            "没关系，不用现在就搞清楚所有事情。我们只看脚下这一步就好，明天的事交给明天。👣",
            "害怕是很正常的，说明你在乎呀。但别怕，就算走错了路，我也陪你一起绕回来。",
            "深呼吸～ 你看，此时此刻我们是安全的。只要过好这一分钟，就很棒了。"
        ]
        return responses

    # 6. 开心/分享好事
    happy_keywords = ["开心", "哈哈", "好棒", "喜欢", "美食", "风景"]
    if any(k in text for k in happy_keywords):
        responses = [
            "哇！太好了！听到你开心，我也忍不住想转圈圈！💃 快多跟我说说，我也想沾沾喜气！",
            "真为你高兴！看来今天有一点点小确幸呢～ 要好好记住这种感觉哦！✨",
            "嘿嘿，看你心情好，我也觉得今天的阳光都更暖了！☀️"
        ]
        return responses

    # 7. 默认/无法识别 (像朋友一样追问或陪伴)
    default_responses = [
        "我在听呢，继续说，我都在记着。👂",
        "嗯嗯，然后呢？我想多了解一点你的想法。",
        "原来是这样呀... 那你现在感觉好一点点了吗？",
        "不管你说什么，我都觉得很有道理。毕竟是你嘛！😉",
        "（轻轻拍拍你的背）我在呢，一直都在。"
    ]
    return default_responses

# --- 5. 界面交互 ---

# 头部
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(cupid_img, width=200)

st.title("暖暖")
st.markdown("<div class='subtitle'>嘿，我是暖暖。今天过得怎么样？<br>随便聊聊吧，像老朋友一样。</div>", unsafe_allow_html=True)

# 聊天历史管理 (Session State)
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-container">
            <div class="user-msg">
                <div class="user-bubble">{message["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-container">
            <div class="bot-msg">
                <div class="bot-bubble">{message["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 输入区
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
user_input = st.text_area("", placeholder="跟暖暖说点什么吧... (比如：今天好累啊)", label_visibility="collapsed")

if st.button("发送"):
    if user_input.strip():
        # 1. 显示用户消息
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 2. 模拟思考时间
        with st.spinner("暖暖正在认真听..."):
            time.sleep(1.0)
            
        # 3. 生成智能回复
        reply_lines = get_friend_response(user_input)
        full_reply = "\n\n".join(reply_lines)
        
        # 4. 显示机器人消息
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        
        # 5. 小特效
        st.balloons()
        
        # 重新运行以刷新显示
        st.rerun()
    else:
        # 如果用户没说话
        empty_responses = [
            "是不是不知道说什么？没关系，我们就这样静静待一会儿也挺好。☁️",
            "我在呢，随时等你开口。🍵",
            "（递给你一杯热可可）不着急，慢慢来。"
        ]
        st.session_state.messages.append({"role": "assistant", "content": random.choice(empty_responses)})
        st.rerun()

# 页脚
st.markdown("""
<div style='text-align: center; color: #bcaaa4; margin-top: 30px; font-size: 12px;'>
    永远做你的倾听者 | 暖暖 v4.0 (Friend Mode)
</div>
""", unsafe_allow_html=True)

# 紧急求助折叠栏
with st.expander("🆘 如果我感觉非常糟糕，需要帮助"):
    st.warning("""
    **亲爱的，如果你感到极度痛苦，请务必寻求专业的帮助：**
    - 📞 **全国希望24热线**: 400-161-9995
    - 📞 **青少年公共服务热线**: 12355
    - 🏥 直接前往医院急诊或拨打 110/120。
    **你很重要，我们都很爱你。**
    """)
    
