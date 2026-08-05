# 1. Aşama: Resmi, hafif ve güvenli Python imajını çekiyoruz
FROM python:3.10-slim

# 2. İşletim sistemi güncellemelerini yap ve gereksiz dosyaları temizle (İmaj boyutunu küçültmek için)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 3. Konteyner içindeki çalışma klasörümüzü belirliyoruz
WORKDIR /app

# 4. Önce sadece kütüphane listesini kopyala (Docker Cache avantajı için)
COPY requirements.txt .

# 5. Kütüphaneleri kur
RUN pip install --no-cache-dir -r requirements.txt

# 6. Kalan tüm proje dosyalarını (main.py ve core/scanner.py) kopyala
COPY . .

# 7. GÜVENLİK (Least Privilege): Root kullanıcısı yerine kısıtlı bir kullanıcı oluştur ve ona geç
RUN useradd -m securuser
RUN chown -R securuser:securuser /app
USER securuser

# 8. Uygulamanın 8000 portundan dışarı açılacağını belirt
EXPOSE 8000

# 9. Konteyner ayağa kalktığında çalışacak ana komut
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]