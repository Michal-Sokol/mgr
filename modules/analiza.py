import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.filters import apply_global_filters

def run(df):
    st.title("📊 Analiza Konsumencka")

    # Konwersja kolumny 'miesiąc' na datetime
    df['miesiąc'] = pd.to_datetime(df['miesiąc'], format="%d.%m.%Y")

    # --- SIDEBAR Z FILTRAMI ---
    with st.sidebar:
        st.header("🔍 Filtry")

        # Zakres dat jako slider
        min_date = df['miesiąc'].min().date()
        max_date = df['miesiąc'].max().date()

        val = st.session_state.get("filtr_miesiac", (min_date, max_date))
        default_start = pd.to_datetime(val[0]).date()
        default_end = pd.to_datetime(val[1]).date()

        date_range = st.slider(
            "📅 Zakres dat",
            min_value=min_date,
            max_value=max_date,
            value=(default_start, default_end),
            format="MM/YYYY"
        )
        st.session_state["filtr_miesiac"] = (
            pd.to_datetime(date_range[0]),
            pd.to_datetime(date_range[1])
        )

        # Kategoria (multiselect)
        if "kategoria" in df.columns:
            all_kat = sorted(df['kategoria'].dropna().unique())
            default_kat = st.session_state.get("filtr_kategoria", all_kat)
            st.session_state["filtr_kategoria"] = st.multiselect(
                "📦 Kategoria",
                options=all_kat,
                default=default_kat
            )

        # Płeć (multiselect)
        if "płeć" in df.columns:
            all_plec = sorted(df['płeć'].dropna().unique())
            default_plec = st.session_state.get("filtr_plec", all_plec)
            st.session_state["filtr_plec"] = st.multiselect(
                "👤 Płeć",
                options=all_plec,
                default=default_plec
            )

        # Przycisk resetowania
        if st.button("🔄 Zresetuj filtry"):
            for key in ["filtr_kategoria", "filtr_miesiac", "filtr_plec"]:
                st.session_state.pop(key, None)
            st.rerun()

    # Zastosuj filtry
    df = apply_global_filters(df)

    # Formatowanie dodatkowe
    wiek_order = ["<20", "20-30", "30-40", "40-50", "50-60", "60-70", ">70"]
    df["przedział_wiekowy"] = pd.Categorical(df["przedział_wiekowy"], categories=wiek_order, ordered=True)

    # Layout w dwóch kolumnach 2x3
    col1, col2 = st.columns(2)

    # W1: Miesięczny przychód
    with col1:
        st.subheader("W1: Miesięczny Przychód")
        monthly = df.groupby('miesiąc')['suma'].sum().sort_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly.index,
            y=monthly.values,
            mode='lines+markers+text',
            name='Przychód miesięczny',
            line=dict(color='mediumorchid', width=3),
            text=[f"{val/1e6:.1f}M" for val in monthly.values],
            textposition="top center"
        ))

        fig.update_layout(
            title="\U0001F4C8 Miesięczny przychód (suma)",
            xaxis_title="Miesiąc",
            yaxis_title="Przychód",
            xaxis=dict(tickformat="%b %Y"),
            height=500,
            hovermode="x unified",
            margin=dict(t=50, b=50, l=30, r=30),
        )

        st.plotly_chart(fig, use_container_width=True)

    # W4: Udział grup wiekowych w przychodach
    with col2:
        st.subheader("W4: Przychód wg grup wiekowych")
        age = df.groupby('przedział_wiekowy')['suma'].sum().reindex(wiek_order)

        fig4 = px.bar(
            x=age.index,
            y=age.values,
            text=[f"{v/1e6:.1f}M" for v in age.values],
            title="\U0001F4CA Przychód z podziałem na grupy wiekowe"
        )
        fig4.update_traces(marker_color='lightskyblue', textposition='outside')
        fig4.update_layout(
            xaxis_title="Grupa wiekowa",
            yaxis_title="Przychód",
            height=500,
            margin=dict(t=50, b=50, l=30, r=30)
        )

        st.plotly_chart(fig4, use_container_width=True)

    # Nowy wiersz — kolumny na kolejne wykresy
    col3, col4 = st.columns(2)

    # W2: Procentowy udział regionów w przychodach
    with col3:
        st.subheader("W2: Przychód wg regionu [%]")
        regional = df.groupby('region')['suma'].sum().sort_values(ascending=False)

        fig2 = px.pie(
            names=regional.index,
            values=regional.values,
            hole=0.4,
            title="Udział procentowy przychodów wg regionu"
        )
        fig2.update_traces(
            textinfo='percent+label',
            pull=[0.05] * len(regional),
            marker=dict(line=dict(color="#000000", width=1))
        )
        fig2.update_layout(height=500)

        st.plotly_chart(fig2, use_container_width=True)

    # W5: Średnia suma zamówień miesięcznie
    with col4:
        st.subheader("W5: Średnia suma zamówień")
        avg_sum = df.groupby('miesiąc')['średnia suma'].mean().sort_index()

        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=avg_sum.index,
            y=avg_sum.values,
            mode='lines+markers+text',
            name='Średnia suma',
            line=dict(color='mediumvioletred', width=3),
            text=[f"{val:.0f}" for val in avg_sum.values],
            textposition='top center'
        ))

        fig5.update_layout(
            title="\U0001F4C8 Średnia suma zamówień miesięcznie",
            xaxis_title="Miesiąc",
            yaxis_title="Średnia suma",
            xaxis=dict(tickformat="%b %Y"),
            height=500,
            hovermode="x unified",
            margin=dict(t=50, b=50, l=30, r=30),
        )

        st.plotly_chart(fig5, use_container_width=True)

    # Trzeci wiersz — kolumny na kolejne wykresy
    col5, col6 = st.columns(2)

    # W3: TOP 7 dostawców płatności
    with col5:
        st.subheader("W3: TOP 7 dostawców płatności")
        top7 = df.groupby('metoda_płatności')['suma'].sum().nlargest(7)

        fig3 = px.pie(
            names=top7.index,
            values=top7.values,
            title="Udział 7 największych dostawców płatności",
            hole=0.3
        )
        fig3.update_traces(textinfo='percent+label')
        fig3.update_layout(height=500)

        st.plotly_chart(fig3, use_container_width=True)


    # W6: Przychód wg kategorii i płci (wykres motylkowy)
    with col6:
        st.subheader("W6: Przychód wg kategorii i płci")

        # Przygotowanie danych
        df['płeć'] = df['płeć'].replace({
            'F': 'Kobieta', 'M': 'Mężczyzna',
            'f': 'Kobieta', 'm': 'Mężczyzna',
            'Female': 'Kobieta', 'Male': 'Mężczyzna'
        })

        if 'Kobieta' not in df['płeć'].unique() or 'Mężczyzna' not in df['płeć'].unique():
            st.warning("Brakuje danych dla jednej z płci.")
        else:
            grouped = df.groupby(['kategoria', 'płeć'])['suma'].sum().unstack(fill_value=0)
            grouped['suma'] = grouped['Kobieta'] + grouped['Mężczyzna']
            grouped = grouped.sort_values('suma', ascending=True)  # sortowanie rosnące

            fig6 = go.Figure()
            fig6.add_trace(go.Bar(
                y=grouped.index,
                x=-grouped['Kobieta'],
                name='Kobiety',
                orientation='h',
                marker=dict(color='lightpink'),
                text=[f"{val/1e6:.1f}M" for val in grouped['Kobieta']],
                textposition='auto',
                cliponaxis=False
            ))
            fig6.add_trace(go.Bar(
                y=grouped.index,
                x=grouped['Mężczyzna'],
                name='Mężczyźni',
                orientation='h',
                marker=dict(color='cornflowerblue'),
                text=[f"{val/1e6:.1f}M" for val in grouped['Mężczyzna']],
                textposition='auto',
                cliponaxis=False
            ))

            max_val = max(grouped[['Kobieta', 'Mężczyzna']].max())
            tick_range = int((max_val // 2e7 + 1) * 2e7)
            tickvals = [-tick_range, -tick_range//2, 0, tick_range//2, tick_range]
            ticktext = [f"{abs(val)//1e6:.0f}M" if val != 0 else "0" for val in tickvals]

            fig6.update_layout(
                title="W6: Przychód wg kategorii i płci (wykres motylkowy)",
                barmode='relative',
                xaxis=dict(
                    title="Przychód",
                    tickvals=tickvals,
                    ticktext=ticktext
                ),
                yaxis_title="Kategoria",
                height=700,
                margin=dict(t=50, b=50, l=120, r=120)
            )

            st.plotly_chart(fig6, use_container_width=True)

