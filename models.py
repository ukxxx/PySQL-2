import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=255), unique=True)

    def __str__(self):
        return f'ID: {self.id}, Publisher: {self.name}'

class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=255), unique=True)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)
    publisher = relationship('Publisher', backref='books')

    def __str__(self):
        return f'ID: {self.id}, Title: {self.title}, Publisher: {self.publisher}'

class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    book = relationship('Book', backref='stocks')
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    shop = relationship('Shop', backref='stocks')
    count = sq.Column(sq.Integer)

    def __str__(self):
        return f'ID: {self.id}, Book: {self.book}, Shop: {self.shop}, Quantity: {self.count}'

class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=255), unique=True)

    def __str__(self):
        return f'ID: {self.id}, Shop: {self.name}'

class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.Date)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    stock = relationship('Stock', backref='sales')
    count = sq.Column(sq.Integer)

    def __str__(self):
        return f'Price: {self.price}, Sale Date: {self.date_sale}, Quantity: {self.count}'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    print('Tables dropped')
    Base.metadata.create_all(engine)
    print('New tables created')