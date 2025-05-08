<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Üst Bilgi Kartı -->
    <div
      class="bg-gradient-to-r from-emerald-800 to-emerald-900 p-6 text-white"
    >
      <div class="flex justify-between items-start">
        <div class="flex items-center space-x-6">
          <div class="w-32 h-32 bg-white rounded-lg overflow-hidden">
            <img
              v-if="currentProfileImage"
              :src="currentProfileImage"
              @click="openImagePreview(currentProfileImage)"
              class="w-full h-full object-cover cursor-pointer hover:opacity-90"
              alt="Profil Resmi"
              @error="
                console.error('Profil resmi yüklenemedi:', currentProfileImage)
              "
            />
            <div
              v-else
              class="w-full h-full flex items-center justify-center bg-gray-200"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-16 w-16 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
            </div>
          </div>
          <div>
            <h1 class="text-3xl font-bold">
              {{ dosya?.ad }} {{ dosya?.soyad }}
            </h1>
            <p class="text-emerald-100 mt-1">Dosya No: {{ dosya?.dosya_no }}</p>
            <p class="text-emerald-100">Kimlik No: {{ dosya?.kimlik_no }}</p>
            <div class="mt-2">
              <span
                :class="getStatusClass(dosya?.durum)"
                class="px-3 py-1 rounded-full text-sm"
              >
                {{ dosya?.durum }}
              </span>
            </div>
          </div>
        </div>
        <button
          @click="router.back()"
          class="bg-white text-emerald-800 px-4 py-2 rounded-lg hover:bg-emerald-50 transition-colors"
        >
          <span class="flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 mr-2"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
                clip-rule="evenodd"
              />
            </svg>
            Geri Dön
          </span>
        </button>
      </div>
    </div>

    <!-- Durum Değiştirme Bölümü -->
    <div class="container mx-auto px-4 py-4">
      <div class="bg-white rounded-lg shadow p-4 mb-6">
        <h3 class="text-lg font-semibold mb-4">Onay Durumu Güncelleme</h3>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block mb-2 font-medium">Yeni Durum</label>
            <select v-model="yeniDurum" class="w-full border rounded p-2">
              <option value="BEKLEMEDE">Beklemede</option>
              <option value="ONAYLANDI">Onaylandı</option>
              <option value="REDDEDILDI">Reddedildi</option>
            </select>
          </div>
          <div>
            <label class="block mb-2 font-medium">Güncelleme Tarihi</label>
            <input
              v-model="guncellemeTarihi"
              type="date"
              class="w-full border rounded p-2"
            />
          </div>
          <div class="col-span-2">
            <label class="block mb-2 font-medium">Açıklama Notu</label>
            <textarea
              v-model="durumAciklama"
              class="w-full border rounded p-2"
              rows="3"
              placeholder="Durum değişikliği ile ilgili açıklama"
            ></textarea>
          </div>
        </div>
        <div class="mt-4 flex justify-end">
          <button
            @click="updateDurum"
            class="bg-emerald-600 text-white px-4 py-2 rounded-md hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
          >
            Durumu Güncelle
          </button>
        </div>
      </div>
    </div>

    <!-- Tab Menüsü -->
    <div class="container mx-auto px-4 py-8">
      <div class="bg-white shadow-lg rounded-lg overflow-hidden">
        <!-- Tab Menüsü -->
        <div class="border-b border-gray-200">
          <nav class="flex -mb-px">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                activeTab === tab.id
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm',
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>

        <!-- Tab İçerikleri -->
        <div class="p-6">
          <!-- Kişisel Bilgiler Tab -->
          <div v-if="activeTab === 'personal'" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="bg-gray-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold mb-4">Kişisel Bilgiler</h3>
                <div class="space-y-3">
                  <div>
                    <p class="text-sm text-gray-600">Ad</p>
                    <p class="font-medium">{{ dosya?.ad }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">Soyad</p>
                    <p class="font-medium">{{ dosya?.soyad }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">Kimlik No</p>
                    <p class="font-medium">{{ dosya?.kimlik_no }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">Telefon</p>
                    <p class="font-medium">{{ dosya?.telefon }}</p>
                  </div>
                </div>
              </div>

              <div class="bg-gray-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold mb-4">Adres Bilgileri</h3>
                <div class="space-y-3">
                  <div>
                    <p class="text-sm text-gray-600">Mahalle</p>
                    <p class="font-medium">{{ dosya?.mahalle }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">Cadde/Sokak</p>
                    <p class="font-medium">{{ dosya?.cadde_sokak }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">Bina No</p>
                    <p class="font-medium">{{ dosya?.bina_no }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">Daire No</p>
                    <p class="font-medium">{{ dosya?.daire_no }}</p>
                  </div>
                </div>
              </div>

              <div class="bg-gray-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold mb-4">Diğer Bilgiler</h3>
                <div class="space-y-3">
                  <div>
                    <p class="text-sm text-gray-600">Kayıt Tarihi</p>
                    <p class="font-medium">
                      {{ formatDate(dosya?.kayit_tarihi) }}
                    </p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">Uyruk</p>
                    <p class="font-medium">{{ dosya?.uyruk }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">Dolduran Kişi</p>
                    <p class="font-medium">
                      {{ dosya?.dolduran_kisi || "Belirtilmemiş" }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Aile Üyeleri Tab -->
          <div v-if="activeTab === 'family'" class="space-y-6">
            <div class="bg-white rounded-lg shadow overflow-hidden">
              <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold">Aile Üyeleri</h3>
                <p class="text-sm text-gray-600">
                  Toplam {{ familyMembers.length + 1 }} üye
                </p>
              </div>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        Ad
                      </th>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        Soyad
                      </th>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        Cinsiyet
                      </th>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        Engel Durumu
                      </th>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        Engel Açıklaması
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr
                      v-for="(member, index) in familyMembers"
                      :key="index"
                      class="hover:bg-gray-50"
                    >
                      <td class="px-6 py-4 whitespace-nowrap">
                        {{ member.ad }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        {{ member.soyad }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        {{ member.cinsiyet === "E" ? "Erkek" : "Kadın" }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span
                          :class="
                            member.engel_durumu
                              ? 'bg-red-100 text-red-800'
                              : 'bg-green-100 text-green-800'
                          "
                          class="px-2 py-1 rounded-full text-xs"
                        >
                          {{ member.engel_durumu ? "Var" : "Yok" }}
                        </span>
                      </td>
                      <td class="px-6 py-4">
                        {{ member.engel_aciklama || "-" }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Belgeler Tab -->
          <div v-if="activeTab === 'documents'" class="space-y-6">
            <div class="bg-white rounded-lg shadow overflow-hidden">
              <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold">Yüklenen Belgeler</h3>
              </div>
              <div class="p-6">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div
                    v-for="(belge, key) in dosyaBelgeleri"
                    :key="key"
                    class="bg-gray-50 rounded-lg p-4"
                  >
                    <div class="flex justify-between items-center mb-4">
                      <h4 class="font-medium">{{ getBelgeAdi(key) }}</h4>
                      <div class="flex space-x-2">
                        <button
                          v-if="belge"
                          @click="deleteBelge(key)"
                          class="text-red-600 hover:text-red-800"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-5 w-5"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                          >
                            <path
                              fill-rule="evenodd"
                              d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                              clip-rule="evenodd"
                            />
                          </svg>
                        </button>
                        <label
                          v-if="!belge"
                          class="text-blue-600 hover:text-blue-800 cursor-pointer"
                        >
                          <input
                            type="file"
                            class="hidden"
                            @change="uploadBelge($event, key)"
                            accept=".jpg,.jpeg,.png,.pdf,.doc,.docx"
                          />
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-5 w-5"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                          >
                            <path
                              fill-rule="evenodd"
                              d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L7.707 6.707a1 1 0 01-1.414 0z"
                              clip-rule="evenodd"
                            />
                          </svg>
                        </label>
                      </div>
                    </div>
                    <div v-if="isImageFile(belge)" class="relative group">
                      <img
                        :src="belge"
                        alt="Belge"
                        class="w-full h-48 object-cover rounded cursor-pointer hover:opacity-75 transition-opacity"
                        @click="openImagePreview(belge)"
                      />
                      <div
                        class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                        @click="openImagePreview(belge)"
                      >
                        <span
                          class="text-white bg-black bg-opacity-50 px-2 py-1 rounded"
                          >Büyük görüntüle</span
                        >
                      </div>
                    </div>
                    <div v-else-if="belge" class="text-center">
                      <a
                        :href="belge"
                        target="_blank"
                        class="text-blue-600 hover:text-blue-800 underline"
                      >
                        {{ getBelgeAdi(key) }} - İndir
                      </a>
                    </div>
                    <div v-else class="text-center text-gray-500">
                      Belge yüklenmemiş
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Durum Geçmişi Tab -->
          <div v-if="activeTab === 'history'" class="space-y-6">
            <div class="bg-white rounded-lg shadow overflow-hidden">
              <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold">Durum Değişiklik Geçmişi</h3>
              </div>
              <div class="p-6">
                <div
                  class="space-y-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar"
                >
                  <div
                    v-for="(degisiklik, index) in durumDegisiklikleri"
                    :key="index"
                    class="border-b pb-4 last:border-b-0"
                  >
                    <div class="flex justify-between items-start">
                      <div>
                        <p class="font-medium">
                          {{ formatDate(degisiklik.degisiklik_tarihi) }}
                          {{ formatTime(degisiklik.degisiklik_tarihi) }} -
                          <span :class="getStatusClass(degisiklik.yeni_durum)">
                            {{ degisiklik.yeni_durum_adi }}
                          </span>
                        </p>
                        <p class="text-sm text-gray-600 mt-1">
                          Değiştiren: {{ degisiklik.degistiren_adi }}
                        </p>
                        <p
                          v-if="degisiklik.aciklama"
                          class="text-sm text-gray-700 mt-2"
                        >
                          Açıklama: {{ degisiklik.aciklama }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Resim Önizleme Modalı -->
    <div
      v-if="selectedImage"
      class="fixed inset-0 bg-black bg-opacity-75 z-[60] flex items-center justify-center"
      @click="selectedImage = null"
    >
      <div class="relative max-w-4xl mx-auto" @click.stop>
        <img
          :src="selectedImage"
          class="max-w-full max-h-[80vh] object-contain"
          alt="Belge önizleme"
        />
        <button
          @click="selectedImage = null"
          class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2 hover:bg-red-600 focus:outline-none"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
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
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import apiService from "../api";
import { DURUM_CHOICES } from "../constants";

export default {
  name: "DosyaDetay",
  setup() {
    const route = useRoute();
    const router = useRouter();
    const dosya = ref(null);
    const familyMembers = ref([]);
    const dosyaBelgeleri = ref({
      KONTRAT: null,
      OLUM_BELGESI: null,
      VUKUATLI_NUFUS: null,
      OGRENCI_BELGESI: null,
      BANKA_EKSTRESI: null,
      TEMVIYYE: null,
    });
    const selectedImage = ref(null);
    const currentProfileImage = ref(null);
    const durumDegisiklikleri = ref([]);
    const activeTab = ref("personal");
    const yeniDurum = ref("");
    const durumAciklama = ref("");
    const guncellemeTarihi = ref(new Date().toISOString().split("T")[0]);

    const tabs = [
      { id: "personal", name: "Kişisel Bilgiler" },
      { id: "family", name: "Aile Üyeleri" },
      { id: "documents", name: "Belgeler" },
      { id: "history", name: "Durum Geçmişi" },
    ];

    const fetchDosya = async () => {
      try {
        const response = await apiService.getDosya(route.params.dosyaNo);
        dosya.value = response.data;
        familyMembers.value = response.data.aile_bilgileri || [];
        currentProfileImage.value = response.data.profil_resmi;

        // Belgeleri yükle
        if (response.data.belgeler) {
          dosyaBelgeleri.value = {
            ...dosyaBelgeleri.value,
            ...response.data.belgeler,
          };
        }

        // Durum değişikliklerini yükle
        if (response.data.durum_degisiklikleri) {
          durumDegisiklikleri.value = response.data.durum_degisiklikleri;
        }
      } catch (error) {
        console.error("Dosya bilgileri yüklenirken hata:", error);
      }
    };

    const getStatusClass = (status) => {
      const statusClasses = {
        BEKLEMEDE: "bg-yellow-100 text-yellow-800",
        ONAYLANDI: "bg-green-100 text-green-800",
        REDDEDILDI: "bg-red-100 text-red-800",
      };
      return statusClasses[status] || "bg-gray-100 text-gray-800";
    };

    const formatDate = (date) => {
      if (!date) return "";
      return new Date(date).toLocaleDateString("tr-TR");
    };

    const formatTime = (date) => {
      if (!date) return "";
      return new Date(date).toLocaleTimeString("tr-TR", {
        hour: "2-digit",
        minute: "2-digit",
      });
    };

    const getBelgeAdi = (key) => {
      const belgeAdlari = {
        KONTRAT: "Kira Kontratı",
        OLUM_BELGESI: "Ölüm Belgesi",
        VUKUATLI_NUFUS: "Vukuatlı Nüfus Kayıt Örneği",
        OGRENCI_BELGESI: "Öğrenci Belgesi",
        BANKA_EKSTRESI: "Banka Ekstresi",
        TEMVIYYE: "Temviyye Belgesi",
      };
      return belgeAdlari[key] || key;
    };

    const isImageFile = (url) => {
      if (!url || typeof url !== "string") return false;
      const lowerUrl = url.toLowerCase();
      return (
        lowerUrl.endsWith(".jpg") ||
        lowerUrl.endsWith(".jpeg") ||
        lowerUrl.endsWith(".png") ||
        lowerUrl.endsWith(".gif") ||
        lowerUrl.includes("/media/images/") ||
        lowerUrl.includes("/media/documents/") ||
        lowerUrl.match(/\.(jpe?g|png|gif)($|\?)/)
      );
    };

    const openImagePreview = (imageUrl) => {
      console.log("Resim önizleme açılıyor:", imageUrl);
      selectedImage.value = imageUrl;
    };

    const deleteBelge = async (belgeTuru) => {
      if (!confirm("Bu belgeyi silmek istediğinizden emin misiniz?")) return;

      try {
        // Belge türünü kontrol et
        if (!belgeTuru || belgeTuru === "0") {
          console.error("Geçersiz belge türü:", belgeTuru);
          return;
        }

        const response = await apiService.deleteBelge(
          route.params.dosyaNo,
          belgeTuru
        );

        if (response.status === 200 || response.status === 204) {
          // Belge silindikten sonra belgeleri yeniden yükle
          await loadDosyaBelgeleri();
          alert("Belge başarıyla silindi.");
        } else {
          throw new Error("Belge silme işlemi başarısız oldu.");
        }
      } catch (error) {
        console.error("Belge silinirken hata:", error);
        let errorMessage = "Belge silinirken bir hata oluştu.";

        if (error.response) {
          if (error.response.status === 404) {
            errorMessage = "Belge bulunamadı veya silinmiş olabilir.";
          } else if (error.response.data && error.response.data.detail) {
            errorMessage = error.response.data.detail;
          }
        }

        alert(errorMessage);
      }
    };

    const uploadBelge = async (event, belgeTuru) => {
      const file = event.target.files[0];
      if (!file) return;

      try {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("belge_turu", belgeTuru);

        const response = await apiService.uploadBelge(
          route.params.dosyaNo,
          formData
        );

        // Belge yüklendikten sonra belgeleri yeniden yükle
        await loadDosyaBelgeleri();

        // Başarılı mesajı göster
        alert("Belge başarıyla yüklendi.");
      } catch (error) {
        console.error("Belge yükleme hatası:", error);
        alert(
          "Belge yüklenirken bir hata oluştu: " +
            (error.response?.data?.detail || error.message)
        );
      }
    };

    // Belge yükleme fonksiyonunu ekle
    const loadDosyaBelgeleri = async () => {
      try {
        const response = await apiService.getBelgeler(route.params.dosyaNo);
        const belgeler = response.data;
        console.log("Belgeler yüklendi:", belgeler);

        // Belge türlerine göre boş obje oluştur
        const belgeMap = {
          KONTRAT: null,
          OLUM_BELGESI: null,
          VUKUATLI_NUFUS: null,
          OGRENCI_BELGESI: null,
          BANKA_EKSTRESI: null,
          TEMVIYYE: null,
        };

        // Her bir belgeyi ilgili türe göre eşle
        belgeler.forEach((belge) => {
          // Belge türü geçerli bir anahtar mı kontrol et
          if (belge.belge_turu && belge.belge_turu in belgeMap) {
            // Tam URL oluştur
            let belgeUrl = belge.belge_url;
            // Eğer URL http:// veya https:// ile başlamıyorsa, backend URL'sine ekle
            if (
              belgeUrl &&
              !belgeUrl.startsWith("http://") &&
              !belgeUrl.startsWith("https://")
            ) {
              const backendUrl =
                import.meta.env.VITE_API_URL || "http://localhost:8000";
              belgeUrl = `${backendUrl}${belgeUrl}`;
            }
            belgeMap[belge.belge_turu] = belgeUrl;
          }
        });

        dosyaBelgeleri.value = belgeMap;
      } catch (error) {
        console.error("Belgeler yüklenirken hata:", error);
      }
    };

    const updateDurum = async () => {
      if (!yeniDurum.value) {
        alert("Lütfen yeni durum seçiniz.");
        return;
      }

      try {
        await apiService.updateDosyaDurum(route.params.dosyaNo, {
          durum: yeniDurum.value,
          aciklama: durumAciklama.value || "",
          tarih: guncellemeTarihi.value,
          degistiren_id: localStorage.getItem("userId"),
        });

        // Dosya bilgilerini yeniden yükle
        await fetchDosya();

        // Form alanlarını temizle
        yeniDurum.value = "";
        durumAciklama.value = "";
        guncellemeTarihi.value = new Date().toISOString().split("T")[0];

        alert("Durum başarıyla güncellendi.");
      } catch (error) {
        console.error("Durum güncellenirken hata:", error);
        if (error.response?.data?.detail) {
          alert(error.response.data.detail);
        } else {
          alert("Durum güncellenirken bir hata oluştu.");
        }
      }
    };

    onMounted(() => {
      fetchDosya();
      loadDosyaBelgeleri();
    });

    return {
      dosya,
      familyMembers,
      dosyaBelgeleri,
      selectedImage,
      currentProfileImage,
      durumDegisiklikleri,
      activeTab,
      tabs,
      yeniDurum,
      durumAciklama,
      DURUM_CHOICES,
      getStatusClass,
      formatDate,
      formatTime,
      getBelgeAdi,
      isImageFile,
      openImagePreview,
      deleteBelge,
      uploadBelge,
      updateDurum,
      router,
      guncellemeTarihi,
    };
  },
};
</script>

<style scoped>
.tab-content {
  transition: all 0.3s ease;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
