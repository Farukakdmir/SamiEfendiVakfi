// apiService.js
import axios from "axios";
import router from "./router";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
  withCredentials: true, // CORS için önemli
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Sunucudan gelen hata yanıtı
      console.error("Hata Kodu:", error.response.status);
      console.error("Hata Detayları:", error.response.data);

      if (error.response.status === 401) {
        // Token geçersiz veya süresi dolmuş
        localStorage.removeItem("token");
        router.push("/login");
      }
    } else if (error.request) {
      // İstek yapıldı ama yanıt alınamadı
      console.error("Sunucu yanıt vermedi:", error.request);
    } else {
      // İstek oluşturulurken hata oluştu
      console.error("İstek hatası:", error.message);
    }
    return Promise.reject(error);
  }
);

const refreshToken = async () => {
  try {
    const response = await api.post("/token/refresh/", {
      refresh: localStorage.getItem("refresh_token"),
    });
    return response.data.access;
  } catch (error) {
    throw error;
  }
};

const handleLogout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
  router.push("/login");
  console.error("Oturumunuzun süresi doldu. Lütfen tekrar giriş yapın.");
};

const handleErrorResponse = (error) => {
  if (!error) {
    console.error("Bilinmeyen bir hata oluştu");
    return;
  }

  try {
    if (error.response) {
      const status = error.response.status;
      console.error(`Hata Kodu: ${status}`);
      if (error.response.data) {
        console.error("Hata Detayları:", JSON.stringify(error.response.data));
      }
    } else if (error.request) {
      console.error("Sunucuya istek gönderilemedi");
    } else {
      console.error("Hata:", error.message || "Bilinmeyen bir hata oluştu");
    }
  } catch (logError) {
    console.error("Hata loglaması sırasında bir sorun oluştu", logError);
  }
};

const apiService = {
  // Endpoints
  endpoints: {
    auth: {
      login: "/auth/login/",
      logout: "/auth/logout/",
      register: "/auth/register/",
      refreshToken: "/auth/token/refresh/",
    },
    dosyalar: {
      base: "/dosyalar/",
      stats: "/dosyalar/stats/",
      updateStatus: (dosyaNo) => `/dosyalar/${dosyaNo}/update_status/`,
      restore: "/dosyalar/restore/",
      update: (dosyaNo) => `/dosyalar/${dosyaNo}/`,
    },
    aileBilgileri: "/aile-bilgileri/",
    belgeler: "/belgeler/",
    dosyaBelgeleri: "/dosya-belgeleri/",
    deletedDosyalar: "/deleted-dosyalar/",
    maddiYardim: {
      base: "/maddi-yardimlar/",
    },
    durumDegisiklikleri: "/durum-degisiklikleri/",
    sahsiYardim: {
      base: "/sahsi-yardim/",
    },
  },

  // Kimlik Doğrulama
  login: (credentials) =>
    api.post(apiService.endpoints.auth.login, credentials),
  logout: () => api.post(apiService.endpoints.auth.logout),
  register: (userData) =>
    api.post(apiService.endpoints.auth.register, userData),

  // Genel HTTP metodları
  get: (url, config = {}) => api.get(url, config),
  post: (url, data, config = {}) => api.post(url, data, config),
  put: (url, data, config = {}) => api.put(url, data, config),
  patch: (url, data, config = {}) => api.patch(url, data, config),
  delete: (url, config = {}) => api.delete(url, config),

  // Dosya İşlemleri
  getDosyalar: (page = 1, pageSize = 10, filters = {}) => {
    const params = {
      page,
      page_size: pageSize,
      ...filters,
    };
    return api.get(apiService.endpoints.dosyalar.base, { params });
  },
  getAllDosyalar: () => api.get(`${apiService.endpoints.dosyalar.base}all/`),
  getDeletedDosyalar: () => api.get(apiService.endpoints.deletedDosyalar),
  getDosya: (id) => api.get(`${apiService.endpoints.dosyalar.base}${id}/`),
  createDosya: async (formData) => {
    try {
      const response = await api.post(
        apiService.endpoints.dosyalar.base,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      return response;
    } catch (error) {
      handleErrorResponse(error);
      throw error;
    }
  },

  // Dosya güncelleme
  updateDosya: async (dosyaNo, formData) => {
    try {
      // FormData mı yoksa JSON objesi mi olduğunu kontrol et
      let requestData = formData;
      let headers = {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      };

      // FormData türündeyse multipart/form-data, değilse application/json
      if (formData instanceof FormData) {
        headers["Content-Type"] = "multipart/form-data";
      } else {
        headers["Content-Type"] = "application/json";
        // Eğer normal obje ise, API'ye gönderilecek şekilde dönüştür
        requestData = { ...formData };
      }

      const response = await api.put(
        apiService.endpoints.dosyalar.update(dosyaNo),
        requestData,
        { headers }
      );
      return response;
    } catch (error) {
      handleErrorResponse(error);
      throw error;
    }
  },

  deleteDosya: async (dosyaNo) => {
    try {
      await api.delete(`${apiService.endpoints.dosyalar.base}${dosyaNo}/`);
      return true;
    } catch (error) {
      handleErrorResponse(error);
      throw error;
    }
  },

  // Dosya Durum Güncelleme
  updateDosyaDurum: (dosyaNo, durumData) =>
    api.patch(apiService.endpoints.dosyalar.updateStatus(dosyaNo), durumData),

  // Durum Değişiklikleri
  getDurumDegisiklikleri: (dosyaNo) =>
    api.get(
      apiService.endpoints.dosyalar.base + `${dosyaNo}/durum_degisiklikleri/`
    ),

  // İstatistikler
  getDosyaStats: async () => {
    try {
      const response = await api.get(apiService.endpoints.dosyalar.stats);
      return response;
    } catch (error) {
      console.error("İstatistikler alınırken hata oluştu:", error);
      throw error;
    }
  },

  // Aile Bilgileri
  getFamilyMembers: (dosyaId) =>
    api.get(apiService.endpoints.aileBilgileri, {
      params: { dosya: dosyaId },
    }),
  getAileBilgileri: (dosyaId) =>
    api.get(apiService.endpoints.aileBilgileri, { params: { dosya: dosyaId } }),
  createAileBilgisi: (data) =>
    api.post(apiService.endpoints.aileBilgileri, data),
  updateAileBilgisi: (id, data) =>
    api.patch(`${apiService.endpoints.aileBilgileri}${id}/`, data),
  deleteAileBilgisi: (id) =>
    api.delete(`${apiService.endpoints.aileBilgileri}${id}/`),

  // Belge İşlemleri
  getBelgeler: (dosyaNo) =>
    api.get(`${apiService.endpoints.belgeler}?dosya=${dosyaNo}`),
  uploadBelge: (dosyaNo, formData) => {
    const url = `${apiService.endpoints.dosyalar.base}${dosyaNo}/upload_belge/`;
    return api.post(url, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
  deleteBelge: (dosyaNo, belgeTuru) =>
    api.delete(`${apiService.endpoints.belgeler}delete_belge/`, {
      params: {
        dosya: dosyaNo,
        belge_turu: belgeTuru,
      },
    }),

  // Dosya Arama
  searchDosyalar: (query) => {
    return api.get(`${apiService.endpoints.dosyalar.base}`, {
      params: {
        search: query,
        page_size: 10000, // Tüm sonuçları getir
      },
    });
  },

  // Maddi Yardım API'leri
  getMaddiYardimlar: (params) =>
    api.get(apiService.endpoints.maddiYardim.base, { params }),
  getMaddiYardim: (id) =>
    api.get(`${apiService.endpoints.maddiYardim.base}${id}/`),
  createMaddiYardim: (data) =>
    api.post(apiService.endpoints.maddiYardim.base, data),
  updateMaddiYardim: (id, data) =>
    api.put(`${apiService.endpoints.maddiYardim.base}${id}/`, data),
  deleteMaddiYardim: (id) =>
    api.delete(`${apiService.endpoints.maddiYardim.base}${id}/`),

  // Son İşlemler
  getSonIslemler: async () => {
    try {
      const sonIslemler = [];

      // Maddi yardımları getir
      const yardimResponse = await api.get(
        apiService.endpoints.maddiYardim.base
      );
      const yardimlar = yardimResponse.data.results || yardimResponse.data;

      // Maddi yardımları son işlemlere ekle
      yardimlar.forEach((yardim) => {
        sonIslemler.push({
          id: `yardim_${yardim.id}`,
          islem_turu: "Maddi Yardım",
          ad_soyad: yardim.yardim_yapan_ad_soyad,
          tutar: yardim.yardim_tutar,
          tarih: yardim.created_at,
          durum: "Onaylandı",
        });
      });

      // Şahsi yardımları getir
      const sahsiYardimResponse = await api.get(
        apiService.endpoints.sahsiYardim.base
      );
      const sahsiYardimlar =
        sahsiYardimResponse.data.results || sahsiYardimResponse.data;

      // Şahsi yardımları son işlemlere ekle
      sahsiYardimlar.forEach((yardim) => {
        sonIslemler.push({
          id: `sahsi_${yardim.id}`,
          islem_turu: "Şahsi Yardım",
          ad_soyad: yardim.ad_soyad,
          tutar: null,
          tarih: yardim.created_at,
          durum: "Onaylandı",
        });
      });

      // Aktif dosyaları getir
      const dosyaResponse = await api.get(apiService.endpoints.dosyalar.base);
      const dosyalar = dosyaResponse.data.results || dosyaResponse.data;

      // Dosya kayıtlarını son işlemlere ekle
      dosyalar.forEach((dosya) => {
        sonIslemler.push({
          id: `dosya_${dosya.id}`,
          islem_turu: "Dosya Kayıt",
          dosya_no: dosya.dosya_no,
          ad_soyad: dosya.ad_soyad,
          tutar: null,
          tarih: dosya.created_at,
          durum: dosya.durum,
        });
      });

      // Silinen dosyaları getir
      const silinenDosyaResponse = await api.get(
        apiService.endpoints.deletedDosyalar
      );
      const silinenDosyalar =
        silinenDosyaResponse.data.results || silinenDosyaResponse.data;

      // Silinen dosyaları son işlemlere ekle
      silinenDosyalar.forEach((dosya) => {
        sonIslemler.push({
          id: `silinen_${dosya.id}`,
          islem_turu: "Dosya Silme",
          dosya_no: dosya.dosya_no,
          ad_soyad: dosya.ad_soyad,
          tutar: null,
          tarih: dosya.deleted_at || dosya.updated_at,
          durum: "Silindi",
        });
      });

      // Durum değişikliklerini getir
      const durumDegisiklikleriResponse = await api.get(
        apiService.endpoints.durumDegisiklikleri
      );
      const durumDegisiklikleri =
        durumDegisiklikleriResponse.data.results ||
        durumDegisiklikleriResponse.data;

      // Durum değişikliklerini son işlemlere ekle
      durumDegisiklikleri.forEach((degisiklik) => {
        sonIslemler.push({
          id: `durum_${degisiklik.id}`,
          islem_turu: "Durum Değişikliği",
          ad_soyad: degisiklik.degistiren_ad_soyad,
          tutar: null,
          tarih: degisiklik.tarih,
          durum: degisiklik.yeni_durum,
        });
      });

      // Tarihe göre sırala (en yeniden en eskiye)
      sonIslemler.sort((a, b) => new Date(b.tarih) - new Date(a.tarih));

      return { data: sonIslemler };
    } catch (error) {
      console.error("Son işlemler alınırken hata oluştu:", error);
      throw error;
    }
  },

  // Şahsi Yardım API'leri
  getSahsiYardimlar: (params = {}) => {
    const queryParams = {
      page: params.page || 1,
      page_size: params.page_size || 10,
      search: params.search || "",
      ordering: params.ordering || "-created_at",
    };
    return api.get(apiService.endpoints.sahsiYardim.base, {
      params: queryParams,
    });
  },
  getSahsiYardim: (id) =>
    api.get(`${apiService.endpoints.sahsiYardim.base}${id}/`),
  createSahsiYardim: (data) => {
    const formData = {
      yardim_tipi: data.yardim_tipi,
      ad_soyad: data.ad_soyad,
      telefon: data.telefon,
      grup_uye_sayisi: data.grup_uye_sayisi,
      yardimcilar: data.yardimcilar,
      dosyalar: data.dosyalar,
    };
    return api.post(apiService.endpoints.sahsiYardim.base, formData);
  },
  updateSahsiYardim: (id, data) => {
    const formData = {
      yardim_tipi: data.yardim_tipi,
      ad_soyad: data.ad_soyad,
      telefon: data.telefon,
      grup_uye_sayisi: data.grup_uye_sayisi,
      yardimcilar: data.yardimcilar,
      dosyalar: data.dosyalar,
    };
    return api.put(`${apiService.endpoints.sahsiYardim.base}${id}/`, formData);
  },
  deleteSahsiYardim: (id) =>
    api.delete(`${apiService.endpoints.sahsiYardim.base}${id}/`),

  // Yardım Tipleri
  getYardimTipleri: () => api.get("/dosyalar/yardim_tipleri/"),
};

export default apiService;
