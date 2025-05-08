import { defineStore } from "pinia";

export const useNavbarStore = defineStore("navbar", {
  state: () => ({
    isOpen: true,
  }),
  actions: {
    toggle() {
      this.isOpen = !this.isOpen;
    },
    setOpen(value) {
      this.isOpen = value;
    },
  },
  persist: true,
});
