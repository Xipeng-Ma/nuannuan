import streamlit as st
import random
import time
from PIL import Image, ImageDraw, ImageFont

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="暖暖·心灵栖息地",
    page_icon="🕊️",
    layout="centered"
)

# --- 2. 核心功能：用代码画一个丘比特 (解决图片加载失败问题) ---
def create_cupid_image():
    # 创建一个透明背景的图像
    img = Image.new('RGBA', (300, 300), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # 定义颜色
    skin_color = (255, 224, 189) # 肤色
    wing_color = (255, 255, 255) # 翅膀白
    bow_color = (255, 171, 145)  # 弓箭粉
    heart_color = (255, 128, 128) # 爱心红
    
    # 画身体 (简单的圆形代表头)
    draw.ellipse([100, 80, 200, 180], fill=skin_color, outline=(255, 200, 150), width=3)
    
    # 画眼睛 (闭着的笑眼，表示温柔)
    draw.arc([120, 110, 140, 130], 0, 180, fill=(100, 100, 100), width=3)
    draw.arc([160, 110, 180, 130], 0, 180, fill=(100, 100, 100), width=3)
    
    # 画嘴巴 (微笑)
    draw.arc([130, 130, 170, 160], 0, 180, fill=(100, 100, 100), width=3)
    
    # 画翅膀 (左右各一个半圆)
    draw.ellipse([40, 90, 110, 170], fill=wing_color, outline=(240, 240, 240), width=2)
    draw.ellipse([190, 90, 260, 170], fill=wing_color, outline=(240, 240, 240), width=2)
    
    # 画手里的弓 (简单的弧线)
    draw.arc([80, 180, 220, 280], 0, 180, fill=bow_color, width=5)
    
    # 画一颗飘在旁边的爱心
    draw.polygon([(230, 60), (240, 50), (250, 60), (240, 80)], fill=heart_color)
    draw.polygon([(230, 60), (220, 50), (210, 60), (220, 80)], fill=heart_color)
    
    return img

# 生成图片对象
cupid_img = create_cupid_image()

# --- 3. 温柔系 CSS (低饱和度，护眼，宁静) ---
st.markdown("""
<style>
    /* 背景：温暖的米白色到淡粉色的渐变 */
    .stApp {
        background: linear-gradient(180deg, #fdfbf7 0%, #fff0f5 100%);
    }
    /* 字体颜色：深灰褐色，比纯黑更柔和 */
    h1, h2, h3, p, div, label, span {
        color: #5d5d5d;
        font-family: 'Helvetica', 'Microsoft YaHei', sans-serif;
    }
    /* 标题居中，字号适中，去掉攻击性 */
    h1 {
        text-align: center;
        font-weight: normal;
        letter-spacing: 2px;
        color: #8d6e63;
        margin-top: 20px;
    }
    /* 副标题样式 */
    .subtitle {
        text-align: center;
        color: #a1887f;
        font-size: 16px;
        margin-bottom: 30px;
        line-height: 1.6;
    }
    /* 输入框样式：圆润，无边框感 */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
        color: #5d5d5d;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    /* 按钮样式：像棉花糖一样柔软 */
    .stButton > button {
        background-color: #ffccbc;
        color: #5d4037;
        border-radius: 25px;
        border: none;
        font-weight: normal;
        width: 100%;
        padding: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #ffab91;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        color: #5d4037;
    }
    /* 消息气泡样式 */
    .success-box {
        background-color: #fff3e0;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ffccbc;
        margin-top: 20px;
        line-height: 1.6;
        color: #5d4037;
    }
    /* 隐藏默认的 Streamlit 菜单，保持界面纯净 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 4. 主界面内容 ---

# 顶部：展示生成的图片和新文案
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(cupid_img, use_column_width=False, caption="") # 显示代码画的图

st.title("暖暖")
# ✅ 修改后的文案：去掉了“射中”，改为“陪伴”和“接纳”
st.markdown("""
<div class='subtitle'>
    你不必完美，只需存在。<br>
    这里有一个安静的角落，愿意接住你所有的情绪。
</div>
""", unsafe_allow_html=True)

# --- 功能一：情绪树洞 (核心) ---
st.subheader("🌲 今天，想聊聊吗？")
st.write("无论是开心、难过，还是仅仅觉得累了，都可以写下来。丘比特会一直在这里听着。")

user_feeling = st.text_area(
    "在这里写下你的心情...", 
    height=150, 
    placeholder="例如：今天觉得好累，好像什么都做不好... 或者只是发个句号也可以。",
    label_visibility="collapsed"
)

# 预设的温柔回应库 (针对抑郁情绪的特别设计)
comfort_responses = [
    "谢谢你愿意告诉我这些。即使现在很黑，我也会提着灯陪你坐一会儿。🕯️",
    "辛苦了，真的辛苦了。你不需要时刻都坚强，此刻的脆弱也是被允许的。🫂",
    "我听到了你的声音。请记住，你的存在本身，就是一件很美好的事情。🌟",
    "没关系，不用急着好起来。我们就这样慢慢地呼吸，一下，又一下。🍃",
    "世界有时候很冷，但我想给你一个暖暖的拥抱。你值得被爱，无条件地。❤️",
    "你已经做得很好了，真的。能撑过今天，就是一种伟大的胜利。🏆",
    "如果觉得太重了，就先把包袱放下来吧。丘比特帮你保管一会儿。🎒"
]

if st.button("🕊️ 发送给丘比特"):
    if user_feeling:
        with st.spinner("丘比特正在认真倾听..."):
            time.sleep(1.5) # 模拟思考，表示重视
        
        # 随机选择一句温柔的话
        response = random.choice(comfort_responses)
        
        st.markdown(f"""
        <div class="success-box">
            <b>🕊️ 丘比特说：</b><br><br>
            {response}
            <br><br>
            <i>(你的这段话，我已经好好收在心里了。)</i>
        </div>
        """, unsafe_allow_html=True)
        
        # 触发轻微的撒花，不要太吵闹
        st.balloons()
    else:
        st.info("不想说话也没关系，丘比特会静静地陪着你。☁️")

# --- 功能二：能量补给站 ---
st.markdown("---")
st.subheader("☀️ 小小能量站")
st.write("如果心里太累，试着做一件最小的事，或者读一句暖暖的话。")

col1, col2 = st.columns(2)

with col1:
    if st.button("🌬️ 带我深呼吸"):
        st.success("来，跟着我：吸气——(停顿)——呼气——。你做得很棒。")
        st.write("> 再试一次：吸气... 感受空气进入身体... 呼气... 把烦恼都吹走...")

with col2:
    if st.button("🍬 领取今日糖果"):
        candies = [
            "你今天喝水了吗？记得照顾好自己的身体哦。",
            "窗外的云在慢慢飘，你也像云一样自由，不必停留在原地。",
            "哪怕只是起床刷了牙，今天也已经是成功的一天了。",
            "有人也许正在世界的某个角落，因为你的存在而感到温暖。",
            "允许自己休息一下，这不是偷懒，是充电。"
        ]
        st.success(f"🍬 **{random.choice(candies)}**")

# --- 功能三：紧急求助 (重要！) ---
st.markdown("---")
with st.expander("🆘 如果我感觉非常糟糕，该怎么办？"):
    st.warning("""
    **亲爱的，如果你感到极度痛苦，或者有伤害自己的念头，请务必寻求专业的帮助：**
    
    - 📞 **全国希望24热线**: 400-161-9995
    - 📞 **青少年公共服务热线**: 12355
    - 🏥 请直接前往最近的医院急诊科，或拨打 110 / 120。
    
    你很重要，这个世界需要你。请给专业人士一个机会来帮助你。
    """)

# 页脚
st.markdown("""
<div style='text-align: center; color: #bcaaa4; margin-top: 40px; font-size: 12px;'>
    愿温暖常伴你左右 | 暖暖 · 守护版
</div>
""", unsafe_allow_html=True)
