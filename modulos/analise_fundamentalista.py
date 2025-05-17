import streamlit as st
import yfinance as yf


def show():
    st.header('Análise Fundamentalista')

    ticker = st.text_input('Digite o ticker da ação', 'AAPL')

    if ticker:
        stock = yf.Ticker(ticker)
        info = stock.info

        if info:
            st.write(info)
        else:
            st.error("Não foram encontrados dados fundamentalistas para o ticker fornecido.")
