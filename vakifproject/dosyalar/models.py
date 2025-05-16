from django.db import models
from django.contrib.auth.models import User

# Seçenek Sabitleri
class UyrukSecenekleri(models.TextChoices):
    TURKIYE = 'TC', 'Türkiye'
    SURIYE = 'SURIYE', 'Suriye'
    IRAK = 'IRAK', 'Irak'
    IRAN = 'IRAN', 'İran'
    AFGANISTAN = 'AFGANISTAN', 'Afganistan'
    SUDAN = 'SUDAN', 'Sudan'
    DIGER = 'DIGER', 'Diğer'

class DurumSecenekleri(models.TextChoices):
    BEKLEMEDE = 'BEKLEMEDE', 'Beklemede'
    ONAYLANDI = 'ONAYLANDI', 'Onaylandı'
    REDDEDILDI = 'REDDEDILDI', 'Reddedildi'

class KiraDurumuSecenekleri(models.TextChoices):
    KIRACI = 'KIRACI', 'Kiracı'
    EV_SAHIBI = 'EV_SAHIBI', 'Ev Sahibi'

class YakinlikSecenekleri(models.TextChoices):
    KENDISI = 'KENDISI', 'Kendisi'
    ES = 'ES', 'Eş'
    COCUK = 'COCUK', 'Çocuk'
    ANNE = 'ANNE', 'Anne'
    BABA = 'BABA', 'Baba'
    KARDES = 'KARDES', 'Kardeş'
    DIGER = 'DIGER', 'Diğer'

class CinsiyetSecenekleri(models.TextChoices):
    ERKEK = 'E', 'Erkek'
    KADIN = 'K', 'Kadın'

class BelgeTuruSecenekleri(models.TextChoices):
    KONTRAT = 'KONTRAT', 'Kontrat'
    OLUM_BELGESI = 'OLUM_BELGESI', 'Ölüm Belgesi'
    VUKUATLI_NUFUS = 'VUKUATLI_NUFUS', 'Vukuatlı Nüfus Kayıt Örneği'
    OGRENCI_BELGESI = 'OGRENCI_BELGESI', 'Öğrenci Belgesi'
    BANKA_EKSTRESI = 'BANKA_EKSTRESI', 'Banka Ekstresi'
    TEMVIYYE = 'TEMVIYYE', 'Temviyye'

# Ana Dosya Modeli
class Dosya(models.Model):
    id = models.AutoField(primary_key=True)
    dosya_no = models.IntegerField(unique=True)
    kayit_tarihi = models.DateField()
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    kimlik_no = models.CharField(max_length=20)
    profil_resmi = models.ImageField(upload_to='profil_resimleri/%Y/%m/', null=True, blank=True)
    uyruk = models.CharField(
        max_length=20,
        choices=UyrukSecenekleri.choices,
        default=UyrukSecenekleri.TURKIYE
    )
    telefon = models.CharField(max_length=20)
    ilce = models.CharField(max_length=100, default='Yeni Mahalle')
    mahalle = models.CharField(max_length=100)
    cadde_sokak = models.CharField(max_length=100)
    bina_no = models.CharField(max_length=20)
    daire_no = models.CharField(max_length=20)
    kira_durumu = models.CharField(
        max_length=20,
        choices=KiraDurumuSecenekleri.choices
    )
    gelir_durumu = models.DecimalField(max_digits=10, decimal_places=2)
    dolduran_kisi = models.CharField(max_length=100)
    iban = models.CharField(max_length=50, blank=True, null=True)
    yardim_aldigi_yerler = models.TextField(blank=True, null=True)
    durum = models.CharField(
        max_length=20,
        choices=DurumSecenekleri.choices,
        default=DurumSecenekleri.BEKLEMEDE
    )
    engel_durumu = models.BooleanField(default=False, verbose_name="Engel Durumu")
    notlar = models.TextField(blank=True, null=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    silinme_tarihi = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'dosyalar'
        ordering = ['dosya_no']
        default_related_name = 'dosyalar'
        
    def __str__(self):
        return f"{self.dosya_no} - {self.ad} {self.soyad}"

# Aile Bilgileri Modeli
class AileBilgisi(models.Model):
    dosya = models.ForeignKey(
        Dosya, 
        on_delete=models.CASCADE, 
        related_name='aile_bilgileri'
    )
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    kimlik_no = models.CharField(max_length=20, blank=True, null=True)
    yakinlik = models.CharField(max_length=20)
    cinsiyet = models.CharField(max_length=1)
    dogum_tarihi = models.DateField(null=True, blank=True)
    engel_durumu = models.BooleanField(null=True, blank=True)
    engel_aciklama = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'aile_bilgileri'
        
    def __str__(self):
        return f"{self.ad} {self.soyad} - {self.get_yakinlik_display()}"

# Belge Modeli
class Belge(models.Model):
    dosya = models.ForeignKey(
        Dosya, 
        on_delete=models.CASCADE, 
        related_name='belgeler'
    )
    belge_turu = models.CharField(
        max_length=50,
        choices=BelgeTuruSecenekleri.choices
    )
    belge = models.FileField(upload_to='belgeler/%Y/%m/')
    yukleme_tarihi = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'belgeler'
        unique_together = ('dosya', 'belge_turu')
        
    def __str__(self):
        return f"{self.dosya.dosya_no} - {self.get_belge_turu_display()}"
    
    @property
    def belge_url(self):
        if self.belge:
            return self.belge.url
        return None

# Durum Değişikliği Geçmişi
class DurumDegisikligi(models.Model):
    dosya = models.ForeignKey(
        Dosya, 
        on_delete=models.CASCADE, 
        related_name='durum_degisiklikleri'
    )
    eski_durum = models.CharField(
        max_length=20,
        choices=DurumSecenekleri.choices
    )
    yeni_durum = models.CharField(
        max_length=20,
        choices=DurumSecenekleri.choices
    )
    degisiklik_tarihi = models.DateTimeField(auto_now_add=True)
    aciklama = models.TextField(blank=True, null=True)
    degistiren = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    class Meta:
        db_table = 'durum_degisiklikleri'
        ordering = ['-degisiklik_tarihi']
        
    def __str__(self):
        return f"{self.dosya.dosya_no} - {self.eski_durum} -> {self.yeni_durum}"

class MaddiYardim(models.Model):
    yardim_yapan_ad_soyad = models.CharField(max_length=100, verbose_name="Yardım Yapan Ad Soyad", default="")
    yardim_yapan_telefon = models.CharField(max_length=20, verbose_name="Yardım Yapan Telefon", default="")
    yardim_tutar = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Yardım Tutarı")
    tutar = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Toplam Tutar")
    aciklama = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Maddi Yardım"
        verbose_name_plural = "Maddi Yardımlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.yardim_yapan_ad_soyad} - {self.tutar} TL"

    def save(self, *args, **kwargs):
        if self.pk:  # Eğer kayıt zaten varsa
            # Dosya tutarlarını hesapla
            dosya_tutarlari = sum(dt.tutar for dt in self.dosya_tutarlari.all())
            # Manuel kayıt tutarlarını hesapla
            manuel_tutarlar = sum(mk.tutar for mk in self.manuel_kayitlar.all())
            # Toplam tutarı güncelle
            self.tutar = dosya_tutarlari + manuel_tutarlar
        super().save(*args, **kwargs)

class DosyaTutari(models.Model):
    maddi_yardim = models.ForeignKey(
        MaddiYardim,
        on_delete=models.CASCADE,
        related_name='dosya_tutarlari'
    )
    dosya = models.ForeignKey(
        Dosya,
        on_delete=models.CASCADE,
        related_name='yardim_tutarlari',
        null=True,
        blank=True
    )
    tutar = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Dosya Tutarı"
        verbose_name_plural = "Dosya Tutarları"
        unique_together = [('maddi_yardim', 'dosya')]

    def __str__(self):
        return f"{self.dosya} - {self.tutar} TL"

class SahsiYardim(models.Model):
    YARDIM_TIPLERI = [
        ('individual', 'Bireysel'),
        ('group', 'Grup'),
    ]

    yardim_tipi = models.CharField(max_length=20, choices=YARDIM_TIPLERI)
    ad_soyad = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    grup_uye_sayisi = models.IntegerField(null=True, blank=True)
    dosyalar = models.ManyToManyField('Dosya', related_name='sahsi_yardimlar')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ad_soyad} - {self.get_yardim_tipi_display()}"

class SahsiYardimci(models.Model):
    yardim = models.ForeignKey(SahsiYardim, on_delete=models.CASCADE, related_name='yardimcilar')
    ad_soyad = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)

    def __str__(self):
        return self.ad_soyad

class ManuelMaddiYardim(models.Model):
    ad_soyad = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    adres = models.TextField()
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    aciklama = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ad_soyad} - {self.tutar} TL"

    class Meta:
        verbose_name = "Manuel Maddi Yardım"
        verbose_name_plural = "Manuel Maddi Yardımlar"
        ordering = ['-created_at']

class ManuelMaddiYardimKayit(models.Model):
    maddi_yardim = models.ForeignKey(MaddiYardim, on_delete=models.CASCADE, related_name='manuel_kayitlar')
    ad_soyad = models.CharField(max_length=100)
    tc_kimlik = models.CharField(max_length=11)
    telefon = models.CharField(max_length=20)
    adres = models.TextField()
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    aciklama = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'manuel_maddi_yardim_kayitlar'
        verbose_name = 'Manuel Maddi Yardım Kaydı'
        verbose_name_plural = 'Manuel Maddi Yardım Kayıtları'

    def __str__(self):
        return f"{self.ad_soyad} - {self.tutar} TL"
