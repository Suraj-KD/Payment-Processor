from django.urls import path
from api.views import PaymentView


urlpatterns = [
    path('processTransaction', PaymentView.as_view(), name='process_transaction'),
]
