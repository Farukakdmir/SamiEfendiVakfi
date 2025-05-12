from rest_framework import serializers
from .models import Dosya, AileBilgisi, Belge, DurumDegisikligi, MaddiYardim, DosyaTutari, SahsiYardimci, SahsiYardim, ManuelMaddiYardim, ManuelMaddiYardimKayit
from django.db import transaction


class AileBilgisiSerializer(serializers.ModelSerializer):
    class Meta:
        model = AileBilgisi
        fields = '__all__'


class BelgeSerializer(serializers.ModelSerializer):
    belge_turu_adi = serializers.CharField(source='get_belge_turu_display', read_only=True)
    
    class Meta:
        model = Belge
        fields = [
            'id', 'dosya', 'belge_turu', 'belge_turu_adi', 'belge', 
            'belge_url', 'yukleme_tarihi'
        ]
        extra_kwargs = {
            'dosya': {'required': False}
        }


class DurumDegisikligiSerializer(serializers.ModelSerializer):
    eski_durum_adi = serializers.CharField(source='get_eski_durum_display', read_only=True)
    yeni_durum_adi = serializers.CharField(source='get_yeni_durum_display', read_only=True)
    degistiren_adi = serializers.CharField(source='degistiren.username', read_only=True)
    
    class Meta:
        model = DurumDegisikligi
        fields = [
            'id', 'dosya', 'eski_durum', 'eski_durum_adi', 'yeni_durum', 
            'yeni_durum_adi', 'degisiklik_tarihi', 'aciklama', 'degistiren',
            'degistiren_adi'
        ]
        extra_kwargs = {
            'dosya': {'required': False}
        }


class DosyaSerializer(serializers.ModelSerializer):
    aile_bilgileri = AileBilgisiSerializer(many=True, required=False, read_only=True)
    belgeler = BelgeSerializer(many=True, required=False, read_only=True)
    durum_degisiklikleri = DurumDegisikligiSerializer(many=True, read_only=True)
    
    uyruk_adi = serializers.CharField(source='get_uyruk_display', read_only=True)
    durum_adi = serializers.CharField(source='get_durum_display', read_only=True)
    kira_durumu_adi = serializers.CharField(source='get_kira_durumu_display', read_only=True)
    
    class Meta:
        model = Dosya
        fields = [
            'id',
            'dosya_no', 'kayit_tarihi', 'ad', 'soyad', 'kimlik_no', 
            'uyruk', 'uyruk_adi', 'telefon', 'ilce', 'mahalle', 
            'cadde_sokak', 'bina_no', 'daire_no', 'kira_durumu', 
            'kira_durumu_adi', 'gelir_durumu', 'dolduran_kisi', 
            'iban', 'yardim_aldigi_yerler',
            'durum', 'durum_adi', 'notlar', 'guncellenme_tarihi',
            'aile_bilgileri', 'belgeler', 'durum_degisiklikleri',
            'profil_resmi'
        ]
        read_only_fields = ['id', 'dosya_no']
    
    def create(self, validated_data):
        aile_bilgileri_data = validated_data.pop('aile_bilgileri', [])
        last_dosya = Dosya.objects.all().order_by('dosya_no').last()
        validated_data['dosya_no'] = (last_dosya.dosya_no + 1) if last_dosya else 1

        with transaction.atomic():
            dosya = Dosya.objects.create(**validated_data)
            
            for aile_bilgisi_data in aile_bilgileri_data:
                AileBilgisi.objects.create(dosya=dosya, **aile_bilgisi_data)
            
            return dosya
    
    def update(self, instance, validated_data):
        aile_bilgileri_data = validated_data.pop('aile_bilgileri', None)
        
        with transaction.atomic():
            # Önce dosya bilgilerini güncelle
            for attr, value in validated_data.items():
                if attr not in self.Meta.read_only_fields:
                    setattr(instance, attr, value)
            instance.save()
            
            # Sonra aile bilgilerini güncelle
            if aile_bilgileri_data is not None:
                # Önce tüm mevcut aile bilgilerini sil
                instance.aile_bilgileri.all().delete()
                
                # Sonra yeni aile bilgilerini ekle
                for aile_bilgisi_data in aile_bilgileri_data:
                    AileBilgisi.objects.create(dosya=instance, **aile_bilgisi_data)
        
        return instance


class DosyaListSerializer(serializers.ModelSerializer):
    durum_adi = serializers.CharField(source='get_durum_display', read_only=True)
    kira_durumu_adi = serializers.CharField(source='get_kira_durumu_display', read_only=True)
    aile_bilgileri = AileBilgisiSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dosya
        fields = [
            'id', 'dosya_no', 'kayit_tarihi', 'ad', 'soyad', 'kimlik_no', 
            'telefon', 'ilce', 'mahalle', 'cadde_sokak', 'bina_no', 
            'daire_no', 'durum', 'durum_adi', 'kira_durumu', 'kira_durumu_adi',
            'aile_bilgileri'
        ]
        ordering = ['dosya_no']


class DosyaTutariSerializer(serializers.ModelSerializer):
    dosya_bilgisi = DosyaSerializer(source='dosya', read_only=True)
    
    class Meta:
        model = DosyaTutari
        fields = ['id', 'dosya', 'dosya_bilgisi', 'tutar']


class ManuelMaddiYardimKayitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuelMaddiYardimKayit
        fields = ['id', 'ad_soyad', 'tc_kimlik', 'telefon', 'adres', 'tutar', 'aciklama', 'created_at', 'updated_at']


class MaddiYardimSerializer(serializers.ModelSerializer):
    dosya_bilgileri = DosyaTutariSerializer(source='dosya_tutarlari', many=True, read_only=True)
    manuel_kayitlar = ManuelMaddiYardimKayitSerializer(many=True, read_only=True)
    toplam_tutar = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    dosya_tutarlari_list = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    manuel_kayitlar_list = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = MaddiYardim
        fields = [
            'id', 'yardim_yapan_ad_soyad', 'yardim_yapan_telefon',
            'yardim_tutar', 'tutar', 'toplam_tutar', 'aciklama', 'created_at', 'updated_at',
            'dosya_bilgileri', 'manuel_kayitlar',
            'dosya_tutarlari_list', 'manuel_kayitlar_list'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'toplam_tutar']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Toplam tutarı hesapla
        dosya_tutarlari = sum(dt.tutar for dt in instance.dosya_tutarlari.all())
        manuel_tutarlar = sum(mk.tutar for mk in instance.manuel_kayitlar.all())
        toplam_tutar = dosya_tutarlari + manuel_tutarlar
        
        # Tutarları güncelle
        data['tutar'] = toplam_tutar
        data['toplam_tutar'] = toplam_tutar
        data['yardim_tutar'] = instance.yardim_tutar
        
        # Dosya bilgilerini düzenle
        dosya_bilgileri = []
        for dt in instance.dosya_tutarlari.all():
            if dt.dosya:  # Sadece dosyası olan kayıtları ekle
                dosya_bilgileri.append({
                    'id': dt.id,
                    'dosya': dt.dosya.id,
                    'dosya_bilgisi': {
                        'id': dt.dosya.id,
                        'dosya_no': dt.dosya.dosya_no,
                        'ad': dt.dosya.ad,
                        'soyad': dt.dosya.soyad,
                        'telefon': dt.dosya.telefon,
                        'mahalle': dt.dosya.mahalle,
                        'cadde_sokak': dt.dosya.cadde_sokak,
                        'durum': dt.dosya.durum
                    },
                    'tutar': dt.tutar
                })
        data['dosya_bilgileri'] = dosya_bilgileri
        
        # Manuel kayıtları düzenle
        manuel_kayitlar = []
        for mk in instance.manuel_kayitlar.all():
            manuel_kayitlar.append({
                'id': mk.id,
                'ad_soyad': mk.ad_soyad,
                'tc_kimlik': mk.tc_kimlik,
                'telefon': mk.telefon,
                'adres': mk.adres,
                'tutar': mk.tutar,
                'aciklama': mk.aciklama,
                'created_at': mk.created_at,
                'updated_at': mk.updated_at
            })
        data['manuel_kayitlar'] = manuel_kayitlar
        
        return data

    def create(self, validated_data):
        dosya_tutarlari_list = validated_data.pop('dosya_tutarlari_list', [])
        manuel_kayitlar_list = validated_data.pop('manuel_kayitlar_list', [])

        with transaction.atomic():
            # Önce ana kaydı oluştur
            maddi_yardim = MaddiYardim.objects.create(
                yardim_yapan_ad_soyad=validated_data.get('yardim_yapan_ad_soyad', ''),
                yardim_yapan_telefon=validated_data.get('yardim_yapan_telefon', ''),
                yardim_tutar=validated_data.get('yardim_tutar', 0),
                aciklama=validated_data.get('aciklama', '')
            )

            # Sonra dosya tutarlarını ekle
            for tutar_data in dosya_tutarlari_list:
                DosyaTutari.objects.create(
                    maddi_yardim=maddi_yardim,
                    dosya_id=tutar_data.get('dosya'),
                    tutar=tutar_data.get('tutar', 0)
                )

            # Son olarak manuel kayıtları ekle
            for kayit_data in manuel_kayitlar_list:
                ManuelMaddiYardimKayit.objects.create(
                    maddi_yardim=maddi_yardim,
                    ad_soyad=kayit_data.get('ad_soyad'),
                    tc_kimlik=kayit_data.get('tc_kimlik'),
                    telefon=kayit_data.get('telefon'),
                    adres=kayit_data.get('adres'),
                    tutar=kayit_data.get('tutar', 0),
                    aciklama=kayit_data.get('aciklama', '')
                )

            # Toplam tutarı güncelle
            maddi_yardim.save()

        return maddi_yardim

    def update(self, instance, validated_data):
        dosya_tutarlari_list = validated_data.pop('dosya_tutarlari_list', [])
        manuel_kayitlar_list = validated_data.pop('manuel_kayitlar_list', [])

        with transaction.atomic():
            # Ana kaydı güncelle
            instance.yardim_yapan_ad_soyad = validated_data.get('yardim_yapan_ad_soyad', instance.yardim_yapan_ad_soyad)
            instance.yardim_yapan_telefon = validated_data.get('yardim_yapan_telefon', instance.yardim_yapan_telefon)
            instance.yardim_tutar = validated_data.get('yardim_tutar', instance.yardim_tutar)
            instance.aciklama = validated_data.get('aciklama', instance.aciklama)
            instance.save()

            # Mevcut ilişkili kayıtları sil
            instance.dosya_tutarlari.all().delete()
            instance.manuel_kayitlar.all().delete()

            # Yeni dosya tutarlarını ekle
            for tutar_data in dosya_tutarlari_list:
                DosyaTutari.objects.create(
                    maddi_yardim=instance,
                    dosya_id=tutar_data.get('dosya'),
                    tutar=tutar_data.get('tutar', 0)
                )

            # Yeni manuel kayıtları ekle
            for kayit_data in manuel_kayitlar_list:
                ManuelMaddiYardimKayit.objects.create(
                    maddi_yardim=instance,
                    ad_soyad=kayit_data.get('ad_soyad'),
                    tc_kimlik=kayit_data.get('tc_kimlik'),
                    telefon=kayit_data.get('telefon'),
                    adres=kayit_data.get('adres'),
                    tutar=kayit_data.get('tutar', 0),
                    aciklama=kayit_data.get('aciklama', '')
                )

            # Toplam tutarı güncelle
            instance.save()

        return instance


class SahsiYardimciSerializer(serializers.ModelSerializer):
    class Meta:
        model = SahsiYardimci
        fields = ['id', 'ad_soyad', 'telefon']


class SahsiYardimSerializer(serializers.ModelSerializer):
    yardimcilar = SahsiYardimciSerializer(many=True, required=False)
    dosyalar = DosyaSerializer(many=True, read_only=True)
    dosya_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = SahsiYardim
        fields = ['id', 'yardim_tipi', 'ad_soyad', 'telefon', 'grup_uye_sayisi',
                 'dosyalar', 'dosya_ids', 'yardimcilar', 'created_at', 'updated_at']

    def validate(self, data):
        # Frontend'den gelen verileri kontrol et ve dönüştür
        if 'type' in self.initial_data:
            data['yardim_tipi'] = self.initial_data['type']
        if 'name' in self.initial_data:
            data['ad_soyad'] = self.initial_data['name']
        if 'phone' in self.initial_data:
            data['telefon'] = self.initial_data['phone']
        if 'groupSize' in self.initial_data and self.initial_data['groupSize']:
            data['grup_uye_sayisi'] = int(self.initial_data['groupSize'])
        if 'helpers' in self.initial_data:
            data['yardimcilar'] = self.initial_data['helpers']
        if 'dosyalar' in self.initial_data:
            data['dosya_ids'] = self.initial_data['dosyalar']
        return data

    def create(self, validated_data):
        yardimcilar_data = validated_data.pop('yardimcilar', [])
        dosya_ids = validated_data.pop('dosya_ids', [])
        
        yardim = SahsiYardim.objects.create(**validated_data)
        
        # Yardımcıları ekle
        for yardimci_data in yardimcilar_data:
            SahsiYardimci.objects.create(yardim=yardim, **yardimci_data)
        
        # Dosyaları ekle
        if dosya_ids:
            yardim.dosyalar.set(dosya_ids)
        
        return yardim

    def update(self, instance, validated_data):
        yardimcilar_data = validated_data.pop('yardimcilar', [])
        dosya_ids = validated_data.pop('dosya_ids', None)
        
        # Ana modeli güncelle
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Yardımcıları güncelle
        if yardimcilar_data:
            instance.yardimcilar.all().delete()
            for yardimci_data in yardimcilar_data:
                SahsiYardimci.objects.create(yardim=instance, **yardimci_data)
        
        # Dosyaları güncelle
        if dosya_ids is not None:
            instance.dosyalar.set(dosya_ids)
        
        return instance 


class ManuelMaddiYardimSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuelMaddiYardim
        fields = [
            'id', 'ad_soyad', 'telefon', 'adres',
            'tutar', 'aciklama', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at'] 