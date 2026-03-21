
import streamlit as st
import requests

# ================= 配置区域 =================
# 🔴 重要：把你的 Kimi API Key 填在下面引号里，不要泄露给他人查看源代码
MY_API_KEY = "sk-gznbJSCkpjPd5mHsY2vgZIE4YNwEtfuSgqlSVx8jw30jFTbb" 
# ===========================================

st.set_page_config(page_title="暖暖 - 你的贴心伙伴", page_icon="🌸")

# 不再需要侧边栏输入了，因为 Key 已经在上面配置好了
# with st.sidebar: ... (这部分删掉了)

st.title("🌸 你好，我是暖暖")
st.markdown("我在这里陪你，无论是职业规划还是生活琐事。")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("和暖暖说点什么吧..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 暖暖正在思考...")
        
        try:
            url = "https://api.moonshot.cn/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {MY_API_KEY}"  # 直接使用内置的 Key
            }
            
            messages_payload = [
                {"role": "system", "content": "你是一个温暖、体贴、善解人意的女孩，名叫'暖暖'。语气温柔亲切，多用表情符号🌸。"}
            ] + st.session_state.messages[-10:] 

            data = {
                "model": "moonshot-v1-8k",
                "messages": messages_payload,
                "temperature": 0.7,
                "stream": False 
            }

            response = requests.post(url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                ai_reply = result['choices'][0]['message']['content']
                message_placeholder.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            else:
                error_msg = f"⚠️ 出错了: {response.text}"
                message_placeholder.markdown(error_msg)

        except Exception as e:
            message_placeholder.markdown(f"⚠️ 连接失败: {str(e)}")

st.markdown("---")
st.caption("Powered by Kimi 🌸")
