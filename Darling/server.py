from flask import Flask, request, jsonify
import time
from collections import deque

app = Flask("Darling")

convo = []

users = {}
#here i am adding some comments 
#verify function to verify the request made is POST or not
@app.route("/verify/", methods=['POST'])
def verify():
    if request.method == 'POST':
        user_id = 'user' + str(time.time())
        q = deque()
        users[user_id] = q
        return user_id

    else:
        print("Not a post request")
        return "Not Success"

#chat function to actually send messages to user by checking GET or POST route
@app.route("/", methods=['GET', 'POST'])
def chat():

    if request.method == 'POST':

        # Time of messaged sent by client
        current_time = time.strftime("%H:%M:%S")
        json_msg = request.get_json()

        if json_msg['purpose']=='post':

            # add time to the json data
            json_msg['time'] = current_time

            # append the json to the keep the history
            convo.append(json_msg)

            # append the message in every inbox
            for user in users:
                if user==json_msg['user_id']:
                    continue

                users[user].append(json_msg)


            print(f"{json_msg['name']} says : {json_msg['msg']}")

            return "sent"

        if json_msg['purpose']=='get':
            new_msgs = []
            q = users[json_msg['user_id']]
            while q:
                new_msgs.append(q.popleft())
            return jsonify(new_msgs)


        
        else:
            return "undefined purpose"

    return "Method Not supportes Darling :("


if __name__ == "__main__":
    app.run(debug=False)
