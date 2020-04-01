from mouse import *

def test_click(m:MouseElf):
    m.click_left()
    m.click_right(press_time=1)
    m.click_middle(press_time=1,before_delay=1,after_delay=1)

def test_move(m:MouseElf):
    m.move(
        point=(10,10)
    )
    m.move(
        point=(1000,800),
        point_start=(400,400)
    )

    m.move(
        point=(400,400),
        speed='slow',
    )

    m.move(
        point=(1000,800),
        point_start=(400,400),
        speed=0,
    )

    m.move(
        point=(1000,800),
        point_start=(400,400),
        speed='normal',
    )

    m.move(
        point=(1000,800),
        point_start=(400,400),
        speed=1,
    )

    m.move(
        point=(1000,800),
        point_start=(400,400),
        speed='fast',
    )

    m.move(
        point=(1000,800),
        point_start=(400,400),
        speed=2,
    )







if __name__ == '__main__':
    m = MouseElf()
    test_click(m)
    test_move(m)
