export const yakinlikSecenekleri = [
  { value: "KENDISI", label: "Kendisi" },
  { value: "ES", label: "Eş" },
  { value: "COCUK", label: "Çocuk" },
  { value: "ANNE", label: "Anne" },
  { value: "BABA", label: "Baba" },
  { value: "KARDES", label: "Kardeş" },
  { value: "DIGER", label: "Diğer" },
];

export const UYRUK_CHOICES = [
  { value: "", label: "Seçiniz" },
  { value: "TC", label: "Türkiye" },
  { value: "SURIYE", label: "Suriye" },
  { value: "IRAK", label: "Irak" },
  { value: "IRAN", label: "İran" },
  { value: "AFGANISTAN", label: "Afganistan" },
  { value: "SUDAN", label: "Sudan" },
  { value: "DIGER", label: "Diğer" },
];

export const DURUM_CHOICES = [
  { value: "BEKLEMEDE", label: "Beklemede" },
  { value: "ONAYLANDI", label: "Onaylandı" },
  { value: "REDDEDILDI", label: "Reddedildi" },
];

export const kiraDurumuSecenekleri = [
  { value: "KIRACI", label: "Kiracı" },
  { value: "EV_SAHIBI", label: "Ev Sahibi" },
];

export const cinsiyetSecenekleri = [
  { value: "ERKEK", label: "Erkek" },
  { value: "KADIN", label: "Kadın" },
];

export const belgeSecenekleri = [
  {
    value: "kimlik_fotokopisi",
    label: "Kimlik Fotokopisi",
    accept: "image/*,.pdf",
  },
  {
    value: "ikametgah",
    label: "İkametgah",
    accept: "image/*,.pdf",
  },
  {
    value: "gelir_belgesi",
    label: "Gelir Belgesi",
    accept: "image/*,.pdf",
  },
  {
    value: "kira_kontrati",
    label: "Kira Kontratı",
    accept: "image/*,.pdf",
  },
  {
    value: "engelli_raporu",
    label: "Engelli Raporu",
    accept: "image/*,.pdf",
  },
  {
    value: "diger_belgeler",
    label: "Diğer Belgeler",
    accept: "image/*,.pdf",
  },
];

export const BELGE_TURU_CHOICES = [
  { value: "KONTRAT", label: "Kontrat" },
  { value: "OLUM_BELGESI", label: "Ölüm Belgesi" },
  { value: "VUKUATLI_NUFUS", label: "Vukuatlı Nüfus Kayıt Örneği" },
  { value: "OGRENCI_BELGESI", label: "Öğrenci Belgesi" },
  { value: "BANKA_EKSTRESI", label: "Banka Ekstresi" },
  { value: "TEMVIYYE", label: "Temviyye" },
];
