from tornado.web import RequestHandler,authenticated
from pycket.session import SessionMixin
from utils.post_press import Post,PostUrl
from utils.autho_press import Like
import redis


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
        """
         关注所有上传的图片
        """
        get_img_url = Post.selec_all_url()
        self.render('index.html',img_num=get_img_url)


class PostHandler(Base):
    """"
    显示单个图页详情
    """
    @authenticated
    def get(self, post_id):
        imgurl = Post.get_imgurl(post_id)  #
        users = Post.get_like_users(post_id)
        post_name = Post.get_post_name(post_id)
        if imgurl:
            self.render("post.html",img_url = imgurl[0],post_name =post_name,users = users)
        else:
            self.write('没有此图片')


class ExploreHandler(Base):
    """
    发现页，浏览当前用户最新上传所有图片的缩略图
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
            p_posturl.save_post_img(static_addr,post_url, img_file['body'])


            # thurmb_make(save_img_path)    #储存缩略图
            thumbs_url = p_posturl.get_thumbs_url(img_file['filename'])
            p_posturl.save_thumbs_img(static_addr,thumbs_url,post_url,img_file['body'])

            current_user_id = self.current_user #把upload和thumbs图片url 存入数据库
            p_posturl.save_sql_url(current_user_id, post_url, thumbs_url)
        self.redirect('/explore')

class ProfileHandler(Base):
    """
    用户中心页
    """
    @authenticated
    def get(self):
        id = self.get_argument('id','')
        like_url_list=[]
        img_id_list =[]
        if id:
           userid = id
        else:
            userid = Post.get_current_user_id(self.current_user)
            if not userid:
                self.set_status(404)
                self.write('用户Id出错！')
        post_img_url = Post.selec_thumbs_url(userid)   #获取上传图片的缩略图地址

        img_id = Like.get_post_id(userid) #获取喜欢图片的地址，返回列表

        for id in img_id:
            for i in id:
                if i:
                    a_list = Post.get_thumbs_url(i) # 通过img_id取缩略图地址,返回一个列表
                    for j in a_list:
                        for k in j:
                            like_url_list.append(k)
        print(post_img_url,like_url_list)
        self.render('profile.html',post_img_url=post_img_url,like_url=like_url_list)