import wx
from pubsub import pub


class RecordView(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, -1, "Dopapon ASR Client")
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "Threshold")
        ctrl = wx.TextCtrl(self, -1, "")
        record_button = wx.Button(self, -1, "Record")
        sizer.Add(text, 0, wx.EXPAND | wx.ALL)
        sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL)
        sizer.Add(record_button, 0, wx.EXPAND | wx.ALL)

        # Bind Event
        ctrl.Bind(wx.EVT_TEXT, self.on_threshold_control_changed)
        record_button.Bind(wx.EVT_BUTTON, self.on_record_clicked)

        # Set element
        self.thresholdCtrl = ctrl
        self.thresholdText = text
        self.SetSizer(sizer)

        self.config_status_bar()

        pub.subscribe(self.on_threshold_changed, "threshold_changed")
        pub.subscribe(self.on_status_changed, "status_changed")

    def config_status_bar(self):
        self.statusbar = self.CreateStatusBar(1)
        self.on_status_changed("Ready")

    def on_threshold_changed(self, threshold):
        self.thresholdText.SetLabelText("Threshold: " + str(threshold))

    def on_threshold_control_changed(self, event):
        if (self.thresholdCtrl.Value.isdigit()):
            pub.sendMessage("changing_threshold",
                            threshold=int(self.thresholdCtrl.Value))

    def on_status_changed(self, status):
        self.statusbar.SetStatusText("status: " + status)

    def on_record_clicked(self, event):
        pub.sendMessage("record_audio")

    def set_threshold_control_value(self, threshold):
        self.thresholdCtrl.SetValue(threshold)
