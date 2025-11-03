# Centraliza todos los modelos del módulo gestion
from .bill_of_lading import BillOfLading
from .container import Container
from .customs import CustomsAgent
from .document import Document
from .payment import PaymentPlan, PaymentCategory
from .port import Port
from .product import Product
from .shipping import ShippingLine
from .supplier import Supplier

# Opcional: define qué se exporta al usar `from umi.gestion.models import *`
__all__ = [
    "BillOfLading",
    "Container",
    "CustomsAgent",
    "Document",
    "PaymentPlan",
    "PaymentCategory",
    "Port",
    "Product",
    "ShippingLine",
    "Supplier",
]
