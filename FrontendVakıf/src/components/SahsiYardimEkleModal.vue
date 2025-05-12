<template>
  <v-dialog
    v-model="dialog"
    max-width="1200px"
    transition="dialog-bottom-transition"
  >
    <v-card class="rounded-lg">
      <v-card-title class="text-h5 bg-emerald-800 text-white pa-4">
        <v-icon start icon="mdi-plus" class="mr-2"></v-icon>
        Yeni Şahsi Yardım Kaydı
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form ref="form" v-model="isFormValid">
          <!-- Yardım Bilgileri -->
          <v-card class="mb-4 rounded-lg" elevation="1">
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-account" class="mr-2"></v-icon>
              Yardım Bilgileri
            </v-card-title>
            <v-card-text class="pa-4">
              <div class="grid grid-cols-2 gap-6">
                <v-select
                  v-model="formData.yardim_tipi"
                  :items="yardimTipleri"
                  label="Yardım Tipi"
                  variant="outlined"
                  density="comfortable"
                  :rules="[(v) => !!v || 'Yardım tipi seçiniz']"
                ></v-select>

                <v-text-field
                  v-model="formData.ad_soyad"
                  label="Ad Soyad"
                  variant="outlined"
                  density="comfortable"
                  :rules="[(v) => !!v || 'Ad soyad giriniz']"
                ></v-text-field>

                <v-text-field
                  v-model="formData.telefon"
                  label="Telefon"
                  variant="outlined"
                  density="comfortable"
                  :rules="[(v) => !!v || 'Telefon giriniz']"
                ></v-text-field>

                <v-text-field
                  v-if="formData.yardim_tipi === 'group'"
                  v-model="formData.grup_uye_sayisi"
                  label="Grup Üye Sayısı"
                  type="number"
                  variant="outlined"
                  density="comfortable"
                  :rules="[(v) => !!v || 'Grup üye sayısı giriniz']"
                ></v-text-field>
              </div>
            </v-card-text>
          </v-card>

          <!-- Yardımcılar -->
          <v-card
            v-if="formData.yardim_tipi === 'group'"
            class="mb-4 rounded-lg"
            elevation="1"
          >
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-account-multiple" class="mr-2"></v-icon>
              Yardımcılar
            </v-card-title>
            <v-card-text class="pa-4">
              <div
                v-if="formData.yardimcilar && formData.yardimcilar.length > 0"
              >
                <v-table density="comfortable" hover class="modern-table">
                  <thead>
                    <tr>
                      <th class="text-left">Ad Soyad</th>
                      <th class="text-left">Telefon</th>
                      <th class="text-right">İşlemler</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(yardimci, index) in formData.yardimcilar"
                      :key="index"
                      class="hover-row"
                    >
                      <td>{{ yardimci.ad_soyad }}</td>
                      <td>{{ yardimci.telefon }}</td>
                      <td class="text-right">
                        <v-btn
                          icon="mdi-delete"
                          variant="text"
                          color="error"
                          size="small"
                          @click="yardimciSil(index)"
                        ></v-btn>
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </div>
              <p v-else class="text-sm text-gray-500">Yardımcı bulunmuyor</p>

              <!-- Yeni Yardımcı Ekleme Formu -->
              <v-form
                ref="yardimciForm"
                v-model="isYardimciFormValid"
                class="mt-4"
              >
                <div class="grid grid-cols-2 gap-4">
                  <v-text-field
                    v-model="yeniYardimci.ad_soyad"
                    label="Ad Soyad"
                    variant="outlined"
                    density="comfortable"
                    :rules="[(v) => !!v || 'Ad soyad giriniz']"
                  ></v-text-field>

                  <v-text-field
                    v-model="yeniYardimci.telefon"
                    label="Telefon"
                    variant="outlined"
                    density="comfortable"
                    :rules="[(v) => !!v || 'Telefon giriniz']"
                  ></v-text-field>
                </div>

                <div class="flex justify-end mt-4">
                  <v-btn
                    color="primary"
                    variant="outlined"
                    @click="yardimciEkle"
                    :disabled="!isYardimciFormValid"
                  >
                    <v-icon start icon="mdi-plus"></v-icon>
                    Yardımcı Ekle
                  </v-btn>
                </div>
              </v-form>
            </v-card-text>
          </v-card>

          <!-- Dosya Bilgileri -->
          <v-card class="mb-4 rounded-lg" elevation="1">
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-file-document" class="mr-2"></v-icon>
              Yardım Edilecek Dosyalar
            </v-card-title>
            <v-card-text class="pa-4">
              <v-text-field
                v-model="searchQuery"
                label="Dosya no, ad veya soyad ile arayın..."
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="comfortable"
                @input="searchDosyalar"
                class="mb-4"
              ></v-text-field>

              <!-- Arama Sonuçları -->
              <v-expand-transition>
                <div
                  v-if="searchResults.length > 0 && showResults"
                  class="mb-4"
                >
                  <v-list>
                    <v-list-item
                      v-for="dosya in filteredSearchResults"
                      :key="dosya.id"
                      @click="selectDosya(dosya)"
                      class="cursor-pointer"
                    >
                      <v-list-item-title>
                        {{ dosya.ad }} {{ dosya.soyad }}
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        Dosya No: {{ dosya.dosya_no }} - Tel:
                        {{ dosya.telefon }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </div>
              </v-expand-transition>

              <!-- Seçili Dosyalar -->
              <div v-if="selectedDosyalar.length > 0">
                <v-table density="comfortable" hover class="modern-table">
                  <thead>
                    <tr>
                      <th class="text-left">Dosya No</th>
                      <th class="text-left">Ad Soyad</th>
                      <th class="text-left">Telefon</th>
                      <th class="text-right">İşlemler</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="dosya in selectedDosyalar"
                      :key="dosya.id"
                      class="hover-row"
                    >
                      <td>{{ dosya.dosya_no }}</td>
                      <td>{{ dosya.ad }} {{ dosya.soyad }}</td>
                      <td>{{ dosya.telefon }}</td>
                      <td class="text-right">
                        <v-btn
                          icon="mdi-delete"
                          variant="text"
                          color="error"
                          size="small"
                          @click="removeDosya(dosya)"
                        ></v-btn>
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </div>
              <p v-else class="text-sm text-gray-500">Dosya seçilmedi</p>
            </v-card-text>
          </v-card>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4 bg-grey-lighten-4">
        <v-spacer></v-spacer>
        <v-btn
          color="error"
          variant="outlined"
          @click="dialog = false"
          class="mr-2"
        >
          <v-icon start icon="mdi-close"></v-icon>
          İptal
        </v-btn>
        <v-btn
          color="primary"
          variant="outlined"
          @click="saveRecord"
          :disabled="!isFormValid || loading"
          :loading="loading"
        >
          <v-icon start icon="mdi-content-save"></v-icon>
          {{ loading ? "Kaydediliyor..." : "Kaydet" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, watch, computed } from "vue";
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
    const dialog = ref(props.show);
    const form = ref(null);
    const yardimciForm = ref(null);
    const isFormValid = ref(false);
    const isYardimciFormValid = ref(false);
    const loading = ref(false);

    const yardimTipleri = [
      { title: "Bireysel", value: "individual" },
      { title: "Grup", value: "group" },
    ];

    const formData = ref({
      yardim_tipi: "individual",
      ad_soyad: "",
      telefon: "",
      grup_uye_sayisi: null,
      yardimcilar: [],
      dosyalar: [],
    });

    const yeniYardimci = ref({
      ad_soyad: "",
      telefon: "",
    });

    const searchQuery = ref("");
    const searchResults = ref([]);
    const showResults = ref(false);
    const selectedDosyalar = ref([]);

    const filteredSearchResults = computed(() => {
      return searchResults.value.filter(
        (dosya) =>
          !selectedDosyalar.value.some((selected) => selected.id === dosya.id)
      );
    });

    watch(
      () => props.show,
      (newVal) => {
        dialog.value = newVal;
      }
    );

    watch(dialog, (newVal) => {
      if (!newVal) {
        emit("close");
        resetForm();
      }
    });

    const yardimciEkle = () => {
      if (!isYardimciFormValid.value) return;

      formData.value.yardimcilar.push({
        ...yeniYardimci.value,
      });

      yeniYardimci.value = {
        ad_soyad: "",
        telefon: "",
      };

      yardimciForm.value.reset();
    };

    const yardimciSil = (index) => {
      formData.value.yardimcilar.splice(index, 1);
    };

    const searchDosyalar = async () => {
      if (searchQuery.value.length < 2) {
        searchResults.value = [];
        showResults.value = false;
        return;
      }

      try {
        const response = await apiService.searchDosyalar(searchQuery.value);
        searchResults.value = response.data.results || response.data;
        showResults.value = true;
      } catch (error) {
        console.error("Arama yapılırken hata:", error);
        searchResults.value = [];
        showResults.value = false;
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
      yeniYardimci.value = {
        ad_soyad: "",
        telefon: "",
      };
    };

    const saveRecord = async () => {
      const { valid } = await form.value.validate();
      if (!valid) return;

      if (formData.value.dosyalar.length === 0) {
        alert("En az bir dosya seçmelisiniz");
        return;
      }

      try {
        loading.value = true;
        const data = {
          yardim_tipi: formData.value.yardim_tipi,
          ad_soyad: formData.value.ad_soyad.trim(),
          telefon: formData.value.telefon.trim(),
          grup_uye_sayisi:
            formData.value.yardim_tipi === "group"
              ? parseInt(formData.value.grup_uye_sayisi)
              : null,
          yardimcilar:
            formData.value.yardim_tipi === "group"
              ? formData.value.yardimcilar.map((helper) => ({
                  ad_soyad: helper.ad_soyad.trim(),
                  telefon: helper.telefon.trim(),
                }))
              : [],
          dosyalar: formData.value.dosyalar,
        };

        const response = await apiService.createSahsiYardim(data);
        if (response && response.data) {
          emit("saved");
          dialog.value = false;
          resetForm();
        }
      } catch (error) {
        console.error("Form gönderilirken hata:", error);
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
      } finally {
        loading.value = false;
      }
    };

    return {
      dialog,
      form,
      yardimciForm,
      isFormValid,
      isYardimciFormValid,
      loading,
      yardimTipleri,
      formData,
      yeniYardimci,
      searchQuery,
      searchResults,
      showResults,
      selectedDosyalar,
      filteredSearchResults,
      yardimciEkle,
      yardimciSil,
      searchDosyalar,
      selectDosya,
      removeDosya,
      saveRecord,
      resetForm,
    };
  },
};
</script>

<style scoped>
.hover-row:hover {
  background-color: transparent !important;
}

.v-card-title {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.modern-table {
  border-radius: 8px;
  overflow: hidden;
}

.modern-table .v-table__wrapper > table {
  border-collapse: separate;
  border-spacing: 0;
}

.modern-table .v-table__wrapper > table > thead > tr > th {
  background-color: transparent !important;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.6);
}

.modern-table .v-table__wrapper > table > thead > tr > th,
.modern-table .v-table__wrapper > table > tbody > tr > td {
  border: none !important;
}

.modern-table .v-table__wrapper > table > thead > tr > th {
  background-color: transparent !important;
}

.modern-table .v-table__wrapper > table > tbody > tr > td {
  background-color: transparent !important;
}

.modern-table .v-table__wrapper > table > tbody > tr:hover > td,
.modern-table .v-table__wrapper > table > tbody > tr:hover {
  background-color: transparent !important;
}

.v-table--hover
  > .v-table__wrapper
  > table
  > tbody
  > tr:hover:not(.v-data-table__expanded__content):not(
    .v-data-table__empty-wrapper
  ) {
  background-color: transparent !important;
}
</style>
