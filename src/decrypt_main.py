import os
import time

# --- Módulos de Criptografia ---
from ngram_score import ngram_score
from utils import (
    binary_to_ascii,
    clean_text_for_ciphers,
    save_text_to_file,
    break_caesar,
    break_substitution
)

# Tenta importar wordninja para segmentação de palavras
try:
    import wordninja
    _WORDNINJA_OK = True
except Exception as _e:
    _WORDNINJA_OK = False
    _WORDNINJA_ERR = _e

# --- Definição dos Caminhos de Arquivo ---
DATA_FOLDER = 'data'
BIN_FILE_PATH = os.path.join(DATA_FOLDER, 'encrypted_message.txt')
NGRAM_FILE_PATH = os.path.join(DATA_FOLDER, 'quadgrams.txt')
ASCII_OUTPUT_FILE = os.path.join(DATA_FOLDER, 'raw_ascii_output.txt')
CAESAR_OUTPUT_FILE = os.path.join(DATA_FOLDER, 'decrypted_caesar.txt')       # NOVO: Saída César
SUBSTITUTION_OUTPUT_FILE = os.path.join(DATA_FOLDER, 'decrypted_substitution.txt') # NOVO: Saída Substituição


def initialize_tools():
    """
    Função principal de inicialização: lê a mensagem, salva o texto bruto, 
    limpa o texto e configura a métrica de N-Gramas.
    """
    print("--- 1. Conversão e Inicialização ---")
    
    raw_ascii_text = binary_to_ascii(BIN_FILE_PATH)
    
    if raw_ascii_text.startswith("Erro"):
        print(raw_ascii_text)
        return None, None
    
    # Salva o texto bruto (com espaços e pontuações)
    if save_text_to_file(raw_ascii_text, ASCII_OUTPUT_FILE):
        print(f"Texto ASCII bruto (com símbolos) salvo em: {ASCII_OUTPUT_FILE}")
    else:
        print("Falha ao salvar o arquivo ASCII bruto. Continuando...")

    print(f"Mensagem Binária convertida (Primeiros 50 chars):\n{raw_ascii_text[:50]}...")
    
    # Limpa o texto, deixando apenas letras MAIÚSCULAS
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

    # --- 2. QUEBRA DA CIFRA DE CÉSAR (FORÇA BRUTA) ---
    print("\n--- 2. Quebra da Cifra de César (Força Bruta) ---")
    
    best_shift, decrypted_caesar_text, best_score = break_caesar(encrypted_text, scorer)

    print(f"Chave Encontrada (Shift): {best_shift}")
    print(f"Score de N-Gramas: {best_score:.2f}")

    # Salva o texto descriptografado de César
    if save_text_to_file(decrypted_caesar_text, CAESAR_OUTPUT_FILE):
        print(f"Mensagem de César SALVA em: {CAESAR_OUTPUT_FILE}")

    # --- 3. QUEBRA DA CIFRA DE SUBSTITUIÇÃO (Heurística de N-Gramas) ---
    print("\n--- 3. Quebra da Cifra de Substituição (Heurística de N-Gramas) ---")
    
    best_key, decrypted_substitution_text, best_score_sub = break_substitution(encrypted_text, scorer)

    print(f"Chave Encontrada (Mapa de Substituição):\n{best_key}")
    print(f"Score de N-Gramas: {best_score_sub:.2f}")
    
    # >>> Inserção de espaços com wordninja ANTES de salvar <<<
    if _WORDNINJA_OK:
        spaced_substitution_text = " ".join(wordninja.split(decrypted_substitution_text))
    else:
        spaced_substitution_text = decrypted_substitution_text
        print(
            "\n[AVISO] 'wordninja' não está instalado. "
            "O arquivo de substituição será salvo sem espaços.\n"
            "Para ativar a segmentação automática, instale:\n"
            "    pip install wordninja\n"
            f"Erro original do import: {_WORDNINJA_ERR}\n"
        )

    # Salva o texto descriptografado de Substituição (com espaços se possível)
    if save_text_to_file(spaced_substitution_text, SUBSTITUTION_OUTPUT_FILE):
        print(f"Mensagem de Substituição SALVA em: {SUBSTITUTION_OUTPUT_FILE}")
    
    end_time = time.time()
    print(f"\n--- Processo Concluído em {end_time - start_time:.2f} segundos ---")


if __name__ == "__main__":
    main()
