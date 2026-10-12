"""
Luz & Palavra — Assistente de Estudos Bíblicos
Aplicação em Python + Streamlit + API Groq.

Instalação:
    pip install streamlit groq

Execução:
    streamlit run estudos_biblicos.py

Configure GROQ_API_KEY nos Secrets privados do Streamlit Cloud.
Nunca publique sua chave de API no GitHub.
"""

import streamlit as st
from groq import Groq

# --------------------------- Configuração da página ---------------------------
st.set_page_config(
    page_title="Luz & Palavra | Estudos Bíblicos",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------- Estilo visual ------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    .stApp {
        background:
            radial-gradient(circle at 90% 3%, rgba(203, 169, 106, 0.13), transparent 26%),
            linear-gradient(180deg, #fbfaf6 0%, #f4f1e8 100%);
        color: #26352d;
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #173b31 0%, #102a23 100%);
    }
    [data-testid="stSidebar"] * { color: #f7f4eb !important; }
    [data-testid="stSidebar"] input {
        color: #20372e !important;
        background: #fffdf8 !important;
    }
    .hero {
        padding: 2.0rem 2.2rem;
        border-radius: 24px;
        background: linear-gradient(120deg, #173b31 0%, #285545 70%, #426a50 100%);
        color: #fffaf0;
        border: 1px solid rgba(255,255,255,.12);
        box-shadow: 0 14px 34px rgba(25, 55, 42, .14);
        margin-bottom: 1.3rem;
    }
    .hero h1 {
        font-family: 'Playfair Display', Georgia, serif;
        color: #fffaf0;
        font-size: clamp(2rem, 4vw, 3.15rem);
        margin: 0 0 .4rem 0;
        line-height: 1.12;
    }
    .hero p { color: #e6eadf; font-size: 1.03rem; margin: 0; }
    .eyebrow {
        color: #e4c58b;
        text-transform: uppercase;
        letter-spacing: .16em;
        font-size: .72rem;
        font-weight: 700;
        margin-bottom: .7rem;
    }
    .section-card {
        background: rgba(255, 255, 255, .78);
        border: 1px solid #e7e0d2;
        padding: 1.1rem 1.25rem;
        border-radius: 18px;
        margin-bottom: .8rem;
    }
    .section-card h3 { color: #214637; margin-top: 0; }
    .small-muted { color: #68766d; font-size: .9rem; }
    /* Contraste consistente em todas as abas e respostas */
    .stApp, .stApp p, .stApp li, .stApp label,
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span {
        color: #26352d;
    }
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    .stApp label {
        color: #34473b !important;
        opacity: 1 !important;
    }

    /* Abas: corrigir texto branco antes e depois do hover */
    div[data-testid="stTabs"] button,
    div[data-testid="stTabs"] button *,
    div[data-testid="stTabs"] [role="tab"],
    div[data-testid="stTabs"] [role="tab"] * {
        color: #214637 !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stTabs"] button:hover,
    div[data-testid="stTabs"] button:hover *,
    div[data-testid="stTabs"] [role="tab"]:hover,
    div[data-testid="stTabs"] [role="tab"]:hover * {
        color: #102a23 !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"],
    div[data-testid="stTabs"] button[aria-selected="true"] *,
    div[data-testid="stTabs"] [role="tab"][aria-selected="true"],
    div[data-testid="stTabs"] [role="tab"][aria-selected="true"] * {
        color: #173b31 !important;
        font-weight: 700 !important;
    }

    /* Controles claros: texto digitado escuro, placeholder cinza */
    .stApp input,
    .stApp textarea,
    .stApp [data-baseweb="input"] input,
    .stApp [data-baseweb="textarea"] textarea,
    .stApp [data-baseweb="select"] div {
        color: #26352d !important;
        -webkit-text-fill-color: #26352d !important;
    }
    .stApp input::placeholder,
    .stApp textarea::placeholder {
        color: #68766d !important;
        -webkit-text-fill-color: #68766d !important;
        opacity: 1 !important;
    }

    /* Respostas do assistente: impedir títulos brancos no fundo claro */
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] *,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMarkdownContainer"] em {
        color: #26352d !important;
        opacity: 1 !important;
    }
    [data-testid="stChatMessage"] {
        color: #26352d !important;
    }
    .stButton > button, .stFormSubmitButton > button {
        border-radius: 12px;
        border: 0;
        font-weight: 700;
        min-height: 2.7rem;
    }
    .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
        background: #214f3e;
        color: white;
    }
    div[data-testid="stChatMessage"] {
        border-radius: 16px;
        border: 1px solid #e8e1d5;
        background: rgba(255,255,255,.7);
    }
    .verse-box {
        border-left: 4px solid #c49b55;
        background: #fffaf0;
        padding: 1rem 1.2rem;
        border-radius: 0 14px 14px 0;
        color: #34473b;
        margin: .8rem 0 1rem 0;
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------- Prompts da IA ------------------------------------
BASE_PROMPT = """
Você é o Luz & Palavra, um assistente de apoio ao estudo bíblico.
Seu objetivo é ajudar pessoas a ler, compreender, discutir e aplicar a Bíblia
com respeito, clareza e humildade.

Regras:
- Responda em português brasileiro, com linguagem acolhedora, clara e didática.
- Diferencie o que o texto bíblico diz, o contexto histórico-literário e possíveis
  interpretações. Quando houver diferenças entre tradições cristãs, deixe isso claro.
- Sempre que explicar uma pessoa, acontecimento, viagem, reino, carta ou passagem
  bíblica com contexto histórico, informe também o período/data aproximada (por exemplo,
  "por volta de 400 a.C.") e o local/região relacionado ao acontecimento, quando isso
  for relevante para a compreensão.
- Se a data ou o local exato não forem conhecidos, forneça uma estimativa histórica
  razoável e identifique explicitamente como aproximada ("cerca de", "provavelmente",
  "a localização exata é incerta"). Se nem uma estimativa confiável estiver disponível,
  diga isso claramente em vez de inventar precisão.
- Separe datas e locais mencionados diretamente no texto bíblico daqueles estimados
  por estudiosos. Quando existirem hipóteses diferentes, apresente-as brevemente.
- Não invente citações, versículos, referências ou palavras bíblicas. Se não tiver
  certeza do texto exato, informe a referência e peça que a pessoa confira em sua Bíblia.
- Evite afirmar que existe apenas uma interpretação quando o tema é debatido.
- Não substitua a leitura direta da Bíblia, o diálogo com responsáveis religiosos
  ou o discernimento da comunidade.
- Não trate a IA como autoridade espiritual infalível.
- Ao sugerir aplicações práticas, seja respeitoso e não culpabilize a pessoa.
"""

STUDY_PROMPT = BASE_PROMPT + """
Para pedidos de estudo, organize a resposta, quando apropriado, em:
1. Tema e objetivo do estudo
2. Texto ou passagens bíblicas para ler
3. Contexto e explicação em linguagem simples
4. Ideias principais
5. Perguntas para reflexão
6. Aplicação prática
7. O que vale conferir diretamente no texto bíblico
Não invente o texto integral de passagens bíblicas.
"""

CHILDREN_PROMPT = BASE_PROMPT + """
Você é também um educador que ajuda adultos a preparar conversas bíblicas para crianças.
Crie material adequado à idade indicada, simples, seguro e participativo.
Inclua: objetivo, história/passagem para o adulto ler na Bíblia, explicação infantil,
perguntas abertas, respostas esperadas apenas como orientação para o adulto,
uma atividade ou brincadeira sem materiais caros e uma frase para memorizar.
Não use medo, ameaça, vergonha ou pressão emocional para ensinar.
Não apresente paráfrases como se fossem citações literais da Bíblia.
"""

CHAT_PROMPT = BASE_PROMPT + """
Converse de forma natural. Faça perguntas de esclarecimento se faltar contexto.
Ajude a pessoa a pensar e a conferir as referências na própria Bíblia.
"""

# --------------------------- Estado da sessão ---------------------------------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "study_result" not in st.session_state:
    st.session_state.study_result = ""
if "kids_result" not in st.session_state:
    st.session_state.kids_result = ""
if "reading_plan" not in st.session_state:
    st.session_state.reading_plan = ""

# --------------------------- Barra lateral ------------------------------------
with st.sidebar:
    st.markdown("## 📖 Luz & Palavra")
    st.markdown("Seu espaço de apoio para estudar, refletir e preparar encontros bíblicos.")
    st.markdown("---")
    st.markdown("### 🔐 Inteligência artificial")
    st.caption("A conexão é configurada pelo responsável pelo aplicativo.")
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = ""
        st.warning("A chave GROQ_API_KEY não está configurada nos Secrets do Streamlit.")
    model = st.selectbox(
        "Modelo de IA",
        options=["openai/gpt-oss-120b", "llama-3.3-70b-versatile"],
        index=0,
        help="Se um modelo não estiver disponível para sua conta, selecione o outro.",
    )
    st.markdown("---")
    st.markdown("### ✨ O que você pode fazer")
    st.markdown(
        "- Preparar estudos por tema ou passagem\n"
        "- Criar perguntas bíblicas para crianças\n"
        "- Conversar e tirar dúvidas\n"
        "- Montar um plano de leitura"
    )
    st.markdown("---")
    st.caption("A IA pode errar referências ou interpretações. Confira sempre na sua Bíblia.")
    st.caption("Desenvolvido em Python com Streamlit e Groq.")

client = None
if api_key:
    try:
        client = Groq(api_key=api_key.strip())
    except Exception as exc:
        st.sidebar.error(f"Não foi possível iniciar a conexão: {exc}")

def ask_ai(system_prompt: str, user_prompt: str, temperature: float = 0.5) -> str:
    """Envia uma solicitação à API e retorna a resposta da IA."""
    if client is None:
        raise RuntimeError("A conexão com a IA não está configurada. O responsável pelo aplicativo deve verificar os Secrets do Streamlit.")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=2500,
    )
    answer = response.choices[0].message.content
    return answer.strip() if answer else "A IA não retornou uma resposta. Tente novamente."

def render_result(title: str, content: str):
    st.markdown(f"### {title}")
    st.markdown(content)
    st.download_button(
        "⬇️ Salvar conteúdo em TXT",
        data=content,
        file_name="luz_e_palavra_estudo.txt",
        mime="text/plain",
        key=f"download_{title}_{len(content)}",
    )

# --------------------------- Cabeçalho ----------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">LEITURA • REFLEXÃO • PRÁTICA</div>
        <h1>Estude a Palavra com propósito.</h1>
        <p>Prepare estudos, crie perguntas para crianças e explore dúvidas com apoio da IA.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="section-card"><h3>📚 Estudo bíblico</h3><span class="small-muted">Tema, passagem, contexto e reflexão.</span></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="section-card"><h3>🧒 Para crianças</h3><span class="small-muted">Perguntas, atividades e explicações por idade.</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="section-card"><h3>💬 Converse</h3><span class="small-muted">Faça perguntas e aprofunde sua leitura.</span></div>', unsafe_allow_html=True)

study_tab, children_tab, chat_tab, plan_tab, about_tab = st.tabs(
    ["📖 Estudo bíblico", "🧒 Perguntas para crianças", "💬 Pergunte à IA", "🗓️ Plano de leitura", "ℹ️ Sobre"]
)

# --------------------------- Aba: estudo bíblico ------------------------------
with study_tab:
    st.subheader("Monte seu estudo")
    st.write("Defina um tema ou uma passagem. A IA ajudará a organizar o estudo; confira as referências na Bíblia.")
    with st.form("study_form"):
        c1, c2 = st.columns([1.25, 1])
        with c1:
            study_topic = st.text_input(
                "Tema ou dúvida",
                placeholder="Ex.: perdão, coragem, parábola do bom samaritano",
            )
            bible_passage = st.text_input(
                "Passagem bíblica (opcional)",
                placeholder="Ex.: Lucas 10:25–37",
            )
        with c2:
            audience = st.selectbox(
                "Para quem é o estudo?",
                ["Estudo individual", "Grupo de jovens", "Adultos", "Crianças", "Grupo misto"],
            )
            depth = st.select_slider(
                "Nível de profundidade",
                options=["Simples", "Intermediário", "Aprofundado"],
                value="Intermediário",
            )
        study_goal = st.text_area(
            "O que você quer compreender ou preparar?",
            placeholder="Ex.: entender o contexto, preparar uma reunião ou refletir sobre como aplicar o ensinamento.",
            height=100,
        )
        submit_study = st.form_submit_button("✨ Preparar estudo", type="primary", use_container_width=True)

    if submit_study:
        if not study_topic.strip() and not bible_passage.strip():
            st.warning("Informe um tema ou uma passagem bíblica para começar.")
        elif client is None:
            st.warning("A conexão com a IA não está configurada. Avise o responsável pelo aplicativo.")
        else:
            request = (
                f"Prepare um estudo bíblico.\nTema: {study_topic or 'Não especificado'}\n"
                f"Passagem: {bible_passage or 'Sugerir referências para leitura'}\n"
                f"Público: {audience}\nProfundidade: {depth}\n"
                f"Objetivo e contexto: {study_goal or 'Não informado'}\n"
                "Use títulos claros, perguntas para reflexão e aplicações cuidadosas. "
                "Não invente citações literais."
            )
            with st.spinner("Organizando o estudo..."):
                try:
                    st.session_state.study_result = ask_ai(STUDY_PROMPT, request)
                except Exception as exc:
                    st.error(f"Não foi possível gerar o estudo: {exc}")
    if st.session_state.study_result:
        render_result("Seu estudo", st.session_state.study_result)

# --------------------------- Aba: crianças ------------------------------------
with children_tab:
    st.subheader("Crie perguntas bíblicas para crianças")
    st.write("Prepare uma conversa participativa, com linguagem adequada à idade e sem transformar o momento em uma prova.")
    with st.form("children_form"):
        cc1, cc2 = st.columns(2)
        with cc1:
            kids_topic = st.text_input(
                "História, tema ou passagem",
                placeholder="Ex.: Noé, Davi e Golias, amor ao próximo",
            )
            kids_age = st.selectbox(
                "Faixa etária",
                ["3–5 anos", "6–8 anos", "9–11 anos", "12–14 anos"],
                index=1,
            )
        with cc2:
            kids_count = st.slider("Quantidade de perguntas", min_value=3, max_value=15, value=8)
            kids_format = st.selectbox(
                "Tipo de perguntas",
                [
                    "Misturadas: compreensão e aplicação",
                    "Perguntas simples e diretas",
                    "Múltipla escolha",
                    "Verdadeiro ou falso",
                    "Perguntas para conversar em grupo",
                ],
            )
        kids_context = st.text_area(
            "Contexto da atividade (opcional)",
            placeholder="Ex.: aula de 20 minutos, grupo de crianças, tema da semana...",
            height=85,
        )
        include_answers = st.checkbox("Incluir respostas sugeridas para o adulto", value=True)
        include_activity = st.checkbox("Incluir uma brincadeira ou atividade rápida", value=True)
        submit_kids = st.form_submit_button("🎈 Criar perguntas", type="primary", use_container_width=True)

    if submit_kids:
        if not kids_topic.strip():
            st.warning("Informe uma história, tema ou passagem bíblica.")
        elif client is None:
            st.warning("A conexão com a IA não está configurada. Avise o responsável pelo aplicativo.")
        else:
            request = (
                f"Crie uma atividade bíblica infantil sobre: {kids_topic}.\n"
                f"Idade: {kids_age}\nQuantidade de perguntas: {kids_count}\n"
                f"Formato: {kids_format}\nContexto: {kids_context or 'Não informado'}\n"
                f"Incluir respostas sugeridas para o adulto: {'sim' if include_answers else 'não'}.\n"
                f"Incluir atividade ou brincadeira: {'sim' if include_activity else 'não'}.\n"
                "Organize em: objetivo, passagem para o adulto conferir na Bíblia, explicação para a idade, "
                "perguntas numeradas e fechamento acolhedor. Se houver respostas, deixe claro que são sugestões "
                "para orientar o adulto, não um gabarito rígido para a criança."
            )
            with st.spinner("Preparando uma atividade para a turma..."):
                try:
                    st.session_state.kids_result = ask_ai(CHILDREN_PROMPT, request, temperature=0.65)
                except Exception as exc:
                    st.error(f"Não foi possível criar as perguntas: {exc}")
    if st.session_state.kids_result:
        render_result("Atividade para crianças", st.session_state.kids_result)

# --------------------------- Aba: chat ----------------------------------------
with chat_tab:
    st.subheader("Converse com o assistente bíblico")
    st.write("Faça uma pergunta sobre uma passagem, um tema ou o contexto de um texto.")
    if st.button("🧹 Limpar conversa", key="clear_chat"):
        st.session_state.chat_messages = []
        st.rerun()

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat_input = st.chat_input("Ex.: Qual é o contexto de Filipenses 4:6–7?")
    if chat_input:
        if client is None:
            st.warning("A conexão com a IA ainda não está configurada pelo responsável pelo aplicativo.")
        else:
            st.session_state.chat_messages.append({"role": "user", "content": chat_input})
            with st.chat_message("user"):
                st.markdown(chat_input)
            with st.chat_message("assistant"):
                with st.spinner("Consultando o assistente..."):
                    try:
                        messages = [{"role": "system", "content": CHAT_PROMPT}]
                        messages.extend(st.session_state.chat_messages[-12:])
                        response = client.chat.completions.create(
                            model=model,
                            messages=messages,
                            temperature=0.55,
                            max_tokens=2000,
                        )
                        answer = response.choices[0].message.content or "Não consegui formular uma resposta."
                        st.markdown(answer)
                        st.session_state.chat_messages.append({"role": "assistant", "content": answer})
                    except Exception as exc:
                        st.error(f"Erro ao conversar com a IA: {exc}")

# --------------------------- Aba: plano de leitura ----------------------------
with plan_tab:
    st.subheader("Crie um plano de leitura")
    with st.form("plan_form"):
        plan_goal = st.text_input(
            "Objetivo de leitura",
            placeholder="Ex.: conhecer a vida de Jesus, ler Salmos ou estudar sobre sabedoria",
        )
        plan_duration = st.selectbox("Duração", ["7 dias", "14 dias", "21 dias", "30 dias"])
        plan_time = st.selectbox("Tempo disponível por dia", ["5 minutos", "10 minutos", "15 minutos", "20+ minutos"])
        plan_level = st.selectbox("Experiência com leitura bíblica", ["Estou começando", "Já leio às vezes", "Tenho hábito de leitura"])
        plan_submit = st.form_submit_button("🗓️ Montar meu plano", type="primary", use_container_width=True)

    if plan_submit:
        if not plan_goal.strip():
            st.warning("Informe um objetivo para o plano.")
        elif client is None:
            st.warning("A conexão com a IA não está configurada. Avise o responsável pelo aplicativo.")
        else:
            request = (
                f"Monte um plano de leitura bíblica de {plan_duration} sobre: {plan_goal}.\n"
                f"Tempo por dia: {plan_time}. Experiência: {plan_level}.\n"
                "Apresente uma tabela por dia com referências para leitura, foco da leitura e uma pergunta de reflexão. "
                "Não invente texto literal de versículos. Equilibre o volume de leitura e explique como recuperar um dia perdido sem culpa."
            )
            with st.spinner("Montando um plano realista..."):
                try:
                    st.session_state.reading_plan = ask_ai(STUDY_PROMPT, request)
                except Exception as exc:
                    st.error(f"Não foi possível montar o plano: {exc}")
    if st.session_state.reading_plan:
        render_result("Seu plano de leitura", st.session_state.reading_plan)

# --------------------------- Aba: sobre ---------------------------------------
with about_tab:
    st.subheader("Sobre o Luz & Palavra")
    st.markdown(
        """
        <div class="section-card">
        <h3>Uma ferramenta de apoio, não uma autoridade espiritual</h3>
        O Luz & Palavra usa inteligência artificial para ajudar a organizar estudos,
        preparar perguntas e estimular a leitura e a reflexão. A IA pode errar referências,
        contexto ou interpretações; confira os textos na sua Bíblia e converse com pessoas
        de confiança em sua comunidade religiosa.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("**Tecnologias usadas**")
    st.markdown("- Python: lógica da aplicação\n- Streamlit: interface web\n- Groq: acesso ao modelo de linguagem\n- `st.session_state`: histórico temporário da conversa")
    st.markdown("**Privacidade e segurança**")
    st.markdown(
        "- A chave da API é lida dos Secrets privados do Streamlit.\n"
        "- Nunca coloque sua chave diretamente no código-fonte ou no GitHub.\n"
        "- Não compartilhe dados pessoais ou informações privadas no chat.\n"
        "- A conversa fica na sessão atual; este exemplo não implementa banco de dados nem login."
    )

st.markdown("---")
st.caption("Luz & Palavra • Estude com curiosidade, confira as referências e converse com respeito.")
