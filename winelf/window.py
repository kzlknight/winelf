import numpy as np
import pyautogui
import time
import win32gui
from winelf import global_settings
import win32con


def blockWrapper(block=True, timeout=5):
    def wrapper1(func):
        def wrapper2(*args, **kwargs):
            # 堵塞
            if not block:
                return func(*args, **kwargs)
            # 不堵塞
            else:
                start_timestamp = int(time.time())
                while True:
                    ret = func(*args, **kwargs)
                    if ret:
                        return ret
                    current_timestamp = int(time.time())
                    if current_timestamp - start_timestamp >= timeout:
                        return ret

        return wrapper2

    return wrapper1


class WindowElf():
    def __init__(self, hwnd=None, title=None, foreground=False, window_manager=True):
        '''
        例子：
            1.指定句柄:
                windowElf = WindowElf(hwnd=123)
            2.指定title
                windowElf = WindowElf(title='mytitle') or windowElf = WindowElf(title=['mytitle1','mytitle2])
            3.最上层的应用
                windowElf = WindowElf(foreground=True)
            4.桌面句柄
                windowElf = WindowElf() or windowElf = WindowElf(window_manager=True)
            5.空句柄
                windowElf = WindowElf(window_manager=False)
        '''
        self.settings = dict(
            manage_timeout=global_settings.WINDOW_MANAGE_TIMEOUT,  # window操作的默认最大堵塞时间
            new_build_timeout=global_settings.WINDOW_NEW_BUILD_TIMEOUT,  # 与新窗口创建有关的最大堵塞时间
        )
        if hwnd:
            self.hwnd = hwnd
        elif title:
            window_data = self.get_window_data(titles=title)
            self.hwnd = window_data['hwnd']
        elif foreground:
            window_data = self.get_window_data_foreground()
            self.hwnd = window_data['hwnd']
        elif window_manager:
            window_data = self.get_window_data(titles=global_settings.WINDOW_TITLE)
            self.hwnd = window_data['hwnd']
        else:
            self.hwnd = None

    # 获取实时的title
    @property
    def title(self):
        return win32gui.GetWindowText(self.hwnd)

    # 获取实时的position
    @property
    def position(self):
        position, size = self.get_postion_size(self.hwnd)
        return position

    # 改变window的位置
    @position.setter
    def position(self, value):
        position, size = self.get_postion_size(self.hwnd)
        win32gui.SetWindowPos(
            self.hwnd,
            win32con.HWND_TOPMOST,
            value[0], value[1],
            size[0], size[1],
            win32con.SWP_SHOWWINDOW
        )

    # 得到window的尺寸
    @property
    def size(self):
        position, size = self.get_postion_size(self.hwnd)
        return size

    # 设置window的尺寸
    @size.setter
    def size(self, value):
        position, size = self.get_postion_size(self.hwnd)
        win32gui.SetWindowPos(
            self.hwnd,
            win32con.HWND_TOPMOST,
            position[0], position[1],
            value[0], value[1],
            win32con.SWP_SHOWWINDOW
        )

    # 根据指定了hwnd返回position,size
    def get_postion_size(self, hwnd=None):
        '''
        :param hwnd:默认为self.hwnd
        :return:None|(position,size)
        '''
        if not hwnd: hwnd = self.hwnd
        try:
            left, top, right, bot = win32gui.GetWindowRect(hwnd)
            position = (left, top)
            size = (right - left), (bot - top)
            return position, size
        except:
            return None

    # 改变window的位置与大小,改变后会进行验证
    def set_position_size(self, position=None, size=None, block=True, timeout=None):
        '''
        :return: True|False 表示操作的结果
        '''
        if block and not timeout:
            timeout = self.settings['manage_timeout']
        # 当前的位置与尺寸
        current_position, current_size = self.get_postion_size()
        # 结果位置与尺寸，参数position或size如果输入为None,表示不改变
        target_position = position or current_position
        target_size = size or current_size
        # 发送修改消息
        win32gui.SetWindowPos(
            self.hwnd,
            win32con.HWND_TOPMOST,
            target_position[0], target_position[1],
            target_size[0], target_size[1],
            win32con.SWP_SHOWWINDOW
        )

        @blockWrapper(block=block, timeout=timeout)
        def check_position_size(position, size):
            this_position, this_size = self.get_postion_size()
            if this_position == position and this_size == size:
                return True
            else:
                return False

        # 返回结果
        return check_position_size(
            position=target_position,
            size=target_size,
        )

    # 返回满足条件的所有的window_data
    def get_window_datas(self, hwnds=None, titles=None, sizes=None, positions=None):
        '''
        :param hwnds: None|Int|List|Set|Tuple 例如:123 or [123,456]
        :param titles: None|Str|List|Set|Tupple 例如:'mytitle' or ('mytitle1','mytitle2')
        :param sizes:
            例如：sizes=[(100,200),(300,400)] or (100,200)
            注意：不可以写size=[100,200] size与position必须为元组
        :param positions: 同size
        :return: window_datas
        查询规则,例如：
            1. WindowElf().get_window_datas() 相当于：
                    select hwnd,title,size,position from 【全部的window_datas】
            2. WindowElf.get_window_datas(hwnds=[123,]) 或 WindowElf.get_window_datas(hwnds=123) 相当于:
                    select hwnd,title,size,position from 【全部的window_datas】 where hwnd in [123,]
            3. WindowElf.get_window_datas(hwnds=123,sizes=[(100,200),(300,400]) 相当于:
                    select hwnd,title,size,position from 【全部的window_datas】 where hwnd in [123,] and size in [(100,200),(300,400)]
        '''
        # 全部的窗口信息
        window_datas_all = []

        # 获取方法
        def get_all_hwnd(this_hwnd, mouse):
            if win32gui.IsWindow(this_hwnd) and win32gui.IsWindowEnabled(this_hwnd) and win32gui.IsWindowVisible(
                    this_hwnd):
                this_title = win32gui.GetWindowText(this_hwnd)
                if this_title:
                    this_position, this_size = self.get_postion_size(this_hwnd)
                    window_datas_all.append(
                        {'hwnd': this_hwnd, 'title': this_title, 'position': this_position, 'size': this_size, }
                    )

        # 填充window_datas_all
        win32gui.EnumWindows(get_all_hwnd, 0)
        # 要返回的结果
        ret_window_datas = []
        # 扩展参数类型
        if hwnds:  # 如果条件中有hwnds
            if type(hwnds).__name__ == 'int': hwnds = [hwnds, ]  # 支持int类型
        if titles:  # 如果条件中有titles
            if type(titles).__name__ == 'str': titles = [titles, ]  # 支持str类型
        if sizes:  # 如果条件中有sizes
            if type(sizes[0]).__name__ == ('int' or 'float'): sizes = [sizes, ]  # 支持单元组，单列表
        if positions:  # 如果条件中有positions
            if type(positions[0]).__name__ == ('int' or 'float'): positions = [positions, ]  # 支持单元组，单列表
        # 根据条件检索
        for window_data in window_datas_all:
            if ((not hwnds) or window_data['hwnd'] in hwnds) and \
                    ((not titles) or window_data['title'] in titles) and \
                    ((not sizes) or window_data['size'] in sizes) and \
                    ((not positions) or window_data['position'] in positions):
                ret_window_datas.append(window_data)
        return ret_window_datas

    # 根据指定了hwnd返回window_data，包含hwnd,title,size,position
    def get_window_data(self, hwnd=None, titles=None, sizes=None, positions=None, block=True, timeout=None):
        '''
        :param hwnd: None|Int
        :param titles: None|Str|List|Set|Tupple 例如:'mytitle' or ('mytitle1','mytitle2')
        :param sizes:
            例如：sizes=[(100,200),(300,400)] or (100,200)
            注意：不可以写size=[100,200] size与position必须为元组
        :param positions: 同size
        :block:如果返回值为空，是否堵塞
        :timeout:堵塞的最大时长,timeout=None等价于timeout=self.settings['new_build_timeout']
        :return: window_data|None
        查询规则:
            1.get_window_data()相当于get_window_data(hwnd=self.hwnd)
            2.get_window_data(titles='mytitle') 相当于：
                select hwnd,title,size,positon from 【全部的window_datas]】 where title in ['mytitle'] limit 1;
            3.get_window_data(hwnd=123,titles='mytitle',sizes=(100,200)) 相当于：
                select hwnd,title,size,positon from 【全部的window_datas]】 where hwnd=123 and title in ['mytitle'] and size in [(100,200),]limit 1;
        '''
        # 堵塞最大时间
        if block and timeout == None:
            timeout = self.settings['new_build_timeout']
        # 扩展参数类型
        if titles:  # 如果条件中有titles
            if type(titles).__name__ == 'str': titles = [titles, ]  # 支持str类型
        if sizes:  # 如果条件中有sizes
            if type(sizes[0]).__name__ == ('int' or 'float'): sizes = [sizes, ]  # 支持单元组，单列表
        if positions:  # 如果条件中有positions
            if type(positions[0]).__name__ == ('int' or 'float'): positions = [positions, ]  # 支持单元组，单列表
        # 如果没有任何约束，返回self.hwnd的window_data
        if (not hwnd) and (not titles) and (not sizes) and (not positions):
            window_data = {}
            window_data['hwnd'] = self.hwnd
            window_data['title'] = self.title
            window_data['position'] = self.position
            window_data['size'] = self.size
            return window_data
        # 有约束，返回满足约束的window_data，没有找到返回None
        else:
            @blockWrapper(block=block, timeout=timeout)
            def get_this_window_data(hwnd, titles, sizes, positions):
                window_data = {}

                def get_all_hwnd(this_hwnd, mouse):
                    if (not hwnd) or (hwnd == this_hwnd):
                        if win32gui.IsWindow(this_hwnd) and win32gui.IsWindowEnabled(
                                this_hwnd) and win32gui.IsWindowVisible(this_hwnd):  # 此处加入了hwnd的判断
                            this_title = win32gui.GetWindowText(this_hwnd)
                            this_position, this_size = self.get_postion_size(this_hwnd)
                            if ((not titles) or this_title in titles) and \
                                    ((not sizes) or this_size in sizes) and \
                                    ((not positions) or this_position in positions):
                                window_data['hwnd'] = this_hwnd
                                window_data['title'] = this_title
                                window_data['size'] = this_size
                                window_data['position'] = this_position

                win32gui.EnumWindows(get_all_hwnd, 0)
                return window_data

            # 返回window_data
            window_data = get_this_window_data(
                hwnd=hwnd,
                titles=titles,
                sizes=sizes,
                positions=positions,
            )
            return window_data if window_data else None

    # 得到顶层窗口的window_data
    def get_window_data_foreground(self):
        '''
        :return: None|window_data
        '''
        hwnd = win32gui.GetForegroundWindow()
        return self.get_window_data(hwnd=hwnd)

    # 判断self.hwnd是否还存在窗口
    def is_window(self):
        '''
        :return: True|False
        '''
        return bool(win32gui.IsWindow(self.hwnd))

    # 根据条件关闭窗口
    def close_window(self, hwnds=None, titles=None, block=True, timeout=None):
        '''
        :return: True|False
        '''
        if block and not timeout:
            timeout = self.settings['manage_timeout']

        # 初始化所有需要关闭的hwnd
        target_hwnds = []
        # if hwnds=None,titles=None --> close_window(hwnds=self.hwnd)
        if not hwnds and not titles:
            target_hwnds.append(self.hwnd)
        # 如果有关闭的条件
        else:
            # 统计hwnds条件，并添加到target_hwnds
            if hwnds:
                if type(hwnds).__name__ == 'int':
                    target_hwnds.append(hwnds)
                else:
                    target_hwnds += hwnds
            # 统计titles条件，并添加到hwnd_all中
            if titles:
                window_datas = self.get_window_datas(titles=titles)
                if window_datas:
                    for window_data in window_datas:
                        target_hwnds.append(window_data['hwnd'])
            # 去重
            target_hwnds = list(set(target_hwnds))

        # 尝试发送关闭消息
        for target_hwnd in target_hwnds:
            try:
                win32gui.PostMessage(target_hwnd, win32con.WM_CLOSE, 0, 0)
            except:
                pass

        @blockWrapper(block=block, timeout=timeout)
        def check_windows_close_by_hwnds(hwnds):
            for hwnd in hwnds:
                if win32gui.IsWindow(hwnd):
                    return False
            return True

        # 返回关闭结果
        return check_windows_close_by_hwnds(
            hwnds=target_hwnds,
        )

    # 设置句柄窗口在最上层
    def set_foreground(self, hwnd=None, block=True, timeout=None):
        '''
        :param hwnd: 句柄
        :param manage_delay: 操作延时
        :param manage_confirm_max_num: 最大确认次数
        :return: True|Flase
        '''
        if block and timeout == None:
            timeout = self.settings['manage_timeout']

        # 不输入句柄默认控制self.hwnd
        if not hwnd:
            hwnd = self.hwnd

        @blockWrapper(block=block, timeout=timeout)
        def this_set_foreground(hwnd):
            try:
                win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
                win32gui.SetForegroundWindow(hwnd)
                win32gui.BringWindowToTop(hwnd)
            except:
                pass
            window_data = self.get_window_data_foreground()
            if hwnd == window_data['hwnd']:
                return True
            else:
                return False

        # 返回操作结果
        return this_set_foreground(
            hwnd=hwnd
        )

    # 最小化窗口
    def set_window_min(self, hwnd):
        if not hwnd:
            hwnd = self.hwnd
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    # 最大化窗口
    def set_window_max(self, hwnd):
        if not hwnd:
            hwnd = self.hwnd
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


if __name__ == '__main__':
    w = WindowElf()
    print(w.hwnd)
    print(w.title)
    a = w.get_window_data(hwnd=131398)
    print(a)
    print(
        w.get_window_data(titles='企业微信')
    )
    w2 = WindowElf(hwnd=66640)
    print(w2.is_window())
    print(w2.close_window())
    print(w2.is_window())
    time.sleep(1)
    print(w2.is_window())

    # time.sleep(4)
    # w = WindowElf(foreground=True)
    # print(w.title)
    # print(w.hwnd)
    # print(w.position)
    # print(w.size)
    # window_datas = w.get_window_datas()
    # for wd in window_datas:
    #     print(wd)
    # ret = w.close_window(hwnds=855166,titles=['Q-Dir 7.09','confirm_百度搜索 - 极速浏览器'])
    # w.close_window()
