import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Client(Base):
    __tablename__ = 'client'
    
    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String(length = 40), unique = False)
    surname = sq.Column(sq.String(length = 40), unique = False)
    mail = sq.Column(sq.String(length = 40), unique = False)
    #первый способ в обоих классах
    #phone = relationship('Phone', back_populates = "client")
    def __str__(self):
        return f'{self.id} : {self.name} : {self.surname} : {self.mail}'


class Phone(Base):
    __tablename__ = 'phones'
    
    #без примари кей не работает нихуя id обязателен
    id = sq.Column(sq.Integer, primary_key = True)
    id_client = sq.Column(sq.Integer, sq.ForeignKey('client.id'), nullable=False)
    name = sq.Column(sq.String(length = 40), unique = False)
    #первый способ в обоих классах
    #client = relationship(Client, back_populates = 'phone')
    # второй
    client = relationship(Client, backref = 'phones')
    
    def __str__(self):
        return f'{self.id} : {self.id_client} : {self.name}'
    
    
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop_all(engine)
