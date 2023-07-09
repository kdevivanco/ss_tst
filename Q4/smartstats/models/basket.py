import pdb
import psycopg2
from models.products import Product
from models.basket_product import BasketProduct

conn = psycopg2.connect(
                host="localhost",
                port = 5432,
                dbname="postgres"
            )

    # Crear un cursor para ejecutar consultas
cursor = conn.cursor()

class Basket:
    def __init__(self, data):
        self.id = data[0]
        self.total_price = data[1]
        self.user_id = data[2]
        self.prod_quantity = data[3]

    @classmethod
    def add_products(cls,product_id,quantity,client_id):
        #update selected_products table set product_id to =
        query = "INSERT INTO smartstats.selected_products (product_id, basket_id, user_id,quantity) VALUES (%s, %s,%s,%s)"
        cursor.execute(query,(product_id,client_id, client_id,quantity,))
        conn.commit()
        return True
    
    @classmethod
    def get_products(cls,client_id):
        query = "SELECT product_id FROM smartstats.selected_products WHERE user_id = %s"
        cursor.execute(query,(client_id,))
        products = []
        results = cursor.fetchall()
        for id in results: 
            products.append(BasketProduct.get(id))
        return products
    
    @classmethod
    def get(cls, user_id):
        query = "SELECT * FROM smartstats.basket WHERE user_id = %s"
        cursor.execute(query,(user_id,))
        results = cursor.fetchall()
        return cls(results[0])
    

    @classmethod
    def delete_product(cls,product_id,client_id):
        query = "DELETE FROM smartstats.selected_products WHERE product_id = %s AND user_id = %s"
        cursor.execute(query,(product_id,client_id,))
        conn.commit()
        return True

    @classmethod
    def change_quantity(cls,new_quant,client_id, product_id):
        query = "UPDATE smartstats.selected_products SET quantity = %s WHERE user_id = %s AND product_id = %s"
        cursor.execute(query,(new_quant,client_id,product_id,))
        conn.commit()
        return True
    
    @classmethod
    def get_price(cls,user_id):
        query='''SELECT total_price FROM smartstats.basket WHERE user_id=%s '''
        cursor.execute(query,(user_id,))
        results = cursor.fetchall()
        return int(results[0])


