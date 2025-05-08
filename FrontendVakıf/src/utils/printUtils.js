export const formatDate = (dateString) => {
  if (!dateString) return "";
  return new Date(dateString).toLocaleDateString("tr-TR");
};

export const formatAddress = (dosya) => {
  return `${dosya.mahalle} Mah. ${dosya.cadde_sokak} Cad. No:${dosya.bina_no} Daire:${dosya.daire_no}`;
};

export const getBelgeDurumu = (dosya, belgeTuru) => {
  if (dosya && dosya.belgeler && Array.isArray(dosya.belgeler)) {
    return dosya.belgeler.some((b) => b.belge_turu === belgeTuru)
      ? "VAR"
      : "YOK";
  }
  return "YOK";
};

export const calculateAge = (birthDate) => {
  if (!birthDate) return "";
  const birth = new Date(birthDate);
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  return age >= 0 ? age : "";
};

export const generatePrintHtml = (currentDosya, profilResmiUrl) => {
  return `
    <!DOCTYPE html>
    <html>
      <head>
        <title>Dosya Yazdırma</title>
        <meta charset="UTF-8">
        <style>
          @import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css');
          body { margin: 0; padding: 20px; }
          @media print {
            @page { size: A4; margin: 1cm; }
            body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid black; padding: 4px 8px; text-align: left; font-size: 10pt; vertical-align: top; }
            th { background-color: #f2f2f2; font-weight: bold; }
            img { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
          }
          .profile-image {
            width: 120px;
            height: 120px;
            object-fit: cover;
            border: 1px solid black;
          }
        </style>
      </head>
      <body>
        <div class="max-w-4xl mx-auto p-4 font-sans">
          <table class="min-w-full border border-black text-xs mb-4">
            <tbody>
              <tr>
                <td class="border border-black py-1 px-2 w-1/5 font-bold">TARİHİ</td>
                <td class="border border-black py-1 px-2 w-1/5">${formatDate(
                  currentDosya.kayit_tarihi
                )}</td>
                <td class="border border-black py-1 px-2 w-1/5 font-bold">İSTENEN BELGELER</td>
                <td class="border border-black py-1 px-2 w-2/5" rowspan="3">
                  ${
                    currentDosya.profil_resmi
                      ? `<img src="${profilResmiUrl}" class="profile-image" alt="Profil Resmi" />`
                      : ""
                  }
                </td>
              </tr>
              <tr>
                <td class="border border-black py-1 px-2 font-bold">DOSYA NUMARASI</td>
                <td class="border border-black py-1 px-2">${
                  currentDosya.dosya_no
                }</td>
                <td class="border border-black py-1 px-2 font-bold">KİMLİK NO</td>
              </tr>
              <tr>
                <td class="border border-black py-1 px-2 font-bold">ADI SOYADI</td>
                <td class="border border-black py-1 px-2">${currentDosya.ad} ${
    currentDosya.soyad
  }</td>
                <td class="border border-black py-1 px-2 font-bold">KONTRAT</td>
              </tr>
              <tr>
                <td class="border border-black py-1 px-2 font-bold">UYRUĞU</td>
                <td class="border border-black py-1 px-2">${
                  currentDosya.uyruk
                }</td>
                <td class="border border-black py-1 px-2 font-bold">ÖLÜM BELGESİ</td>
                <td class="border border-black py-1 px-2">${getBelgeDurumu(
                  currentDosya,
                  "OLUM_BELGESI"
                )}</td>
              </tr>
              <tr>
                <td class="border border-black py-1 px-2 font-bold">KİRA DURUMU</td>
                <td class="border border-black py-1 px-2">${
                  currentDosya.kira_durumu
                }</td>
                <td class="border border-black py-1 px-2 font-bold">VUKUAT N.KA.</td>
                <td class="border border-black py-1 px-2">${getBelgeDurumu(
                  currentDosya,
                  "VUKUATLI_NUFUS"
                )}</td>
              </tr>
              <tr>
                <td class="border border-black py-1 px-2 font-bold">TELEFON NU.</td>
                <td class="border border-black py-1 px-2">${
                  currentDosya.telefon
                }</td>
                <td class="border border-black py-1 px-2 font-bold">ÖĞR.BELGESİ</td>
                <td class="border border-black py-1 px-2">${getBelgeDurumu(
                  currentDosya,
                  "OGRENCI_BELGESI"
                )}</td>
              </tr>
              <tr>
                <td class="border border-black py-1 px-2 font-bold">ADRES</td>
                <td class="border border-black py-1 px-2" colspan="1">${formatAddress(
                  currentDosya
                )}</td>
                <td class="border border-black py-1 px-2 font-bold">BANKA EKSTRESİ</td>
                <td class="border border-black py-1 px-2">${getBelgeDurumu(
                  currentDosya,
                  "BANKA_EKSTRESI"
                )}</td>
              </tr>
              <tr>
                <td class="border border-black py-1 px-2 font-bold">IBAN</td>
                <td class="border border-black py-1 px-2" colspan="1">${
                  currentDosya.iban
                }</td>
                <td class="border border-black py-1 px-2 font-bold" rowspan="2">TETKİK</td>
                <td class="border border-black py-1 px-2" rowspan="2"></td>
              </tr>
              <tr>
                <td class="border border-black py-1 px-2 font-bold">DOLDURAN KİŞİ</td>
                <td class="border border-black py-1 px-2">${
                  currentDosya.dolduran_kisi
                }</td>
              </tr>
              <tr>
                <td class="border border-black py-1 px-2 font-bold">GELİR DURUMU</td>
                <td class="border border-black py-1 px-2">${
                  currentDosya.gelir_durumu
                } TL</td>
              </tr>
              <tr>
                <td class="border border-black py-1 px-2 font-bold">YARDIM AL. YERLER</td>
                <td class="border border-black py-1 px-2" colspan="3">${
                  currentDosya.yardim_aldigi_yerler
                }</td>
              </tr>
            </tbody>
          </table>

          <!-- Kişi Bilgisi Tablosu -->
          <table class="min-w-full border border-black text-xs mt-4">
            <thead>
              <tr>
                <th class="border border-black py-1 px-2 text-center font-bold" colspan="6">KİŞİ BİLGİSİ</th>
              </tr>
              <tr>
                <th class="border border-black py-1 px-2 font-bold">S.NU.</th>
                <th class="border border-black py-1 px-2 font-bold">YAKINLIK</th>
                <th class="border border-black py-1 px-2 font-bold">ADI SOYADI</th>
                <th class="border border-black py-1 px-2 font-bold">E/K</th>
                <th class="border border-black py-1 px-2 font-bold">YAŞI</th>
                <th class="border border-black py-1 px-2 font-bold">AÇIKLAMA</th>
              </tr>
            </thead>
            <tbody>
              ${
                currentDosya.aile_bilgileri &&
                currentDosya.aile_bilgileri.length > 0
                  ? currentDosya.aile_bilgileri
                      .map(
                        (member, index) => `
                  <tr>
                    <td class="border border-black py-1 px-2 text-center">${
                      index + 1
                    }</td>
                    <td class="border border-black py-1 px-2">${
                      member.yakinlik
                    }</td>
                    <td class="border border-black py-1 px-2">${member.ad} ${
                          member.soyad
                        }</td>
                    <td class="border border-black py-1 px-2 text-center">${
                      member.cinsiyet
                    }</td>
                    <td class="border border-black py-1 px-2 text-center">${calculateAge(
                      member.dogum_tarihi
                    )}</td>
                    <td class="border border-black py-1 px-2">${
                      member.engel_aciklama ||
                      (member.engel_durumu ? "Engelli" : "")
                    }</td>
                  </tr>
                `
                      )
                      .join("")
                  : `<tr>
                    <td class="border border-black py-1 px-2 text-center text-gray-500" colspan="6">Aile üyesi bilgisi bulunmamaktadır.</td>
                  </tr>`
              }
            </tbody>
          </table>

          <!-- İmza -->
          <table class="min-w-full border border-gray-800 text-sm mt-4">
            <thead>
              <tr>
                <th class="border-b border-gray-800 py-1 px-2 text-center" colspan="2">
                  EK AÇIKLAMA
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="border-b border-gray-800 py-24 px-24 min-h-[100px]">
                  <p class="whitespace-pre-line"></p>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- İmza -->
          <div class="mt-8">
            <p class="text-sm">SAMİ EFENDİ VAKFINA ANKARA</p>
            <p class="text-sm text-justify mt-2">
              SAMİ EFENDİ VAKFINA; yapmış olduğum iş bu yardım başvurusunda beyan
              ettiğim bilgilerin doğru olduğunu; bilgilerimin doğruluğunun tesbiti
              için dernek görevlilerinin her türlü araştırma yapmasına,gerekirse beyan
              ettiğim yerlere girmesine,derneğin çalışma usul ve esaslarına muvafakat
              ettiğim,bilgilerimin yanlış çıkması halinde tüm sorumluluğun tarafıma
              ait olacağını,tarafıma yardım yapılmış veya yapılmamış olması verdiğim
              evrakları hiç bir şekilde geri talep etmeyeceğimi peşinen kabul ve beyan
              ederim.Rahmeteli Gıda Bankası Derneği yardım kararı durdurabilir.Gerekçe
              göstermek zorunda değildir.Ayrıca derneğin faaliyetlerinde kullanılmak
              üzere şahsıma ve bana ait yerlerde her türlü görsel belirtme kamera
              kullanılmasına muvafakat ediyorum.
            </p>
          </div>

          <!-- İmza ve Tarih Alanı -->
          <div class="mt-12 flex justify-between text-xs">
            <div>
              <p>İMZA:</p>
              <div class="border-b border-black w-48 mt-8"></div>
            </div>
            <div>
              <p>TARİH:</p>
              <div class="border-b border-black w-48 mt-8"></div>
            </div>
          </div>
        </div>
      </body>
    </html>
  `;
};

export const printDosya = async (dosya, apiService) => {
  try {
    const response = await apiService.getDosya(dosya.dosya_no);
    const currentDosya = response.data;

    let profilResmiUrl = "";
    if (currentDosya.profil_resmi) {
      const backendUrl =
        import.meta.env.VITE_API_URL || "http://localhost:8000";
      profilResmiUrl = currentDosya.profil_resmi.startsWith("http")
        ? currentDosya.profil_resmi
        : `${backendUrl}${currentDosya.profil_resmi}`;
    }

    const printWindow = window.open("", "_blank");
    const htmlContent = generatePrintHtml(currentDosya, profilResmiUrl);

    printWindow.document.write(htmlContent);
    printWindow.document.close();

    setTimeout(() => {
      printWindow.document.title = `Dosya_${currentDosya.dosya_no}_Print`;
      printWindow.focus();
      printWindow.print();
      printWindow.onafterprint = () => {
        setTimeout(() => printWindow.close(), 500);
      };
    }, 1000);
  } catch (error) {
    console.error("Yazdırma hatası:", error);
    alert(
      "Dosya bilgileri getirilemedi veya yazdırma sırasında bir hata oluştu."
    );
  }
};
