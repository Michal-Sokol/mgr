import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import pandas as pd

def run(df):
    st.title("Profilowanie danych")

    # Inicjalizacja miejsca w session_state na raport i opcje
    if "profiling_report" not in st.session_state:
        st.session_state["profiling_report"] = None
    if "profiling_options" not in st.session_state:
        st.session_state["profiling_options"] = {"minimal": False, "filter_text": True}

    # Checkboksy opcji
    minimal = st.checkbox("Minimalny raport?", value=st.session_state["profiling_options"]["minimal"])
    filter_text = st.checkbox("Pomiń kolumny tekstowe (np. e-mail, nazwiska)", value=st.session_state["profiling_options"]["filter_text"])

    st.session_state["profiling_options"]["minimal"] = minimal
    st.session_state["profiling_options"]["filter_text"] = filter_text

    # Przycisk generowania raportu
    if st.button("Generuj raport"):
        with st.spinner("Generowanie raportu..."):
            try:
                if filter_text:
                    df_filtered = df[[col for col in df.columns if df[col].dtype != "object" or df[col].nunique() < 50]]
                    st.info(f"Do raportu wybrano {df_filtered.shape[1]} kolumn (pominięto długie tekstowe).")
                else:
                    df_filtered = df
                    st.info(f"Do raportu wybrano {df_filtered.shape[1]} kolumn (pełny zestaw).")

                profile = ProfileReport(df_filtered, minimal=minimal)
                st.session_state["profiling_report"] = profile
                st.success("Raport wygenerowany pomyślnie.")
            except Exception as e:
                st.session_state["profiling_report"] = None
                st.error(f"Wystąpił błąd podczas generowania raportu: {e}")
                return

    # Wyświetlenie raportu, jeśli został wygenerowany
    if st.session_state["profiling_report"] is not None:
        st_profile_report(st.session_state["profiling_report"])
