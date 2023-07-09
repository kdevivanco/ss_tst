import pdb
import psycopg2

conn = psycopg2.connect(
                host="localhost",
                port = 5432,
                dbname="postgres"
            )

    # Crear un cursor para ejecutar consultas
cursor = conn.cursor()


class Product:
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.brand = data[2]
        self.image_path = data[3]
        self.description = data[4]
        self.store_price = data[5]
        self.supplier_price = data[6]

    @classmethod
    def get_by_category(cls,categoryname):
        query='''SELECT product_id FROM smartstats.product_categories where categories_id = %s;'''
        cursor.execute(query,(categoryname,))
        results = cursor.fetchall()
        p = []
        for id in results: 
            p.append(cls.find_one(id))
        return p
    
    @classmethod
    def sort_by_price(cls,value,prefilter):
        brand = prefilter['brand']
        category = prefilter['category']
        if value == 'high_to_low':
            if brand == 'not_selected':
                query='''SELECT * FROM smartstats.products where category = %s ORDER BY store_price DESC;'''
                cursor.execute(query,(category,))
                results = cursor.fetchall()
                return cls.classify_all(results)
            else:
                query='''SELECT * FROM smartstats.products where category =%s AND brand = %s ORDER BY store_price DESC;'''
                cursor.execute(query,(category,brand,))
                results = cursor.fetchall()
                return cls.classify_all(results)
        elif value == 'low_to_high':
            if brand == 'not_selected':
                query='''SELECT * FROM smartstats.products where category = %s ORDER BY store_price ASC;'''
                cursor.execute(query,(category,))
                results = cursor.fetchall()
                return cls.classify_all(results)
            else:
                query='''SELECT * FROM smartstats.products where category =%s AND brand = %s ORDER BY store_price ASC;'''
                cursor.execute(query,(category,brand,))
                results = cursor.fetchall()
                return cls.classify_all(results)
        else:
            return None

    @classmethod #Product.find_one(product_id)
    def find_one(cls,product_id):
        query='''SELECT * FROM smartstats.products where id = %s;'''
        cursor.execute(query,(product_id,))
        results = cursor.fetchall()
        return cls(results[0])
    
    @classmethod
    def classify(cls,results):
        p = []
        for product in results:
            p.append(cls(product))
        return p