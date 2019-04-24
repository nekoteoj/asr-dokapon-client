from pubsub import pub
from ..recorder import recorder
import threading


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

            def run(self):
                pub.sendMessage("status_changed", status="Recording")
                recorder.record_to_file("speak.wav")
                pub.sendMessage("status_changed", status="Ready")

        recordThread = RecordThread(1)
        recordThread.start()
