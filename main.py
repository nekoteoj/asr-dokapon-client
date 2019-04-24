import wx
from pubsub import pub
import threading

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

from recorder import recorder
from view.record_view import RecordView

useNotifyByWriteFile(sys.stdout)


class Model:
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


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = RecordView()
        self.view.on_threshold_changed(self.model.threshold)
        self.view.set_threshold_control_value(str(self.model.threshold))
        self.view.Show()

        pub.subscribe(self.set_threshold, "changing_threshold")
        pub.subscribe(self.record_audio, "record_audio")

    def set_threshold(self, threshold):
        self.model.set_threshold(threshold)

    def record_audio(self):
        self.model.record_audio()


def main():
    app = wx.App()
    c = Controller()
    sys.stdout = sys.__stdout__
    print('---- Starting main event loop ----')
    app.MainLoop()
    print('---- Exited main event loop ----')


if __name__ == "__main__":
    main()
