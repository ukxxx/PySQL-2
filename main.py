import os
import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, Book, Publisher, Stock, Shop, Sale


class FileError(Exception):
    def __init__(self, message):
        super().__init__(message)

try:
    with open(os.path.join(os.getcwd(),'postgres_config.json'), 'r') as file:
        config = json.load(file)
except:
     raise FileError("There is no config.json file or file is corrupted.")
 
# Function which imports data from provided json file
def import_data(file_name):
    with open(os.path.join(os.getcwd(), file_name), 'r') as file:
        for item in json.load(file):
            if item["model"] == "publisher":
                publisher = Publisher(id=item["pk"], name=item["fields"]["name"])
                session.add(publisher)
            elif item["model"] == "book":
                book = Book(id=item["pk"], title=item["fields"]["title"], publisher_id=item["fields"]["id_publisher"])
                session.add(book)
            elif item["model"] == "shop":
                shop = Shop(id=item["pk"], name=item["fields"]["name"])
                session.add(shop)
            elif item["model"] == "stock":
                stock = Stock(id=item["pk"], shop_id=item["fields"]["id_shop"], book_id=item["fields"]["id_book"], count=item["fields"]["count"])
                session.add(stock)
            elif item["model"] == "sale":
                sale = Sale(id=item["pk"], price=item["fields"]["price"], date_sale=item["fields"]["date_sale"], count=item["fields"]["count"], stock_id=item["fields"]["id_stock"])
                session.add(sale)
            session.commit()

# Function which finds sales by publisher
def find_sales_by_publisher(publisher_input):
        try:
            publisher_str = session.query(Publisher).filter(Publisher.name == publisher_input).first().name
            sales = (
                    session.query(Sale)
                    .join(Stock)
                    .join(Book)
                    .join(Publisher)
                    .filter(Publisher.name == publisher_str)
                    .all()
                )
            return sales
        except AttributeError:
            publisher_id = session.query(Publisher).filter(Publisher.id == publisher_input).first().id
            sales = (
                    session.query(Sale)
                    .join(Stock)
                    .join(Book)
                    .join(Publisher)
                    .filter(Publisher.id == int(publisher_id))
                    .all()
                )
            return sales


if __name__ == "__main__":
    DSN = f'postgresql://{config["login"]}:{config["password"]}@{config["host"]}:{config["port"]}/{config["db_name"]}'
    engine = sq.create_engine(DSN)
    session = sessionmaker(bind=engine)()
    
    create_tables(engine)
    import_data('data.json')

    publisher_name = input("Enter publisher name: ")
    try:
        sales = find_sales_by_publisher(publisher_name)
    except:
        print("Publisher not found")
        exit()
    print(f'\n\033[1mSales by {publisher_name}:\033[0m')
    print("\n\033[1m| Book name                      | Store name                | Price      | Date\033[0m")
    for sale in sales:
        book_name = sale.stock.book.title[:30].ljust(30)
        store_name = sale.stock.shop.name[:25].ljust(25)
        price = "{:.2f}".format(sale.price).rjust(10)
        date = str(sale.date_sale)
        print("| {:<30} | {:<25} | {:>10} | {:}".format(book_name, store_name, price, date))
    session.close()