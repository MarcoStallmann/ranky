import streamlit as st
from ranky.database import Session, Stock

st.title("📊 Aktienverwaltung mit Ranky")

session = Session()

stocks = session.query(Stock).all()

st.subheader("Aktuelle Bestände")
if stocks:
    st.table([{
        "Aktienname": s.name,
        "ISIN": s.isin,
        "Bestand": s.quantity,
        "Kurs": s.price,
        "Marktwert": s.market_value
    } for s in stocks])
else:
    st.info("Noch keine Aktien eingetragen.")

st.subheader("Neue Aktie hinzufügen / bearbeiten")
with st.form("stock_form"):
    isin = st.text_input("ISIN")
    name = st.text_input("Aktienname")
    quantity = st.number_input("Bestand", min_value=0.0, step=1.0)
    price = st.number_input("Kurs", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Speichern")

    if submitted:
        stock = session.query(Stock).filter_by(isin=isin).first()
        if stock:
            stock.name = name
            stock.quantity = quantity
            stock.price = price
            st.success("Aktie aktualisiert.")
        else:
            new_stock = Stock(isin=isin, name=name, quantity=quantity, price=price)
            session.add(new_stock)
            st.success("Aktie hinzugefügt.")
        session.commit()
        st.experimental_rerun()
