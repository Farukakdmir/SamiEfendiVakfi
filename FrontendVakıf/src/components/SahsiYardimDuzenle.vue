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
        Şahsi Yardım Düzenle
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form ref="form" v-model="isValid" @submit.prevent="saveYardim">
          <!-- Yardım Tipi -->
          <v-radio-group
            v-model="formData.yardim_tipi"
            label="Yardım Tipi"
            class="mb-4"
          >
            <v-radio label="Bireysel" value="individual"></v-radio>
            <v-radio label="Grup" value="group"></v-radio>
          </v-radio-group>

          <!-- Ad Soyad ve Telefon -->
          <div class="grid grid-cols-2 gap-4 mb-4">
            <v-text-field
              v-model="formData.ad_soyad"
              label="Ad Soyad"
              :rules="[(v) => !!v || 'Ad Soyad zorunludur']"
              required
            ></v-text-field>
            <v-text-field
              v-model="formData.telefon"
              label="Telefon"
              :rules="[(v) => !!v || 'Telefon zorunludur']"
              required
            ></v-text-field>
          </div>

          <!-- Grup Üye Sayısı -->
          <v-text-field
            v-if="formData.yardim_tipi === 'group'"
            v-model.number="formData.grup_uye_sayisi"
            label="Grup Üye Sayısı"
            type="number"
            :rules="[(v) => !!v || 'Grup üye sayısı zorunludur']"
            required
            class="mb-4"
          ></v-text-field>

          <!-- Yardımcılar -->
          <div class="mb-4">
            <h3 class="text-lg font-semibold mb-2">Yardımcılar</h3>
            <div
              v-for="(yardimci, index) in formData.yardimcilar"
              :key="index"
              class="grid grid-cols-2 gap-4 mb-2"
            >
              <v-text-field
                v-model="yardimci.ad_soyad"
                label="Ad Soyad"
                :rules="[(v) => !!v || 'Ad Soyad zorunludur']"
                required
              ></v-text-field>
              <div class="flex items-center gap-2">
                <v-text-field
                  v-model="yardimci.telefon"
                  label="Telefon"
                  :rules="[(v) => !!v || 'Telefon zorunludur']"
                  required
                ></v-text-field>
                <v-btn
                  color="error"
                  icon
                  @click="removeYardimci(index)"
                  class="mt-2"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </div>
            </div>
            <v-btn
              color="primary"
              variant="text"
              @click="addYardimci"
              class="mt-2"
            >
              <v-icon left>mdi-plus</v-icon>
              Yardımcı Ekle
            </v-btn>
          </div>

          <!-- Dosya Seçimi -->
          <div class="mb-4">
            <h3 class="text-lg font-semibold mb-2">Yardım Edilecek Dosyalar</h3>
            <v-autocomplete
              v-model="formData.dosyalar"
              :items="dosyalar"
              item-title="dosya_no"
              item-value="id"
              label="Dosya Seçin"
              multiple
              chips
              closable-chips
              :rules="[(v) => v.length > 0 || 'En az bir dosya seçilmelidir']"
              required
              return-object
            >
              <template v-slot:chip="{ props, item }">
                <v-chip v-bind="props" class="bg-blue-100 text-blue-800">
                  {{ item.raw.dosya_no }} - {{ item.raw.ad }}
                  {{ item.raw.soyad }}
                </v-chip>
              </template>
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props">
                  <v-list-item-title class="font-medium">
                    {{ item.raw.dosya_no }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    {{ item.raw.ad }} {{ item.raw.soyad }}
                  </v-list-item-subtitle>
                </v-list-item>
              </template>
            </v-autocomplete>
          </div>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn color="gray" variant="text" @click="$emit('close')">
          İptal
        </v-btn>
        <v-btn color="primary" :disabled="!isValid" @click="saveYardim">
          Kaydet
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, onMounted } from "vue";
import apiService from "../api";

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
  emits: ["close", "saved", "update:show"],
  setup(props, { emit }) {
    const form = ref(null);
    const isValid = ref(false);
    const dosyalar = ref([]);
    const formData = ref({
      yardim_tipi: "individual",
      ad_soyad: "",
      telefon: "",
      grup_uye_sayisi: null,
      yardimcilar: [],
      dosyalar: [],
    });

    const loadDosyalar = async () => {
      try {
        const response = await apiService.getDosyalar();
        dosyalar.value = response.data.results || response.data;
      } catch (error) {
        console.error("Dosyalar yüklenirken hata:", error);
      }
    };

    const addYardimci = () => {
      formData.value.yardimcilar.push({
        ad_soyad: "",
        telefon: "",
      });
    };

    const removeYardimci = (index) => {
      formData.value.yardimcilar.splice(index, 1);
    };

    const saveYardim = async () => {
      if (!form.value.validate()) return;

      try {
        const data = {
          yardim_tipi: formData.value.yardim_tipi,
          ad_soyad: formData.value.ad_soyad,
          telefon: formData.value.telefon,
          grup_uye_sayisi: formData.value.grup_uye_sayisi,
          yardimcilar: formData.value.yardimcilar,
          dosyalar: formData.value.dosyalar.map((d) => d.id),
        };

        await apiService.updateSahsiYardim(props.yardim.id, data);
        emit("saved");
        emit("close");
      } catch (error) {
        console.error("Yardım güncellenirken hata:", error);
      }
    };

    onMounted(() => {
      loadDosyalar();
      if (props.yardim) {
        formData.value = {
          yardim_tipi: props.yardim.yardim_tipi,
          ad_soyad: props.yardim.ad_soyad,
          telefon: props.yardim.telefon,
          grup_uye_sayisi: props.yardim.grup_uye_sayisi,
          yardimcilar: props.yardim.yardimcilar || [],
          dosyalar: props.yardim.dosyalar || [],
        };
      }
    });

    return {
      form,
      isValid,
      dosyalar,
      formData,
      addYardimci,
      removeYardimci,
      saveYardim,
    };
  },
};
</script>
