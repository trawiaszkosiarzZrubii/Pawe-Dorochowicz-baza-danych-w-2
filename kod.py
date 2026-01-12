import streamlit as st
from supabase import create_client, Client
import random
import time

# --- Konfiguracja Strony i Motywu ---
st.set_page_config(
    page_title="Guild Master's Vault",
    page_icon="🐉",
    layout="wide"  # Zmieniono na wide, aby zmieścić smoki po bokach
)

# --- STYLE CSS (Light / Parchment Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato&display=swap');

    /* Tło całej strony - kolor ściany/stołu pod pergaminem */
    .stApp {
        background-color: #2b2b2b;
    }

    /* Środkowa kolumna - imitacja pergaminu */
    [data-testid="column"]:nth-of-type(2) {
        background-color: #fdfbf7;
        background-image: linear-gradient(to bottom, #fdfbf7, #f4eacc);
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #d4c4a8;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
    }

    /* Nagłówki */
    h1, h2, h3, h4 {
        font-family: 'Cinzel', serif !important;
        color: #8a1212 !important;
        text-shadow: none;
        font-weight: 700;
    }

    /* Tekst */
    p, label, .stMarkdown, .stCaption {
        font-family: 'Lato', sans-serif;
        color: #3b2f2f !important;
        font-size: 1.05rem;
    }

    /* Inputy */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea, 
    .stNumberInput > div > div > input, 
    .stSelectbox > div > div > div {
        background-color: #ffffff;
        color: #000000;
        border: 2px solid #8a1212;
        border-radius: 4px;
        font-family: 'Lato', sans-serif;
    }
    
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
        color: #5c4033 !important;
        font-weight: bold;
    }

    /* Przyciski */
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
        color: #fff;
        border-color: #5c0a0a;
        transform: scale(1.02);
    }

    /* Zakładki (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e6dec5;
        border-radius: 5px 5px 0 0;
        color: #555555;
        font-family: 'Cinzel', serif;
        border: 1px solid #dcdcdc;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #8a1212;
        color: #ffffff;
    }

    /* Tabela */
    [data-testid="stDataFrame"] {
        border: 2px solid #8a1212;
        background-color: #fff;
    }

    /* Sidebar - dopasowanie do ciemnego tła zewnętrznego */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        border-right: 1px solid #333;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p {
        color: #d4c4a8 !important;
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
        return None

supabase = init_connection()

if not supabase:
    st.error("💀 Błąd połączenia z bazą danych (Sprawdź secrets).")
    st.stop()

# --- UKŁAD KOLUMN (SMOKI PO BOKACH) ---
# Dzielimy ekran na: [Lewy Smok] - [Główny Pergamin] - [Prawy Smok]
col_left, col_center, col_right = st.columns([1, 2, 1])

# --- LEWY SMOK ---
with col_left:
    st.write("") # Pusty odstęp, by obniżyć obrazek jeśli trzeba
    st.write("")
    # URL do herbowego smoka (czerwony)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Dragon_rampant_gules.svg/800px-Dragon_rampant_gules.svg.png", use_container_width=True)
    st.caption("Strażnik Zachodu")

# --- PRAWY SMOK ---
with col_right:
    st.write("")
    st.write("")
    # URL do herbowego smoka (zielony) - odwrócimy go (w CSS ciężko, więc używamy innego lub po prostu wstawiamy)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Dragon_rampant_vert.svg/800px-Dragon_rampant_vert.svg.png", use_container_width=True)
    st.caption("Strażnik Wschodu")

# --- GŁÓWNA ZAWARTOŚĆ (ŚRODEK) ---
with col_center:
    st.title("🏰 Królewskie Rejestry Gildii")
    st.markdown("**Oficjalny spis inwentarza (Baza Supabase)**")
    
    # --- Sidebar (został w standardowym miejscu po lewej stronie ekranu, niezależnie od kolumn) ---
    with st.sidebar:
        st.header("⚖️ Panel Zarządcy")
        st.write("Witaj, Skrybo.")
        st.markdown("---")
        if st.button("Rzuć kością k20"):
            roll = random.randint(1, 20)
            if roll == 20:
                st.balloons()
                st.success(f"CRITICAL HIT: {roll}!")
            else:
                st.info(f"Wynik rzutu: **{roll}**")

    # --- ZMIENIONA KOLEJNOŚĆ ZAKŁADEK ---
    # Tab 1: Rejestracja (dawniej Tab 2)
    # Tab 2: Dekret (dawniej Tab 1)
    # Tab 3: Księga (bez zmian)
    tab1, tab2, tab3 = st.tabs(["⚔️ Rejestracja Dóbr", "📜 Nowy Dekret (Kategoria)", "💎 Księga Inwentarza"])

    # ==========================================
    # ZAKŁADKA 1: DODAWANIE PRODUKTU (Teraz pierwsza)
    # ==========================================
    with tab1:
        st.header("Przyjęcie Towaru")
        st.write("Wprowadź przedmiot do magazynu głównego.")

        # Pobranie kategorii
        try:
            response = supabase.table("Kategorie").select("ID, nazwa").execute()
            categories = response.data
        except Exception:
            categories = []

        cat_options = {cat['nazwa']: cat['ID'] for cat in categories}

        if not categories:
            st.warning("📜 Brak kategorii. Przejdź do zakładki 'Nowy Dekret', by je zdefiniować.")
        else:
            with st.form("product_form", clear_on_submit=True):
                col_icon, col_input = st.columns([1, 5])
                with col_icon:
                    st.markdown("<h1 style='text-align: center;'>📦</h1>", unsafe_allow_html=True)
                with col_input:
                    prod_nazwa = st.text_input("Nazwa Przedmiotu")
                
                st.markdown("---")
                col_a, col_b = st.columns(2)
                with col_a:
                    prod_liczba = st.number_input("Ilość sztuk", min_value=0, step=1, format="%d")
                with col_b:
                    prod_cena = st.number_input("Wartość (Złoto)", min_value=0.0, step=0.01, format="%.2f")
                
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
                            st.error(f"❌ Błąd: {e}")
                    else:
                        st.warning("⚠️ Nazwa przedmiotu jest wymagana.")

    # ==========================================
    # ZAKŁADKA 2: DODAWANIE KATEGORII (Teraz druga)
    # ==========================================
    with tab2:
        st.header("Zdefiniuj Typ Dóbr")
        st.write("Wpisz nową kategorię do rejestru.")
        
        with st.form("category_form", clear_on_submit=True):
            cat_nazwa = st.text_input("Nazwa Kategorii (np. Bronie, Eliksiry)")
            cat_opis = st.text_area("Opis przeznaczenia")
            
            submitted_cat = st.form_submit_button("✒️ Złóż Podpis i Zapisz")
            
            if submitted_cat:
                if cat_nazwa:
                    try:
                        data = {"nazwa": cat_nazwa, "opis": cat_opis}
                        supabase.table("Kategorie").insert(data).execute()
                        st.success(f"✅ Kategoria **{cat_nazwa}** została wpisana do ksiąg.")
                        time.sleep(1)
                        st.rerun() # Odśwież, aby zaktualizować listę w pierwszej zakładce
                    except Exception as e:
                        st.error(f"❌ Błąd zapisu: {e}")
                else:
                    st.warning("⚠️ Pole nazwy nie może być puste.")

    # ==========================================
    # ZAKŁADKA 3: PODGLĄD DANYCH
    # ==========================================
    with tab3:
        st.header("Stan Magazynowy")
        
        col_btn, col_rest = st.columns([1, 4])
        with col_btn:
            if st.button("🔄 Odśwież"):
                st.rerun()
                
        try:
            products_response = supabase.table("Stół").select("*").execute()
            products_data = products_response.data
            
            if products_data:
                st.dataframe(
                    products_data,
                    use_container_width=True,
                    column_config={
                        "id": st.column_config.NumberColumn("ID", format="%d"),
                        "Nazwa": st.column_config.TextColumn("Nazwa Towaru"),
                        "cena": st.column_config.NumberColumn("Wartość", format="%.2f gp"),
                        "liczba": st.column_config.ProgressColumn("Stan", min_value=0, max_value=100, format="%f"),
                        "Kategoria_ID": "ID Kat."
                    }
                )
            else:
                st.info("📜 Pusto w księgach.")
        except Exception:
            st.error("Błąd połączenia.")
