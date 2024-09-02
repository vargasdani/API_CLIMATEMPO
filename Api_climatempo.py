import requests
import json

# Token de acesso à API
iTOKEN = 'f0ab6c560f54ced16999b37ae243bed5'

def obter_id_cidade(nome_cidade):
    iURL = f"http://apiadvisor.climatempo.com.br/api/v1/locale/city?name={nome_cidade}&token={iTOKEN}"
    try:
        iRESPONSE = requests.get(iURL)
        iRESPONSE.raise_for_status()
        iRETORNO_REQ = iRESPONSE.json()

        if not iRETORNO_REQ:
            print("Cidade não encontrada.")
            return None
        
        cidades = []
        for cidade in iRETORNO_REQ:
            iID = cidade['id']
            iNAME = cidade['name']
            iSTATE = cidade['state']
            iCOUNTRY = cidade['country']
            cidades.append((iID, iNAME, iSTATE, iCOUNTRY))
        
        if len(cidades) == 0:
            print("Nenhuma cidade encontrada.")
            return None

        if len(cidades) > 1:
            print("Múltiplas cidades encontradas. Selecione a cidade correta:")
            for idx, (iID, iNAME, iSTATE, iCOUNTRY) in enumerate(cidades, 1):
                print(f"{idx}: id: {iID} - state: {iSTATE} - country: {iCOUNTRY} - name: {iNAME}")

            try:
                escolha = int(input("Digite o número da cidade desejada: "))
                if 1 <= escolha <= len(cidades):
                    return cidades[escolha - 1][0]
                else:
                    print("Escolha inválida.")
                    return None
            except ValueError:
                print("Entrada inválida.")
                return None
        else:
            return cidades[0][0]
    
    except requests.RequestException as e:
        print(f"Erro ao buscar dados da cidade: {e}")
        return None

def consultar_clima():
    iCIDADE = None

    while True:
        print("\nEscolha o tipo de consulta:")
        print("1: Tempo agora na cidade")
        print("2: Status do tempo no país")
        print("3: Previsão para os próximos 15 dias")
        print("4: Previsão para os próximos 3 dias por região")
        print("5: Previsão para as próximas 72 horas")
        print("6: Pesquisa ID da cidade")
        print("7: Pesquisar o ID da cidade vinculado ao seu Token")
        print("8: Pesquisar a cidade por ID")
        print("9: Alterar o ID da cidade relacionada ao Token")
        print("0: Sair")

        try:
            iTIPOCONSULTA = int(input("Digite o número da consulta desejada: "))
        except ValueError:
            print("Escolha inválida. Por favor, digite um número.")
            continue

        if iTIPOCONSULTA == 0:
            print("Saindo...")
            break

        if iTIPOCONSULTA in [1, 3, 5, 8, 9] and iCIDADE is None:
            nome_cidade = input('Informe o nome da cidade: ')
            iCIDADE = obter_id_cidade(nome_cidade)
            if iCIDADE is None:
                continue

        if iTIPOCONSULTA == 1:
            iURL = f"http://apiadvisor.climatempo.com.br/api/v1/weather/locale/{iCIDADE}/current?token={iTOKEN}"
            try:
                iRESPONSE = requests.get(iURL)
                iRESPONSE.raise_for_status()
                iRETORNO_REQ = iRESPONSE.json()

                if 'error' in iRETORNO_REQ:
                    print(f"Erro: {iRETORNO_REQ.get('detail')}")
                else:
                    print(iRETORNO_REQ)
                    for chave in iRETORNO_REQ:
                        print(f"{chave} : {iRETORNO_REQ[chave]}")
                    for chave in iRETORNO_REQ.get('data', {}):
                        print(f"{chave} : {iRETORNO_REQ['data'][chave]}")
            except requests.RequestException as e:
                print(f"Erro ao buscar o clima atual: {e}")

        elif iTIPOCONSULTA == 2:
            iURL = f"http://apiadvisor.climatempo.com.br/api/v1/anl/synoptic/locale/BR?token={iTOKEN}"
            try:
                iRESPONSE = requests.get(iURL)
                iRESPONSE.raise_for_status()
                iRETORNO_REQ = iRESPONSE.json()
                print(f"Country: {iRETORNO_REQ.get('country')}")
                print(f"Date: {iRETORNO_REQ.get('date')}")
                print(f"Text: {iRETORNO_REQ.get('text')}\n")
            except requests.RequestException as e:
                print(f"Erro ao buscar o status do tempo no país: {e}")

        elif iTIPOCONSULTA == 3:
            iURL = f"http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/{iCIDADE}/days/15?token={iTOKEN}"
            try:
                iRESPONSE = requests.get(iURL)
                iRESPONSE.raise_for_status()
                iRETORNO_REQ = iRESPONSE.json()

                if 'error' in iRETORNO_REQ:
                    print(f"Erro: {iRETORNO_REQ.get('detail')}")
                else:
                    print(f"\ncidade: {iRETORNO_REQ.get('name')} - {iRETORNO_REQ.get('state')}")
                    for chave in iRETORNO_REQ.get('data', []):
                        iDATA = chave.get('date_br')
                        iCHUVA = chave['rain'].get('probability', 0)
                        iTEXTMORNING = chave['text_icon']['text']['phrase'].get('reduced', 'Sem dados')
                        iTEMPERATURAMIN = chave['temperature'].get('min', 'Sem dados')
                        iTEMPERATURAMAX = chave['temperature'].get('max', 'Sem dados')
                        print(f"data: {iDATA} chuva: {iCHUVA}% temp: min({iTEMPERATURAMIN}) max({iTEMPERATURAMAX}) resumo: {iTEXTMORNING}\n")
            except requests.RequestException as e:
                print(f"Erro ao buscar a previsão para os próximos 15 dias: {e}")

        elif iTIPOCONSULTA == 4:
            iURL = f"http://apiadvisor.climatempo.com.br/api/v1/forecast/region/centro-oeste?token={iTOKEN}"
            try:
                iRESPONSE = requests.get(iURL)
                iRESPONSE.raise_for_status()
                iRETORNO_REQ = iRESPONSE.json()

                if 'error' in iRETORNO_REQ:
                    print(f"Erro: {iRETORNO_REQ.get('detail')}")
                else:
                    for chave in iRETORNO_REQ.get('data', []):
                        iDATA = chave.get('date_br')
                        iTEXT = chave.get('text', 'sem dados para esta data')
                        print(f"data: {iDATA} texto: {iTEXT}\n")
            except requests.RequestException as e:
                print(f"Erro ao buscar a previsão para os próximos 3 dias por região: {e}")

        elif iTIPOCONSULTA == 5:
            iURL = f"http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/{iCIDADE}/hours/72?token={iTOKEN}"
            try:
                iRESPONSE = requests.get(iURL)
                iRESPONSE.raise_for_status()
                iRETORNO_REQ = iRESPONSE.json()

                if 'error' in iRETORNO_REQ:
                    print(f"Erro: {iRETORNO_REQ.get('detail')}")
                else:
                    for chave in iRETORNO_REQ.get('data', []):
                        iDATA = chave.get('date_br')
                        iTEMPERATURA = chave['temperature'].get('temperature', 'Sem dados')
                        print(f"data: {iDATA} {iTEMPERATURA}º\n")
            except requests.RequestException as e:
                print(f"Erro ao buscar a previsão para as próximas 72 horas: {e}")

        elif iTIPOCONSULTA == 6:
            nome_cidade = input('Informe o nome da cidade: ')
            iID = obter_id_cidade(nome_cidade)
            if iID:
                print(f"ID da cidade '{nome_cidade}': {iID}")

        elif iTIPOCONSULTA == 7:
            iURL = f"http://apiadvisor.climatempo.com.br/api-manager/user-token/{iTOKEN}/locales"
            try:
                iRESPONSE = requests.get(iURL)
                iRESPONSE.raise_for_status()
                iRETORNO_REQ = iRESPONSE.json()
                print(f"ID da cidade vinculada ao Token: {iRETORNO_REQ.get('locales')}")
            except requests.RequestException as e:
                print(f"Erro ao buscar o ID da cidade vinculada ao Token: {e}")

        elif iTIPOCONSULTA == 8:
            if iCIDADE:
                iURL = f"http://apiadvisor.climatempo.com.br/api/v1/locale/city/{iCIDADE}?token={iTOKEN}"
                try:
                    iRESPONSE = requests.get(iURL)
                    iRESPONSE.raise_for_status()
                    iRETORNO_REQ = iRESPONSE.json()
                    print(f"id: {iRETORNO_REQ.get('id')}")
                    print(f"name: {iRETORNO_REQ.get('name')}")
                    print(f"state: {iRETORNO_REQ.get('state')}")
                    print(f"country: {iRETORNO_REQ.get('country')}\n")
                except requests.RequestException as e:
                    print(f"Erro ao buscar a cidade por ID: {e}")

        elif iTIPOCONSULTA == 9:
            if iCIDADE:
                iURL = f"http://apiadvisor.climatempo.com.br/api-manager/user-token/{iTOKEN}/locales"
                payload = f"localeId[]={iCIDADE}"
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                try:
                    iRESPONSE = requests.put(iURL, headers=headers, data=payload)
                    iRESPONSE.raise_for_status()
                    print("ID da cidade alterado com sucesso.")
                except requests.RequestException as e:
                    print(f"Erro ao alterar o ID da cidade relacionada ao Token: {e}")

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    consultar_clima()
