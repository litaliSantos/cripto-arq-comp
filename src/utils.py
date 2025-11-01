import re
import string

# O alfabeto é essencial para as cifras
ALPHABET = string.ascii_uppercase # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def read_binary_file(file_path):
    """Lê o conteúdo do arquivo e retorna a string bruta de binários e espaços."""
    try:
        with open(file_path, 'r') as f:
            # Lemos o conteúdo inteiro e removemos espaços em branco nas extremidades
            return f.read().strip()
    except FileNotFoundError:
        # Retorna uma string de erro para ser checada em decrypt_main.py
        return f"Erro: Arquivo não encontrado no caminho: {file_path}"

def convert_binary_to_text(binary_string_with_spaces):
    """
    Converte uma string de binários separados por espaço (7 bits) para texto ASCII.
    """
    # 1. Separa a string em blocos de 7 bits, usando o espaço como delimitador
    # O método split() é perfeito para isso.
    binary_blocks = binary_string_with_spaces.split() 

    # 2. Converte cada bloco binário para seu caractere ASCII
    text_chars = []
    for block in binary_blocks:
        try:
            # Converte a string binária (bloco, base 2) para um número inteiro
            char_code = int(block, 2)
            # Converte o número inteiro para o caractere ASCII correspondente
            text_char = chr(char_code)
            text_chars.append(text_char)
        except ValueError:
            # Caso algum bloco não seja um binário válido (deve ser raro)
            print(f"Aviso: Bloco binário inválido encontrado: {block}. Ignorando.")
            
    return "".join(text_chars)


def clean_text_for_ciphers(raw_text):
    """
    Remove caracteres não alfabéticos e converte tudo para MAIÚSCULAS.
    """
    # 1. Converte para maiúsculas
    text = raw_text.upper()
    
    # 2. Usa expressão regular para manter apenas caracteres de A a Z
    cleaned_text = re.sub(r'[^A-Z]', '', text) 
    
    return cleaned_text

# --- Sua função binary_to_ascii que o decrypt_main.py espera ---
def binary_to_ascii(bin_file_path):
    """
    Função wrapper que executa o processo completo: Ler -> Converter -> Limpar.
    """
    # 1. Ler o binário
    binary_data_raw = read_binary_file(bin_file_path)
    if binary_data_raw.startswith("Erro"):
        return binary_data_raw # Repassa o erro de arquivo

    # 2. Converter o binário para texto ASCII (texto bruto, com pontuação e espaços)
    raw_ascii_text = convert_binary_to_text(binary_data_raw)
    
    # 3. Limpar o texto, deixando apenas letras MAIÚSCULAS
    encrypted_text_clean = clean_text_for_ciphers(raw_ascii_text)
    
    # Retornamos o texto pronto para ser processado pelas cifras
    return encrypted_text_clean

# --- Deixe as funções break_caesar e break_substitution vazias por enquanto ---

def break_caesar(encrypted_text, scorer):
    """A ser implementada."""
    # Retornos fictícios para evitar erros de execução no decrypt_main.py
    return 0, "[TEXTO DESCRIPTOGRAFADO CÉSAR A SER EXIBIDO]", 0.0

def break_substitution(encrypted_text, scorer):
    """A ser implementada."""
    # Retornos fictícios para evitar erros de execução no decrypt_main.py
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "[TEXTO DESCRIPTOGRAFADO SUBSTITUIÇÃO A SER EXIBIDO]", 0.0