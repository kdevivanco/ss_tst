import pdb
import psycopg2
from models.products import Product

conn = psycopg2.connect(
                host="localhost",
                port = 5432,
                dbname="postgres"
            )

    # Crear un cursor para ejecutar consultas
cursor = conn.cursor()


class BasketProduct:
    def __init__(self, data):
        self.product_id = data[0]
        self.basket_id = data[1]
        self.user_id = data[2]
        self.quantity = data[3]
        self.price = data[4]

    @classmethod
    def create(cls,form_data,product_id,user_id):
        query = "INSERT INTO smartstats.selected_products (product_id,basket_id, user_id,quantity) VALUES (%s, %s,%s,%s)"
        cursor.execute(query,(product_id,user_id,user_id,form_data['quantity'],))
        conn.commit()
        return True
    
    @classmethod
    def get_all(cls,user_id):
        query = "SELECT * FROM smartstats.selected_products WHERE user_id = %s"
        cursor.execute(query,(user_id,))
        results = cursor.fetchall()
        prod_list = []
        for res in results:
            product = cls(res)
            product.data = Product.find_one(product.product_id)
            prod_list.append(product)
        return prod_list
    
   