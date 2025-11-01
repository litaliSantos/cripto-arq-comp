import re
import string
import os

# O alfabeto é essencial para as cifras
ALPHABET = string.ascii_uppercase # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def read_binary_file(file_path):
    """Lê o conteúdo do arquivo e retorna a string bruta de binários e espaços."""
    try:
        # Verifica se a pasta existe antes de tentar abrir o arquivo
        if not os.path.exists(os.path.dirname(file_path)) and os.path.dirname(file_path):
             return f"Erro: Diretório não encontrado no caminho: {os.path.dirname(file_path)}"
             
        with open(file_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        # Retorna uma string de erro para ser checada em decrypt_main.py
        return f"Erro: Arquivo não encontrado no caminho: {file_path}"
    except Exception as e:
        return f"Erro inesperado ao ler o arquivo: {e}"


def convert_binary_to_text(binary_string_with_spaces):
    """
    Converte uma string de binários separados por espaço (7 bits) para texto ASCII.
    """
    binary_blocks = binary_string_with_spaces.split() 
    text_chars = []
    
    for block in binary_blocks:
        try:
            # Converte o bloco binário (base 2) para um número inteiro
            char_code = int(block, 2)
            # Converte o número inteiro para o caractere ASCII correspondente
            text_char = chr(char_code)
            text_chars.append(text_char)
        except ValueError:
            print(f"Aviso: Bloco binário inválido encontrado: {block}. Ignorando.")
            
    return "".join(text_chars)


def clean_text_for_ciphers(raw_text):
    """
    Remove caracteres não alfabéticos e converte tudo para MAIÚSCULAS.
    """
    # 1. Converte para maiúsculas
    text = raw_text.upper()
    
    # 2. Mantém apenas caracteres de A a Z
    cleaned_text = re.sub(r'[^A-Z]', '', text) 
    
    return cleaned_text

def save_text_to_file(text, file_path):
    """Salva uma string de texto em um arquivo."""
    try:
        # Garante que o diretório de saída existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo em {file_path}: {e}")
        return False


def binary_to_ascii(bin_file_path):
    """
    Função principal wrapper que o decrypt_main.py chama.
    """
    # 1. Ler o binário
    binary_data_raw = read_binary_file(bin_file_path)
    if binary_data_raw.startswith("Erro"):
        return binary_data_raw 

    # 2. Converter o binário para texto ASCII (texto bruto)
    raw_ascii_text = convert_binary_to_text(binary_data_raw)
    
    # Retornamos o texto bruto, pois o decrypt_main irá salvá-lo e depois limpá-lo
    return raw_ascii_text

# --- PLACEHOLDERS PARA FUNÇÕES FUTURAS (para evitar erros de importação) ---

def break_caesar(encrypted_text, scorer):
    """Placeholder: A ser implementada para quebrar Cifra de César."""
    # Retornos fictícios para que decrypt_main.py execute
    return "SHIFT AINDA NÃO CALCULADO", "NÃO IMPLEMENTADO AINDA", 0.0

def break_substitution(encrypted_text, scorer):
    """Placeholder: A ser implementada para quebrar Cifra de Substituição."""
    # Retornos fictícios para que decrypt_main.py execute
    return "CHAVE FICTÍCIA", "NÃO IMPLEMENTADO AINDA", 0.0