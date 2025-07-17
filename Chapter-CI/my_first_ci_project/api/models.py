from django.db import models
from mongoengine import Document, StringField, IntField

class Product(Document):
    nombre = StringField(required=True)
    precio = IntField()
    talla = StringField(required=True)

