<template>
  <div class="flex h-screen bg-gray-50">
    <Navbar />
    <main
      class="flex-1 bg-gray-200 overflow-y-auto transition-all duration-300"
      :class="{ 'ml-64': isOpen, 'ml-0': !isOpen }"
    >
      <div class="max-w-7xl mx-auto p-8">
        <div class="mb-8">
          <div class="flex justify-center">
            <img
              src="../assets/logo.png"
              alt="Sami Efendi Vakfı"
              class="h-24"
            />
          </div>
        </div>

        <!-- Toplam Maddi Yardım Widget -->
        <div class="max-w-3xl mx-auto mb-8">
          <div class="bg-white overflow-hidden shadow-lg rounded-lg">
            <div class="p-6">
              <div class="flex items-center justify-center">
                <div class="flex-shrink-0">
                  <div class="rounded-md p-4 bg-purple-100">
                    <i
                      class="fas fa-hand-holding-usd text-purple-600 text-2xl"
                    ></i>
                  </div>
                </div>
                <div class="ml-6">
                  <h3 class="text-lg font-medium text-gray-900">
                    Toplam Maddi Yardım
                  </h3>
                  <div class="mt-2">
                    <span class="text-3xl font-bold text-gray-900">
                      {{ formatCurrency(stats.toplam_maddi_yardim || 0) }} ₺
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- İstatistik Kartları -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <!-- Toplam Dosya -->
          <div class="bg-white overflow-hidden shadow-lg rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="rounded-md p-3 bg-green-100">
                    <i class="fas fa-folder text-green-600 text-xl"></i>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Toplam Dosya
                    </dt>
                    <dd class="flex items-baseline">
                      <div class="text-2xl font-semibold text-gray-900">
                        {{ stats.toplam_dosya || 0 }}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Beklemede -->
          <div class="bg-white overflow-hidden shadow-lg rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="rounded-md p-3 bg-yellow-200">
                    <i class="fas fa-clock text-yellow-600 text-xl"></i>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Beklemede
                    </dt>
                    <dd class="flex items-baseline">
                      <div class="text-2xl font-semibold text-gray-900">
                        {{ stats.bekleyen_dosya || 0 }}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Onaylandı -->
          <div class="bg-white overflow-hidden shadow-lg rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="rounded-md p-3 bg-green-200">
                    <i class="fas fa-check-circle text-green-600 text-xl"></i>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Onaylandı
                    </dt>
                    <dd class="flex items-baseline">
                      <div class="text-2xl font-semibold text-gray-900">
                        {{ stats.onaylanan_dosya || 0 }}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Reddedildi -->
          <div class="bg-white overflow-hidden shadow-lg rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="rounded-md p-3 bg-red-200">
                    <i class="fas fa-times-circle text-red-600 text-xl"></i>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Reddedildi
                    </dt>
                    <dd class="flex items-baseline">
                      <div class="text-2xl font-semibold text-gray-900">
                        {{ stats.reddedilen_dosya || 0 }}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Grafikler -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12">
          <!-- Dairesel Grafik -->
          <div class="bg-white shadow-lg rounded-lg p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">
              Dosya Durumları Dağılımı
            </h3>
            <div class="h-80">
              <PieChart :data="pieChartData" :options="pieChartOptions" />
            </div>
          </div>

          <!-- Sütun Grafik -->
          <div class="bg-white shadow-lg rounded-lg p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">
              Dosya Durumları Karşılaştırması
            </h3>
            <div class="h-80">
              <BarChart :data="barChartData" :options="barChartOptions" />
            </div>
          </div>
        </div>

        <!-- Son İşlemler Widget -->
        <div class="bg-white shadow-lg rounded-lg p-6 mb-8">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">
            Son 10 Yardım İşlemi
          </h3>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    İşlem Türü
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Ad Soyad
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Tutar
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Tarih
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Durum
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr
                  v-for="islem in sonIslemler"
                  :key="islem.id"
                  class="hover:bg-gray-50"
                >
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ islem.islem_turu }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ islem.ad_soyad }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ islem.tutar ? formatCurrency(islem.tutar) + " ₺" : "-" }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(islem.tarih) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      :class="[
                        'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
                        islem.durum === 'Onaylandı'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-yellow-100 text-yellow-800',
                      ]"
                    >
                      {{ islem.durum }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, computed, onUnmounted } from "vue";
import Navbar from "../components/Navbar.vue";
import apiService from "../api";
import { useNavbarStore } from "../store/navbar";
import { Pie as PieChart, Bar as BarChart } from "vue-chartjs";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);

export default {
  name: "Home",
  components: {
    Navbar,
    PieChart,
    BarChart,
  },
  setup() {
    const stats = ref({
      toplam_dosya: 0,
      bekleyen_dosya: 0,
      onaylanan_dosya: 0,
      reddedilen_dosya: 0,
      toplam_maddi_yardim: 0,
    });
    const navbarStore = useNavbarStore();
    const sonIslemler = ref([]);

    const pieChartData = computed(() => ({
      labels: ["Beklemede", "Onaylandı", "Reddedildi"],
      datasets: [
        {
          data: [
            stats.value.bekleyen_dosya || 0,
            stats.value.onaylanan_dosya || 0,
            stats.value.reddedilen_dosya || 0,
          ],
          backgroundColor: [
            "#FCD34D", // Sarı
            "#3B82F6", // Mavi
            "#EF4444", // Kırmızı
          ],
          borderWidth: 0,
          hoverOffset: 4,
        },
      ],
    }));

    const pieChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            boxWidth: 12,
            padding: 15,
            font: {
              size: 14,
            },
            generateLabels: function (chart) {
              const datasets = chart.data.datasets;
              return chart.data.labels.map(function (label, i) {
                const meta = chart.getDatasetMeta(0);
                const style = meta.controller.getStyle(i);
                return {
                  text: label,
                  fillStyle: style.backgroundColor,
                  strokeStyle: style.borderColor,
                  lineWidth: style.borderWidth,
                  hidden: isNaN(datasets[0].data[i]) || meta.data[i].hidden,
                  index: i,
                };
              });
            },
          },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = context.label || "";
              const value = context.raw || 0;
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const percentage = Math.round((value / total) * 100);
              return `${label}: ${value} (${percentage}%)`;
            },
          },
        },
      },
    };

    const barChartData = computed(() => ({
      labels: ["Beklemede", "Onaylandı", "Reddedildi"],
      datasets: [
        {
          label: "Dosya Sayısı",
          data: [
            stats.value.bekleyen_dosya || 0,
            stats.value.onaylanan_dosya || 0,
            stats.value.reddedilen_dosya || 0,
          ],
          backgroundColor: [
            "#FCD34D", // Sarı
            "#3B82F6", // Mavi
            "#EF4444", // Kırmızı
          ],
          borderWidth: 0,
          borderRadius: 6,
          hoverBackgroundColor: [
            "#FBBF24", // Koyu Sarı
            "#2563EB", // Koyu Mavi
            "#DC2626", // Koyu Kırmızı
          ],
          barThickness: 40,
          maxBarThickness: 50,
        },
      ],
    }));

    const barChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: "rgba(0, 0, 0, 0.8)",
          padding: 12,
          titleFont: {
            size: 14,
            family: "'Inter', sans-serif",
          },
          bodyFont: {
            size: 13,
            family: "'Inter', sans-serif",
          },
          callbacks: {
            label: function (context) {
              const label = context.dataset.label || "";
              const value = context.raw || 0;
              return `${label}: ${value}`;
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            font: {
              size: 12,
              family: "'Inter', sans-serif",
            },
            padding: 10,
          },
          grid: {
            display: true,
            color: "rgba(0, 0, 0, 0.1)",
          },
        },
        x: {
          ticks: {
            font: {
              size: 12,
              family: "'Inter', sans-serif",
            },
            padding: 10,
          },
          grid: {
            display: false,
          },
        },
      },
      animation: {
        duration: 1000,
        easing: "easeInOutQuart",
      },
      onHover: (event, elements) => {
        event.native.target.style.cursor = elements[0] ? "pointer" : "default";
      },
    };

    // Para formatı için yardımcı fonksiyon
    const formatCurrency = (value) => {
      return new Intl.NumberFormat("tr-TR").format(value);
    };

    // Tarih formatı için yardımcı fonksiyon
    const formatDate = (date) => {
      if (!date) return "-";
      try {
        const dateObj = new Date(date);
        if (isNaN(dateObj.getTime())) return "-";
        return dateObj.toLocaleDateString("tr-TR", {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        });
      } catch (error) {
        console.error("Tarih formatı hatası:", error);
        return "-";
      }
    };

    const fetchStats = async () => {
      try {
        const response = await apiService.getDosyaStats();
        stats.value = response.data;

        // Maddi yardım toplamını getir
        const yardimResponse = await apiService.getMaddiYardimlar();
        const toplamYardim =
          yardimResponse.data.results?.reduce(
            (acc, curr) => acc + (curr.yardim_tutar || 0),
            0
          ) || 0;
        stats.value.toplam_maddi_yardim = toplamYardim;

        // Son işlemleri getir
        const islemlerResponse = await apiService.getSonIslemler();

        // Sadece yardım işlemlerini filtrele
        sonIslemler.value = islemlerResponse.data
          .filter(
            (islem) =>
              islem.islem_turu === "Maddi Yardım" ||
              islem.islem_turu === "Şahsi Yardım"
          )
          .sort((a, b) => new Date(b.tarih) - new Date(a.tarih))
          .slice(0, 10);
      } catch (error) {
        console.error("İstatistikler yüklenirken hata oluştu:", error);
        stats.value = {
          toplam_dosya: 0,
          bekleyen_dosya: 0,
          onaylanan_dosya: 0,
          reddedilen_dosya: 0,
          toplam_maddi_yardim: 0,
        };
        sonIslemler.value = [];
      }
    };

    // Sayfa yüklendiğinde ve her 30 saniyede bir verileri güncelle
    onMounted(() => {
      fetchStats();
      const interval = setInterval(fetchStats, 30000);
      onUnmounted(() => clearInterval(interval));
    });

    return {
      stats,
      isOpen: computed(() => navbarStore.isOpen),
      pieChartData,
      pieChartOptions,
      barChartData,
      barChartOptions,
      formatCurrency,
      formatDate,
      sonIslemler,
    };
  },
};
</script>

<style scoped>
/* Tailwind classes handle most styling */
</style>
