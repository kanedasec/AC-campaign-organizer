from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    # IMPORTANTE: incluir cascade também para maps
    maps   = db.relationship("Map",   backref="campaign", lazy=True, cascade="all, delete-orphan")
    guilds = db.relationship("Guild", backref="campaign", lazy=True, cascade="all, delete-orphan")

class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False)
    guilda_vencedora = db.Column(db.String(50), nullable=True)  # "Vermelha", "Azul", "Laranja", "Verde" ou None

class Guild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False)
    heroes = db.relationship("Hero", backref="guild", lazy=True, cascade="all, delete-orphan")

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    guild_id = db.Column(db.Integer, db.ForeignKey("guild.id", ondelete="CASCADE"), nullable=False)

    # Campos extras (se quiser mantê-los agora ou depois):
    defesa = db.Column(db.Integer, nullable=True)
    vida = db.Column(db.Integer, nullable=True)
    habilidade = db.Column(db.String(200), nullable=True)
    efeito = db.Column(db.String(300), nullable=True)
    death_tokens = db.Column(db.Integer, default=0, nullable=False)

class Curse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Integer, nullable=False)
    tier = db.Column(db.Integer, nullable=False)
    efeito = db.Column(db.String(300), nullable=False)
    qtd = db.Column(db.Integer, nullable=False)

class HeroMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey("hero.id", ondelete="CASCADE"))
    map_id = db.Column(db.Integer, db.ForeignKey("map.id", ondelete="CASCADE"))

    death_tokens = db.Column(db.Integer, default=0)
    curse_nome = db.Column(db.String(100), nullable=True)
    curse_valor = db.Column(db.Integer, nullable=True)
    curse_efeito = db.Column(db.String(300), nullable=True)

    hero = db.relationship("Hero", backref="maps")
    mapa = db.relationship("Map", backref="heroes_status")
