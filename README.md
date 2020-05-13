
# ChatApp

### Overview

This project an online messaging service using Flask, similar in spirit to Slack. Users will be able to sign into this site with a display name, create channels (i.e. chatrooms) to communicate in, and join existing channels. Once a channel is selected, users will be able to send and receive messages with one another in real time and see history of old chats. 

### Installing

pip install virtualenv
virtualenv chatapp
cd chatapp
. chatcpp/bin/activate
pip install -r requirements.txt
export FLASK_APP=application.py
flask run
