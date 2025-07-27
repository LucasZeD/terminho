# Terminho Bot para Telegram

Um bot de Telegram robusto e escalável para jogar "Terminho" (a versão brasileira de Wordle), construído com uma arquitetura moderna e práticas de desenvolvimento profissional. Este projeto serve como um estudo de caso completo em design de sistemas, deploy automatizado e gerenciamento de estado.

**Para jogar agora, encontre o bot no Telegram:** `[@terminhobot]` ou clique [aqui](https://t.me/terminhobot).

---

## 🚀 Stack de Tecnologias

| Camada | Tecnologia | Motivo da Escolha |
| :--- | :--- | :--- |
| **Plataforma** | Telegram | API amigável para desenvolvedores e ideal para projetos MVP. |
| **Backend** | Python (FastAPI) | Alto desempenho para operações de I/O, tipagem moderna e ecossistema robusto. |
| **Persistência de Sessão**| Redis | Acesso em memória de baixíssima latência para gerenciar o estado dos jogos ativos. |
| **Persistência Histórica**| PostgreSQL | Confiabilidade (ACID) e queries relacionais ricas para histórico e estatísticas. |
| **Deployment** | Docker | Garante a paridade entre os ambientes de desenvolvimento e produção. |
| **Hospedagem** | Render (PaaS) | Plano gratuito robusto que suporta Web Service, Redis e PostgreSQL. |
| **CI/CD** | GitHub Actions | Automação do deploy a cada `push`, garantindo agilidade e confiabilidade. |

---

## 🏛️ Diagrama da Arquitetura

Este projeto utiliza uma arquitetura desacoplada para garantir escalabilidade e manutenção. A lógica do jogo é independente da plataforma de mensagens e da infraestrutura de hospedagem.

![Diagrama da Arquitetura do Bot](link)

**Fluxo de uma mensagem:**
1.  O usuário envia uma mensagem para o bot no **Telegram**.
2.  O Telegram envia um `POST` JSON para um **Webhook** exposto pela nossa aplicação.
3.  A aplicação, rodando no **Render** dentro de um container **Docker**, recebe a requisição.
4.  A aplicação busca ou cria a sessão do jogador no **Redis** para obter o estado atual do jogo.
5.  A lógica do jogo processa a tentativa.
6.  Ao final de um jogo, o resultado é salvo de forma permanente no **PostgreSQL**.
7.  A resposta é formatada e enviada de volta ao usuário através da API do Telegram.

---

## Requisitos
- Usuario pode jogar com amigos em grupo (FUTURO)
- Usuario recebe instruções suficientes
  - Ex:. "🟨 na letra E significa que ela está na palavra, mas em posição diferente."
- Usuario deve visualizar as tentativas anteriores
- Usuario deve perceber claramente as letras corretas
- Usuario deve saber claramente quando o jogo terminou
- Usuario nao perde tentativas ao tentar a mesma palavra
- Usuario nao perde tentativas ao tentar palavras inventadas
- Sistema nao aceita palavras inventadas
- Apos inatividade o usuario recebe novamente as instrucoes de uso do game
- Apos o resultado final da sessao sistema envia dados da sessao para o bd historico e apaga a sessao do redis

---

## Pastas
```
wordle-bot/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── webhook.py           # Endpoint do mensageiro
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
│       └── Telegram_client.py   # Envia mensagens para a API do Telegram
├── data/
│   └── words.txt                # Dicionário de palavras
├── .dockerignore
├── .env.example                 # Exemplo de variáveis de ambiente
├── Dockerfile
├── main.py                      # Ponto de entrada da aplicação
└── requirements.txt
```

---

## ✨ Funcionalidades

* Lógica completa do jogo Termo/Wordle.
* Validação de palavras contra um dicionário completo.
* Não penaliza o usuário por tentativas repetidas ou inválidas.
* Gerenciamento de sessão individual por usuário.
* Histórico de tentativas exibido a cada jogada.
* Persistência de histórico de jogos para futuras estatísticas.
* Painel de administração (em desenvolvimento) para visualização de estatísticas e jogos ativos.

---

## Desafios

1.  **Por que Redis *e* PostgreSQL?**
    * Optei por uma estratégia de persistência dupla. O **Redis** é usado para o estado efêmero das sessões ativas, onde a velocidade de leitura/escrita é crítica. O **PostgreSQL** serve como o registro permanente e confiável do histórico, permitindo análises futuras e garantindo que