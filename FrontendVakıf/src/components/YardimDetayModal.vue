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
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Yardım Detayları
                </h3>
                <button
                  @click="$emit('close')"
                  class="text-gray-400 hover:text-gray-500"
                >
                  <span class="sr-only">Kapat</span>
                  <svg
                    class="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
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

              <!-- Kişisel Bilgiler -->
              <div class="bg-gray-50 p-4 rounded-lg mb-4">
                <h4 class="text-lg font-medium text-gray-900 mb-3">
                  {{ dosya.ad }} {{ dosya.soyad }}
                </h4>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <p class="text-sm text-gray-600">
                      <span class="font-medium">İsim:</span>
                      {{ dosya.ad }} {{ dosya.soyad }}
                    </p>
                    <p class="text-sm text-gray-600">
                      <span class="font-medium">Dosya No:</span>
                      {{ dosya.dosya_no }}
                    </p>
                    <p class="text-sm text-gray-600">
                      <span class="font-medium">Kimlik No:</span>
                      {{ dosya.kimlik_no }}
                    </p>
                    <p class="text-sm text-gray-600">
                      <span class="font-medium">Telefon:</span>
                      {{ dosya.telefon }}
                    </p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">
                      <span class="font-medium">Adres:</span>
                      {{ formatAddress(dosya) }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- Toplam Yardım Özeti -->
              <div class="bg-emerald-50 p-4 rounded-lg mb-4">
                <h4 class="text-lg font-semibold mb-2">Toplam Yardım Özeti</h4>
                <div class="grid grid-cols-2 gap-4">
                  <div class="bg-white p-3 rounded-lg shadow">
                    <p class="text-sm text-gray-600">Toplam Yardım Tutarı</p>
                    <p class="text-xl font-bold text-emerald-600">
                      {{ formatCurrency(totalYardimTutari) }} ₺
                    </p>
                  </div>
                  <div class="bg-white p-3 rounded-lg shadow">
                    <p class="text-sm text-gray-600">Toplam Yardım Sayısı</p>
                    <p class="text-xl font-bold text-emerald-600">
                      {{ yardimlar.length }} Adet
                    </p>
                  </div>
                </div>
              </div>

              <!-- Yardım Detayları -->
              <div class="bg-white rounded-lg">
                <h4 class="text-lg font-semibold mb-4">Yardım Geçmişi</h4>
                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                      <tr>
                        <th
                          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Tarih
                        </th>
                        <th
                          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Yardım Yapan
                        </th>
                        <th
                          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Telefon
                        </th>
                        <th
                          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Tutar
                        </th>
                        <th
                          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Açıklama
                        </th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr
                        v-for="yardim in yardimlar"
                        :key="yardim.id"
                        class="hover:bg-gray-50"
                      >
                        <td
                          class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                        >
                          {{ formatDate(yardim.created_at) }}
                        </td>
                        <td
                          class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                        >
                          {{ yardim.yardim_yapan_ad_soyad }}
                        </td>
                        <td
                          class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                        >
                          {{ yardim.yardim_yapan_telefon }}
                        </td>
                        <td
                          class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                        >
                          {{ formatCurrency(yardim.tutar) }} ₺
                        </td>
                        <td class="px-6 py-4 text-sm text-gray-500">
                          {{ yardim.aciklama || "Açıklama yok" }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            @click="$emit('close')"
          >
            Kapat
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from "vue";
import { formatDate, formatAddress } from "../utils/printUtils";

export default {
  name: "YardimDetayModal",
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    dosya: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    // Para formatı için yardımcı fonksiyon
    const formatCurrency = (value) => {
      return new Intl.NumberFormat("tr-TR").format(value);
    };

    // Yardımları hesapla
    const yardimlar = computed(() => {
      console.log("Yardımlar computed çalıştı:", props.dosya?.yardimlar);
      if (!props.dosya?.yardimlar) return [];

      return props.dosya.yardimlar.map((yardim) => ({
        ...yardim,
        tutar: Number(yardim.tutar) || 0,
        created_at: new Date(yardim.created_at),
      }));
    });

    // Toplam yardım tutarını hesapla
    const totalYardimTutari = computed(() => {
      console.log("Dosya yardımları:", props.dosya?.yardimlar);
      if (!props.dosya?.yardimlar) return 0;

      const total = props.dosya.yardimlar.reduce((sum, yardim) => {
        console.log("Yardım tutarı:", yardim.tutar);
        return sum + (Number(yardim.tutar) || 0);
      }, 0);

      console.log("Toplam tutar:", total);
      return total;
    });

    return {
      formatDate,
      formatAddress,
      formatCurrency,
      yardimlar,
      totalYardimTutari,
    };
  },
};
</script>
