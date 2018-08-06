from tornado.web import RequestHandler,authenticated
from pycket.session import SessionMixin
from utils.post_press import Post,PostUrl


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
    """"
    显示单个图页详情
    """
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
    发现页，浏览最新上传所有图片的缩略图
    """
    @authenticated
    def get(self):
        userid = Post.get_current_user_id(self.current_user)
        get_thumbsimg_url =  Post.selec_thumbs_url(userid)
        self.render("explore.html",img_num=get_thumbsimg_url)

class UploadHandler(Base):
    """
    上传图片
    """
    @authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        imgs_files = self.request.files.get('newimg',None)
        static_addr = self.settings['static_path']
        p_posturl = PostUrl(static_addr)
        for img_file in imgs_files:

            post_url = p_posturl.get_post_url(img_file['filename'])
            p_posturl.save_post_img(static_addr,post_url,img_file['filename'], img_file['body'])


            # thurmb_make(save_img_path)    #储存缩略图
            thumbs_url = p_posturl.get_thumbs_url(img_file['filename'])
            p_posturl.save_thumbs_img(static_addr,thumbs_url,img_file['filename'],img_file['body'])

            current_user_id = self.session.get('s_user')
            p_posturl.save_sql_url(current_user_id, post_url, thumbs_url)
        self.redirect('/explore')