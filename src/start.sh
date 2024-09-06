#!/bin/bash
cd /srv/chat-doenca
waitress-serve --call app:start_app
