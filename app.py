import streamlit as st
from agent.agent import Agent
from utils.logger_handler import logger
import time

st.set_page_config(page_title="智能客服", page_icon="🤖")

if "agent" not in st.session_state:
    st.session_state.agent = Agent()
    st.session_state.messages = []

st.title("🤖 扫地机器人智能客服")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("请输入您的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        config = {"configurable": {"thread_id": "streamlit_session"}}
        thinking_expander = st.expander("💭 思考过程", expanded=True)
        thinking_placeholder = thinking_expander.empty()
        answer_placeholder = st.empty()

        try:
            response = st.session_state.agent.stream(prompt, config)
            thinking_content = []
            final_answer = ""
            is_thinking = True

            for chunk in response:
                chunk_str = str(chunk).strip()
                if chunk_str:
                    thinking_content.append(chunk_str + "\n")
                    if len(thinking_content) > 1:
                        thinking_placeholder.markdown("".join(thinking_content[:-1]))
                    else:
                        thinking_placeholder.markdown("".join(thinking_content))

            if len(thinking_content) > 1:
                final_answer = thinking_content[-1]
                thinking_expander.expanded = False
            elif thinking_content:
                final_answer = thinking_content[-1]

            if final_answer:

                response_messages = []
                def capture(generator,cache_list):
                    for chunk in generator:
                        cache_list.append(chunk)
                        for char in chunk:
                            time.sleep(0.05)
                            yield char
                answer_placeholder.write_stream(capture(final_answer,response_messages))
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
            else:
                answer_placeholder.markdown("".join(thinking_content))
                st.session_state.messages.append({"role": "assistant", "content": "".join(thinking_content)})

        except Exception as e:
            error_msg = f"抱歉，发生了错误：{str(e)}"
            st.error(error_msg)
            logger.error(f"Streamlit Agent Error: {e}")