import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from serpapi import GoogleSearch
import re

def compare(med_name):
    params = {
        "engine": "google_shopping",
        "q": med_name,
        "api_key": "0afbf2cc9910429995c2f7d49bed72ed2723d3b8866b7f416c7812a935f3f8a8",
        "gl": "in",
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results.get("shopping_results", [])
    return shopping_results

c1, c2 = st.columns(2)
c1.image("e_pharmacy.png", width=200)
c2.header("E-Pharmacy Price Comparison System")

st.sidebar.title("Enter Medicine Name:")
med_name = st.sidebar.text_input("Enter Name here 👇:")
number = st.sidebar.text_input("Enter Number of options here 👇:")

medicine_comp = []
med_price = []

if med_name.strip() != "":
    if st.sidebar.button("Price Compare"):
        shopping_results = compare(med_name)
        
        if not shopping_results:
            st.error("No results found!")
        else:
            # Validate number input
            num_options = int(number) if number.isdigit() else len(shopping_results)
            num_options = min(num_options, len(shopping_results))  # prevent index error

            # Find lowest price
            lowest_price = parse_price(shopping_results[0].get('price'))
            lowest_price_index = 0

            st.sidebar.image(shopping_results[0].get('thumbnail'))


for i in range(num_options):
    result = shopping_results[i]
    current_price = parse_price(result.get("price"))
    medicine_comp.append(result.get("source"))
    med_price.append(current_price)

    st.title(f"Option {i+1}")
    c1, c2 = st.columns(2)  # <- ये line aligned with st.title, same indentation
    c1.write("Company:")
    c2.write(result.get("source"))


                c1.write("Medicine Name:")
                c2.write(result.get("title"))

                c1.write("Price:")
                c2.write(result.get("price"))

                c1.write("Buy Link:")
                c2.write(f"[Link]({result.get('product_link')})")
    

                # Check for lowest price
                if current_price < lowest_price:
                    lowest_price = current_price
                    lowest_price_index = i
st.title("Best Option:")
            c1, c2 = st.columns(2)
            best_result = shopping_results[lowest_price_index]

            c1.write("Company:")
            c2.write(best_result.get("source"))

            c1.write("Medicine Name:")
            c2.write(best_result.get("title"))

            c1.write("Price:")
            c2.write(best_result.get("price"))

            c1.write("Buy Link:")
            c2.write(f"[Link]({best_result.get('product_link')})")


 df = pd.DataFrame({'Price': med_price}, index=medicine_comp)
            st.title("Chart Comparison:")
            st.bar_chart(df)

            fig, ax = plt.subplots()
            ax.pie(med_price, labels=medicine_comp, shadow=True, autopct='%1.1f%%')
            ax.axis("equal")
            st.pyplot(fig)






















