#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

The Google Assistant Library can be installed with:
    env/bin/pip install google-assistant-library==0.0.2

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import subprocess
import sys

import aiy.assistant.auth_helpers
import aiy.assistant.device_helpers
import aiy.audio
import aiy.voicehat
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))

def stream_npr():
    aiy.audio.say('Streaming NPR')
    subprocess.call('cvlc https://www.npr.org//streams//mp3//nprlive24.m3u', shell=True)

def stream_top40():
    aiy.audio.say('Streaming top40')
    subprocess.call('cvlc http://icy.ihrcast.arn.com.au/1065.mp3', shell=True)

def stream_jazz():
    aiy.audio.say('Streaming jazz')
    subprocess.call('cvlc http://eastsidestreamer.myradio.click:8000/stream', shell=True)

def stream_classical():
    aiy.audio.say('Streaming classical')
    subprocess.call('cvlc http://eno.emit.com:8000/2mbs_live_128.mp3', shell=True)

def stream_kissfm():
    aiy.audio.say('Streaming kiss FM')
    subprocess.call('cvlc http://c2icy.prod.playlists.ihrhls.com/185_icy', shell=True)

def stream_cebu():
    aiy.audio.say('Streaming cebu')
    subprocess.call('cvlc http://icecast.eradioportal.com:8000/rxcebu', shell=True)

def stream_hamburg():
    aiy.audio.say('Streaming Radio Hamburg')
    subprocess.call('cvlc http://stream.radiohamburg.de/koffeinkick/mp3-128', shell=True)

def stream_germantechno():
    aiy.audio.say('Streaming German Techno')
    subprocess.call('cvlc http://listen.pioneerdjradio.com:8550/', shell=True)

def stream_frenchcarib():
    aiy.audio.say('Streaming French Caribbean')
    subprocess.call('cvlc http://intertropical.vestaradio.com/listen.pls', shell=True)

def stream_hawaiian():
    aiy.audio.say('Streaming Hawaiian')
    subprocess.call('cvlc http://s3.voscast.com:8662/', shell=True)

def stream_nigerian():
    aiy.audio.say('Streaming Nigerian')
    subprocess.call('cvlc http://listen.radionomy.com/rnbhitsradio-afrobeatsnaija1', shell=True)

def stream_russian():
    aiy.audio.say('Streaming Russian Dance')
    subprocess.call('cvlc http://air2.radiorecord.ru:805/rr_320', shell=True)

def stream_bbcworld():
    aiy.audio.say('Streaming BBC World')
    subprocess.call('cvlc http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-eieuk', shell=True)

def stream_kcrw():
    aiy.audio.say('Streaming KCRW Eclectic')
    subprocess.call('cvlc http://www.kcrw.com/pls/kcrwmusic.pls', shell=True)

def start_kodi():
    aiy.audio.say('Starting Kodi')
    subprocess.call('kodi', shell=True)

def start_vpn():
    aiy.audio.say('Starting VPN')
    subprocess.call('unuhi-b-udp-443-config.ovpn &', shell=True)

def stop_vpn():
    subprocess.call('pkill openvpn', shell=True)
    aiy.audio.say('VPN Stopped')


def on_button_pressed():
    subprocess.call('pkill vlc', shell=True)
    aiy.audio.say('Stream Stopped')


def process_event(assistant, event):
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        aiy.voicehat.get_button().on_press(on_button_pressed)
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'internal ip address':
            assistant.stop_conversation()
            say_ip()
        elif text == 'start kodi':
            assistant.stop_conversation()
            start_kodi()
        elif text == 'start vpn':
            assistant.stop_conversation()
            start_vpn()
        elif text == 'stop vpn':
            assistant.stop_conversation()
            stop_vpn()
        elif text == 'stream npr':
            assistant.stop_conversation()
            stream_npr()
        elif text == 'stream top 40':
            assistant.stop_conversation()
            stream_top40()
        elif text == 'stream jazz':
            assistant.stop_conversation()
            stream_jazz()
        elif text == 'stream classical':
            assistant.stop_conversation()
            stream_classical()
        elif text == 'stream kiss':
            assistant.stop_conversation()
            stream_kissfm()
        elif text == 'stream cebu':
            assistant.stop_conversation()
            stream_cebu()
        elif text == 'stream radio hamburg':
            assistant.stop_conversation()
            stream_hamburg()
        elif text == 'stream german techno':
            assistant.stop_conversation()
            stream_germantechno()
        elif text == 'stream french caribbean':
            assistant.stop_conversation()
            stream_frenchcarib()
        elif text == 'stream hawaiian':
            assistant.stop_conversation()
            stream_hawaiian()
        elif text == 'stream nigerian':
            assistant.stop_conversation()
            stream_nigerian()
        elif text == 'stream russian dance':
            assistant.stop_conversation()
            stream_russian()
        elif text == 'stream bbc world':
            assistant.stop_conversation()
            stream_bbcworld()
        elif text == 'stream eclectic':
            assistant.stop_conversation()
            stream_kcrw()


    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    model_id, device_id = aiy.assistant.device_helpers.get_ids(credentials)
    with Assistant(credentials, model_id) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
