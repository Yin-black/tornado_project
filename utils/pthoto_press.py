from PIL import Image
from  os import path
import glob

def thurmb_make(file_path):
    """
    制作缩略图

    """
    name = path.basename(file_path)
    f_name, ext = path.splitext(name)
    img = Image.open(file_path)
    img.thumbnail((200,200))
    img.save('static/uploads/thubms/{}_{}_{}{}'.format(f_name,200,200,ext), "JPEG")

def get_img(file_path):
    """
    获取所有jpg文件
    :param file_path:
    :return:
    """
    exp_file= glob.glob(file_path+'/*.jpg')
    return exp_file