import os
import time

from ngram_score import ngram_score
from utils import (
    binary_to_ascii,
    clean_text_for_ciphers,
    save_text_to_file,
    break_substitution
)

try:
    import wordninja
    _WORDNINJA_OK = True
except Exception as _e:
    _WORDNINJA_OK = False
    _WORDNINJA_ERR = _e

DATA_FOLDER = 'data'
BIN_FILE_PATH = os.path.join(DATA_FOLDER, 'encrypted_message.txt')
NGRAM_FILE_PATH = os.path.join(DATA_FOLDER, 'quadgrams.txt')
ASCII_OUTPUT_FILE = os.path.join(DATA_FOLDER, 'raw_ascii_output.txt')
SUBSTITUTION_OUTPUT_FILE = os.path.join(DATA_FOLDER, 'decrypted_substitution.txt')


def initialize_tools():
    """
    Função principal de inicialização: lê a mensagem, salva o texto bruto, 
    limpa o texto e configura a métrica de N-Gramas.
    """
    print("--- 1. Conversão e Inicialização ---")
    
    raw_ascii_text = binary_to_ascii(BIN_FILE_PATH)

    print("\n--- Texto ASCII (resultado da conversão binário → ASCII) ---")
    print(raw_ascii_text)

    if raw_ascii_text.startswith("Erro"):
        print(raw_ascii_text)
        return None, None
    
    # Salva o texto bruto (com espaços e pontuações)
    if save_text_to_file(raw_ascii_text, ASCII_OUTPUT_FILE):
        print(f"\nTexto ASCII bruto (com símbolos) salvo em: {ASCII_OUTPUT_FILE}")
    else:
        print("Falha ao salvar o arquivo ASCII bruto. Continuando...")
        return None, None
    
    # Limpa o texto, deixando apenas letras MAIÚSCULAS
    encrypted_text_clean = clean_text_for_ciphers(raw_ascii_text)
    print("\nMensagem LIMPA e Pronta")
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

    print("\n--- 2. Quebra da Cifra de Substituição (Heurística de N-Gramas) ---")
    
    best_key, decrypted_substitution_text, best_score_sub = break_substitution(encrypted_text, scorer)

    print(f"Chave Encontrada (Mapa de Substituição):\n{best_key}")
    print(f"Score de N-Gramas: {best_score_sub:.2f}")
    
    # Inserção de espaços com wordninja antes de salvar
    if _WORDNINJA_OK:
        spaced_substitution_text = ' '.join(wordninja.split(decrypted_substitution_text))
    else:
        spaced_substitution_text = decrypted_substitution_text
        print(
            "\n[AVISO] 'wordninja' não está instalado. "
            "O arquivo de substituição será salvo sem espaços.\n"
            "Para ativar a segmentação automática, instale:\n"
            "    pip install wordninja\n"
            f"Erro original do import: {_WORDNINJA_ERR}\n"
        )

    print("\n--- Mensagem Decriptografada FINAL ---")
    print(spaced_substitution_text)

    # Salva o texto descriptografado de Substituição
    if save_text_to_file(spaced_substitution_text, SUBSTITUTION_OUTPUT_FILE):
        print(f"Mensagem de Substituição SALVA em: {SUBSTITUTION_OUTPUT_FILE}")
    
    end_time = time.time()
    print(f"\n--- Processo Concluído em {end_time - start_time:.2f} segundos ---")


if __name__ == "__main__":
    main()
