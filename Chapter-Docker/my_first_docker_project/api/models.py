from mongoengine import Document, StringField, DecimalField

class Product(Document):
    nombre = StringField(max_length=100, required=True)
    precio = DecimalField(max_digits=10, decimal_places=2, required=True)
    talla = StringField(max_length=10, required=True)
    
    meta = {
        'collection': 'products'  # Tu colección en MongoDB
    }

