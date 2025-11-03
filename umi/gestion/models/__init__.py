# Centraliza todos los modelos del módulo gestion
from .bill_of_lading import BillOfLading
from .container import Container
from .customs import CustomsAgent
from .document import Document
from .payment import PaymentPlan, PaymentCategory, PaymentAttachment
from .port import Port
from .product import Product
from .shipping import ShippingLine
from .supplier import Supplier
from .transshipment import Transshipment

# Opcional: define qué se exporta al usar `from umi.gestion.models import *`
__all__ = [
    "BillOfLading",
    "Container",
    "CustomsAgent",
    "Document",
    "PaymentPlan",
    "PaymentCategory",
    "PaymentAttachment",
    "Port",
    "Product",
    "ShippingLine",
    "Supplier",
    "Transshipment"
]
