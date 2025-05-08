<template>
  <div
    v-if="dosya && !showEditModal"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-[200]"
    @click.self="$emit('close')"
  >
    <div
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-[201]"
    >
      <div
        class="relative bg-white w-[1200px] shadow-lg rounded-md p-8 max-h-[90vh] overflow-y-auto z-[202]"
      >
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold">
            Dosya Detayı - {{ dosya.dosya_no }}
          </h2>
          <button
            @click="$emit('close')"
            class="fixed top-4 right-4 text-gray-500 hover:text-gray-700 bg-white rounded-full p-2 shadow-lg hover:shadow-xl z-[103]"
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

        <!-- Kişisel Bilgiler -->
        <div class="bg-gray-50 p-4 rounded-lg mb-6">
          <div class="flex items-center space-x-6 mb-6">
            <div class="w-32 h-32 bg-gray-200 rounded-lg">
              <img
                v-if="currentProfileImage"
                :src="currentProfileImage"
                @click="openImagePreview(currentProfileImage)"
                class="w-full h-full object-cover rounded-lg cursor-pointer hover:opacity-90"
                alt="Profil Resmi"
                @error="
                  console.error(
                    'Profil resmi yüklenemedi:',
                    currentProfileImage
                  )
                "
                @load="
                  console.log('Profil resmi yüklendi:', currentProfileImage)
                "
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center text-gray-400"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-16 w-16"
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
              <h2 class="text-2xl font-bold text-gray-900">
                {{ dosya.ad }} {{ dosya.soyad }}
              </h2>
              <p class="text-gray-600">Dosya No: {{ dosya.dosya_no }}</p>
              <p class="text-gray-600">Kimlik No: {{ dosya.kimlik_no }}</p>
            </div>
          </div>

          <h4 class="text-lg font-semibold mb-4">Kişisel Bilgiler</h4>
          <div class="grid grid-cols-3 gap-4">
            <div>
              <p class="text-sm text-gray-600">Ad</p>
              <p class="font-medium">{{ dosya.ad }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Soyad</p>
              <p class="font-medium">{{ dosya.soyad }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Kimlik No</p>
              <p class="font-medium">{{ dosya.kimlik_no }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Telefon</p>
              <p class="font-medium">{{ dosya.telefon }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Kayıt Tarihi</p>
              <p class="font-medium">{{ formatDate(dosya.kayit_tarihi) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Mevcut Durum</p>
              <span :class="getStatusClass(dosya.durum)">
                {{ dosya.durum }}
              </span>
            </div>
            <div>
              <p class="text-sm text-gray-600">Uyruk</p>
              <p class="font-medium">{{ dosya.uyruk }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Dolduran Kişi</p>
              <p class="font-medium">
                {{ dosya.dolduran_kisi || "Belirtilmemiş" }}
              </p>
            </div>
          </div>
        </div>

        <!-- Onay Durumu Güncelleme -->
        <div class="bg-gray-50 p-4 rounded-lg mb-6">
          <h4 class="text-lg font-semibold mb-4">Onay Durumu Güncelleme</h4>
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
                v-model="aciklamaNotu"
                class="w-full border rounded p-2"
                rows="3"
                placeholder="Durum değişikliği ile ilgili açıklama"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Durum Değişiklik Geçmişi -->
        <div class="bg-gray-50 p-4 rounded-lg mb-6">
          <h4 class="text-lg font-semibold mb-4">Durum Değişiklik Geçmişi</h4>
          <div class="space-y-4 max-h-[300px] overflow-y-auto pr-2">
            <div
              v-for="(degisiklik, index) in durumDegisiklikleri"
              :key="index"
              class="border-b pb-4"
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

        <!-- Aile Bilgileri -->
        <div class="bg-gray-50 p-4 rounded-lg mb-6">
          <div class="flex justify-between items-center mb-4">
            <h4 class="text-lg font-semibold">Aile Bilgileri</h4>
            <div class="bg-blue-100 text-blue-800 px-4 py-2 rounded-lg">
              Toplam Aile Üyesi: {{ familyMembers.length + 1 }}
            </div>
          </div>
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-100">
              <tr>
                <th class="px-4 py-2 text-left">Ad</th>
                <th class="px-4 py-2 text-left">Soyad</th>
                <th class="px-4 py-2 text-left">Cinsiyet</th>
                <th class="px-4 py-2 text-left">Engel Durumu</th>
                <th class="px-4 py-2 text-left">Engel Açıklaması</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(member, index) in familyMembers"
                :key="index"
                class="hover:bg-gray-50"
              >
                <td class="px-4 py-2">{{ member.ad }}</td>
                <td class="px-4 py-2">{{ member.soyad }}</td>
                <td class="px-4 py-2">
                  {{ member.cinsiyet === "E" ? "Erkek" : "Kadın" }}
                </td>
                <td class="px-4 py-4 text-sm">
                  <span
                    :class="
                      member.engel_durumu
                        ? 'text-red-600 bg-red-100 px-2 py-1 rounded-md text-xs'
                        : 'text-green-600 bg-green-100 px-2 py-1 rounded-md text-xs'
                    "
                  >
                    {{ member.engel_durumu ? "Var" : "Yok" }}
                  </span>
                </td>
                <td class="px-4 py-2">{{ member.engel_aciklama || "-" }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Yüklenen Belgeler -->
        <div class="bg-gray-50 p-4 rounded-lg mb-6">
          <h4 class="text-lg font-semibold mb-4">Yüklenen Belgeler</h4>
          <div class="grid grid-cols-3 gap-4">
            <div
              v-for="(belge, key) in dosyaBelgeleri"
              :key="key"
              class="border rounded p-3 bg-white"
            >
              <div class="flex justify-between items-center mb-2">
                <p class="font-medium">{{ getBelgeAdi(key) }}</p>
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
              </div>
              <div v-if="isImageFile(belge)" class="relative group w-full">
                <img
                  :src="belge"
                  alt="Belge"
                  class="w-32 h-32 object-cover rounded cursor-pointer hover:opacity-75 transition-opacity"
                  @click.stop="openImagePreview(belge)"
                />
                <div
                  class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                  @click.stop="openImagePreview(belge)"
                >
                  <span
                    class="text-white bg-black bg-opacity-50 px-2 py-1 rounded"
                  >
                    Büyük görüntüle
                  </span>
                </div>
              </div>
              <div v-else>
                <a
                  :href="belge"
                  target="_blank"
                  class="text-blue-600 hover:text-blue-800 underline"
                >
                  {{ getBelgeAdi(key) }} - İndir
                </a>
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

        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 border rounded hover:bg-gray-100"
          >
            İptal
          </button>
          <button
            @click="saveChanges"
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Değişiklikleri Kaydet
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import apiService from "../api";
import {
  DURUM_CHOICES,
  UYRUK_CHOICES,
  kiraDurumuSecenekleri,
  cinsiyetSecenekleri,
  yakinlikSecenekleri,
} from "../constants";

export default {
  name: "DosyaDetayModal",
  props: {
    dosya: {
      type: Object,
      required: true,
    },
    showEditModal: {
      type: Boolean,
      default: false,
    },
    editMode: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { emit }) {
    const yeniDurum = ref(props.dosya.durum);
    const guncellemeTarihi = ref(new Date().toISOString().split("T")[0]);
    const aciklamaNotu = ref(props.dosya.notlar || "");
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

    // Yakınlık türleri tanımı
    const yakinlikTurleri = {
      KENDISI: "Kendisi",
      ES: "Eş",
      COCUK: "Çocuk",
      ANNE: "Anne",
      BABA: "Baba",
      KARDES: "Kardeş",
      DIGER: "Diğer",
    };

    // Profil resmi URL'sini oluştur
    const getProfileImageUrl = (imagePath) => {
      if (!imagePath) return null;

      // Eğer URL zaten http ile başlıyorsa, olduğu gibi döndür
      if (imagePath.startsWith("http")) {
        return imagePath;
      }

      // Backend URL'sini al
      const backendUrl =
        import.meta.env.VITE_API_URL || "http://localhost:8000";

      // URL'yi oluştur
      return `${backendUrl}${imagePath}`;
    };

    // Profil resmini izle ve güncelle
    watch(
      () => props.dosya,
      async (newDosya) => {
        if (newDosya && newDosya.profil_resmi) {
          try {
            // Güncel dosya bilgilerini al
            const response = await apiService.getDosya(newDosya.dosya_no);
            const updatedDosya = response.data;

            // Profil resmi URL'sini güncelle
            if (updatedDosya.profil_resmi) {
              const backendUrl =
                import.meta.env.VITE_API_URL || "http://localhost:8000";
              if (!updatedDosya.profil_resmi.startsWith("http")) {
                currentProfileImage.value = `${backendUrl}${updatedDosya.profil_resmi}`;
              } else {
                currentProfileImage.value = updatedDosya.profil_resmi;
              }
              console.log(
                "Profil resmi güncellendi:",
                currentProfileImage.value
              );
            }
          } catch (error) {
            console.error("Profil resmi güncellenirken hata:", error);
          }
        }
      },
      { immediate: true, deep: true }
    );

    // Aile üyelerini yükleme
    const loadFamilyMembers = async () => {
      try {
        const response = await apiService.getFamilyMembers(
          props.dosya.dosya_no
        );
        // Sadece gerekli alanları al
        familyMembers.value = response.data.map((member) => ({
          ad: member.ad,
          soyad: member.soyad,
          cinsiyet: member.cinsiyet,
          engel_durumu: member.engel_durumu || false,
          engel_aciklama: member.engel_aciklama || "",
        }));

        // Toplam aile üyesi sayısını hesapla ve kaydet
        const toplamAileUyesi = familyMembers.value.length + 1; // Aile reisi dahil
        try {
          // Önce mevcut dosya bilgilerini al
          const dosyaResponse = await apiService.getDosya(props.dosya.dosya_no);
          const mevcutDosya = dosyaResponse.data;

          // profil_resmi alanını çıkar ve diğer bilgileri koru
          const { profil_resmi, ...guncellenecekDosya } = mevcutDosya;

          // Mevcut bilgileri koruyarak sadece toplam_aile_uyesi'ni güncelle
          await apiService.updateDosya(props.dosya.dosya_no, {
            ...guncellenecekDosya,
            toplam_aile_uyesi: toplamAileUyesi,
          });

          console.log("Toplam aile üyesi sayısı güncellendi:", toplamAileUyesi);
        } catch (error) {
          console.error("Toplam aile üyesi sayısı güncellenirken hata:", error);
        }
      } catch (error) {
        console.error("Aile üyeleri yüklenirken hata:", error);
      }
    };

    // Belge yüklemelerini yükleme
    const loadDosyaBelgeleri = async () => {
      try {
        const response = await apiService.getBelgeler(props.dosya.dosya_no);
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
          if (belge.belge_turu in belgeMap) {
            // Tam URL oluştur
            let belgeUrl = belge.belge_url;
            // Eğer URL http:// veya https:// ile başlamıyorsa, backend URL'sine ekle
            if (
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
        console.log("Belge haritası:", dosyaBelgeleri.value);
      } catch (error) {
        console.error("Belgeler yüklenirken hata:", error);
      }
    };

    // Dosya detaylarını yeniden yükle
    const reloadDosyaDetails = async () => {
      try {
        const response = await apiService.getDosya(props.dosya.dosya_no);
        const updatedDosya = response.data;
        emit("update:dosya", updatedDosya);

        // Açıklama notunu güncelle
        if (updatedDosya.notlar) {
          aciklamaNotu.value = updatedDosya.notlar;
        }
      } catch (error) {
        console.error("Dosya detayları yüklenirken hata:", error);
      }
    };

    // Durum değişikliklerini yükle
    const loadDurumDegisiklikleri = async () => {
      try {
        const response = await apiService.getDurumDegisiklikleri(
          props.dosya.dosya_no
        );
        durumDegisiklikleri.value = response.data;
      } catch (error) {
        console.error("Durum değişiklikleri yüklenirken hata:", error);
      }
    };

    // Değişiklikleri kaydetme
    const saveChanges = async () => {
      try {
        // API'ye durum güncellemesi için özel istek yap
        const response = await apiService.updateDosyaDurum(
          props.dosya.dosya_no,
          {
            durum: yeniDurum.value,
            aciklama: aciklamaNotu.value,
            tarih: guncellemeTarihi.value,
          }
        );

        if (response.status === 200) {
          // Dosya detaylarını yeniden yükle
          await reloadDosyaDetails();
          // Durum değişikliklerini yeniden yükle
          await loadDurumDegisiklikleri();

          // Özel bir event yayınlama - stats değişikliğini bildirme
          const statsUpdateEvent = new CustomEvent("stats-update-needed");
          window.dispatchEvent(statsUpdateEvent);

          // Başarılı mesajı göster
          alert("Değişiklikler başarıyla kaydedildi.");
          emit("close");
        }
      } catch (error) {
        console.error("Kaydetme hatası:", error);
        alert(
          "Değişiklikler kaydedilirken bir hata oluştu: " +
            (error.response?.data?.error || error.message)
        );
      }
    };

    // Tarih formatını düzenleme
    const formatDate = (date) => {
      return date
        ? new Date(date).toLocaleDateString("tr-TR")
        : "Belirtilmemiş";
    };

    // Zaman formatını düzenleme
    const formatTime = (date) => {
      return date
        ? new Date(date).toLocaleTimeString("tr-TR")
        : "Belirtilmemiş";
    };

    // Durum rengini belirleme
    const getStatusClass = (status) => {
      const statusClasses = {
        BEKLEMEDE: "bg-yellow-100 text-yellow-800",
        ONAYLANDI: "bg-green-100 text-green-800",
        REDDEDILDI: "bg-red-100 text-red-800",
      };
      return `px-2 py-1 rounded-full text-xs ${
        statusClasses[status] || "bg-gray-100 text-gray-800"
      }`;
    };

    // Belge adını çevirme
    const getBelgeAdi = (key) => {
      const belgeAdlari = {
        KONTRAT: "Kontrat",
        OLUM_BELGESI: "Ölüm Belgesi",
        VUKUATLI_NUFUS: "Vukuatlı Nüfus Kayıt Örneği",
        OGRENCI_BELGESI: "Öğrenci Belgesi",
        BANKA_EKSTRESI: "Banka Ekstresi",
        TEMVIYYE: "Temviyye Belgesi",
      };
      return belgeAdlari[key] || key;
    };

    // Resim dosyası kontrolü
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

    // Resim önizleme
    const openImagePreview = (imageUrl) => {
      console.log("Resim önizleme açılıyor:", imageUrl);
      selectedImage.value = imageUrl;
    };

    // Belge silme fonksiyonu
    const deleteBelge = async (belgeTuru) => {
      if (confirm("Bu belgeyi silmek istediğinizden emin misiniz?")) {
        try {
          await apiService.deleteBelge(
            props.dosya.dosya_no,
            belgeTuru.toUpperCase()
          );
          dosyaBelgeleri.value[belgeTuru] = null;
        } catch (error) {
          console.error("Belge silme hatası:", error);
          alert("Belge silinirken bir hata oluştu.");
        }
      }
    };

    // Bileşen yüklendiğinde
    onMounted(async () => {
      await reloadDosyaDetails();
      loadFamilyMembers();
      loadDosyaBelgeleri();
      loadDurumDegisiklikleri();
    });

    return {
      yeniDurum,
      guncellemeTarihi,
      aciklamaNotu,
      familyMembers,
      dosyaBelgeleri,
      selectedImage,
      currentProfileImage,
      durumDegisiklikleri,
      yakinlikTurleri,
      saveChanges,
      formatDate,
      formatTime,
      getStatusClass,
      getBelgeAdi,
      isImageFile,
      openImagePreview,
      deleteBelge,
      getProfileImageUrl,
      DURUM_CHOICES,
      UYRUK_CHOICES,
      kiraDurumuSecenekleri,
      cinsiyetSecenekleri,
      yakinlikSecenekleri,
    };
  },
};
</script>
