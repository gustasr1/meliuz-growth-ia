# Méliuz Growth | Automação de Testes A/B (AI-Native)

Este repositório contém a resolução do desafio técnico para a vaga de Estágio em Growth (AI-Native) no Méliuz. A solução consiste num pipeline de dados automatizado que avalia resultados de testes A/B de parceiros de cashback, substituindo a análise manual por um fluxo validado por IA e integrado diretamente na nuvem (sheets).

## Entendimento do Negócio

A métrica de sucesso de um teste A/B de cashback não pode ser baseada estritamente em métricas de vaidade, como o volume bruto de vendas (GMV) ou o aumento absoluto de compradores, se estes destruírem a margem da operação. 

O motor analítico deste projeto foi parametrizado para avaliar os parceiros com base em duas métricas de eficiência:
1. **Receita Líquida:** `Comissão recebida - Cashback pago`
2. **Retorno Percentual (ROI):** `(Receita Líquida / Cashback pago) * 100`

## Arquitetura da Solução

O projeto é feito em três camadas modulares para garantir manutenção simples, tratamento seguro de dados e resiliência na comunicação com APIs externas:

* **Processamento de Dados:** Utiliza `Pandas` para higienização de dados financeiros sujos (ex: formatação de strings de moeda BRL para floats numéricos), tratamento nulos e consolidação matemática. Impede alucinações matemáticas da IA.
* **Camada Cognitiva (Análise de Growth):** Integração com o SDK `google-genai` (modelo `gemini-2.5-flash`). Consome os dados tabulares em Markdown e gera pareceres executivos padronizados. Inclui um mecanismo de *Retry* automatizado para lidar com eventuais instabilidades da API (Erro 503).
* **Camada de Integração e Persistência:** Regista o acompanhamento histórico (Data, Parceiro, Parecer) localmente em CSV e efetua o envio em tempo real para um *Dashboard* no Google Sheets via API (`gspread` e autenticação *Service Account*).

## Visualização dos Resultados (Google Sheets)

Como diferencial técnico da solução, o pipeline foi estruturado para alimentar uma planilha na nuvem em tempo real, permitindo que a liderança de Growth acompanhe o histórico de decisões e os pareceres de forma centralizada.

O resultado final consolidado pela automação pode ser visualizado no link abaixo:
* [Acessar a Planilha de Resultados do Teste A/B](https://docs.google.com/spreadsheets/d/17r8OD9Tni_jd5y_l_oGn-hqHop-tdiagQLXOHYASfrQ/edit?usp=sharing)

## Estrutura do Repositório

```text
/
├── data/
│   ├── raw/             # Datasets originais do teste (Parceiros A, B e C)
│   └── processed/       # Backups dos dados limpos e consolidados pelo Pandas
├── notebooks/           # Rascunho de EDA inicial e validação de limpeza
├── reports/             # Relatórios executivos (.md) e histórico consolidado (.csv)
├── src/
│   ├── main.py               # Orquestrador do pipeline
│   ├── data_process.py       # Motor de higienização e cálculo
│   ├── analise_ia.py         # Engenharia de prompt e conexão com o Gemini
│   └── integracao_sheets.py  # Autenticação e escrita no Google Sheets
├── .env.example         # Variáveis de ambiente (Template)
├── requirements.txt     # Dependências do projeto
└── README.md
