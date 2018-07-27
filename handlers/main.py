from tornado.web import RequestHandler

class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")

class PostHandler(RequestHandler):
    def get(self, post_id):
        # self.write(post_id+'<br>' )
        self.render("post.html",post_id=post_id)


class ExploreHandler(RequestHandler):
    def get(self):
        self.render("explore.html")