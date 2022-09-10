import streamlit as st
from streamlit_chat import message, AvatarStyle
import os
import datetime
import petname
import configparser
import requests
import logging
import uuid

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=os.environ.get("LOGLEVEL", "INFO")
)
logger = logging.getLogger()

config = configparser.ConfigParser()
config.read('config/config.ini')

BOT_AVATAR          = config['app'].get('BOT_AVATAR')
USER_AVATAR         = config['app'].get('USER_AVATAR')
MODERATED_MESSAGE   = config['app'].get('MODERATED_MESSAGE')

PREDICTION_SERVICE_URL = config['moderation_service'].get('ENDPOINT')
PREDICTION_SERVICE_THRESHOLD = config['moderation_service'].getfloat('THRESHOLD')

def message_moderated(message, message_id):    
    should_moderate = False
    message = {
        'Records':[{
            'body': message,
            'message_id': message_id
        },]
    }
    url = PREDICTION_SERVICE_URL
    print(f'URL: {url}')
    try:
        response = requests.post(url, json=message)        
        data = response.json()
        print(data)
        prediction = data['predictions'][0]
        should_moderate =  prediction['prediction']['moderate_message'] > PREDICTION_SERVICE_THRESHOLD
    except Exception as e:
        logger.error('error occured', e)
    return should_moderate

def init_message_history(chat_id):    
    welcome_messages = [
        {
            "message": f"Hi {chat_id}, "
                "welcome to chat moderation service."
                "Please type messages to experience chat moderation service",
            "is_user": False,
            "key": datetime.datetime.now().timestamp()
        }
    ]    
    write_message_history(chat_id, welcome_messages)

def load_message_history(chat_id):
    if 'message_history' not in st.session_state:
        init_message_history(st.session_state['user'])
    return st.session_state['message_history']

def write_message_history(chat_id, message_history):
    st.session_state['message_history'] = message_history

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
        input_=''
        init_message_history(self.chat_id)
        self.placeholder.empty()
        # st.experimental_rerun()
    def on_message_send(self):
        input_ = st.session_state.new_message_box
        input_ = input_.strip()
        with self.placeholder.container():
            if input_ :
                message_id = str(uuid.uuid4())
                new_message_text = MODERATED_MESSAGE if message_moderated(input_, message_id) else input_
                message_ = {
                    "message": new_message_text,
                    "is_user": True,
                    "key": datetime.datetime.now().timestamp()
                }
                self.message_history.append(message_)
                write_message_history(self.chat_id, self.message_history)
    def window(self):
        st.title("Chat moderation service")
        st.write("""
            Chat moderation service aims to detect and flag unhealty chat messages.
            And reduce burden on moderators.
        """)
        self.render_chats()

        self.placeholder = st.empty()
        cols = st.columns([4,1])
        with cols[0]:
            input_ = st.text_input("you:", on_change=self.on_message_send, key='new_message_box')            
        with cols[1]:
        #     send_button =st.button("send", on_click=self.on_message_send)
        # with cols[2]:
            clear_history_button =st.button("Clear history", on_click=self.on_clear_chat_history)

def main():
    chat_id = get_user_id()
    messaging_page = MessagingPage(chat_id)    

if __name__=='__main__':
    main()