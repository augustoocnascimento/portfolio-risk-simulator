import streamlit as st
import datetime as dt
import sys
from pathlib import Path
import investpy

# Adiciona o diretório base ao sys.path
sys.path.append(str(Path(__file__).parents[1]))

from utils.calculations import var_historico, var_parametrico

def show():
    st.header("Calculadora VaR de Ações")
    
    
    stocks = investpy.stocks.get_stocks(country='brazil')
    all_tickers = stocks['symbol'].tolist()

    # Entradas do usuário
    ticker = st.multiselect("Ticker:", all_tickers)
    
    investimento = st.number_input("Valor do Investimento:", min_value=1000, max_value=1000000, value = 50_000)
    
    data_inicial = st.date_input("Data Inicial", dt.date(2020, 1, 1))
    
    data_final = st.date_input("Data Final", dt.date.today())
   
    nivel_confianca = st.slider("Nível de Confiança:", min_value=0.85, max_value=0.99, step=0.01, value=0.95)

    if st.button("Calcular VaR"):
        try:
            var_hist = var_historico(ticker, data_inicial, data_final, investimento, nivel_confianca)
            var_param = var_parametrico(ticker, data_inicial, data_final, investimento, nivel_confianca)
            
            st.write(f"VaR Histórico: R${var_hist:.2f}")
            st.write(f"VaR Paramétrico: R${var_param:.2f}")
        except ValueError as e:
            st.error(f"Erro: {e}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")