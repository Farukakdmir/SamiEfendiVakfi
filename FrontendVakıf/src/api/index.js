import axios from "axios";

const apiService = {
  // Dosya İşlemleri
  getDosyalar(page = 1, pageSize = 10, params = {}) {
    return axios.get("/api/dosyalar/", {
      params: { page, page_size: pageSize, ...params },
    });
  },

  getDosya(id) {
    return axios.get(`/api/dosyalar/${id}/`);
  },

  createDosya(data) {
    return axios.post("/api/dosyalar/", data);
  },

  updateDosya(id, data) {
    return axios.put(`/api/dosyalar/${id}/`, data);
  },

  deleteDosya(id) {
    return axios.delete(`/api/dosyalar/${id}/`);
  },

  // Maddi Yardım İşlemleri
  getMaddiYardimlar(params = {}) {
    return axios.get("/api/maddi-yardimlar/", { params });
  },

  getMaddiYardim(id) {
    return axios.get(`/api/maddi-yardimlar/${id}/`);
  },

  createMaddiYardim(data) {
    return axios.post("/api/maddi-yardimlar/", data);
  },

  updateMaddiYardim(id, data) {
    return axios.patch(`/api/maddi-yardimlar/${id}/`, data);
  },

  deleteMaddiYardim(id) {
    return axios.delete(`/api/maddi-yardimlar/${id}/`);
  },

  getMaddiYardimYears() {
    return axios.get("/api/maddi-yardimlar/years/");
  },
};

export default apiService;
