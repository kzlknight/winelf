import numpy as np
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
import time
from winelf import global_settings
import warnings


def action_decorator(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        # default:before_delay = self.before_delay
        # before_delay默认等于self.before_delay
        before_delay = kwargs.get('before_delay',self.before_delay)
        if before_delay: time.sleep(before_delay)
        ret = func(*args, **kwargs)
        # default:after_delay = self.after_delay
        # after_delay默认为self.action_delay
        after_delay = kwargs.get('after_delay',self.after_delay)
        if after_delay: time.sleep(after_delay)
        return ret
    return wrapper




class MouseElf():

    def __init__(
            self,
            press_time=global_settings.MOUSE_PRESS_TIME,
            before_delay=global_settings.MOUSE_BEFORE_DELAY,
            after_delay=global_settings.MOUSE_AFTER_DELAY,
            click_interval=global_settings.CLICK_INTERVAL,
    ):
        self.settings = dict(
            press_time = press_time,
            before_delay = before_delay,
            after_delay = after_delay,
            click_interval = click_interval
        )
        self.mouse = MouseController()


    @action_decorator
    def __click(self,action,press_time=None,num=1,click_interval=None,**kwargs):
        for i in range(num):
            self.mouse.press(action)
            time.sleep(press_time or self.settings['press_time'])
            self.mouse.release(action)
            if i < num - 1: time.sleep(click_interval or self.settings['click_interval'])


    def click_left(self, press_time=None,**kwargs):
        return self.__click(action=Button.left,press_time=press_time,**kwargs)

    def click_right(self, press_time=None,**kwargs):
        return self.__click(action=Button.right,press_time=press_time,**kwargs)

    def click_middle(self, press_time=None,**kwargs):
        return self.__click(action=Button.middle,press_time=press_time,**kwargs)

    def click_db_left(self, press_time=None,click_interval=None,**kwargs):
        return self.__click(action=Button.left,press_time=press_time,click_interval=click_interval,num=2,**kwargs)

    def click_db_right(self, press_time=None,click_interval=None,**kwargs):
        return self.__click(action=Button.right,press_time=press_time,click_interval=click_interval,num=2,**kwargs)

    def click_db_middle(self, press_time=None,click_interval=None,**kwargs):
        return self.__click(action=Button.middle,press_time=press_time,click_interval=click_interval,num=2,**kwargs)

    def __point_space(self,point_start,point_end):
        delta_x,delta_y = point_end[0] - point_start[0],point_end[1] - point_end[1]
        return np.linspace(
            np.array(point_start),np.array(point_end),max(
                abs(delta_x),abs(delta_y),
            )
        ).astype(int).tolist()

    @action_decorator
    def __move(self,point,point_start=None,speed='normal'):
        if not speed:
            self.mouse.position = point
        else:
            if not point_start:point_start = self.mouse.position
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


    def move(self,point,point_start=None,speed=None,**kwargs):
        return self.__move(point=point,point_start=point_start,speed=speed,**kwargs)

    def __move_click(self,action,point,point_start=None,speed=None,press_time=None,**kwargs):
        if not speed:
            self.__move(point=point, **kwargs)
            self.__click(action=action,press_time=press_time,**kwargs)
        else:
            if not point_start:
                point_start = self.mouse.position
            self.__move_continuation(point_start=point_start, point=point, speed=speed, **kwargs)
            self.__click(action=action,press_time=press_time,**kwargs)


    def move_l(self,point,point_start=None,speed=None,press_time=None,**kwargs):
        return self.__move_click(action=Button.left,point=point,point_start=point_start,speed=speed,press_time=press_time,**kwargs)


    def move_r(self,point,point_start=None,speed=None,press_time=None,**kwargs):
        return self.__move_click(action=Button.right,point=point,point_start=point_start,speed=speed,press_time=press_time,**kwargs)


    def move_m(self,point,point_start=None,speed=None,press_time=None,**kwargs):
        return self.__move_click(action=Button.middle,point=point,point_start=point_start,speed=speed,press_time=press_time,**kwargs)



    def __move_relative(self,deviation,speed=None,**kwargs):
        current_point = self.mouse.position
        point = current_point[0]+deviation[0],current_point[1]+deviation[1]
        if not speed:
            self.__move(point=point,**kwargs)
        else:
            self.__move_continuation(point_start=current_point,point=point,speed=speed,**kwargs)

    def move_relative(self, deviation, speed=None, **kwargs):
        self.__move_relative(deviation=deviation,speed=speed,**kwargs)

    def move_relative_l(self,deviation,speed=None,press_time=None,**kwargs):
        self.__move_relative(deviation=deviation,speed=speed,**kwargs)












    def move_relative(self, point_relative,continuation=None,speed=None,before_delay=None,after_delay=None,**kwargs):
        current_point = self.mouse.position
        point_absolute = current_point[0] + point_relative[0],current_point[1] + point_relative[1]
        self.move(point=point_absolute,continuation=continuation,speed=speed,before_delay=before_delay,after_delay=after_delay,**kwargs)

    def scroll(self,x,y):
        self.mouse.scroll(x,y)

    def select_l(self,point_start,point_end,continuation=False,speed=None,press_time=None,after_delay=None,**kwargs):








    def test(self):
        a = self.__point_space(
            (10,20),
            (100,30),
        )
        print(a)
        print(type(a))



if __name__ == '__main__':

    mouseElf = MouseElf()
    # mouseElf.move(
    #     (100,200),continuation=True,speed=''
    # )
    mouseElf.move_relative(
        (100,100),continuation=True,speed='1'
    )
    mouseElf.aaa()
