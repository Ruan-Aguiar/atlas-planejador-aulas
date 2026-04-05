# 📚 ATLAS – Planejador de Aulas com IA

Aplicação web que gera planejamentos de aula completos e alinhados à BNCC usando Inteligência Artificial.

## Como rodar localmente

**1. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**2. Configure sua chave da API:**
- Renomeie o arquivo `.env.exemplo` para `.env`
- Substitua `sua_chave_aqui` pela sua chave do Google Gemini
- Você pode obter sua chave gratuitamente em: https://aistudio.google.com

**3. Rode o projeto:**
```bash
streamlit run app.py
```

O navegador abrirá automaticamente com o projeto rodando.

## Tecnologias utilizadas
- Python
- Streamlit
- Google Gemini API
- python-dotenv
