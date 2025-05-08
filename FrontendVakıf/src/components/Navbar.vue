<!-- src/components/Navbar.vue -->
<template>
  <div>
    <!-- Toggle Button -->
    <button
      @click="toggleNavbar"
      :class="[
        'fixed top-4 z-50 p-2 bg-emerald-800 text-white rounded-lg hover:bg-emerald-900 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105',
        isOpen ? 'left-[248px]' : 'left-4',
      ]"
      v-if="!isModalOpen"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-5 w-5 transform transition-transform duration-300"
        :class="{ 'rotate-180': isOpen }"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 5l7 7-7 7"
        />
      </svg>
    </button>

    <!-- Navbar -->
    <nav
      :class="[
        'fixed top-0 left-0 h-full bg-emerald-800 shadow-lg z-40 transition-all duration-300',
        isOpen ? 'w-64' : 'w-0',
      ]"
    >
      <div class="flex flex-col h-full">
        <div class="p-4 border-b border-emerald-900">
          <div class="flex items-center justify-center">
            <div
              class="bg-white p-2 rounded-lg transform transition-transform duration-300 hover:scale-105"
            >
              <img src="../assets/logo.png" alt="Logo" class="h-12 w-auto" />
            </div>
          </div>
        </div>
        <div class="flex-1">
          <ul class="py-4">
            <li>
              <router-link
                to="/"
                exact
                class="flex items-center px-6 py-3 text-white hover:bg-emerald-900 transition-all duration-200 transform hover:translate-x-2 hover:shadow-md active:bg-emerald-950"
                active-class="bg-emerald-950 shadow-md"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5 mr-3 transform transition-transform duration-200 group-hover:scale-110"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                  />
                </svg>
                Ana Sayfa
              </router-link>
            </li>
            <li>
              <router-link
                to="/files"
                class="flex items-center px-6 py-3 text-white hover:bg-emerald-900 transition-all duration-200 transform hover:translate-x-2 hover:shadow-md active:bg-emerald-950"
                active-class="bg-emerald-950 shadow-md"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5 mr-3 transform transition-transform duration-200 group-hover:scale-110"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                Dosya Kayıtları
              </router-link>
            </li>
            <li>
              <router-link
                to="/maddi-yardim"
                class="flex items-center px-6 py-3 text-white hover:bg-emerald-900 transition-all duration-200 transform hover:translate-x-2 hover:shadow-md active:bg-emerald-950"
                active-class="bg-emerald-950 shadow-md"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5 mr-3 transform transition-transform duration-200 group-hover:scale-110"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                Maddi Yardım
              </router-link>
            </li>
            <li>
              <router-link
                to="/sahsi-yardim"
                class="flex items-center px-6 py-3 text-white hover:bg-emerald-900 transition-all duration-200 transform hover:translate-x-2 hover:shadow-md active:bg-emerald-950"
                active-class="bg-emerald-950 shadow-md"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5 mr-3 transform transition-transform duration-200 group-hover:scale-110"
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
                Şahsi Yardım
              </router-link>
            </li>
          </ul>
        </div>
        <div class="p-4 border-t border-emerald-900">
          <div class="flex items-center">
            <div class="flex-1">
              <p class="text-sm font-medium text-white">{{ username }}</p>
              <p class="text-xs text-emerald-100">Yönetici</p>
            </div>
            <button
              @click="logout"
              class="p-2 text-white hover:bg-emerald-900 rounded-lg transition-all duration-200 transform hover:scale-110 hover:shadow-md"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useNavbarStore } from "../store/navbar";

export default {
  name: "Navbar",
  setup() {
    const router = useRouter();
    const username = ref(localStorage.getItem("username") || "");
    const navbarStore = useNavbarStore();
    const isOpen = ref(navbarStore.isOpen);
    const isModalOpen = computed(() => {
      // Modalların açık olup olmadığını kontrol et
      return (
        document.querySelector(".fixed.inset-0.bg-gray-600") !== null ||
        document.querySelector(".fixed.inset-0.bg-gray-600.bg-opacity-50") !==
          null
      );
    });

    const toggleNavbar = () => {
      navbarStore.toggle();
      isOpen.value = navbarStore.isOpen;
    };

    const logout = () => {
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      router.push("/login");
    };

    return {
      username,
      logout,
      isOpen,
      toggleNavbar,
      isModalOpen,
    };
  },
};
</script>

<style scoped>
nav {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-x: hidden;
}

ul {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

ul::-webkit-scrollbar {
  width: 6px;
}

ul::-webkit-scrollbar-track {
  background: transparent;
}

ul::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 6px;
}
</style>
