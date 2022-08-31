import streamlit as st
from streamlit_chat import message, AvatarStyle
import json
import os
import datetime

BOT_AVATAR="jdenticon" #gridy
USER_AVATAR="micah"
MESSAGE_HISTORY = "message_history.json"

def init_new_chat(chat_id):
    welcome_messages = [
        {
            "message": "Hi <User>, "
                "welcome to chat moderation service."
                "Please type messages to experience chat moderation service",
            "is_user": False,
            "key": datetime.datetime.now().timestamp()
        }
    ]    
    with open(chat_id, 'w') as file:
        json.dump(welcome_messages, file)

def load_message_history(chat_id):
    if not os.path.exists(chat_id):
        init_new_chat(chat_id)
    with open(chat_id, 'r') as file:
        return json.load(file)

def write_message_history(chat_id, message_history):
    # if os.path.exists(chat_id):
    #     with open(chat_id, 'r') as file:
    #         data = json.load(file)
        # data.append(message)
        with open(chat_id, 'w') as file:
            return json.dump(message_history, file)
def clear_message_history(chat_id):
    init_new_chat(chat_id)

def on_message_send(placeholder):
    value = st.session_state.new_message_box
    print(value)


def main(chat_id = MESSAGE_HISTORY):

    st.title("Chat moderation service")
    st.write("""
        Chat moderation service aims to detect and flag unhealty chat messages.
        And reduce burden on moderators.
    """)

    message_history = load_message_history(chat_id)    

    for message_ in message_history:    
        avatar = USER_AVATAR if message_["is_user"] else BOT_AVATAR
        message(
            message_["message"],
            is_user=message_["is_user"],
            avatar_style=avatar, 
            key=message_["key"]
        )

    placeholder = st.empty()
    cols = st.columns([3,1,1])
    with cols[0]:
        input_ = st.text_input("you:", on_change=on_message_send, args=(placeholder,), key='new_message_box')
    with cols[1]:
        send_button =st.button("send")
    with cols[2]:
        clear_history_button =st.button("Clear history")
    
    if clear_history_button:
        print("clear button")
        input_=''
        clear_message_history(chat_id)
        placeholder.empty()
        # st.experimental_rerun()


if __name__=='__main__':
    main()