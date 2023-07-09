import pdb
import psycopg2
from models.products import Product
from models.basket_product import BasketProduct
import uuid


conn = psycopg2.connect(
                host="localhost",
                port = 5432,
                dbname="postgres"
            )

    # Crear un cursor para ejecutar consultas
cursor = conn.cursor()


class Order:
    def __init__(self, data):
        self.id = data[0]
        self.status = data[1]
        self.created_at = data[2]
        self.updated_at = data[3]
        self.basket_id = data[4]
        self.user_id = data[5]

    @classmethod
    def create(cls,user_id):
        #create unique key
        uniqueid=str(uuid.uuid4())
        order_id = f'{uniqueid[:8]}{user_id}'
        query = '''insert into smartstats.orders(id,status,created_at,updated_at,basket_id,user_id) values %s, %s, NOW(), NOW(), %s, %s;'''
        cursor.execute(query, (
            order_id,
            'pending',
            user_id,
            user_id,
        ))
        cursor.commit()
        results = cls.get(order_id)
        return cls(results[0])

    @classmethod
    def get(cls,id):
        query='SELECT * FROM orders WHERE id=%s'
        cursor.execute(query,(id,))
        row=cursor.fetchone()
        return cls(row)
