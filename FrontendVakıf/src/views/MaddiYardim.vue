<template>
  <div class="flex h-screen overflow-hidden">
    <Navbar />
    <main
      class="flex-1 bg-gray-200 overflow-y-auto transition-all duration-300"
      :class="{ 'ml-64': isOpen, 'ml-0': !isOpen }"
    >
      <div class="p-8 flex flex-col">
        <div class="mb-6 flex justify-between items-center flex-shrink-0">
          <div class="flex-1 max-w-md ml-8">
            <v-text-field
              v-model="searchQuery"
              placeholder="Ad, soyad veya telefon ara..."
              prepend-inner-icon="mdi-magnify"
              clearable
              @click:clear="clearSearch"
              variant="outlined"
              density="comfortable"
              hide-details
              class="bg-white"
            ></v-text-field>
          </div>
          <div class="flex gap-2">
            <button
              @click="showNewRecordModal = true"
              class="px-8 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 flex items-center gap-2 text-base font-medium w-48"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4v16m8-8H4"
                />
              </svg>
              Yeni Kayıt
            </button>
            <button
              @click="exportToExcel"
              class="px-8 py-2 bg-green-600 text-white rounded-xl hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200 flex items-center gap-2 text-base font-medium"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
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
          </div>
        </div>

        <!-- No Results Message -->
        <div v-if="showNoResults" class="bg-white rounded-lg shadow p-4 mb-4">
          <p class="text-gray-500 text-center">
            Arama kriterlerinize uygun sonuç bulunamadı.
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="bg-white rounded-lg shadow p-4 mb-4">
          <p class="text-gray-500 text-center">Yükleniyor...</p>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="bg-white rounded-lg shadow p-4 mb-4">
          <p class="text-red-500 text-center">{{ error }}</p>
        </div>

        <!-- Kayıtlar Tablosu -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <v-table>
            <thead>
              <tr>
                <th>Yardım Yapan</th>
                <th>Telefon</th>
                <th>Yardım Tutarı</th>
                <th>Toplam Tutar</th>
                <th>Kalan Tutar</th>
                <th>Tarih</th>
                <th>İşlemler</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="yardim in yardimlar" :key="yardim.id">
                <td>{{ yardim.yardim_yapan_ad_soyad }}</td>
                <td>{{ yardim.yardim_yapan_telefon }}</td>
                <td>{{ formatCurrency(yardim.yardim_tutar) }} ₺</td>
                <td>{{ formatCurrency(yardim.tutar) }} ₺</td>
                <td>
                  <span
                    :class="
                      getKalanTutarClass(yardim.yardim_tutar - yardim.tutar)
                    "
                  >
                    {{ formatCurrency(yardim.yardim_tutar - yardim.tutar) }} ₺
                  </span>
                </td>
                <td>
                  {{ new Date(yardim.created_at).toLocaleDateString("tr-TR") }}
                </td>
                <td>
                  <div class="relative">
                    <v-menu
                      location="bottom end"
                      :close-on-content-click="true"
                      :close-on-click="true"
                    >
                      <template v-slot:activator="{ props }">
                        <v-btn
                          v-bind="props"
                          variant="text"
                          class="text-gray-400 hover:text-gray-500"
                        >
                          <v-icon icon="mdi-dots-vertical"></v-icon>
                        </v-btn>
                      </template>
                      <v-list>
                        <v-list-item
                          @click="showDetail(yardim)"
                          class="hover:bg-gray-50 transition-colors duration-200"
                        >
                          <template v-slot:prepend>
                            <v-icon
                              icon="mdi-eye"
                              color="blue"
                              class="mr-2"
                            ></v-icon>
                          </template>
                          <v-list-item-title class="text-sm"
                            >Detay</v-list-item-title
                          >
                        </v-list-item>
                        <v-divider class="my-2"></v-divider>
                        <v-list-item
                          @click="editYardim(yardim)"
                          class="hover:bg-gray-50 transition-colors duration-200"
                        >
                          <template v-slot:prepend>
                            <v-icon
                              icon="mdi-pencil"
                              color="blue"
                              class="mr-2"
                            ></v-icon>
                          </template>
                          <v-list-item-title class="text-sm"
                            >Düzenle</v-list-item-title
                          >
                        </v-list-item>
                        <v-divider class="my-2"></v-divider>
                        <v-list-item
                          @click="deleteYardim(yardim.id)"
                          class="hover:bg-red-50 transition-colors duration-200"
                        >
                          <template v-slot:prepend>
                            <v-icon
                              icon="mdi-delete"
                              color="red"
                              class="mr-2"
                            ></v-icon>
                          </template>
                          <v-list-item-title class="text-sm text-red-600"
                            >Sil</v-list-item-title
                          >
                        </v-list-item>
                      </v-list>
                    </v-menu>
                  </div>
                </td>
              </tr>
            </tbody>
          </v-table>
        </div>

        <!-- Sayfalama -->
        <div class="bg-white rounded-lg shadow mb-4">
          <div
            class="px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
          >
            <div class="flex-1 flex justify-between sm:hidden">
              <button
                @click="currentPage > 1 ? currentPage-- : null"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Önceki
              </button>
              <button
                @click="currentPage < totalPages ? currentPage++ : null"
                :disabled="currentPage === totalPages"
                class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Sonraki
              </button>
            </div>
            <div
              class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"
            >
              <div>
                <p class="text-sm text-gray-700">
                  Toplam
                  <span class="font-medium">{{ totalItems }}</span> kayıttan
                  <span class="font-medium">{{
                    (currentPage - 1) * pageSize + 1
                  }}</span>
                  -
                  <span class="font-medium">{{
                    Math.min(currentPage * pageSize, totalItems)
                  }}</span>
                  arası gösteriliyor
                </p>
              </div>
              <div>
                <nav
                  class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
                  aria-label="Pagination"
                >
                  <!-- İlk Sayfa Butonu -->
                  <button
                    @click="currentPage = 1"
                    :disabled="currentPage === 1"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span class="sr-only">İlk Sayfa</span>
                    <svg
                      class="h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M15.707 15.707a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 010 1.414zm-6 0a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 011.414 1.414L5.414 10l4.293 4.293a1 1 0 010 1.414z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </button>

                  <!-- Önceki Sayfa Butonu -->
                  <button
                    @click="currentPage > 1 ? currentPage-- : null"
                    :disabled="currentPage === 1"
                    class="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span class="sr-only">Önceki</span>
                    <svg
                      class="h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </button>

                  <!-- Sayfa Numaraları -->
                  <template
                    v-for="page in displayedPages"
                    :key="'page-' + page"
                  >
                    <button
                      v-if="page !== '...'"
                      @click="currentPage = page"
                      :class="[
                        currentPage === page
                          ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                          : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
                        'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                      ]"
                    >
                      {{ page }}
                    </button>
                    <span
                      v-else
                      :key="'ellipsis-' + Math.random()"
                      class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
                    >
                      ...
                    </span>
                  </template>

                  <!-- Sonraki Sayfa Butonu -->
                  <button
                    @click="currentPage < totalPages ? currentPage++ : null"
                    :disabled="currentPage === totalPages"
                    class="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span class="sr-only">Sonraki</span>
                    <svg
                      class="h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </button>

                  <!-- Son Sayfa Butonu -->
                  <button
                    @click="currentPage = totalPages"
                    :disabled="currentPage === totalPages"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span class="sr-only">Son Sayfa</span>
                    <svg
                      class="h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M4.293 15.707a1 1 0 001.414 0l5-5a1 1 0 000-1.414l-5-5a1 1 0 00-1.414 1.414L8.586 10 4.293 14.293a1 1 0 000 1.414zm6 0a1 1 0 001.414 0l5-5a1 1 0 000-1.414l-5-5a1 1 0 00-1.414 1.414L14.586 10l-4.293 4.293a1 1 0 000 1.414z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>

        <!-- Modaller -->
        <MaddiYardimEkleModal
          :show="showNewRecordModal"
          @close="showNewRecordModal = false"
          @saved="handleYardimSaved"
        />

        <MaddiYardimDetay
          v-if="showDetailModal"
          :show="showDetailModal"
          :yardim="selectedYardim"
          @close="showDetailModal = false"
        />

        <MaddiYardimDuzenle
          v-if="showEditModal"
          :show="showEditModal"
          :yardim="selectedYardim"
          @close="handleEditModalClose"
          @saved="handleYardimSaved"
        />
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import Navbar from "../components/Navbar.vue";
import MaddiYardimEkleModal from "../components/MaddiYardimEkleModal.vue";
import MaddiYardimDetay from "../components/MaddiYardimDetay.vue";
import MaddiYardimDuzenle from "../components/MaddiYardimDuzenle.vue";
import { useNavbarStore } from "../store/navbar";
import apiService from "../api";
import { utils as XLSXUtils, writeFile } from "xlsx";

export default {
  name: "MaddiYardim",
  components: {
    Navbar,
    MaddiYardimEkleModal,
    MaddiYardimDetay,
    MaddiYardimDuzenle,
  },
  setup() {
    const navbarStore = useNavbarStore();
    const isOpen = computed(() => navbarStore.isOpen);
    const showNewRecordModal = ref(false);
    const showDetailModal = ref(false);
    const showEditModal = ref(false);
    const searchQuery = ref("");
    const yardimlar = ref([]);
    const selectedYardim = ref(null);
    const showNoResults = ref(false);
    const isLoading = ref(false);
    const error = ref(null);

    // Table headers
    const tableHeaders = [
      "Ad Soyad",
      "Telefon",
      "Yardım Tutarı",
      "Toplam Tutar",
      "İşlemler",
    ];

    // Sayfalama için state
    const currentPage = ref(1);
    const pageSize = ref(10);
    const totalItems = ref(0);
    const totalPages = computed(() =>
      Math.ceil(totalItems.value / pageSize.value)
    );

    // Sayfalama hesaplamaları
    const displayedPages = computed(() => {
      const pages = [];
      const maxPages = 5;
      let start = Math.max(1, currentPage.value - Math.floor(maxPages / 2));
      let end = Math.min(totalPages.value, start + maxPages - 1);
      if (end - start + 1 < maxPages) {
        start = Math.max(1, end - maxPages + 1);
      }
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    });

    // Para formatı için yardımcı fonksiyon
    const formatCurrency = (value) => {
      return new Intl.NumberFormat("tr-TR").format(value);
    };

    // Debounce fonksiyonu
    const debounce = (fn, delay) => {
      let timeoutId;
      return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn(...args), delay);
      };
    };

    // Debounced fetchYardimlar fonksiyonu
    const debouncedFetchYardimlar = debounce(() => {
      currentPage.value = 1; // Arama yapıldığında ilk sayfaya dön
      fetchYardimlar();
    }, 500); // 500ms gecikme

    // Yardımları getir
    const fetchYardimlar = async () => {
      try {
        isLoading.value = true;
        error.value = null;

        // API parametrelerini hazırla
        const params = new URLSearchParams();
        params.append("page", currentPage.value);
        params.append("page_size", pageSize.value);

        // Arama filtresi
        if (searchQuery.value && searchQuery.value.trim()) {
          params.append("search", searchQuery.value.trim());
        }

        // API çağrısı
        const response = await apiService.get(
          `/maddi-yardimlar/?${params.toString()}`
        );

        if (response.data && response.data.results) {
          yardimlar.value = response.data.results;
          totalItems.value = response.data.count || 0;
          showNoResults.value = yardimlar.value.length === 0;
        } else {
          error.value = "Yardımlar yüklenirken bir hata oluştu.";
          yardimlar.value = [];
          totalItems.value = 0;
          showNoResults.value = true;
        }
      } catch (error) {
        console.error("Yardımlar yüklenirken hata:", error);
        error.value = "Yardımlar yüklenirken bir hata oluştu.";
        yardimlar.value = [];
        totalItems.value = 0;
        showNoResults.value = true;
      } finally {
        isLoading.value = false;
      }
    };

    // Sayfa değiştiğinde verileri yeniden yükle
    watch(currentPage, (newPage) => {
      if (newPage > 0 && newPage <= totalPages.value) {
        fetchYardimlar();
      }
    });

    // Arama sorgusu değiştiğinde debounced fonksiyonu çağır
    watch(searchQuery, () => {
      currentPage.value = 1; // Arama yapıldığında ilk sayfaya dön
      debouncedFetchYardimlar();
    });

    // Arama sorgusu değiştiğinde verileri yeniden yükle
    watch(searchQuery, () => {
      fetchYardimlar();
    });

    // Arama sorgusunu temizle
    const clearSearch = () => {
      searchQuery.value = "";
      currentPage.value = 1;
      fetchYardimlar();
    };

    // Yeni yardım kaydet
    const handleYardimSaved = async (updatedYardim) => {
      if (showNewRecordModal.value) {
        showNewRecordModal.value = false;
      }
      if (showEditModal.value) {
        showEditModal.value = false;
      }

      // Her durumda listeyi yenile
      await fetchYardimlar();
    };

    // Yardım detaylarını göster
    const showDetail = async (yardim) => {
      try {
        const response = await apiService.getMaddiYardim(yardim.id);
        selectedYardim.value = response.data;
        showDetailModal.value = true;
      } catch (error) {
        console.error("Yardım detayları yüklenirken hata:", error);
      }
    };

    // Yardım düzenle
    const editYardim = async (yardim) => {
      try {
        const response = await apiService.getMaddiYardim(yardim.id);
        selectedYardim.value = response.data;
        showEditModal.value = true;
      } catch (error) {
        console.error("Yardım detayları yüklenirken hata:", error);
      }
    };

    // Düzenleme modalını kapat
    const handleEditModalClose = () => {
      showEditModal.value = false;
      selectedYardim.value = null;
    };

    // Yardım sil
    const deleteYardim = async (id) => {
      if (confirm("Bu yardım kaydını silmek istediğinizden emin misiniz?")) {
        try {
          await apiService.deleteMaddiYardim(id);
          await fetchYardimlar();
        } catch (error) {
          console.error("Yardım silinirken hata:", error);
        }
      }
    };

    // Excel'e aktarma fonksiyonu
    const exportToExcel = async () => {
      try {
        // Filtrelenmiş kayıtları al
        const recordsToExport = yardimlar.value;

        // Excel için veri hazırlama
        const data = [];

        // Başlık satırı
        data.push([
          "Ad Soyad",
          "Telefon",
          "Yardım Tutarı",
          "Toplam Tutar",
          "Tarih",
          "Açıklama",
        ]);

        // Kayıtları ekle
        recordsToExport.forEach((yardim) => {
          data.push([
            yardim.yardim_yapan_ad_soyad,
            yardim.yardim_yapan_telefon,
            formatCurrency(yardim.yardim_tutar),
            formatCurrency(yardim.tutar),
            new Date(yardim.created_at).toLocaleDateString("tr-TR"),
            yardim.aciklama || "-",
          ]);
        });

        // Excel dosyası oluştur
        const ws = XLSXUtils.aoa_to_sheet(data);
        const wb = XLSXUtils.book_new();
        XLSXUtils.book_append_sheet(wb, ws, "Maddi Yardımlar");

        // Sütun genişliklerini ayarla
        const colWidths = [
          { wch: 30 }, // Ad Soyad
          { wch: 15 }, // Telefon
          { wch: 15 }, // Yardım Tutarı
          { wch: 15 }, // Toplam Tutar
          { wch: 12 }, // Tarih
          { wch: 40 }, // Açıklama
        ];
        ws["!cols"] = colWidths;

        // Dosya adını oluştur
        const fileName = `Maddi_Yardimlar_${new Date().toLocaleDateString(
          "tr-TR"
        )}.xlsx`;

        // Excel dosyasını indir
        writeFile(wb, fileName);
      } catch (error) {
        console.error("Excel'e aktarma hatası:", error);
        alert("Excel dosyası oluşturulurken bir hata oluştu: " + error.message);
      }
    };

    // Yeni eklenen fonksiyon
    const getKalanTutarClass = (kalanTutar) => {
      if (kalanTutar > 0) {
        return "text-green-600 font-medium";
      } else if (kalanTutar < 0) {
        return "text-red-600 font-medium";
      }
      return "text-gray-600";
    };

    onMounted(() => {
      fetchYardimlar();
    });

    onUnmounted(() => {
      // Event listener'ı kaldırdık
    });

    return {
      isOpen,
      showNewRecordModal,
      showDetailModal,
      showEditModal,
      searchQuery,
      yardimlar,
      selectedYardim,
      formatCurrency,
      handleYardimSaved,
      showDetail,
      editYardim,
      deleteYardim,
      currentPage,
      pageSize,
      totalItems,
      totalPages,
      displayedPages,
      clearSearch,
      handleEditModalClose,
      exportToExcel,
      tableHeaders,
      getKalanTutarClass,
      showNoResults,
      isLoading,
      error,
    };
  },
};
</script>
