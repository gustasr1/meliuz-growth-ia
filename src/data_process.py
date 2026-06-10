import pandas as pd
import os

# Mesmo código usado para EDA no jupyter notebook
def carregar_data_clean(filepath):
    df = pd.read_csv(filepath)
    
    cols_financeiras = ['comissão', 'cashback', 'vendas totais']
    
    for col in cols_financeiras:
        if col in df.columns:
            # Removendo o R$, os espaços em branco, tira os pontos de milhar e troca a vírgula decimal
            df[col] = (df[col]
                       .astype(str)
                       .str.replace('R$', '', regex=False)
                       .str.replace('.', '', regex=False)
                       .str.replace(',', '.', regex=False)
                       .str.strip())
            # Converte para float
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    if 'compradores' in df.columns:
        df['compradores'] = df['compradores'].fillna(0).astype(int)
        
    return df

def calcular_metricas(df):
    # Agrupa os dados por Grupo 1, 2, 3 e soma os resultados do período
    df_agrupamento = df.groupby('Grupos de usuários').agg({
        'compradores': 'sum',
        'comissão': 'sum',
        'cashback': 'sum',
        'vendas totais': 'sum'
    }).reset_index()
    
    df_agrupamento['receita_liquida'] = df_agrupamento['comissão'] - df_agrupamento['cashback']
    
    # Qual foi o retorno percentual sobre o cashback investido?
    df_agrupamento['ret_percentual'] = df_agrupamento.apply(
        lambda row: (row['receita_liquida'] / row['cashback'] * 100) if row['cashback'] > 0 else 0, 
        axis=1
    )
    
    # Arredondamento
    df_agrupamento = df_agrupamento.round(2)
    
    return df_agrupamento

def processar_teste_ab(filepath):
    df_clean = carregar_data_clean(filepath)
    df_sumario = calcular_metricas(df_clean)
    return df_sumario