import os
import gspread
from google.oauth2.service_account import Credentials

def registrar_no_google_sheets(dados_teste):
    # Necessários para acessar o Sheets e Drive
    escopos = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    link_planilha = os.getenv("GOOGLE_SHEETS_URL")
    if not link_planilha:
        print("[-] LINK DO GOOGLE SHEETS NÃO CONFIGURADO NO .ENV!")
        return False

    # Aponta para o arquivo credenciais.json
    caminho_credenciais = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "credenciais.json")
    )

    if not os.path.exists(caminho_credenciais):
        print(f"[-] Arquivo de credenciais não encontrado em: {caminho_credenciais}")
        return False

    try:
        # Faz a autenticação segura
        credenciais = Credentials.from_service_account_file(caminho_credenciais, scopes=escopos)
        cliente_sheets = gspread.authorize(credenciais)

        # Abre a planilha utilizando a URL
        planilha = cliente_sheets.open_by_url(link_planilha)
        aba_principal = planilha.get_worksheet(0)

        #Verifica se a aba está vazia para criar o cabeçalho de Growth
        valores_existentes = aba_principal.get_all_values()
        if not valores_existentes:
            cabecalho = ["Data do Run", "Parceiro", "Decisão e Justificativa da IA"]
            aba_principal.append_row(cabecalho)

        # Insere os novos dados linha por linha
        for linha in dados_teste:
            nova_linha = [
                linha.get("Data do Teste"),
                linha.get("Parceiro"),
                linha.get("Decisão e Justificação da IA"),
            ]
            aba_principal.append_row(nova_linha)

        print("🌐 [Google Sheets] Dados sincronizados na nuvem com sucesso!")
        return True

    except Exception as e:
        print(f"[-] Erro na conexão com o Google Sheets: {e}")
        print("\nVerifique se você cumpriu o Passo OBRIGATÓRIO de compartilhamento da planilha!")
        return False