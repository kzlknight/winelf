from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
import numpy as np
import warnings
import time
from winelf import global_settings

__all__ = [
    'Button','MouseElf'
]

# 动作延迟
def _mouseSecurityDelay(func):
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


class MouseElf():
    def __init__(
            self,
            press_time=global_settings.MOUSE_PRESS_TIME,  # 按键时间
            before_delay=global_settings.MOUSE_BEFORE_DELAY,  # 前置延迟
            after_delay=global_settings.MOUSE_AFTER_DELAY,  # 后置延迟
            click_interval=global_settings.CLICK_INTERVAL,  # 连续点击延时
    ):
        self.settings = dict(
            press_time=press_time,
            before_delay=before_delay,
            after_delay=after_delay,
            click_interval=click_interval
        )
        self.mouse = MouseController()

    # 得到两点间的points
    def __point_space(self, point_start, point_end):
        delta_x, delta_y = point_end[0] - point_start[0], point_end[1] - point_end[1]
        return np.linspace(
            np.array(point_start), np.array(point_end), max(
                abs(delta_x), abs(delta_y),
            )
        ).astype(int).tolist()

    # 按下
    @_mouseSecurityDelay
    def __press(self, action, **kwargs):
        self.mouse.press(action)

    # 抬起
    @_mouseSecurityDelay
    def __release(self, action, **kwargs):
        self.mouse.release(action)

    # 按键
    @_mouseSecurityDelay
    def __click(self, action, press_time=None, num=1, click_interval=None, **kwargs):
        for i in range(num):
            self.mouse.press(action)
            time.sleep(press_time or self.settings['press_time'])
            self.mouse.release(action)
            if i < num - 1: time.sleep(click_interval or self.settings['click_interval'])

    # 移动鼠标
    @_mouseSecurityDelay
    def __move(self, point, point_start=None, speed='normal', **kwargs):
        if not speed:
            self.mouse.position = point
        else:
            if not point_start: point_start = self.mouse.position
            continuation_points: list = self.__point_space(
                point_start=point_start,
                point_end=point,
            )
            if speed in ['slow', 0, ]:
                continuation_delay = 0.005
            elif speed in ['normal', 1, ]:
                continuation_delay = 0.003
            elif speed in ['fast', 2, ]:
                continuation_delay = 0.001
            else:
                warnings.warn('位置speed，自动设置为normal')
                continuation_delay = 0.003
            for continuation_point in continuation_points:
                self.mouse.position = continuation_point
                time.sleep(continuation_delay)

    # 相对移动
    def __move_relative(self, deviation, point_start=None, speed=None, **kwargs):
        if not point_start: point_start = self.mouse.position
        point = point_start[0] + deviation[0], point_start[1] + deviation[1]
        self.__move(point=point, point_start=point_start, speed=speed, **kwargs)

    # 滚动
    @_mouseSecurityDelay
    def __scroll(self, x, y, **kwargs):
        self.mouse.scroll(x, y)

    # 按住移动
    def __select(self, action, point, point_start=None, speed=None, **kwargs):
        if not point_start:
            point_start = self.mouse.position
        self.__move(point=point_start, **kwargs)
        self.__press(action=action, **kwargs)
        self.__move(point=point, point_start=point_start, speed=speed, **kwargs)
        self.__release(action=action, **kwargs)

    # 1.点击----------------------------------------------------------------------
    # 点击鼠标左键
    def click_left(self, press_time=None, **kwargs):
        ''' 点击鼠标左键
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param kwargs: 包含参数如下
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
            num=1(点击次数)
            click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :return:None
        '''
        return self.__click(action=Button.left, press_time=press_time, **kwargs)

    # 点击鼠标右键
    def click_right(self, press_time=None, **kwargs):
        ''' 点击鼠标右键
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param kwargs: 包含参数如下
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
            num=1(点击次数)
            click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :return:None
        '''
        return self.__click(action=Button.right, press_time=press_time, **kwargs)

    # 点击鼠标中键
    def click_middle(self, press_time=None, **kwargs):
        ''' 点击鼠标中键
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param kwargs: 包含参数如下
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
            num=1(点击次数)
            click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :return:None
        '''
        return self.__click(action=Button.middle, press_time=press_time, **kwargs)

    # 双击鼠标左键
    def click_db_left(self, press_time=None, click_interval=None, **kwargs):
        '''双击鼠标左键
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param click_interval: click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        return self.__click(action=Button.left, press_time=press_time, click_interval=click_interval, num=2, **kwargs)

    # 双击鼠标右键
    def click_db_right(self, press_time=None, click_interval=None, **kwargs):
        '''双击鼠标右键
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param click_interval: click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        return self.__click(action=Button.right, press_time=press_time, click_interval=click_interval, num=2, **kwargs)

    # 双击鼠标中键
    def click_db_middle(self, press_time=None, click_interval=None, **kwargs):
        '''双击鼠标中键
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param click_interval: click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        return self.__click(action=Button.middle, press_time=press_time, click_interval=click_interval, num=2, **kwargs)

    # 绝对位置移动
    def move(self, point, point_start=None, speed=None, **kwargs):
        '''绝对位置移动
        :param point:(x,y),绝对位置终点
        :param point_start: (x,y),起点,None则使用当前位置
        :param speed:
            直接移动到终点 speed = None
            连续移动:
                慢速 speed = 0 | 'slow'
                中速 speed = 1 | 'normal'
                快速 speed = 2 | 'fast'
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        return self.__move(point=point, point_start=point_start, speed=speed, **kwargs)

    # 移动后左键点击
    def move_l(self, point, point_start=None, speed=None, press_time=None, num=1, click_interval=None, **kwargs):
        '''移动后左键点击
        :param point:(x,y),绝对位置终点
        :param point_start: (x,y),起点,None则使用当前位置
        :param speed:
            直接移动到终点 speed = None
            连续移动:
                慢速 speed = 0 | 'slow'
                中速 speed = 1 | 'normal'
                快速 speed = 2 | 'fast'
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param num:
            num=1(点击次数)
        :param click_interval:
            click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        # 移动位置
        self.__move(point=point, point_start=point_start, speed=speed, **kwargs)
        # 点击左键
        self.__click(action=Button.left, press_time=press_time, click_interval=click_interval, num=num, **kwargs)

    # 移动后右键点击
    def move_r(self, point, point_start=None, speed=None, press_time=None, num=1, click_interval=None, **kwargs):
        '''移动后右键点击
        :param point:(x,y),绝对位置终点
        :param point_start: (x,y),起点,None则使用当前位置
        :param speed:
            直接移动到终点 speed = None
            连续移动:
                慢速 speed = 0 | 'slow'
                中速 speed = 1 | 'normal'
                快速 speed = 2 | 'fast'
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param num:
            num=1(点击次数)
        :param click_interval:
            click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        # 位置移动
        self.__move(point=point, point_start=point_start, speed=speed, **kwargs)
        # 点击右键
        self.__click(action=Button.right, press_time=press_time, click_interval=click_interval, num=num, **kwargs)

    # 移动后点击中键
    def move_m(self, point, point_start=None, speed=None, press_time=None, num=1, click_interval=None, **kwargs):
        '''移动后点击中键
        :param point:(x,y),绝对位置终点
        :param point_start: (x,y),起点,None则使用当前位置
        :param speed:
            直接移动到终点 speed = None
            连续移动:
                慢速 speed = 0 | 'slow'
                中速 speed = 1 | 'normal'
                快速 speed = 2 | 'fast'
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param num:
            num=1(点击次数)
        :param click_interval:
            click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        # 位置移动
        self.__move(point=point, point_start=point_start, speed=speed, **kwargs)
        # 点击中键
        self.__click(action=Button.middle, press_time=press_time, click_interval=click_interval, num=num, **kwargs)

    # 相对移动
    def move_relative(self, deviation, point_start=None, speed=None, **kwargs):
        '''偏移移动
        :param deviation: (x,y)相对于point_start的偏移量
        :param point_start: (x,y),起点,None则使用当前位置
        :param speed:
            直接移动到终点 speed = None
            连续移动:
                慢速 speed = 0 | 'slow'
                中速 speed = 1 | 'normal'
                快速 speed = 2 | 'fast'
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        self.__move_relative(deviation=deviation, point_start=point_start, speed=speed, **kwargs)

    # 相对移动后点击左键
    def move_relative_l(self, deviation, point_start=None, speed=None, press_time=None, num=1, click_interval=None,
                        **kwargs):
        '''相对移动后点击左键
        :param deviation: (x,y)相对于point_start的偏移量
        :param point_start: (x,y),起点,None则使用当前位置
        :param speed:
            直接移动到终点 speed = None
            连续移动:
                慢速 speed = 0 | 'slow'
                中速 speed = 1 | 'normal'
                快速 speed = 2 | 'fast'
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param num:
            num=1(点击次数)
        :param click_interval:
            click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        self.__move_relative(deviation=deviation, point_start=point_start, speed=speed, **kwargs)
        self.__click(action=Button.left, press_time=press_time, click_interval=click_interval, num=num, **kwargs)

    # 相对移动后点击右键
    def move_relative_r(self, deviation, point_start=None, speed=None, press_time=None, num=1, click_interval=None,
                        **kwargs):
        '''相对移动后点击右键
        :param deviation: (x,y)相对于point_start的偏移量
        :param point_start: (x,y),起点,None则使用当前位置
        :param speed:
            直接移动到终点 speed = None
            连续移动:
                慢速 speed = 0 | 'slow'
                中速 speed = 1 | 'normal'
                快速 speed = 2 | 'fast'
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param num:
            num=1(点击次数)
        :param click_interval:
            click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        self.__move_relative(deviation=deviation, point_start=point_start, speed=speed, **kwargs)
        self.__click(action=Button.right, press_time=press_time, click_interval=click_interval, num=num, **kwargs)

    # 相对移动后点击中键
    def move_relative_m(self, deviation, point_start=None, speed=None, press_time=None, num=1, click_interval=None,
                        **kwargs):
        '''相对移动后点击中键
        :param deviation: (x,y)相对于point_start的偏移量
        :param point_start: (x,y),起点,None则使用当前位置
        :param speed:
            直接移动到终点 speed = None
            连续移动:
                慢速 speed = 0 | 'slow'
                中速 speed = 1 | 'normal'
                快速 speed = 2 | 'fast'
        :param press_time:
            按住时间 = press_time or self.settings['press_time']
        :param num:
            num=1(点击次数)
        :param click_interval:
            click_interval=None(点击时间间隔),如果为None:使用self.settings['click_interval']
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        self.__move_relative(deviation=deviation, point_start=point_start, speed=speed, **kwargs)
        self.__click(action=Button.middle, press_time=press_time, click_interval=click_interval, num=num, **kwargs)

    # 滚轮滚动
    def scroll(self, x, y, **kwargs):
        '''滚轮滚动
        :param x: 横向滚动量
        :param y: 纵向滚动量
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        self.__scroll(x=x, y=y, **kwargs)

    # 左键点击后移动
    def select_l(self, point, point_start=None, speed=None, **kwargs):
        ''' 左键点击后移动
        :param point:(x,y),绝对位置终点
        :param point_start:(x,y),起点,None则使用当前位置
        :param speed:
            直接移动到终点 speed = None
            连续移动:
                慢速 speed = 0 | 'slow'
                中速 speed = 1 | 'normal'
                快速 speed = 2 | 'fast'
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        return self.__select(action=Button.left, point=point, point_start=point_start, speed=speed, **kwargs)

    # 右键点击后移动
    def select_r(self, point, point_start=None, speed=None, **kwargs):
        ''' 右键点击后移动
        :param point:(x,y),绝对位置终点
        :param point_start:(x,y),起点,None则使用当前位置
        :param speed:
            直接移动到终点 speed = None
            连续移动:
                慢速 speed = 0 | 'slow'
                中速 speed = 1 | 'normal'
                快速 speed = 2 | 'fast'
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        return self.__select(action=Button.right, point=point, point_start=point_start, speed=speed, **kwargs)

    # 中键点击后移动
    def select_m(self, point, point_start=None, speed=None, **kwargs):
        ''' 中键点击后移动
        :param point:(x,y),绝对位置终点
        :param point_start:(x,y),起点,None则使用当前位置
        :param speed:
            直接移动到终点 speed = None
            连续移动:
                慢速 speed = 0 | 'slow'
                中速 speed = 1 | 'normal'
                快速 speed = 2 | 'fast'
        :param kwargs:
            before_delay = None (前置延时),如果为None:使用self.settings['before_delay']
            after_delay = None (后置延时),如果为None:使用self.settings['after_delay']
        :return:None
        '''
        return self.__select(action=Button.middle, point=point, point_start=point_start, speed=speed, **kwargs)


# if __name__ == '__main__':
#     mouseElf = MouseElf()
#     mouseElf.click_left()
#     mouseElf.click_right()

