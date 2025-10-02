from import_export import resources
from .models import Container, Document, PaymentPlan, ShippingLine

class ContainerResource(resources.ModelResource):
    class Meta:
        model = Container
        import_id_fields = ('id',)  # ajusta según tu modelo
        fields = '__all__'

class DocumentResource(resources.ModelResource):
    class Meta:
        model = Document
        import_id_fields = ('id',)
        fields = '__all__'

class PaymentPlanResource(resources.ModelResource):
    class Meta:
        model = PaymentPlan
        import_id_fields = ('id',)
        fields = '__all__'

class ShippingLineResource(resources.ModelResource):
    class Meta:
        model = ShippingLine
        import_id_fields = ('id',)
        fields = '__all__'
