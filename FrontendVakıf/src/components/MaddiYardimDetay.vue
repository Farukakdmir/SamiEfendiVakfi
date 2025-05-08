<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div
      class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
    >
      <div class="fixed inset-0 transition-opacity" aria-hidden="true">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div>

      <div
        class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
      >
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Maddi Yardım Detayı
                </h3>
                <div class="flex items-center space-x-2">
                  <button
                    @click="exportToExcel"
                    class="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-white bg-emerald-800 hover:bg-emerald-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-4 w-4 mr-1"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                    Excel'e Aktar
                  </button>
                  <button
                    @click="$emit('close')"
                    class="text-gray-400 hover:text-gray-500"
                  >
                    <span class="sr-only">Kapat</span>
                    <svg
                      class="h-6 w-6"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
              </div>

              <!-- Yardım Yapan Bilgileri -->
              <div class="mb-6">
                <h4 class="text-sm font-medium text-gray-500 mb-2">
                  Yardım Yapan Bilgileri
                </h4>
                <div class="bg-gray-50 rounded-md p-4">
                  <p class="text-sm text-gray-900">
                    <span class="font-medium">Ad Soyad:</span>
                    {{ yardim.yardim_yapan_ad_soyad }}
                  </p>
                  <p class="text-sm text-gray-900 mt-1">
                    <span class="font-medium">Telefon:</span>
                    {{ yardim.yardim_yapan_telefon }}
                  </p>
                </div>
              </div>

              <!-- Yardım Detayları -->
              <div class="mb-6">
                <h4 class="text-sm font-medium text-gray-500 mb-2">
                  Yardım Detayları
                </h4>
                <div class="bg-gray-50 rounded-md p-4">
                  <p class="text-sm text-gray-900">
                    <span class="font-medium">Toplam Tutar:</span>
                    {{ formatTutar(yardim.tutar) }} TL
                  </p>
                  <p class="text-sm text-gray-900 mt-1">
                    <span class="font-medium">Tarih:</span>
                    {{ formatDate(yardim.created_at) }}
                  </p>
                  <p class="text-sm text-gray-900 mt-1">
                    <span class="font-medium">Açıklama:</span>
                    {{ yardim.aciklama || "Açıklama yok" }}
                  </p>
                </div>
              </div>

              <!-- Dosya Kayıtları -->
              <div class="mb-6">
                <h4 class="text-sm font-medium text-gray-500 mb-2">
                  Dosya Kayıtları
                </h4>
                <div class="bg-gray-50 rounded-md p-4">
                  <div
                    v-if="
                      yardim.dosya_bilgileri &&
                      yardim.dosya_bilgileri.length > 0
                    "
                  >
                    <div
                      v-for="(dosya, index) in yardim.dosya_bilgileri"
                      :key="index"
                      class="mb-3 last:mb-0 p-2 bg-white rounded-md border border-gray-200"
                    >
                      <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-4">
                          <div class="flex-shrink-0">
                            <div class="font-medium">
                              {{ dosya.dosya_bilgisi.ad }}
                              {{ dosya.dosya_bilgisi.soyad }}
                            </div>
                            <div class="text-sm text-gray-500">
                              Dosya No: {{ dosya.dosya_bilgisi.dosya_no }}
                            </div>
                          </div>
                          <div class="flex items-center space-x-2">
                            <span
                              :class="[
                                'px-2 py-1 rounded-full text-xs font-medium',
                                dosya.dosya_bilgisi.durum === 'ONAYLANDI'
                                  ? 'bg-green-100 text-green-800'
                                  : dosya.dosya_bilgisi.durum === 'REDDEDILDI'
                                  ? 'bg-red-100 text-red-800'
                                  : dosya.dosya_bilgisi.durum === 'BEKLEMEDE'
                                  ? 'bg-yellow-100 text-yellow-800'
                                  : 'bg-gray-100 text-gray-800',
                              ]"
                            >
                              {{ dosya.dosya_bilgisi.durum }}
                            </span>
                          </div>
                        </div>
                        <div class="text-right">
                          <p class="text-sm font-medium text-gray-900">
                            {{ formatTutar(dosya.tutar) }} TL
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <p v-else class="text-sm text-gray-500">
                    Dosya kaydı bulunmamaktadır.
                  </p>
                </div>
              </div>

              <!-- Manuel Kayıtlar -->
              <div class="mb-6">
                <h4 class="text-sm font-medium text-gray-500 mb-2">
                  Manuel Kayıtlar
                </h4>
                <div class="bg-gray-50 rounded-md p-4">
                  <div
                    v-if="
                      yardim.manuel_kayitlar &&
                      yardim.manuel_kayitlar.length > 0
                    "
                  >
                    <div
                      v-for="(kayit, index) in yardim.manuel_kayitlar"
                      :key="index"
                      class="mb-3 last:mb-0 p-2 bg-white rounded-md border border-gray-200"
                    >
                      <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-4">
                          <div class="flex-shrink-0">
                            <div class="font-medium">
                              {{ kayit.ad_soyad }}
                            </div>
                            <div class="text-sm text-gray-500">
                              TC: {{ kayit.tc_kimlik }}
                            </div>
                            <div class="text-sm text-gray-500">
                              Tel: {{ kayit.telefon }}
                            </div>
                          </div>
                        </div>
                        <div class="text-right">
                          <p class="text-sm font-medium text-gray-900">
                            {{ formatTutar(kayit.tutar) }} TL
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <p v-else class="text-sm text-gray-500">
                    Manuel kayıt bulunmamaktadır.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            @click="$emit('close')"
          >
            Kapat
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { utils as XLSXUtils, writeFile } from "xlsx";

export default {
  name: "MaddiYardimDetay",
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    yardim: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      aileBilgileri: [],
    };
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString("tr-TR");
    },
    formatTutar(tutar) {
      return Number(tutar).toLocaleString("tr-TR");
    },
    getDosyaTutari(dosyaId) {
      const dosyaTutar = this.yardim.dosya_tutarlari?.find(
        (dt) => dt.dosya_id === dosyaId
      );
      return dosyaTutar
        ? Number(dosyaTutar.tutar).toLocaleString("tr-TR")
        : "0";
    },
    exportToExcel() {
      try {
        console.log("Excel'e aktarma başladı");
        console.log("Yardım verisi:", this.yardim);

        // Excel için veri hazırlama
        const data = [];

        // Başlık satırı
        data.push([
          "Ad Soyad",
          "TC Kimlik",
          "Telefon",
          "Adres",
          "Tutar",
          "Açıklama",
          "Kayıt Tipi",
        ]);

        // Dosya kayıtlarını ekle
        if (
          this.yardim.dosya_bilgileri &&
          this.yardim.dosya_bilgileri.length > 0
        ) {
          console.log(
            "Dosya kayıtları ekleniyor:",
            this.yardim.dosya_bilgileri
          );
          this.yardim.dosya_bilgileri.forEach((dosya) => {
            data.push([
              `${dosya.dosya_bilgisi.ad} ${dosya.dosya_bilgisi.soyad}`,
              dosya.dosya_bilgisi.tc_kimlik || "-",
              dosya.dosya_bilgisi.telefon || "-",
              `${dosya.dosya_bilgisi.mahalle || ""} ${
                dosya.dosya_bilgisi.cadde_sokak || ""
              }`,
              this.formatTutar(dosya.tutar),
              dosya.aciklama || "-",
              "Dosya Kaydı",
            ]);
          });
        }

        // Manuel kayıtları ekle
        if (
          this.yardim.manuel_kayitlar &&
          this.yardim.manuel_kayitlar.length > 0
        ) {
          console.log(
            "Manuel kayıtlar ekleniyor:",
            this.yardim.manuel_kayitlar
          );
          this.yardim.manuel_kayitlar.forEach((kayit) => {
            data.push([
              kayit.ad_soyad,
              kayit.tc_kimlik || "-",
              kayit.telefon || "-",
              kayit.adres || "-",
              this.formatTutar(kayit.tutar),
              kayit.aciklama || "-",
              "Manuel Kayıt",
            ]);
          });
        }

        console.log("Hazırlanan veri:", data);

        // Excel dosyası oluştur
        const ws = XLSXUtils.aoa_to_sheet(data);
        const wb = XLSXUtils.book_new();
        XLSXUtils.book_append_sheet(wb, ws, "Maddi Yardım Detayı");

        // Dosya adını oluştur
        const fileName = `Maddi_Yardim_${
          this.yardim.yardim_yapan_ad_soyad
        }_${this.formatDate(this.yardim.created_at)}.xlsx`;
        console.log("Dosya adı:", fileName);

        // Excel dosyasını indir
        writeFile(wb, fileName);
        console.log("Excel dosyası oluşturuldu ve indirildi");
      } catch (error) {
        console.error("Excel'e aktarma hatası:", error);
        alert("Excel dosyası oluşturulurken bir hata oluştu: " + error.message);
      }
    },
  },
  watch: {
    yardim: {
      handler(newYardim) {
        console.log("Tüm yardım verisi:", newYardim);
        if (newYardim?.dosya_bilgileri?.[0]) {
          console.log("İlk dosya bilgisi:", newYardim.dosya_bilgileri[0]);
          console.log(
            "Engel durumu:",
            newYardim.dosya_bilgileri[0].engel_durumu
          );
          console.log(
            "Engel sayısı:",
            newYardim.dosya_bilgileri[0].engel_sayisi
          );
        }
        if (newYardim?.dosyalar?.[0]) {
          console.log("İlk dosya ID:", newYardim.dosyalar[0]);
        }
        if (newYardim?.dosya_tutarlari?.[0]) {
          console.log("İlk dosya tutarı:", newYardim.dosya_tutarlari[0]);
        }
      },
      deep: true,
      immediate: true,
    },
  },
};
</script>
