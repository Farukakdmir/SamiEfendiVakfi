# Vakıf Projesi - Backend

Bu proje, Vakıf uygulamasının Django REST Framework ile oluşturulmuş backend kısmıdır. Frontend Vue.js ile geliştirilmiştir.

## Özellikler

- Dosya kayıtları yönetimi
- Aile bilgileri yönetimi
- Belge yükleme ve görüntüleme
- Durum değişikliği takibi
- Token tabanlı kullanıcı kimlik doğrulama
- Admin panel

## Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- Virtual Environment (venv)

### Adımlar

1. Sanal ortamı aktifleştirin:

```
venv\Scripts\activate
```

2. Gerekli paketleri yükleyin:

```
pip install -r requirements.txt
```

3. Veritabanını oluşturun:

```
python manage.py migrate
```

4. Süper kullanıcı oluşturun:

```
python manage.py createsuperuser
```

5. Sunucuyu başlatın:

```
python manage.py runserver
```

## API Endpointleri

### Kimlik Doğrulama

- `POST /api/auth/login/`: Kullanıcı girişi
- `POST /api/auth/logout/`: Kullanıcı çıkışı
- `POST /api/auth/register/`: Yeni kullanıcı kaydı

### Dosya İşlemleri

- `GET /api/dosyalar/`: Tüm dosyaları listele
- `POST /api/dosyalar/`: Yeni dosya oluştur
- `GET /api/dosyalar/{id}/`: Dosya detaylarını görüntüle
- `PUT /api/dosyalar/{id}/`: Dosyayı güncelle
- `DELETE /api/dosyalar/{id}/`: Dosyayı sil (arşivle)
- `POST /api/dosyalar/{id}/update_status/`: Dosya durumunu güncelle
- `POST /api/dosyalar/restore/`: Silinmiş dosyayı geri yükle
- `GET /api/dosyalar/stats/`: Dosya istatistiklerini görüntüle
- `GET /api/deleted-dosyalar/`: Silinmiş dosyaları listele

### Aile Bilgileri

- `GET /api/aile-bilgileri/?dosya={id}`: Bir dosyaya ait aile bilgilerini listele
- `POST /api/aile-bilgileri/`: Yeni aile bilgisi ekle
- `PUT /api/aile-bilgileri/{id}/`: Aile bilgisini güncelle
- `DELETE /api/aile-bilgileri/{id}/`: Aile bilgisini sil

### Belgeler

- `GET /api/belgeler/?dosya={id}`: Bir dosyaya ait belgeleri listele
- `POST /api/belgeler/`: Yeni belge yükle
- `DELETE /api/belgeler/delete_belge/?dosya={id}&belge_turu={tur}`: Belgeyi sil

## Veritabanı Şeması

### Dosya Modeli

- dosya_no (AutoField, PK)
- kayit_tarihi (DateField)
- ad, soyad, kimlik_no (CharField)
- uyruk, durum, kira_durumu (ChoiceField)
- telefon (CharField)
- adres bilgileri (ilce, mahalle, cadde_sokak, bina_no, daire_no)
- gelir_durumu (DecimalField)
- dolduran_kisi (CharField)
- durum (ChoiceField: BEKLEMEDE, ONAYLANDI, REDDEDILDI)

### AileBilgisi Modeli

- dosya (ForeignKey)
- ad, soyad, kimlik_no (CharField)
- yakinlik (ChoiceField)
- cinsiyet (ChoiceField)
- dogum_tarihi (DateField)
- engel_durumu (BooleanField)

### Belge Modeli

- dosya (ForeignKey)
- belge_turu (ChoiceField)
- belge (FileField)
- yukleme_tarihi (DateTimeField)

### DurumDegisikligi Modeli

- dosya (ForeignKey)
- eski_durum, yeni_durum (ChoiceField)
- degisiklik_tarihi (DateTimeField)
- aciklama (TextField)
- degistiren (ForeignKey: User)

## Frontend Entegrasyonu

Bu backend, Vue.js ile oluşturulmuş frontend ile çalışmak üzere tasarlanmıştır. Frontend kısmı için `/FrontendVakıf` dizinine bakınız.

## Lisans

Bu proje özel kullanım içindir.
