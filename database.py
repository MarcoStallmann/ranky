from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    isin = Column(String, unique=True)
    quantity = Column(Float)
    price = Column(Float)

    @property
    def market_value(self):
        return self.quantity * self.price

engine = create_engine('sqlite:///data/stocks.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
