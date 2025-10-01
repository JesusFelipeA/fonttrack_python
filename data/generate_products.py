from faker import Faker
from datetime import datetime
import random

fake = Faker()

# Categorías simuladas
CATEGORIES = ["electrónica", "ropa", "hogar", "libros", "juguetes", "deportes", "belleza"]

def generate_product(index):
    return {
        "name": f"{fake.word().capitalize()}_{index}",
        "description": fake.sentence(nb_words=8),
        "price": round(random.uniform(10.0, 1500.0), 2),
        "stock": random.randint(1, 1000),
        "category": random.choice(CATEGORIES),
        "created_at": datetime.utcnow()
    }

def generate_bulk_products(total=500_000, batch_size=5000):
    """
    Genera productos en lotes para inserción eficiente.
    """
    for i in range(total // batch_size):
        yield [generate_product(index=i * batch_size + j) for j in range(batch_size)]
