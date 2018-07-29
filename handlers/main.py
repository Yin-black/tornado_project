from tornado.web import RequestHandler
from utils.pthoto_press import thurmb_make,get_img
import os

class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")

class PostHandler(RequestHandler):
    def get(self, post_id):
        # self.write(post_id+'<br>' )

        self.render("post.html",post_id=post_id)


class ExploreHandler(RequestHandler):
    def get(self):
        os.chdir('static')
        path = 'uploads/thubms'
        get_loadimg =get_img(path)
        os.chdir("..")
        self.render("explore.html",img_num=get_loadimg)

class UploadHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        imgs_files = self.request.files.get('newimg',None)
        for img_file in imgs_files:
            print("got {}".format(img_file['filename']))
            with open ("static/uploads/{}".format(img_file['filename']),'wb') as f:
                f.write(img_file['body'])
                print(f)

            save_img_path = 'static/uploads/'+img_file['filename']
            thurmb_make(save_img_path)

        self.redirect('/explore')