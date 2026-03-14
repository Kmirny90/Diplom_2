from faker import Faker
import random
import string

fake = Faker()

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_data():
    return {
        "email": fake.email(),
        "password": fake.password(length=10),
        "name": fake.first_name()
    }