from revChatGPT.revChatGPT import Chatbot
from flask import Flask, Response, request, make_response
app = Flask(__name__)




class MyChatbot(Chatbot):
    def __init__(self, debug=False):
        class CaptchaSolver: 
            """ 
            Captcha solver 
            """ 
            @staticmethod 
            def solve_captcha(raw_svg): 
                svg = raw_svg 
                with open("captcha.svg", "w") as f: 
                    print("Captcha saved to captcha.svg") 
                    f.write(svg) 
                solution = input("Please solve the captcha: ") 
                return solution 
        
        config = {
            "email": "fly19940923@outlook.com",
            "password": "xxxx",
            #"session_token": "<SESSION_TOKEN>", # Deprecated. Use only if you encounter captcha with email/password
            "proxy": "http://127.0.0.1:10886"
        }
        super(MyChatbot, self).__init__(config, conversation_id=None, debug=debug, captcha_solver=CaptchaSolver())


chatbot = MyChatbot(debug=True)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    r_content = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        r_content = request.get_json().get("data")
    elif(content_type == 'application/x-www-form-urlencoded'):
        print(request.form)
        r_content = request.form[0].get('data')
    else:
        print(request.content)
        return 'Content-Type not supported!'
    print(r_content)
    RETRIES = 2
    for _ in range(RETRIES):

        response = chatbot.get_chat_response(r_content, output="text")
        print("[chatGPT:]", response)
        if response.get("message"):
            res = make_response({"data": response['message'], "code": 200}, 200)
            return res
        else:
            continue

if __name__ == "__main__":
    app.run(port=8001)
# from asyncChatGPT.asyncChatGPT import Chatbot # async!!!!
# import asyncio
# message = asyncio.run(chatbot.get_chat_response("Hello world"))['message']
# print(message)
# ... # After the initial setup
# import asyncio
# async def printMessage():
#     async for i in await chatbot.get_chat_response("hello", output="stream"):
#         print(i['message'])
# asyncio.run(printMessage())

# For the config please go here:
# https://github.com/acheong08/ChatGPT/wiki/Setup




 # After the initial setup
# The text output



# returns {'message':message, 'conversation_id':self.conversation_id, 'parent_id':self.parent_id}

# The stream output
# response = chatbot.get_chat_response("Hello world", output="stream")
# for res in response:
#     print(res['message'])

# returns {'message':message, 'conversation_id':self.conversation_id, 'parent_id':self.parent_id}
