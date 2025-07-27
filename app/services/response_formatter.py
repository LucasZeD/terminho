def format_attempts(session: dict) -> str:
    history = ""
    for i, attempt in enumerate(session["guesses"]):
        result_emojis = "".join(attempt["result"])
        history += f"{i+1}: {attempt['word']} / {result_emojis}\n"
    return history.strip()

def format_current_game(session: dict) -> str:
    attempts_left = 6 - len(session["guesses"])
    header = f"Tentativa atual: {len(session['guesses'])} / 6\n"
    history = format_attempts(session)
    return f"{header}\n*Suas tentativas:*\n{history}"

def get_initial_instructions() -> str:
    return(
        "Bem-vindo ao Terminho para Telegram! 🎮\n\n"
        "Adivinhe a palavra de 5 letras em 6 tentativas.\n"
        "Após cada tentativa, as cores mostrarão o quão perto você está:\n\n"
        "🟩 Letra correta na posição correta.\n"
        "🟨 Letra correta na posição errada.\n"
        "⬛ Letra não está na palavra.\n\n"
        "Envie sua primeira palavra de 5 letras para começar!"
    )
    
def format_final_message(session: dict) -> str:
    history = format_attempts(session)
    if session["status"] == "WON":
        message = f"Parabéns, você acertou! 🥳\nA palavra era *{session['secret_word']}*.\n\n{history}"
    else: # LOST
        message = f"Que pena, não foi dessa vez! 😥\nA palavra era *{session['secret_word']}*.\n\n{history}"
    
    message += "\n\nPara jogar novamente, envie qualquer mensagem."
    return message