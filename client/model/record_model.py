from pubsub import pub
from ..recorder import recorder
import threading
import subprocess
import requests


GETDATA = "http://localhost:3000/getdata"
KEYBOARD = "http://192.168.43.75:3000/keyboard"


class RecordModel:
    def __init__(self):
        self.set_threshold(3000)

    def set_threshold(self, threshold):
        self.threshold = threshold
        pub.sendMessage("threshold_changed", threshold=self.threshold)
        recorder.set_threshold(threshold)

    def record_audio(self):
        class RecordThread (threading.Thread):
            def __init__(self, threadID):
                threading.Thread.__init__(self)
                self.threadID = threadID
            
            def speech_to_text(self):
                word = subprocess.check_output([
                    "python", "sender.py", "-u",
                    "ws://localhost:8080/client/ws/speech",
                    "-r", "32000", "speak.wav"
                ])
                data = " ".join(word.decode("utf-8").split()[:-1])
                pub.sendMessage("current_word", word="".join(data.split()))
                pub.sendMessage("status_changed", status="Processing")
                return data

            def text_to_command(self, data):
                response = requests.get(
                    url=GETDATA,
                    params={"sentence": data}
                )
                command = response.json()
                pub.sendMessage("current_word", word=command["command"])
                pub.sendMessage("status_changed", status="Ready")
                return command

            def command_to_keyboard(self, command_id):
                response = requests.post(
                    KEYBOARD,
                    {"command": command_id}
                )

            def run(self):
                recorder.record_to_file("speak.wav")
                data = self.speech_to_text()
                command = self.text_to_command(data)
                self.command_to_keyboard(command["command_id"])

        pub.sendMessage("status_changed", status="Recording")
        recordThread = RecordThread(1)
        recordThread.start()
