<template>
  <v-dialog
    v-model="dialog"
    max-width="1200px"
    transition="dialog-bottom-transition"
  >
    <v-card class="rounded-lg">
      <v-card-title class="text-h5 bg-emerald-800 text-white pa-4">
        <v-icon start icon="mdi-eye" class="mr-2"></v-icon>
        Maddi Yardım Detayı
      </v-card-title>

      <v-card-text class="pa-6">
        <div v-if="yardim" class="space-y-6">
          <!-- Yardım Bilgileri -->
          <v-card class="mb-4 rounded-lg" elevation="1">
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-account" class="mr-2"></v-icon>
              Yardım Yapan Bilgileri
            </v-card-title>
            <v-card-text class="pa-4">
              <p class="text-sm text-gray-900">
                <span class="font-medium">Ad Soyad:</span>
                {{ yardim.yardim_yapan_ad_soyad }}
              </p>
              <p class="text-sm text-gray-900 mt-1">
                <span class="font-medium">Telefon:</span>
                {{ yardim.yardim_yapan_telefon }}
              </p>
            </v-card-text>
          </v-card>

          <!-- Yardım Detayları -->
          <v-card class="mb-4 rounded-lg" elevation="1">
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-information" class="mr-2"></v-icon>
              Yardım Detayları
            </v-card-title>
            <v-card-text class="pa-4">
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
            </v-card-text>
          </v-card>

          <!-- Dosya Kayıtları -->
          <v-card class="mb-4 rounded-lg" elevation="1">
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-file-document" class="mr-2"></v-icon>
              Dosya Kayıtları
            </v-card-title>
            <v-card-text class="pa-4">
              <div
                v-if="
                  yardim.dosya_bilgileri && yardim.dosya_bilgileri.length > 0
                "
              >
                <v-table density="comfortable" hover class="modern-table">
                  <thead>
                    <tr>
                      <th class="text-left">Dosya No</th>
                      <th class="text-left">Ad Soyad</th>
                      <th class="text-left">Telefon</th>
                      <th class="text-left">Adres</th>
                      <th class="text-right">Tutar</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="dosya in yardim.dosya_bilgileri"
                      :key="dosya.id"
                      class="hover-row"
                    >
                      <td>{{ dosya.dosya_bilgisi.dosya_no }}</td>
                      <td>
                        {{ dosya.dosya_bilgisi.ad }}
                        {{ dosya.dosya_bilgisi.soyad }}
                      </td>
                      <td>{{ dosya.dosya_bilgisi.telefon }}</td>
                      <td>
                        {{ dosya.dosya_bilgisi.mahalle }}
                        {{ dosya.dosya_bilgisi.cadde_sokak }}
                      </td>
                      <td class="text-right">
                        {{ formatTutar(dosya.tutar) }} TL
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </div>
              <p v-else class="text-sm text-gray-500">
                Dosya kaydı bulunmamaktadır.
              </p>
            </v-card-text>
          </v-card>

          <!-- Manuel Kayıtlar -->
          <v-card class="mb-4 rounded-lg" elevation="1">
            <v-card-title class="bg-grey-lighten-4">
              <v-icon start icon="mdi-account-multiple" class="mr-2"></v-icon>
              Manuel Kayıtlar
            </v-card-title>
            <v-card-text class="pa-4">
              <div
                v-if="
                  yardim.manuel_kayitlar && yardim.manuel_kayitlar.length > 0
                "
              >
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
                      v-for="kayit in yardim.manuel_kayitlar"
                      :key="kayit.id"
                      class="hover-row"
                    >
                      <td>{{ kayit.ad_soyad }}</td>
                      <td>{{ kayit.tc_kimlik }}</td>
                      <td>{{ kayit.telefon }}</td>
                      <td>{{ kayit.adres }}</td>
                      <td class="text-right">
                        {{ formatTutar(kayit.tutar) }} TL
                      </td>
                      <td>{{ kayit.aciklama || "-" }}</td>
                    </tr>
                  </tbody>
                </v-table>
              </div>
              <p v-else class="text-sm text-gray-500">
                Manuel kayıt bulunmamaktadır.
              </p>
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
        <v-btn
          color="success"
          variant="elevated"
          @click="exportToExcel"
          class="excel-btn"
          elevation="2"
        >
          <v-icon start icon="mdi-file-excel" class="mr-2"></v-icon>
          Excel'e Aktar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, watch } from "vue";
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
      return new Date(date).toLocaleDateString("tr-TR");
    };

    const formatTutar = (tutar) => {
      return Number(tutar).toLocaleString("tr-TR");
    };

    const exportToExcel = () => {
      try {
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
          props.yardim.dosya_bilgileri &&
          props.yardim.dosya_bilgileri.length > 0
        ) {
          props.yardim.dosya_bilgileri.forEach((dosya) => {
            data.push([
              `${dosya.dosya_bilgisi.ad} ${dosya.dosya_bilgisi.soyad}`,
              dosya.dosya_bilgisi.tc_kimlik || "-",
              dosya.dosya_bilgisi.telefon || "-",
              `${dosya.dosya_bilgisi.mahalle || ""} ${
                dosya.dosya_bilgisi.cadde_sokak || ""
              }`,
              formatTutar(dosya.tutar),
              dosya.aciklama || "-",
              "Dosya Kaydı",
            ]);
          });
        }

        // Manuel kayıtları ekle
        if (
          props.yardim.manuel_kayitlar &&
          props.yardim.manuel_kayitlar.length > 0
        ) {
          props.yardim.manuel_kayitlar.forEach((kayit) => {
            data.push([
              kayit.ad_soyad,
              kayit.tc_kimlik || "-",
              kayit.telefon || "-",
              kayit.adres || "-",
              formatTutar(kayit.tutar),
              kayit.aciklama || "-",
              "Manuel Kayıt",
            ]);
          });
        }

        const ws = XLSXUtils.aoa_to_sheet(data);
        const wb = XLSXUtils.book_new();
        XLSXUtils.book_append_sheet(wb, ws, "Maddi Yardım Detayı");

        const fileName = `Maddi_Yardim_${
          props.yardim.yardim_yapan_ad_soyad
        }_${formatDate(props.yardim.created_at)}.xlsx`;
        writeFile(wb, fileName);
      } catch (error) {
        console.error("Excel'e aktarma hatası:", error);
        alert("Excel dosyası oluşturulurken bir hata oluştu: " + error.message);
      }
    };

    return {
      dialog,
      formatDate,
      formatTutar,
      exportToExcel,
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

.excel-btn {
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: none;
  min-width: 150px;
  transition: all 0.3s ease;
}

.excel-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.excel-btn .v-icon {
  font-size: 1.2em;
}
</style>
