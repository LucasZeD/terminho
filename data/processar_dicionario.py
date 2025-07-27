# processar_json.py
import httpx
import json
from unidecode import unidecode
import re

# URL direta para o arquivo JSON bruto
JSON_URL = "https://gist.githubusercontent.com/un-versed/6373912fbf4649704b6823ea696cfcb1/raw/629137a0d0c7160b94c35013df8d570b31100174/termooo-wordsv2.json"

# Arquivo de saída para o seu jogo
OUTPUT_FILE = "words.txt"

def processar_lista_json():
    """
    Baixa a lista de palavras em JSON, normaliza (remove acentos),
    valida e salva em um arquivo de texto.
    """
    print(f"Baixando a lista de palavras de: {JSON_URL}")
    
    try:
        # Faz o download do conteúdo
        response = httpx.get(JSON_URL, timeout=30.0)
        response.raise_for_status() # Lança um erro se o download falhar
        
        # Carrega o conteúdo JSON em uma lista Python
        palavras_com_acento = response.json()
        print(f"Download concluído. {len(palavras_com_acento)} palavras encontradas.")
        
    except Exception as e:
        print(f"Ocorreu um erro durante o download ou processamento do JSON: {e}")
        return

    palavras_finais = set()
    # Expressão regular para garantir que a palavra tem apenas letras A-Z após a normalização
    regex_valida = re.compile(r'^[A-Z]{5}$')

    # Itera sobre cada palavra, normaliza e adiciona a um set (para evitar duplicatas)
    for palavra in palavras_com_acento:
        palavra_normalizada = unidecode(palavra.strip().upper())
        
        if regex_valida.match(palavra_normalizada):
            palavras_finais.add(palavra_normalizada)

    # Salva a lista final, ordenada, no arquivo de saída
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for palavra in sorted(list(palavras_finais)):
            f.write(f"{palavra}\n")
            
    print(f"\nProcesso finalizado com sucesso!")
    print(f"{len(palavras_finais)} palavras de 5 letras, sem acentos, foram salvas em '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    processar_lista_json()