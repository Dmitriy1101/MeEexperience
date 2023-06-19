import django
import psycopg2
import sqlalchemy

# Версия джанго
print (django.get_version())

#Связь с базой данных
#base_conn = psycopg2.connect(database='music_service', user='postgres', password='NotGoodNotBad')

# Курсор нужен для запросов к базе
#cur = base_conn.cursor()
# cur надо закрывать
#cur.close()

# А лучше так:
#with base_conn.cursor() as cur:
    #Делаем запрос
#    cur.execute('CREATE TABLE IF NOT EXISTS test ( id SERIAL PRIMARY KEY);')
    # Если все выше рабочее то запишим в базу, base_conn.rollback() команда не записывать запросы в базу, тоесть правильность запроса не гарантирует запись?
#    cur.execute('DROP TABLE test;')
#    base_conn.commit()
#Закрываем связь 
#base_conn.close()

# еще урок
base_conn = psycopg2.connect(database='music_service', user='postgres', password='NotGoodNotBad')
with base_conn.cursor() as cur:
    #пересоздаем таблицу, чтобы небылопутаницы в начале все таблицы удаляем
    cur.execute('''
    DROP TABLE IF EXISTS worker;
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS worker (
        id SERIAL PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        birthday date,
        function VARCHAR(40) NOT NULL,
        wage money
    );
    ''')
    base_conn.commit()# отправляем в бд
#
    cur.execute('''
        insert into worker (name, birthday, function, wage) values 
        ('Kent', '2000-01-22', 'salesman', 30000.01) RETURNING id, name, wage;  
    ''')
    print(cur.fetchone()) # такой запрос автоматически отправит в бд все что выше(извлекает одну строку)
    #print(cur.fetchall())  извлекает все строки(список)
    #print(cur.fetchmany(3))  извлекает 3 строки(список)
    cur.execute('''
        SELECT id, wage FROM worker WHERE name=%s;  
        ''', ('Kent',)) # так правильно делать запрос
    print(cur.fetchone())
    
    cur.execute('''
    DROP TABLE IF EXISTS worker;
    ''')
    
    base_conn.commit()

base_conn.close()

#print('\xa') для денег пррочитай кодировку символа юникод

# Теперь про sqlalchemy

# создаем строку подключения 'драйвер://пользователь:пароль@сервер:порт/имя базы'
DSN = 'postgresql://postgres:NotGoodNotBad@localhost:5432/music_service'
# функция создает объект подключения к базе
engine = sqlalchemy.create_engine(DSN)
# теперь сессия подключения, создается класс сессии
Session = sqlalchemy.sessionmaker(bind = engine)
#и объект класса для работы
session = Session()
#не забываем закрывать сессию
session.close()

