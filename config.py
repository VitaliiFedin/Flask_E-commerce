import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:fed123321@localhost/e-commerce'
    SECRET_KEY = 'My_key'
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'app/static/images')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    pass


config = {
    'default': DevelopmentConfig,
    'config': Config

}
