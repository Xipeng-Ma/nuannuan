import streamlit as st
import random
import time

# --- 1. 页面配置：强调宁静与安全 ---
st.set_page_config(
    page_title="暖暖·心灵栖息地",
    page_icon="🕊️",
    layout="centered"
)

# --- 2. 资源链接 ---
IMAGE_URL = "https://raw.githubusercontent.com/Xipeng-Ma/nuannuan/main/cupid.png"

# --- 3. 温柔系 CSS (低饱和度，护眼，宁静) ---
st.markdown("""
<style>
    /* 背景：温暖的米白色，不刺眼 */
    .stApp {
        background-color: #fdfbf7;
    }
    /* 字体颜色：深灰褐色，比纯黑更柔和 */
    h1, h2, h3, p, div, label {
        color: #5d5d5d;
        font-family: 'Helvetica', 'Microsoft YaHei', sans-serif;
    }
    /* 标题居中，字号适中 */
    h1 {
        text-align: center;
        font-weight: normal;
        letter-spacing: 2px;
        color: #8d6e63;
    }
    /* 输入框样式：圆润，无边框感 */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
        color: #5d5d5d;
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
    }
    /* 隐藏默认的 Streamlit 菜单，保持界面纯净 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 4. 核心内容：温柔的陪伴 ---

# 顶部：丘比特的问候
st.title("🕊️ 你并不孤单")
try:
    st.image(IMAGE_URL, width=220, caption="我会一直在这里陪着你")
except:
    pass

st.markdown("""
<div style='text-align: center; color: #8d6e63; margin-bottom: 30px;'>
    这里没有评判，没有压力。<br>
    只有暖暖的丘比特，愿意倾听你的一切。
</div>
""", unsafe_allow_html=True)

# --- 功能一：情绪树洞 (核心) ---
st.subheader("🌲 今天的你，还好吗？")
st.write("想说什么都可以，哪怕是碎碎念，或者是沉默的叹息。丘比特都会认真听。")

user_feeling = st.text_area(
    "在这里写下你的心情...", 
    height=150, 
    placeholder="例如：今天觉得好累，好像什么都做不好...",
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
        
        # 随机选择一句温柔的话，或者根据长度简单反馈
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

# --- 功能二：能量补给站 (替代之前的测试) ---
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
    愿温暖常伴你左右 | 暖暖丘比特 · 守护版
</div>
""", unsafe_allow_html=True)
