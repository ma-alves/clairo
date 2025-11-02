# clairo
Batizado em homenagem a cantora indie, clairo é um chat app desenvolvido com o intuito de explorar as possibilidades de WebSockets, utilizando código assíncrono em seu consumidor através do Django Channels e Redis como Message Broker. O foco é o desenvolvimento do backend, enquanto o frontend possui uma interface simples e intuitiva construída utilizando Tailwind.

## Tech Stack
- [Django](https://github.com/django) - Web Framework
- [Channels](https://github.com/django/channels) - Extensão do Django para código assíncrono
- [Daphne](https://github.com/django/daphne) - Servidor
- [SQLite3](https://www.sqlite.org/index.html) - Banco de Dados SQL
- [Redis](https://redis.io/) - Message Broker
- [Tailwind](https://tailwindcss.com/) - CSS Framework
- [Docker](https://www.docker.com/) - Container para o Redis

## Uso
1. Clone este repositório:\
`git clone https://github.com/ma-alves/clairo.git`
2. Crie o banco de dados:\
`touch database.db`
3. Suba o container redis:\
`docker run --rm -p 6379:6379 redis:7`
5. Em progresso :)
