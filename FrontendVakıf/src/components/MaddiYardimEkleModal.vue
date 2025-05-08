<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div
      class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0"
    >
      <div class="fixed inset-0 transition-opacity" aria-hidden="true">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div>

      <div
        class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full"
      >
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                Maddi Yardım Ekle
              </h3>

              <form @submit.prevent="handleSubmit" class="space-y-4">
                <!-- Yardım Yapan Bilgileri -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700"
                      >Yardım Yapan Ad Soyad</label
                    >
                    <input
                      v-model="form.yardim_yapan_ad_soyad"
                      type="text"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                      required
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700"
                      >Yardım Yapan Telefon</label
                    >
                    <input
                      v-model="form.yardim_yapan_telefon"
                      type="tel"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                      required
                    />
                  </div>
                </div>

                <!-- Aile Seçimi -->
                <div class="mt-4">
                  <div class="flex items-center justify-between mb-2">
                    <h4 class="text-sm font-medium text-gray-700">
                      Yardım Alacak Aileler
                    </h4>
                    <div class="flex items-center space-x-2">
                      <button
                        type="button"
                        @click="showManualEntry = !showManualEntry"
                        class="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                      >
                        <svg
                          class="h-4 w-4 mr-1"
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
                        Manuel Kayıt
                      </button>
                    </div>
                  </div>

                  <!-- Manuel Kayıt Formu -->
                  <div
                    v-if="showManualEntry"
                    class="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200"
                  >
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label class="block text-sm font-medium text-gray-700"
                          >Ad Soyad</label
                        >
                        <input
                          v-model="manualEntry.ad_soyad"
                          type="text"
                          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                          required
                        />
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-gray-700"
                          >TC Kimlik No</label
                        >
                        <input
                          v-model="manualEntry.tc_kimlik"
                          type="text"
                          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                          required
                        />
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-gray-700"
                          >Telefon</label
                        >
                        <input
                          v-model="manualEntry.telefon"
                          type="tel"
                          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                          required
                        />
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-gray-700"
                          >Adres</label
                        >
                        <input
                          v-model="manualEntry.adres"
                          type="text"
                          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                          required
                        />
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-gray-700"
                          >Tutar</label
                        >
                        <input
                          v-model="manualEntry.tutar"
                          type="number"
                          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                          required
                        />
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-gray-700"
                          >Açıklama</label
                        >
                        <input
                          v-model="manualEntry.aciklama"
                          type="text"
                          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                        />
                      </div>
                    </div>
                    <div class="mt-4 flex justify-end">
                      <button
                        type="button"
                        @click="addManualEntry"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                      >
                        Ekle
                      </button>
                    </div>
                  </div>

                  <!-- Arama Kutusu -->
                  <div class="relative">
                    <input
                      v-model="searchQuery"
                      type="text"
                      placeholder="Dosya no, ad veya soyad ile arayın..."
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                      @input="searchAileler"
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
                        @click="selectAile(dosya)"
                      >
                        <div class="font-medium">
                          {{ dosya.ad }} {{ dosya.soyad }}
                        </div>
                        <div class="text-sm text-gray-600">
                          Dosya No: {{ dosya.dosya_no }} - Tel:
                          {{ dosya.telefon }}
                        </div>
                        <div class="text-sm text-gray-500">
                          {{ dosya.mahalle }} Mah. {{ dosya.cadde_sokak }}
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Seçili Aileler -->
                  <div
                    v-if="form.dosyalar && form.dosyalar.length > 0"
                    class="mt-4"
                  >
                    <h4 class="text-sm font-medium text-gray-700 mb-2">
                      Seçili Aileler
                    </h4>
                    <div class="space-y-2">
                      <div
                        v-for="aile in form.dosyalar"
                        :key="aile.id"
                        class="flex items-center justify-between p-2 bg-gray-50 rounded-md"
                      >
                        <div class="flex items-center space-x-4">
                          <div class="flex-shrink-0">
                            <div class="font-medium">
                              {{ aile.ad_soyad || `${aile.ad} ${aile.soyad}` }}
                            </div>
                            <div class="text-sm text-gray-500">
                              {{
                                aile.dosya_no
                                  ? `Dosya No: ${aile.dosya_no}`
                                  : "Manuel Kayıt"
                              }}
                            </div>
                          </div>
                          <div class="flex items-center space-x-2">
                            <span
                              :class="[
                                'px-2 py-1 rounded-full text-xs font-medium',
                                getStatusClass(aile.durum || 'manuel'),
                              ]"
                            >
                              {{ aile.durum || "Manuel Kayıt" }}
                            </span>
                          </div>
                        </div>
                        <div class="flex items-center space-x-4">
                          <div class="flex items-center space-x-2">
                            <label class="text-sm text-gray-700">Tutar:</label>
                            <input
                              v-model="aile.tutar"
                              type="number"
                              class="w-24 rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                              placeholder="0"
                            />
                          </div>
                          <button
                            v-if="aile.dosya_no"
                            type="button"
                            @click="openDosyaDetay(aile)"
                            class="text-blue-600 hover:text-blue-800"
                          >
                            {{ aile.dosya_no }}
                          </button>
                          <button
                            type="button"
                            class="text-red-600 hover:text-red-800"
                            @click="removeAile(aile)"
                          >
                            Kaldır
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Toplam Tutar -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700"
                      >Yardım Tutarı</label
                    >
                    <input
                      v-model="form.yardim_tutar"
                      type="number"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                      required
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700"
                      >Toplam Tutar</label
                    >
                    <input
                      v-model="form.tutar"
                      type="number"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500 bg-gray-50"
                      readonly
                    />
                  </div>
                </div>

                <!-- Açıklama -->
                <div>
                  <label class="block text-sm font-medium text-gray-700"
                    >Açıklama</label
                  >
                  <textarea
                    v-model="form.aciklama"
                    rows="3"
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                    placeholder="Yardım hakkında açıklama ekleyin..."
                  ></textarea>
                </div>
              </form>
            </div>
          </div>
        </div>

        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-purple-600 text-base font-medium text-white hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:ml-3 sm:w-auto sm:text-sm"
            @click="handleSubmit"
            :disabled="loading"
          >
            <svg
              v-if="loading"
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            {{ loading ? "Kaydediliyor..." : "Kaydet" }}
          </button>
          <button
            type="button"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            @click="handleClose"
          >
            İptal
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, onUnmounted } from "vue";
import apiService from "../api";
import { useRouter } from "vue-router";

export default {
  name: "MaddiYardimEkleModal",
  props: {
    show: {
      type: Boolean,
      required: true,
    },
  },
  emits: ["close", "saved"],
  setup(props, { emit }) {
    const loading = ref(false);
    const formErrors = ref({});
    const form = ref({
      yardim_yapan_ad_soyad: "",
      yardim_yapan_telefon: "",
      yardim_tutar: 0,
      tutar: 0,
      aciklama: "",
      dosyalar: [],
      dosya_tutarlari_list: [],
      manuel_kayitlar_list: [],
    });

    const searchQuery = ref("");
    const searchResults = ref([]);
    const showResults = ref(false);
    const filteredSearchResults = ref([]);
    const showManualEntry = ref(false);
    const manualEntry = ref({
      ad_soyad: "",
      tc_kimlik: "",
      telefon: "",
      adres: "",
      tutar: 0,
      aciklama: "",
    });

    const router = useRouter();

    // Manuel kayıt ekleme
    const addManualEntry = () => {
      if (
        !manualEntry.value.ad_soyad ||
        !manualEntry.value.tc_kimlik ||
        !manualEntry.value.telefon ||
        !manualEntry.value.adres
      ) {
        return;
      }

      const newEntry = {
        id: `manual_${Date.now()}`,
        ad_soyad: manualEntry.value.ad_soyad,
        tc_kimlik: manualEntry.value.tc_kimlik,
        telefon: manualEntry.value.telefon,
        adres: manualEntry.value.adres,
        tutar: Number(manualEntry.value.tutar) || 0,
        aciklama: manualEntry.value.aciklama,
        durum: "manuel",
      };

      form.value.dosyalar.push(newEntry);
      updateTotalTutar();

      // Manuel giriş formunu temizle
      manualEntry.value = {
        ad_soyad: "",
        tc_kimlik: "",
        telefon: "",
        adres: "",
        tutar: 0,
        aciklama: "",
      };
      showManualEntry.value = false;
    };

    // Status class helper function
    const getStatusClass = (status) => {
      switch (status) {
        case "aktif":
          return "bg-green-100 text-green-800";
        case "pasif":
          return "bg-red-100 text-red-800";
        case "beklemede":
          return "bg-yellow-100 text-yellow-800";
        case "manuel":
          return "bg-blue-100 text-blue-800";
        default:
          return "bg-gray-100 text-gray-800";
      }
    };

    // Arama fonksiyonu
    const searchAileler = async () => {
      if (searchQuery.value.length < 2) {
        searchResults.value = [];
        showResults.value = false;
        return;
      }

      try {
        const response = await apiService.searchDosyalar(searchQuery.value);
        searchResults.value = response.data.results || response.data;
        filteredSearchResults.value = searchResults.value.filter(
          (dosya) =>
            !form.value.dosyalar.some((selected) => selected.id === dosya.id)
        );
        showResults.value = true;
      } catch (error) {
        console.error("Arama yapılırken hata:", error);
        searchResults.value = [];
        showResults.value = false;
      }
    };

    // Aile seçme fonksiyonu
    const selectAile = (dosya) => {
      if (!form.value.dosyalar.some((selected) => selected.id === dosya.id)) {
        form.value.dosyalar.push({
          ...dosya,
          tutar: 0,
        });
        updateTotalTutar();
      }
      searchQuery.value = "";
      showResults.value = false;
    };

    // Aile kaldırma fonksiyonu
    const removeAile = (dosya) => {
      const index = form.value.dosyalar.findIndex((a) => a.id === dosya.id);
      if (index !== -1) {
        form.value.dosyalar.splice(index, 1);
        updateTotalTutar();
      }
    };

    // Toplam tutarı güncelle
    const updateTotalTutar = () => {
      const toplamTutar = form.value.dosyalar.reduce(
        (total, dosya) => total + (Number(dosya.tutar) || 0),
        0
      );
      form.value.tutar = toplamTutar;
    };

    // Tutar değişikliğini izle
    watch(
      () => form.value.dosyalar,
      () => {
        updateTotalTutar();
      },
      { deep: true }
    );

    // Dosya detayını göster
    const openDosyaDetay = (dosya) => {
      if (dosya.dosya_no) {
        router.push(`/dosya/${dosya.dosya_no}`);
      }
    };

    const resetForm = () => {
      form.value = {
        yardim_yapan_ad_soyad: "",
        yardim_yapan_telefon: "",
        yardim_tutar: 0,
        dosyalar: [],
        dosya_tutarlari_list: [],
        manuel_kayitlar_list: [],
        aciklama: "",
      };
      searchQuery.value = "";
      searchResults.value = [];
      showManualEntry.value = false;
      manualEntry.value = {
        ad_soyad: "",
        tc_kimlik: "",
        telefon: "",
        adres: "",
        tutar: "",
        aciklama: "",
      };
    };

    const handleSubmit = async () => {
      try {
        loading.value = true;
        formErrors.value = {};

        // Form validasyonu
        if (!form.value.yardim_yapan_ad_soyad) {
          formErrors.value.yardim_yapan_ad_soyad =
            "Yardım yapan kişinin adı soyadı zorunludur";
        }
        if (!form.value.yardim_yapan_telefon) {
          formErrors.value.yardim_yapan_telefon =
            "Yardım yapan kişinin telefonu zorunludur";
        }
        if (form.value.dosyalar.length === 0) {
          formErrors.value.dosyalar =
            "En az bir dosya veya manuel kayıt seçilmelidir";
        }

        if (Object.keys(formErrors.value).length > 0) {
          return;
        }

        // Dosya tutarlarını ve manuel kayıtları ayır
        const dosyaTutarlari = form.value.dosyalar
          .filter((dosya) => !dosya.id.toString().startsWith("manual_"))
          .map((dosya) => ({
            dosya: dosya.id,
            tutar: Number(dosya.tutar) || 0,
          }));

        const manuelKayitlar = form.value.dosyalar
          .filter((dosya) => dosya.id.toString().startsWith("manual_"))
          .map((dosya) => ({
            ad_soyad: dosya.ad_soyad,
            tc_kimlik: dosya.tc_kimlik,
            telefon: dosya.telefon,
            adres: dosya.adres,
            tutar: Number(dosya.tutar) || 0,
            aciklama: dosya.aciklama || "",
          }));

        const submitData = {
          yardim_yapan_ad_soyad: form.value.yardim_yapan_ad_soyad,
          yardim_yapan_telefon: form.value.yardim_yapan_telefon,
          yardim_tutar: Number(form.value.yardim_tutar),
          tutar: form.value.tutar,
          aciklama: form.value.aciklama,
          dosya_tutarlari_list: dosyaTutarlari,
          manuel_kayitlar_list: manuelKayitlar,
        };

        const response = await apiService.createMaddiYardim(submitData);
        if (response.data) {
          emit("saved");
          emit("close");
          resetForm();
        }
      } catch (error) {
        console.error("Maddi yardım kaydedilirken hata:", error);
        if (error.response?.data) {
          formErrors.value = error.response.data;
        }
      } finally {
        loading.value = false;
      }
    };

    // Modal kapandığında formu sıfırla
    const handleClose = () => {
      resetForm();
      emit("close");
    };

    // Dışarı tıklandığında arama sonuçlarını kapat
    const handleClickOutside = (event) => {
      const searchContainer = document.querySelector(".relative");
      if (searchContainer && !searchContainer.contains(event.target)) {
        showResults.value = false;
      }
    };

    onMounted(() => {
      document.addEventListener("click", handleClickOutside);
    });

    onUnmounted(() => {
      document.removeEventListener("click", handleClickOutside);
    });

    return {
      form,
      searchQuery,
      searchResults,
      showResults,
      filteredSearchResults,
      showManualEntry,
      manualEntry,
      loading,
      formErrors,
      searchAileler,
      selectAile,
      removeAile,
      updateTotalTutar,
      openDosyaDetay,
      handleSubmit,
      getStatusClass,
      addManualEntry,
      handleClose,
      resetForm,
    };
  },
};
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
