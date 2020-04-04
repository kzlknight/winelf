import cv2
import numpy as np
import pyautogui
import aircv as ac
import pytesseract
import time


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


def to_digital(img):
    # 1.如果是路径
    if type(img).__name__ == 'str':
        return cv2.imread(img)
    # 2.如果是PIL的Image类
    if type(img).__name__ == 'Image':
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    # 3.如果是数字对象
    if type(img).__name__ == 'ndarray':
        return img
    else:
        raise Exception('the type of img in not in [str,Image,ndarray]')


# 指定左顶点，大小进行截图，如果传递save_path，为图片保存路径
def screenshot(position=(0, 0), size=(1920, 1080), save_path=None, digital=False):
    # 截图，返回Image对象
    img = pyautogui.screenshot(
        region=[position[0], position[1], size[0], size[1]]
    )
    # 保存到指定位置
    if save_path:
        img.save(save_path)
    # 返回图片或数字结果
    if digital:
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    else:
        return img


# 读取src路径的图片，在范围中所有返回所有匹配到图片的中心位置
def search_imgs(imgs, position=(0, 0), size=(1920, 1080), confidence=0.8, block=False, timeout=5):
    '''
    :return: [point,point,]
    '''
    # 得到target_digital_imgs，内容为ndarray
    if not type(imgs).__name__ in ['list', 'tuple']:
        imgs = [imgs, ]
    target_digital_imgs = [
        to_digital(img) for img in imgs
    ]

    @blockWrapper(block=block, timeout=timeout)
    def get_result_points(target_digital_imgs, position, size, confidence):
        # 截屏后的Image转成ndarray
        screenshot_digital_img = screenshot(position=position, size=size, digital=True)
        # 结果点集
        result_points = set()
        for target_digital_img in target_digital_imgs:
            # 单次图片得到的结果对象
            match_results = ac.find_all_template(
                screenshot_digital_img,
                target_digital_img,
                confidence
            )
            # 添加到结果点集中
            if match_results:
                for match_result in match_results:
                    x = int(match_result['result'][0]) + position[0]
                    y = int(match_result['result'][1]) + position[1]
                    result_points.add((x, y))
        # 转换为列表
        result_points = list(result_points)
        return result_points

    return get_result_points(
        target_digital_imgs=target_digital_imgs,
        position=position,
        size=size,
        confidence=confidence,
    )


# 读取src路径的图片，在范围中所有返回第一个匹配到图片的中心位置
def search_img(imgs, position=(0, 0), size=(1920, 1080), confidence=0.8, block=False, timeout=5):
    '''
    :return: None|point
    '''
    # 得到target_digital_imgs，内容为ndarray
    if not type(imgs).__name__ in ['list', 'tuple']:
        imgs = [imgs, ]
    target_digital_imgs = [
        to_digital(img) for img in imgs
    ]

    @blockWrapper(block=block, timeout=timeout)
    def get_result_point(target_digital_imgs, position, size, confidence):

        # 截屏后的Image转成ndarray
        screenshot_digital_img = screenshot(position=position, size=size, digital=True)

        # 一找到结果，就立马返回，避免不必要的继续搜索
        for target_digital_img in target_digital_imgs:
            # 单次图片得到的结果对象
            match_results = ac.find_all_template(
                screenshot_digital_img,
                target_digital_img,
                confidence
            )
            # 添加到结果点集中
            if match_results:
                for match_result in match_results:
                    x = int(match_result['result'][0]) + position[0]
                    y = int(match_result['result'][1]) + position[1]
                    return (x, y)
        # 如果没有找到，返回None
        return None

    return get_result_point(
        target_digital_imgs=target_digital_imgs,
        position=position,
        size=size,
        confidence=confidence,
    )

# 屏幕内容转文字
def screen_to_word(position,size,block=False,timeout=5):
    '''
    :return: str|None
    '''
    @blockWrapper(block=block,timeout=timeout)
    def __get_screen_to_word(position,size):
        screenshot_img = screenshot(position=position,size=size)
        word = pytesseract.image_to_string(screenshot_img)
        return word if word else None
    return __get_screen_to_word(
        position=position,
        size=size,
    )



from winelf.mouse import MouseElf
if __name__ == '__main__':
    img1 = screenshot((100,100),(200,200))
    img2 = screenshot((300,300),(400,400))
    a = search_img(
        imgs=[img1,img2]
    )
    print(a)
