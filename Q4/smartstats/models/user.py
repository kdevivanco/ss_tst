from datetime import datetime
import pdb
from datetime import datetime
import psycopg2
import uuid
import random
from faker import Faker

# # Create an instance of Faker
fake = Faker()

conn = psycopg2.connect(
                host="localhost",
                port = 5432,
                dbname="postgres"
            )

    # Crear un cursor para ejecutar consultas
cursor = conn.cursor()


class User:
    def __init__(self, data):
        self.id = data[0]
        self.first_name = data[1]
        self.last_name = data[2]
        self.email = data[3]
        self.password = data[4]
        self.created_at = data[5]
        self.updated_at = data[6]
        self.date_of_birth = data[7]

    

    @classmethod
    def login(cls, form_data,bcrypt):
        email = form_data['email']

        query='''SELECT password FROM smartstats.users where email = %s;'''  
        cursor.execute(query,(email,))
        results = cursor.fetchall()
        print(results[0][0])
        pdb.set_trace()
        # if (bcrypt.check_password_hash(results[0][0],form_data['password']) or
        if(results[0][0] == form_data['password']):
            valid = True

        if valid:
            user = cls.get_by_email(email)
            return user
        else:
            return False
            


    @classmethod
    def get_by_email(cls,email):
        query='''SELECT * FROM smartstats.users where email = %s;'''  
        cursor.execute(query,(email,))
        results = cursor.fetchall()
        if len(results)>0: 
            return cls(results[0])
        else:
            return False
        

    @classmethod
    def email_free(self, new_email):
        query='''SELECT id FROM smartstats.users where email = %s;'''  
        cursor.execute(query,(new_email,))
        results = cursor.fetchall()
        len(results)
        return len(results)==0


    @classmethod
    def create_code(cls):
        unique_id = str(uuid.uuid4())
        b = random.randint(10,99)
        w = fake.word()  # Generate a random word as the password
        unique_id = f'{unique_id[:8]}{w[-3:-1]}{b}'
        return unique_id
    
    @classmethod
    def create_uid(cls):
        query='''SELECT id from smartstats.users;'''
        cursor.execute(query)
        results = cursor.fetchall()
        used_ids =[]
        for result in results: 
            used_ids.append(result[0])
        unique_id = cls.create_code()
        while unique_id in used_ids:
            unique_id = cls.create_code()

        return unique_id


    @classmethod
    def create(cls, form_data,bcrypt):
        
        # password = bcrypt.generate_password_hash(form_data['password'])
        unique_id = cls.create_uid()
        query = '''
            INSERT INTO smartstats.users
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW(),%s) RETURNING id;
        '''
        cursor.execute(query, (
            unique_id,
            form_data['first_name'],
            form_data['last_name'],
            form_data['email'],
            # password,
            form_data['password'],
            form_data['date_of_birth'],
        ))
        
        conn.commit()
        pdb.set_trace()
        obj = cls.get_by_id(unique_id)
        
        return obj


    @classmethod
    def get_by_id(cls,user_id):
        query='''SELECT * FROM smartstats.users where id = %s;'''  
        cursor.execute(query,(user_id,))
        results = cursor.fetchall()
        return cls(results[0])

    @classmethod
    def edit(self, new_data):
        #missing
        return True