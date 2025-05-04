import streamlit as st
from utils.data_loader import load_data
import modules.profilowanie_danych as profilowanie_danych
import modules.analiza as analiza
import modules.geoanaliza as geoanaliza

from humanize import naturalsize

# Konfiguracja strony
st.set_page_config(page_title='Aplikacja Magisterska', layout='wide', initial_sidebar_state="collapsed")

# Inicjalizacja danych
if 'df' not in st.session_state:
    st.session_state.df = None

if 'page' not in st.session_state:
    st.session_state.page = "Strona główna"

# Sidebar jako menu
st.sidebar.title("Nawigacja")
if st.sidebar.button("Strona główna"):
    st.session_state.page = "Strona główna"
if st.sidebar.button("Profilowanie danych"):
    st.session_state.page = "Profilowanie danych"
if st.sidebar.button("Analiza"):
    st.session_state.page = "Analiza"
if st.sidebar.button("Geoanaliza"):
    st.session_state.page = "Geoanaliza"

# Główna zawartość
if st.session_state.page == "Strona główna":
    st.title('Aplikacja Magisterska')

    uploaded_file = st.file_uploader("Wczytaj plik .csv lub .xlsx", type=["csv", "xlsx"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        st.session_state.df = df
        st.success("Dane zostały załadowane!")
        st.write("Załadowano plik o rozmiarze:", naturalsize(uploaded_file.size))
        st.write("Dostępne kolumny:", list(df.columns))

elif st.session_state.df is not None:
    if st.session_state.page == "Profilowanie danych":
        profilowanie_danych.run(st.session_state.df)
    elif st.session_state.page == "Analiza":
        analiza.run(st.session_state.df)
    elif st.session_state.page == "Geoanaliza":
        geoanaliza.run(st.session_state.df)
else:
    st.info("Wczytaj dane, aby korzystać z innych zakładek.")
