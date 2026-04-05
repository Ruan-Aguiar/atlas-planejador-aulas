import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Carrega a chave do arquivo .env (local) ou dos Secrets do Streamlit (online)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

# Configura o Groq
client = Groq(api_key=api_key) if api_key else None

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="ATLAS – Planejador de Aulas",
    page_icon="📚",
    layout="centered"
)

# ── Estilo visual ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
    }

    .titulo {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1F60D8;
        margin-bottom: 0;
    }

    .subtitulo {
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
    }

    .boas-vindas {
        background-color: #f4f7ff;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #1F60D8;
        font-size: 0.97rem;
        color: #333;
        line-height: 1.7;
    }

    .area-selecionada {
        background-color: #e8f0fe;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        color: #1F60D8;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }

    .resultado-box {
        background-color: #f4f7ff;
        border-left: 4px solid #1F60D8;
        padding: 1.5rem;
        border-radius: 8px;
        white-space: pre-wrap;
        font-size: 0.95rem;
        line-height: 1.7;
    }

    .stButton > button {
        background-color: #1F60D8;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        border: none;
        width: 100%;
        font-size: 1rem;
    }

    .stButton > button:hover {
        background-color: #1549b0;
    }
</style>
""", unsafe_allow_html=True)

# ── Prompts por área ────────────────────────────────────────────────────────
INSTRUCOES_POR_AREA = {
    "Linguagens": """
        Foque em atividades de leitura, interpretação, produção textual e oralidade.
        Inclua sugestões de gêneros textuais relevantes para o tema.
        Considere o desenvolvimento da competência comunicativa dos alunos.
        Sugira atividades que estimulem a criatividade e a expressão.
    """,
    "Ciências Humanas": """
        Foque na análise crítica de contextos históricos, geográficos e sociais.
        Inclua sugestões de fontes primárias, mapas ou documentos históricos quando pertinente.
        Estimule o pensamento crítico e a reflexão sobre cidadania e sociedade.
        Proponha atividades de debate ou análise de diferentes perspectivas.
    """,
    "Ciências da Natureza": """
        Inclua obrigatoriamente uma atividade prática ou experimental, mesmo que simples.
        Relacione o conteúdo com situações do cotidiano dos alunos.
        Destaque o método científico quando aplicável.
        Sugira experimentos acessíveis com materiais simples quando possível.
    """,
    "Matemática": """
        Inclua obrigatoriamente exercícios práticos com níveis variados de dificuldade.
        Apresente ao menos uma situação-problema contextualizada do cotidiano.
        Indique fórmulas ou propriedades relevantes que devem ser trabalhadas.
        Sugira atividades que desenvolvam o raciocínio lógico e a resolução de problemas.
    """,
    "Outra": """
        Adapte o planejamento de forma interdisciplinar e flexível.
        Foque nos objetivos pedagógicos centrais do tema proposto.
    """
}

# ── Inicializa estado da sessão ─────────────────────────────────────────────
if "area_selecionada" not in st.session_state:
    st.session_state.area_selecionada = None

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown('<p class="titulo">📚 ATLAS</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Planejador de Aulas com Inteligência Artificial</p>', unsafe_allow_html=True)
st.divider()

# ── TELA 1: Boas-vindas e seleção de área ───────────────────────────────────
if st.session_state.area_selecionada is None:
    st.markdown("""
    <div class="boas-vindas">
        👋 <strong>Bem-vindo ao ATLAS!</strong><br><br>
        Aqui você gera planejamentos de aula completos e alinhados à BNCC em segundos,
        com a ajuda da Inteligência Artificial.<br><br>
        Para começar, selecione a <strong>área do conhecimento</strong> da sua disciplina:
    </div>
    """, unsafe_allow_html=True)

    areas = {
        "🗣️ Linguagens": "Linguagens",
        "🌍 Ciências Humanas": "Ciências Humanas",
        "🔬 Ciências da Natureza": "Ciências da Natureza",
        "📐 Matemática": "Matemática",
        "📌 Outra": "Outra"
    }

    col1, col2 = st.columns(2)
    area_keys = list(areas.keys())

    for i, label in enumerate(area_keys):
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.button(label, key=label):
                st.session_state.area_selecionada = areas[label]
                st.rerun()

# ── TELA 2: Formulário ──────────────────────────────────────────────────────
else:
    area = st.session_state.area_selecionada

    st.markdown(f'<div class="area-selecionada">📂 Área selecionada: {area}</div>', unsafe_allow_html=True)

    if st.button("← Trocar área"):
        st.session_state.area_selecionada = None
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Campos do formulário
    col1, col2 = st.columns(2)

    with col1:
        tema = st.text_input("Tema da aula *", placeholder="Ex: Fotossíntese")
        serie = st.text_input("Série / Ano *", placeholder="Ex: 7º ano do Ensino Fundamental")

    with col2:
        duracao = st.number_input("Duração (minutos) *", min_value=10, max_value=300, value=50, step=5)
        disciplina = st.text_input("Disciplina", placeholder="Ex: Ciências")

    habilidades = st.text_input(
        "Habilidades BNCC (opcional)",
        placeholder="Ex: EF07CI07 – Caracterizar os principais ecossistemas brasileiros"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Geração ─────────────────────────────────────────────────────────────
    if st.button("Gerar Planejamento"):

        # Validações
        erros = []
        if not tema.strip():
            erros.append("O campo **Tema da aula** é obrigatório.")
        if not serie.strip():
            erros.append("O campo **Série / Ano** é obrigatório.")
        if not api_key:
            erros.append("Chave da API não encontrada. Verifique o arquivo **.env**.")

        if erros:
            for erro in erros:
                st.warning(erro)
        else:
            with st.spinner("Gerando planejamento, aguarde..."):
                try:
                    instrucoes_area = INSTRUCOES_POR_AREA.get(area, "")

                    prompt = f"""
                    Monte um planejamento de aula detalhado com base nas seguintes informações:

                    Área do Conhecimento: {area}
                    Tema: {tema}
                    Série/Ano: {serie}
                    Duração: {duracao} minutos
                    Disciplina: {disciplina if disciplina.strip() else "Não especificada"}
                    Habilidades/BNCC: {habilidades if habilidades.strip() else "Não especificado"}

                    Instruções específicas para esta área:
                    {instrucoes_area}

                    Estruture o planejamento nos seguintes tópicos:
                    - Objetivos
                    - Conteúdos
                    - Metodologia
                    - Recursos Didáticos
                    - Avaliação
                    - Encerramento / Reflexão
                    """

                    resposta = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Você é um assistente pedagógico especializado em criação de planejamentos de aula claros, objetivos e alinhados à BNCC."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    planejamento = resposta.choices[0].message.content

                    st.success("Planejamento gerado com sucesso!")
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(planejamento)

                    # Botão de download
                    nome_arquivo = f"planejamento_{tema.strip().replace(' ', '_')}.txt"
                    st.download_button(
                        label="⬇️ Baixar como .txt",
                        data=planejamento,
                        file_name=nome_arquivo,
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"Erro ao gerar planejamento: {e}")