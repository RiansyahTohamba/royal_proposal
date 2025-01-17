Berikut adalah perbaikan dan penyesuaian:

1. **Perbaikan di ViewSet:**
   - Buat satu saja definisi `upload_cv` untuk menghindari konflik. Gunakan POST saja.
   - Sesuaikan metode jika ada logika tambahan yang diperlukan.

2. **Konfigurasi `urls.py`:**
   - Gunakan `router` dari `rest_framework.routers` untuk mendaftarkan `CandidateViewSet`.

Berikut adalah kode yang sudah diperbaiki dan termasuk penyesuaian `urls.py`:

### Perbaikan di `views.py` (untuk `CandidateViewSet`):
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Candidate
from .serializers import CandidateSerializer

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    @action(detail=True, methods=['post'])
    def upload_cv(self, request, pk=None):
        candidate = self.get_object()
        candidate.cv = request.data.get('cv')
        candidate.save()
        return Response({'message': 'CV uploaded successfully'}, status=status.HTTP_200_OK)
```

### Konfigurasi `urls.py`:
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet

# Buat router untuk mendaftarkan ViewSet
router = DefaultRouter()
router.register(r'candidates', CandidateViewSet, basename='candidate')

urlpatterns = [
    path('', include(router.urls)),  # Termasuk semua route dari router
]
```

### Penjelasan:
1. **Perbaikan Metode `upload_cv`:**
   - Menghapus duplikasi metode.
   - Menggunakan `request.data.get('cv')` untuk memastikan data diambil dengan aman.
   - Memberikan respons JSON dengan pesan sukses.

2. **Router di `urls.py`:**
   - `DefaultRouter` dari Django REST Framework digunakan untuk membuat rute CRUD otomatis.
   - `router.register()` mendaftarkan `CandidateViewSet` dengan URL dasar `candidates/`.

3. **Fitur CRUD Otomatis:**
   - Dengan pendekatan ini, endpoint seperti berikut akan tersedia:
     - `GET /candidates/`: Daftar kandidat.
     - `POST /candidates/`: Tambah kandidat.
     - `GET /candidates/{id}/`: Detail kandidat.
     - `PUT /candidates/{id}/`: Perbarui kandidat.
     - `DELETE /candidates/{id}/`: Hapus kandidat.
     - `POST /candidates/{id}/upload_cv/`: Upload CV kandidat (custom action).

Cobalah solusi ini, dan pastikan semua dependensi seperti Django REST Framework telah terinstal dengan benar. Jika masih ada kendala, beri tahu saya! 😊