import wx

from pubsub.utils.notification import useNotifyByWriteFile
import sys

from client.controller.record_controller import RecordController

useNotifyByWriteFile(sys.stdout)


def main():
    app = wx.App()
    c = RecordController()
    sys.stdout = sys.__stdout__
    print('---- Starting main event loop ----')
    app.MainLoop()
    print('---- Exited main event loop ----')


if __name__ == "__main__":
    main()
