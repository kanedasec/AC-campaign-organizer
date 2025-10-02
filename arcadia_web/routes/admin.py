from flask import Blueprint, render_template, request, redirect, session, abort
from models import db, Campaign, Guild, Hero, Map, HeroMap
from data import herois as HEROES_DATA, death_curses
import random

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ------------------
# Helpers para curses
# ------------------
def deck_preparer():
    curse_deck = [card for card in death_curses for _ in range(card["Qtd"])]
    random.shuffle(curse_deck)
    return curse_deck

def curse_applier(death_tokens, curse_deck):
    if death_tokens <= 2:
        possible_deck = [card for card in curse_deck if card["Tier"] <= death_tokens]
    else:
        possible_deck = curse_deck[:]

    if not possible_deck:
        return None

    picked_cards = [random.choice(possible_deck) for _ in range(death_tokens or 1)]
    return max(picked_cards, key=lambda c: c["Valor"])


# ------------------
# Rotas Admin
# ------------------
@admin_bp.route("/")
def dashboard():
    if session.get("role") != "admin":
        return "Acesso negado"
    campaigns = Campaign.query.all()
    return render_template("admin_dashboard.html", campaigns=campaigns)


@admin_bp.route("/campaign/create", methods=["POST"])
def create_campaign():
    if session.get("role") != "admin":
        return "Acesso negado"

    nome = request.form["nome"].strip()
    c = Campaign(nome=nome)
    db.session.add(c)
    db.session.commit()

    # cria 5 mapas
    for i in range(1, 6):
        db.session.add(Map(nome=f"Mapa {i}", campaign_id=c.id))

    # cria 4 guildas
    for g_nome in ["Vermelha", "Azul", "Laranja", "Verde"]:
        db.session.add(Guild(nome=g_nome, campaign_id=c.id))

    db.session.commit()
    return redirect("/admin")


@admin_bp.route("/campaign/<int:campaign_id>")
def campaign_detail(campaign_id):
    if session.get("role") != "admin":
        return "Acesso negado"
    c = Campaign.query.get_or_404(campaign_id)
    return render_template("campaign_detail.html", campaign=c)


@admin_bp.route("/campaign/<int:campaign_id>/add_guild", methods=["POST"])
def add_guild(campaign_id):
    if session.get("role") != "admin":
        return "Acesso negado"
    nome = request.form["nome"].strip().capitalize()
    g = Guild(nome=nome, campaign_id=campaign_id)
    db.session.add(g)
    db.session.commit()
    return redirect(f"/admin/campaign/{campaign_id}")


@admin_bp.route("/campaign/<int:campaign_id>/add_map", methods=["POST"])
def add_map(campaign_id):
    if session.get("role") != "admin":
        return "Acesso negado"
    nome = request.form["nome"].strip().capitalize()
    m = Map(nome=nome, campaign_id=campaign_id)
    db.session.add(m)
    db.session.commit()
    return redirect(f"/admin/campaign/{campaign_id}")


@admin_bp.route("/guild/<int:guild_id>/add_hero", methods=["POST"])
def add_hero_to_guild(guild_id):
    if session.get("role") != "admin":
        return "Acesso negado"

    nome = request.form["nome"].strip().capitalize()
    dados = next((h for h in HEROES_DATA if h["Herói"].lower() == nome.lower()), None)
    if not dados:
        return f"Herói '{nome}' não encontrado!", 400

    h = Hero(
        nome=dados["Herói"],
        guild_id=guild_id,
        defesa=dados["Def"],
        vida=dados["Vida"],
        habilidade=dados["Habilidade"],
        efeito=dados["Efeito"],
    )
    db.session.add(h)
    db.session.commit()
    return redirect(f"/admin/campaign/{Guild.query.get(guild_id).campaign_id}")


@admin_bp.route("/map/<int:map_id>/set_winner", methods=["POST"])
def set_map_winner(map_id):
    if session.get("role") != "admin":
        return "Acesso negado"

    m = Map.query.get_or_404(map_id)
    escolha = request.form.get("guilda_vencedora", "").strip()
    validas = [g.nome for g in m.campaign.guilds]

    if escolha and escolha not in validas:
        abort(400, description="Guilda inválida para esta campanha.")

    m.guilda_vencedora = escolha or None
    db.session.commit()
    return redirect(f"/admin/campaign/{m.campaign_id}")


# ------------------
# Rotas para Death Tokens & Curses
# ------------------
@admin_bp.route("/map/<int:map_id>")
def map_detail(map_id):
    if session.get("role") != "admin":
        return "Acesso negado"
    mapa = Map.query.get_or_404(map_id)
    return render_template("map_detail.html", mapa=mapa)


@admin_bp.route("/map/<int:map_id>/update_tokens", methods=["POST"])
def update_tokens(map_id):
    if session.get("role") != "admin":
        return "Acesso negado"

    mapa = Map.query.get_or_404(map_id)
    for g in mapa.campaign.guilds:
        for h in g.heroes:
            field_name = f"hero_{h.id}"
            if field_name in request.form:
                tokens = int(request.form[field_name])
                hm = HeroMap.query.filter_by(hero_id=h.id, map_id=mapa.id).first()
                if not hm:
                    hm = HeroMap(hero_id=h.id, map_id=mapa.id, death_tokens=tokens)
                    db.session.add(hm)
                else:
                    hm.death_tokens = tokens
    db.session.commit()
    return redirect(f"/admin/map/{map_id}")


@admin_bp.route("/map/<int:map_id>/apply_curses", methods=["POST"])
def apply_curses(map_id):
    if session.get("role") != "admin":
        return "Acesso negado"

    mapa = Map.query.get_or_404(map_id)
    hero_statuses = mapa.heroes_status
    sorted_heroes = sorted(hero_statuses, key=lambda hs: hs.death_tokens, reverse=True)

    curse_deck = deck_preparer()
    last_curse = None

    for idx, hs in enumerate(sorted_heroes):
        if idx == 0:
            curse = curse_applier(hs.death_tokens, curse_deck)
        else:
            if last_curse and last_curse in curse_deck:
                curse_deck.remove(last_curse)
            curse = curse_applier(hs.death_tokens, curse_deck)

        if curse:
            hs.curse_nome = curse["Nome"]
            hs.curse_valor = curse["Valor"]
            hs.curse_efeito = curse["Efeito"]

        last_curse = curse

    db.session.commit()
    return redirect(f"/admin/map/{map_id}")
