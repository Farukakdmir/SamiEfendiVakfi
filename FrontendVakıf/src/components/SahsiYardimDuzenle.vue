<template>
  <v-dialog
    v-model="dialog"
    max-width="1200px"
    transition="dialog-bottom-transition"
  >
    <v-card class="rounded-lg">
      <v-card-title class="text-h5 bg-emerald-800 text-white pa-4">
        <v-icon start icon="mdi-pencil" class="mr-2"></v-icon>
        Şahsi Yardım Düzenle
      </v-card-title>

      <v-card-text class="pa-6">
        <div v-if="yardim" class="space-y-6">
          <!-- Yardım Bilgileri -->
          <v-card class="mb-4 rounded-lg" elevation="1">
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-account" class="mr-2"></v-icon>
              Yardım Bilgileri
            </v-card-title>
            <v-card-text class="pa-4">
              <v-form ref="form" v-model="isFormValid">
                <div class="grid grid-cols-2 gap-6">
                  <v-select
                    v-model="yardim.yardim_tipi"
                    :items="yardimTipleri"
                    label="Yardım Tipi"
                    variant="outlined"
                    density="comfortable"
                    :rules="[(v) => !!v || 'Yardım tipi seçiniz']"
                  ></v-select>

                  <v-text-field
                    v-model="yardim.ad_soyad"
                    label="Ad Soyad"
                    variant="outlined"
                    density="comfortable"
                    :rules="[(v) => !!v || 'Ad soyad giriniz']"
                  ></v-text-field>

                  <v-text-field
                    v-model="yardim.telefon"
                    label="Telefon"
                    variant="outlined"
                    density="comfortable"
                    :rules="[(v) => !!v || 'Telefon giriniz']"
                  ></v-text-field>

                  <v-text-field
                    v-if="yardim.yardim_tipi === 'group'"
                    v-model="yardim.grup_uye_sayisi"
                    label="Grup Üye Sayısı"
                    type="number"
                    variant="outlined"
                    density="comfortable"
                    :rules="[(v) => !!v || 'Grup üye sayısı giriniz']"
                  ></v-text-field>
                </div>
              </v-form>
            </v-card-text>
          </v-card>

          <!-- Yardımcılar -->
          <v-card class="mb-4 rounded-lg" elevation="1">
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-account-multiple" class="mr-2"></v-icon>
              Yardımcılar
            </v-card-title>
            <v-card-text class="pa-4">
              <div v-if="yardim.yardimcilar && yardim.yardimcilar.length > 0">
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
                      v-for="yardimci in yardim.yardimcilar"
                      :key="yardimci.id"
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
                          @click="yardimciSil(yardimci.id)"
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
              Yardım Edilen Dosyalar
            </v-card-title>
            <v-card-text class="pa-4">
              <div v-if="yardim.dosyalar && yardim.dosyalar.length > 0">
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
                      v-for="dosya in yardim.dosyalar"
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
                          @click="dosyaSil(dosya.id)"
                        ></v-btn>
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </div>
              <p v-else class="text-sm text-gray-500">Dosya bulunmuyor</p>

              <!-- Yeni Dosya Ekleme Formu -->
              <v-form ref="dosyaForm" v-model="isDosyaFormValid" class="mt-4">
                <div class="grid grid-cols-2 gap-4">
                  <v-text-field
                    v-model="yeniDosya.dosya_no"
                    label="Dosya No"
                    variant="outlined"
                    density="comfortable"
                    :rules="[(v) => !!v || 'Dosya no giriniz']"
                  ></v-text-field>

                  <v-text-field
                    v-model="yeniDosya.ad"
                    label="Ad"
                    variant="outlined"
                    density="comfortable"
                    :rules="[(v) => !!v || 'Ad giriniz']"
                  ></v-text-field>

                  <v-text-field
                    v-model="yeniDosya.soyad"
                    label="Soyad"
                    variant="outlined"
                    density="comfortable"
                    :rules="[(v) => !!v || 'Soyad giriniz']"
                  ></v-text-field>

                  <v-text-field
                    v-model="yeniDosya.telefon"
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
                    @click="dosyaEkle"
                    :disabled="!isDosyaFormValid"
                  >
                    <v-icon start icon="mdi-plus"></v-icon>
                    Dosya Ekle
                  </v-btn>
                </div>
              </v-form>
            </v-card-text>
          </v-card>
        </div>
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
          @click="kaydet"
          :disabled="!isFormValid"
        >
          <v-icon start icon="mdi-content-save"></v-icon>
          Kaydet
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, watch } from "vue";

export default {
  name: "SahsiYardimDuzenle",
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
  emits: ["close", "update"],
  setup(props, { emit }) {
    const dialog = ref(props.show);
    const form = ref(null);
    const yardimciForm = ref(null);
    const dosyaForm = ref(null);
    const isFormValid = ref(false);
    const isYardimciFormValid = ref(false);
    const isDosyaFormValid = ref(false);

    const yardimTipleri = [
      { title: "Bireysel", value: "individual" },
      { title: "Grup", value: "group" },
    ];

    const yeniYardimci = ref({
      ad_soyad: "",
      telefon: "",
    });

    const yeniDosya = ref({
      dosya_no: "",
      ad: "",
      soyad: "",
      telefon: "",
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
      }
    });

    const yardimciEkle = () => {
      if (!isYardimciFormValid.value) return;

      if (!props.yardim.yardimcilar) {
        props.yardim.yardimcilar = [];
      }

      props.yardim.yardimcilar.push({
        id: Date.now(),
        ...yeniYardimci.value,
      });

      yeniYardimci.value = {
        ad_soyad: "",
        telefon: "",
      };

      yardimciForm.value.reset();
    };

    const yardimciSil = (id) => {
      props.yardim.yardimcilar = props.yardim.yardimcilar.filter(
        (y) => y.id !== id
      );
    };

    const dosyaEkle = () => {
      if (!isDosyaFormValid.value) return;

      if (!props.yardim.dosyalar) {
        props.yardim.dosyalar = [];
      }

      props.yardim.dosyalar.push({
        id: Date.now(),
        ...yeniDosya.value,
      });

      yeniDosya.value = {
        dosya_no: "",
        ad: "",
        soyad: "",
        telefon: "",
      };

      dosyaForm.value.reset();
    };

    const dosyaSil = (id) => {
      props.yardim.dosyalar = props.yardim.dosyalar.filter((d) => d.id !== id);
    };

    const kaydet = async () => {
      const { valid } = await form.value.validate();
      if (!valid) return;

      emit("update", props.yardim);
      dialog.value = false;
    };

    return {
      dialog,
      form,
      yardimciForm,
      dosyaForm,
      isFormValid,
      isYardimciFormValid,
      isDosyaFormValid,
      yardimTipleri,
      yeniYardimci,
      yeniDosya,
      yardimciEkle,
      yardimciSil,
      dosyaEkle,
      dosyaSil,
      kaydet,
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
