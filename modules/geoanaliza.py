import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit.components.v1 import html

def run(df):
    st.title("\U0001F30E Geoanaliza")

    # --- Normalizacja nazw kolumn ---
    df.columns = [col.strip().lower() for col in df.columns]

    # --- Walidacja kolumn ---
    required_cols = ["stan", "suma", "miesiąc", "płeć", "przedział_wiekowy"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Brakuje kolumn w danych: {', '.join(missing_cols)}")
        return

    # --- Filtry ---
    with st.sidebar:
        st.header("\U0001F9F0 Filtry")

        df['miesiąc'] = pd.to_datetime(df['miesiąc'], format="%d.%m.%Y")

        min_date = df['miesiąc'].min().date()
        max_date = df['miesiąc'].max().date()

        val = st.session_state.get("filtr_miesiac", (min_date, max_date))
        default_start = pd.to_datetime(val[0]).date()
        default_end = pd.to_datetime(val[1]).date()

        date_range = st.slider(
            "\U0001F5D5️ Zakres dat",
            min_value=min_date,
            max_value=max_date,
            value=(default_start, default_end),
            format="YYYY-MM-DD"
        )
        st.session_state["filtr_miesiac"] = (
            pd.to_datetime(date_range[0]),
            pd.to_datetime(date_range[1])
        )

        df['suma'] = pd.to_numeric(df['suma'], errors='coerce')
        df = df.dropna(subset=['suma'])

        min_sum, max_sum = df['suma'].min(), df['suma'].max()

        def format_currency(x):
            if x >= 1e6:
                return f"{x/1e6:.2f}M"
            elif x >= 1e3:
                return f"{x/1e3:.2f}K"
            else:
                return f"{x:.2f}"

        suma_range = st.slider("\U0001F4B0 Zakres przychodu (suma)", float(min_sum), float(max_sum),
                               (float(min_sum), float(max_sum)),
                               format="%.2f",
                               label_visibility="visible")
        st.caption(f"Od: {format_currency(suma_range[0])} do {format_currency(suma_range[1])}")

        wiekowe = sorted(df['przedział_wiekowy'].dropna().unique())
        selected_wiek = st.multiselect("\U0001F465 Przedział wiekowy", wiekowe, default=wiekowe)

    # --- Przefiltrowanie danych ---
    df = df[(df['miesiąc'] >= pd.to_datetime(date_range[0])) & (df['miesiąc'] <= pd.to_datetime(date_range[1]))]
    df = df[df['suma'].between(suma_range[0], suma_range[1])]
    df = df[df['przedział_wiekowy'].isin(selected_wiek)]

    if df.empty:
        st.warning("Brak danych po filtracji. Zmień zakres dat lub inne filtry.")
        return

    # Układ siatki 2x2
    col1, col2 = st.columns(2)

    # W7: Przychód ogółem
    with col1:
        st.subheader("W7: Przychód ogółem")
        grouped = df.groupby("stan")["suma"].sum().reset_index()
        grouped["state_code"] = grouped["stan"]

        fig1 = px.choropleth(
            grouped,
            locations="state_code",
            locationmode="USA-states",
            color="suma",
            scope="usa",
            color_continuous_scale="RdYlGn_r",
            labels={"suma": "Przychód"}
        )
        fig1.update_traces(marker_line_width=0.5, marker_line_color="white")
        st.plotly_chart(fig1, use_container_width=True)

    # W8: Dystrybucja klientów wg wieku
    with col2:
        st.subheader("W8: Dystrybucja wieku klientów")
        if "ilość_produktów" not in df.columns:
            st.error("Brakuje kolumny \"ilość_produktów\" jako proxy liczby klientów")
            return
        grouped_wiek = df.groupby("stan")["ilość_produktów"].sum().reset_index()
        grouped_wiek["state_code"] = grouped_wiek["stan"]

        fig2 = px.choropleth(
            grouped_wiek,
            locations="state_code",
            locationmode="USA-states",
            color="ilość_produktów",
            scope="usa",
            color_continuous_scale="RdYlGn_r",
            labels={"ilość_produktów": "Klienci"}
        )
        fig2.update_traces(marker_line_width=0.5, marker_line_color="white")
        st.plotly_chart(fig2, use_container_width=True)

    # W9: Przychód od kobiet
    with col1:
        st.subheader("W9: Przychód od kobiet")
        kobiety = df[df['płeć'] == 'F'].groupby("stan")["przychód_generowany_przez_kobiety"].sum().reset_index()
        kobiety["state_code"] = kobiety["stan"]

        fig3 = px.choropleth(
            kobiety,
            locations="state_code",
            locationmode="USA-states",
            color="przychód_generowany_przez_kobiety",
            scope="usa",
            color_continuous_scale="RdYlGn_r",
            labels={"przychód_generowany_przez_kobiety": "Kobiety"}
        )
        fig3.update_traces(marker_line_width=0.5, marker_line_color="white")
        st.plotly_chart(fig3, use_container_width=True)

    # W10: Przychód od mężczyzn
    with col2:
        st.subheader("W10: Przychód od mężczyzn")
        faceci = df[df['płeć'] == 'M'].groupby("stan")["przychód_generowany_przez_mężczyzn"].sum().reset_index()
        faceci["state_code"] = faceci["stan"]

        fig4 = px.choropleth(
            faceci,
            locations="state_code",
            locationmode="USA-states",
            color="przychód_generowany_przez_mężczyzn",
            scope="usa",
            color_continuous_scale="RdYlGn_r",
            labels={"przychód_generowany_przez_mężczyzn": "Mężczyźni"}
        )
        fig4.update_traces(marker_line_width=0.5, marker_line_color="white")
        st.plotly_chart(fig4, use_container_width=True)
