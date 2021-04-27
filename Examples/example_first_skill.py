# Add mistyPy directory to sys path
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mistyPy.Robot import Robot
from mistyPy.Events import Events


def start_skill():
    misty.RegisterEvent("initTTSComplete", Events.TextToSpeechComplete, keep_alive=False, callback_function=tts_intro_completed)

    misty.DisplayImage("e_defaultcontent.jpg")
    misty.MoveHead(0, 0, 0, 85)
    misty.Speak("I'd like to show you an image and have you tell me what you see.", None, None, None, True, "tts-content")

def tts_intro_completed(event):
    misty.DisplayImage("inkblot.jpg")
    # keep_alive defaults to false
    misty.RegisterEvent("whatDoYouSeeTTSComplete", Events.TextToSpeechComplete, callback_function=tts_what_do_you_see_completed)
    misty.Speak("What do you see when you look at this image?", None, None, None, True, "tts-content")

def tts_what_do_you_see_completed(event):
    misty.RegisterEvent("VoiceRecord", Events.VoiceRecord, callback_function=voice_record_complete)
    misty.CaptureSpeechAzure(True, 2000, 15000, False, False, "en-us", "<azure_cognitive_services_key>", "eastus")

def voice_record_complete(event):
    if "message" in event:
        parsed_message = event["message"]
        misty_heard = parsed_message["speechRecognitionResult"]
        print(f"Misty heard: {misty_heard}")
    # do something with this data
    misty.DisplayImage("e_defaultcontent.jpg")
    misty.MoveHead(-30, 20, -50, 85, None, None)
    misty.RegisterEvent("finalTTSComplete", Events.TextToSpeechComplete, callback_function=tts_all_i_ever_see)
    misty.Speak("That's interesting. All I ever see is a butterfly.", None, None, None, True, "tts-content")

def tts_all_i_ever_see(self, event):
    misty.DisplayImage("e_joy.jpg")


if __name__ == "__main__":
    ipAddress = "192.168.1.12"
    misty = Robot(ipAddress)
    start_skill()
