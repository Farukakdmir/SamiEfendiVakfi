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
            <!-- Yardım Tipi Filtresi -->
            <div class="relative">
              <button
                @click="showFilters = !showFilters"
                class="px-4 py-2 bg-white text-gray-700 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 flex items-center gap-2 border border-gray-300"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z"
                    clip-rule="evenodd"
                  />
                </svg>
                Filtrele
                <span
                  v-if="selectedYardimTipi"
                  class="ml-1 px-2 py-0.5 text-xs bg-blue-100 text-blue-800 rounded-full"
                >
                  {{
                    selectedYardimTipi === "individual" ? "Bireysel" : "Grup"
                  }}
                </span>
              </button>
              <div
                v-if="showFilters"
                class="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg py-2 z-[100] border border-gray-200"
              >
                <div class="px-4 py-2">
                  <div class="mb-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                      >Yardım Tipi</label
                    >
                    <select
                      v-model="selectedYardimTipi"
                      class="block w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded-lg leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                    >
                      <option value="">Tüm Yardım Tipleri</option>
                      <option value="individual">Bireysel Yardım</option>
                      <option value="group">Grup Yardımı</option>
                    </select>
                  </div>
                </div>
                <div class="px-4 py-2 border-t border-gray-200">
                  <button
                    @click="clearFilters"
                    class="w-full text-left px-4 py-2 text-sm text-blue-600 hover:bg-gray-100 rounded-lg transition-colors duration-200"
                  >
                    Filtreleri Temizle
                  </button>
                </div>
              </div>
            </div>
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
          </div>
        </div>

        <!-- Kayıtlar Tablosu -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Ad Soyad
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Telefon
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Yardım Tipi
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Durum
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  İşlemler
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="record in displayedYardimlar" :key="record.id">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">
                    {{ record.ad_soyad }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ record.telefon }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">
                    {{
                      record.yardim_tipi === "individual" ? "Bireysel" : "Grup"
                    }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="[
                      'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
                      record.grup_uye_sayisi
                        ? 'bg-green-100 text-green-800'
                        : 'bg-blue-100 text-blue-800',
                    ]"
                  >
                    {{
                      record.grup_uye_sayisi
                        ? `Grup (${record.grup_uye_sayisi} kişi)`
                        : "Bireysel"
                    }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <v-menu>
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
                        @click="showDetail(record)"
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
                        @click="editRecord(record)"
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
                        @click="deleteRecord(record.id)"
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
                </td>
              </tr>
            </tbody>
          </table>
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
                  <template v-for="page in displayedPages" :key="page">
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

        <!-- Yeni Kayıt Modal -->
        <SahsiYardimEkleModal
          :show="showNewRecordModal"
          @close="showNewRecordModal = false"
          @saved="handleYardimSaved"
        />

        <!-- Modaller -->
        <SahsiYardimDetay
          v-if="showDetailModal"
          v-model:show="showDetailModal"
          :yardim="selectedYardim"
          @close="showDetailModal = false"
        />

        <SahsiYardimDuzenle
          v-if="showEditModal"
          v-model:show="showEditModal"
          :yardim="selectedYardim"
          @close="showEditModal = false"
          @saved="handleYardimSaved"
        />
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, onUnmounted } from "vue";
import Navbar from "../components/Navbar.vue";
import SahsiYardimEkleModal from "../components/SahsiYardimEkleModal.vue";
import SahsiYardimDetay from "../components/SahsiYardimDetay.vue";
import SahsiYardimDuzenle from "../components/SahsiYardimDuzenle.vue";
import { useNavbarStore } from "../store/navbar";
import apiService from "../api";

export default {
  name: "SahsiYardim",
  components: {
    Navbar,
    SahsiYardimEkleModal,
    SahsiYardimDetay,
    SahsiYardimDuzenle,
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
    const selectedYardimTipi = ref("");
    const showFilters = ref(false);
    const displayedYardimlar = ref([]);

    // Sayfalama için state
    const currentPage = ref(1);
    const pageSize = ref(10);
    const totalItems = ref(0);
    const totalPages = computed(() =>
      Math.ceil(totalItems.value / pageSize.value)
    );

    const clearSearch = () => {
      searchQuery.value = "";
    };

    // Yardımları getir
    const fetchYardimlar = async () => {
      try {
        const response = await apiService.getSahsiYardimlar();
        yardimlar.value = response.data;
        totalItems.value = response.data.length;
        updateDisplayedRecords();
      } catch (error) {
        console.error("Yardımlar yüklenirken hata:", error);
      }
    };

    // Görüntülenecek kayıtları güncelle
    const updateDisplayedRecords = () => {
      const filtered = filteredRecords.value;
      const startIndex = (currentPage.value - 1) * pageSize.value;
      const endIndex = startIndex + pageSize.value;
      displayedYardimlar.value = filtered.slice(startIndex, endIndex);
    };

    const filteredRecords = computed(() => {
      let filtered = yardimlar.value;

      // Arama filtresi
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        filtered = filtered.filter(
          (record) =>
            record.ad_soyad.toLowerCase().includes(query) ||
            record.telefon.toLowerCase().includes(query)
        );
      }

      // Yardım tipi filtresi
      if (selectedYardimTipi.value) {
        filtered = filtered.filter(
          (record) => record.yardim_tipi === selectedYardimTipi.value
        );
      }

      return filtered;
    });

    // Sayfa değiştiğinde görüntülenecek kayıtları güncelle
    watch([currentPage, filteredRecords], () => {
      updateDisplayedRecords();
    });

    // Yardım tipi değiştiğinde sayfayı sıfırla
    watch(selectedYardimTipi, () => {
      currentPage.value = 1;
      updateDisplayedRecords();
    });

    // Arama yapıldığında sayfayı sıfırla
    watch(searchQuery, () => {
      currentPage.value = 1;
      updateDisplayedRecords();
    });

    // Yeni yardım kaydet
    const handleYardimSaved = async () => {
      if (showNewRecordModal.value) {
        showNewRecordModal.value = false;
      }
      if (showEditModal.value) {
        showEditModal.value = false;
      }
      await fetchYardimlar();
    };

    // Yardım detaylarını göster
    const showDetail = async (yardim) => {
      try {
        const response = await apiService.getSahsiYardim(yardim.id);
        selectedYardim.value = response.data;
        showDetailModal.value = true;
      } catch (error) {
        console.error("Yardım detayları yüklenirken hata:", error);
      }
    };

    // Yardım düzenle
    const editRecord = (record) => {
      selectedYardim.value = record;
      showEditModal.value = true;
    };

    // Yardım sil
    const deleteRecord = async (id) => {
      if (confirm("Bu yardım kaydını silmek istediğinizden emin misiniz?")) {
        try {
          await apiService.deleteSahsiYardim(id);
          await fetchYardimlar();
        } catch (error) {
          console.error("Yardım silinirken hata:", error);
        }
      }
    };

    // Filtreleri temizle
    const clearFilters = () => {
      selectedYardimTipi.value = "";
      showFilters.value = false;
    };

    // Dışarı tıklandığında filtreleri kapat
    const handleClickOutside = (event) => {
      const filterButton = event.target.closest(".relative");
      if (!filterButton) {
        showFilters.value = false;
      }
    };

    // Sayfalama hesaplamaları
    const displayedPages = computed(() => {
      const pages = [];
      const maxVisiblePages = 5;

      if (totalPages.value <= maxVisiblePages) {
        for (let i = 1; i <= totalPages.value; i++) {
          pages.push(i);
        }
      } else {
        pages.push(1);

        const start = Math.max(2, currentPage.value - 1);
        const end = Math.min(totalPages.value - 1, currentPage.value + 1);

        if (start > 2) {
          pages.push("...");
        }

        for (let i = start; i <= end; i++) {
          pages.push(i);
        }

        if (end < totalPages.value - 1) {
          pages.push("...");
        }

        pages.push(totalPages.value);
      }

      return pages;
    });

    onMounted(() => {
      fetchYardimlar();
      document.addEventListener("click", handleClickOutside);
    });

    onUnmounted(() => {
      document.removeEventListener("click", handleClickOutside);
    });

    return {
      isOpen,
      showNewRecordModal,
      showDetailModal,
      showEditModal,
      searchQuery,
      yardimlar,
      selectedYardim,
      selectedYardimTipi,
      handleYardimSaved,
      showDetail,
      editRecord,
      deleteRecord,
      currentPage,
      pageSize,
      totalItems,
      totalPages,
      filteredRecords,
      clearSearch,
      showFilters,
      clearFilters,
      displayedPages,
      displayedYardimlar,
    };
  },
};
</script>
