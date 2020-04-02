import win32clipboard
import win32con
from winelf import global_settings

class Clipboard():
    def __init__(
            self,
            charset=global_settings.CLIPBOARD_CHARSET,
    ):
        self.charest = charset

    def get(self):
        win32clipboard.OpenClipboard()
        try: text = win32clipboard.GetClipboardData(win32con.CF_TEXT).decode(self.charest, "ignore")
        except: text = ''
        win32clipboard.CloseClipboard()
        return text

    def set(self,content:str):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(content)
        win32clipboard.CloseClipboard()

    def clear(self):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()


