import win32clipboard
import win32con
from winelf import global_settings

__all__ = ['Clipboard']


class Clipboard():
    def __init__(self, charset=global_settings.CLIPBOARD_CHARSET):
        # 剪贴板的编码
        self.charest = charset

    # 得到剪贴板的字符串内容
    def get(self) -> str:
        win32clipboard.OpenClipboard()
        try:
            text = win32clipboard.GetClipboardData(win32con.CF_TEXT).decode(self.charest, "ignore")
        except:
            text = ''
        win32clipboard.CloseClipboard()
        return text

    # 设置剪贴板的字符串内容
    def set(self, content: str):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(content)
        win32clipboard.CloseClipboard()

    # 清除剪贴板的字符串内容
    def clear(self):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
