import time
import uuid
from datetime import datetime, timedelta
import random
from faker import Faker
import csv
from flask_bcrypt import Bcrypt

# # Create an instance of Faker
fake = Faker()


def generate_user_data(num_entries):
    start_time = time.time()  # Start the time measurer
    ca = 0
    user_data = []
    for _ in range(num_entries):
        ca +=1
        b = random.randint(10,99)
        c = random.randint(1000, 9999) 
        ead = ['@gmail.com','@outlook.com','@yahoo.com','@yahoo.cm','@yahoo.org','@yahoo.es','@hotmail.com','@company.com','@gov.gov', '@outlook.es','@example.com', '@example.es']
        rand_ead = ead[random.randint(0,(len(ead)-1))]
        lett = ['a','b','c','d','e','p','f','g','h','i','k']
        rand_lett = lett[random.randint(0,(len(lett)-1))]
        unique_id = str(uuid.uuid4())
        first_name = fake.first_name()
        last_name = fake.last_name()
        password = fake.word()  # Generate a random word as the password
        email = f'{first_name.lower()}{last_name.lower()}{c}{rand_lett}{b}{password[:2]}{rand_ead}'  # Append the counter value before '@' and add a domain
        created_at = datetime.now()
        updated_at = created_at + timedelta(days=random.randint(1, 365))
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=70)
        unique_id = f'{unique_id[:8]}{password[-3:-1]}{b}'

        user_entry = {
            'id': unique_id[:12],
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'created_at': created_at,
            'updated_at': updated_at,
            'date_of_birth': date_of_birth
        }
        user_data.append(user_entry)
    # Calculate the elapsed time
    elapsed_time = time.time() - start_time  
    print(elapsed_time)
    return user_data


def save_data_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        # writer.writeheader()
        writer.writerows(data)


# Usage
num_entries = 1000000  # Number of entries to generate
user_data = generate_user_data(num_entries)
filename = 'user_test.csv'
save_data_to_csv(user_data, filename)
