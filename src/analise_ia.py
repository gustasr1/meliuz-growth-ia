import os
from dotenv import load_dotenv
from google import genai

# Carrega o .env
load_dotenv()

CHAVE_API = os.getenv("GEMINI_API_KEY")

if not CHAVE_API:
    raise ValueError("Chave da API não encontrada! Verifique o arquivo .env.")

# Inicializa o cliente do novo SDK do Google
cliente = genai.Client(api_key=CHAVE_API)

def analisar_dados_com_ia(tabela_markdown, nome_parceiro):
    """
    Envia os dados consolidados para IA analisar
    """
    prompt_sistema = f"""Atue como um sistema automatizado de análise de dados do time de Growth do Méliuz.
Sua tarefa é gerar um relatório executivo, padronizado e estritamente impessoal sobre os resultados de um teste de variação de cashback para o Parceiro {nome_parceiro}.

REGRA DE NEGÓCIO DO MÉLIUZ:
- Receita Líquida = Comissão recebida - Cashback pago aos usuários.
- O objetivo principal é maximizar a Receita Líquida, mantendo um volume saudável de compradores.
- Não se deixe enganar apenas pelo volume de 'vendas totais' (GMV) se a margem de lucro for destruída pelo alto cashback.

DADOS DO TESTE A/B:
{tabela_markdown}

INSTRUÇÕES DE SAÍDA E TOM DE VOZ:
Escreva de forma puramente técnica e objetiva. NUNCA utilize a primeira pessoa (eu recomendo/nós vemos) e NUNCA cite a si mesmo como "analista" ou "IA".
Retorne o relatório contendo exatamente os 3 tópicos abaixo:
1. Variante Vencedora: (Apenas o nome do Grupo que deve ser escalado para 100% do tráfego).
2. Justificativa: (Um parágrafo técnico explicando o motivo da escolha, evidenciando os números de Receita Líquida e o Retorno Percentual).
3. Alerta de Risco: (Se a variante vencedora teve menos compradores que as outras, aponte isso de forma direta como um ponto de atenção para a retenção a longo prazo).
"""
    # Chamando o modelo Gemini 2.5 Flash
    resposta = cliente.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_sistema,
    )
    
    return resposta.text

# Bloco de teste
if __name__ == "__main__":
    tabela_teste = """
| Grupos de usuários   |   compradores |   comissão |   cashback |   vendas totais |   receita_liquida |   ret_percentual |
|:---------------------|--------------:|-----------:|-----------:|----------------:|------------------:|-----------------:|
| Grupo 1              |          9633 |     638135 |     233424 |         5605173 |            404711 |           173.38 |
| Grupo 2              |         10814 |     728178 |     370659 |         6423096 |            357519 |            96.45 |
| Grupo 3              |         11410 |     767887 |     503600 |         6785856 |            264287 |            52.48 |
    """
    
    print("Enviando dados para a IA...")
    analise = analisar_dados_com_ia(tabela_teste, "Parceiro A")
    print("\n--- RELATÓRIO DO TESTE A/B ---")
    print(analise)