from flask import session, render_template, request
from ..models import Product, Brand, Category
from . import main
from .. import search


@main.route('/', methods=['GET'])
def home_page():
    print(session.items())
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).paginate(page=page, per_page=4)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/index.html', products=products, brands=brands, categories=categories)


@main.route('/result')
def get_result():
    search_word = request.args.get('q')
    products = Product.query.msearch(search_word, fields=['name', 'description'], limit=3)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/result.html', products=products,brands=brands, categories=categories)


@main.route('/product/<int:id>')
def single_page(id):
    product = Product.query.get_or_404(id)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/single_page.html', product=product, brands=brands, categories=categories)


@main.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    brand = Product.query.filter_by(brand_id=get_brand.id).paginate(page=page, per_page=4)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/index.html', brand=brand, brands=brands, categories=categories,
                           get_brand=get_brand)


@main.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    category = Product.query.filter_by(category_id=get_cat.id).paginate(page=page, per_page=4)
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    return render_template('products/index.html', category=category, categories=categories, brands=brands,
                           get_cat=get_cat)
