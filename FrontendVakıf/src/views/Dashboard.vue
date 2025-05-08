<!-- src/views/Dashboard.vue -->
<template>
  <div class="flex h-screen">
    <Navbar />
    <div class="container mx-auto px-4 py-8 ml-64">
      <div class="bg-white rounded-lg shadow p-6 mb-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-blue-100 p-6 rounded-lg">
            <h3 class="text-xl font-bold text-blue-800">Toplam Dosya</h3>
            <p class="text-3xl font-bold text-blue-600">{{ toplamDosya }}</p>
          </div>
          <!-- Diğer istatistikler buraya eklenebilir -->
        </div>
      </div>

      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">Dosyalar</h2>
        <button
          @click="showAddModal = true"
          class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg"
        >
          Yeni Dosya Ekle
        </button>
      </div>

      <!-- Dosya Listesi -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <table class="min-w-full">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Dosya No
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Ad Soyad
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                İşlemler
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="dosya in dosyalar" :key="dosya.dosya_no">
              <td class="px-6 py-4 whitespace-nowrap">
                <button
                  @click="openDosyaDetay(dosya)"
                  class="text-blue-600 hover:text-blue-800"
                >
                  {{ dosya.dosya_no }}
                </button>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {{ dosya.ad }} {{ dosya.soyad }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button
                  @click="showDetails(dosya)"
                  class="text-blue-600 hover:text-blue-900 mr-3"
                >
                  Detaylar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Yeni Dosya Ekleme Modal -->
      <DosyaEkleModal
        v-if="showAddModal"
        @close="showAddModal = false"
        @saved="dosyaEklendi"
        class="z-50"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import DosyaEkleModal from "../components/DosyaEkleModal.vue";
import Navbar from "../components/Navbar.vue";
import axios from "axios";
import { useRouter } from "vue-router";

const dosyalar = ref([]);
const toplamDosya = ref(0);
const showAddModal = ref(false);
const selectedDosya = ref(null);
const router = useRouter();

// Modal açıldığında arka plan scrollunu devre dışı bırakma
watch(showAddModal, (newVal) => {
  if (newVal) {
    document.body.style.overflow = "hidden";
  } else {
    document.body.style.overflow = "auto";
  }
});

watch(selectedDosya, (newVal) => {
  if (newVal) {
    document.body.style.overflow = "hidden";
  } else {
    document.body.style.overflow = "auto";
  }
});

const fetchDosyalar = async () => {
  try {
    const response = await axios.get("/api/dosyalar/");
    dosyalar.value = response.data;
    toplamDosya.value = response.data.length;
  } catch (error) {
    console.error("Dosyalar yüklenirken hata:", error);
  }
};

const showDetails = (dosya) => {
  selectedDosya.value = dosya;
};

const dosyaEklendi = () => {
  showAddModal.value = false;
  fetchDosyalar();
};

const openDosyaDetay = (dosya) => {
  router.push(`/dosya/${dosya.dosya_no}`);
};

onMounted(() => {
  fetchDosyalar();
});
</script>
