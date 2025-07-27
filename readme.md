# Fluxo Geral
WhatsApp -> Webhook (POST JSON) -> Processamento Backend:
- Extrai telefone do user
- Carrega ou cria sessao no Redis
- Valida a tentativa enviada
- Atualiza a sessão
- Gera resposta formatada
```
Tentativas X / 6
Tentativas:
    1: XXXXX / ⬛⬛🟩⬛🟨
    2: XXXXX / ⬛🟩⬛🟨🟨
    ...
```
- Envia resposta para o user

# Requisitos
- Usuario pode jogar com amigos em grupo (FUTURO)
- Usuario recebe instruções suficientes
  - "🟨 na letra E significa que ela está na palavra, mas em posição diferente."
  - 
- Usuario deve visualizar as tentativas anteriores
- Usuario deve perceber claramente as letras corretas
- Usuario deve saber claramente quando o jogo terminou
- Usuario nao perde tentativas ao tentar a mesma palavra
- Usuario nao perde tentativas ao tentar palavras inventadas
- Sistema nao aceita palavras inventadas
- Apos inatividade o usuario recebe novamente as instrucoes de uso do game
- Apos o resultado final da sessao sistema envia dados da sessao para o bd historico e apaga a sessao do redis

# Folder Structure
```
wordle-bot/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── webhook.py           # Endpoint do WhatsApp
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py            # Configurações e variáveis de ambiente
│   ├── crud/
│   │   ├── __init__.py
│   │   └── crud_game.py         # Funções para salvar no PostgreSQL
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py          # Conexão com PostgreSQL (SQLAlchemy)
│   │   └── redis_client.py      # Conexão com Redis
│   ├── models/
│   │   ├── __init__.py
│   │   └── game_history.py      # Modelo da tabela do PostgreSQL
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── game.py              # Pydantic Schemas para validação de dados
│   └── services/
│       ├── __init__.py
│       ├── game_logic.py        # A lógica pura do jogo Wordle
│       ├── response_formatter.py  # Formata as mensagens de resposta
│       └── whatsapp_client.py   # Envia mensagens para a API do WhatsApp
├── data/
│   └── words.txt                # Dicionário de palavras
├── .dockerignore
├── .env.example                 # Exemplo de variáveis de ambiente
├── Dockerfile
├── main.py                      # Ponto de entrada da aplicação
└── requirements.txt
```

# Observability
## Traçar ciclo completo:
    webhook -> Redis -> PostgreSQL -> resposta

# Painel Admin
- Tela FASTAPI com autenticacao
- estatisticas, jogos ativos, erros do sentry, log do redis