from django.test import TestCase
from umi.gestion.models import (
    ShippingLine,
    Port,
    CustomsAgent,
    Product,
    BillOfLading,
    Transshipment,
    Container,
    Document,
    PaymentCategory,
    PaymentPlan,
    PaymentAttachment,
    Supplier
)
from datetime import date


class ShippingLineModelTest(TestCase):
    def test_create_shipping_line(self):
        line = ShippingLine.objects.create(
            name="Maersk",
            contact_emails=["info@maersk.com"],
            phone_numbers=["+58-412-5551234"]
        )
        self.assertEqual(str(line), "Maersk")
        self.assertIn("info@maersk.com", line.contact_emails)


class PortModelTest(TestCase):
    def test_port_str_and_type(self):
        port = Port.objects.create(name="Puerto Cabello", country="Venezuela", port_type="departure")
        self.assertIn("Departure Port", str(port))
        self.assertEqual(port.port_type, "departure")


class CustomsAgentModelTest(TestCase):
    def test_agent_str(self):
        agent = CustomsAgent.objects.create(name="Agencia Aduanal XYZ")
        self.assertEqual(str(agent), "Agencia Aduanal XYZ")


class ProductModelTest(TestCase):
    def test_characteristics_default_empty_dict(self):
        product = Product.objects.create(
            code="TV-55",
            description="Smart TV 55 pulgadas",
            characteristics=None
        )
        self.assertEqual(product.characteristics, {})
        self.assertIn("TV-55", str(product))


class BillOfLadingModelTest(TestCase):
    def setUp(self):
        self.line = ShippingLine.objects.create(name="Evergreen")
        self.departure = Port.objects.create(name="Shanghai", port_type="departure")
        self.arrival = Port.objects.create(name="Puerto Cabello", port_type="arrival")

    def test_create_bill_of_lading(self):
        bl = BillOfLading.objects.create(
            number_bl="BL001",
            invoice_number="INV001",
            shipping_line=self.line,
            etd=date.today(),
            eta=date.today(),
            investment=5000.00,
            departure_port=self.departure,
            arrival_port=self.arrival
        )
        self.assertEqual(str(bl), "BL BL001")
        self.assertEqual(bl.departure_port.name, "Shanghai")


class TransshipmentModelTest(TestCase):
    def test_create_transshipment(self):
        line = ShippingLine.objects.create(name="MSC")
        port = Port.objects.create(name="Panamá", port_type="transshipment")
        bl = BillOfLading.objects.create(
            number_bl="BL123",
            invoice_number="INV123",
            shipping_line=line,
            etd=date.today(),
            eta=date.today(),
            investment=1500.00
        )
        trans = Transshipment.objects.create(
            bill_of_lading=bl,
            port=port,
            notes="Cambio de contenedor",
            date=date.today()
        )
        self.assertIn("Transshipment via", str(trans))


class ContainerModelTest(TestCase):
    def test_create_container(self):
        line = ShippingLine.objects.create(name="CMA CGM")
        bl = BillOfLading.objects.create(
            number_bl="BL002",
            invoice_number="INV002",
            shipping_line=line,
            etd=date.today(),
            eta=date.today(),
            investment=2500.00
        )
        container = Container.objects.create(bill_of_lading=bl, container_number="CONT123")
        self.assertEqual(str(container), "CONT123")


class DocumentModelTest(TestCase):
    def test_create_document(self):
        line = ShippingLine.objects.create(name="APL")
        bl = BillOfLading.objects.create(
            number_bl="BL100",
            invoice_number="INV100",
            shipping_line=line,
            etd=date.today(),
            eta=date.today(),
            investment=3000.00
        )
        doc = Document.objects.create(
            bill_of_lading=bl,
            name="Certificado",
            is_sencamer=True
        )
        self.assertEqual(str(doc), "Certificado")
        self.assertTrue(doc.is_sencamer)


class PaymentModelsTest(TestCase):
    def test_payment_category_and_plan(self):
        category = PaymentCategory.objects.create(name="Freight")
        payment = PaymentPlan.objects.create(
            invoice_number="INV-900",
            invoice_date=date.today(),
            category=category,
            provider="Maersk",
            pi_number="PI123",
            amount=500.00
        )
        self.assertIn("INV-900", str(payment))
        self.assertEqual(payment.status, "pending")

    def test_payment_attachment(self):
        payment = PaymentPlan.objects.create(
            invoice_number="INV-901",
            invoice_date=date.today(),
            provider="Maersk",
            pi_number="PI321",
            amount=800.00
        )
        attachment = PaymentAttachment.objects.create(payment=payment, file="payment_attachments/test.pdf")
        self.assertIn("Attachment for INV-901", str(attachment))


class SupplierModelTest(TestCase):
    def test_supplier_str(self):
        supplier = Supplier.objects.create(name="LG Electronics", contact_person="María López")
        self.assertEqual(str(supplier), "LG Electronics")
