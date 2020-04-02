from pynput.keyboard import Key, KeyCode
from pynput.keyboard import Controller as KeyController
import time
from winelf import global_settings

__all__ = ['Key', 'KeyboardElf']


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
    '''
    num:按键次数
    interval:按键的时间间隔
    '''
    def __init__(
            self,
            before_delay=global_settings.KEYBOARD_BEFORE_DELAY,  # 前置延时
            after_delay=global_settings.KEYBOARD_AFTER_DELAY,  # 后置延时
            press_time=global_settings.KEYBOARD_PRESS_TIME,  # 按键时间
            interval=global_settings.KEYBOARD_INTERVAL,  # 连续按键间隔
    ):
        self.settings = dict(
            before_delay=before_delay,
            after_delay=after_delay,
            press_time=press_time,
            interval=interval,
        )
        self.keyboard = KeyController()

    # 按住key
    @_keyboardSecurityDelay
    def __keydown(self, key, **kwargs):
        self.keyboard.press(key)

    # 弹起key
    @_keyboardSecurityDelay
    def __keyup(self, key, **kwargs):
        self.keyboard.release(key)

    # 按下后抬起key
    @_keyboardSecurityDelay
    def __press_key(self, key, press_time=None, num=1, interval=None, **kwargs):
        for i in range(num):
            self.keyboard.press(key)
            time.sleep(press_time or self.settings['press_time'])
            self.keyboard.release(key)
            if i < num - 1:
                time.sleep(interval or self.settings['interval'])

    # 按住pressed_key不松开，按键key，在key弹起后，弹起pressed_key
    @_keyboardSecurityDelay
    def __press_key_with(self, key, pressed_key, press_time=None, num=1, interval=None, **kwargs):
        with self.keyboard.pressed(pressed_key):
            self.__press_key(key=key, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按下key
    def keydown(self, key, **kwargs):
        self.__keydown(key, **kwargs)

    # 弹起key
    def keyup(self, key, **kwargs):
        self.__keyup(key, **kwargs)

    # 按键key
    def press_key(self, key, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=key, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按键up
    def press_up(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=Key.up, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按键down
    def press_down(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=Key.down, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按键left
    def press_left(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=Key.left, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按键right
    def press_right(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=Key.right, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按键enter
    def press_enter(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=Key.enter, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按键delete
    def press_delete(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=Key.delete, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按键esc
    def press_esc(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=Key.esc, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按键tab
    def press_tab(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=Key.tab, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按键space
    def press_space(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=Key.space, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按键backspace
    def press_backspace(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=Key.backspace, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按键insert
    def press_insert(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key(key=Key.insert, press_time=press_time, num=num, interval=interval, **kwargs)

    # 按住pressed_key，然后按键key，结束后弹起pressed_key
    def press_key_with(self, key, pressed_key, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key_with(key=key, pressed_key=pressed_key, press_time=press_time, num=num, interval=interval,
                              **kwargs)

    # 按住ctrl,按键key,弹起ctrl
    def press_key_with_ctrl(self, key, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key_with(key=key, pressed_key=Key.ctrl, press_time=press_time, num=num, interval=interval,
                              **kwargs)

    # 按住shift,按键key,弹起shift
    def press_key_with_shift(self, key, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key_with(key=key, pressed_key=Key.shift, press_time=press_time, num=num, interval=interval,
                              **kwargs)

    # 按住alt,按键key,弹起alt
    def press_key_with_alt(self, key, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key_with(key=key, pressed_key=Key.alt, press_time=press_time, num=num, interval=interval, **kwargs)

    # ctrl + c
    def press_c_with_ctrl(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key_with(key='c', pressed_key=Key.ctrl, press_time=press_time, num=num, interval=interval,
                              **kwargs)

    # ctrl + v
    def press_v_with_ctrl(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key_with(key='v', pressed_key=Key.ctrl, press_time=press_time, num=num, interval=interval,
                              **kwargs)

    # ctrl + z
    def press_z_with_ctrl(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key_with(key='z', pressed_key=Key.ctrl, press_time=press_time, num=num, interval=interval,
                              **kwargs)

    # ctrl + x
    def press_x_with_ctrl(self, press_time=None, num=1, interval=None, **kwargs):
        self.__press_key_with(key='x', pressed_key=Key.ctrl, press_time=press_time, num=num, interval=interval,
                              **kwargs)

if __name__ == '__main__':
    k = KeyboardElf()
