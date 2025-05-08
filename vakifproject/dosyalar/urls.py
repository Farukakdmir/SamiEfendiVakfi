from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DosyaViewSet, AileBilgisiViewSet, BelgeViewSet,
    DurumDegisikligiViewSet, MaddiYardimViewSet,
    SahsiYardimViewSet
)

router = DefaultRouter()
router.register(r'dosyalar', DosyaViewSet)
router.register(r'aile-bilgileri', AileBilgisiViewSet)
router.register(r'belgeler', BelgeViewSet)
router.register(r'durum-degisiklikleri', DurumDegisikligiViewSet)
router.register(r'maddi-yardimlar', MaddiYardimViewSet)
router.register(r'sahsi-yardim', SahsiYardimViewSet)

app_name = 'dosyalar'

urlpatterns = [
    path('', include(router.urls)),
    path('deleted-dosyalar/', DosyaViewSet.as_view({'get': 'deleted'}), name='deleted-dosyalar'),
] 