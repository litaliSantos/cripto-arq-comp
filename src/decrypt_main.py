# Importa a função de conversão que criamos
from utils import binary_to_ascii 

# Importa a classe de pontuação fornecida
from ngram_score import ngram_score 

# --- Definição dos Caminhos de Arquivo ---
BIN_FILE_PATH = 'data/encrypted_message.txt'
NGRAM_FILE_PATH = 'data/quadgrams.txt'

def initialize_tools():
    """
    Inicializa a classe ngram_score e retorna a string ASCII convertida.
    """
    print("--- 1. Conversão e Inicialização ---")
    
    # TAREFA 1: Ler e Converter a Mensagem Binária
    encrypted_text_ascii = binary_to_ascii(BIN_FILE_PATH)
    
    if encrypted_text_ascii.startswith("Erro"):
        print(encrypted_text_ascii)
        return None, None # Retorna None em caso de erro

    print(f"Mensagem Binária convertida (Primeiros 50 chars):\n{encrypted_text_ascii[:50]}...")
    
    # Inicializa a Classe de Pontuação (Scorer)
    try:
        # Inicializa o scorer, passando o caminho para o arquivo de frequência
        scorer = ngram_score(NGRAM_FILE_PATH)
        print("Scorer de N-Gramas inicializado com sucesso!")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo de N-gramas não encontrado em: {NGRAM_FILE_PATH}")
        return encrypted_text_ascii, None
    
    return encrypted_text_ascii, scorer

if __name__ == "__main__":
    # Chama a função de inicialização
    encrypted_text, scorer = initialize_tools()
    
    if scorer:
        print("\n--- 2. Próximo Passo: Quebra da Cifra de César (Força Bruta) ---")
        # AQUI VOCÊ CHAMARÁ AS FUNÇÕES DE QUEBRA DE CRIPTOGRAFIA
        # Ex: best_caesar_shift = break_caesar(encrypted_text, scorer)
        # Ex: best_substitution_key = break_substitution(encrypted_text, scorer)
    else:
        print("\nO projeto não pode continuar sem o scorer de N-gramas.")