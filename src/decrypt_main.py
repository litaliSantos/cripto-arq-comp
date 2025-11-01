import os
import time

# --- Módulos de Criptografia ---
# Importações ajustadas (absolutas)
from ngram_score import ngram_score 
from utils import (
    binary_to_ascii,
    clean_text_for_ciphers,
    save_text_to_file,
    break_caesar,      
    break_substitution 
)

# --- Definição dos Caminhos de Arquivo ---
# O caminho é relativo ao diretório raiz do repositório
DATA_FOLDER = 'data'
BIN_FILE_PATH = os.path.join(DATA_FOLDER, 'encrypted_message.txt')
NGRAM_FILE_PATH = os.path.join(DATA_FOLDER, 'quadgrams.txt')
ASCII_OUTPUT_FILE = os.path.join(DATA_FOLDER, 'raw_ascii_output.txt') # Arquivo de saída


def initialize_tools():
    """
    Função principal de inicialização: lê a mensagem, salva o texto bruto, 
    limpa o texto e configura a métrica de N-Gramas.
    """
    print("--- 1. Conversão e Inicialização ---")
    
    # TAREFA 1: Ler e Converter a Mensagem Binária (para texto ASCII bruto)
    raw_ascii_text = binary_to_ascii(BIN_FILE_PATH)
    
    if raw_ascii_text.startswith("Erro"):
        print(raw_ascii_text)
        return None, None
    
    # ----------------------------------------------------
    # NOVO: Salva o texto bruto (com espaços e pontuações) em um arquivo
    if save_text_to_file(raw_ascii_text, ASCII_OUTPUT_FILE):
        print(f"Texto ASCII bruto (com símbolos) salvo em: {ASCII_OUTPUT_FILE}")
    else:
         print("Falha ao salvar o arquivo ASCII bruto. Continuando...")

    print(f"Mensagem Binária convertida (Primeiros 50 chars):\n{raw_ascii_text[:50]}...")
    
    # 1.3. Limpar o texto, deixando apenas letras MAIÚSCULAS para a criptoanálise
    encrypted_text_clean = clean_text_for_ciphers(raw_ascii_text)
    print(f"Mensagem LIMPA e Pronta (Primeiros 50 chars):\n{encrypted_text_clean[:50]}...")
    print(f"Comprimento da mensagem para a cifra: {len(encrypted_text_clean)} caracteres.")
    
    # 2. Inicializa a Classe de Pontuação (Scorer)
    try:
        scorer = ngram_score(NGRAM_FILE_PATH)
        print("Scorer de N-Gramas inicializado com sucesso!")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo de N-gramas não encontrado em: {NGRAM_FILE_PATH}")
        return encrypted_text_clean, None
    
    return encrypted_text_clean, scorer


def main():
    start_time = time.time()
    
    encrypted_text, scorer = initialize_tools()
    
    if not scorer:
        print("\nO projeto não pode continuar sem o scorer de N-gramas.")
        return

    # --- 2. QUEBRA DA CIFRA DE CÉSAR (PLACEHOLDER) ---
    print("\n--- 2. Quebra da Cifra de César (Força Bruta) ---")
    
    # Chamada da função placeholder:
    best_shift, decrypted_caesar_text, best_score = break_caesar(encrypted_text, scorer)

    print(f"Mensagem Descriptografada (César):\n{decrypted_caesar_text}")
    
    
    # --- 3. QUEBRA DA CIFRA DE SUBSTITUIÇÃO (PLACEHOLDER) ---
    print("\n--- 3. Quebra da Cifra de Substituição (Heurística de N-Gramas) ---")
    
    # Chamada da função placeholder:
    best_key, decrypted_substitution_text, best_score_sub = break_substitution(encrypted_text, scorer)

    print(f"Mensagem Descriptografada (Substituição):\n{decrypted_substitution_text}")
    
    
    end_time = time.time()
    print(f"\n--- Processo Concluído em {end_time - start_time:.2f} segundos ---")


if __name__ == "__main__":
    main()