import os
import glob
import pandas as pd
import time 
from datetime import datetime
from dotenv import load_dotenv

from data_process import processar_teste_ab
from analise_ia import analisar_dados_com_ia
from integracao_sheets import registrar_no_google_sheets

def salvar_historico_testes(dados_historico, caminho_arquivo):
    df_novo = pd.DataFrame(dados_historico)
    if os.path.exists(caminho_arquivo):
        df_existente = pd.read_csv(caminho_arquivo)
        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
    else:
        df_final = df_novo
        
    df_final.to_csv(caminho_arquivo, index=False, encoding='utf-8')
    print(f"\nRegisto de acompanhamento atualizado em: {caminho_arquivo}")

def executar_pipeline():
    pasta_dados_brutos = "../data/raw/"
    pasta_relatorios = "../reports/"
    pasta_dados_processados = "../data/processed"
    caminho_historico = os.path.join(pasta_relatorios, "historico_testes.csv")
    
    os.makedirs(pasta_relatorios, exist_ok=True)
    os.makedirs(pasta_dados_processados, exist_ok=True)
    
    arquivos_csv = glob.glob(os.path.join(pasta_dados_brutos, "*.csv"))
    
    if not arquivos_csv:
        print(f"Nenhum arquivo CSV encontrado na pasta {pasta_dados_brutos}.")
        return

    registro_historicos = []

    for caminho_arquivo in arquivos_csv:
        nome_arquivo = os.path.basename(caminho_arquivo)
        nome_parceiro = nome_arquivo.replace(".csv", "")
        print(f"\n========================================")
        print(f"A processar os dados do: {nome_parceiro}")
        print(f"========================================")

        #Limpeza e Agregação
        df_resumo = processar_teste_ab(caminho_arquivo)
        
        caminho_processado = os.path.join(pasta_dados_processados, f"resumo_{nome_arquivo}")
        df_resumo.to_csv(caminho_processado, index=False, encoding='utf-8')
        
        tabela_markdown = df_resumo.to_markdown(index=False)
        
        #Tratamento de erro
        print("A solicitar parecer analítico à IA...")
        
        #Sistema de "tentativas" para lidar com a instabilidade da API que gera erro de instabilidade dependendo da demanda
        tentativas = 3
        sucesso_ia = False
        parecer_ia = "Erro na análise automatizada."
        
        for tentativa in range(tentativas):
            try:
                parecer_ia = analisar_dados_com_ia(tabela_markdown, nome_parceiro)
                print("Análise concluída com sucesso.")
                sucesso_ia = True
                break
                
            except Exception as e:
                print(f"Aviso: Servidor ocupado (Tentativa {tentativa + 1}/{tentativas}). A aguardar 10 segundos...")
                time.sleep(10) #Pausa o código por 10 seg para o servidor do Google conseguir executar o teste - (Erro 503)
                
        if not sucesso_ia:
            print(f"Falha ao analisar {nome_parceiro} após 3 tentativas. A avançar para o próximo...")
        
        #Guardar o Relatório Individual
        caminho_relatorio = os.path.join(pasta_relatorios, f"relatorio_{nome_parceiro}.md")
        with open(caminho_relatorio, 'w', encoding='utf-8') as f:
            f.write(f"RELATÓRIO DE TESTE A/B - {nome_parceiro}\n")
            f.write(f"Data da execução: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("DADOS CONSOLIDADOS:\n")
            f.write(tabela_markdown + "\n\n")
            f.write("PARECER DA IA:\n")
            f.write(parecer_ia)
            
        #Preparar os dados para o google planilha
        registro_historicos.append({
            "Data do Teste": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "Parceiro": nome_parceiro,
            "Decisão e Justificação da IA": parecer_ia.replace('\n', ' | ') 
        })
        
        #Pausa antes de ir para o próximo arquivo do loop
        time.sleep(5)

    salvar_historico_testes(registro_historicos, caminho_historico)
    
    print("\n Iniciando sincronização em tempo real com o Google Sheets...")
    registrar_no_google_sheets(registro_historicos)
    
    print("\n✅ PIPELINE EXECUTADO COM SUCESSO! Todos os testes foram processados.")

if __name__ == "__main__":
    executar_pipeline()