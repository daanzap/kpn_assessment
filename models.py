from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship

# DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
import settings

DB_URI = 'sqlite:///' + settings.db_path

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URI))
session = scoped_session(Session)
Base = declarative_base()


# customer Model
class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    infix = Column(String(50))
    last_name = Column(String(50))
    address_street = Column(String(50))
    address_number = Column(Integer)
    city = Column(String(50))
    zipcode = Column(String(10))
    country = Column(String(50))
    purchases = relationship("Purchase")

    def __init__(self, first_name, infix, last_name, address_street, address_number, city, zipcode, country):
        self.first_name = first_name
        self.infix = infix
        self.last_name = last_name
        self.address_street = address_street
        self.address_number = address_number
        self.city = city
        self.zipcode = zipcode
        self.country = country


    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['id', 'first_name', 'infix', 'last_name', 'address_street', 'address_number', 'city', 'zipcode', 'country']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d


# product Model
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Numeric(10,2))
    description = Column(String(500))
    image_url = Column(String(50))


    def __init__(self, name, price, description, image_url):
        self.name = name
        self.price = price
        self.description = description
        self.image_url = image_url



    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['id', 'name', 'price', 'description', 'image_url']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d


# product Model
class Purchase(Base):
    __tablename__ = 'purchase'
    id = Column(Integer, primary_key=True)
    customer = Column(Integer, ForeignKey('customer.id'))
    product = Column(Integer, ForeignKey('product.id'))
    price = Column(Numeric(10,2))
    description = Column(String(500))
    image_url = Column(String(50))


    def __init__(self, name, price, description, image_url):
        self.name = name
        self.price = price
        self.description = description
        self.image_url = image_url



    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['id', 'name', 'price', 'description', 'image_url']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d




# creates database
if __name__ == "__main__":
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
