  from __future__ import annotations
import streamlit as st
from lib.data import load_data
from lib.ui import set_base, hero, filter_bar, project_card, detail_view, footer

set_base("Lance Locker • Portfolio")

data = load_data()
profile = data.get("profile", {})
projects = list(data.get("projects", []))

# HERO
hero(profile)

# Router: use query param p=slug if available, otherwise gallery
slug = None
try:
    # stlite generally supports Streamlit's query params; fall back gracefully if not
    qd = st.query_params if hasattr(st, "query_params") else {}
    slug = qd.get("p") if isinstance(qd, dict) else None
except Exception:
    slug = None

by_id = {p["id"]: p for p in projects if "id" in p}

if isinstance(slug, str) and slug in by_id:
    detail_view(by_id[slug])
else:
    # FILTER / SEARCH
    all_tags = sorted({t for p in projects for t in p.get("tags", [])})
    active = [t for t in all_tags if st.session_state.get(f"tag_{t.replace(' ','_')}", False)]
    chosen = filter_bar(all_tags, active)
    q = (st.session_state.get("q","") or "").strip().lower()
    sort = st.session_state.get("sort","Featured")

    def include(p):
        if chosen and not set(chosen).issubset(set(p.get("tags", []))): return False
        if q:
            blob = " ".join([
                p.get("title",""), p.get("tagline",""), p.get("summary",""),
                " ".join(p.get("tags", [])),
                " ".join([a for row in p.get("facts", []) for a in row])
            ]).lower()
            if q not in blob: return False
        return True

    view = [p for p in projects if include(p)]
    if sort == "Title A→Z":
        view = sorted(view, key=lambda x: (x.get("title","").lower(), x.get("id","")))

    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown("### Featured Projects")
    cols = st.columns(3)
    for i, proj in enumerate(view):
        with cols[i % 3]:
            project_card(proj)
    st.markdown("</div>", unsafe_allow_html=True)

footer()
