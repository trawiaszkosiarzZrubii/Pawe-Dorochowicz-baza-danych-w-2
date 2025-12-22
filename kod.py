import streamlit as st
from supabase import create_client, Client

# --- Konfiguracja Strony ---
st.set_page_config(page_title="Supabase Manager", layout="centered")
st.title("📦 Zarządzanie Magazynem (Supabase)")

# --- Połączenie z Supabase ---
# Używamy st.cache_resource, aby nie łączyć się przy każdym kliknięciu
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Błąd konfiguracji sekretów: {e}")
        return None

supabase = init_connection()

if not supabase:
    st.stop()

# --- Zakładki ---
tab1, tab2, tab3 = st.tabs(["➕ Dodaj Kategorię", "🪑 Dodaj Produkt (Stół)", "📊 Podgląd Danych"])

# ==========================================
# ZAKŁADKA 1: DODAWANIE KATEGORII
# ==========================================
with tab1:
    st.header("Nowa Kategoria")
    
    with st.form("category_form", clear_on_submit=True):
        cat_nazwa = st.text_input("Nazwa kategorii")
        cat_opis = st.text_area("Opis kategorii")
        
        submitted_cat = st.form_submit_button("Zapisz kategorię")
        
        if submitted_cat:
            if cat_nazwa:
                try:
                    data = {
                        "nazwa": cat_nazwa,
                        "opis": cat_opis
                    }
                    supabase.table("Kategorie").insert(data).execute()
                    st.success(f"Dodano kategorię: {cat_nazwa}")
                except Exception as e:
                    st.error(f"Wystąpił błąd: {e}")
            else:
                st.warning("Nazwa kategorii jest wymagana.")

# ==========================================
# ZAKŁADKA 2: DODAWANIE PRODUKTU (STÓŁ)
# ==========================================
with tab2:
    st.header("Nowy Produkt")

    # 1. Pobranie aktualnych kategorii do listy wyboru
    try:
        response = supabase.table("Kategorie").select("ID, nazwa").execute()
        categories = response.data
    except Exception as e:
        st.error("Nie udało się pobrać kategorii.")
        categories = []

    # Tworzenie słownika {Nazwa: ID} dla łatwiejszego wyboru
    cat_options = {cat['nazwa']: cat['ID'] for cat in categories}

    if not categories:
        st.warning("Najpierw dodaj przynajmniej jedną kategorię w zakładce obok!")
    else:
        with st.form("product_form", clear_on_submit=True):
            prod_nazwa = st.text_input("Nazwa produktu")
            
            col1, col2 = st.columns(2)
            with col1:
                # int8 w bazie -> step=1
                prod_liczba = st.number_input("Liczba (ilość)", min_value=0, step=1, format="%d")
            with col2:
                # numeric w bazie -> float
                prod_cena = st.number_input("Cena", min_value=0.0, step=0.01, format="%.2f")
            
            selected_cat_name = st.selectbox("Wybierz kategorię", options=list(cat_options.keys()))
            
            submitted_prod = st.form_submit_button("Zapisz produkt")
            
            if submitted_prod:
                if prod_nazwa and selected_cat_name:
                    try:
                        # Pobranie ID na podstawie wybranej nazwy
                        cat_id = cat_options[selected_cat_name]
                        
                        data = {
                            "Nazwa": prod_nazwa,      # Zgodnie z obrazkiem (wielka litera N)
                            "liczba": prod_liczba,
                            "cena": prod_cena,
                            "kategoria_ID": cat_id
                        }
                        
                        # Tabela nazywa się "Stół" (z polskim znakiem)
                        supabase.table("Stół").insert(data).execute()
                        st.success(f"Dodano produkt: {prod_nazwa}")
                    except Exception as e:
                        st.error(f"Wystąpił błąd przy zapisie: {e}")
                else:
                    st.warning("Uzupełnij nazwę produktu.")

# ==========================================
# ZAKŁADKA 3: PODGLĄD (OPCJONALNIE)
# ==========================================
with tab3:
    st.subheader("Ostatnio dodane produkty")
    if st.button("Odśwież dane"):
        pass # Streamlit przeładuje skrypt i pobierze dane na nowo
        
    try:
        # Pobieramy dane i łączymy (join) z kategoriami dla czytelności
        # Składnia select: *, Kategorie(nazwa) wymaga ustawienia foreign key w Supabase
        products = supabase.table("Stół").select("*").execute()
        st.dataframe(products.data)
    except Exception as e:
        st.info("Brak danych lub błąd pobierania.")
