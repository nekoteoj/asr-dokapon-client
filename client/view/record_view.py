import wx
from pubsub import pub


class RecordView(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, -1, "Dopapon ASR Client")
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "Threshold")
        ctrl = wx.TextCtrl(self, -1, "")
        record_button = wx.Button(self, -1, "Record")
        current_word = wx.StaticText(self, -1, "Current: -")
        status_text = wx.StaticText(self, -1, "status: Ready")

        font18 = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        font20 = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        current_word.SetFont(font20)
        record_button.SetFont(font18)
        status_text.SetFont(font18)

        sizer.Add(text, 0, wx.EXPAND | wx.ALL)
        sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL)
        sizer.Add(record_button, 0, wx.EXPAND | wx.ALL)
        sizer.Add(current_word, 0, wx.EXPAND | wx.ALL)
        sizer.Add(status_text, 0, wx.EXPAND | wx.ALL)

        # Bind Event
        ctrl.Bind(wx.EVT_TEXT, self.on_threshold_control_changed)
        record_button.Bind(wx.EVT_BUTTON, self.on_record_clicked)

        # Set element
        self.thresholdCtrl = ctrl
        self.thresholdText = text
        self.current_word = current_word
        self.status_text = status_text
        self.SetSizer(sizer)

        pub.subscribe(self.on_threshold_changed, "threshold_changed")
        pub.subscribe(self.on_status_changed, "status_changed")
        pub.subscribe(self.on_current_word, "current_word")

    def on_threshold_changed(self, threshold):
        self.thresholdText.SetLabelText("Threshold: " + str(threshold))

    def on_threshold_control_changed(self, event):
        if (self.thresholdCtrl.Value.isdigit()):
            pub.sendMessage("changing_threshold",
                            threshold=int(self.thresholdCtrl.Value))

    def on_status_changed(self, status):
        self.status_text.SetLabelText("status: " + status)

    def on_record_clicked(self, event):
        pub.sendMessage("record_audio")

    def on_current_word(self, word):
        self.current_word.SetLabelText("Current: " + word)

    def set_threshold_control_value(self, threshold):
        self.thresholdCtrl.SetValue(threshold)
