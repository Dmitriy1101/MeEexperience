import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from PSQLAlchemy_models import create_tables, Client, Phone, drop_tables

#sql_база://логин:пароль@сервер:порт/имя_базы
DSN = 'postgresql://postgres:NotGoodNotBad@localhost:5432/music_service'
#Создаем способ подключения
engine = sq.create_engine(DSN)
#Создаем таблицы
create_tables(engine)
#Сессии для подключения
Session = sessionmaker(bind = engine)
session = Session()

#добавим клиента
client1 = Client(name = 'Семен', surname = 'Коркин', mail = 'почтовый_ящик@почта.кг')
print(f'Новый клиент {client1.id} еще не добавлен')
#отправим клиента в базу
session.add(client1)
session.commit()
print(f'А так добавлен ===>  {client1}')

#добавим телефоны клиента и отправим в базу
p1 = Phone (id_client = '1', name = '8800553535')
p2 = Phone (id_client = '1', name = '88004443334')
session.add_all([p1, p2])
session.commit()

#получаем и печатаем ВСЕ телефоны
#for p in session.query(Phone).all():
#    print(p)
#получаем и печатаем фильтрованые телефоны и клиенты
print('получаем и печатаем фильтрованые телефоны ')
for p in session.query(Phone).filter(Phone.id_client == '1').all():
    print(p)
print(' и клиенты')
for c in session.query(Client).filter(Client.mail.like('%ящик%')).all():
    print(c)

#объединяем
print('объединяем')
for c in session.query(Client).join(Phone.client).filter(Phone.name.like('%8%')).all():
    print(c)
for p in session.query(Phone).join(Client.phones).filter(Client.name.like('%н%')).all():
    print(p)

#для подзапроса добавим клиента
c2 = Client(name = 'Васян', surname = 'Петросян', mail = 'почетный_ящик@почта.кг')
p3 = Phone (id_client = '2', name = '88001123244')
session.add_all([c2, p3])
session.commit()
#подзапрос все клиенты где телефоны с '8' 
print('подзапрос')
subq = session.query(Phone).filter(Phone.name.like('%8%')).subquery()
for sub in session.query(Client).join(subq, Client.id == subq.c.id_client):
    print(sub)
    
#меняем данные
session.query(Client).filter(Client.surname == 'Коркин').update({'surname' : 'Теркин'})
session.commit()
print(f'меняем данные Коркин на Теркин ===> {client1}')

#удаляем данные
session.query(Phone).filter(Phone.name == '8800553535').delete()
session.commit()
print('Телефон 8800553535 убег')
for p in session.query(Phone).all():
    print(p)
    
#подчистим
drop_tables(engine)

#не забудь закрыть 
session.close()