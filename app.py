import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Siniestros Viales CABA · Dashboard",
    page_icon="🚦", layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background-color:#0d1117!important;color:#e6edf3!important}
[data-testid="stAppViewBlockContainer"]{background-color:#0d1117!important;padding:1.5rem 2rem!important;max-width:1400px!important}
section[data-testid="stSidebar"]{background-color:#0d1117!important;border-right:1px solid #21262d!important}
section[data-testid="stSidebar"]>div{background-color:#0d1117!important}
*{font-family:'DM Sans',sans-serif!important}
section[data-testid="stSidebar"] *{color:#8b949e!important}
section[data-testid="stSidebar"] label{color:#58a6ff!important;font-size:.7rem!important;font-family:'DM Mono',monospace!important;letter-spacing:.12em!important;text-transform:uppercase!important}
[data-testid="stMultiSelect"] [data-baseweb="tag"]{background-color:#1f6feb22!important;border:1px solid #1f6feb!important;color:#58a6ff!important}
[data-baseweb="select"]>div{background-color:#161b22!important;border:1px solid #30363d!important;color:#e6edf3!important}
[data-baseweb="menu"]{background-color:#161b22!important;border:1px solid #30363d!important}
[data-testid="stTabs"] button{color:#8b949e!important;font-family:'DM Mono',monospace!important;font-size:.75rem!important;border-bottom:2px solid transparent!important}
[data-testid="stTabs"] button[aria-selected="true"]{color:#58a6ff!important;border-bottom:2px solid #58a6ff!important;background:transparent!important}
[data-testid="stTabs"] [data-baseweb="tab-list"]{background:transparent!important;border-bottom:1px solid #21262d!important}
[data-testid="stTabPanel"]{background:transparent!important}
hr{border-color:#21262d!important}
.hero-title{font-family:'Syne',sans-serif!important;font-size:2.6rem;font-weight:800;color:#e6edf3;letter-spacing:-.02em;line-height:1.1;margin:0}
.hero-subtitle{font-size:.95rem;color:#8b949e;margin-top:.5rem;font-weight:300;line-height:1.6;max-width:700px}
.hero-tag{display:inline-block;background:#1f6feb22;border:1px solid #1f6feb55;color:#58a6ff;font-family:'DM Mono',monospace!important;font-size:.68rem;letter-spacing:.1em;padding:3px 10px;border-radius:20px;margin-right:6px;margin-bottom:12px;text-transform:uppercase}
.kpi-card{background:#161b22;border:1px solid #21262d;border-radius:10px;padding:20px 22px;position:relative;overflow:hidden}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#58a6ff,#1f6feb)}
.kpi-card.red::before{background:linear-gradient(90deg,#f85149,#da3633)}
.kpi-card.orange::before{background:linear-gradient(90deg,#e3b341,#d29922)}
.kpi-card.green::before{background:linear-gradient(90deg,#3fb950,#238636)}
.kpi-label{font-family:'DM Mono',monospace!important;font-size:.65rem;letter-spacing:.14em;text-transform:uppercase;color:#8b949e;margin-bottom:10px}
.kpi-value{font-family:'Syne',sans-serif!important;font-size:2.4rem;font-weight:800;color:#e6edf3;line-height:1;margin-bottom:6px}
.kpi-value.red{color:#f85149}.kpi-value.orange{color:#e3b341}.kpi-value.green{color:#3fb950}
.kpi-detail{font-size:.78rem;color:#8b949e;line-height:1.4}.kpi-detail b{color:#c9d1d9}
.chart-card{background:#161b22;border:1px solid #21262d;border-radius:10px;padding:20px 20px 14px 20px}
.chart-title{font-family:'Syne',sans-serif!important;font-size:1rem;font-weight:700;color:#e6edf3;margin-bottom:2px}
.chart-subtitle{font-size:.78rem;color:#8b949e;margin-bottom:14px;line-height:1.4}
.insight-panel{background:#0d1117;border:1px solid #21262d;border-left:3px solid #58a6ff;border-radius:6px;padding:12px 16px;margin-top:12px}
.insight-panel.red{border-left-color:#f85149}.insight-panel.orange{border-left-color:#e3b341}.insight-panel.green{border-left-color:#3fb950}
.insight-header{font-family:'DM Mono',monospace!important;font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:#58a6ff;margin-bottom:5px}
.insight-header.red{color:#f85149}.insight-header.orange{color:#e3b341}.insight-header.green{color:#3fb950}
.insight-text{font-size:.82rem;color:#c9d1d9;line-height:1.55}.insight-text b{color:#e6edf3}
.section-header{display:flex;align-items:center;gap:10px;margin:28px 0 16px 0;padding-bottom:10px;border-bottom:1px solid #21262d}
.section-header-number{font-family:'DM Mono',monospace!important;font-size:.65rem;color:#58a6ff;letter-spacing:.1em;background:#1f6feb15;border:1px solid #1f6feb33;padding:2px 8px;border-radius:4px}
.section-header-title{font-family:'Syne',sans-serif!important;font-size:1.1rem;font-weight:700;color:#e6edf3}
.section-header-desc{font-size:.78rem;color:#8b949e;margin-left:auto}
</style>
""", unsafe_allow_html=True)

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#8b949e", size=11),
    margin=dict(t=10, b=10, l=0, r=0),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c9d1d9", size=10), orientation="h", yanchor="bottom", y=1.02),
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickfont=dict(color="#8b949e", size=10), zeroline=False),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickfont=dict(color="#8b949e", size=10), zeroline=False),
    hoverlabel=dict(bgcolor="#161b22", bordercolor="#30363d", font=dict(color="#e6edf3", size=11))
)
PALETA       = ["#58a6ff","#f85149","#3fb950","#e3b341","#d2a8ff","#79c0ff","#ffa657"]
COLORES_MODO = {"MOTO":"#f85149","PEATON":"#58a6ff","AUTO":"#e3b341","BICICLETA":"#3fb950"}
MODOS_TOP    = ["MOTO","PEATON","AUTO","BICICLETA"]

@st.cache_data
def load_data():
    df_raw   = pd.read_csv("siniestros_viales_victimas.csv", sep=None, engine="python")
    df_clean = df_raw.dropna(subset=["id_siniestro"]).copy()
    df       = df_clean[df_clean["GRAVEdad_victima"] == "MORTAL"].copy()
    df["fecha_dt"] = pd.to_datetime(df["fecha_siniestro"], errors="coerce")
    df["anio"]     = df["anio_siniestro"].astype(int)
    df["mes"]      = df["fecha_dt"].dt.month
    df["modo"]     = df["modo_desplazamiento_victima"].str.upper().str.strip()
    df["sexo"]     = df["sexo_victima"].str.upper().str.strip()
    df["rol"]      = df["rol_victima"].str.upper().str.strip()
    df["edad"]     = pd.to_numeric(df["edad_victima"], errors="coerce")
    return df

df_full = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style='padding:4px 0 20px 0;'>
        <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#e6edf3;'>🚦 FILTROS</div>
        <div style='font-size:.72rem;color:#484f58;margin-top:4px;font-family:DM Mono,monospace;letter-spacing:.06em;'>SINIESTROS VIALES FATALES · CABA</div>
    </div>""", unsafe_allow_html=True)
    anios    = sorted(df_full["anio"].unique())
    anio_sel = st.slider("Período", int(min(anios)), int(max(anios)), (int(min(anios)), int(max(anios))))
    modos_opts = sorted([m for m in df_full["modo"].unique()])
    modo_sel   = st.multiselect("Modo de desplazamiento", options=modos_opts, default=modos_opts)
    sexo_opts  = ["M","F"]
    sexo_sel   = st.multiselect("Sexo", options=sexo_opts, default=sexo_opts,
                                format_func=lambda x: "Masculino" if x=="M" else "Femenino")
    st.markdown("---")
    st.markdown("""<div style='font-size:.72rem;color:#484f58;line-height:1.7;font-family:DM Mono,monospace;'>
        FUENTE<br>Buenos Aires Data · OMSV<br>PERÍODO<br>2019 – 2024<br>REGISTROS<br>610 víctimas fatales<br>TOTAL DATASET<br>62.076 siniestros
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div style='font-size:.7rem;color:#30363d;line-height:1.6;'>
        Desarrollado por<br><span style='color:#58a6ff'>David Palacio Velásquez</span><br>Ciencias de Datos · UBA
    </div>""", unsafe_allow_html=True)

# ── FILTRO ────────────────────────────────────────────────────────────────────
df = df_full[
    (df_full["anio"] >= anio_sel[0]) & (df_full["anio"] <= anio_sel[1]) &
    (df_full["modo"].isin(modo_sel)) &
    (df_full["sexo"].isin(sexo_sel + ["SD"]))
].copy()

# ── HERO ──────────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3,1])
with col_h1:
    st.markdown("""<div style='margin-bottom:6px;'>
        <span class='hero-tag'>Buenos Aires · 2019–2024</span>
        <span class='hero-tag'>610 víctimas fatales</span>
        <span class='hero-tag'>Datos oficiales OMSV · GCBA</span>
    </div>
    <div class='hero-title'>Siniestros Viales Fatales<br>en la Ciudad de Buenos Aires</div>
    <div class='hero-subtitle'>
        Análisis de víctimas fatales en siniestros viales de CABA basado en datos oficiales del
        Observatorio de Movilidad y Seguridad Vial (OMSV). Las muertes en tránsito no son
        aleatorias — responden a patrones identificables e intervenibles con políticas concretas.
    </div>""", unsafe_allow_html=True)
with col_h2:
    prom = round(len(df_full) / (df_full["anio"].max() - df_full["anio"].min() + 1))
    st.markdown(f"""<div style='background:#161b22;border:1px solid #21262d;border-radius:10px;
                padding:18px;text-align:center;margin-top:12px;'>
        <div style='font-family:DM Mono,monospace;font-size:.6rem;color:#484f58;letter-spacing:.14em;text-transform:uppercase;margin-bottom:6px;'>promedio anual</div>
        <div style='font-family:Syne,sans-serif;font-size:2.8rem;font-weight:800;color:#f85149;line-height:1;'>{prom}</div>
        <div style='font-size:.78rem;color:#8b949e;margin-top:4px;'>muertes por año<br>en el período</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
total    = len(df)
df_s     = df[df["sexo"].isin(["M","F"])]
pct_masc = (df_s["sexo"]=="M").mean()*100 if len(df_s)>0 else 0
edad_med = df["edad"].median()
top_modo = df["modo"].value_counts()
top_nom  = top_modo.index[0] if len(top_modo)>0 else "—"
top_pct  = top_modo.iloc[0]/len(df)*100 if len(df)>0 else 0
años_span = max(anio_sel[1]-anio_sel[0]+1,1)

c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class='kpi-card red'><div class='kpi-label'>Víctimas fatales</div>
        <div class='kpi-value red'>{total:,}</div>
        <div class='kpi-detail'><b>~{total//años_span}</b> por año · casi <b>2 semanales</b></div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class='kpi-card orange'><div class='kpi-label'>Víctimas masculinas</div>
        <div class='kpi-value orange'>{pct_masc:.0f}%</div>
        <div class='kpi-detail'><b>3 de cada 4</b> víctimas son hombres</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class='kpi-card'><div class='kpi-label'>Edad mediana</div>
        <div class='kpi-value'>{edad_med:.0f} <span style='font-size:1.2rem;color:#8b949e'>años</span></div>
        <div class='kpi-detail'>Adultos en <b>edad productiva</b> · moto (31) ↔ peatón (57)</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class='kpi-card green'><div class='kpi-label'>Modo más vulnerable</div>
        <div class='kpi-value green' style='font-size:1.6rem;padding-top:4px'>{top_nom}</div>
        <div class='kpi-detail'><b>{top_pct:.0f}%</b> del total de víctimas fatales</div></div>""", unsafe_allow_html=True)

# ═══ SEC 1 — TENDENCIA ═══════════════════════════════════════════════════════
st.markdown("""<div class='section-header'>
    <span class='section-header-number'>01</span>
    <span class='section-header-title'>Evolución temporal</span>
    <span class='section-header-desc'>¿Cómo cambió la siniestralidad 2019–2024?</span>
</div>""", unsafe_allow_html=True)

col_a, col_b = st.columns([3,2])
with col_a:
    st.markdown("""<div class='chart-card'><div class='chart-title'>Víctimas fatales por año</div>
    <div class='chart-subtitle'>2024 marca el máximo post-pandemia — la tendencia es ascendente</div>""", unsafe_allow_html=True)
    por_anio = df.groupby("anio").size().reset_index(name="n")
    media_a  = por_anio["n"].mean()
    fig_evo  = go.Figure()
    fig_evo.add_trace(go.Scatter(
        x=por_anio["anio"], y=por_anio["n"], fill="tozeroy",
        fillcolor="rgba(248,81,73,0.08)", line=dict(color="#f85149",width=2.5),
        mode="lines+markers", marker=dict(size=9,color="#f85149",line=dict(color="#0d1117",width=2)),
        hovertemplate="<b>%{x}</b><br>%{y} víctimas fatales<extra></extra>"
    ))
    fig_evo.add_hline(y=media_a, line_dash="dot", line_color="#30363d", line_width=1.5,
                      annotation_text=f"  promedio: {media_a:.0f}", annotation_font_color="#484f58", annotation_font_size=10)
    fig_evo.add_vrect(x0=2019.7, x1=2020.9, fillcolor="rgba(63,185,80,0.07)", layer="below", line_width=0)
    fig_evo.add_annotation(x=2020.3, y=por_anio["n"].max()*0.92, text="ASPO<br>COVID-19",
                           showarrow=False, font=dict(size=9,color="#3fb950"))
    for _, row in por_anio.iterrows():
        c = "#3fb950" if row["n"]==por_anio["n"].min() else ("#f85149" if row["n"]==por_anio["n"].max() else "#484f58")
        fig_evo.add_annotation(x=row["anio"], y=row["n"], text=str(int(row["n"])),
                               showarrow=False, yshift=16, font=dict(size=10,color=c,family="DM Mono"))
    lay = {**PLOT_LAYOUT,"height":290}
    lay["xaxis"] = dict(**PLOT_LAYOUT["xaxis"],tickmode="linear",dtick=1)
    lay["yaxis"] = dict(**PLOT_LAYOUT["yaxis"],title="víctimas fatales")
    fig_evo.update_layout(**lay)
    st.plotly_chart(fig_evo, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""<div class='insight-panel red'><div class='insight-header red'>↓ Señal de alerta</div>
    <div class='insight-text'>El ASPO de 2020 redujo las víctimas un <b>22%</b> (104→81) — experimento natural que confirma que la siniestralidad es función directa del volumen de tránsito. La recuperación hacia <b>113 en 2024</b> (máximo del período) muestra que sin intervención estructural el sistema escala con el tránsito.</div></div>""", unsafe_allow_html=True)

with col_b:
    st.markdown("""<div class='chart-card'><div class='chart-title'>Composición por modo</div>
    <div class='chart-subtitle'>Participación relativa de cada modo — los peatones se acercan a las motos</div>""", unsafe_allow_html=True)
    df_ev  = df[df["modo"].isin(MODOS_TOP)]
    por_at = df_ev.groupby(["anio","modo"]).size().reset_index(name="n")
    por_at["pct"] = por_at["n"]/por_at.groupby("anio")["n"].transform("sum")*100
    fig_comp = px.bar(por_at, x="anio", y="pct", color="modo", barmode="stack",
                      color_discrete_map=COLORES_MODO,
                      labels={"pct":"%","anio":"Año","modo":""},
                      custom_data=["modo","n"])
    fig_comp.update_traces(hovertemplate="<b>%{customdata[0]}</b><br>%{y:.1f}% · %{customdata[1]} víctimas<extra></extra>")
    lay2 = {**PLOT_LAYOUT,"height":290}
    lay2["xaxis"] = dict(**PLOT_LAYOUT["xaxis"],tickmode="linear",dtick=1)
    lay2["yaxis"] = dict(**PLOT_LAYOUT["yaxis"],title="%",ticksuffix="%")
    fig_comp.update_layout(**lay2)
    st.plotly_chart(fig_comp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""<div class='insight-panel orange'><div class='insight-header orange'>↑ Tendencia preocupante</div>
    <div class='insight-text'>En 2024 los <b>peatones casi alcanzan a los motociclistas</b> en participación relativa. Los ciclistas muestran crecimiento sostenido desde 2022 — la expansión de ciclovías no fue suficiente para contener la siniestralidad.</div></div>""", unsafe_allow_html=True)

# ═══ SEC 2 — PERFIL ══════════════════════════════════════════════════════════
st.markdown("""<div class='section-header'>
    <span class='section-header-number'>02</span>
    <span class='section-header-title'>Perfil de la víctima</span>
    <span class='section-header-desc'>¿Quiénes mueren? Modo, sexo y edad</span>
</div>""", unsafe_allow_html=True)

col_c,col_d,col_e = st.columns([2,2,3])
with col_c:
    st.markdown("""<div class='chart-card'><div class='chart-title'>Por modo de desplazamiento</div>
    <div class='chart-subtitle'>Motos y peatones concentran el 81% de las víctimas fatales</div>""", unsafe_allow_html=True)
    vc = df["modo"].value_counts().reset_index()
    vc.columns = ["modo","n"]
    vc["pct"] = (vc["n"]/vc["n"].sum()*100).round(1)
    fig_vc = px.bar(vc.sort_values("n"), x="n", y="modo", orientation="h",
                    color="n", color_continuous_scale=["#21262d","#f85149"],
                    text=vc.sort_values("n")["pct"].apply(lambda x: f"{x}%"),
                    labels={"n":"","modo":""})
    fig_vc.update_traces(textposition="outside", textfont=dict(color="#8b949e",size=10,family="DM Mono"))
    fig_vc.update_coloraxes(showscale=False)
    lay3 = {**PLOT_LAYOUT,"height":280}
    lay3["xaxis"] = dict(**PLOT_LAYOUT["xaxis"],showgrid=False)
    fig_vc.update_layout(**lay3)
    st.plotly_chart(fig_vc, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_d:
    st.markdown("""<div class='chart-card'><div class='chart-title'>% masculino por modo</div>
    <div class='chart-subtitle'>El sesgo de género varía — desde 88% en motos hasta 58% en peatones</div>""", unsafe_allow_html=True)
    df_gs  = df[df["sexo"].isin(["M","F"])]
    conteo_modo = df["modo"].value_counts()
    modos_v = conteo_modo[conteo_modo >= 5].index
    pct_m  = (df_gs[df_gs["modo"].isin(modos_v)]
              .groupby("modo")["sexo"]
              .apply(lambda x: (x=="M").mean()*100)
              .reset_index())
    pct_m.columns = ["modo","pct_masc"]
    pct_m = pct_m.sort_values("pct_masc")
    avg_m = (df_gs["sexo"]=="M").mean()*100
    fig_gen = go.Figure()
    fig_gen.add_trace(go.Bar(
        y=pct_m["modo"], x=pct_m["pct_masc"], orientation="h",
        marker=dict(color=pct_m["pct_masc"],colorscale=[[0,"#21262d"],[1,"#e3b341"]],showscale=False),
        text=pct_m["pct_masc"].apply(lambda x: f"{x:.0f}%"), textposition="outside",
        textfont=dict(color="#8b949e",size=10,family="DM Mono"),
        hovertemplate="<b>%{y}</b><br>%{x:.1f}% masculino<extra></extra>"
    ))
    fig_gen.add_vline(x=avg_m, line_dash="dot", line_color="#484f58", line_width=1.2,
                      annotation_text=f"  prom. {avg_m:.1f}%", annotation_font_color="#484f58", annotation_font_size=9)
    lay4 = {**PLOT_LAYOUT,"height":280}
    lay4["xaxis"] = dict(**PLOT_LAYOUT["xaxis"],range=[0,110],ticksuffix="%",showgrid=False)
    fig_gen.update_layout(**lay4)
    st.plotly_chart(fig_gen, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_e:
    st.markdown("""<div class='chart-card'><div class='chart-title'>Distribución de edad por modo</div>
    <div class='chart-subtitle'>Brecha de 26 años entre motociclistas (mediana 31) y peatones (mediana 57)</div>""", unsafe_allow_html=True)
    df_box = df[df["modo"].isin(MODOS_TOP)].dropna(subset=["edad"])
    orden_b = df_box.groupby("modo")["edad"].median().sort_values().index.tolist()
    fig_box = go.Figure()
    for modo in orden_b:
        sub = df_box[df_box["modo"]==modo]["edad"]
        fig_box.add_trace(go.Box(
            x=sub, name=modo, orientation="h",
            marker_color=COLORES_MODO.get(modo,"#8b949e"),
            line_color=COLORES_MODO.get(modo,"#8b949e"),
            fillcolor=COLORES_MODO.get(modo,"#8b949e")+"26",
            boxmean=True, jitter=0.3, marker=dict(size=3,opacity=0.35),
            hovertemplate=f"<b>{modo}</b><br>mediana: %{{median:.0f}} años<extra></extra>"
        ))
    lay5 = {**PLOT_LAYOUT,"height":280,"showlegend":False}
    lay5["xaxis"] = dict(**PLOT_LAYOUT["xaxis"],title="Edad (años)")
    fig_box.update_layout(**lay5)
    st.plotly_chart(fig_box, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""<div class='insight-panel'><div class='insight-header'>↓ Dos crisis distintas bajo el mismo número</div>
<div class='insight-text'>
<b>Motociclistas:</b> el 54% tiene menos de 35 años, 88% masculinos — en gran parte trabajadores del delivery, herramienta de trabajo masiva sin marco regulatorio adecuado.<br>
<b>Peatones:</b> el 38% tiene 60+ años — adultos mayores cruzando vías diseñadas para cuerpos más jóvenes. Son la misma cantidad de víctimas pero requieren intervenciones radicalmente distintas.
</div></div>""", unsafe_allow_html=True)

# ═══ SEC 3 — ESTACIONALIDAD + TABLA RESUMEN ══════════════════════════════════
st.markdown("""<div class='section-header'>
    <span class='section-header-number'>03</span>
    <span class='section-header-title'>Estacionalidad y tabla resumen</span>
    <span class='section-header-desc'>Distribución mensual y perfil comparado por modo</span>
</div>""", unsafe_allow_html=True)

col_f, col_g = st.columns([2,3])
with col_f:
    st.markdown("""<div class='chart-card'><div class='chart-title'>Distribución mensual</div>
    <div class='chart-subtitle'>Las muertes viales ocurren todo el año — sin estacionalidad fuerte</div>""", unsafe_allow_html=True)
    por_mes = df.groupby("mes").size().reset_index(name="n")
    meses   = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    por_mes["mes_label"] = por_mes["mes"].apply(lambda x: meses[x-1])
    fig_mes = px.bar(por_mes, x="mes_label", y="n",
                     color="n", color_continuous_scale=["#21262d","#58a6ff"],
                     text="n", labels={"mes_label":"","n":"Víctimas"})
    fig_mes.update_traces(textposition="outside", textfont=dict(size=9,color="#8b949e",family="DM Mono"))
    fig_mes.update_coloraxes(showscale=False)
    fig_mes.add_hline(y=por_mes["n"].mean(), line_dash="dot", line_color="#484f58", line_width=1.2)
    lay6 = {**PLOT_LAYOUT,"height":280}
    fig_mes.update_layout(**lay6)
    st.plotly_chart(fig_mes, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""<div class='insight-panel'><div class='insight-header'>↓ Sin estacionalidad marcada</div>
    <div class='insight-text'>A diferencia de otros países, CABA no muestra una caída invernal fuerte. Las muertes viales son un fenómeno continuo — lo que cambia es el <b>perfil del siniestro</b>, no su frecuencia.</div></div>""", unsafe_allow_html=True)

with col_g:
    st.markdown("""<div class='chart-card'><div class='chart-title'>Tabla resumen por modo</div>
    <div class='chart-subtitle'>Perfil integrado — n, participación, género y edad para los 4 modos principales</div>""", unsafe_allow_html=True)
    resumen = []
    for modo in MODOS_TOP:
        sub   = df[df["modo"]==modo]
        sub_s = sub[sub["sexo"].isin(["M","F"])]
        sub_e = sub["edad"].dropna()
        resumen.append({
            "Modo":         modo,
            "Víctimas":     len(sub),
            "% del total":  f"{len(sub)/max(len(df),1)*100:.1f}%",
            "% masculino":  f"{(sub_s['sexo']=='M').mean()*100:.0f}%" if len(sub_s)>0 else "—",
            "Edad media":   f"{sub_e.mean():.0f}" if len(sub_e)>0 else "—",
            "Edad mediana": f"{sub_e.median():.0f}" if len(sub_e)>0 else "—",
            "% < 35 años":  f"{(sub_e<35).mean()*100:.0f}%" if len(sub_e)>0 else "—",
            "% ≥ 60 años":  f"{(sub_e>=60).mean()*100:.0f}%" if len(sub_e)>0 else "—",
        })
    df_res = pd.DataFrame(resumen)
    st.dataframe(
        df_res.style
        .set_properties(**{"background-color":"#0d1117","color":"#c9d1d9","border-color":"#21262d","font-size":"13px"})
        .set_table_styles([
            {"selector":"th","props":[("background-color","#161b22"),("color","#58a6ff"),
                                      ("font-family","DM Mono, monospace"),("font-size","11px"),
                                      ("text-transform","uppercase"),("letter-spacing","0.08em")]},
            {"selector":"tr:hover","props":[("background-color","#161b22")]},
        ]),
        use_container_width=True, hide_index=True, height=220
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""<div class='insight-panel orange'><div class='insight-header orange'>↓ La tabla en una lectura</div>
    <div class='insight-text'>La bipolaridad es clara: <b>MOTO</b> (joven, masculino, 54% menor de 35) vs <b>PEATON</b> (mayor, más equilibrado, 38% de 60+). Son el mismo volumen de víctimas con perfiles opuestos — cada uno requiere su propia política.</div></div>""", unsafe_allow_html=True)

# ═══ SEC 4 — RECOMENDACIONES ══════════════════════════════════════════════════
st.markdown("""<div class='section-header'>
    <span class='section-header-number'>04</span>
    <span class='section-header-title'>Implicaciones y recomendaciones</span>
    <span class='section-header-desc'>¿Qué deberían hacer los tomadores de decisión?</span>
</div>""", unsafe_allow_html=True)

recs = [
    ("🏍️","#f85149","Motociclistas & Delivery","Regulación laboral urgente",
     "Seguro obligatorio para riders, límite de horas de trabajo, capacitación vial certificada. El 54% de las víctimas en moto tiene menos de 35 años — en gran parte trabajadores del delivery sin protección legal.",
     ["42% de víctimas","88% masculinos","Mediana 31 años","Crecimiento sostenido"]),
    ("🚶","#58a6ff","Peatones Adultos Mayores","Infraestructura adaptada",
     "Ciclos semafóricos más largos en avenidas con alto flujo peatonal. Un adulto mayor necesita 6–8 segundos para cruzar — la mayoría de los semáforos no lo permiten. El 38% de los peatones fallecidos tiene 60+ años.",
     ["39% de víctimas","Mediana 57 años","38% tiene 60+ años","Casi igual a motos"]),
    ("🚲","#3fb950","Ciclistas","Red segregada completa",
     "La expansión de ciclovías no contuvo la siniestralidad ciclista. Se necesita infraestructura segregada real — no pintura en el suelo — en los corredores de mayor siniestralidad.",
     ["42 víctimas 2019–24","Tendencia creciente","76% masculinos","Mediana 47 años"])
]
rec1,rec2,rec3 = st.columns(3)
for col_r,(icon,color,titulo,subtitulo,texto,tags) in zip([rec1,rec2,rec3],recs):
    with col_r:
        tags_html = "".join([
            f"<span style='display:inline-block;background:{color}18;border:1px solid {color}44;"
            f"color:{color};font-family:DM Mono,monospace;font-size:.62rem;"
            f"padding:2px 8px;border-radius:12px;margin:2px 3px 2px 0'>{t}</span>"
            for t in tags
        ])
        st.markdown(f"""<div style='background:#161b22;border:1px solid {color}33;
                    border-top:3px solid {color};border-radius:10px;padding:20px;'>
            <div style='font-size:1.8rem;margin-bottom:10px'>{icon}</div>
            <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;color:#e6edf3;margin-bottom:2px'>{titulo}</div>
            <div style='font-family:DM Mono,monospace;font-size:.65rem;color:{color};letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px'>{subtitulo}</div>
            <div style='font-size:.82rem;color:#8b949e;line-height:1.6;margin-bottom:14px'>{texto}</div>
            <div>{tags_html}</div>
        </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
st.markdown("""<div style='border-top:1px solid #21262d;padding-top:20px;margin-top:8px;
            display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;'>
    <div style='font-family:DM Mono,monospace;font-size:.7rem;color:#30363d;'>SINIESTROS VIALES CABA · DATOS OFICIALES OMSV · 2019–2024</div>
    <div style='font-size:.78rem;color:#484f58;'>
        Desarrollado por <a href='https://www.linkedin.com/in/davidpalacio-velasquez-3864b6298' target='_blank' style='color:#58a6ff;text-decoration:none;'>David Palacio Velásquez</a>
        · Ciencias de Datos, UBA ·
        <a href='https://github.com/davidpalacio1/TP-3-Siniestros' target='_blank' style='color:#58a6ff;text-decoration:none;'>Ver análisis completo →</a>
    </div>
    <div style='font-family:DM Mono,monospace;font-size:.65rem;color:#30363d;'>FUENTE: BUENOS AIRES DATA · GCBA · CC ATTRIBUTION</div>
</div>""", unsafe_allow_html=True)
