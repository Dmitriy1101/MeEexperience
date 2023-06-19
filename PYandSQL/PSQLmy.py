#Функция, создающая структуру БД (таблицы)+
#Функция, позволяющая добавить нового клиента+
#Функция, позволяющая добавить телефон для существующего клиента+
#Функция, позволяющая изменить данные о клиенте+
#Функция, позволяющая удалить телефон для существующего клиента+
#Функция, позволяющая удалить существующего клиента+
#Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)+
#Функции выше являются обязательными, но это не значит что должны быть только они. При необходимости можете создавать дополнительные функции и классы.

import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
            cur.execute('''
                DROP TABLE IF EXISTS phone;
            ''')
            
            cur.execute('''
                DROP TABLE IF EXISTS client;
            ''')

            cur.execute('''
                CREATE TABLE IF NOT EXISTS client (
                id SERIAL PRIMARY KEY,
                name VARCHAR(40) NOT NULL,
                surname VARCHAR(40) NOT NULL,
                mail VARCHAR(40) NOT NULL          
                );
                ''')
                
            cur.execute('''
                CREATE TABLE IF NOT EXISTS phone (
                id_client INTEGER REFERENCES client(id),
                name VARCHAR(40)        
            );
            ''')
            
            conn.commit()
            print('База собрана')

            
def add_client(conn, name, surname, mail, phone=None):
    with conn.cursor() as cur:
        
        cur.execute(f'''
            insert into client (name, surname, mail) values 
            ('{name}', '{surname}', '{mail}')         
        ;
        ''')
        
        conn.commit()
    
        if phone != None:
            cur.execute(f'''
                insert into phone (id_client, name) values 
                ((select id from client where name = '{name}' and surname = '{surname}' and mail = '{mail}'), '{phone}')         
            ;
            ''')
            
        conn.commit()
    print(f'Добавлен клиент. {name}')

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        
        cur.execute(f'''
            insert into phone (id_client, name) values 
            ({client_id}, '{phone}')         
        ;
        ''')
                
        conn.commit()
    print('Добавлен телефон клиенту.')

def change_client(conn, client_id, name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        
        if name != None:
            cur.execute(f'''
                update client (name) set 
                name = '{name}' where id = {client_id}     
            );
            ''')
            
        if surname != None:
            cur.execute(f'''
                update client (surname) set 
                 surname = '{surname}' where id = {client_id}     
            );
            ''') 
            
        if email != None:
            cur.execute(f'''
                update client (mail) set 
                mail = '{email}' where id = {client_id}     
            );
            ''')        
        
        if phone != None:
            add_phone(conn, client_id, phone)
        
        conn.commit()
        
    print(f'Клиент индекс:{client_id} изменен')

def delete_phone(conn, client_id, phone):
    
    with conn.cursor() as cur:
        
        cur.execute(f'''
            delete from phone where 
            id_client = '{client_id}' and name='{phone}'         
        ;
        ''')
        
        conn.commit()
        
        print(f'Клиент индекс:{client_id} потерял телефон:{phone} ')

def delete_all_client(conn):
    
    with conn.cursor() as cur:
        
        cur.execute(f'''
            delete from phone          
        ;
        ''')
        
        cur.execute(f'''
            delete from client; 
            ALTER SEQUENCE client_id_seq RESTART WITH 1;
            UPDATE client SET id=nextval('client_id_seq');          
        ;
        ''')
               
        conn.commit()
        
        print(f'Клиенты на выход')
        
def delete_client(conn, client_id ):
    
    with conn.cursor() as cur:
        
        cur.execute(f'''
            delete from phone where 
            id_client = '{client_id}'          
        ;
        ''')
        
        cur.execute(f'''
            delete from client where 
            id = '{client_id}'          
        ;
        ''')
               
        conn.commit()
        
        print(f'Клиент индекс:{client_id} ушел')

def find_client(conn, name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        
        str_conn = ''
        
        if name != None:
            str_conn += f"c.name like '{name}'"
                        
        if surname != None:
            if str_conn != '':
                str_conn += ' and '
            str_conn += f"c.surname like '{surname}'"
            
        if email != None:
            if str_conn != '':
                str_conn += ' and '
            str_conn += f"c.mail like '{email}'"        
        
        if phone != None:
            if str_conn != '':
                str_conn += ' and '
            str_conn += f"p.name like '{phone}'" 
            
        if str_conn != '':
            str_conn = f" where {str_conn}"
        
        cur.execute(f'''
            select c.id, c.name, c.surname, c.mail, p.name from client c left join phone p on c.id = p.id_client
            {str_conn}    
        ;
        ''')
        
        ans = cur.fetchall()
        print(ans)
        return ans
def find_phone(conn, client_id):
    with conn.cursor() as cur:
        
        cur.execute(f'''
            select name from phone where 
            id_client = '{client_id}'          
        ;
        ''')
                
        conn.commit()
        
        ans = cur.fetchall()
        print(f'Телефончики. {ans}')
        return ans


#with psycopg2.connect(database='music_service', user='postgres', password='NotGoodNotBad') as conn:
            
        

#conn.close()
