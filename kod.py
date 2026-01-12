import streamlit as st
from supabase import create_client, Client
import random
import time

# --- Konfiguracja Strony ---
st.set_page_config(
    page_title="Guild Master's Vault",
    page_icon="🐉",
    layout="wide" # Zmienione na wide, aby smoki po bokach miały miejsce
)

# --- STYLE CSS (Jasny Pergamin + Poprawiona czytelność) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato&display=swap');

    .stApp {
        background-color: #fdfbf7;
        background-image: linear-gradient(to bottom, #fdfbf7, #f4eacc);
        color: #2c1e1e;
    }

    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: #FF0000 !important;
        font-weight: 700;
    }

    p, label {
        font-family: 'Lato', sans-serif;
        color: #3b2f2f !important;
    }

    /* Stylizacja przycisków */
    .stButton > button {
        background-color: #fff8e1;
        color: #FF0000;
        border: 2px solid #FF0000;
        font-family: 'Cinzel', serif;
    }
    
    .stButton > button:hover {
        background-color: #FF0000;
        color: #ffffff;
    }

    /* Karty */
    .stTabs [data-baseweb="tab"] {
        background-color: #e6dec5;
        color: #555555;
        font-family: 'Cinzel', serif;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #FF0000;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# --- Połączenie z Supabase ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"💀 Błąd połączenia: {e}")
        return None

supabase = init_connection()

# --- UKŁAD GŁÓWNY (3 Kolumny: Smok - Treść - Smok) ---
col_left, col_main, col_right = st.columns([1, 4, 1])

with col_left:
    st.image("https://db4sgowjqfwig.cloudfront.net/campaigns/154443/assets/704772/Dragon_Statue_Left.png", use_container_width=True)
    st.image("https://www.pngarts.com/files/1/Dragon-PNG-Free-Download.png", use_container_width=True)

with col_right:
    st.image("https://pngimg.com/uploads/dragon/dragon_PNG84.png", use_container_width=True)
    st.image("https://vignette.wikia.nocookie.net/forgottenrealms/images/a/a2/Red_dragon.png", use_container_width=True)

# --- TREŚĆ GŁÓWNA ---
with col_main:
    st.title("🏰 Królewskie Rejestry Gildii")
    
    if not supabase:
        st.stop()

    # --- Zakładki (ZAMienione miejscami zgodnie z prośbą) ---
    # 1. Rejestracja Dóbr, 2. Nowy Dekret, 3. Księga Inwentarza
    tab1, tab2, tab3 = st.tabs(["⚔️ Rejestracja Dóbr", "📜 Nowy Dekret (Kategoria)", "💎 Księga Inwentarza"])

    # ==========================================
    # ZAKŁADKA 1: DODAWANIE PRODUKTU (Teraz jako pierwsza)
    # ==========================================
    with tab1:
        st.header("Przyjęcie Towaru")
        try:
            response = supabase.table("Kategorie").select("ID, nazwa").execute()
            categories = response.data
            cat_options = {cat['nazwa']: cat['ID'] for cat in categories}
            
            if not categories:
                st.warning("📜 Brak kategorii. Najpierw wydaj Nowy Dekret!")
            else:
                with st.form("product_form", clear_on_submit=True):
                    prod_nazwa = st.text_input("Nazwa Przedmiotu")
                    c1, c2 = st.columns(2)
                    prod_liczba = c1.number_input("Ilość", min_value=0, step=1)
                    prod_cena = c2.number_input("Wartość (gp)", min_value=0.0, step=0.01)
                    selected_cat_name = st.selectbox("Kategoria", options=list(cat_options.keys()))
                    
                    if st.form_submit_button("🔨 Zatwierdź Przyjęcie"):
                        if prod_nazwa:
                            data = {"Nazwa": prod_nazwa, "liczba": prod_liczba, "cena": prod_cena, "kategoria_ID": cat_options[selected_cat_name]}
                            supabase.table("Stół").insert(data).execute()
                            st.success("✅ Dodano do skarbca!")
                        else:
                            st.error("⚠️ Podaj nazwę!")
        except:
            st.error("Błąd bazy danych.")

    # ==========================================
    # ZAKŁADKA 2: DODAWANIE KATEGORII (Teraz jako druga)
    # ==========================================
    with tab2:
        st.header("Zdefiniuj Typ Dóbr")
        with st.form("category_form", clear_on_submit=True):
            cat_nazwa = st.text_input("Nazwa Kategorii")
            cat_opis = st.text_area("Opis")
            if st.form_submit_button("✒️ Złóż Podpis"):
                if cat_nazwa:
                    supabase.table("Kategorie").insert({"nazwa": cat_nazwa, "opis": cat_opis}).execute()
                    st.success(f"✅ Kategoria {cat_nazwa} zapisana.")
                else:
                    st.warning("⚠️ Brak nazwy!")

    # ==========================================
    # ZAKŁADKA 3: PODGLĄD
    # ==========================================
    with tab3:
        st.header("Stan Magazynowy")
        if st.button("🔄 Odśwież"):
            st.rerun()
        try:
            products = supabase.table("Stół").select("*").execute()
            if products.data:
                st.dataframe(products.data, use_container_width=True)
            else:
                st.info("Skarbiec jest pusty.")
        except:
            st.error("Nie można otworzyć ksiąg.")

# --- Panel Boczny (Sidebar) ---
with st.sidebar:
    st.header("🎲 Rzuć kością K20")
    if st.button("Rzuć k20"):
        res = random.randint(1, 20)
        st.subheader(f"Wynik: {res}")
        if res == 20: st.balloons()
            
