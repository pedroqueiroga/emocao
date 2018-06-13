import deepaffects
import operator
from deepaffects.rest import ApiException
from pprint import pprint
import ntpath


class API:
    def __init__(self, api_key, url):
        self.API_KEY = api_key
        self.URL = url.strip('/')

    def denoise(self, AUDIO_PATH, emotion=False):
        # Configure API key authorization: UserSecurity
        deepaffects.configuration.api_key['apikey'] = self.API_KEY
        # create an instance of the API class
        api_instance = deepaffects.DenoiseApi()
        # Audio | Audio Object that needs to be denoised.
        body = deepaffects.Audio.from_file(AUDIO_PATH)
        # str | The Webhook url where result from async resource is posted
        webhook = self.URL + '/denoise'
        if emotion:
            webhook = webhook + '/emotion'
        # str | Unicode identifier for the request (optional)
        request_id = self.__path_leaf(AUDIO_PATH)

        try:
            # Denoise an audio file
            api_response = api_instance.async_denoise_audio(
                body, webhook, request_id=request_id)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling DenoiseApi -> async_denoise_audio: %s\n" % e)

    def get_emotion(self, AUDIO_PATH):
        # Configure API key authorization: UserSecurity
        deepaffects.configuration.api_key['apikey'] = self.API_KEY
        # create an instance of the API class
        api_instance = deepaffects.EmotionApi()
        # Audio | Audio Object that needs to be denoised.
        body = deepaffects.Audio.from_file(AUDIO_PATH)
    # str | The Webhook url where result from async resource is posted
        webhook = self.URL + '/emotion'
        # str | Unicode identifier for the request (optional)
        request_id = self.__path_leaf(AUDIO_PATH)

        try:
            # Get emotions from an audio file
            api_response = api_instance.sync_recognise_emotion(body)
            emotions = dict()
            for emotion in api_response:
                emotions[emotion.emotion] = emotion.score
            sorted_emotions = sorted(
                emotions.items(), key=operator.itemgetter(1), reverse=True)
            for item in sorted_emotions:
                print(item[0] + ':', item[1])
        except ApiException as e:
            print(
                "Exception when calling EmotionApi -> sync_recognise_emotion: %s\n" % e)

    def __path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)
