#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import json
import operator
import argparse
import os
from api import API

API_KEY = ''
URL = ''
DIR_NAME = 'processed_files'


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'text-html')
        self.end_headers()

        message = "Hello World"
        self.wfile.write(bytes(message, "utf8"))
        return

    # POST
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()

        length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(length).decode('utf-8')
        post_body = json.loads(post_body)

        req_id = post_body['request_id']

        audio_name = req_id

        resp = post_body['response']
        if self.path.startswith('/denoise/emotion'):
            my_api = API(API_KEY, URL)
            filename = self.__denoise(audio_name, resp)
            my_api.get_emotion(filename)
            self.wfile.write(json.dumps(post_body).encode())
        elif self.path.startswith('/denoise'):
            self.__denoise(audio_name, resp)
            self.wfile.write(json.dumps(post_body).encode())
        elif self.path.startswith('/emotion'):
            emotions, sorted_emotions = self.__emotion(resp)
            print('emotion from audio:', audio_name)
            for item in sorted_emotions:
                print(item[0] + ':', item[1])
            self.wfile.write(json.dumps(post_body).encode())
        else:
            self.wfile.write(bytes("oi", "utf8"))
        return

    def __emotion(self, resp):
        emotions = dict()
        print(resp)
        for emotion in resp:
            emotions[emotion['emotion']] = emotion['score']
        sorted_emotions = sorted(
            emotions.items(), key=operator.itemgetter(1), reverse=True)

        return emotions, sorted_emotions

    def __denoise(self, audio_name, resp):
        audio_data = base64.b64decode(resp['content'])
        audio_encoding = resp['encoding']
        audio_language = resp['languageCode']
        audio_SR = resp['sampleRate']
        filename = (audio_name + "_" + audio_language +
                    '_' + audio_SR + '.' + audio_encoding)

        print(filename)

        if not os.path.exists(DIR_NAME):
            os.makedirs(DIR_NAME)
        filename = os.path.join(DIR_NAME, filename)

        with open(filename, 'wb') as f:
            f.write(audio_data)

        return filename


def startServer():
    parser = argparse.ArgumentParser(
        description='Servidor que cuida dos webhooks.')
    parser.add_argument('--key', '-k', type=str,
                        help='DeepAffects API KEY', required=True)
    parser.add_argument('--url', '-u', type=str,
                        help='webhook url', required=True)
    parser.add_argument('--port', '-p', type=int,
                        help='porta do servidor', required=False)

    args = parser.parse_args()
    global API_KEY
    global URL
    API_KEY = args.key
    URL = args.url
    porta = 8081
    if args.port is not None:
        porta = args.port
    print('starting server...')

    server_address = ("127.0.0.1", porta)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print('running server....')
    httpd.serve_forever()


startServer()
