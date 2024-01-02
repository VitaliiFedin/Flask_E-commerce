import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:fed123321@localhost/e-commerce'
    SECRET_KEY = 'My_key'
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'app/static/images')
    ADMIN_EMAIL = 'vetal270399@gmail.com'
    PUBLISHABLE_KEY = 'pk_test_51OQ76iCml4QlIMYOs05ur4oBRZrE2zxEbHHpqQqkuI7kbpdoAH0y4v7k0Bm3uOoSZXS9dZfNBhydl2FaFTwxYXQc00kfB7nlEU'
    SECRET_KEY_STRIPE = 'sk_test_51OQ76iCml4QlIMYOTlEwV6lL7PPj8z62nstHbLlO2HxIB63VQ4Xe9oraL0OtA5Stxd9g82agb23zdLXecspC6TPV00ViY4rMe6'
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    pass


config = {
    'default': DevelopmentConfig,
    'config': Config

}
