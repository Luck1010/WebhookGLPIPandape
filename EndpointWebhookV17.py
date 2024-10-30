import requests
import json
from urllib.parse import quote 

# Essa versão tem os dados formatados

# 1. Autenticação no Pandapé e obtenção dos dados do pré-colaborador

# URL do endpoint de token do Pandapé
auth_url = "https://loginqa3.pandape.com.br/connect/token"

# URL base da API para pré-colaboradores
base_url = "https://apiqa3.pandape.com.br/v3/precollaborators/"

base_vagas = "https://apiqa3.pandape.com.br/v2/vacancies/"

# Dados de autenticação para o Pandapé
auth_data = {
    "client_id": "", # Acresente aqui seu id da api pandapé
    "client_secret": "", # Acresente aqui a senha de acesso a API
    "grant_type": "client_credentials",
    "scope": "PandapeApi"
}

# Cabeçalhos da requisição de autenticação do Pandapé
auth_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Fazendo a requisição POST para autenticação no Pandapé
auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)

# Verificando a resposta da autenticação no Pandapé
if auth_response.status_code == 200:
    # Obtendo o token de acesso do Pandapé
    access_token = auth_response.json().get("access_token")

    # Cabeçalhos para buscar os dados do pré-colaborador
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Fazendo a requisição GET para buscar o pré-colaborador
    response = requests.get(base_url + "129117", headers=headers)  # Substitua 98231 pelo ID do pré-colaborador correto

    # Verificando a resposta da requisição GET
    if response.status_code == 200:
        # Processando os dados do pré-colaborador
        data = response.json()
        print("Dados do pré-colaborador:", data)

        # Extraindo informações do JSON
        name = data.get("name", "Nome não encontrado")
        surname = data.get("surname", "Sobrenome não encontrado")
        email = data.get("email", "Email não encontrado")
        admission_date = data.get("admissionDate", "Data de admissão não encontrada")
        vacancy_job = data.get("vacancyJob", "Vaga não encontrada")
        vacancy_reference = data.get("vacancyReference", "Referência da vaga não encontrada")
        forms = data.get("forms", [])
        current_folder_name = data.get("currentFolderName", "")

        link = data.get("link","")
        planilha_url = link[0]['link', ""] if link else 'URL da planilha não encontrada'
        

    # Só vai abrir chamado se caso o mesmo estiver em admissão finalizada
    if current_folder_name == "Admissão finalizada":
        # Construindo o conteúdo do chamado
        ticket_content = (
            f"Vaga: {vacancy_job}\n"
            
            
        )

        ticket_content_planejamento = ""
        ticket_content_ti = ""

         
        # Exibir os Dados Planejamento 
        for form in forms:
         if form['name'] =="Dados Planejamento ":
            ticket_content_planejamento += f"{form['name']}\n"
            for answer in form['answers']:
                ticket_content_planejamento += f"{answer['fieldName']}: {answer['answer']}\n"
            ticket_content_planejamento += "\n"    
                

         # Exibir os dados TI
        for form in forms:
            if form['name'] == "Dados TI":
                ticket_content_ti += f"{form['name']}\n"
                for answer in form['answers']:
                    ticket_content_ti += f"{answer['fieldName']}: {answer['answer']}\n"
                ticket_content_ti += "\n"     

        # Trecho que coloca a planilha no chamado do glpi (Dados Planejamento)
        for form in forms:
            documents = form.get('documents',[])
            for document in documents:
              link = document['link'].strip()  
              ticket_content_planejamento += f"{document['name']}: {document['link']}\n"
            ticket_content_planejamento += "\n"

        # Trecho que coloca a planilha no chamado do glpi (Dados TI)
        for form in forms:
            documents = form.get('documents', [])
            for document in documents:
                link = document['link'].strip()
                ticket_content_ti += f"{document['name']}: {document['link']}\n"
            ticket_content_ti += "\n"        

    

        # Dicionário de mapeamento dos números para as palavras correspondentes
        substitutions = {
           
            # Dados Planejamento

            # Dados Planejamento - Escala

            "10347" : " 220 HS 5X2",
            "21202" : " 180 HS - 6X1",
            "514643" : " 220 HS - 6X1",


            # Dados Planejamento - Carga horária

            "5380924" : " 40 Horas semanais",
            "5380923" : " 44 Horas semanais",
            "5380927" : " 36 Horas semanais",
            "5380925" : " 30 Horas semanais",
            "5380926" : " 20 Horas semanais",
            "5832046" : " 12 Horas semanais",
            "5832047" : " Escalas de plantão",

            # Dados Planejamento - Centro de Custo / Informe operação/departamento - Dados TI
             
            "5380928" : " Beyond",
            "5380929" : " Bom Pra Crédito",
            "5380930" : " Bossa Nova",
            "5380931" : " BuenoNetto",
            "5380932" : " Comunicação",
            "5380933" : " Cruzeiro Do Sul Fidelização/Retenção",
            "5380934" : " Cruzeiro do Sul Vendas",
            "5380935" : " Digital",
            "5380936" : " Diretoria",
            "5380937" : " DoTerra",
            "5380938" : " DP",
            "5380939" : " Even",
            "5380940" : " Fibra Experts",
            "5380941" : " Financeiro",
            "5380942" : " Green Drain",
            "5380943" : " Grupo Nortis",
            "5380944" : " Livelo",
            "5380945" : " Manutenção",
            "5380946" : " Movida",
            "5380947" : " Pede Pronto",
            "5380948" : " PetLove Cobrança",
            "5380949" : " PetLove Vendas",
            "5380950" : " Planejamento",
            "5380951" : " PraValer",
            "5380952" : " Processos",
            "5380953" : " Projetos",
            "5380954" : " Qista",
            "5380955" : " Qualidade",
            "5380956" : " Recepção",
            "5380957" : " RH",
            "5380958" : " TI",
            "5380959" : " Tishman Speyer",
            "5380960" : " Treinamento",

            # Dados Planejamento - Status

            "5380922" : " Ativo",
            "5380919" : " Demitido",
            "5380920" : " Demissionário",
            "5380921" : " Processo de abandono",

          
            # Dados TI

            # Selecione os acessos necessários  - Dados TI
            
            "380961" : " Buran",
            "380962" : " Catracas",
            "380963" : " Chat YH",
            "380964" : " Chave de E-mail",
            "380965" : " CRM",
            "380966" : " E-mail",
            "380967" : " GLPI",
            "380968" : " LH",
            "380969" : " Login de rede",
            "380970" : " Neoassit",
            "380971" : " Pacote Office",
            "380972" : " Pasta de Rede",
            "380973" : " Teams",
            "380974" : " Power BI",
            "380975" : " SDCOMMSL",
            "380976" : " Weduka",

            # Informe a carteira - Dados TI
            
             "5832027" : " Cruzeiro do Sul Vendas",
             "5832028" : " Cruzeiro do Sul Fidelização/Retenção",
             "5832029" : " Beyond",
             "5832030" : " Benx",
             "5832031" : " Bom pra Crédito",
             "5832032" : " Bossa Nova",
             "5832033" : " Fibra Experts",
             "5832034" : " Green Drain",
             "5832035" : " Grupo Nortis",
             "5832037" : " Movida",
             "5832038" : " PetLove Cobrança",
             "5832039":  " PetLove Vendas",
             "5832040" : " PraValerTopo",
             "5832041" : " PV",
             "5832042" : " Qista",
             "5832043" : " Solfacil",
             "5832044" : " Tishman Speyer",


            # Colaborador vai utilizar - Dados TI
             
             "5380979" : " Desktop",
             "5380980" : " Notebook",

           # É reposição - Dados TI 
              "5380977" : " Sim",
              "5380978" : " Não",

           # Home office - Dados TI
              "5380981" : " Sim",
              "5380982" : " Não",

           # Já existe equipamento no local
               "5380983" : " Sim",
               "5380984" : " Não",

            # Incluir headset
               "5380985" : " Sim",
               "5380986" : " Não",

            # Incluir mouse
               "5380989" : " Sim",
               "5380990" : " Não",  
            
            # Incluir monitor
               "5380987" : " Sim",
               "5380988" : " Não",

            # Incluir teclado 
              "5380991" : " Sim",
              "5380992" : " Não",
        }

        

        # Função para substituir os números pelas palavras no conteúdo do chamado
        def substituir_numeros_por_palavras(texto, substitutions,):

            # Substituindo pelo dicionário substitutions
            for numero, palavra in substitutions.items():
                texto = texto.replace(numero, palavra)
                
            return texto

        # Processando o conteúdo do chamado com as substituições
        ticket_content_substituido_planejamento = substituir_numeros_por_palavras(ticket_content_planejamento, substitutions,)
        ticket_content_substituido_ti = substituir_numeros_por_palavras(ticket_content_ti, substitutions,) 

        # 2. Autenticação no GLPI
        glpi_auth_url = "https://servicedesk.yhbrasil.com/apirest.php/initSession"  # Substitua pela URL correta do GLPI

        glpi_auth_data = {
            "app_token": "",  # Substitua pelo seu app_token do GLPI
            "user_token": ""  # Substitua pelo seu user_token do GLPI
        }

        glpi_response = requests.post(glpi_auth_url, json=glpi_auth_data)

        if glpi_response.status_code == 200:
            glpi_session_token = glpi_response.json().get("session_token")

            # Cabeçalhos para a criação do chamado no GLPI
            glpi_headers = {
                "Session-Token": glpi_session_token,
                "App-Token": "",  # Substitua pelo seu app_token do GLPI
                "Content-Type": "application/json"
            }

            glpi_ticket_url = "https://servicedesk.yhbrasil.com/apirest.php/Ticket"  # Substitua pela URL correta do GLPI

            # 3. Criação dos três chamados

            # Chamado para Planejamento
            glpi_ticket_data_planejamento = {
                "input": {
                    "name": f"Chamado Pandapé - Planejamento - Novos Colaboradores {vacancy_job}",
                    "content": ticket_content_substituido_planejamento,
                    "status": 2,
                    "groups_id": 89,  # Substitua pelo ID do grupo Planejamento
                    "requesttypes_id": 11
                }
            }

            # Chamado para TI > Gestão de Acesso
            glpi_ticket_data_gestao_acesso = {
                "input": {
                    "name": f"Chamado Pandapé - Gestão de Acessos - Novos Colaboradores {vacancy_job}",
                    "content": ticket_content_substituido_ti,
                    "status": 2,
                    "groups_id": 6,  # Substitua pelo ID do grupo Gestão de Acesso
                    "requesttypes_id": 11,
                    
                }
            }

            # Chamado para TI > Controle de Ativos
            glpi_ticket_data_controle_ativos = {
                "input": {
                    "name": f"Chamado Pandapé - Controle de Ativos - Novos colaboradores {vacancy_job}",
                    "content": ticket_content_substituido_ti,
                    "status": 2,
                    "groups_id": 4,  # Substitua pelo ID do grupo Controle de Ativos
                    "requesttypes_id": 11
                }
            }

            # Criando os três chamados
            for ticket_data, grupo in [
                (glpi_ticket_data_planejamento, "Planejamento"),
                (glpi_ticket_data_gestao_acesso, "Gestão de Acesso"),
                (glpi_ticket_data_controle_ativos, "Controle de Ativos"),
            ]:
                response = requests.post(glpi_ticket_url, headers=glpi_headers, json=ticket_data)
                if response.status_code == 201:
                    print(f"Chamado para {grupo} criado com sucesso!")
                else:
                    print(f"Erro ao criar o chamado para {grupo}: {response.status_code} - {response.text}")
        else:
            print(f"Erro ao autenticar no GLPI: {glpi_response.status_code} - {glpi_response.text}")
    else:
        print(f"Erro ao buscar dados do pré-colaborador: {response.status_code} - {response.text}")
else:
    print(f"Erro na autenticação do Pandapé: {auth_response.status_code} - {auth_response.text}")
