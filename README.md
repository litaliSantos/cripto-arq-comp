# 🧩 Projeto de Criptoanálise – Cifra de Substituição e Binário ASCII

Este projeto implementa um **decodificador automático de mensagens criptografadas** usando **binário ASCII + Cifra de Substituição**, com pontuação por **N-Gramas** e reconstrução automática de espaços via `wordninja`.  
Ele foi desenvolvido em Python e aplica técnicas heurísticas de **hill climbing** para análise de frequência de letras.

---

## 🚀 Visão Geral

O sistema realiza as seguintes etapas:

1. **Conversão de binário (7 bits ASCII)** em texto legível  
2. **Limpeza e normalização** (remoção de caracteres não alfabéticos)  
3. **Descriptografia da Cifra de Substituição**, maximizando o score de N-Gramas  
4. **Reconstrução de espaços** entre palavras com `wordninja`  
5. **Geração de arquivos de saída** em `/data`

O resultado é uma mensagem criptografada convertida em **texto natural legível**.

---

## 🧰 Dependências

O projeto usa apenas bibliotecas padrão do Python, mais o pacote externo:
```
wordninja
```

---

## ⚙️ Instalação

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/seu-usuario/cripto-arq-comp.git
cd cripto-arq-comp
```

### 2️⃣ Crie e ative um ambiente virtual (recomendado)

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Instale as dependências
```bash
pip install --upgrade pip
pip install wordninja
```

---

## ▶️ Passo a Passo para Execução

1️⃣ Confirme que a mensagem binária está no arquivo:
```bash
data/encrypted_message.txt
```

2️⃣ Rode o script principal:
```bash
python src/decrypt_main.py
```

3️⃣ Observe o progresso no terminal:
- Mostrará logs do processo de descriptografia (`Iter: 00000 | Score: ...`)
- Exibirá a chave encontrada e o score de N-Gramas final.

4️⃣ Verifique os arquivos de saída:
```
data/raw_ascii_output.txt          → Texto convertido de binário  
data/decrypted_substitution.txt    → Texto final legível com espaços automáticos
```

---

## ⚙️ Como Funciona

🔹 **1. Conversão Binária**  
Cada bloco de 7 bits é interpretado como um caractere ASCII:  
```python
binary_to_ascii("data/encrypted_message.txt")
```

🔹 **2. Limpeza do Texto**  
Remove tudo que não for A–Z:  
```python
clean_text_for_ciphers(text)
```

🔹 **3. Descriptografia da Substituição**  
O algoritmo hill climbing tenta milhares de permutações de chave e escolhe a que maximiza o score:  
```python
break_substitution(encrypted_text, scorer)
```

🔹 **4. Pontuação por N-Gramas**  
Usa o arquivo `quadgrams.txt` como modelo linguístico (frequência de 4 letras consecutivas em inglês).

🔹 **5. Inserção de Espaços**  
Após descriptografar, usa o `wordninja` para dividir o texto em palavras reconhecidas:  
```python
" ".join(wordninja.split(decrypted_substitution_text))
```

---

## 🧪 Exemplo de Resultado

**Saída final:**
```text
THE DAY WE CEASE THE EXPLORATION OF THE COSMOS IS THE DAY WE THREATEN THE CONTINUING OF OUR SPECIES IN THAT BLEAK WORLD ARMS BEARING RESOURCE HUNGRY PEOPLE AND NATIONS WOULD BE PRONE TO ACT ON THEIR LOW CONTRACTED PREJUDICES AND WOULD HAVE SEEN THE LAST GASP OF HUMAN ENLIGHTENMENT UNTIL THE RISE OF A VISIONARY NEW CULTURE THAT ONCE AGAIN EMBRACES THE COSMIC PERSPECTIVE A PERSPECTIVE IN WHICH WE ARE ONE FITTING NEITHER ABOVE NOR BELOW BUT WITHIN
```
