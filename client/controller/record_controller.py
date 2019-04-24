from pubsub import pub
from ..model.record_model import RecordModel
from ..view.record_view import RecordView


class RecordController:
    def __init__(self):
        self.model = RecordModel()
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
