<template>
  <div
    v-if="show"
    class="fixed inset-0 backdrop-blur-sm bg-black/30 flex items-center justify-center z-50 overflow-y-auto"
  >
    <div class="bg-white rounded-lg w-full max-w-2xl my-8 flex flex-col">
      <!-- Modal Header -->
      <div class="p-6 border-b border-gray-200">
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold">Yeni Şahsi Yardım Kaydı</h2>
          <button
            @click="$emit('close')"
            class="text-gray-500 hover:text-gray-700 focus:outline-none"
          >
            <svg
              class="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
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

      <!-- Modal Content -->
      <div class="p-6 overflow-y-auto">
        <!-- Yardım Tipi Seçimi -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >Yardım Tipi</label
          >
          <div class="flex gap-4">
            <button
              @click="selectedType = 'individual'"
              :class="[
                'px-4 py-2 rounded-lg',
                selectedType === 'individual'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
              ]"
            >
              Bireysel
            </button>
            <button
              @click="selectedType = 'group'"
              :class="[
                'px-4 py-2 rounded-lg',
                selectedType === 'group'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
              ]"
            >
              Grup
            </button>
          </div>
        </div>

        <!-- Bireysel Form -->
        <div v-if="selectedType === 'individual'" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Ad Soyad</label
            >
            <input
              v-model="formData.ad_soyad"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Telefon</label
            >
            <input
              v-model="formData.telefon"
              type="tel"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        <!-- Grup Form -->
        <div v-if="selectedType === 'group'" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Grup Üye Sayısı</label
            >
            <input
              v-model="formData.grup_uye_sayisi"
              type="number"
              min="1"
              @wheel.prevent
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <!-- Yardım Eden Kişiler -->
          <div v-if="formData.grup_uye_sayisi > 0" class="space-y-3">
            <div
              v-for="(helper, index) in parseInt(formData.grup_uye_sayisi)"
              :key="index"
              class="p-3 border border-gray-200 rounded-lg bg-gray-50"
            >
              <h4 class="text-sm font-medium text-gray-700 mb-2">
                Yardım Eden Kişi {{ index + 1 }}
              </h4>
              <div class="space-y-2">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1"
                    >Ad Soyad</label
                  >
                  <input
                    v-model="formData.yardimcilar[index].ad_soyad"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1"
                    >Telefon</label
                  >
                  <input
                    v-model="formData.yardimcilar[index].telefon"
                    type="tel"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Dosya Arama ve Seçme -->
        <div class="mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-2">
            Yardım Yapılacak Aileler
          </h4>
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
              placeholder="Dosya no, ad veya soyad ile arayın..."
              @input="searchDosyalar"
            />
            <!-- Arama Sonuçları -->
            <div
              v-if="searchResults.length > 0 && showResults"
              class="absolute z-10 w-full mt-1 bg-white shadow-lg rounded-md border border-gray-200 max-h-60 overflow-y-auto"
            >
              <div
                v-for="dosya in filteredSearchResults"
                :key="dosya.id"
                class="p-2 hover:bg-gray-100 cursor-pointer"
                @click="selectDosya(dosya)"
              >
                <div class="font-medium">{{ dosya.ad }} {{ dosya.soyad }}</div>
                <div class="text-sm text-gray-600">
                  Dosya No: {{ dosya.dosya_no }} - Tel: {{ dosya.telefon }}
                </div>
                <div class="text-sm text-gray-500">
                  {{ dosya.mahalle }} Mah. {{ dosya.cadde_sokak }}
                </div>
              </div>
            </div>
          </div>

          <!-- Seçilen Dosyalar -->
          <div v-if="selectedDosyalar.length > 0" class="mt-2 space-y-2">
            <div
              v-for="dosya in selectedDosyalar"
              :key="dosya.id"
              class="flex justify-between items-center p-3 bg-purple-50 rounded-md border border-purple-200"
            >
              <div class="flex-1">
                <div class="font-medium text-purple-800">
                  {{ dosya.ad }} {{ dosya.soyad }}
                </div>
                <div class="text-sm text-purple-600">
                  Dosya No: {{ dosya.dosya_no }}
                </div>
                <div class="text-sm text-purple-600">
                  {{ dosya.mahalle }} Mah. {{ dosya.cadde_sokak }}
                </div>
              </div>
              <button
                type="button"
                @click="removeDosya(dosya)"
                class="text-red-600 hover:text-red-800"
              >
                <svg
                  class="h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
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
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="p-6 border-t border-gray-200 bg-gray-50">
        <div class="flex justify-end gap-3">
          <button
            @click="$emit('close')"
            class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors"
          >
            İptal
          </button>
          <button
            @click="saveRecord"
            class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Kaydet
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, computed, onMounted } from "vue";
import apiService from "../api";

export default {
  name: "SahsiYardimEkleModal",
  props: {
    show: {
      type: Boolean,
      required: true,
    },
  },
  emits: ["close", "saved"],
  setup(props, { emit }) {
    const selectedType = ref("individual");
    const searchQuery = ref("");
    const searchResults = ref([]);
    const showResults = ref(false);
    const selectedDosyalar = ref([]);

    const formData = ref({
      yardim_tipi: "individual",
      ad_soyad: "",
      telefon: "",
      grup_uye_sayisi: null,
      yardimcilar: [],
      dosyalar: [],
    });

    const filteredSearchResults = computed(() => {
      return searchResults.value.filter(
        (dosya) =>
          !selectedDosyalar.value.some((selected) => selected.id === dosya.id)
      );
    });

    const searchDosyalar = async () => {
      if (searchQuery.value.length < 2) {
        searchResults.value = [];
        showResults.value = false;
        return;
      }

      try {
        const response = await apiService.getDosyalar(1, 10, {
          search: searchQuery.value,
        });
        searchResults.value = response.data.results || response.data;
        showResults.value = true;
      } catch (error) {
        console.error("Dosyalar aranırken hata:", error);
        searchResults.value = [];
      }
    };

    const loadDosyalar = async () => {
      try {
        const response = await apiService.getDosyalar(1, 10);
        searchResults.value = response.data.results || response.data;
      } catch (error) {
        console.error("Dosyalar yüklenirken hata:", error);
        searchResults.value = [];
      }
    };

    const selectDosya = (dosya) => {
      if (
        !selectedDosyalar.value.some((selected) => selected.id === dosya.id)
      ) {
        selectedDosyalar.value.push(dosya);
        formData.value.dosyalar.push(dosya.id);
      }
      searchQuery.value = "";
      showResults.value = false;
    };

    const removeDosya = (dosya) => {
      selectedDosyalar.value = selectedDosyalar.value.filter(
        (d) => d.id !== dosya.id
      );
      formData.value.dosyalar = formData.value.dosyalar.filter(
        (id) => id !== dosya.id
      );
    };

    const resetForm = () => {
      formData.value = {
        yardim_tipi: "individual",
        ad_soyad: "",
        telefon: "",
        grup_uye_sayisi: null,
        yardimcilar: [],
        dosyalar: [],
      };
      selectedDosyalar.value = [];
      searchQuery.value = "";
      searchResults.value = [];
      showResults.value = false;
    };

    const saveRecord = async () => {
      console.log("Form verileri:", JSON.stringify(formData.value, null, 2));
      console.log("Seçilen tip:", selectedType.value);

      // Validasyon kontrolleri
      if (selectedType.value === "individual") {
        if (!formData.value.ad_soyad || !formData.value.ad_soyad.trim()) {
          alert("Ad Soyad alanı zorunludur");
          return;
        }
        if (!formData.value.telefon || !formData.value.telefon.trim()) {
          alert("Telefon alanı zorunludur");
          return;
        }
      } else if (selectedType.value === "group") {
        // Grup validasyonu
        if (
          !formData.value.grup_uye_sayisi ||
          formData.value.grup_uye_sayisi < 1
        ) {
          alert("Grup üye sayısı en az 1 olmalıdır");
          return;
        }

        // Yardımcıların bilgilerini kontrol et
        for (let i = 0; i < formData.value.yardimcilar.length; i++) {
          const helper = formData.value.yardimcilar[i];
          if (!helper.ad_soyad?.trim()) {
            alert(
              `${i + 1}. yardım eden kişinin ad soyad bilgisi doldurulmalıdır`
            );
            return;
          }
          if (!helper.telefon?.trim()) {
            alert(
              `${i + 1}. yardım eden kişinin telefon bilgisi doldurulmalıdır`
            );
            return;
          }
        }

        // Grup seçildiğinde ilk yardımcının bilgilerini bireysel alanlara da kopyala
        if (formData.value.yardimcilar.length > 0) {
          formData.value.ad_soyad = formData.value.yardimcilar[0].ad_soyad;
          formData.value.telefon = formData.value.yardimcilar[0].telefon;
        }
      }

      if (formData.value.dosyalar.length === 0) {
        alert("En az bir dosya seçmelisiniz");
        return;
      }

      try {
        const data = {
          yardim_tipi: selectedType.value,
          ad_soyad: formData.value.ad_soyad.trim(),
          telefon: formData.value.telefon.trim(),
          grup_uye_sayisi:
            selectedType.value === "group"
              ? parseInt(formData.value.grup_uye_sayisi)
              : null,
          yardimcilar:
            selectedType.value === "group"
              ? formData.value.yardimcilar.map((helper) => ({
                  ad_soyad: helper.ad_soyad.trim(),
                  telefon: helper.telefon.trim(),
                }))
              : [],
          dosyalar: formData.value.dosyalar,
        };

        console.log("Gönderilecek veri:", JSON.stringify(data, null, 2));
        const response = await apiService.createSahsiYardim(data);
        console.log("API Yanıtı:", response);

        if (response && response.data) {
          emit("saved");
          emit("close");
          resetForm();
        }
      } catch (error) {
        console.error("Form gönderilirken hata:", error);
        console.error("Hata detayları:", error.response?.data);

        if (error.response?.data) {
          const errorMessages = Object.entries(error.response.data)
            .map(([key, value]) => {
              if (Array.isArray(value)) {
                return `${key}: ${value.join(", ")}`;
              }
              return `${key}: ${value}`;
            })
            .join("\n");
          alert(`Hata:\n${errorMessages}`);
        } else {
          alert("Bir hata oluştu. Lütfen tekrar deneyin.");
        }
      }
    };

    onMounted(() => {
      loadDosyalar();
      formData.value = {
        yardim_tipi: "individual",
        ad_soyad: "",
        telefon: "",
        grup_uye_sayisi: null,
        yardimcilar: [],
        dosyalar: [],
      };
    });

    // Grup üye sayısı değiştiğinde helpers array'ini güncelle
    watch(
      () => formData.value.grup_uye_sayisi,
      (newSize) => {
        const size = parseInt(newSize) || 0;
        // Mevcut yardımcıların bilgilerini koru
        const currentHelpers = [...formData.value.yardimcilar];
        formData.value.yardimcilar = Array(size)
          .fill()
          .map((_, index) => ({
            ad_soyad: currentHelpers[index]?.ad_soyad || "",
            telefon: currentHelpers[index]?.telefon || "",
          }));

        // İlk yardımcının bilgilerini bireysel alanlara kopyala
        if (size > 0 && currentHelpers[0]) {
          formData.value.ad_soyad = currentHelpers[0].ad_soyad;
          formData.value.telefon = currentHelpers[0].telefon;
        }
      }
    );

    // selectedType değiştiğinde formData.yardim_tipi'ni güncelle
    watch(
      () => selectedType.value,
      (newType) => {
        formData.value.yardim_tipi = newType;
        // Tip değiştiğinde ilgili alanları sıfırla
        if (newType === "individual") {
          formData.value.grup_uye_sayisi = null;
          formData.value.yardimcilar = [];
        } else if (newType === "group") {
          // Grup seçildiğinde bireysel alanları sıfırlama
          // İlk yardımcı eklendiğinde otomatik dolacak
        }
      }
    );

    return {
      selectedType,
      formData,
      searchQuery,
      searchResults,
      showResults,
      selectedDosyalar,
      filteredSearchResults,
      searchDosyalar,
      loadDosyalar,
      selectDosya,
      removeDosya,
      saveRecord,
      resetForm,
    };
  },
};
</script>
