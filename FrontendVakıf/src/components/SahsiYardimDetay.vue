<template>
  <v-dialog
    v-model="dialog"
    max-width="1200px"
    transition="dialog-bottom-transition"
  >
    <v-card class="rounded-lg">
      <v-card-title class="text-h5 bg-emerald-800 text-white pa-4">
        <v-icon start icon="mdi-eye" class="mr-2"></v-icon>
        Şahsi Yardım Detayı
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
              <div class="grid grid-cols-2 gap-6">
                <div>
                  <p class="text-sm text-gray-900">
                    <span class="font-medium">Yardım Tipi:</span>
                    {{
                      yardim.yardim_tipi === "individual" ? "Bireysel" : "Grup"
                    }}
                  </p>
                  <p class="text-sm text-gray-900 mt-1">
                    <span class="font-medium">Ad Soyad:</span>
                    {{ yardim.ad_soyad }}
                  </p>
                  <p class="text-sm text-gray-900 mt-1">
                    <span class="font-medium">Telefon:</span>
                    {{ yardim.telefon }}
                  </p>
                  <p
                    v-if="yardim.grup_uye_sayisi"
                    class="text-sm text-gray-900 mt-1"
                  >
                    <span class="font-medium">Grup Üye Sayısı:</span>
                    {{ yardim.grup_uye_sayisi }}
                  </p>
                </div>
              </div>
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
                    </tr>
                  </tbody>
                </v-table>
              </div>
              <p v-else class="text-sm text-gray-500">Yardımcı bulunmuyor</p>
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
                    </tr>
                  </tbody>
                </v-table>
              </div>
              <p v-else class="text-sm text-gray-500">Dosya bulunmuyor</p>
            </v-card-text>
          </v-card>

          <!-- Tarih Bilgileri -->
          <v-card class="mb-4 rounded-lg" elevation="1">
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-calendar" class="mr-2"></v-icon>
              Tarih Bilgileri
            </v-card-title>
            <v-card-text class="pa-4">
              <div class="grid grid-cols-2 gap-6">
                <div>
                  <p class="text-sm text-gray-900">
                    <span class="font-medium">Oluşturulma Tarihi:</span>
                    {{ formatDate(yardim.created_at) }}
                  </p>
                </div>
                <div>
                  <p class="text-sm text-gray-900">
                    <span class="font-medium">Son Güncelleme:</span>
                    {{ formatDate(yardim.updated_at) }}
                  </p>
                </div>
              </div>
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
          Kapat
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, watch } from "vue";

export default {
  name: "SahsiYardimDetay",
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
  emits: ["close"],
  setup(props, { emit }) {
    const dialog = ref(props.show);

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

    const formatDate = (date) => {
      if (!date) return "";
      return new Date(date).toLocaleDateString("tr-TR", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    };

    return {
      dialog,
      formatDate,
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
