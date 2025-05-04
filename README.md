# 📊 Aplikacja Magisterska – Analiza Konsumencka i Geoanaliza

Projekt wykonany w ramach pracy magisterskiej. Aplikacja służy do eksploracji, profilowania oraz wizualizacji danych konsumenckich w podziale na czas, region, kategorię oraz dane demograficzne klientów.

## 🚀 Funkcjonalności

### ✅ Strona główna

- Wczytywanie plików `.csv` oraz `.xlsx`
- Informacje o załadowanym pliku i podgląd kolumn

### 🔍 Profilowanie danych

- Generowanie raportów z wykorzystaniem `ydata-profiling`
- Pomijanie kolumn tekstowych
- Raport dostępny do ponownego podglądu bez ponownego generowania

### 📈 Analiza konsumencka

- Interaktywne wykresy (Plotly)
- Siatka 2x3 wykresów:
  - Miesięczny przychód
  - Średnia suma zamówienia
  - Przychód wg grup wiekowych
  - Przychód wg regionów
  - TOP 7 metod płatności
  - Wykres motylkowy: kategorie i płeć
- Filtrowanie po dacie, kategorii, płci

### 🌍 Geoanaliza

- Interaktywne mapy USA:
  - Przychód ogółem
  - Przychód wg płci
  - Klienci wg przedziałów wiekowych
- Filtrowanie po:
  - Dacie
  - Zakresie przychodu
  - Grupach wiekowych (multi select)
- Ujednolicona kolorystyka (zielono-czerwona)

## 🛠️ Wymagania

- Python 3.10+
- Streamlit
- Plotly
- Pandas
- ydata-profiling
- humanize

Można zainstalować wymagania poleceniem:

```bash
pip install -r requirements.txt


```
