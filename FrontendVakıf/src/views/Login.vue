<!-- /Login.vue -->
<template>
  <div
    class="min-h-screen flex items-center justify-center bg-green-50 py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-lg shadow-xl">
      <div class="flex justify-center">
        <img src="../assets/logo.png" alt="Sami Efendi Vakfı" class="h-20" />
      </div>
      <form class="mt-8 space-y-8" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="username" class="sr-only">Kullanıcı Adı</label>
            <input
              id="username"
              v-model="username"
              type="text"
              required
              class="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 text-lg"
              placeholder="Kullanıcı Adı"
            />
          </div>
          <div class="relative">
            <label for="password" class="sr-only">Şifre</label>
            <div class="relative">
              <input
                id="password"
                v-model="password"
                type="password"
                required
                class="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 text-lg"
                placeholder="Şifre"
              />
            </div>
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-lg font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            :disabled="loading"
          >
            <span v-if="loading">Giriş yapılıyor...</span>
            <span v-else>Giriş Yap</span>
          </button>
        </div>
      </form>

      <div v-if="error" class="mt-4 text-center text-red-600">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import apiService from "../api";

// State tanımlamaları
const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);
const router = useRouter();

// Login işlemi
const handleLogin = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await apiService.login({
      username: username.value,
      password: password.value,
    });

    console.log("Login response:", response.data);

    // Yeni API yanıt formatına göre güncellendi
    if (response.data.access) {
      // Token ve kullanıcı bilgilerini kaydet
      localStorage.setItem("token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);

      if (response.data.user) {
        localStorage.setItem("user", JSON.stringify(response.data.user));
        localStorage.setItem(
          "username",
          response.data.user.username || username.value
        );
      }

      console.log("Giriş başarılı, ana sayfaya yönlendiriliyor...");

      // Ana sayfaya yönlendir
      await router.push("/home");
    } else {
      error.value = "Sunucudan geçersiz yanıt alındı.";
    }
  } catch (err) {
    console.error("Login error:", err);
    error.value = "Giriş başarısız. Lütfen bilgilerinizi kontrol edin.";
  } finally {
    loading.value = false;
  }
};
</script>
