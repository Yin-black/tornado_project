from tornado.web import RequestHandler,authenticated
from utils.pthoto_press import thurmb_make,get_img
import os
from pycket.session import SessionMixin
from utils.post_press import Post


class Base(RequestHandler,SessionMixin):
    """
    验证是否登陆
    """
    def get_current_user(self):
        current_user = self.session.get('s_user')
        if current_user:
            return current_user
        else:
            return None

class IndexHandler(Base):
    """
    主页
    """
    @authenticated
    def get(self):
        self.render("index.html")

class PostHandler(Base):

    @authenticated
    def get(self, post_id):
        imgurl = Post.get_imgurl(post_id)
        if imgurl:
            img = imgurl.imgurl.replace('static/','')
            self.render("post.html",img_url = img)
        else:
            self.write('没有此图片')


class ExploreHandler(Base):
    """
    浏览页面
    """
    @authenticated
    def get(self):
        os.chdir('static')
        path = 'uploads/thubms'
        get_loadimg =get_img(path)
        os.chdir("..")

        self.render("explore.html",img_num=get_loadimg)

class UploadHandler(Base):
    """
    上传图片
    """
    @authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        imgs_files = self.request.files.get('newimg',None)
        for img_file in imgs_files:
            print("got {}".format(img_file['filename']))
            file_url = "static/uploads/{}".format(img_file['filename'])

            with open (file_url,'wb') as f:
                f.write(img_file['body'])
            current_user_id = Post.get_current_user_id(self.session.get('s_user'))
            if current_user_id != False:
                Post.Add(current_user_id,file_url)
            else:
                self.write('UserID有误！')
            save_img_path = 'static/uploads/'+img_file['filename']
            thurmb_make(save_img_path)    #储存缩略图
        self.redirect('/explore')