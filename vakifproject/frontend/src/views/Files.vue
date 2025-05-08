const tableHeaders = [ { title: 'Dosya No', key: 'dosya_no', sortable: true }, {
title: 'Ad Soyad', key: 'ad_soyad', sortable: true }, { title: 'Telefon', key:
'telefon', sortable: true }, { title: 'Adres', key: 'adres', sortable: true }, {
title: 'Durum', key: 'durum', sortable: true }, { title: 'Kira Durumu', key:
'kira_durumu', sortable: true }, { title: 'Engelli Sayısı', key:
'engelli_sayisi', sortable: true }, { title: 'İşlemler', key: 'actions',
sortable: false } ] const filterFiles = async () => { try { loading.value = true
const params = new URLSearchParams() if (searchQuery.value) {
params.append('search', searchQuery.value) } if (selectedStatus.value) {
params.append('durum', selectedStatus.value) } if (selectedRentStatus.value) {
params.append('kira_durumu', selectedRentStatus.value) } if
(selectedDisabilityStatus.value) { params.append('engel_durumu',
selectedDisabilityStatus.value) } if (selectedSort.value) {
params.append('ordering', selectedSort.value) } const response = await
axios.get(`${API_URL}/dosyalar/?${params.toString()}`) files.value =
response.data } catch (error) { console.error('Dosyalar yüklenirken hata:',
error) snackbar.value = true snackbarText.value = 'Dosyalar yüklenirken bir hata
oluştu' snackbarColor.value = 'error' } finally { loading.value = false } }
