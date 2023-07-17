from flask import Flask, jsonify, render_template, request
from fsm_chatbot.fsm import FiniteStateMachine as FSM
from bs4 import BeautifulSoup

import re

# import logging
from loguru import logger

app = Flask(__name__)
app.static_folder = 'static'

# Initialize Database and Finite State Machine  
fsm = FSM()
file_path = f"Log/chat-history.log"
logger.add(file_path, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} - {message}")

@app.route("/")
def home():
    return render_template("fix-index.html")

@app.route("/chatbot", methods=["POST"])
def main_fsm():
    # get data when the send button is clicked
    data = request.get_json()
    user_input = data['userInput']

    # detect intent based on user input
    intent = fsm.detect_intent(user_input)
    print('Intent : ', intent)

    # reply to user based on user intent
    bot_response = fsm.respond(intent, user_input)
    current_state = fsm.get_state()

    # save the conversation between bot and user to log file
    chat_log('User', f"{user_input}. (Current State : {current_state})")
    
    for response in bot_response: 
        # if re.search(r'<.*?>', response):
        #     soup = BeautifulSoup(response, 'html.parser')
        #     trs = soup.find_all('tr')

        #     if trs:
        #         data = {}

        #         for tr in trs:
        #             elements = tr.find_all(['td', 'th'])
        #             element_values = [element.text.strip() for element in elements if element.text.strip()]
        #             if len(element_values) == 2:
        #                 data[element_values[0]] = element_values[1]

        #         msg = '\n'.join([f"{key}: {value}" for key, value in data.items()])
        #         chat_log('Bot', msg)
            
        #     button_texts = [button.get_text().strip() for button in soup.find_all('button')]

        #     if button_texts:
        #         chat_log('Bot', button_texts)

        # else:
        chat_log('Bot', response)

    # return bot response as json object
    return jsonify({'response': bot_response, 'current_state': current_state})


@app.route("/reset", methods=['POST'])
def reset_chat():
    data = request.get_json()
    chat_history = data['history']
    chat_history = []
    
    fsm.current_state = 'greeting'
    fsm.is_login = False
    fsm.is_confirm = False
    fsm.ner.remove_merktipe()
    fsm.checkout.delete_slot_checkout()
    fsm.regis.delete_slot_regis()
    fsm.login.delete_slot_login()
    
    return chat_history

def chat_log(user, message):
    logger.info(f"[{user}]: {message}")

if __name__ == "__main__":
    app.run(debug=True)
