import streamlit as st
import openai

# --- CONFIG ---
st.set_page_config(page_title="MentorApp PRO", layout="wide")

# Настройки стиля для визуалов
st.markdown("""
    <style>
    .stAlert { border-radius: 10px; }
    .lesson-card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 8px solid #007bff; margin-bottom: 20px; }
    .st-emotion-cache-16ids93 { font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SETTINGS & AI ---
st.sidebar.title("🛠 Настройки")
ai_provider = st.sidebar.selectbox("ИИ Движок", ["OpenAI", "DeepSeek"])
api_key = st.sidebar.text_input(f"Ключ {ai_provider}", type="password")

st.sidebar.divider()
chapter = st.sidebar.radio("Курс: Сети & ИБ", [
    "1. OSI и Физика сети",
    "2. IP, DNS и Маршруты",
    "3. Шифрование и Web (HTTPS)",
    "4. Взломы и Защита периметра"
])

# --- AI AGENT LOGIC ---
def ask_tutor(question, current_chapter):
    if not api_key:
        return "⚠️ Введите API ключ в меню слева."
    try:
        # Системная установка (Тот самый 'умный' ассистент)
        system_instr = f"""
        Ты - элитный IT-ментор. Твой ученик - руководитель поддержки в проекте Росимущество.
        Твоя задача: объяснять сложные темы Сетей и ИБ максимально наглядно.
        Используй аналогии из жизни и бизнеса. Текущая тема: {current_chapter}.
        Если вопрос не по теме - кратко ответь и верни ученика к обучению.
        """
        
        base_url = "https://api.deepseek.com" if ai_provider == "DeepSeek" else None
        model = "deepseek-chat" if ai_provider == "DeepSeek" else "gpt-4-turbo-preview"
        
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_instr},
                {"role": "user", "content": question}
            ]
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Ошибка связи с ИИ: {str(e)}"

# --- UI LAYOUT ---
col_content, col_ai = st.columns([1.5, 1])

with col_content:
    if chapter == "1. OSI и Физика сети":
        st.title("🌐 Глава 1: Фундамент (OSI)")
        st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
        st.subheader("Как данные превращаются в ток")
        st.write("Любой сбой в Росимуществе начинается здесь. Если пакет не ушел с уровня 1, уровень 7 (сайт) не поможет.")
        st.graphviz_chart('''
            digraph {
                rankdir=LR; node [shape=box, style=filled, fillcolor="#E3F2FD"];
                "7.Приложение" -> "4.Транспорт" -> "3.Сетевой (IP)" -> "1.Кабель";
                "1.Кабель" -> "3.Сетевой (IP)" -> "4.Транспорт" -> "7.Приложение";
            }
        ''')
        st.info("**Задание:** Вспомни, когда в офисе пропадал интернет. Это был 'слой 1' (кабель) или 'слой 3' (настройки роутера)?")
        st.markdown('</div>', unsafe_allow_html=True)

    elif chapter == "2. IP, DNS и Маршруты":
        st.title("🗺 Глава 2: Навигация в сети")
        st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
        st.subheader("DNS — это телефонная книга интернета")
        st.write("Когда ты вводишь 'gov.ru', твой ПК не знает, куда идти. Он спрашивает у DNS-сервера IP-адрес.")
        st.graphviz_chart('''
            digraph {
                node [shape=ellipse, style=filled, fillcolor="#FFF9C4"];
                "Твой ПК" -> "DNS Сервер" [label="Где живет сайт?"];
                "DNS Сервер" -> "Твой ПК" [label="Его IP: 95.173.x.x"];
            }
        ''', use_container_width=True)
        st.warning("**ИБ-риск:** Хакеры могут подменить ответ DNS и увести тебя на фальшивый сайт-клон.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif chapter == "3. Шифрование и Web (HTTPS)":
        st.title("🔐 Глава 3: Секретные разговоры")
        st.write("Разбираем SSL-сертификаты и почему 'замочек' в браузере — это важно.")
        st.image("https://img.icons8.com/clouds/200/lock.png") # Просто визуальный акцент

    elif chapter == "4. Взломы и Защита периметра":
        st.title("🏴‍☠️ Глава 4: Как нас ломают")
        st.error("Топ-1 атака на госсектор: Социальная инженерия.")
        st.write("Никакой Firewall не спасет, если админ нажал на ссылку в почте.")

with col_ai:
    st.subheader("🤖 Твой Тьютор")
    st.write(f"Задавай любые вопросы по главе: *{chapter}*")
    
    # Чат в реальном времени
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Напиши мне...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.chat_message("assistant"):
            response = ask_tutor(user_input, chapter)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
