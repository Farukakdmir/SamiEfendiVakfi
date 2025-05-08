<template>
  <v-dialog
    :model-value="show"
    @update:model-value="$emit('update:show', $event)"
    max-width="800px"
  >
    <v-card>
      <v-card-title
        class="text-h5 font-weight-bold bg-emerald-800 text-white pa-4"
      >
        Şahsi Yardım Detayları
      </v-card-title>

      <v-card-text class="pa-6">
        <div v-if="yardim" class="space-y-6">
          <!-- Yardım Bilgileri -->
          <div class="grid grid-cols-2 gap-6">
            <div>
              <h3 class="text-lg font-semibold mb-2">Yardım Bilgileri</h3>
              <div class="space-y-2">
                <p>
                  <span class="font-medium">Yardım Tipi:</span>
                  {{
                    yardim.yardim_tipi === "individual" ? "Bireysel" : "Grup"
                  }}
                </p>
                <p>
                  <span class="font-medium">Ad Soyad:</span>
                  {{ yardim.ad_soyad }}
                </p>
                <p>
                  <span class="font-medium">Telefon:</span> {{ yardim.telefon }}
                </p>
                <p v-if="yardim.grup_uye_sayisi">
                  <span class="font-medium">Grup Üye Sayısı:</span>
                  {{ yardim.grup_uye_sayisi }}
                </p>
              </div>
            </div>

            <div>
              <h3 class="text-lg font-semibold mb-2">Yardımcılar</h3>
              <div
                v-if="yardim.yardimcilar && yardim.yardimcilar.length > 0"
                class="space-y-2"
              >
                <div
                  v-for="yardimci in yardim.yardimcilar"
                  :key="yardimci.id"
                  class="p-2 bg-gray-50 rounded"
                >
                  <p>
                    <span class="font-medium">Ad Soyad:</span>
                    {{ yardimci.ad_soyad }}
                  </p>
                  <p>
                    <span class="font-medium">Telefon:</span>
                    {{ yardimci.telefon }}
                  </p>
                </div>
              </div>
              <p v-else class="text-gray-500">Yardımcı bulunmuyor</p>
            </div>
          </div>

          <!-- Dosya Bilgileri -->
          <div>
            <h3 class="text-lg font-semibold mb-2">Yardım Edilen Dosyalar</h3>
            <div
              v-if="yardim.dosyalar && yardim.dosyalar.length > 0"
              class="space-y-2"
            >
              <div
                v-for="dosya in yardim.dosyalar"
                :key="dosya.id"
                class="p-2 bg-gray-50 rounded"
              >
                <p>
                  <span class="font-medium">Dosya No:</span>
                  {{ dosya.dosya_no }}
                </p>
                <p>
                  <span class="font-medium">Ad Soyad:</span> {{ dosya.ad }}
                  {{ dosya.soyad }}
                </p>
                <p>
                  <span class="font-medium">Telefon:</span> {{ dosya.telefon }}
                </p>
              </div>
            </div>
            <p v-else class="text-gray-500">Dosya bulunmuyor</p>
          </div>

          <!-- Tarih Bilgileri -->
          <div class="grid grid-cols-2 gap-6">
            <div>
              <p>
                <span class="font-medium">Oluşturulma Tarihi:</span>
                {{ formatDate(yardim.created_at) }}
              </p>
            </div>
            <div>
              <p>
                <span class="font-medium">Son Güncelleme:</span>
                {{ formatDate(yardim.updated_at) }}
              </p>
            </div>
          </div>
        </div>
      </v-card-text>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn color="gray" variant="text" @click="$emit('close')">
          Kapat
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
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
  methods: {
    formatDate(date) {
      if (!date) return "";
      return new Date(date).toLocaleDateString("tr-TR", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
};
</script>
