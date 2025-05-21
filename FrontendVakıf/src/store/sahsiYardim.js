import { defineStore } from "pinia";
import apiService from "../api";

export const useSahsiYardimStore = defineStore("sahsiYardim", {
  state: () => ({
    yardimlar: [],
    isLoading: false,
    error: null,
    lastFetch: null,
  }),

  getters: {
    getYardimByDosyaNo: (state) => (dosyaNo) => {
      return state.yardimlar.find(
        (yardim) =>
          yardim.dosyalar && yardim.dosyalar.some((d) => d.id === dosyaNo)
      );
    },
  },

  actions: {
    async fetchYardimlar() {
      // Eğer son 5 dakika içinde veri çekildiyse ve veriler varsa, tekrar çekme
      const now = new Date().getTime();
      if (
        this.lastFetch &&
        now - this.lastFetch < 5 * 60 * 1000 &&
        this.yardimlar.length > 0
      ) {
        return;
      }

      try {
        this.isLoading = true;
        this.error = null;
        const response = await apiService.getSahsiYardimlar();
        this.yardimlar = response.data.results || response.data;
        this.lastFetch = now;
      } catch (error) {
        console.error("Şahsi yardımlar yüklenirken hata:", error);
        this.error = error.message;
      } finally {
        this.isLoading = false;
      }
    },

    // Yardım eklendiğinde veya güncellendiğinde store'u güncelle
    updateYardimlar() {
      this.lastFetch = null; // Son fetch zamanını sıfırla
      this.fetchYardimlar(); // Verileri yeniden çek
    },
  },
});
