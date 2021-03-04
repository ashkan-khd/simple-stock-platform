from django.urls import path

from symbols.views import SymbolUpdateRedirectView

urlpatterns = [
    path('<int:pk>/admin_update/', SymbolUpdateRedirectView.as_view(), name='admin-symbol-update'),
]
