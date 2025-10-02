from flask import Blueprint, render_template, session
from models import Campaign, Map

player_bp = Blueprint("player", __name__, url_prefix="/player")


@player_bp.route("/")
def dashboard():
    if session.get("role") != "player":
        return "Acesso negado"
    campaigns = Campaign.query.all()
    return render_template("player_dashboard.html", campaigns=campaigns)


@player_bp.route("/campaign/<int:campaign_id>")
def campaign_detail(campaign_id):
    if session.get("role") != "player":
        return "Acesso negado"
    c = Campaign.query.get_or_404(campaign_id)
    return render_template("player_campaign_detail.html", campaign=c)


@player_bp.route("/map/<int:map_id>")
def map_detail(map_id):
    if session.get("role") != "player":
        return "Acesso negado"
    mapa = Map.query.get_or_404(map_id)
    return render_template("player_map_detail.html", mapa=mapa)


@player_bp.route("/campaign/<int:campaign_id>/timeline")
def campaign_timeline(campaign_id):
    if session.get("role") != "player":
        return "Acesso negado"
    c = Campaign.query.get_or_404(campaign_id)
    # Ordenar mapas pelo ID (ou nome, se preferir)
    maps = sorted(c.maps, key=lambda m: m.id)
    return render_template("player_campaign_timeline.html", campaign=c, maps=maps)
