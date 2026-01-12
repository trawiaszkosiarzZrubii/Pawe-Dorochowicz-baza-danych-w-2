import streamlit as st
from supabase import create_client, Client
import random
import time

# --- Konfiguracja Strony i Motywu ---
st.set_page_config(
    page_title="Guild Master's Vault",
    page_icon="🐉",
    layout="centered"
)

# --- STYLE CSS (D&D Theme) ---
# Wstrzykujemy kod CSS, aby zmienić wygląd standardowego Streamlit
st.markdown("""
<style>
    /* Import czcionki fantasy z Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato&display=swap');

    /* Główne tło aplikacji - ciemny loch */
    .stApp {
        background-color: #1a1a1a;
        background-image: linear-gradient(to bottom right, #1a1a1a, #2d2d2d);
        color: #e0d6c2;
    }

    /* Nagłówki */
    h1, h2, h3, h4 {
        font-family: 'Cinzel', serif !important;
        color: #ffcc00 !important;
        text-shadow: 2px 2px 4px #000000;
    }

    /* Pola tekstowe i inputy */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stNumberInput > div > div > input, .stSelectbox > div > div > div {
        background-color: #2b2b2b;
        color: #ffffff;
        border: 2px solid #5c4033;
        border-radius: 5px;
        font-family: 'Lato', sans-serif;
    }

    /* Przyciski - Styl starego zwoju/przycisku magicznego */
    .stButton > button {
        background-color: #5c0a0a;
        color: #ffcc00;
        border: 2px solid #ffcc00;
        font-family: 'Cinzel', serif;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #8a1212;
        box-shadow: 0 0 10px #ffcc00;
        transform: scale(1.02);
    }

    /* Karty (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #2b2b2b;
        border-radius: 5px 5px 0 0;
        color: #aaaaaa;
        font-family: 'Cinzel', serif;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #5c0a0a;
        color: #ffcc00;
    }

    /* Alerty i komunikaty */
    .stAlert {
        background-color: #2b2b2b;
        border: 1px solid #ffcc00;
        color: #e0d6c2;
    }
</style>
""", unsafe_allow_html=True)

# --- Tytuł Aplikacji ---
st.title("🏰 Skarbiec Gildii Kupieckiej")
st.markdown("*Zarządzaj ekwipunkiem, zwojami i artefaktami (Baza Supabase)*")

# --- Połączenie z Supabase ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"💀 Krytyczny błąd rzucania zaklęcia połączenia: {e}")
        return None

supabase = init_connection()

if not supabase:
    st.stop()

# --- Sidebar: Mistrz Podziemi ---
with st.sidebar:
    st.header("🎲 Panel Mistrza Gry")
    st.write("Witaj w panelu zarządzania.")
    if st.button("Rzuć kością k20"):
        roll = random.randint(1, 20)
        st.success(f"Wyrzuciłeś: **{roll}**")
        if roll == 20:
            st.balloons()
            st.write("KRYTYCZNY SUKCES! 🌟")
        elif roll == 1:
            st.error("KRYTYCZNA PORAŻKA! 💀")
    
    st.markdown("---")
    st.info("💡 Pamiętaj: Każdy przedmiot musi mieć przypisaną kategorię (Typ Magii/Przedmiotu).")

# --- Zakładki ---
tab1, tab2, tab3 = st.tabs(["📜 Spisz Nowy Typ", "⚔️ Wykuj Przedmiot", "💎 Przegląd Skarbca"])

# ==========================================
# ZAKŁADKA 1: DODAWANIE KATEGORII (RPG Style)
# ==========================================
with tab1:
    st.header("Nowa Kategoria Ekwipunku")
    st.write("Dodaj nowy typ przedmiotów do ksiąg gildii (np. Mikstury, Broń, Zwoje).")
    
    with st.form("category_form", clear_on_submit=True):
        cat_nazwa = st.text_input("Nazwa Kategorii (np. Bronie Dwuręczne)")
        cat_opis = st.text_area("Opis (Lore / Zastosowanie)")
        
        submitted_cat = st.form_submit_button("✒️ Spisz w Kronikach")
        
        if submitted_cat:
            if cat_nazwa:
                try:
                    data = {
                        "nazwa": cat_nazwa,
                        "opis": cat_opis
                    }
                    supabase.table("Kategorie").insert(data).execute()
                    st.success(f"📜 Sukces! Kategoria **{cat_nazwa}** została dodana do kronik.")
                except Exception as e:
                    st.error(f"🔮 Mroczna magia zablokowała zapis: {e}")
            else:
                st.warning("⚠️ Musisz nadać nazwę, zanim spiszesz kategorię.")

# ==========================================
# ZAKŁADKA 2: DODAWANIE PRODUKTU (Stół -> Ekwipunek)
# ==========================================
with tab2:
    st.header("Dodaj do Inwentarza")
    st.write("Wprowadź nowy artefakt lub mebel do magazynu.")

    # 1. Pobranie aktualnych kategorii
    try:
        response = supabase.table("Kategorie").select("ID, nazwa").execute()
        categories = response.data
    except Exception as e:
        st.error("❌ Nie udało się odczytać zwojów z kategoriami.")
        categories = []

    cat_options = {cat['nazwa']: cat['ID'] for cat in categories}

    if not categories:
        st.warning("🕯️ Twoje zwoje są puste. Dodaj najpierw kategorię w pierwszej zakładce!")
    else:
        with st.form("product_form", clear_on_submit=True):
            col_img, col_data = st.columns([1, 2])
            
            with col_img:
                st.markdown("### 🛡️") # Ikona obok formularza
            
            with col_data:
                prod_nazwa = st.text_input("Nazwa Przedmiotu/Stołu")
            
            col1, col2 = st.columns(2)
            with col1:
                prod_liczba = st.number_input("Ilość w Magazynie", min_value=0, step=1, format="%d")
            with col2:
                prod_cena = st.number_input("Wartość (sztuki złota)", min_value=0.0, step=0.01, format="%.2f")
            
            selected_cat_name = st.selectbox("Typ Przedmiotu (Kategoria)", options=list(cat_options.keys()))
            
            submitted_prod = st.form_submit_button("🔨 Wykuj i Dodaj")
            
            if submitted_prod:
                if prod_nazwa and selected_cat_name:
                    try:
                        with st.spinner('Kowale pracują...'):
                            time.sleep(0.5) # Mały efekt oczekiwania dla klimatu
                            
                            cat_id = cat_options[selected_cat_name]
                            
                            # Używamy kluczy zgodnie z Twoją bazą danych
                            data = {
                                "Nazwa": prod_nazwa,  # Wielka litera N, jak na obrazku
                                "liczba": prod_liczba,
                                "cena": prod_cena,
                                "kategoria_ID": cat_id # Uwaga na wielkość liter w Supabase!
                            }
                            
                            # Tabela "Stół"
                            supabase.table("Stół").insert(data).execute()
                        
                        st.success(f"⚔️ Przedmiot **{prod_nazwa}** trafił do skarbca!")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"👹 Gobliny ukradły dane! Błąd: {e}")
                else:
                    st.warning("⚠️ Każdy przedmiot musi mieć nazwę.")

# ==========================================
# ZAKŁADKA 3: PODGLĄD DANYCH
# ==========================================
with tab3:
    st.header("Zawartość Skarbca")
    
    col_refresh, col_info = st.columns([1, 4])
    with col_refresh:
        if st.button("🔄 Przelicz"):
            st.rerun()
    
    try:
        # Pobieranie danych
        products_response = supabase.table("Stół").select("*").execute()
        products_data = products_response.data
        
        # Opcjonalnie: Pobranie nazw kategorii, aby wyświetlić nazwę zamiast ID
        # (Wymagałoby mapowania w Pythonie lub Join w Supabase)
        
        if products_data:
            st.markdown(f"### Znaleziono **{len(products_data)}** unikalnych artefaktów.")
            
            # Wyświetlanie jako tabela z customową konfiguracją
            st.dataframe(
                products_data,
                use_container_width=True,
                column_config={
                    "id": st.column_config.NumberColumn("ID", format="%d"),
                    "Nazwa": st.column_config.TextColumn("Artefakt", help="Nazwa przedmiotu"),
                    "cena": st.column_config.NumberColumn("Wartość (gp)", format="%.2f gp"),
                    "liczba": st.column_config.ProgressColumn("Stan Magazynowy", min_value=0, max_value=100, format="%f szt."),
                    "Kategoria_ID": "ID Kategorii"
                }
            )
        else:
            st.info("🕸️ Skarbiec jest pusty. Pora wyruszyć na wyprawę!")
            
    except Exception as e:
        st.error("Błąd odczytu ksiąg wieczystych.")
