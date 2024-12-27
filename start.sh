#!/bin/bash

# Install dependencies for Chrome
apt-get update
apt-get install -y wget curl unzip

# Download and install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt --fix-broken install -y

# Now run the Python script
python3 bot.py
