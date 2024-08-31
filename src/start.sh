#!/bin/bash
#flask run --host=192.168.1.9
cd /srv/chat-doenca
waitress-serve --call app:start_app
