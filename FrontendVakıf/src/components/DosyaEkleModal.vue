<template>
  <div
    v-if="showModal"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-[200]"
    @click.self="$emit('close')"
  >
    <div class="flex items-center justify-center min-h-screen">
      <div
        class="relative bg-white w-[1200px] shadow-lg rounded-md p-8 max-h-[90vh] overflow-y-auto z-[201]"
      >
        <div class="mt-3">
          <h3 class="text-2xl font-bold text-gray-900 mb-4">
            {{ editMode ? "Dosya Düzenle" : "Yeni Dosya Ekle" }}
          </h3>
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
          <form @submit.prevent="handleSubmit">
            <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
              <div class="grid grid-cols-4 gap-4 bg-gray-50 p-4 rounded">
                <div class="col-span-4 mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-2"
                    >Profil Resmi</label
                  >
                  <div class="flex flex-col items-center space-y-4">
                    <div
                      v-if="formData.profil_resmi_preview"
                      class="relative w-32 h-32"
                    >
                      <img
                        :src="formData.profil_resmi_preview"
                        class="w-32 h-32 object-cover rounded-lg"
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
                      <button
                        type="button"
                        @click="$refs.fileInput.click()"
                        class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        <i class="fas fa-upload mr-2"></i>
                        Dosyadan Yükle
                      </button>
                      <button
                        type="button"
                        @click="startCamera"
                        class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        <i class="fas fa-camera mr-2"></i>
                        Kameradan Çek
                      </button>
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
                <div class="mb-4" v-if="editMode">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Dosya No</label
                  >
                  <input
                    v-model="formData.dosya_no"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    readonly
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Kayıt Tarihi</label
                  >
                  <input
                    v-model="formData.kayit_tarihi"
                    type="date"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2">Ad</label>
                  <input
                    v-model="formData.ad"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Soyad</label
                  >
                  <input
                    v-model="formData.soyad"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Kimlik No</label
                  >
                  <input
                    v-model="formData.kimlik_no"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                    pattern="[0-9]*"
                    inputmode="numeric"
                    @input="handleKimlikNoInput"
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Uyruk</label
                  >
                  <select
                    v-model="formData.uyruk"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  >
                    <option
                      v-for="secenek in UYRUK_CHOICES"
                      :key="secenek.value"
                      :value="secenek.value"
                    >
                      {{ secenek.label }}
                    </option>
                  </select>
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Telefon</label
                  >
                  <input
                    v-model="formData.telefon"
                    type="tel"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                    pattern="[0-9]*"
                    inputmode="numeric"
                    maxlength="11"
                    @input="handleTelefonInput"
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2">İlçe</label>
                  <input
                    v-model="formData.ilce"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    value="Yeni Mahalle"
                    readonly
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Mahalle</label
                  >
                  <input
                    v-model="formData.mahalle"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Cadde/Sokak</label
                  >
                  <input
                    v-model="formData.cadde_sokak"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Bina No</label
                  >
                  <input
                    v-model="formData.bina_no"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Daire No</label
                  >
                  <input
                    v-model="formData.daire_no"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Kira Durumu</label
                  >
                  <select
                    v-model="formData.kira_durumu"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  >
                    <option value="EV_SAHIBI">Ev Sahibi</option>
                    <option value="KIRACI">Kiracı</option>
                  </select>
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Gelir Durumu (TL)</label
                  >
                  <input
                    v-model="formData.gelir_durumu"
                    type="number"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Dolduran Kişi</label
                  >
                  <input
                    v-model="formData.dolduran_kisi"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    readonly
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2">IBAN</label>
                  <input
                    v-model="formData.iban"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                    @input="handleIbanInput"
                  />
                </div>
                <div class="mb-4">
                  <label class="block text-gray-700 font-bold mb-2"
                    >Yardım Aldığı Yerler</label
                  >
                  <input
                    v-model="formData.yardim_aldigi_yerler"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>
              </div>

              <div class="mt-6">
                <h4 class="text-xl font-bold mb-4">İstenen Belgeler</h4>
                <div class="grid grid-cols-2 gap-6">
                  <div
                    v-for="(belgeType, index) in Object.keys(formData.belgeler)"
                    :key="index"
                    class="bg-gray-50 p-4 rounded-lg border border-gray-200 hover:border-blue-300 transition-all duration-200"
                  >
                    <div class="flex items-center justify-between mb-2">
                      <label class="block text-gray-700 font-bold">
                        {{ getBelgeLabel(belgeType) }}
                      </label>
                      <div class="flex items-center space-x-2">
                        <button
                          type="button"
                          @click="triggerFileInput(belgeType)"
                          class="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600 transition-colors duration-200"
                        >
                          Yükle
                        </button>
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
                            <a
                              v-if="file.url && isImageFile(file.name)"
                              @click.prevent="showPreview(file.url)"
                              href="#"
                              class="text-blue-500 hover:text-blue-700 cursor-pointer"
                            >
                              <svg
                                xmlns="http://www.w3.org/2000/svg"
                                class="h-4 w-4"
                                viewBox="0 0 20 20"
                                fill="currentColor"
                              >
                                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                                <path
                                  fill-rule="evenodd"
                                  d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                                  clip-rule="evenodd"
                                />
                              </svg>
                            </a>
                            <a
                              v-if="file.url"
                              :href="file.url"
                              target="_blank"
                              class="text-blue-500 hover:text-blue-700"
                            >
                              <svg
                                xmlns="http://www.w3.org/2000/svg"
                                class="h-4 w-4"
                                viewBox="0 0 20 20"
                                fill="currentColor"
                              >
                                <path
                                  fill-rule="evenodd"
                                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z"
                                  clip-rule="evenodd"
                                />
                              </svg>
                            </a>
                          </div>
                        </div>
                        <button
                          type="button"
                          @click="removeFile(belgeType, fileIndex)"
                          class="text-red-500 hover:text-red-700"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-5 w-5"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                          >
                            <path
                              fill-rule="evenodd"
                              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                              clip-rule="evenodd"
                            />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-6">
                <h4 class="text-xl font-bold mb-4">Aile Bilgileri</h4>
                <div
                  v-for="(member, index) in formData.aile_bilgileri"
                  :key="index"
                  class="mb-4 p-4 border rounded-lg"
                >
                  <label class="block text-gray-700 font-bold mb-2">
                    Aile Üyesi {{ index + 1 }}
                  </label>
                  <div class="grid grid-cols-3 gap-4">
                    <div>
                      <label class="block text-sm text-gray-600 mb-1">Ad</label>
                      <input
                        v-model="member.ad"
                        type="text"
                        placeholder="Ad"
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        required
                      />
                    </div>
                    <div>
                      <label class="block text-sm text-gray-600 mb-1"
                        >Soyad</label
                      >
                      <input
                        v-model="member.soyad"
                        type="text"
                        placeholder="Soyad"
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        required
                      />
                    </div>
                    <div>
                      <label class="block text-sm text-gray-600 mb-1"
                        >Kimlik No</label
                      >
                      <input
                        v-model="member.kimlik_no"
                        type="text"
                        placeholder="Kimlik No"
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        required
                      />
                    </div>
                    <div>
                      <label class="block text-sm text-gray-600 mb-1"
                        >Yakınlık</label
                      >
                      <select
                        v-model="member.yakinlik"
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        required
                      >
                        <option value="KENDISI">Kendisi</option>
                        <option value="ES">Eş</option>
                        <option value="COCUK">Çocuk</option>
                        <option value="ANNE">Anne</option>
                        <option value="BABA">Baba</option>
                        <option value="KARDES">Kardeş</option>
                        <option value="DIGER">Diğer</option>
                      </select>
                    </div>
                    <div>
                      <label class="block text-sm text-gray-600 mb-1"
                        >Cinsiyet</label
                      >
                      <select
                        v-model="member.cinsiyet"
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        required
                      >
                        <option value="E">Erkek</option>
                        <option value="K">Kadın</option>
                      </select>
                    </div>
                    <div>
                      <label class="block text-sm text-gray-600 mb-1"
                        >Doğum Tarihi</label
                      >
                      <input
                        v-model="member.dogum_tarihi"
                        type="date"
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                      />
                    </div>
                  </div>
                  <div class="mt-2 flex items-center">
                    <label class="mr-2 text-sm text-gray-600"
                      >Engel Durumu</label
                    >
                    <input
                      type="checkbox"
                      v-model="member.engel_durumu"
                      class="form-checkbox h-5 w-5 text-blue-600"
                    />
                    <div v-if="member.engel_durumu" class="ml-4 flex-1">
                      <div class="mb-2">
                        <label class="block text-sm text-gray-600 mb-1"
                          >Engel Açıklaması</label
                        >
                        <textarea
                          v-model="member.engel_aciklama"
                          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                          rows="2"
                          placeholder="Engel durumu hakkında detaylı açıklama..."
                        ></textarea>
                      </div>
                    </div>
                    <button
                      type="button"
                      @click="removeFamilyMember(index)"
                      class="ml-auto text-red-600 hover:text-red-900 flex items-center"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5 mr-1"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      Kaldır
                    </button>
                  </div>
                </div>
                <button
                  type="button"
                  @click="addFamilyMember"
                  class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 flex items-center"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 mr-2"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  Aile Üyesi Ekle
                </button>
              </div>
            </div>

            <div class="flex justify-end mt-6">
              <button
                type="submit"
                class="bg-blue-500 text-white px-4 py-2 rounded"
              >
                {{ editMode ? "Güncelle" : "Kaydet" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Kamera Modal -->
    <div
      v-if="showCamera"
      class="fixed inset-0 z-[300] overflow-y-auto"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <div
        class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          aria-hidden="true"
        ></div>
        <div
          class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
        >
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  Fotoğraf Çek
                </h3>
                <div class="relative">
                  <video
                    ref="videoRef"
                    class="w-full rounded-lg"
                    autoplay
                    playsinline
                  ></video>
                  <canvas ref="canvasRef" class="hidden"></canvas>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="capturePhoto"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Fotoğraf Çek
            </button>
            <button
              type="button"
              @click="closeCamera"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              İptal
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Resim Önizleme Modal -->
    <div
      v-if="previewImage"
      class="fixed inset-0 z-[70] overflow-y-auto"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <div class="flex items-center justify-center min-h-screen p-4">
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          @click="closePreview"
        ></div>
        <div
          class="relative bg-white rounded-lg overflow-hidden shadow-xl max-w-3xl mx-auto"
        >
          <div class="relative">
            <img
              :src="previewImage"
              class="max-h-[80vh] w-auto"
              alt="Belge Önizleme"
            />
            <button
              @click="closePreview"
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
    </div>
  </div>
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
  emits: ["close", "saved"],
  setup(props, { emit }) {
    const username = ref(localStorage.getItem("username") || "");
    const fileInputs = ref({});
    const videoRef = ref(null);
    const canvasRef = ref(null);
    const previewImage = ref(null);

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
    };
  },
};
</script>
