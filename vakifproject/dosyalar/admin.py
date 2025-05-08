from django.contrib import admin
from .models import Dosya, AileBilgisi, Belge, DurumDegisikligi, ManuelMaddiYardimKayit

class AileBilgisiInline(admin.TabularInline):
    model = AileBilgisi
    extra = 0

class BelgeInline(admin.TabularInline):
    model = Belge
    extra = 0

class DurumDegisikligiInline(admin.TabularInline):
    model = DurumDegisikligi
    extra = 0
    readonly_fields = ('degisiklik_tarihi',)

@admin.register(Dosya)
class DosyaAdmin(admin.ModelAdmin):
    list_display = ('dosya_no', 'ad', 'soyad', 'kimlik_no', 'durum', 'kayit_tarihi', 'is_deleted')
    list_filter = ('durum', 'is_deleted', 'uyruk', 'ilce')
    search_fields = ('ad', 'soyad', 'kimlik_no', 'dosya_no')
    readonly_fields = ('guncellenme_tarihi',)
    inlines = [AileBilgisiInline, BelgeInline, DurumDegisikligiInline]

@admin.register(AileBilgisi)
class AileBilgisiAdmin(admin.ModelAdmin):
    list_display = ('id', 'dosya', 'ad', 'soyad', 'yakinlik', 'engel_durumu')
    list_filter = ('yakinlik', 'engel_durumu')
    search_fields = ('ad', 'soyad', 'kimlik_no')

@admin.register(Belge)
class BelgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'dosya', 'belge_turu', 'yukleme_tarihi')
    list_filter = ('belge_turu', 'yukleme_tarihi')
    search_fields = ('dosya__ad', 'dosya__soyad')

@admin.register(DurumDegisikligi)
class DurumDegisikligiAdmin(admin.ModelAdmin):
    list_display = ('id', 'dosya', 'eski_durum', 'yeni_durum', 'degisiklik_tarihi', 'degistiren')
    list_filter = ('eski_durum', 'yeni_durum', 'degisiklik_tarihi')
    search_fields = ('dosya__ad', 'dosya__soyad', 'aciklama')
    readonly_fields = ('degisiklik_tarihi',)

@admin.register(ManuelMaddiYardimKayit)
class ManuelMaddiYardimKayitAdmin(admin.ModelAdmin):
    list_display = ('ad_soyad', 'tc_kimlik', 'telefon', 'tutar', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('ad_soyad', 'tc_kimlik', 'telefon')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
