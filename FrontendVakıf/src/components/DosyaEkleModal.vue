<template>
  <v-dialog
    :model-value="showModal"
    @update:model-value="$emit('update:showModal', $event)"
    max-width="1200px"
    transition="dialog-bottom-transition"
  >
    <v-card class="rounded-lg">
      <v-card-title class="text-h5 bg-emerald-800 text-white pa-4">
        <v-icon start icon="mdi-plus" class="mr-2"></v-icon>
        {{ editMode ? "Dosya Düzenle" : "Yeni Dosya Ekle" }}
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form ref="form" v-model="valid">
          <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
            <div class="grid grid-cols-4 gap-4 bg-grey-lighten-4 p-4 rounded">
              <!-- Profil Resmi Bölümü -->
              <div class="col-span-4 mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2"
                  >Profil Resmi</label
                >
                <div class="flex flex-col items-center space-y-4">
                  <div
                    v-if="formData.profil_resmi_preview"
                    class="relative w-40 h-40"
                  >
                    <img
                      :src="formData.profil_resmi_preview"
                      class="w-40 h-40 object-cover rounded-lg"
                      alt="Profil Resmi"
                    />
                    <button
                      @click="removeProfileImage"
                      class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 focus:outline-none"
                    >
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                  <div class="flex space-x-4">
                    <v-btn
                      color="primary"
                      variant="outlined"
                      @click="$refs.fileInput.click()"
                      prepend-icon="mdi-upload"
                      size="large"
                    >
                      Dosyadan Yükle
                    </v-btn>
                    <v-btn
                      color="primary"
                      variant="outlined"
                      @click="startCamera"
                      prepend-icon="mdi-camera"
                      size="large"
                    >
                      Kameradan Çek
                    </v-btn>
                  </div>
                  <input
                    type="file"
                    accept="image/jpeg,image/jpg,image/png"
                    @change="handleProfileImageChange"
                    class="hidden"
                    ref="fileInput"
                  />
                </div>
              </div>

              <!-- Temel Bilgiler -->
              <v-col cols="12" md="6" v-if="editMode">
                <v-text-field
                  v-model="formData.dosya_no"
                  label="Dosya No"
                  variant="outlined"
                  readonly
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.kayit_tarihi"
                  label="Kayıt Tarihi"
                  type="date"
                  variant="outlined"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.ad"
                  label="Ad"
                  variant="outlined"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.soyad"
                  label="Soyad"
                  variant="outlined"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.kimlik_no"
                  label="Kimlik No"
                  variant="outlined"
                  required
                  pattern="[0-9]*"
                  inputmode="numeric"
                  @input="handleKimlikNoInput"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-select
                  v-model="formData.uyruk"
                  :items="UYRUK_CHOICES"
                  item-title="label"
                  item-value="value"
                  label="Uyruk"
                  variant="outlined"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.telefon"
                  label="Telefon"
                  variant="outlined"
                  required
                  pattern="[0-9]*"
                  inputmode="numeric"
                  maxlength="11"
                  @input="handleTelefonInput"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.ilce"
                  label="İlçe"
                  variant="outlined"
                  value="YeniMahalle"
                  readonly
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.mahalle"
                  label="Mahalle"
                  variant="outlined"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.cadde_sokak"
                  label="Cadde/Sokak"
                  variant="outlined"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.bina_no"
                  label="Bina No"
                  variant="outlined"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.daire_no"
                  label="Daire No"
                  variant="outlined"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-select
                  v-model="formData.kira_durumu"
                  :items="[
                    { title: 'Ev Sahibi', value: 'EV_SAHIBI' },
                    { title: 'Kiracı', value: 'KIRACI' },
                  ]"
                  label="Kira Durumu"
                  variant="outlined"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.gelir_durumu"
                  label="Gelir Durumu (TL)"
                  type="number"
                  variant="outlined"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.dolduran_kisi"
                  label="Dolduran Kişi"
                  variant="outlined"
                  readonly
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.iban"
                  label="IBAN"
                  variant="outlined"
                  required
                  @input="handleIbanInput"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="10">
                <v-text-field
                  v-model="formData.yardim_aldigi_yerler"
                  label="Yardım Aldığı Yerler"
                  variant="outlined"
                  required
                ></v-text-field>
              </v-col>
            </div>

            <!-- İstenen Belgeler -->
            <div class="mt-6">
              <v-card class="mb-4 rounded-lg" elevation="1">
                <v-card-title class="bg-grey-lighten-4">
                  <v-icon start icon="mdi-file-document" class="mr-2"></v-icon>
                  İstenen Belgeler
                </v-card-title>
                <v-card-text>
                  <div class="grid grid-cols-2 gap-6">
                    <div
                      v-for="(belgeType, index) in Object.keys(
                        formData.belgeler
                      )"
                      :key="index"
                      class="bg-grey-lighten-4 p-4 rounded-lg border border-grey-lighten-2 hover:border-primary transition-all duration-200"
                    >
                      <div class="flex items-center justify-between mb-2">
                        <label class="block text-gray-700 font-bold">
                          {{ getBelgeLabel(belgeType) }}
                        </label>
                        <div class="flex items-center space-x-2">
                          <v-btn
                            color="primary"
                            variant="text"
                            @click="triggerFileInput(belgeType)"
                            size="small"
                          >
                            <v-icon start icon="mdi-upload"></v-icon>
                            Yükle
                          </v-btn>
                          <input
                            type="file"
                            :ref="(el) => (fileInputs[belgeType] = el)"
                            @change="handleFileUpload($event, belgeType)"
                            class="hidden"
                            accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                            multiple
                          />
                        </div>
                      </div>
                      <p class="text-sm text-gray-600 mb-3">
                        {{ getBelgeAciklama(belgeType) }}
                      </p>
                      <div
                        v-if="formData.belgeler[belgeType]?.length"
                        class="space-y-2"
                      >
                        <div
                          v-for="(file, fileIndex) in formData.belgeler[
                            belgeType
                          ]"
                          :key="fileIndex"
                          class="flex items-center justify-between bg-white p-2 rounded border"
                        >
                          <div class="flex items-center space-x-2">
                            <span class="text-sm text-gray-700 truncate">{{
                              file.name
                            }}</span>
                            <div class="flex space-x-2">
                              <v-btn
                                v-if="file.url && isImageFile(file.name)"
                                @click="showPreview(file.url)"
                                color="primary"
                                variant="text"
                                size="small"
                                icon="mdi-eye"
                              ></v-btn>
                              <v-btn
                                v-if="file.url"
                                :href="file.url"
                                target="_blank"
                                color="primary"
                                variant="text"
                                size="small"
                                icon="mdi-download"
                              ></v-btn>
                            </div>
                          </div>
                          <v-btn
                            color="error"
                            variant="text"
                            size="small"
                            icon="mdi-delete"
                            @click="removeFile(belgeType, fileIndex)"
                          ></v-btn>
                        </div>
                      </div>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </div>

            <!-- Aile Bilgileri -->
            <div class="mt-6">
              <v-card class="mb-4 rounded-lg" elevation="1">
                <v-card-title class="bg-grey-lighten-4">
                  <v-icon start icon="mdi-account-group" class="mr-2"></v-icon>
                  Aile Bilgileri
                </v-card-title>
                <v-card-text>
                  <div
                    v-for="(member, index) in formData.aile_bilgileri"
                    :key="index"
                    class="mb-4 p-4 border rounded-lg bg-grey-lighten-4"
                  >
                    <div class="flex justify-between items-center mb-4">
                      <h4 class="text-lg font-semibold">
                        Aile Üyesi {{ index + 1 }}
                      </h4>
                      <v-btn
                        color="error"
                        variant="text"
                        size="small"
                        @click="removeFamilyMember(index)"
                        prepend-icon="mdi-delete"
                      >
                        Kaldır
                      </v-btn>
                    </div>
                    <v-row>
                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="member.ad"
                          label="Ad"
                          variant="outlined"
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="member.soyad"
                          label="Soyad"
                          variant="outlined"
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="member.kimlik_no"
                          label="Kimlik No"
                          variant="outlined"
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="4">
                        <v-select
                          v-model="member.yakinlik"
                          :items="[
                            { title: 'Kendisi', value: 'KENDISI' },
                            { title: 'Eş', value: 'ES' },
                            { title: 'Çocuk', value: 'COCUK' },
                            { title: 'Anne', value: 'ANNE' },
                            { title: 'Baba', value: 'BABA' },
                            { title: 'Kardeş', value: 'KARDES' },
                            { title: 'Diğer', value: 'DIGER' },
                          ]"
                          label="Yakınlık"
                          variant="outlined"
                          required
                        ></v-select>
                      </v-col>
                      <v-col cols="12" md="4">
                        <v-select
                          v-model="member.cinsiyet"
                          :items="[
                            { title: 'Erkek', value: 'E' },
                            { title: 'Kadın', value: 'K' },
                          ]"
                          label="Cinsiyet"
                          variant="outlined"
                          required
                        ></v-select>
                      </v-col>
                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="member.dogum_tarihi"
                          label="Doğum Tarihi"
                          type="date"
                          variant="outlined"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="12">
                        <v-checkbox
                          v-model="member.engel_durumu"
                          label="Engel Durumu"
                          color="primary"
                        ></v-checkbox>
                        <v-expand-transition>
                          <div v-if="member.engel_durumu">
                            <v-textarea
                              v-model="member.engel_aciklama"
                              label="Engel Açıklaması"
                              variant="outlined"
                              rows="2"
                              placeholder="Engel durumu hakkında detaylı açıklama..."
                            ></v-textarea>
                          </div>
                        </v-expand-transition>
                      </v-col>
                    </v-row>
                  </div>
                  <v-btn
                    color="success"
                    @click="addFamilyMember"
                    prepend-icon="mdi-plus"
                    class="mt-4"
                  >
                    Aile Üyesi Ekle
                  </v-btn>
                </v-card-text>
              </v-card>
            </div>
          </div>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4 bg-grey-lighten-4">
        <v-spacer></v-spacer>
        <v-btn
          color="error"
          variant="outlined"
          @click="$emit('close')"
          class="mr-2"
        >
          <v-icon start icon="mdi-close"></v-icon>
          İptal
        </v-btn>
        <v-btn
          color="primary"
          :loading="loading"
          :disabled="!valid || loading"
          @click="handleSubmit"
        >
          <v-icon start icon="mdi-content-save"></v-icon>
          {{ editMode ? "Güncelle" : "Kaydet" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Kamera Modal -->
  <v-dialog v-model="showCamera" max-width="600px">
    <v-card>
      <v-card-title class="text-h5 bg-emerald-800 text-white pa-4">
        <v-icon start icon="mdi-camera" class="mr-2"></v-icon>
        Fotoğraf Çek
      </v-card-title>
      <v-card-text class="pa-4">
        <div class="relative">
          <video
            ref="videoRef"
            class="w-full rounded-lg"
            autoplay
            playsinline
          ></video>
          <canvas ref="canvasRef" class="hidden"></canvas>
        </div>
      </v-card-text>
      <v-card-actions class="pa-4 bg-grey-lighten-4">
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="capturePhoto" prepend-icon="mdi-camera">
          Fotoğraf Çek
        </v-btn>
        <v-btn
          color="error"
          variant="outlined"
          @click="closeCamera"
          class="ml-2"
        >
          İptal
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Resim Önizleme Modal -->
  <v-dialog v-model="previewImage" max-width="800px">
    <v-card>
      <v-card-title class="text-h5 bg-emerald-800 text-white pa-4">
        <v-icon start icon="mdi-image" class="mr-2"></v-icon>
        Belge Önizleme
      </v-card-title>
      <v-card-text class="pa-4">
        <div class="relative">
          <img
            :src="previewImage"
            class="max-h-[80vh] w-auto mx-auto"
            alt="Belge Önizleme"
          />
        </div>
      </v-card-text>
      <v-card-actions class="pa-4 bg-grey-lighten-4">
        <v-spacer></v-spacer>
        <v-btn color="error" variant="outlined" @click="closePreview">
          Kapat
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, onMounted, nextTick, watch } from "vue";
import apiService from "../api";
import { UYRUK_CHOICES } from "../constants";

export default {
  name: "DosyaEkleModal",
  props: {
    showModal: {
      type: Boolean,
      required: true,
    },
    editMode: {
      type: Boolean,
      default: false,
    },
    initialData: {
      type: Object,
      default: () => ({}),
    },
  },
  emits: ["close", "saved", "update:showModal"],
  setup(props, { emit }) {
    const username = ref(localStorage.getItem("username") || "");
    const fileInputs = ref({});
    const videoRef = ref(null);
    const canvasRef = ref(null);
    const previewImage = ref(null);

    const valid = ref(false);
    const form = ref(null);
    const loading = ref(false);

    const initialFormData = {
      dosya_no: null,
      kayit_tarihi: new Date().toISOString().split("T")[0],
      ad: "",
      soyad: "",
      kimlik_no: "",
      uyruk: "TURKIYE",
      telefon: "",
      ilce: "Yeni Mahalle",
      mahalle: "",
      cadde_sokak: "",
      bina_no: "",
      daire_no: "",
      kira_durumu: "",
      gelir_durumu: null,
      iban: "",
      yardim_aldigi_yerler: "",
      dolduran_kisi: username.value,
      durum: "BEKLEMEDE",
      aile_bilgileri: [],
      belgeler: {
        KONTRAT: null,
        OLUM_BELGESI: null,
        VUKUATLI_NUFUS: null,
        OGRENCI_BELGESI: null,
        BANKA_EKSTRESI: null,
        TEMVIYYE: null,
      },
      profil_resmi_preview: null,
      profil_resmi_file: null,
    };

    const formData = ref({ ...initialFormData });

    // formData değişince validasyonu tetikle
    watch(
      formData,
      async () => {
        await nextTick();
        if (form.value) {
          form.value.validate();
        }
      },
      { deep: true }
    );

    const getBelgeAciklama = (belgeType) => {
      const aciklamalar = {
        KONTRAT:
          "Lütfen geçerli bir kontrat yükleyin. (PDF, DOC, DOCX, JPEG, PNG, maks. 5MB)",
        OLUM_BELGESI:
          "Lütfen geçerli bir ölüm belgesi yükleyin. (PDF, DOC, DOCX, JPEG, PNG, maks. 5MB)",
        VUKUATLI_NUFUS:
          "Lütfen vukuatlı nüfus kayıt örneğini yükleyin. (PDF, DOC, DOCX, JPEG, PNG, maks. 5MB)",
        OGRENCI_BELGESI:
          "Lütfen öğrenci belgesini yükleyin. (PDF, DOC, DOCX, JPEG, PNG, maks. 5MB)",
        BANKA_EKSTRESI:
          "Lütfen banka tasdikli kredi kartı ekstresini yükleyin. (PDF, DOC, DOCX, JPEG, PNG, maks. 5MB)",
        TEMVIYYE:
          "Lütfen temviyye belgesini yükleyin. (PDF, DOC, DOCX, JPEG, PNG, maks. 5MB)",
      };
      return aciklamalar[belgeType] || "Belge yükleyin";
    };

    const getBelgeLabel = (belgeType) => {
      const labels = {
        KONTRAT: "Kontrat",
        OLUM_BELGESI: "Ölüm Belgesi",
        VUKUATLI_NUFUS: "Vukuatlı Nüfus Kayıt Örneği",
        OGRENCI_BELGESI: "Öğrenci Belgesi",
        BANKA_EKSTRESI: "Banka Tasdikli Kredi Kartı Ekstresi",
        TEMVIYYE: "Temviyye",
      };
      return labels[belgeType] || belgeType;
    };

    const triggerFileInput = (belgeType) => {
      if (fileInputs.value[belgeType]) {
        fileInputs.value[belgeType].click();
      }
    };

    const removeFile = async (belgeType, fileIndex) => {
      if (!formData.value.belgeler[belgeType]) return;

      const file = formData.value.belgeler[belgeType][fileIndex];

      if (file.isExisting) {
        // Eğer mevcut bir belge ise, API üzerinden silme işlemi yap
        try {
          await apiService.deleteBelge(formData.value.dosya_no, belgeType);
          formData.value.belgeler[belgeType].splice(fileIndex, 1);
        } catch (error) {
          console.error("Belge silme hatası:", error);
          alert("Belge silinirken bir hata oluştu.");
        }
      } else {
        // Yeni yüklenmiş bir dosya ise, sadece listeden kaldır
        formData.value.belgeler[belgeType].splice(fileIndex, 1);
      }
    };

    const handleFileUpload = async (event, belgeType) => {
      if (event.target.files.length > 0) {
        const files = Array.from(event.target.files);

        // Dosya boyutu ve format kontrolü
        for (const file of files) {
          if (file.size > 5 * 1024 * 1024) {
            alert("Dosya boyutu 5MB'ı aşamaz.");
            event.target.value = "";
            return;
          }

          const allowedExtensions = [
            ".pdf",
            ".doc",
            ".docx",
            ".jpg",
            ".jpeg",
            ".png",
          ];
          const fileExtension = "." + file.name.split(".").pop().toLowerCase();

          if (!allowedExtensions.includes(fileExtension)) {
            alert(
              "Yalnızca PDF, DOC, DOCX, JPEG ve PNG formatları kabul edilir."
            );
            event.target.value = "";
            return;
          }
        }

        try {
          // Mevcut dosyaları koru ve yeni dosyaları ekle
          if (!formData.value.belgeler[belgeType]) {
            formData.value.belgeler[belgeType] = [];
          }

          // Her bir dosyayı yükle
          for (const file of files) {
            const belgeFormData = new FormData();
            belgeFormData.append("belge_turu", belgeType);
            belgeFormData.append("belge", file);

            if (formData.value.dosya_no) {
              // Mevcut dosya için belge yükleme
              const response = await apiService.uploadBelge(
                formData.value.dosya_no.toString(),
                belgeFormData
              );
              if (response.data) {
                formData.value.belgeler[belgeType].push({
                  name: file.name,
                  url: response.data.belge_url,
                  isExisting: true,
                });
              }
            } else {
              // Yeni dosya için belgeyi geçici olarak sakla
              formData.value.belgeler[belgeType].push(file);
            }
          }

          // Başarılı yükleme mesajı
          alert("Belge(ler) başarıyla yüklendi.");
        } catch (error) {
          console.error("Belge yükleme hatası:", error);
          alert(
            "Belge yüklenirken bir hata oluştu: " +
              (error.response?.data?.detail || error.message)
          );
        }

        event.target.value = "";
      }
    };

    const addFamilyMember = () => {
      formData.value.aile_bilgileri.push({
        ad: "",
        soyad: "",
        kimlik_no: "",
        yakinlik: "DIGER",
        cinsiyet: "E",
        dogum_tarihi: null,
        engel_durumu: false,
        engel_aciklama: "",
      });

      console.log(
        "Added new family member, current members:",
        formData.value.aile_bilgileri
      );
    };

    const removeFamilyMember = (index) => {
      formData.value.aile_bilgileri.splice(index, 1);
    };

    const handleSubmit = async () => {
      try {
        console.log("Form data before submit:", formData.value);

        const formDataToSend = new FormData();

        // Temel bilgileri ekle
        const basicFields = [
          "ad",
          "soyad",
          "kimlik_no",
          "telefon",
          "kayit_tarihi",
          "uyruk",
          "ilce",
          "mahalle",
          "cadde_sokak",
          "bina_no",
          "daire_no",
          "kira_durumu",
          "gelir_durumu",
          "iban",
          "yardim_aldigi_yerler",
          "dolduran_kisi",
          "durum",
        ];

        basicFields.forEach((field) => {
          if (
            formData.value[field] !== null &&
            formData.value[field] !== undefined
          ) {
            formDataToSend.append(field, formData.value[field]);
          }
        });

        // Profil resmini ekle
        if (formData.value.profil_resmi_file) {
          formDataToSend.append(
            "profil_resmi",
            formData.value.profil_resmi_file
          );
        }

        // Aile bilgilerini ekle
        if (
          formData.value.aile_bilgileri &&
          formData.value.aile_bilgileri.length > 0
        ) {
          const processedAileData = formData.value.aile_bilgileri.map(
            (member) => ({
              ...member,
              engel_aciklama: member.engel_aciklama || "",
            })
          );
          formDataToSend.append(
            "aile_bilgileri",
            JSON.stringify(processedAileData)
          );
        }

        // Belgeleri ekle
        Object.entries(formData.value.belgeler).forEach(
          ([belgeType, files]) => {
            if (files && files.length > 0) {
              files.forEach((file) => {
                if (!file.isExisting) {
                  formDataToSend.append(`belgeler_${belgeType}`, file);
                }
              });
            }
          }
        );

        let response;
        if (props.editMode && formData.value.dosya_no) {
          response = await apiService.updateDosya(
            formData.value.dosya_no,
            formDataToSend
          );
        } else {
          response = await apiService.createDosya(formDataToSend);
        }

        if (response.data) {
          alert(
            props.editMode
              ? "Dosya başarıyla güncellendi!"
              : "Dosya başarıyla oluşturuldu!"
          );
          emit("saved");
          emit("close");
        }
      } catch (error) {
        console.error("Dosya kaydetme hatası:", error);
        alert(
          `Hata: ${
            error.response?.data?.error ||
            error.message ||
            "Beklenmeyen bir hata oluştu!"
          }`
        );
      }
    };

    const deleteBelge = async (belgeTuru) => {
      if (confirm("Bu belgeyi silmek istediğinizden emin misiniz?")) {
        try {
          await apiService.deleteBelge(
            formData.value.dosya_no,
            belgeTuru.toUpperCase()
          );
          // Belgeleri güncelle
          const response = await apiService.getBelgeler(
            formData.value.dosya_no
          );
          const belgeler = response.data;
          formData.value.belgeler = belgeler;
        } catch (error) {
          console.error("Belge silme hatası:", error);
          alert("Belge silinirken bir hata oluştu.");
        }
      }
    };

    const handleProfileImageChange = (event) => {
      const file = event.target.files[0];
      if (file) {
        // Dosya boyutu kontrolü (5MB)
        if (file.size > 5 * 1024 * 1024) {
          alert("Dosya boyutu 5MB'ı aşamaz.");
          event.target.value = "";
          return;
        }

        // Dosya tipi kontrolü
        const allowedTypes = ["image/jpeg", "image/png", "image/jpg"];
        if (!allowedTypes.includes(file.type)) {
          alert("Sadece JPEG, JPG ve PNG formatları kabul edilir.");
          event.target.value = "";
          return;
        }

        // Dosyayı FormData için sakla ve önizleme için URL oluştur
        formData.value.profil_resmi_file = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          formData.value.profil_resmi_preview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };

    const removeProfileImage = () => {
      formData.value.profil_resmi_file = null;
      formData.value.profil_resmi_preview = null;
    };

    const showCamera = ref(false);
    const stream = ref(null);

    const startCamera = async () => {
      try {
        const constraints = {
          video: {
            width: { ideal: 1280 },
            height: { ideal: 720 },
            facingMode: "user",
          },
          audio: false,
        };

        stream.value = await navigator.mediaDevices.getUserMedia(constraints);
        showCamera.value = true;
        await nextTick();
        if (videoRef.value) {
          videoRef.value.srcObject = stream.value;
        }
      } catch (error) {
        console.error("Kamera erişim hatası:", error);
        if (error.name === "NotAllowedError") {
          alert(
            "Kamera erişimi reddedildi. Lütfen tarayıcı ayarlarından kamera izinlerini kontrol edin."
          );
        } else if (error.name === "NotFoundError") {
          alert(
            "Kamera bulunamadı. Lütfen bir kameranın bağlı olduğundan emin olun."
          );
        } else {
          alert(`Kamera erişim hatası: ${error.message}`);
        }
      }
    };

    const closeCamera = () => {
      if (stream.value) {
        stream.value.getTracks().forEach((track) => track.stop());
        stream.value = null;
      }
      showCamera.value = false;
    };

    const capturePhoto = () => {
      if (!videoRef.value || !canvasRef.value) return;

      const video = videoRef.value;
      const canvas = canvasRef.value;
      const context = canvas.getContext("2d");

      // Video boyutlarını al
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      // Videodan görüntüyü canvas'a çiz
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Canvas'taki görüntüyü base64 formatına çevir
      canvas.toBlob(
        (blob) => {
          // Dosya nesnesini oluştur
          const file = new File([blob], "camera-photo.jpg", {
            type: "image/jpeg",
          });

          // Profil resmi olarak ayarla
          formData.value.profil_resmi_file = file;
          formData.value.profil_resmi_preview = URL.createObjectURL(blob);

          // Kamerayı kapat
          closeCamera();
        },
        "image/jpeg",
        0.9
      );
    };

    const isImageFile = (filename) => {
      const imageExtensions = [".jpg", ".jpeg", ".png", ".gif"];
      const ext = "." + filename.split(".").pop().toLowerCase();
      return imageExtensions.includes(ext);
    };

    const showPreview = (imageUrl) => {
      previewImage.value = imageUrl;
    };

    const closePreview = () => {
      previewImage.value = null;
    };

    const handleKimlikNoInput = (event) => {
      // Sadece sayıları kabul et
      formData.value.kimlik_no = event.target.value.replace(/[^0-9]/g, "");
    };

    const handleTelefonInput = (event) => {
      // Sadece sayıları kabul et ve 11 haneyle sınırla
      formData.value.telefon = event.target.value
        .replace(/[^0-9]/g, "")
        .slice(0, 11);
    };

    const handleIbanInput = (event) => {
      // IBAN'ı büyük harfe çevir ve boşlukları kaldır
      let iban = event.target.value.toUpperCase().replace(/\s/g, "");

      // Eğer TR ile başlamıyorsa, TR ekle
      if (!iban.startsWith("TR")) {
        iban = "TR" + iban;
      }

      // Her 4 karakterde bir boşluk ekle
      iban = iban.replace(/(.{4})/g, "$1 ").trim();

      formData.value.iban = iban;
    };

    // aile_bilgileri içindeki değişiklikleri izle
    const watchAileBilgileri = () => {
      for (let i = 0; i < formData.value.aile_bilgileri.length; i++) {
        const member = formData.value.aile_bilgileri[i];
        // Her üye için engel_durumu değişimini izle
        watch(
          () => member.engel_durumu,
          (newValue) => {
            console.log(`Member ${i} engel_durumu changed to: ${newValue}`);
            // Engel durumu false olduğunda bile açıklamayı koru
            if (!newValue) {
              // Önceki açıklamayı sakla
              const savedAciklama = member.engel_aciklama;
              if (savedAciklama) {
                // Korunan açıklama
                console.log(
                  `Preserving explanation for member ${i}: ${savedAciklama}`
                );
              }
            }
          }
        );
      }
    };

    // aile_bilgileri değiştiğinde watchları güncelle
    watch(
      () => formData.value.aile_bilgileri.length,
      () => {
        console.log("Aile bilgileri length changed, updating watchers");
        watchAileBilgileri();
      },
      { immediate: true }
    );

    onMounted(() => {
      if (props.editMode && props.initialData) {
        // API verilerini logla
        console.log("Initial Data from API:", props.initialData);
        console.log(
          "Family Members from API:",
          props.initialData.aile_bilgileri
        );

        // Mevcut formData'yı API verisiyle güncelle
        formData.value = {
          ...initialFormData,
          ...props.initialData,
          kayit_tarihi: props.initialData.kayit_tarihi
            ? new Date(props.initialData.kayit_tarihi)
                .toISOString()
                .split("T")[0]
            : initialFormData.kayit_tarihi,
          aile_bilgileri: props.initialData.aile_bilgileri
            ? JSON.parse(JSON.stringify(props.initialData.aile_bilgileri))
            : [],
          belgeler: { ...initialFormData.belgeler },
          profil_resmi_preview: props.initialData.profil_resmi,
          profil_resmi_file: null,
        };

        console.log(
          "Form aile_bilgileri after initialization:",
          formData.value.aile_bilgileri
        );

        // Belgeleri işle
        if (
          props.initialData.belgeler &&
          Array.isArray(props.initialData.belgeler)
        ) {
          props.initialData.belgeler.forEach((belge) => {
            if (
              belge.belge_turu &&
              belge.belge_turu in formData.value.belgeler
            ) {
              formData.value.belgeler[belge.belge_turu] =
                formData.value.belgeler[belge.belge_turu] || [];
              formData.value.belgeler[belge.belge_turu].push({
                name:
                  belge.belge?.split("/").pop() ||
                  `Mevcut Belge (${belge.belge_turu})`,
                url: belge.belge_url,
                isExisting: true,
              });
            }
          });
        }

        // dolduran_kisi alanını koru
        formData.value.dolduran_kisi =
          props.initialData.dolduran_kisi || username.value;
      }
    });

    return {
      formData,
      UYRUK_CHOICES,
      getBelgeAciklama,
      getBelgeLabel,
      triggerFileInput,
      removeFile,
      handleFileUpload,
      addFamilyMember,
      removeFamilyMember,
      handleSubmit,
      fileInputs,
      deleteBelge,
      handleProfileImageChange,
      removeProfileImage,
      showCamera,
      startCamera,
      closeCamera,
      capturePhoto,
      videoRef,
      canvasRef,
      previewImage,
      isImageFile,
      showPreview,
      closePreview,
      handleKimlikNoInput,
      handleTelefonInput,
      handleIbanInput,
      valid,
      form,
      loading,
    };
  },
};
</script>

<style scoped>
.v-card {
  border-radius: 8px;
  overflow: hidden;
}

.v-card-title {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.form-field {
  font-size: 1.1rem;
}

.form-field :deep(.v-field__input) {
  min-height: 48px;
  padding-top: 12px;
  padding-bottom: 12px;
}

.form-field :deep(.v-field__outline) {
  border-width: 2px;
}

.form-field :deep(.v-label) {
  font-size: 1.1rem;
  opacity: 0.8;
}

.modern-table {
  border-radius: 8px;
  overflow: hidden;
}

.modern-table .v-table__wrapper > table {
  border-collapse: separate;
  border-spacing: 0;
}

.modern-table .v-table__wrapper > table > thead > tr > th {
  background-color: transparent !important;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.6);
}

.modern-table .v-table__wrapper > table > thead > tr > th,
.modern-table .v-table__wrapper > table > tbody > tr > td {
  border: none !important;
}

.hover-row:hover {
  background-color: transparent !important;
}

.search-results-list {
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 4px;
}

.search-results-list::-webkit-scrollbar {
  width: 8px;
}

.search-results-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.search-results-list::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.search-results-list::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
