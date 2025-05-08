<template>
  <v-dialog
    v-model="dialog"
    max-width="1200px"
    transition="dialog-bottom-transition"
  >
    <v-card class="rounded-lg">
      <v-card-title class="text-h5 bg-emerald-800 text-white pa-4">
        <v-icon start icon="mdi-pencil" class="mr-2"></v-icon>
        Maddi Yardım Düzenle
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form ref="form" v-model="valid">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="yardim.yardim_yapan_ad_soyad"
                label="Yardım Yapan Ad Soyad"
                :rules="[(v) => !!v || 'Ad Soyad zorunludur']"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-account"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="yardim.yardim_yapan_telefon"
                label="Yardım Yapan Telefon"
                :rules="[(v) => !!v || 'Telefon zorunludur']"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-phone"
                required
              ></v-text-field>
            </v-col>
          </v-row>

          <!-- Dosya Listesi -->
          <v-card class="mb-4 rounded-lg" elevation="1">
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-file-document" class="mr-2"></v-icon>
              Dosya Tutarları
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                variant="text"
                @click="showManualEntry = !showManualEntry"
                class="ml-2"
              >
                <v-icon start icon="mdi-plus"></v-icon>
                Manuel Kayıt Ekle
              </v-btn>
            </v-card-title>

            <!-- Manuel Kayıt Formu -->
            <v-expand-transition>
              <div v-if="showManualEntry" class="pa-4 bg-grey-lighten-4">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="manualEntry.ad_soyad"
                      label="Ad Soyad"
                      variant="outlined"
                      density="comfortable"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="manualEntry.tc_kimlik"
                      label="TC Kimlik No"
                      variant="outlined"
                      density="comfortable"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="manualEntry.telefon"
                      label="Telefon"
                      variant="outlined"
                      density="comfortable"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="manualEntry.adres"
                      label="Adres"
                      variant="outlined"
                      density="comfortable"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model.number="manualEntry.tutar"
                      label="Tutar"
                      type="number"
                      variant="outlined"
                      density="comfortable"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="manualEntry.aciklama"
                      label="Açıklama"
                      variant="outlined"
                      density="comfortable"
                    ></v-text-field>
                  </v-col>
                </v-row>
                <div class="d-flex justify-end">
                  <v-btn
                    color="primary"
                    @click="addManualEntry"
                    :disabled="
                      !manualEntry.ad_soyad ||
                      !manualEntry.tc_kimlik ||
                      !manualEntry.telefon ||
                      !manualEntry.adres
                    "
                  >
                    Ekle
                  </v-btn>
                </div>
              </div>
            </v-expand-transition>

            <!-- Dosya Arama -->
            <v-card-text class="pa-4">
              <v-text-field
                v-model="searchQuery"
                label="Dosya no, ad veya soyad ile arayın..."
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="comfortable"
                @input="searchAileler"
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
                      @click="selectAile(dosya)"
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
            </v-card-text>

            <v-card-text class="pa-0">
              <v-table density="comfortable" hover class="modern-table">
                <thead>
                  <tr>
                    <th class="text-left">Dosya No</th>
                    <th class="text-left">Ad Soyad</th>
                    <th class="text-left">Telefon</th>
                    <th class="text-left">Adres</th>
                    <th class="text-right">Tutar</th>
                    <th class="text-center">İşlemler</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="dosya in dosyalar"
                    :key="dosya.id"
                    class="hover-row"
                  >
                    <td>{{ dosya.dosya_no }}</td>
                    <td>{{ dosya.ad }} {{ dosya.soyad }}</td>
                    <td>{{ dosya.telefon }}</td>
                    <td>{{ dosya.mahalle }} {{ dosya.cadde_sokak }}</td>
                    <td class="text-right">
                      <v-text-field
                        v-model.number="dosyaTutarlari[dosya.id]"
                        type="number"
                        density="compact"
                        variant="outlined"
                        hide-details
                        class="tutar-input"
                        @input="updateTotalTutar"
                      ></v-text-field>
                    </td>
                    <td class="text-center">
                      <v-btn
                        color="primary"
                        size="small"
                        variant="text"
                        @click="openDosyaDetay(dosya)"
                      >
                        <v-icon icon="mdi-eye"></v-icon>
                        Detay
                      </v-btn>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </v-card-text>
          </v-card>

          <!-- Manuel Kayıtlar -->
          <v-card class="mb-4 rounded-lg" elevation="1">
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-account-multiple" class="mr-2"></v-icon>
              Manuel Kayıtlar
            </v-card-title>
            <v-card-text class="pa-0">
              <v-table density="comfortable" hover class="modern-table">
                <thead>
                  <tr>
                    <th class="text-left">Ad Soyad</th>
                    <th class="text-left">TC Kimlik</th>
                    <th class="text-left">Telefon</th>
                    <th class="text-left">Adres</th>
                    <th class="text-right">Tutar</th>
                    <th class="text-left">Açıklama</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(kayit, index) in manuelKayitlar"
                    :key="index"
                    class="hover-row"
                  >
                    <td>{{ kayit.ad_soyad }}</td>
                    <td>{{ kayit.tc_kimlik }}</td>
                    <td>{{ kayit.telefon }}</td>
                    <td>{{ kayit.adres }}</td>
                    <td class="text-right">
                      <v-text-field
                        v-model.number="kayit.tutar"
                        type="number"
                        density="compact"
                        variant="outlined"
                        hide-details
                        class="tutar-input"
                        @input="updateTotalTutar"
                      ></v-text-field>
                    </td>
                    <td>{{ kayit.aciklama }}</td>
                  </tr>
                </tbody>
              </v-table>
            </v-card-text>
          </v-card>

          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="yardim.yardim_tutar"
                label="Yardım Tutarı"
                type="number"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-currency-try"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="yardim.tutar"
                label="Toplam Tutar"
                type="number"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-currency-try"
                readonly
                :model-value="toplamTutar"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="yardim.aciklama"
                label="Açıklama"
                rows="3"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-text"
              ></v-textarea>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" class="text-right">
              <v-card class="pa-4 bg-grey-lighten-4 rounded-lg" elevation="0">
                <div class="text-h6 font-weight-bold">
                  Toplam Tutar: {{ toplamTutar.toLocaleString("tr-TR") }} TL
                </div>
              </v-card>
            </v-col>
          </v-row>
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
          :loading="loading"
          :disabled="!valid || loading"
          @click="handleSubmit"
        >
          <v-icon start icon="mdi-content-save"></v-icon>
          {{ loading ? "Kaydediliyor..." : "Kaydet" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, onMounted, watch, onUnmounted, toRaw, nextTick } from "vue";
import apiService from "../api";
import { useRouter } from "vue-router";

export default {
  name: "MaddiYardimDuzenle",
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
  emits: ["close", "saved", "refresh"],
  setup(props, { emit }) {
    const dialog = ref(props.show);
    const valid = ref(false);
    const loading = ref(false);
    const yardim = ref({
      yardim_yapan_ad_soyad: "",
      yardim_yapan_telefon: "",
      yardim_tutar: 0,
      tutar: 0,
      aciklama: "",
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

    const dosyalar = ref([]);
    const dosyaTutarlari = ref({});
    const manuelKayitlar = ref([]);
    const toplamTutar = ref(0);

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

      manuelKayitlar.value.push(newEntry);
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
            !dosyalar.value.some((selected) => selected.id === dosya.id)
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
      if (!dosyalar.value.some((selected) => selected.id === dosya.id)) {
        dosyalar.value.push({
          ...dosya,
          tutar: 0,
        });
        dosyaTutarlari.value[dosya.id] = 0;
        updateTotalTutar();
      }
      searchQuery.value = "";
      showResults.value = false;
    };

    // Aile kaldırma fonksiyonu
    const removeAile = (dosya) => {
      const index = dosyalar.value.findIndex((a) => a.id === dosya.id);
      if (index !== -1) {
        dosyalar.value.splice(index, 1);
        delete dosyaTutarlari.value[dosya.id];
        updateTotalTutar();
      }
    };

    // Manuel kayıt kaldırma fonksiyonu
    const removeManuelKayit = (kayit) => {
      const index = manuelKayitlar.value.findIndex((k) => k.id === kayit.id);
      if (index !== -1) {
        manuelKayitlar.value.splice(index, 1);
        updateTotalTutar();
      }
    };

    // Toplam tutarı güncelle
    const updateTotalTutar = () => {
      let total = 0;

      // Dosya tutarlarını topla
      Object.values(dosyaTutarlari.value).forEach((tutar) => {
        total += Number(tutar);
      });

      // Manuel kayıt tutarlarını topla
      manuelKayitlar.value.forEach((kayit) => {
        total += Number(kayit.tutar);
      });

      toplamTutar.value = total;
      yardim.value.tutar = total;
    };

    // Kaydet butonuna tıklandığında
    const handleSubmit = async () => {
      try {
        loading.value = true;

        // Dosya tutarlarını hazırla
        const dosyaTutarlariList = Object.entries(dosyaTutarlari.value).map(
          ([dosyaId, tutar]) => ({
            dosya: Number(dosyaId),
            tutar: Number(tutar),
          })
        );

        // Manuel kayıtları hazırla
        const manuelKayitlarList = manuelKayitlar.value.map((kayit) => ({
          ad_soyad: kayit.ad_soyad,
          tc_kimlik: kayit.tc_kimlik,
          telefon: kayit.telefon,
          adres: kayit.adres,
          tutar: Number(kayit.tutar),
          aciklama: kayit.aciklama,
        }));

        // Form verilerini hazırla
        const formData = {
          yardim_yapan_ad_soyad: yardim.value.yardim_yapan_ad_soyad,
          yardim_yapan_telefon: yardim.value.yardim_yapan_telefon,
          yardim_tutar: Number(yardim.value.yardim_tutar),
          tutar: toplamTutar.value,
          aciklama: yardim.value.aciklama || "",
          dosya_tutarlari_list: dosyaTutarlariList,
          manuel_kayitlar_list: manuelKayitlarList,
        };

        // API'ye gönder
        const response = await apiService.updateMaddiYardim(
          yardim.value.id,
          formData
        );

        // Başarılı mesajı göster
        alert("Maddi yardım başarıyla güncellendi");

        // Modalı kapat ve güncel veriyi gönder
        dialog.value = false;
        emit("saved", response.data);
      } catch (error) {
        console.error("Güncelleme hatası:", error);
        alert("Güncelleme sırasında bir hata oluştu");
      } finally {
        loading.value = false;
      }
    };

    // Yardım verilerini izle
    watch(
      () => props.yardim,
      (newYardim) => {
        if (newYardim) {
          yardim.value = {
            ...newYardim,
            yardim_tutar: Number(newYardim.yardim_tutar) || 0,
          };

          // Dosya bilgilerini işle
          if (
            newYardim.dosya_bilgileri &&
            Array.isArray(newYardim.dosya_bilgileri)
          ) {
            dosyalar.value = newYardim.dosya_bilgileri.map((item) => ({
              id: item.dosya,
              dosya_no: item.dosya_bilgisi.dosya_no,
              ad: item.dosya_bilgisi.ad,
              soyad: item.dosya_bilgisi.soyad,
              telefon: item.dosya_bilgisi.telefon,
              mahalle: item.dosya_bilgisi.mahalle,
              cadde_sokak: item.dosya_bilgisi.cadde_sokak,
              durum: item.dosya_bilgisi.durum,
            }));

            // Dosya tutarlarını ayarla
            dosyaTutarlari.value = {};
            newYardim.dosya_bilgileri.forEach((item) => {
              if (item.dosya) {
                dosyaTutarlari.value[item.dosya] = Number(item.tutar);
              }
            });
          } else {
            dosyalar.value = [];
            dosyaTutarlari.value = {};
          }

          // Manuel kayıtları işle
          if (
            newYardim.manuel_kayitlar &&
            Array.isArray(newYardim.manuel_kayitlar)
          ) {
            manuelKayitlar.value = newYardim.manuel_kayitlar.map((kayit) => ({
              id: `manual_${Date.now()}_${Math.random()}`,
              ad_soyad: kayit.ad_soyad,
              tc_kimlik: kayit.tc_kimlik,
              telefon: kayit.telefon,
              adres: kayit.adres,
              tutar: Number(kayit.tutar),
              aciklama: kayit.aciklama || "",
              durum: "manuel",
            }));
          } else {
            manuelKayitlar.value = [];
          }

          // Toplam tutarı güncelle
          updateTotalTutar();
        }
      },
      { immediate: true, deep: true }
    );

    // Modal açıldığında verileri yükle
    watch(
      () => props.show,
      (newVal) => {
        if (newVal && props.yardim) {
          yardim.value = { ...props.yardim };

          // Dosya bilgilerini işle
          if (
            props.yardim.dosya_bilgileri &&
            Array.isArray(props.yardim.dosya_bilgileri)
          ) {
            dosyalar.value = props.yardim.dosya_bilgileri.map((item) => ({
              id: item.dosya,
              dosya_no: item.dosya_bilgisi.dosya_no,
              ad: item.dosya_bilgisi.ad,
              soyad: item.dosya_bilgisi.soyad,
              telefon: item.dosya_bilgisi.telefon,
              mahalle: item.dosya_bilgisi.mahalle,
              cadde_sokak: item.dosya_bilgisi.cadde_sokak,
              durum: item.dosya_bilgisi.durum,
            }));

            // Dosya tutarlarını ayarla
            dosyaTutarlari.value = {};
            props.yardim.dosya_bilgileri.forEach((item) => {
              if (item.dosya) {
                dosyaTutarlari.value[item.dosya] = Number(item.tutar);
              }
            });
          }

          // Manuel kayıtları işle
          if (
            props.yardim.manuel_kayitlar &&
            Array.isArray(props.yardim.manuel_kayitlar)
          ) {
            manuelKayitlar.value = props.yardim.manuel_kayitlar.map(
              (kayit) => ({
                id: `manual_${Date.now()}_${Math.random()}`,
                ad_soyad: kayit.ad_soyad,
                tc_kimlik: kayit.tc_kimlik,
                telefon: kayit.telefon,
                adres: kayit.adres,
                tutar: Number(kayit.tutar),
                aciklama: kayit.aciklama || "",
                durum: "manuel",
              })
            );
          }

          // Toplam tutarı güncelle
          updateTotalTutar();
        }
      },
      { immediate: true }
    );

    // Modal kapatıldığında form verilerini sıfırla
    watch(dialog, (newVal) => {
      if (!newVal) {
        emit("close");
        // Form verilerini sıfırla
        yardim.value = {
          yardim_yapan_ad_soyad: "",
          yardim_yapan_telefon: "",
          yardim_tutar: 0,
          tutar: 0,
          aciklama: "",
        };
        dosyalar.value = [];
        dosyaTutarlari.value = {};
        manuelKayitlar.value = [];
        toplamTutar.value = 0;
        searchQuery.value = "";
        searchResults.value = [];
        showResults.value = false;
        showManualEntry.value = false;
        manualEntry.value = {
          ad_soyad: "",
          tc_kimlik: "",
          telefon: "",
          adres: "",
          tutar: 0,
          aciklama: "",
        };
      }
    });

    // Dosya detayını göster
    const openDosyaDetay = (dosya) => {
      router.push(`/dosya/${dosya.dosya_no}`);
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
        default:
          return "bg-gray-100 text-gray-800";
      }
    };

    return {
      dialog,
      valid,
      loading,
      yardim,
      dosyalar,
      dosyaTutarlari,
      manuelKayitlar,
      toplamTutar,
      searchQuery,
      searchResults,
      showResults,
      filteredSearchResults,
      showManualEntry,
      manualEntry,
      updateTotalTutar,
      handleSubmit,
      openDosyaDetay,
      getStatusClass,
      searchAileler,
      selectAile,
      removeAile,
      addManualEntry,
      removeManuelKayit,
    };
  },
};
</script>

<style scoped>
.hover-row:hover {
  background-color: transparent !important;
}

.tutar-input {
  max-width: 150px;
  margin: 0 auto;
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

/* Hover efektini tamamen kaldır */
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
