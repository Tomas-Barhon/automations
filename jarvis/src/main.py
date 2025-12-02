# from src.agents.jarvis import JARVIS
# from src.speech.text_to_speech import TextToSpeach


def py_error_handler(filename, line, function, err, fmt):
    """Disabling audio warnings
    Credit to
    https://blog.yjl.im/2012/11/pyaudio-portaudio-and-alsa-messages.html
    for solving the warnings
    """
    pass


LISTEN = True


def main():
    """
    Main loop waiting for speech input.
    """
    # speech_recognition = SpeechRecognition()
    # recognizer = sr.Recognizer()
    # jarvis = JARVIS()
    # text_to_speach = TextToSpeach()
    # thread_id identifying my conversation
    # config = {"configurable": {"thread_id": "tomas_test"}}

    # while True:
    #    try:
    #        print("J.A.R.V.I.S. started")
    #        if LISTEN:
    # user_input = speech_recognition.transcribe_input(recognizer)
    # print("Received user input: ",user_input)
    # response = jarvis.send_prompt(
    #     messages = user_input, config = config
    # )
    #           response = jarvis.send_prompt(
    #                messages="Hey, do you know something about Barack Obama?",
    #                config=config,
    #            )
    #            text_to_speach.speak(response)
    #            break

    # except sr.RequestError as e:
    #    print(e)

    # except sr.UnknownValueError as e:
    #    print(e)
