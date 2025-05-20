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
              placeholder="Ad, soyad, dosya no, kimlik no veya adres ara..."
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
            <!-- Filtreleme Butonu -->
            <div class="relative">
              <button
                @click="showFilters = !showFilters"
                class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all duration-200 flex items-center gap-2"
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
              </button>
              <div
                v-if="showFilters"
                class="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg py-2 z-[100] border border-gray-200"
              >
                <div class="px-4 py-2">
                  <div class="mb-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                      >Durum</label
                    >
                    <select
                      v-model="selectedStatus"
                      class="block w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded-lg leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                    >
                      <option value="">Tüm Durumlar</option>
                      <option value="BEKLEMEDE">Beklemede</option>
                      <option value="ONAYLANDI">Onaylandı</option>
                      <option value="REDDEDILDI">Reddedildi</option>
                    </select>
                  </div>
                  <div class="mb-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                      >Kira Durumu</label
                    >
                    <select
                      v-model="selectedKiraDurumu"
                      class="block w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded-lg leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                    >
                      <option value="">Tüm Kira Durumları</option>
                      <option value="KIRACI">Kiracı</option>
                      <option value="EV_SAHIBI">Ev Sahibi</option>
                    </select>
                  </div>
                  <div class="mb-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                      >Engel Durumu</label
                    >
                    <select
                      v-model="selectedEngelDurumu"
                      class="block w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded-lg leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                    >
                      <option value="">Tüm Engel Durumları</option>
                      <option value="engelli">Aile Engel Durumu Var</option>
                      <option value="engelli_degil">
                        Aile Engel Durumu Yok
                      </option>
                    </select>
                  </div>
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
                  <div class="mb-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                      >Aile Üyesi Sayısı</label
                    >
                    <div class="grid grid-cols-2 gap-2">
                      <div>
                        <input
                          v-model="minAileUyesiSayisi"
                          type="number"
                          min="0"
                          max="15"
                          placeholder="Min"
                          class="block w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded-lg leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                        />
                      </div>
                      <div>
                        <input
                          v-model="maxAileUyesiSayisi"
                          type="number"
                          min="0"
                          max="15"
                          placeholder="Max"
                          class="block w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded-lg leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                        />
                      </div>
                    </div>
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
              @click="
                showModal = true;
                editMode = false;
                resetForm();
              "
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
              class="px-8 py-2 bg-green-600 text-white rounded-xl hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200 flex items-center gap-2 text-base font-medium w-48"
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
                  d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
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
                    (currentPage - 1) * itemsPerPage + 1
                  }}</span>
                  -
                  <span class="font-medium">{{
                    Math.min(currentPage * itemsPerPage, totalItems)
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

        <!-- Table -->
        <div class="bg-white rounded-lg shadow">
          <div class="overflow-x-auto">
            <table class="w-full table-fixed">
              <thead class="bg-gray-50">
                <tr>
                  <th
                    class="w-24 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                  >
                    Dosya No
                  </th>
                  <th
                    class="w-32 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                  >
                    Kayıt Tarihi
                  </th>
                  <th
                    class="w-48 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                  >
                    Ad Soyad
                  </th>
                  <th
                    class="w-40 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                  >
                    Kimlik No
                  </th>
                  <th
                    class="w-32 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                  >
                    Telefon
                  </th>
                  <th
                    class="w-64 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Adres
                  </th>
                  <th
                    class="w-32 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                  >
                    Durum
                  </th>
                  <th
                    class="w-48 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                  >
                    Engel Durumu
                  </th>
                  <th
                    class="w-40 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                  >
                    İşlemler
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr
                  v-for="dosya in filteredDosyalar"
                  :key="dosya.dosya_no"
                  class="hover:bg-gray-50"
                >
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center gap-2">
                      <span class="text-gray-900">{{ dosya.dosya_no }}</span>
                      <v-tooltip location="top">
                        <template v-slot:activator="{ props }">
                          <div v-bind="props">
                            <v-icon
                              v-if="getYardimTipi(dosya) === 'individual'"
                              icon="mdi-account"
                              color="blue"
                              size="small"
                            ></v-icon>
                            <v-icon
                              v-else-if="getYardimTipi(dosya) === 'group'"
                              icon="mdi-account-group"
                              color="green"
                              size="small"
                            ></v-icon>
                          </div>
                        </template>
                        <span>{{ getYardimTipiText(dosya) }}</span>
                      </v-tooltip>
                    </div>
                  </td>
                  <td class="px-4 py-4 text-sm whitespace-nowrap">
                    {{ formatDate(dosya.kayit_tarihi) }}
                  </td>
                  <td class="px-4 py-4 text-sm whitespace-nowrap">
                    {{ dosya.ad }} {{ dosya.soyad }}
                  </td>
                  <td class="px-4 py-4 text-sm whitespace-nowrap">
                    {{ dosya.kimlik_no }}
                  </td>
                  <td class="px-4 py-4 text-sm whitespace-nowrap">
                    {{ dosya.telefon }}
                  </td>
                  <td class="px-4 py-4 text-sm">{{ formatAddress(dosya) }}</td>
                  <td class="px-4 py-4 text-sm whitespace-nowrap">
                    <span :class="getStatusClass(dosya.durum)">
                      {{ dosya.durum }}
                    </span>
                  </td>
                  <td class="px-4 py-4 text-sm whitespace-nowrap min-w-[200px]">
                    {{ getEngelDurumuText(dosya) }}
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap">
                    <div class="relative">
                      <v-menu
                        location="bottom end"
                        :close-on-content-click="true"
                        :close-on-click="true"
                      >
                        <template v-slot:activator="{ props }">
                          <v-btn
                            v-bind="props"
                            variant="tonal"
                            density="comfortable"
                            class="text-gray-700 bg-gray-50 hover:bg-gray-100 transition-colors duration-200"
                          >
                            <v-icon
                              icon="mdi-dots-horizontal"
                              class="mr-1"
                            ></v-icon>
                            İşlemler
                          </v-btn>
                        </template>
                        <v-list class="py-2">
                          <v-list-item
                            @click="editDosya(dosya)"
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
                          <v-list-item
                            @click="showDosyaDetay(dosya)"
                            class="hover:bg-gray-50 transition-colors duration-200"
                          >
                            <template v-slot:prepend>
                              <v-icon
                                icon="mdi-eye"
                                color="green"
                                class="mr-2"
                              ></v-icon>
                            </template>
                            <v-list-item-title class="text-sm"
                              >Detay</v-list-item-title
                            >
                          </v-list-item>
                          <v-list-item
                            @click="printDosya(dosya)"
                            class="hover:bg-gray-50 transition-colors duration-200"
                          >
                            <template v-slot:prepend>
                              <v-icon
                                icon="mdi-printer"
                                color="purple"
                                class="mr-2"
                              ></v-icon>
                            </template>
                            <v-list-item-title class="text-sm"
                              >Yazdır</v-list-item-title
                            >
                          </v-list-item>
                          <v-list-item
                            @click="showYardimDetay(dosya)"
                            class="hover:bg-gray-50 transition-colors duration-200"
                          >
                            <template v-slot:prepend>
                              <v-icon
                                icon="mdi-cash-multiple"
                                color="emerald"
                                class="mr-2"
                              ></v-icon>
                            </template>
                            <v-list-item-title class="text-sm"
                              >Yardım Detayları</v-list-item-title
                            >
                          </v-list-item>
                          <v-divider class="my-2"></v-divider>
                          <v-list-item
                            @click="deleteDosya(dosya.dosya_no)"
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
            </table>
          </div>
        </div>

        <DosyaEkleModal
          v-if="showModal"
          :show-modal="showModal"
          :edit-mode="editMode"
          :initial-data="selectedDosya"
          @close="handleModalClose"
          @saved="handleModalSaved"
        />

        <YardimDetayModal
          v-if="showYardimDetayModal"
          :show="showYardimDetayModal"
          :dosya="selectedDosyaForYardim"
          @close="showYardimDetayModal = false"
        />
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import DosyaEkleModal from "../components/DosyaEkleModal.vue";
import YardimDetayModal from "../components/YardimDetayModal.vue";
import apiService from "../api";
import { UYRUK_CHOICES, DURUM_CHOICES, BELGE_TURU_CHOICES } from "../constants";
import * as XLSX from "xlsx";
import { useNavbarStore } from "../store/navbar";
import { printDosya, formatDate, formatAddress } from "../utils/printUtils";

export default {
  name: "Files",
  components: {
    Navbar,
    DosyaEkleModal,
    YardimDetayModal,
  },
  setup() {
    const router = useRouter();
    const navbarStore = useNavbarStore();
    const isOpen = computed(() => navbarStore.isOpen);
    const username = ref(localStorage.getItem("username") || "");
    const dosyalar = ref([]);
    const showModal = ref(false);
    const editMode = ref(false);
    const selectedDosya = ref(null);
    const searchQuery = ref("");
    const selectedStatus = ref("");
    const selectedKiraDurumu = ref("");
    const selectedEngelDurumu = ref("");
    const minAileUyesiSayisi = ref(null);
    const maxAileUyesiSayisi = ref(null);
    const showFilters = ref(false);
    const currentPage = ref(1);
    const itemsPerPage = ref(10);
    const totalItems = ref(0);
    const activeOperations = ref(null);
    const isLoading = ref(false);
    const showYardimDetayModal = ref(false);
    const selectedDosyaForYardim = ref(null);
    const selectedYardimTipi = ref("");
    const showNoResults = ref(false);
    const error = ref(null);

    const totalPages = computed(() => {
      return Math.ceil(totalItems.value / itemsPerPage.value);
    });

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

    const filteredDosyalar = computed(() => {
      if (!searchQuery.value) return dosyalar.value;
      const query = searchQuery.value.toLowerCase();
      return dosyalar.value.filter((dosya) => {
        // String değerleri kontrol et
        const ad = (dosya.ad || "").toString().toLowerCase();
        const soyad = (dosya.soyad || "").toString().toLowerCase();
        const adres = (dosya.adres || "").toString().toLowerCase();

        // Sayısal değerleri string'e çevir
        const dosyaNo = (dosya.dosya_no || "").toString();
        const kimlikNo = (dosya.kimlik_no || "").toString();

        return (
          ad.includes(query) ||
          soyad.includes(query) ||
          dosyaNo.includes(query) ||
          kimlikNo.includes(query) ||
          adres.includes(query)
        );
      });
    });

    // Yardım tipini al
    const getYardimTipi = (dosya) => {
      if (dosya.yardim_tipi === "individual" || dosya.yardim_tipi === "group") {
        return dosya.yardim_tipi;
      }
      return null;
    };

    // Yardım tipi metnini al
    const getYardimTipiText = (dosya) => {
      const tip = getYardimTipi(dosya);
      if (tip === "individual") {
        return "Bireysel Yardım";
      } else if (tip === "group") {
        return "Grup Yardımı";
      }
      return "";
    };

    // Durum sınıfını al
    const getStatusClass = (status) => {
      const statusClasses = {
        BEKLEMEDE: "bg-yellow-100 text-yellow-800",
        ONAYLANDI: "bg-green-100 text-green-800",
        REDDEDILDI: "bg-red-100 text-red-800",
      };
      return statusClasses[status] || "bg-gray-100 text-gray-800";
    };

    // Engel durumu metnini al
    const getEngelDurumuText = (dosya) => {
      if (!dosya.aile_bilgileri || dosya.aile_bilgileri.length === 0) {
        return dosya.engel_durumu
          ? "Aile Engel Durumu Var"
          : "Aile Engel Durumu Yok";
      }

      const engelliCount = dosya.aile_bilgileri.filter(
        (member) => member.engel_durumu
      ).length;
      const hasEngelli = engelliCount > 0 || dosya.engel_durumu;

      return hasEngelli
        ? `Aile Engel Durumu Var (${
            engelliCount + (dosya.engel_durumu ? 1 : 0)
          } kişi)`
        : "Aile Engel Durumu Yok";
    };

    // Filtreleri temizle
    const clearFilters = () => {
      selectedStatus.value = "";
      selectedKiraDurumu.value = "";
      selectedEngelDurumu.value = "";
      selectedYardimTipi.value = "";
      minAileUyesiSayisi.value = null;
      maxAileUyesiSayisi.value = null;
    };

    // Arama sorgusunu temizle
    const clearSearch = () => {
      searchQuery.value = "";
    };

    const handleSearch = () => {
      currentPage.value = 1;
      loadDosyalar();
    };

    const loadDosyalar = async () => {
      try {
        isLoading.value = true;
        error.value = null;
        const params = new URLSearchParams();
        params.append("page", currentPage.value);
        params.append("page_size", itemsPerPage.value);

        // Arama filtresi - trim ve boşluk kontrolü ekle
        if (searchQuery.value && searchQuery.value.trim()) {
          params.append("search", searchQuery.value.trim());
        }

        // Durum filtresi
        if (selectedStatus.value) {
          params.append("status", selectedStatus.value);
        }

        // Kira durumu filtresi
        if (selectedKiraDurumu.value) {
          params.append("kira_durumu", selectedKiraDurumu.value);
        }

        // Engel durumu filtresi
        if (selectedEngelDurumu.value === "engelli") {
          params.append("engel_durumu", "true");
        } else if (selectedEngelDurumu.value === "engelli_degil") {
          params.append("engel_durumu", "false");
        }

        // Aile üyesi sayısı filtresi
        if (minAileUyesiSayisi.value) {
          params.append("min_aile_uyesi_sayisi", minAileUyesiSayisi.value);
        }
        if (maxAileUyesiSayisi.value) {
          params.append("max_aile_uyesi_sayisi", maxAileUyesiSayisi.value);
        }

        // Yardım tipi filtresi
        if (selectedYardimTipi.value) {
          params.append("sahsi_yardim_tipi", selectedYardimTipi.value);
        }

        console.log("Search params:", params.toString());

        // Dosya verilerini al
        const response = await apiService.get(
          `/dosyalar/?${params.toString()}`
        );
        console.log("API Response:", response.data);

        if (!response.data || !response.data.results) {
          console.error("Invalid response format:", response.data);
          dosyalar.value = [];
          totalItems.value = 0;
          return;
        }

        const dosyaData = response.data.results;

        // Yardım verilerini al
        const yardimResponse = await apiService.getSahsiYardimlar();
        const yardimlar = yardimResponse.data.results || yardimResponse.data;

        // Dosya verilerini işle ve yardım tipini ekle
        dosyalar.value = dosyaData.map((dosya) => {
          const yardim = yardimlar.find(
            (y) => y.dosyalar && y.dosyalar.some((d) => d.id === dosya.id)
          );
          return {
            ...dosya,
            yardim_tipi: yardim ? yardim.yardim_tipi : null,
          };
        });

        console.log("Processed dosyalar:", dosyalar.value);

        // Toplam kayıt sayısını güncelle
        totalItems.value = response.data.count || 0;

        // Filtreleme yapıldıysa ve sonuç yoksa
        if (
          totalItems.value === 0 &&
          (searchQuery.value ||
            selectedStatus.value ||
            selectedKiraDurumu.value ||
            selectedEngelDurumu.value ||
            minAileUyesiSayisi.value ||
            maxAileUyesiSayisi.value ||
            selectedYardimTipi.value)
        ) {
          showNoResults.value = true;
        } else {
          showNoResults.value = false;
        }
      } catch (error) {
        console.error("Dosyalar yüklenirken hata:", error);
        console.error("Hata detayı:", error.response?.data);
        error.value = "Dosyalar yüklenirken bir hata oluştu.";
        dosyalar.value = [];
        totalItems.value = 0;
      } finally {
        isLoading.value = false;
      }
    };

    // Debounce fonksiyonu ekle
    const debounce = (fn, delay) => {
      let timeoutId;
      return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn(...args), delay);
      };
    };

    // Debounced loadDosyalar fonksiyonu
    const debouncedLoadDosyalar = debounce(() => {
      currentPage.value = 1; // Arama yapıldığında ilk sayfaya dön
      loadDosyalar();
    }, 300);

    // Filtreler değiştiğinde dosyaları yeniden yükle
    watch(
      [
        selectedStatus,
        selectedKiraDurumu,
        selectedEngelDurumu,
        selectedYardimTipi,
        minAileUyesiSayisi,
        maxAileUyesiSayisi,
      ],
      () => {
        currentPage.value = 1; // Filtre değiştiğinde ilk sayfaya dön
        loadDosyalar();
      }
    );

    // Arama sorgusu değiştiğinde debounced fonksiyonu çağır
    watch(searchQuery, (newValue) => {
      console.log("Search query changed:", newValue);
      debouncedLoadDosyalar();
    });

    // Sayfa değiştiğinde dosyaları yeniden yükle
    watch(currentPage, () => {
      loadDosyalar();
    });

    // Sayfa yüklendiğinde verileri getir
    onMounted(() => {
      loadDosyalar();
    });

    const editDosya = async (dosya) => {
      try {
        const response = await apiService.getDosya(dosya.dosya_no || dosya.id);
        const detailedDosya = response.data;
        editMode.value = true;
        showModal.value = true;
        selectedDosya.value = detailedDosya;
      } catch (error) {
        console.error("Düzenleme hatası:", error);
        alert("Dosya bilgileri getirilemedi");
      }
    };

    const deleteDosya = async (dosyaNo) => {
      if (confirm("Bu kaydı silmek istediğinizden emin misiniz?")) {
        try {
          await apiService.deleteDosya(dosyaNo);
          await loadDosyalar();
          alert("Dosya başarıyla silindi.");
        } catch (error) {
          console.error("Silme hatası:", error);
          alert(
            `Dosya silinirken bir hata oluştu: ${
              error.response?.data?.error || error.message
            }`
          );
        }
      }
    };

    const showDosyaDetay = (dosya) => {
      router.push(`/dosya/${dosya.dosya_no}`);
    };

    const handleDetaySaved = async (updatedDosya) => {
      try {
        await loadDosyalar();
        selectedDosya.value = null;
      } catch (error) {
        console.error("Güncelleme hatası:", error);
      }
    };

    const handleDosyaUpdate = async (updatedDosya) => {
      try {
        await loadDosyalar();
        if (
          selectedDosya.value &&
          selectedDosya.value.dosya_no === updatedDosya.dosya_no
        ) {
          selectedDosya.value = { ...updatedDosya };
        }
      } catch (error) {
        console.error("Güncelleme hatası:", error);
      }
    };

    const handleModalSaved = async () => {
      try {
        await loadDosyalar();
        showModal.value = false;
        editMode.value = false;
        selectedDosya.value = null;
      } catch (error) {
        console.error("Güncelleme hatası:", error);
      }
    };

    const handleModalClose = () => {
      showModal.value = false;
      editMode.value = false;
      selectedDosya.value = null;
    };

    const printDosyaHandler = async (dosya) => {
      await printDosya(dosya, apiService);
    };

    const exportToExcel = async () => {
      try {
        // Filtreleme parametrelerini oluştur
        const params = new URLSearchParams();
        if (searchQuery.value) params.append("search", searchQuery.value);
        if (selectedStatus.value) params.append("status", selectedStatus.value);
        if (selectedKiraDurumu.value)
          params.append("kira_durumu", selectedKiraDurumu.value);
        if (selectedEngelDurumu.value)
          params.append("engel_durumu", selectedEngelDurumu.value);
        if (minAileUyesiSayisi.value)
          params.append("min_aile_uyesi_sayisi", minAileUyesiSayisi.value);
        if (maxAileUyesiSayisi.value)
          params.append("max_aile_uyesi_sayisi", maxAileUyesiSayisi.value);
        if (selectedYardimTipi.value)
          params.append("sahsi_yardim_tipi", selectedYardimTipi.value);

        // Backend'den Excel dosyasını al
        const response = await apiService.get(
          `/dosyalar/export_excel/?${params.toString()}`,
          {
            responseType: "blob",
          }
        );

        // Dosya adını oluştur
        const fileName = `DosyaKayitlari_${new Date()
          .toLocaleDateString("tr-TR")
          .replace(/\./g, "-")}.xlsx`;

        // Dosyayı indir
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", fileName);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error("Excel export error:", error);
        alert(
          "Excel dosyası oluşturulurken bir hata oluştu. Lütfen daha sonra tekrar deneyin."
        );
      }
    };

    const showYardimDetay = async (dosya) => {
      try {
        // Dosya bilgilerini al
        const dosyaResponse = await apiService.getDosya(dosya.dosya_no);
        selectedDosyaForYardim.value = dosyaResponse.data;

        // Maddi yardım verilerini al
        const yardimResponse = await apiService.getMaddiYardimlar();
        const yardimlar = yardimResponse.data.results || yardimResponse.data;

        // Bu dosyaya ait tüm yardımları filtrele
        const dosyaYardimlari = yardimlar.filter((yardim) => {
          if (!yardim.dosya_bilgileri) return false;

          // Dosya bilgileri bir dizi ise
          if (Array.isArray(yardim.dosya_bilgileri)) {
            return yardim.dosya_bilgileri.some(
              (db) => db.dosya_bilgisi.dosya_no === dosya.dosya_no
            );
          }

          return false;
        });

        // Her bir yardımın detaylarını al
        const yardimDetaylari = await Promise.all(
          dosyaYardimlari.map(async (yardim) => {
            const detayResponse = await apiService.getMaddiYardim(yardim.id);
            const detay = detayResponse.data;

            // Bu dosyaya ait tutarı bul
            let dosyaTutari = 0;
            if (detay.dosya_bilgileri && Array.isArray(detay.dosya_bilgileri)) {
              const dosyaBilgisi = detay.dosya_bilgileri.find(
                (db) => db.dosya_bilgisi.dosya_no === dosya.dosya_no
              );
              dosyaTutari = dosyaBilgisi?.tutar || 0;
            }

            // Yardım detayını düzenle
            return {
              id: detay.id,
              yardim_tipi: "maddi",
              tutar: dosyaTutari,
              created_at: detay.created_at,
              yardim_yapan_ad_soyad: detay.yardim_yapan_ad_soyad,
              yardim_yapan_telefon: detay.yardim_yapan_telefon,
              aciklama: detay.aciklama,
              dosya_no: dosya.dosya_no,
              manuel_kayitlar: detay.manuel_kayitlar || [],
            };
          })
        );

        // Tüm yardım detaylarını dosya bilgilerine ekle
        selectedDosyaForYardim.value.yardimlar = yardimDetaylari;
        showYardimDetayModal.value = true;
      } catch (error) {
        console.error("Yardım detayları yüklenirken hata:", error);
        console.error("Hata detayı:", error.response?.data);
      }
    };

    const toggleOperations = (dosyaNo) => {
      if (activeOperations.value === dosyaNo) {
        activeOperations.value = null;
      } else {
        activeOperations.value = dosyaNo;
      }
    };

    const resetForm = () => {
      selectedDosya.value = null;
      editMode.value = false;
    };

    return {
      dosyalar,
      showModal,
      editMode,
      selectedDosya,
      searchQuery,
      selectedStatus,
      selectedKiraDurumu,
      selectedEngelDurumu,
      minAileUyesiSayisi,
      maxAileUyesiSayisi,
      username,
      getStatusClass,
      loadDosyalar,
      editDosya,
      deleteDosya,
      showDosyaDetay,
      handleDetaySaved,
      formatDate,
      formatAddress,
      handleDosyaUpdate,
      handleModalSaved,
      handleModalClose,
      UYRUK_CHOICES,
      DURUM_CHOICES,
      printDosya: printDosyaHandler,
      exportToExcel,
      filteredDosyalar,
      currentPage,
      totalPages,
      displayedPages,
      totalItems,
      activeOperations,
      toggleOperations,
      resetForm,
      showFilters,
      isOpen,
      isLoading,
      getEngelDurumuText,
      clearSearch,
      clearFilters,
      showYardimDetayModal,
      selectedDosyaForYardim,
      showYardimDetay,
      getYardimTipi,
      getYardimTipiText,
      selectedYardimTipi,
      itemsPerPage,
      showNoResults,
      error,
      handleSearch,
    };
  },
};
</script>

<style scoped>
.sticky {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
