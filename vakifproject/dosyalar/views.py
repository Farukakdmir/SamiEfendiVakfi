from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from django.db.models import Q, Count, F, Value, IntegerField, ExpressionWrapper
from django.http import HttpResponse
import xlsxwriter
from io import BytesIO
import logging

from .models import Dosya, AileBilgisi, Belge, DurumDegisikligi, MaddiYardim, SahsiYardim, ManuelMaddiYardim
from .serializers import (
    DosyaSerializer, DosyaListSerializer,
    AileBilgisiSerializer, BelgeSerializer,
    DurumDegisikligiSerializer, MaddiYardimSerializer,
    SahsiYardimSerializer, ManuelMaddiYardimSerializer
)

logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000  # Maksimum sayfa boyutunu artırdık

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class DosyaViewSet(viewsets.ModelViewSet):
    """
    Dosya kayıtlarını yönetmek için API endpointleri.
    """
    queryset = Dosya.objects.all()
    serializer_class = DosyaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ad', 'soyad', 'kimlik_no', 'dosya_no', 'mahalle', 'cadde_sokak']
    ordering_fields = ['kayit_tarihi', 'ad', 'soyad', 'dosya_no']
    ordering = ['-kayit_tarihi']  # Varsayılan sıralama
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DosyaListSerializer
        return DosyaSerializer
    
    def get_queryset(self):
        try:
            queryset = Dosya.objects.select_related().filter(is_deleted=False)
            
            # Arama parametresi
            search = self.request.query_params.get('search', None)
            if search:
                queryset = queryset.filter(
                    Q(ad__icontains=search) |
                    Q(soyad__icontains=search) |
                    Q(dosya_no__icontains=search) |
                    Q(kimlik_no__icontains=search) |
                    Q(mahalle__icontains=search) |
                    Q(cadde_sokak__icontains=search)
                ).distinct()
            
            # Sıralama parametresi
            ordering = self.request.query_params.get('ordering', '-kayit_tarihi')
            if ordering:
                queryset = queryset.order_by(ordering)
            
            # Durum filtresi
            status = self.request.query_params.get('status')
            if status:
                queryset = queryset.filter(durum=status)
            
            # Kira durumu filtresi
            kira_durumu = self.request.query_params.get('kira_durumu')
            if kira_durumu:
                queryset = queryset.filter(kira_durumu=kira_durumu)
            
            # Engel durumu filtresi
            engel_durumu = self.request.query_params.get('engel_durumu')
            if engel_durumu:
                try:
                    if engel_durumu.lower() == 'true':
                        queryset = queryset.filter(
                            Q(engel_durumu=True) | 
                            Q(aile_bilgileri__engel_durumu=True)
                        ).distinct()
                    elif engel_durumu.lower() == 'false':
                        queryset = queryset.filter(
                            Q(engel_durumu=False) & 
                            ~Q(aile_bilgileri__engel_durumu=True)
                        )
                except Exception as e:
                    logger.error("Engel durumu filtrelemesinde hata: %s", str(e))
                    raise
            
            # Aile üyesi sayısı filtresi
            min_au = self.request.query_params.get('min_aile_uyesi_sayisi')
            max_au = self.request.query_params.get('max_aile_uyesi_sayisi')
            if min_au or max_au:
                queryset = queryset.annotate(
                    aile_uyesi_sayisi=Count('aile_bilgileri', distinct=True)
                ).annotate(
                    total_au=ExpressionWrapper(
                        F('aile_uyesi_sayisi') + Value(1),
                        output_field=IntegerField()
                    )
                ).distinct()
                if min_au:
                    queryset = queryset.filter(total_au__gte=int(min_au))
                if max_au:
                    queryset = queryset.filter(total_au__lte=int(max_au))
            
            # Yardım tipi filtresi
            yardim_tipi = self.request.query_params.get('sahsi_yardim_tipi')
            if yardim_tipi:
                queryset = queryset.filter(sahsi_yardimlar__yardim_tipi=yardim_tipi).distinct()
            
            # Debug: SQL sorgusunu logla
            logger.info("SQL query: %s", str(queryset.query))
            
            return queryset
        except Exception as e:
            logger.error("get_queryset'de hata: %s", str(e))
            raise

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Her durumda sayfalama yap
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ['create', 'update', 'partial_update']:
            context['dosya'] = self.get_object() if self.action != 'create' else None
        return context
    
    def perform_create(self, serializer):
        with transaction.atomic():
            # Son dosya numarasını bul
            last_dosya = Dosya.objects.order_by('-dosya_no').first()
            if last_dosya:
                new_dosya_no = str(int(last_dosya.dosya_no) + 1)
            else:
                new_dosya_no = "1"
            
            # Dosya numarasını ayarla
            serializer.save(dosya_no=new_dosya_no)
            return serializer.instance

    def create(self, request, *args, **kwargs):
        # aile_bilgileri verisi var mı kontrol et
        aile_bilgileri_data = None
        if 'aile_bilgileri' in request.data:
            # FormData'dan gelen JSON string'i parse et
            if isinstance(request.data['aile_bilgileri'], str):
                import json
                try:
                    aile_bilgileri_data = json.loads(request.data['aile_bilgileri'])
                except json.JSONDecodeError:
                    return Response(
                        {"error": "aile_bilgileri verisi geçerli bir JSON formatında değil."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                aile_bilgileri_data = request.data['aile_bilgileri']
        
        # Multipart form data'dan dict oluştur
        data = {key: value for key, value in request.data.items() if key != 'aile_bilgileri'}
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        dosya = self.perform_create(serializer)
        
        if aile_bilgileri_data:
            for aile in aile_bilgileri_data:
                aile["dosya"] = serializer.instance.id
                aile_serializer = AileBilgisiSerializer(data=aile)
                aile_serializer.is_valid(raise_exception=True)
                aile_serializer.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # aile_bilgileri verisi var mı kontrol et
        aile_bilgileri_data = None
        if 'aile_bilgileri' in request.data:
            # FormData'dan gelen JSON string'i parse et
            if isinstance(request.data['aile_bilgileri'], str):
                import json
                try:
                    aile_bilgileri_data = json.loads(request.data['aile_bilgileri'])
                except json.JSONDecodeError:
                    return Response(
                        {"error": "aile_bilgileri verisi geçerli bir JSON formatında değil."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                aile_bilgileri_data = request.data['aile_bilgileri']
        
        # Multipart form data'dan dict oluştur
        data = {key: value for key, value in request.data.items() if key != 'aile_bilgileri'}
        
        # Mevcut notları koru
        if 'notlar' not in data:
            data['notlar'] = instance.notlar
        
        serializer = self.get_serializer(instance, data=data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Aile bilgilerini güncelle
        if aile_bilgileri_data:
            # Önce mevcut aile bilgilerini sil
            instance.aile_bilgileri.all().delete()
            
            # Yeni aile bilgilerini ekle
            for aile in aile_bilgileri_data:
                aile["dosya"] = instance.id
                aile_serializer = AileBilgisiSerializer(data=aile)
                aile_serializer.is_valid(raise_exception=True)
                aile_serializer.save()
        
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        with transaction.atomic():
            serializer.save()
    
    def perform_destroy(self, instance):
        # Soft delete - silinme tarihini ve is_deleted işaretini güncelleme
        instance.is_deleted = True
        instance.silinme_tarihi = timezone.now()
        instance.save()
    
    @action(detail=False, methods=['get'])
    def all(self, request):
        """
        Tüm dosyaları listeler (silinmiş olanlar dahil).
        """
        dosyalar = Dosya.objects.all()
        serializer = DosyaListSerializer(dosyalar, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def deleted(self, request):
        """
        Silinmiş/arşivlenmiş dosyaları listeler.
        """
        dosyalar = Dosya.objects.filter(is_deleted=True)
        serializer = DosyaListSerializer(dosyalar, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """
        Silinmiş/arşivlenmiş bir dosyayı geri yükler.
        """
        dosya = self.get_object()
        if not dosya.is_deleted:
            return Response(
                {"error": "Bu dosya zaten aktif durumda."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        dosya.is_deleted = False
        dosya.silinme_tarihi = None
        dosya.save()
        
        serializer = self.get_serializer(dosya)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Dosyanın durumunu, IBAN ve yardım aldığı yerler bilgilerini günceller ve değişiklik kaydı oluşturur.
        """
        dosya = self.get_object()
        
        yeni_durum = request.data.get('durum')
        aciklama = request.data.get('aciklama', '')
        iban = request.data.get('iban')
        yardim_aldigi_yerler = request.data.get('yardim_aldigi_yerler')
        
        if not yeni_durum:
            return Response(
                {"error": "Durum bilgisi zorunludur."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        eski_durum = dosya.durum
        
        # Durum değişikliği ve diğer bilgileri güncelleme
        with transaction.atomic():
            # Önce dosyayı güncelle
            dosya.durum = yeni_durum
            
            # Açıklama notunu güncelle
            if aciklama is not None:
                dosya.notlar = aciklama
            
            # IBAN ve yardım aldığı yerler bilgilerini güncelle
            if iban is not None:
                dosya.iban = iban
            if yardim_aldigi_yerler is not None:
                dosya.yardim_aldigi_yerler = yardim_aldigi_yerler
                
            # Değişiklikleri kaydet
            dosya.save()
            
            # Sonra değişiklik kaydı oluştur
            durum_degisikligi = DurumDegisikligi.objects.create(
                dosya=dosya,
                eski_durum=eski_durum,
                yeni_durum=yeni_durum,
                aciklama=aciklama,
                degistiren=request.user
            )
        
        return Response({
            "message": "Bilgiler başarıyla güncellendi",
            "dosya": DosyaSerializer(dosya).data,
            "degisiklik": DurumDegisikligiSerializer(durum_degisikligi).data
        })
    
    @action(detail=True, methods=['get'])
    def durum_degisiklikleri(self, request, pk=None):
        """
        Dosyanın durum değişiklik geçmişini döndürür.
        """
        dosya = self.get_object()
        degisiklikler = DurumDegisikligi.objects.filter(dosya=dosya).order_by('-degisiklik_tarihi')
        serializer = DurumDegisikligiSerializer(degisiklikler, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Dosya istatistiklerini hesaplar ve döndürür.
        """
        toplam_dosya = Dosya.objects.filter(is_deleted=False).count()
        bekleyen_dosya = Dosya.objects.filter(is_deleted=False, durum='BEKLEMEDE').count()
        onaylanan_dosya = Dosya.objects.filter(is_deleted=False, durum='ONAYLANDI').count()
        reddedilen_dosya = Dosya.objects.filter(is_deleted=False, durum='REDDEDILDI').count()
        
        return Response({
            "toplam_dosya": toplam_dosya,
            "bekleyen_dosya": bekleyen_dosya,
            "onaylanan_dosya": onaylanan_dosya,
            "reddedilen_dosya": reddedilen_dosya
        })

    @action(detail=True, methods=['post'])
    def upload_belge(self, request, pk=None):
        """
        Belirli bir dosyaya belge yükler.
        """
        dosya = self.get_object()
        belge_turu = request.data.get('belge_turu')
        belge = request.FILES.get('belge')
        
        if not belge_turu or not belge:
            return Response(
                {"error": "Belge türü ve belge dosyası zorunludur."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Mevcut belgeyi güncelle veya yeni belge oluştur
            belge_obj, created = Belge.objects.update_or_create(
                dosya=dosya,
                belge_turu=belge_turu,
                defaults={'belge': belge}
            )
            
            return Response({
                "message": "Belge başarıyla yüklendi.",
                "belge": BelgeSerializer(belge_obj).data
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        try:
            # Filtreleme parametrelerini al
            search = request.GET.get('search', '')
            status_filter = request.GET.get('status', '')
            kira_durumu = request.GET.get('kira_durumu', '')
            engel_durumu = request.GET.get('engel_durumu', '')
            min_aile_uyesi = request.GET.get('min_aile_uyesi_sayisi', '')
            max_aile_uyesi = request.GET.get('max_aile_uyesi_sayisi', '')
            sahsi_yardim_tipi = request.GET.get('sahsi_yardim_tipi', '')
            
            logger.info(f"Export request received with params: search={search}, status={status_filter}, kira_durumu={kira_durumu}, engel_durumu={engel_durumu}, min_aile_uyesi={min_aile_uyesi}, max_aile_uyesi={max_aile_uyesi}, sahsi_yardim_tipi={sahsi_yardim_tipi}")
            
            # QuerySet'i filtrele
            dosyalar = Dosya.objects.filter(is_deleted=False)
            
            # Arama filtresi
            if search:
                dosyalar = dosyalar.filter(
                    Q(ad__icontains=search) |
                    Q(soyad__icontains=search) |
                    Q(dosya_no__icontains=search) |
                    Q(kimlik_no__icontains=search) |
                    Q(mahalle__icontains=search) |
                    Q(cadde_sokak__icontains=search)
                )
            
            # Durum filtresi
            if status_filter:
                dosyalar = dosyalar.filter(durum=status_filter)
            
            # Kira durumu filtresi
            if kira_durumu:
                dosyalar = dosyalar.filter(kira_durumu=kira_durumu)
            
            # Engel durumu filtresi
            if engel_durumu == 'engelli':
                dosyalar = dosyalar.filter(aile_bilgileri__engel_durumu=True).distinct()
            elif engel_durumu == 'engelli_degil':
                dosyalar = dosyalar.exclude(aile_bilgileri__engel_durumu=True)

            # Min/Max aile üyesi sayısı filtresi
            if min_aile_uyesi or max_aile_uyesi:
                # Aile üyesi sayısını hesapla (ana dosya sahibi dahil)
                dosyalar = dosyalar.annotate(
                    aile_uyesi_sayisi=models.Count('aile_bilgileri', distinct=True) + 1
                )
                
                if min_aile_uyesi:
                    min_aile_uyesi = int(min_aile_uyesi)
                    dosyalar = dosyalar.filter(aile_uyesi_sayisi__gte=min_aile_uyesi)
                
                if max_aile_uyesi:
                    max_aile_uyesi = int(max_aile_uyesi)
                    dosyalar = dosyalar.filter(aile_uyesi_sayisi__lte=max_aile_uyesi)

            # Şahsi yardım tipi filtresi
            if sahsi_yardim_tipi:
                dosyalar = dosyalar.filter(sahsi_yardim__yardim_tipi=sahsi_yardim_tipi).distinct()
            
            logger.info(f"Filtered queryset count: {dosyalar.count()}")
            
            # BytesIO nesnesi oluştur
            output = BytesIO()
            
            # Excel workbook oluştur
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()
            
            # Başlıkları ekle
            headers = ['Dosya No', 'Ad Soyad', 'Kimlik No', 'Telefon', 'Adres', 'Durum', 'Kira Durumu', 'Engel Durumu', 'Yardım Tipi', 'Açıklama']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)
            
            # Dosyaları ekle
            for row, dosya in enumerate(dosyalar, start=1):
                try:
                    # Engel durumunu kontrol et
                    engel_durumu_text = "Yok"
                    engel_aciklama = ""
                    if dosya.aile_bilgileri.exists():
                        engelli_count = dosya.aile_bilgileri.filter(engel_durumu=True).count()
                        if engelli_count > 0:
                            engel_durumu_text = f"Var ({engelli_count} kişi)"
                            # Engel açıklamalarını birleştir
                            engel_aciklamalar = dosya.aile_bilgileri.filter(engel_durumu=True).values_list('engel_aciklama', flat=True)
                            engel_aciklama = ", ".join(filter(None, engel_aciklamalar))

                    # Yardım tipini kontrol et
                    yardim_tipi = "Yok"
                    if hasattr(dosya, 'sahsi_yardim') and dosya.sahsi_yardim:
                        yardim_tipi = "Bireysel Yardım" if dosya.sahsi_yardim.yardim_tipi == "individual" else "Grup Yardımı"

                    worksheet.write(row, 0, str(dosya.dosya_no))
                    worksheet.write(row, 1, f"{dosya.ad} {dosya.soyad}")
                    worksheet.write(row, 2, str(dosya.kimlik_no))
                    worksheet.write(row, 3, str(dosya.telefon))
                    worksheet.write(row, 4, f"{dosya.mahalle} Mah. {dosya.cadde_sokak} Cad. No:{dosya.bina_no} Daire:{dosya.daire_no}")
                    worksheet.write(row, 5, str(dosya.durum))
                    worksheet.write(row, 6, str(dosya.kira_durumu))
                    worksheet.write(row, 7, engel_durumu_text)
                    worksheet.write(row, 8, yardim_tipi)
                    worksheet.write(row, 9, engel_aciklama)
                except Exception as e:
                    logger.error(f"Error writing row {row} for dosya {dosya.dosya_no}: {str(e)}")
                    continue
            
            workbook.close()
            
            # Response oluştur
            output.seek(0)
            response = HttpResponse(
                output.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=dosyalar.xlsx'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            
            logger.info("Excel file generated successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error in export_excel: {str(e)}")
            return Response(
                {"error": f"Excel dosyası oluşturulurken bir hata oluştu: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AileBilgisiViewSet(viewsets.ModelViewSet):
    """
    Aile üyelerini yönetmek için API endpointleri.
    """
    queryset = AileBilgisi.objects.all()
    serializer_class = AileBilgisiSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = AileBilgisi.objects.all()
        dosya_id = self.request.query_params.get('dosya', None)
        
        if dosya_id:
            queryset = queryset.filter(dosya_id=dosya_id)
        return queryset
    
    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()
    
    def perform_update(self, serializer):
        with transaction.atomic():
            serializer.save()
    
    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.delete()


class BelgeViewSet(viewsets.ModelViewSet):
    """
    Belgeleri yönetmek için API endpointleri.
    """
    queryset = Belge.objects.all()
    serializer_class = BelgeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Belge.objects.all()
        dosya_id = self.request.query_params.get('dosya', None)
        
        if dosya_id:
            queryset = queryset.filter(dosya_id=dosya_id)
        
        return queryset
    
    @action(detail=False, methods=['delete'])
    def delete_belge(self, request):
        """
        Belirli bir dosyaya ait belirli türdeki belgeyi siler.
        """
        dosya_id = request.query_params.get('dosya', None)
        belge_turu = request.query_params.get('belge_turu', None)
        
        if not dosya_id or not belge_turu:
            return Response(
                {"error": "Dosya ID ve belge türü parametreleri zorunludur."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            belge = get_object_or_404(Belge, dosya_id=dosya_id, belge_turu=belge_turu)
            belge.delete()
            return Response(
                {"message": f"{belge.get_belge_turu_display()} başarıyla silindi."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Belge.DoesNotExist:
            return Response(
                {"error": "Belirtilen belge bulunamadı."},
                status=status.HTTP_404_NOT_FOUND
            )


class DurumDegisikligiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Durum değişikliklerini görüntülemek için API endpointleri.
    """
    queryset = DurumDegisikligi.objects.all()
    serializer_class = DurumDegisikligiSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = DurumDegisikligi.objects.all()
        dosya_id = self.request.query_params.get('dosya', None)
        
        if dosya_id:
            queryset = queryset.filter(dosya_id=dosya_id)
        
        return queryset


class MaddiYardimViewSet(viewsets.ModelViewSet):
    queryset = MaddiYardim.objects.all().order_by('-created_at')
    serializer_class = MaddiYardimSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['yardim_yapan_ad_soyad', 'yardim_yapan_telefon']
    ordering_fields = ['created_at', 'tutar']

    def get_queryset(self):
        queryset = MaddiYardim.objects.all()
        search = self.request.query_params.get('search', None)
        
        if search:
            queryset = queryset.filter(
                Q(yardim_yapan_ad_soyad__icontains=search) |
                Q(yardim_yapan_telefon__icontains=search) |
                Q(dosya_tutarlari__dosya__ad__icontains=search) |
                Q(dosya_tutarlari__dosya__soyad__icontains=search) |
                Q(dosya_tutarlari__dosya__dosya_no__icontains=search)
            ).distinct()
        
        return queryset.order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            context['dosya_tutarlari'] = self.request.data.get('dosya_tutarlari', [])
        return context

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class SahsiYardimViewSet(viewsets.ModelViewSet):
    queryset = SahsiYardim.objects.all().order_by('-created_at')
    serializer_class = SahsiYardimSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ad_soyad', 'telefon']
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = SahsiYardim.objects.all()
        search = self.request.query_params.get('search', None)
        
        if search:
            queryset = queryset.filter(
                Q(ad_soyad__icontains=search) |
                Q(telefon__icontains=search)
            ).distinct()
            
        return queryset.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info("Gelen ham veri:")
        logger.info(request.data)
        logger.info("Gelen veri tipleri:")
        for key, value in request.data.items():
            logger.info(f"{key}: {type(value)}")
        
        # Veriyi dönüştür
        data = request.data.copy()
        if 'type' in data:
            data['yardim_tipi'] = data.pop('type')
        if 'name' in data:
            data['ad_soyad'] = data.pop('name')
        if 'phone' in data:
            data['telefon'] = data.pop('phone')
        
        logger.info("Dönüştürülmüş veri:")
        logger.info(data)
        
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            logger.error("Serializer hataları:")
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ManuelMaddiYardimViewSet(viewsets.ModelViewSet):
    queryset = ManuelMaddiYardim.objects.all().order_by('-created_at')
    serializer_class = ManuelMaddiYardimSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ad_soyad', 'telefon', 'adres']
    ordering_fields = ['created_at', 'tutar']

    def get_queryset(self):
        queryset = ManuelMaddiYardim.objects.all()
        search = self.request.query_params.get('search', None)
        
        if search:
            queryset = queryset.filter(
                Q(ad_soyad__icontains=search) |
                Q(telefon__icontains=search) |
                Q(adres__icontains=search)
            ).distinct()
        
        return queryset.order_by('-created_at')
