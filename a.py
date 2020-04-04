import pyautogui
from PIL import Image


# 指定左顶点，大小进行截图，如果传递save_path，为图片保存路径
def screenshot(position=(0, 0), size=(1920, 1080), save_path=None):
    src_img = pyautogui.screenshot(
        region=[position[0], position[1], size[0], size[1]]
    )
    if save_path:
        src_img.save(save_path)
    return src_img

if __name__ == '__main__':
    print(screenshot())

    c = Image.open('1.png')
    # a = Image.fromqimage(screenshot())
    print(c)
