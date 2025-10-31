from __future__ import annotations
from typing import Dict, List
import streamlit as st

def set_base(title="Lance Locker"):
    st.set_page_config(page_title=title, page_icon="🧰", layout="wide")
    st.markdown("""
    <style>
      #MainMenu, header, footer {visibility:hidden}
      .stApp {font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial}
      body {background:#070a12; color:#e6e8ec}
      .container {max-width:1200px; margin:0 auto; padding:0 12px}
      .kicker {display:inline-block;padding:.4rem .7rem;border:1px solid rgba(255,255,255,.12);
               border-radius:9999px;background:rgba(255,255,255,.06); color:#aab1bb; font-size:.85rem}
      .title-xxl {font-family:Outfit, Inter; font-size:54px; line-height:1.02; margin:10px 0;
                  background: linear-gradient(90deg,#e8edf6 0,#c4e6ff 35%,#a0b8ff 70%,#e8edf6 100%);
                  -webkit-background-clip:text; background-clip:text; color:transparent}
      .subtitle {color:#9fb0c4; font-size:1.06rem}
      .chip {display:inline-block; padding:.45rem .75rem; border-radius:9999px;
             border:1px solid rgba(255,255,255,.12); background:rgba(255,255,255,.06);
             margin:8px 8px 0 0; font-size:.92rem}
      .btn {display:inline-flex; align-items:center; gap:.5rem; padding:.7rem 1rem; border-radius:14px; text-decoration:none; color:inherit;
            border:1px solid rgba(255,255,255,.14); background:rgba(255,255,255,.06);
            transition: transform .18s ease, background .18s ease; margin:12px 12px 0 0;}
      .btn:hover {transform:translateY(-2px); background:rgba(255,255,255,.12)}

      .filters {display:flex; flex-wrap:wrap; gap:.6rem; align-items:center; margin: 10px 0 6px}
      .tag {padding:.45rem .7rem; border-radius:9999px; cursor:pointer;
            border:1px solid rgba(255,255,255,.14); background:rgba(255,255,255,.05); color:#c8d0db; font-size:.9rem}
      .tag.active {background:rgba(125,211,252,.18); color:#eaf6ff; border-color: rgba(125,211,252,.45)}

      .card {position:relative; background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.10);
             border-radius:18px; padding:12px; overflow:hidden; transition: border-color .18s ease, transform .18s ease}
      .card:hover {border-color: rgba(255,255,255,.18); transform: translateY(-4px)}
      .thumb {height:230px;width:100%;border-radius:12px;overflow:hidden;background:#0a0f1a}
      .soft {color:#aab1bb}
      .badge {display:inline-block; font-size:.8rem; padding:.3rem .6rem; border-radius:10px;
              background:rgba(125,211,252,.14); border:1px solid rgba(125,211,252,.35); margin-right:6px}

      .viewer {height:520px; width:100%; border-radius:18px; overflow:hidden; background:#0a0f1a; border:1px solid rgba(255,255,255,.10)}
      .section-title {font-family:Outfit, Inter; letter-spacing:.3px}
      .divider {height:1px; background:linear-gradient(90deg, transparent, rgba(255,255,255,.18), transparent); margin:18px 0}
      .footer {opacity:.75; font-size:.9rem; text-align:center; padding:36px 0}
    </style>
    """, unsafe_allow_html=True)

def hero(profile: Dict):
    name = profile.get("name","Lance")
    tagline = profile.get("tagline","Manufacturing & Mechanical Engineering Portfolio")
    chips = profile.get("chips", [])
    links = profile.get("links", [])
    st.markdown('<div class="container" style="padding:64px 0 20px">', unsafe_allow_html=True)
    st.markdown('<span class="kicker">Lance Locker</span>', unsafe_allow_html=True)
    st.markdown(f"<div class='title-xxl'>Hi, I’m {name} 👋</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>{tagline}</div>", unsafe_allow_html=True)
    if chips:
        st.markdown("".join([f"<span class='chip'>{c}</span>" for c in chips]), unsafe_allow_html=True)
    if links:
        st.markdown("<div style='margin-top:4px'>" + "".join(
            [f"<a class='btn' href='{l['url']}' target='_blank'>↗ {l['label']}</a>" for l in links]
        ) + "</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def resolve_model_src(model_path: str, slug: str) -> str:
    """
    We serve static files directly from GitHub Pages.
    - If 'model' is an absolute URL, use it as-is.
    - Else, prefer given relative path; otherwise fall back to your_projects/<slug>.glb
    """
    if isinstance(model_path, str) and (model_path.startswith("http://") or model_path.startswith("https://")):
        return model_path
    return model_path or f"your_projects/{slug}.glb"

def model_viewer(src: str, height=240, zoom=True):
    zoom_attr = "" if zoom else "disable-zoom"
    html = f"""
      <model-viewer src="{src}" camera-controls {zoom_attr} autoplay auto-rotate
        shadow-intensity="1" exposure="1" style="width:100%;height:{height}px;background:#0a0f1a;border-radius:12px;">
      </model-viewer>
    """
    st.components.v1.html(html, height=height+4, scrolling=False)

def filter_bar(all_tags: List[str], active: List[str]) -> List[str]:
    st.markdown('<div class="container">', unsafe_allow_html=True)
    cols = st.columns([2,5,3])
    with cols[0]:
        q = st.text_input("Search", value=st.session_state.get("q",""), placeholder="Search projects, tags, docs…")
        st.session_state["q"] = q
    with cols[1]:
        st.markdown('<div class="filters">', unsafe_allow_html=True)
        sel = set(active)
        for t in all_tags:
            if st.checkbox(t, value=(t in sel), key=f"tag_{t.replace(' ','_')}"):
                sel.add(t)
            else:
                sel.discard(t)
        st.markdown('</div>', unsafe_allow_html=True)
    with cols[2]:
        sort = st.selectbox("Sort by", ["Featured", "Title A→Z"], index=0)
        st.session_state["sort"] = sort
    st.markdown('</div>', unsafe_allow_html=True)
    return sorted(sel)

def project_card(p: Dict):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        src = resolve_model_src(p.get("model",""), p["id"])
        model_viewer(src, height=210, zoom=False)
        st.markdown(f"**{p['title']}**")
        if p.get("tagline"): st.markdown(f"<div class='soft'>{p['tagline']}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1,1])
        with c1:
            if st.button("View project →", key=f"open_{p['id']}", use_container_width=True):
                # Deep-link if query_params supported; otherwise use session_state
                try:
                    st.query_params["p"] = p["id"]  # type: ignore[attr-defined]
                except Exception:
                    st.session_state["__route__"] = p["id"]
        with c2:
            if p.get("tags"):
                st.markdown("<div style='text-align:right'>"+"".join([f"<span class='badge'>{t}</span>" for t in p["tags"][:3]])+"</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def _img(url: str):
    # Use HTML <img> so the browser fetches directly from GitHub Pages (no Python FS needed)
    st.markdown(f"<img src='{url}' style='width:100%;border-radius:12px;border:1px solid rgba(255,255,255,.10);'/>", unsafe_allow_html=True)

def detail_view(p: Dict):
    st.markdown('<div class="container">', unsafe_allow_html=True)
    back = st.columns([1,9])[0]
    with back:
        if st.button("← Back", use_container_width=True):
            try:
                st.query_params.clear()  # type: ignore[attr-defined]
            except Exception:
                st.session_state["__route__"] = None

    st.markdown(f"### {p['title']}")
    if p.get("tagline"): st.caption(p["tagline"])

    left, right = st.columns([2,1], gap="large")
    with left:
        st.markdown('<div class="viewer">', unsafe_allow_html=True)
        src = resolve_model_src(p.get("model",""), p["id"])
        model_viewer(src, height=520, zoom=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown("#### Details")
        for k, v in p.get("facts", []):
            st.markdown(f"**{k}**  \n<span class='soft'>{v}</span>", unsafe_allow_html=True)
        if p.get("tags"):
            st.markdown("<div style='margin:6px 0 12px 0'>"+"".join([f"<span class='badge'>{t}</span>" for t in p["tags"]])+"</div>", unsafe_allow_html=True)
        if p.get("links"):
            st.markdown("#### Docs")
            for link in p["links"]:
                st.markdown(f"- [{link['label']}]({link['url']})")

    st.markdown("#### Summary")
    st.write(p.get("summary","—"))

    imgs = p.get("images", [])
    if imgs:
        st.markdown("#### Visuals")
        cols = st.columns(min(3, max(1, len(imgs))))
        for i, rel in enumerate(imgs):
            url = rel if rel.startswith("http") else f"{rel}"
            with cols[i % len(cols)]:
                _img(url)
    st.markdown("</div>", unsafe_allow_html=True)

def footer():
    st.markdown('<div class="container"><div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
      <div class="footer">
        <img src="assets/logo.svg" alt="logo" style="height:18px;vertical-align:middle;opacity:.8;margin-right:6px"/>
        Built with <strong>Streamlit</strong> on <strong>stlite</strong>, hosted on <strong>GitHub Pages</strong>.
      </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
