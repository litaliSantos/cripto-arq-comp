import re
import string
import os
import random
import time

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
            char_code = int(block, 2)
            text_char = chr(char_code)
            text_chars.append(text_char)
        except ValueError:
            print(f"Aviso: Bloco binário inválido encontrado: {block}. Ignorando.")
            
    return "".join(text_chars)


def clean_text_for_ciphers(raw_text):
    """
    Remove caracteres não alfabéticos e converte tudo para MAIÚSCULAS.
    """
    text = raw_text.upper()
    cleaned_text = re.sub(r'[^A-Z]', '', text) 
    
    return cleaned_text

def save_text_to_file(text, file_path):
    """Salva uma string de texto em um arquivo."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo em {file_path}: {e}")
        return False


def binary_to_ascii(bin_file_path):
    """
    Função principal wrapper que o decrypt_main.py chama para obter o texto BRUTO.
    """
    binary_data_raw = read_binary_file(bin_file_path)
    if binary_data_raw.startswith("Erro"):
        return binary_data_raw 

    raw_ascii_text = convert_binary_to_text(binary_data_raw)
    
    return raw_ascii_text

# --- FUNÇÕES DE QUEBRA DE SUBSTITUIÇÃO ---

def substitution_decrypt(ciphertext, key):
    """
    Descriptografa o texto usando um mapa de substituição (key).
    """
    translation_table = str.maketrans(key, ALPHABET)
    return ciphertext.translate(translation_table)

def generate_random_key():
    """Gera um mapa de substituição aleatório (permuta do ALPHABET)."""
    key_list = list(ALPHABET)
    random.shuffle(key_list)
    return "".join(key_list)

def break_substitution(encrypted_text, scorer, max_iterations=20000):
    """
    Quebra a Cifra de Substituição usando o algoritmo Hill Climbing.
    """
    
    # 1. Geração da Chave Inicial (Random Key)
    current_key = generate_random_key()
    
    # 2. Descriptografia e Avaliação da Chave Inicial
    decrypted_text = substitution_decrypt(encrypted_text, current_key)
    best_score = scorer.score(decrypted_text)
    
    print(f"Início da Criptoanálise por Substituição (Iterações: {max_iterations})...")
    
    # Estrutura para Hill Climbing
    for i in range(max_iterations):
        
        # 3. Mutação: Gerar uma Chave Candidata (trocando 2 letras)
        
        # Escolhe duas posições aleatórias (índices de 0 a 25)
        a = random.randint(0, 25)
        b = random.randint(0, 25)
        
        # Evita a troca da mesma letra por si mesma
        if a == b:
            continue
            
        candidate_key_list = list(current_key)
        
        # Troca as letras (mutação)
        candidate_key_list[a], candidate_key_list[b] = candidate_key_list[b], candidate_key_list[a]
        candidate_key = "".join(candidate_key_list)
        
        # 4. Avaliação da Chave Candidata
        candidate_decrypted = substitution_decrypt(encrypted_text, candidate_key)
        candidate_score = scorer.score(candidate_decrypted)
        
        # 5. Seleção: Aceitar se a nova chave for melhor (score mais alto)
        if candidate_score > best_score:
            best_score = candidate_score
            current_key = candidate_key
            
            # Imprime o progresso a cada 100 iterações (para não poluir o terminal)
            if i % 100 == 0:
                print(f"Iter: {i:05d} | Score: {best_score:.2f} | Decrypt: {candidate_decrypted[:40]}...")
        
        # Adiciona uma condição de parada antecipada se a melhora for muito pequena ou ausente
        # if i > 1000 and best_score_not_improved_for_many_iterations: break
    final_decrypted_text = substitution_decrypt(encrypted_text, current_key)
    
    return current_key, final_decrypted_text, best_score