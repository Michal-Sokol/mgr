# utils/filters.py
import streamlit as st

def apply_global_filters(df):
    df_filtered = df.copy()

    # Kategoria
    if "filtr_kategoria" in st.session_state:
        df_filtered = df_filtered[df_filtered["kategoria"].isin(st.session_state["filtr_kategoria"])]

    # Zakres dat (datetime)
    if 'filtr_miesiac' in st.session_state:
        start, end = st.session_state["filtr_miesiac"]
        df_filtered = df_filtered[(df_filtered["miesiąc"] >= start) & (df_filtered["miesiąc"] <= end)]

    # Płeć
    if "filtr_plec" in st.session_state:
        df_filtered = df_filtered[df_filtered["płeć"].isin(st.session_state["filtr_plec"])]

    return df_filtered
