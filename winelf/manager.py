from winelf.mouse import MouseElf
from winelf.mouse import Button as MouseButton
from winelf.keyboard import KeyboardElf, Key
from winelf.clipboard import ClipboardElf
from winelf.window import WindowElf
import win32gui
import numpy as np
import time
import win32con


def set_window_foreground(hwnd, block=True, timeout=5):
    start_timestamp = time.time()
    # 如果前置窗口就是hwnd,不发送消息，直接返回True
    foreground_hwnd = win32gui.GetForegroundWindow()
    if foreground_hwnd == hwnd:
        return True
    while True:
        # 将hwnd至于顶层
        try:
            win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            win32gui.SetForegroundWindow(hwnd)
            win32gui.BringWindowToTop(hwnd)
        except:
            pass
        # 得到当前顶层窗口
        foreground_hwnd = win32gui.GetForegroundWindow()
        # 如果当前顶层窗口=hwnd，返回True
        if foreground_hwnd == hwnd:
            return True
        else:
            # 如果等待时间超过了timeout，报异常
            current_timestamp = time.time()
            if current_timestamp - start_timestamp > timeout:
                raise Exception('无法将窗口至于顶层')


def windowForegroundWrapper(func):
    def wrapper(*args, **kwargs):
        hwnd = args[0].hwnd
        set_window_foreground(hwnd=hwnd)
        return func(*args, **kwargs)

    return wrapper


class Mouse(MouseElf):
    def __init__(self, hwnd, **kwargs):
        MouseElf.__init__(self, **kwargs)
        self.hwnd = hwnd

    # 根据指定了hwnd返回position,size
    def __get_positions(self):
        try:
            left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
            position_start = (left, top)
            position_end = (right, bot)
            return position_start, position_end
        except:
            return Exception('窗口不存在')

    def point_to_absolute(self, point_relative, clip=True):
        position_start, position_end = self.__get_positions()

        if clip:
            position_start_array = np.array(position_start)
            position_end_array = np.array(position_end)

            point_absolute = np.clip(
                np.array(point_relative) + position_start_array,
                position_start_array,
                position_end_array
            )
            return point_absolute.tolist()
        else:
            point_absolute = (position_start[0] + point_relative[0], position_start[1] + point_relative[1])
            return point_absolute

    def point_to_relative(self, point_absolute, clip=True):
        position_start, position_end = self.__get_positions()
        size = (position_end[0] - position_start[0], position_end[1] - position_start[1])
        if clip:
            position_start_array = np.array(position_start)
            size_array = np.array(size)
            point_absolute_array = np.array(point_absolute)
            point_relative = np.clip(
                point_absolute_array - position_start_array,
                np.array([0, 0]),  # 最小不能为负
                size_array,  # 最大不能超过尺寸
            )
            return point_relative.tolist()
        else:
            point_relative = point_absolute[0] - position_start[0], point_absolute[1] - position_start[1]
            return point_relative

    @windowForegroundWrapper
    def click_left(self, press_time=None, **kwargs):
        return MouseElf.click_left(self, press_time=press_time, **kwargs)

    @windowForegroundWrapper
    def click_right(self, press_time=None, **kwargs):
        return MouseElf.click_right(self, press_time=press_time, **kwargs)

    @windowForegroundWrapper
    def click_middle(self, press_time=None, **kwargs):
        return MouseElf.click_middle(self, press_time=press_time, **kwargs)

    @windowForegroundWrapper
    def click_db_left(self, press_time=None, interval=None, **kwargs):
        return MouseElf.click_db_left(self, press_time=press_time, interval=interval, **kwargs)

    @windowForegroundWrapper
    def click_db_right(self, press_time=None, interval=None, **kwargs):
        return MouseElf.click_db_right(self, press_time=press_time, interval=interval, **kwargs)

    @windowForegroundWrapper
    def click_db_middle(self, press_time=None, interval=None, **kwargs):
        return MouseElf.click_db_middle(self, press_time=press_time, interval=interval, **kwargs)

    @windowForegroundWrapper
    def move(self, point, point_start=None, speed=None, **kwargs):
        # 从相对转化绝对位置
        point = self.point_to_absolute(point)
        if point_start:
            point_start = self.point_to_absolute(point_start)

        return MouseElf.move(self, point=point, point_start=point_start, speed=speed, **kwargs)

    @windowForegroundWrapper
    def move_l(self, point, point_start=None, speed=None, press_time=None, num=1, interval=None, **kwargs):
        # 从相对转化绝对位置
        point = self.point_to_absolute(point)
        if point_start:
            point_start = self.point_to_absolute(point_start)

        return MouseElf.move_l(self, point=point, point_start=point_start, speed=speed, press_time=press_time, num=num,
                               interval=interval, **kwargs)

    @windowForegroundWrapper
    def move_r(self, point, point_start=None, speed=None, press_time=None, num=1, interval=None, **kwargs):
        # 从相对转化绝对位置
        point = self.point_to_absolute(point)
        if point_start:
            point_start = self.point_to_absolute(point_start)

        return MouseElf.move_r(self, point=point, point_start=point_start, speed=speed, press_time=press_time, num=num,
                               interval=interval, **kwargs)

    @windowForegroundWrapper
    def move_m(self, point, point_start=None, speed=None, press_time=None, num=1, interval=None, **kwargs):
        # 从相对转化绝对位置
        point = self.point_to_absolute(point)
        if point_start:
            point_start = self.point_to_absolute(point_start)

        return MouseElf.move_m(self, point=point, point_start=point_start, speed=speed, press_time=press_time, num=num,
                               interval=interval, **kwargs)

    @windowForegroundWrapper
    def move_relative(self, deviation, point_start=None, speed=None, **kwargs):
        if point_start:
            point_start = self.point_to_absolute(point_start)
        else:
            point_start = self.mouse.position
        return MouseElf.move_relative(self, deviation=deviation, point_start=point_start, speed=None, **kwargs)

    @windowForegroundWrapper
    def move_relative_l(self, deviation, point_start=None, speed=None, press_time=None, num=1, interval=None,
                        **kwargs):

        if point_start:
            point_start = self.point_to_absolute(point_start)
        else:
            point_start = self.mouse.position
        return MouseElf.move_relative_l(self, deviation=deviation, point_start=point_start, speed=None,
                                        press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def move_relative_r(self, deviation, point_start=None, speed=None, press_time=None, num=1, interval=None,
                        **kwargs):

        if point_start:
            point_start = self.point_to_absolute(point_start)
        else:
            point_start = self.mouse.position
        return MouseElf.move_relative_r(self, deviation=deviation, point_start=point_start, speed=None,
                                        press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def move_relative_m(self, deviation, point_start=None, speed=None, press_time=None, num=1, interval=None,
                        **kwargs):

        if point_start:
            point_start = self.point_to_absolute(point_start)
        else:
            point_start = self.mouse.position
        return MouseElf.move_relative_m(self, deviation=deviation, point_start=point_start, speed=None,
                                        press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def select_l(self, point, point_start=None, speed=None, **kwargs):
        point = self.point_to_absolute(point)
        if point_start:
            point_start = self.point_to_absolute(point_start)
        return MouseElf.select_l(self, point=point, point_start=point_start, speed=speed, **kwargs)

    @windowForegroundWrapper
    def select_r(self, point, point_start=None, speed=None, **kwargs):
        point = self.point_to_absolute(point)
        if point_start:
            point_start = self.point_to_absolute(point_start)
        return MouseElf.select_r(self, point=point, point_start=point_start, speed=speed, **kwargs)

    @windowForegroundWrapper
    def select_m(self, point, point_start=None, speed=None, **kwargs):
        point = self.point_to_absolute(point)
        if point_start:
            point_start = self.point_to_absolute(point_start)
        return MouseElf.select_m(self, point=point, point_start=point_start, speed=speed, **kwargs)


class Keyboard(KeyboardElf):
    def __init__(self, hwnd, **kwargs):
        KeyboardElf.__init__(self, **kwargs)
        self.hwnd = hwnd

    @windowForegroundWrapper
    def keydown(self, key, **kwargs):
        return KeyboardElf.keydown(self, key=key, **kwargs)

    @windowForegroundWrapper
    def keyup(self, key, **kwargs):
        return KeyboardElf.keyup(self, key=key, **kwargs)

    @windowForegroundWrapper
    def press_key(self, key, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_key(key=key, press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_up(self, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_up(press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_down(self, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_down(press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_left(self, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_left(press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_right(self, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_right(press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_esc(self, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_esc(press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_backspace(self, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_backspace(press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_insert(self, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_insert(press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_key_with(self, key, pressed_key, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_key_with(self, key=key, pressed_key=pressed_key, press_time=press_time, num=num,
                                          interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_key_with_ctrl(self, key, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_key_with_ctrl(self, key=key, press_time=press_time, num=num, interval=interval,
                                               **kwargs)

    @windowForegroundWrapper
    def press_key_with_shift(self, key, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_key_with_shift(self, key=key, press_time=press_time, num=num, interval=interval,
                                                **kwargs)

    @windowForegroundWrapper
    def press_key_with_alt(self, key, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_key_with_alt(self, key=key, press_time=press_time, num=num, interval=interval,
                                              **kwargs)

    @windowForegroundWrapper
    def press_c_with_ctrl(self, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_c_with_ctrl(self, press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_v_with_ctrl(self, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_v_with_ctrl(self, press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_z_with_ctrl(self, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_z_with_ctrl(self, press_time=press_time, num=num, interval=interval, **kwargs)

    @windowForegroundWrapper
    def press_x_with_ctrl(self, press_time=None, num=1, interval=None, **kwargs):
        return KeyboardElf.press_x_with_ctrl(self, press_time=press_time, num=num, interval=interval, **kwargs)


from winelf import image as wimage


class Image():
    def __init__(self, hwnd):
        self.hwnd = hwnd

    # 根据指定了hwnd返回position,size
    def __get_positions(self):
        try:
            left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
            position_start = (left, top)
            position_end = (right, bot)
            return position_start, position_end
        except:
            return Exception('窗口不存在')

    def point_to_absolute(self, point_relative, clip=True):
        position_start, position_end = self.__get_positions()

        if clip:
            position_start_array = np.array(position_start)
            position_end_array = np.array(position_end)

            point_absolute = np.clip(
                np.array(point_relative) + position_start_array,
                position_start_array,
                position_end_array
            )
            return point_absolute.tolist()
        else:
            point_absolute = (position_start[0] + point_relative[0], position_start[1] + point_relative[1])
            return point_absolute

    def point_to_relative(self, point_absolute, clip=True):
        position_start, position_end = self.__get_positions()
        size = (position_end[0] - position_start[0], position_end[1] - position_start[1])
        if clip:
            position_start_array = np.array(position_start)
            size_array = np.array(size)
            point_absolute_array = np.array(point_absolute)
            point_relative = np.clip(
                point_absolute_array - position_start_array,
                np.array([0, 0]),  # 最小不能为负
                size_array,  # 最大不能超过尺寸
            )
            return point_relative.tolist()
        else:
            point_relative = point_absolute[0] - position_start[0], point_absolute[1] - position_start[1]
            return point_relative

    def to_digital(self, img):
        return wimage.to_digital(img)

    # 指定左顶点，大小进行截图，如果传递save_path，为图片保存路径
    def screenshot(self, position=None, size=None, save_path=None, digital=False):
        position_start, position_end = self.__get_positions()
        window_size = position_end[0] - position_start[0], position_end[1] - position_start[1]
        if not position:  # 如果没有位置，为窗口的左上顶点
            position = position_start
        else:  # 如果输入位置，转化为绝对位置
            position = self.point_to_absolute(position)
        if not size:  # 如果没有size，指定为window的尺寸
            size = window_size
        return wimage.screenshot(position=position, size=size, save_path=save_path, digital=digital)

    # 读取src路径的图片，在范围中所有返回所有匹配到图片的中心位置
    def search_imgs(self, imgs, position=None, size=None, confidence=0.8, block=False, timeout=5):
        position_start, position_end = self.__get_positions()
        window_size = position_end[0] - position_start[0], position_end[1] - position_start[1]
        if not position:  # 如果没有位置，为窗口的左上顶点
            position = position_start
        else:  # 如果输入位置，转化为绝对位置
            position = self.point_to_absolute(position)
        if not size:  # 如果没有size，指定为window的尺寸
            size = window_size
        return wimage.search_imgs(imgs=imgs, position=position, size=size, confidence=confidence, block=block,
                                  timeout=timeout)

    # 读取src路径的图片，在范围中所有返回第一个匹配到图片的中心位置
    def search_img(self, imgs, position=None, size=None, confidence=0.8, block=False, timeout=5):
        position_start, position_end = self.__get_positions()
        window_size = position_end[0] - position_start[0], position_end[1] - position_start[1]
        if not position:  # 如果没有位置，为窗口的左上顶点
            position = position_start
        else:  # 如果输入位置，转化为绝对位置
            position = self.point_to_absolute(position)
        if not size:  # 如果没有size，指定为window的尺寸
            size = window_size
        return wimage.search_img(imgs=imgs, position=position, size=size, confidence=confidence, block=block,
                                 timeout=timeout)

    # 屏幕内容转文字
    def screen_to_word(self, position=None, size=None, block=False, timeout=5):
        position_start, position_end = self.__get_positions()
        window_size = position_end[0] - position_start[0], position_end[1] - position_start[1]
        if not position:  # 如果没有位置，为窗口的左上顶点
            position = position_start
        else:  # 如果输入位置，转化为绝对位置
            position = self.point_to_absolute(position)
        if not size:  # 如果没有size，指定为window的尺寸
            size = window_size
        return wimage.screen_to_word(position=position, size=size, block=block, timeout=timeou)


class Clipboard(ClipboardElf):
    def __init__(self, mouse: Mouse, keyboard: Keyboard, **kwargs):
        ClipboardElf.__init__(self, **kwargs)
        self.__mouse = mouse
        self.__keyboard = keyboard

    def write_content(self, content, point=None, clear=False):
        # 如果有位置，鼠标点击位置
        if point:
            self.__mouse.move_l(point)
            # 如果需要清空
            if clear:
                self.__keyboard.press_key_with_ctrl(key='a')
                self.__keyboard.press_delete()
        # 设置剪贴板
        self.set(content)
        # 粘贴
        self.__keyboard.press_key_with_ctrl(key='v')

    def get_content_all(self, point):
        # 点击
        self.__mouse.move_l(point)
        # 全选
        self.__keyboard.press_key_with_ctrl('a')
        # 复制
        self.__keyboard.press_key_with_ctrl('c')
        return self.get()

    def get_content_with_select(self, point_start, point_end, speed=None, **kwargs):
        self.__mouse.select_l(point=point_end, point_start=point_start, speed=speed, **kwargs)
        # 复制
        self.__keyboard.press_key_with_ctrl('c')
        return self.get()


class WindowManager():
    def __init__(self, hwnd=None, title=None, foreground=False):
        self.window = WindowElf(hwnd=hwnd,title=title,foreground=foreground)
        self.hwnd = self.window.hwnd
        self.mouse = Mouse(hwnd=self.hwnd)
        self.keyboard = Keyboard(hwnd=self.hwnd)
        self.image = Image(hwnd=self.hwnd)
        self.clipboard = Clipboard(mouse=self.mouse,keyboard=self.keyboard)



if __name__ == '__main__':
    wm = WindowManager(foreground=True)

    print(wm.window.title)
    wm.mouse.move((200,200))
    wm.window.position = (200,200)
    wm.clipboard.write_content('aaaa')

    wm.image.screenshot(save_path='3.pngaaaa')