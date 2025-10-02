# 🎲 Arcadia Quest Organizer

Organizador de campanhas do boardgame **Arcadia Quest**, feito em **Flask + SQLAlchemy**.  
Este sistema permite que **Admins** e **Players** acompanhem guildas, heróis, mapas, death tokens e curses ao longo da campanha.

![Python](https://img.shields.io/badge/python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/flask-2.x-black?logo=flask)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Funcionalidades

### 👑 Admin
- Criar e gerenciar campanhas
- Adicionar mapas e guildas
- Atribuir heróis às guildas
- Registrar **death tokens** por herói em cada mapa
- Aplicar **death curses** automaticamente com base nos tokens
- Definir guilda vencedora por mapa

### 🎮 Player
- Visualizar detalhes da campanha
- Consultar guildas e heróis
- Acompanhar tokens e curses por mapa
- Ver **linha do tempo** da campanha (timeline estilizada)

---

## 🚀 Tecnologias
- [Python 3.12](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- SQLite (default)

---

## ⚙️ Instalação e Uso

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/arcadia-quest-organizer.git
cd arcadia-quest-organizer/arcadia_web
```

### 2. Crie um ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Rode a aplicação
```bash
python app.py
```

Acesse no navegador:  
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Testando via cURL

### Criar campanha
```bash
curl -X POST http://127.0.0.1:5000/admin/campaign/create   -F "nome=Campanha Teste"
```

### Adicionar guilda
```bash
curl -X POST http://127.0.0.1:5000/admin/campaign/1/add_guild   -F "nome=Azul"
```

### Adicionar herói
```bash
curl -X POST http://127.0.0.1:5000/admin/guild/1/add_hero   -F "nome=Seth"
```

---

## 📸 Screenshots

### Dashboard Admin
![Admin Dashboard](docs/admin-dashboard.png)

### Timeline Player
![Timeline Player](docs/timeline.png)

---

## 📌 Próximos Passos

- [ ] **Autenticação real** (usuários e senhas, em vez de `session["role"]`)
- [ ] **Salvar progressão de campanhas** em JSON exportável
- [ ] Criar opção de **resetar mapas** de uma campanha
- [ ] Adicionar suporte a **PostgreSQL** ou **MySQL** para produção
- [ ] Melhorar UI com [Bootstrap](https://getbootstrap.com/) ou [TailwindCSS](https://tailwindcss.com/)
- [ ] Deploy via [Docker](https://www.docker.com/) ou [Render/Heroku](https://render.com/)

---

## 📜 Licença
Distribuído sob licença MIT.  
Sinta-se livre para usar, modificar e contribuir! 🖤
