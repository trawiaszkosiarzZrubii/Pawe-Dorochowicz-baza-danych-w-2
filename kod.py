import streamlit as st
from supabase import create_client, Client
import random
import time

# --- Konfiguracja Strony i Motywu ---
st.set_page_config(
    page_title="Guild Master's Vault",
    page_icon="📜",
    layout="centered"
)

# --- STYLE CSS (Light / Parchment Theme) ---
st.markdown("""
<style>
    /* Import czcionki fantasy z Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato&display=swap');

    /* Główne tło aplikacji - Jasny Pergamin */
    .stApp {
        background-color: #fdfbf7;
        background-image: linear-gradient(to bottom, #fdfbf7, #f4eacc);
        color: #2c1e1e; /* Ciemny brąz - kolor atramentu */
    }

    /* Nagłówki - Styl Królewski */
    h1, h2, h3, h4 {
        font-family: 'Cinzel', serif !important;
        color: #8a1212 !important; /* Ciemna czerwień / Burgund */
        text-shadow: none;
        font-weight: 700;
    }

    /* Tekst zwykły */
    p, label, .stMarkdown {
        font-family: 'Lato', sans-serif;
        color: #3b2f2f !important; /* Ciemny szary/brąz dla czytelności */
        font-size: 1.05rem;
    }

    /* Pola tekstowe i inputy - Białe tło z obramowaniem */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea, 
    .stNumberInput > div > div > input, 
    .stSelectbox > div > div > div {
        background-color: #ffffff;
        color: #000000;
        border: 2px solid #8a1212; /* Burgundowa ramka */
        border-radius: 4px;
        font-family: 'Lato', sans-serif;
    }
    
    /* Kolor etykiet nad inputami */
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
        color: #5c4033 !important;
        font-weight: bold;
    }

    /* Przyciski - Styl Jasny ze złotem */
    .stButton > button {
        background-color: #fff8e1;
        color: #8a1212;
        border: 2px solid #8a1212;
        font-family: 'Cinzel', serif;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #8a1212;
        color: #fff; /* Biały tekst po najechaniu */
        border-color: #5c0a0a;
        transform: scale(1.02);
    }

    /* Karty (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e6dec5; /* Beżowy przycisk */
        border-radius: 5px 5px 0 0;
        color: #555555;
        font-family: 'Cinzel', serif;
        border: 1px solid #dcdcdc;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #8a1212; /* Aktywna karta - Burgund */
        color: #ffffff;
    }

    /* Tabela (Dataframe) */
    [data-testid="stDataFrame"] {
        border: 2px solid #8a1212;
        background-color: #fff;
    }

    /* Alerty i komunikaty */
    .stAlert {
        background-color: #fff8e1;
        border: 1px solid #8a1212;
        color: #3b2f2f;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f4eacc;
        border-right: 2px solid #d4c4a8;
    }
    [data-testid="stSidebar"] h2 {
        color: #8a1212 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Tytuł Aplikacji ---
st.title("🏰 Królewskie Rejestry Gildii")
st.markdown("**Oficjalny spis inwentarza (Baza Supabase)**")

# --- Połączenie z Supabase ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"💀 Błąd pieczęci królewskiej (połączenia): {e}")
        return None

supabase = init_connection()

if not supabase:
    st.stop()

# --- Sidebar: Skryba ---
with st.sidebar:
    st.header("⚖️ Panel Zarządcy")
    st.write("Witaj, Skrybo.")
    
    st.markdown("---")
    st.write("**Los dnia:**")
    if st.button("Rzuć kością k20"):
        roll = random.randint(1, 20)
        if roll == 20:
            st.success(f"WYNIK: {roll} - Fortuna sprzyja!")
            st.balloons()
        elif roll == 1:
            st.error(f"WYNIK: {roll} - Pech...")
        else:
            st.info(f"Wynik rzutu: **{roll}**")
    
    st.markdown("---")
    st.caption("System zarządzania magazynem v2.0 Light Theme")

# --- Zakładki ---
tab1, tab2, tab3 = st.tabs(["📜 Nowy Dekret (Kategoria)", "⚔️ Rejestracja Dóbr", "💎 Księga Inwentarza"])

# ==========================================
# ZAKŁADKA 1: DODAWANIE KATEGORII
# ==========================================
with tab1:
    st.header("Zdefiniuj Typ Dóbr")
    st.write("Wpisz nową kategorię do rejestru (np. Żywność, Uzbrojenie).")
    
    with st.form("category_form", clear_on_submit=True):
        cat_nazwa = st.text_input("Nazwa Kategorii")
        cat_opis = st.text_area("Opis przeznaczenia")
        
        submitted_cat = st.form_submit_button("✒️ Złóż Podpis i Zapisz")
        
        if submitted_cat:
            if cat_nazwa:
                try:
                    data = {
                        "nazwa": cat_nazwa,
                        "opis": cat_opis
                    }
                    supabase.table("Kategorie").insert(data).execute()
                    st.success(f"✅ Kategoria **{cat_nazwa}** została wpisana do ksiąg.")
                except Exception as e:
                    st.error(f"❌ Błąd zapisu atramentem: {e}")
            else:
                st.warning("⚠️ Pole nazwy nie może pozostać puste.")

# ==========================================
# ZAKŁADKA 2: DODAWANIE PRODUKTU
# ==========================================
with tab2:
    st.header("Przyjęcie Towaru")
    st.write("Wprowadź przedmiot do magazynu głównego.")

    # 1. Pobranie aktualnych kategorii
    try:
        response = supabase.table("Kategorie").select("ID, nazwa").execute()
        categories = response.data
    except Exception as e:
        st.error("❌ Nie udało się odczytać listy kategorii.")
        categories = []

    cat_options = {cat['nazwa']: cat['ID'] for cat in categories}

    if not categories:
        st.warning("📜 Brak kategorii. Udaj się do pierwszej zakładki, by je zdefiniować.")
    else:
        with st.form("product_form", clear_on_submit=True):
            col_icon, col_input = st.columns([1, 4])
            with col_icon:
                st.markdown("<h1 style='text-align: center;'>📦</h1>", unsafe_allow_html=True)
            with col_input:
                prod_nazwa = st.text_input("Nazwa Przedmiotu")
            
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                prod_liczba = st.number_input("Ilość sztuk", min_value=0, step=1, format="%d")
            with col2:
                prod_cena = st.number_input("Wartość jednostkowa (Złoto)", min_value=0.0, step=0.01, format="%.2f")
            
            selected_cat_name = st.selectbox("Przypisz do Kategorii", options=list(cat_options.keys()))
            
            submitted_prod = st.form_submit_button("🔨 Zatwierdź Przyjęcie")
            
            if submitted_prod:
                if prod_nazwa and selected_cat_name:
                    try:
                        with st.spinner('Skrybowie notują...'):
                            time.sleep(0.5)
                            cat_id = cat_options[selected_cat_name]
                            
                            data = {
                                "Nazwa": prod_nazwa,
                                "liczba": prod_liczba,
                                "cena": prod_cena,
                                "kategoria_ID": cat_id 
                            }
                            
                            supabase.table("Stół").insert(data).execute()
                        
                        st.success(f"✅ Przedmiot **{prod_nazwa}** dodany do stanu!")
                        
                    except Exception as e:
                        st.error(f"❌ Wystąpił błąd administracyjny: {e}")
                else:
                    st.warning("⚠️ Nazwa przedmiotu jest wymagana.")

# ==========================================
# ZAKŁADKA 3: PODGLĄD DANYCH
# ==========================================
with tab3:
    st.header("Stan Magazynowy")
    
    col_btn, col_txt = st.columns([1, 3])
    with col_btn:
        if st.button("🔄 Odśwież Księgi"):
            st.rerun()
            
    try:
        products_response = supabase.table("Stół").select("*").execute()
        products_data = products_response.data
        
        if products_data:
            st.markdown(f"W rejestrze znajduje się **{len(products_data)}** pozycji.")
            
            # Konfiguracja wyświetlania tabeli
            st.dataframe(
                products_data,
                use_container_width=True,
                column_config={
                    "id": st.column_config.NumberColumn("ID", format="%d"),
                    "Nazwa": st.column_config.TextColumn("Nazwa Towaru", help="Pełna nazwa inwentaryzacyjna"),
                    "cena": st.column_config.NumberColumn("Cena (gp)", format="%.2f gp"),
                    "liczba": st.column_config.ProgressColumn("Dostępność", min_value=0, max_value=100, format="%f szt."),
                    "Kategoria_ID": "ID Kategorii"
                }
            )
        else:
            st.info("📜 Księgi są puste.")
            
    except Exception as e:
        st.error("Nie można otworzyć ksiąg (Błąd połączenia).")
