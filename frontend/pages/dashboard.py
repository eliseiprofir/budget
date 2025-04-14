import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Verificăm dacă utilizatorul este autentificat
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.error("You need to be logged in to access this page")
    st.stop()

st.title("Dashboard")
st.write("Welcome to your Budget Management Dashboard")

# Obținem date de la API
api = st.session_state.get('api')
user_info = api.get_user_info()
budgets = api.get_budgets()

# Afișăm informații despre utilizator
if user_info:
    st.write(f"Logged in as: {user_info.get('email', 'Unknown')}")

# Date exemplu pentru grafic
data = {
    'Category': ['Food', 'Transport', 'Entertainment', 'Utilities', 'Savings'],
    'Amount': [500, 300, 200, 400, 600]
}

# Dacă avem date reale, le folosim
if budgets:
    # Prelucrăm datele primite de la API
    # Aceasta depinde de structura exactă a datelor returnate
    pass

df = pd.DataFrame(data)

# Afișăm un grafic
st.subheader("Budget Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
ax.pie(df['Amount'], labels=df['Category'], autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# Afișăm datele în format tabelar
st.subheader("Budget Details")
st.dataframe(df, use_container_width=True)

# Secțiune pentru statistici
st.subheader("Statistics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Budget", "$2,000", "5%")
with col2:
    st.metric("Spent", "$1,400", "-10%")
with col3:
    st.metric("Remaining", "$600", "15%")