import streamlit as st
from streamlit_chat import message, AvatarStyle
import json
import os
import datetime
import petname

BOT_AVATAR="jdenticon" #gridy
USER_AVATAR="micah"
JSON_FILE = 'message_history.json'

def load_data(chat_id):
    with open(JSON_FILE, 'r') as file:
        return json.load(file)

def save_data(chat_id, message_history):
    with open(JSON_FILE, 'w') as file:
        json.dump(message_history, file)

def init_new_chat(chat_id):
    welcome_messages = [
        {
            "message": f"Hi {chat_id}, "
                "welcome to chat moderation service."
                "Please type messages to experience chat moderation service",
            "is_user": False,
            "key": datetime.datetime.now().timestamp()
        }
    ]    
    save_data(chat_id, welcome_messages)

def load_message_history(chat_id):
    if not os.path.exists(chat_id):
        init_new_chat(chat_id)
    return load_data(chat_id)

def write_message_history(chat_id, message_history):
    # if os.path.exists(chat_id):
    #     with open(chat_id, 'r') as file:
    #         data = json.load(file)
        # data.append(message)
        save_data(chat_id, message_history)        
def clear_message_history(chat_id):
    init_new_chat(chat_id)


def get_user_id():
    if 'user' not in st.session_state:        
        st.session_state['user'] = petname.generate()
    return st.session_state['user']

class MessagingPage:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.reload_message_history()
        self.window()
    def reload_message_history(self):
        self.message_history = load_message_history(self.chat_id)
    def render_chats(self):
        for message_ in self.message_history:
            avatar = USER_AVATAR if message_["is_user"] else BOT_AVATAR
            message(
                message_["message"],
                is_user=message_["is_user"],
                avatar_style=avatar, 
                key=message_["key"]
            )
    def on_clear_chat_history(self):
        print("clear button")
        input_=''
        clear_message_history(self.chat_id)
        self.placeholder.empty()
        # st.experimental_rerun()
    def on_message_send(self):
        input_ = st.session_state.new_message_box
        input_ = input_.strip()
        with self.placeholder.container():
            if input_ : #and send_button:
                new_message_text = "## MESSAGE MODERATED ##" if "fuck" in input_ else input_
                message_ = {
                    "message": new_message_text,
                    "is_user": True,
                    "key": datetime.datetime.now().timestamp()
                }
                self.message_history.append(message_)
                write_message_history(self.chat_id, self.message_history)
                # avatar = USER_AVATAR if message_["is_user"] else BOT_AVATAR
                # message(message_["message"], is_user=message_["is_user"], avatar_style=avatar, key=message_["key"])
    def window(self):
        st.title("Chat moderation service")
        st.write("""
            Chat moderation service aims to detect and flag unhealty chat messages.
            And reduce burden on moderators.
        """)
        self.render_chats()

        self.placeholder = st.empty()
        cols = st.columns([3,1,1])
        with cols[0]:
            input_ = st.text_input("you:", on_change=self.on_message_send, key='new_message_box')            
        with cols[1]:
            send_button =st.button("send", on_click=self.on_message_send)
        with cols[2]:
            clear_history_button =st.button("Clear history", on_click=self.on_clear_chat_history)

def main():
    chat_id = get_user_id()
    messaging_page = MessagingPage(chat_id)    

if __name__=='__main__':
    main()