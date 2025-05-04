import pandas as pd
import matplotlib.pyplot as plt
import unidecode

# Wczytaj dane z odpowiednim kodowaniem i konwersją na daty
df = pd.read_csv('E:\\PYTHON\\Magisterka\\dane_do magisterki.csv', low_memory=False, encoding='utf-8')

# Tłumaczenie nazw kolumn na wersje bez polskich znaków
df.columns = [unidecode.unidecode(col) for col in df.columns]

# Konwersja kolumny 'data_zamowienia' do formatu datetime
df['data_zamowienia'] = pd.to_datetime(df['data_zamowienia'], errors='coerce')

# Tworzenie kolumny 'miesiac' na podstawie 'data_zamowienia'
df['miesiac'] = df['data_zamowienia'].dt.strftime('%Y-%m')
def format_number(value):
    if value >= 1_000_000:
        return f'{value / 1_000_000:.1f}M'
    elif value >= 1_000:
        return f'{value / 1_000:.1f}K'
    else:
        return f'{value:.1f}'
# Sprawdź, czy 'miesiac' został poprawnie utworzony
print("Unikalne wartości w kolumnie 'miesiac':", df['miesiac'].unique())

# Tworzymy figurę z wykresami w układzie 2x3
fig, axs = plt.subplots(2, 3, figsize=(18, 10))
fig.tight_layout(pad=5.0)

# W1 - Miesięczny przychód z wartością nad każdym punktem
try:
    monthly_revenue = df.groupby('miesiac')[['przychod_generowany_przez_kobiety', 'przychod_generowany_przez_mezczyzn']].sum().sum(axis=1)
    monthly_revenue.plot(kind='line', ax=axs[0, 0], color='purple', marker='o', markersize=5)
    axs[0, 0].set_title('Miesięczny Przychód')
    axs[0, 0].set_ylabel('Przychód')
    axs[0, 0].set_xlabel('Miesiąc')
    axs[0, 0].set_ylim(0, 60_000_000)
    axs[0, 0].set_yticks(range(0, 61_000_000, 5_000_000))
    axs[0, 0].set_xticks(range(len(monthly_revenue)))
    axs[0, 0].set_xticklabels(monthly_revenue.index, rotation=45)
    for idx, value in enumerate(monthly_revenue):
        axs[0, 0].text(x=idx, y=value + 1_000_000, s=f'{value:,.0f}', ha='center', va='bottom', fontsize=8)
except Exception as e:
    print(f"Błąd w generowaniu wykresu W1: {e}")

# W2 - Procentowy udział regionów w przychodach
try:
    region_revenue = df.groupby('region')[['przychod_generowany_przez_kobiety', 'przychod_generowany_przez_mezczyzn']].sum().sum(axis=1)
    wedges, texts, autotexts = axs[0, 1].pie(
        region_revenue, 
        autopct='%1.1f%%', 
        startangle=90,
        textprops={'fontsize': 10},
        pctdistance=0.85,
        wedgeprops={'linewidth': 1, 'edgecolor': 'black'}
    )
    axs[0, 1].set_title('Udział regionów w przychodach')
    axs[0, 1].legend(wedges, region_revenue.index, title="Region", loc="center left", bbox_to_anchor=(1, 0.5))
except Exception as e:
    print(f"Błąd w generowaniu wykresu W2: {e}")

# W3 - TOP 7 Dostawców płatności z etykietami na zewnątrz
try:
    top7_providers = df.groupby('metoda_platnosci')[['przychod_generowany_przez_kobiety', 'przychod_generowany_przez_mezczyzn']].sum().sum(axis=1).nlargest(7)
    wedges, texts, autotexts = axs[0, 2].pie(
        top7_providers, 
        autopct='%1.1f%%', 
        startangle=90,
        textprops={'fontsize': 10},
        pctdistance=1.2,
        wedgeprops={'linewidth': 1, 'edgecolor': 'black'}
    )
    axs[0, 2].set_title('TOP 7 Dostawców Płatności')
    axs[0, 2].legend(wedges, top7_providers.index, title="Metody płatności", loc="center left", bbox_to_anchor=(1, 0.5))
except Exception as e:
    print(f"Błąd w generowaniu wykresu W3: {e}")

# W4 - Udział grup wiekowych w przychodach, posortowane od najmłodszych do najstarszych
try:
    age_group_revenue = df.groupby('przedzial_wiekowy')[['przychod_generowany_przez_kobiety', 'przychod_generowany_przez_mezczyzn']].sum()
    age_group_revenue = age_group_revenue.loc[['<20', '20-30', '30-40', '40-50', '50-60', '60-70', '>70']]
    age_group_revenue.plot(kind='bar', ax=axs[1, 0], color=['purple', 'blue'])
    axs[1, 0].set_title('Udział grup wiekowych w przychodach')
    axs[1, 0].set_ylabel('Przychód')
    axs[1, 0].set_xlabel('Przedział wiekowy')
except Exception as e:
    print(f"Błąd w generowaniu wykresu W4: {e}")

# W5 - Średnia suma zamówień w każdym miesiącu z etykietami
try:
    avg_order_sum = df.groupby('miesiac')['srednia suma'].mean()
    avg_order_sum.plot(kind='line', ax=axs[1, 1], color='green', marker='o', markersize=5)
    axs[1, 1].set_title('Średnia suma zamówień')
    axs[1, 1].set_ylabel('Średnia suma')
    axs[1, 1].set_xlabel('Miesiąc')
    axs[1, 1].set_xticks(range(len(avg_order_sum)))
    axs[1, 1].set_xticklabels(avg_order_sum.index, rotation=45)
    for idx, value in enumerate(avg_order_sum):
        axs[1, 1].text(x=idx, y=value + 20, s=f'{value:.0f}', ha='center', va='bottom', fontsize=8)
except Exception as e:
    print(f"Błąd w generowaniu wykresu W5: {e}")

# W6 - Przychód w rozbiciu na kategorie i płeć jako wykres motylkowy
try:
    category_revenue = df.groupby('kategoria')[['przychod_generowany_przez_kobiety', 'przychod_generowany_przez_mezczyzn']].sum()
    categories = category_revenue.index

    # Oblicz maksymalne wartości do ustalenia osi X
    max_value = max(category_revenue['przychod_generowany_przez_kobiety'].max(), category_revenue['przychod_generowany_przez_mezczyzn'].max())

    # Tworzymy wykres słupkowy poziomy dla kobiet i mężczyzn
    axs[1, 2].barh(categories, category_revenue['przychod_generowany_przez_kobiety'], color='purple', label='Kobiety')
    axs[1, 2].barh(categories, category_revenue['przychod_generowany_przez_mezczyzn'], color='blue', label='Mężczyźni', left=category_revenue['przychod_generowany_przez_kobiety'])

    # Dodajemy etykiety wartości nad słupkami, zaokrąglone z sufiksem
    for idx, value in enumerate(category_revenue['przychod_generowany_przez_kobiety']):
        axs[1, 2].text(value / 2, idx, format_number(value), va='center', fontsize=8, color='white')

    for idx, value in enumerate(category_revenue['przychod_generowany_przez_mezczyzn']):
        axs[1, 2].text(category_revenue['przychod_generowany_przez_kobiety'][idx] + value / 2, idx, format_number(value), va='center', fontsize=8, color='white')

    # Ustawienia osi Y i X dla lepszej czytelności
    axs[1, 2].set_yticks(range(len(categories)))
    axs[1, 2].set_yticklabels(categories)
    axs[1, 2].set_xlabel('Przychód')
    axs[1, 2].set_title('Przychód z podziałem na kategorię i płeć')
    axs[1, 2].legend(loc='upper right')
    axs[1, 2].set_xlim(0, max_value * 1.2)
except Exception as e:
    print(f"Błąd w generowaniu wykresu W6: {e}")
    axs[1, 2].text(0.5, 0.5, 'Błąd w generowaniu wykresu W6', ha='center', va='center')


# Wyświetlenie wszystkich wykresów
plt.tight_layout()
plt.show()