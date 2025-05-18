import pandas as pd
from scipy.stats import norm
import numpy as np
import streamlit as st



################################## RISCO ##################################################
try:
    import yfinance as yf
except ImportError:
    print("Erro ao importar yfinance. Verifique sua instalação ou conexão com a internet.")

import numpy as np
import yfinance as yf

def var_historico(ativos, data_inicial, data_final, investimento, nivel_confianca):
    if len(ativos) == 0:
        raise ValueError("A lista de ativos não pode estar vazia.")

    # Preco do fechamento para todos os ativos
    dados = {}
    for ativo in ativos:
        ativo_tratado = ativo.upper().replace(" ", "") + ".SA"
        dados[ativo_tratado] = yf.download(ativo_tratado, start=data_inicial, end=data_final)['Close']

    # Erro para ativos sem preço
    for ativo_tratado, precos in dados.items():
        if precos.empty:
            raise ValueError(f"Não foram encontrados dados para o ativo {ativo_tratado} no período especificado.")


    precos_df = pd.DataFrame(dados).dropna()
    retornos_logaritmicos = np.log(precos_df / precos_df.shift(1)).dropna()
    cov_matrix = retornos_logaritmicos.cov()
    cotacoes_finais = precos_df.iloc[-1]

    # Cálculo dos pesos com base nas cotações finais
    pesos = cotacoes_finais / cotacoes_finais.sum()

    # Verifica se a soma dos pesos é igual a 1 (se não for, normaliza)
    if pesos.sum() != 1:
        pesos = pesos / pesos.sum()

    # Calcula a variância do portfólio
    var_portfolio = np.dot(pesos.T, np.dot(cov_matrix, pesos))

    # Calcula o VaR histórico com base no nível de confiança
    var_percentil = np.percentile(retornos_logaritmicos.values, (1 - nivel_confianca) * 100)
    var_hist = investimento * var_percentil * np.sqrt(var_portfolio)
    
    return var_hist


def var_parametrico(ativo, data_inicial, data_final, investimento, nivel_confianca):
    ativo_tratado = ativo.upper().replace(" ", "") + ".SA"
    dados = yf.download(ativo_tratado, start=data_inicial, end=data_final)
    precos = dados['Close']
    if precos.empty:
        raise ValueError(f"Não foram encontrados dados para o ativo {ativo_tratado} no período especificado.")

    retornos_logaritmicos = [np.log(precos.iloc[i] / precos.iloc[i-1]) for i in range(1, len(precos))]
    vol_ativo = np.std(retornos_logaritmicos)
    var_param = investimento * norm.ppf(1 - nivel_confianca) * vol_ativo
    
    return var_param


# def var_montecarlo(ativo)


################################## RISCO /FIM ##################################################