from pynput.keyboard import Key,KeyCode
from pynput.keyboard import Controller as KeyController

import time
from winelf import global_settings


# 动作延迟
def _keyboardSecurityDelay(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        # 前置延迟
        before_delay = kwargs.get('before_delay', self.settings['before_delay'])
        if before_delay: time.sleep(before_delay)
        # 执行动作
        ret = func(*args, **kwargs)
        # 后置颜值
        after_delay = kwargs.get('after_delay', self.settings['after_delay'])
        if after_delay: time.sleep(after_delay)
        # 返回动作结果
        return ret
    return wrapper


class KeyboardElf():
    def __init__(
            self,
            before_delay =  global_settings.KEYBOARD_BEFORE_DELAY,
            after_delay = global_settings.KEYBOARD_AFTER_DELAY,
            press_time = global_settings.KEYBOARD_PRESS_TIME,
            interval = global_settings.KEYBOARD_INTERVAL,
    ):
        self.keyboard = KeyController()
        self.settings = dict(
            before_delay = before_delay,
            after_delay = after_delay,
            press_time = press_time,
            interval = interval,
        )
    @_keyboardSecurityDelay
    def __keydown(self,key,**kwargs):
        self.keyboard.press(key)

    @_keyboardSecurityDelay
    def __keyup(self,key,**kwargs):
        self.keyboard.release(key)

    @_keyboardSecurityDelay
    def __press_key(self,key,press_time=None,num=1,interval=None,**kwargs):
        for i in range(num):
            self.keyboard.press(key)
            time.sleep(press_time or self.settings['press_time'])
            self.keyboard.release(key)
            if i < num -1:
                time.sleep(interval or self.settings['interval'])

    @_keyboardSecurityDelay
    def __press_key_with(self,key,pressed_key,press_time=None,num=1,interval=None,**kwargs):
        with self.keyboard.pressed(pressed_key):
            self.__press_key(key=key,press_time=press_time,num=num,interval=interval,**kwargs)

    def keydown(self,key,**kwargs):
        self.__keydown(key,**kwargs)

    def keyup(self,key,**kwargs):
        self.__keyup(key,**kwargs)

    def press_key(self,key,press_time=None,num=1,interval=None,**kwargs):
        self.__press_key(key=key,press_time=press_time,num=num,interval=interval,**kwargs)

    def press_up(self,press_time=None,num=1,interval=None,**kwargs):
        self.__press_key(key=Key.up,press_time=press_time,num=num,interval=interval,**kwargs)

    def press_down(self,press_time=None,num=1,interval=None,**kwargs):
        self.__press_key(key=Key.down,press_time=press_time,num=num,interval=interval,**kwargs)

    def press_left(self,press_time=None,num=1,interval=None,**kwargs):
        self.__press_key(key=Key.left,press_time=press_time,num=num,interval=interval,**kwargs)

    def press_right(self,press_time=None,num=1,interval=None,**kwargs):
        self.__press_key(key=Key.right,press_time=press_time,num=num,interval=interval,**kwargs)

    def press_enter(self,press_time=None,num=1,interval=None,**kwargs):
        self.__press_key(key=Key.enter,press_time=press_time,num=num,interval=interval,**kwargs)

    def press_delete(self,press_time=None,num=1,interval=None,**kwargs):
        self.__press_key(key=Key.delete,press_time=press_time,num=num,interval=interval,**kwargs)

    def press_key_with(self,key,pressed_key,press_time=None,num=1,interval=None,**kwargs):
        self.__press_key_with(key=key,pressed_key=pressed_key,press_time=press_time,num=num,interval=interval,**kwargs)

    def press_key_with_ctrl(self,key,press_time=None,num=1,interval=None,**kwargs):
        self.__press_key_with(key=key,pressed_key=Key.ctrl,press_time=press_time,num=num,interval=interval,**kwargs)

    def press_key_with_shift(self,key,press_time=None,num=1,interval=None,**kwargs):
        self.__press_key_with(key=key,pressed_key=Key.shift,press_time=press_time,num=num,interval=interval,**kwargs)

    def press_key_with_alt(self,key,press_time=None,num=1,interval=None,**kwargs):
        self.__press_key_with(key=key,pressed_key=Key.alt,press_time=press_time,num=num,interval=interval,**kwargs)






