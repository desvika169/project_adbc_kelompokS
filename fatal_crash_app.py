import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================
# KONFIGURASI HALAMAN
# =========================================

st.set_page_config(
    page_title="Fatal Crash Analysis USA 2015",
    page_icon="⚠️",
    layout="wide"
)

# =========================================
# CUSTOM CSS — EARTH TONE / WARM
# =========================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background-color: #f5f0e8;
        color: #3d2b1f;
    }
    section[data-testid="stSidebar"] {
        background-color: #ede5d8 !important;
        border-right: 1px solid #c8b89a;
    }
    section[data-testid="stSidebar"] * {
        color: #4a3728 !important;
    }

    /* ─── Hero Banner ─── */
    .hero-banner {
        background: linear-gradient(135deg, #3d2b1f 0%, #6b3a20 40%, #8b5e3c 100%);
        border: 1px solid #a0724a;
        border-left: 5px solid #c8963c;
        border-radius: 8px;
        padding: 2.2rem 2.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '⚠';
        font-size: 12rem;
        position: absolute;
        right: -1rem;
        top: -2rem;
        opacity: 0.06;
        color: #f5d080;
        font-family: sans-serif;
    }
    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 3.2rem;
        letter-spacing: 3px;
        color: #f5f0e8;
        margin: 0 0 4px;
        line-height: 1;
    }
    .hero-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #c8963c;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .hero-desc {
        color: #d4c0a8;
        font-size: 0.92rem;
        font-weight: 300;
    }

    /* ─── Section Label ─── */
    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #8b5e3c;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #c8b89a, transparent);
    }

    /* ─── Metric Cards ─── */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #ede5d8;
        border: 1px solid #c8b89a;
        border-top: 3px solid #a0522d;
        border-radius: 8px;
        padding: 18px 20px;
    }
    .metric-card.yellow { border-top-color: #c8963c; }
    .metric-card.orange { border-top-color: #b06030; }
    .metric-card.dim    { border-top-color: #9a8878; }
    .metric-value {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.6rem;
        color: #3d2b1f;
        letter-spacing: 1px;
        line-height: 1;
        margin: 6px 0 4px;
    }
    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #7a6650;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ─── Insight Cards ─── */
    .insight-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
    }
    .insight-item {
        background: #ede5d8;
        border: 1px solid #c8b89a;
        border-left: 3px solid #a0522d;
        padding: 14px 16px;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
        color: #4a3728;
        line-height: 1.5;
    }
    .insight-item b { color: #8b3a1a; }
    .insight-item:nth-child(even) { border-left-color: #c8963c; }
    .insight-item:nth-child(even) b { color: #8b6820; }

    /* ─── Divider ─── */
    .divider { border: none; border-top: 1px solid #c8b89a; margin: 1.5rem 0 1rem; }

    /* ─── Sidebar filter tags ─── */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #d4c0a8 !important;
        border: 1px solid #a0724a !important;
        color: #3d2b1f !important;
    }
    .stCaption { color: #7a6650 !important; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; }

    /* ─── Tab styling ─── */
    .stTabs [data-baseweb="tab-list"] { background-color: #ede5d8; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] { color: #7a6650 !important; }
    .stTabs [aria-selected="true"] { color: #8b5e3c !important; border-bottom: 2px solid #8b5e3c !important; }

    /* ─── Button ─── */
    .stButton>button { background:#8b5e3c; color:#f5f0e8; border:none; border-radius:8px; font-weight:600; }
    .stButton>button:hover { background:#6b4428; }

    /* ─── Footer ─── */
    .footer-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #9a8878;
        text-align: center;
        letter-spacing: 1px;
        padding: 1rem 0;
        border-top: 1px solid #c8b89a;
    }

    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =========================================
# PLOTLY EARTH TONE TEMPLATE
# =========================================

PLOTLY_LAYOUT = dict(
    plot_bgcolor='#ede5d8',
    paper_bgcolor='#ede5d8',
    font_color='#4a3728',
    font_family='DM Sans',
    title_font_color='#3d2b1f',
    title_font_size=14,
    title_font_family='DM Sans',
    legend=dict(bgcolor='rgba(0,0,0,0)', font_color='#4a3728'),
    xaxis=dict(gridcolor='#c8b89a', zerolinecolor='#c8b89a', tickfont_color='#7a6650'),
    yaxis=dict(gridcolor='#c8b89a', zerolinecolor='#c8b89a', tickfont_color='#7a6650'),
    margin=dict(l=10, r=10, t=40, b=10),
)

# Palette earth tone
PALETTE_MAIN = ['#a0522d','#c8963c','#6b8f71','#8b7355','#c8b89a','#d4a060','#6b5a30']
PALETTE_SEQ  = ['#f5f0e8','#e8d8c0','#d4b898','#c09060','#a06840','#804820','#5a2810']

# =========================================
# LOAD DATA
# =========================================

@st.cache_data
def load_data():
    df = pd.read_csv("df_clean.csv")
    return df.copy()

_df = load_data()

# =========================================
# PREPROCESSING
# =========================================

hari_mapping  = {1:'Minggu', 2:'Senin', 3:'Selasa', 4:'Rabu',
                 5:'Kamis',  6:'Jumat', 7:'Sabtu'}
bulan_mapping = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'Mei', 6:'Jun',
                 7:'Jul', 8:'Agu', 9:'Sep', 10:'Okt', 11:'Nov', 12:'Des'}

if 'day_of_week'    in _df.columns: _df['nama_hari']  = _df['day_of_week'].map(hari_mapping)
if 'month_of_crash' in _df.columns: _df['nama_bulan'] = _df['month_of_crash'].map(bulan_mapping)

def kategori_waktu(jam):
    if   0  <= jam < 6:  return 'Dini Hari'
    elif 6  <= jam < 12: return 'Pagi'
    elif 12 <= jam < 18: return 'Siang'
    else:                return 'Malam'

def tipe_hari(hari):
    return 'Akhir Pekan' if hari in ['Sabtu', 'Minggu'] else 'Hari Kerja'

if 'hour_of_crash' in _df.columns: _df['kategori_waktu'] = _df['hour_of_crash'].apply(kategori_waktu)
if 'nama_hari'     in _df.columns: _df['tipe_hari']      = _df['nama_hari'].apply(tipe_hari)

URUTAN_HARI  = ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu']
URUTAN_BULAN = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des']

# =========================================
# SIDEBAR FILTER
# =========================================

with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px;'>
        <div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;letter-spacing:3px;color:#8b5e3c;'>FILTER</div>
        <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#9a8878;letter-spacing:2px;'>DASHBOARD CONTROLS</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if 'state_name' in _df.columns:
        all_states = sorted(_df['state_name'].dropna().unique())
        selected_state = st.multiselect("Pilih State", options=all_states, default=all_states)
        _df = _df[_df['state_name'].isin(selected_state)]

    if 'kategori_waktu' in _df.columns:
        selected_waktu = st.multiselect(
            "Pilih Kategori Waktu",
            options=['Dini Hari','Pagi','Siang','Malam'],
            default=['Dini Hari','Pagi','Siang','Malam']
        )
        _df = _df[_df['kategori_waktu'].isin(selected_waktu)]

    if 'nama_hari' in _df.columns:
        selected_hari = st.multiselect("Pilih Hari", options=URUTAN_HARI, default=URUTAN_HARI)
        _df = _df[_df['nama_hari'].isin(selected_hari)]

    st.markdown("---")
    st.caption(f"DATA TERSARING: {len(_df):,} BARIS")

# =========================================
# HERO BANNER
# =========================================

st.markdown("""
<div class="hero-banner">
    <div class="hero-sub">⚠ NHTSA · TRAFFIC FATALITIES · 2015</div>
    <div class="hero-title">ANALISIS POLA KECELAKAAN FATAL</div>
    <div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;letter-spacing:6px;color:#c8963c;margin-bottom:10px;'>AMERIKA SERIKAT</div>
    <div class="hero-desc">Exploratory Data Analysis berdasarkan faktor waktu &amp; geografis menggunakan data NHTSA</div>
</div>
""", unsafe_allow_html=True)

# =========================================
# METRIC CARDS
# =========================================

val_kecelakaan = f"{len(_df):,}"
val_state      = str(_df['state_name'].nunique()) if 'state_name' in _df.columns else "-"
val_fatalitas  = f"{int(_df['number_of_fatalities'].sum()):,}" if 'number_of_fatalities' in _df.columns else "-"
val_drunk      = f"{int(_df['number_of_drunk_drivers'].sum()):,}" if 'number_of_drunk_drivers' in _df.columns else "-"

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Total Kecelakaan</div>
        <div class="metric-value">{val_kecelakaan}</div>
    </div>
    <div class="metric-card dim">
        <div class="metric-label">Jumlah State</div>
        <div class="metric-value">{val_state}</div>
    </div>
    <div class="metric-card orange">
        <div class="metric-label">Total Fatalitas</div>
        <div class="metric-value">{val_fatalitas}</div>
    </div>
    <div class="metric-card yellow">
        <div class="metric-label">Total Drunk Driver</div>
        <div class="metric-value">{val_drunk}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================
# ANALISIS WAKTU
# =========================================

st.markdown('<div class="section-label">▌ ANALISIS WAKTU</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    per_waktu = _df['kategori_waktu'].value_counts().reset_index()
    per_waktu.columns = ['Kategori Waktu', 'Jumlah']
    order = ['Dini Hari','Pagi','Siang','Malam']
    per_waktu['Kategori Waktu'] = pd.Categorical(per_waktu['Kategori Waktu'], categories=order, ordered=True)
    per_waktu = per_waktu.sort_values('Kategori Waktu')

    fig = px.bar(
        per_waktu, x='Kategori Waktu', y='Jumlah',
        color='Kategori Waktu',
        color_discrete_sequence=['#9a8878','#c8963c','#d4a060','#a0522d'],
        text_auto=True,
        title='Distribusi per Kategori Waktu'
    )
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig.update_traces(textposition='outside', textfont_color='#4a3728')
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    per_tipe = _df['tipe_hari'].value_counts().reset_index()
    per_tipe.columns = ['Tipe', 'Jumlah']

    fig2 = px.pie(
        per_tipe, names='Tipe', values='Jumlah',
        color_discrete_sequence=['#a0522d','#c8b89a'],
        hole=0.52,
        title='Hari Kerja vs Akhir Pekan'
    )
    fig2.update_layout(**PLOTLY_LAYOUT)
    fig2.update_traces(textinfo='percent+label', pull=[0.04, 0.04],
                       textfont_color='#3d2b1f')
    st.plotly_chart(fig2, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    per_jam = _df['hour_of_crash'].value_counts().sort_index().reset_index()
    per_jam.columns = ['Jam', 'Jumlah']
    if len(per_jam) > 0:
        peak_jam = per_jam.loc[per_jam['Jumlah'].idxmax(), 'Jam']
        per_jam['warna'] = per_jam['Jam'].apply(lambda x: 'Puncak' if x == peak_jam else 'Normal')
        fig3 = px.bar(
            per_jam, x='Jam', y='Jumlah', color='warna',
            color_discrete_map={'Puncak':'#a0522d','Normal':'#c8b89a'},
            title=f'Kecelakaan per Jam — Puncak: {int(peak_jam):02d}:00'
        )
        fig3.update_layout(**PLOTLY_LAYOUT, showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

with col_d:
    per_hari = _df['nama_hari'].value_counts().reindex(URUTAN_HARI).reset_index()
    per_hari.columns = ['Hari', 'Jumlah']

    fig4 = px.bar(
        per_hari, x='Hari', y='Jumlah',
        color='Jumlah',
        color_continuous_scale=PALETTE_SEQ,
        text_auto=True,
        title='Distribusi per Hari'
    )
    fig4.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
    fig4.update_traces(textposition='outside', textfont_color='#4a3728')
    st.plotly_chart(fig4, use_container_width=True)

# =========================================
# BULAN & HEATMAP
# =========================================

col_e, col_f = st.columns(2)

with col_e:
    per_bulan = _df['nama_bulan'].value_counts().reindex(URUTAN_BULAN).reset_index()
    per_bulan.columns = ['Bulan', 'Jumlah']

    fig5 = px.line(
        per_bulan, x='Bulan', y='Jumlah', markers=True,
        title='Tren Kecelakaan per Bulan',
        color_discrete_sequence=['#a0522d']
    )
    fig5.update_traces(line_width=2.5, marker_size=8,
                       marker_color='#c8963c', marker_line_color='#a0522d',
                       marker_line_width=2, fill='tozeroy',
                       fillcolor='rgba(160,82,45,0.10)')
    fig5.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig5, use_container_width=True)

with col_f:
    pivot = _df.groupby(['nama_hari','hour_of_crash']).size() \
               .unstack(fill_value=0).reindex(URUTAN_HARI)
    fig6 = px.imshow(
        pivot,
        color_continuous_scale=PALETTE_SEQ,
        labels={'x':'Jam','y':'Hari','color':'Jumlah'},
        title='Heatmap: Jam x Hari'
    )
    fig6.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig6, use_container_width=True)

# =========================================
# GEOGRAFIS
# =========================================

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">▌ ANALISIS GEOGRAFIS</div>', unsafe_allow_html=True)

col_g, col_h = st.columns(2)

with col_g:
    per_state = (_df.groupby('state_name')['number_of_fatalities']
                   .sum().sort_values(ascending=False).head(10)
                   .sort_values().reset_index())
    per_state.columns = ['State', 'Fatalitas']

    fig7 = px.bar(
        per_state, x='Fatalitas', y='State', orientation='h',
        color='Fatalitas',
        color_continuous_scale=PALETTE_SEQ,
        text_auto=True,
        title='Top 10 State — Total Fatalitas'
    )
    fig7.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
    fig7.update_traces(textfont_color='#4a3728')
    st.plotly_chart(fig7, use_container_width=True)

with col_h:
    df_map = (_df.groupby('state_name')['number_of_fatalities']
                 .sum().reset_index())
    df_map.columns = ['state_name', 'fatalities']

    fig8 = px.choropleth(
        df_map, locations='state_name', locationmode='USA-states',
        color='fatalities', scope='usa', hover_name='state_name',
        color_continuous_scale=PALETTE_SEQ,
        title='Peta Fatalitas per State'
    )
    fig8.update_layout(
        paper_bgcolor='#ede5d8', font_color='#4a3728',
        title_font_size=14, title_font_color='#3d2b1f',
        geo=dict(bgcolor='#ede5d8', lakecolor='#c8d8e8',
                 landcolor='#d4c0a8', subunitcolor='#a09080'),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig8, use_container_width=True)

# =========================================
# SCATTER — DRUNK DRIVER
# =========================================

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">▌ PENGARUH PENGEMUDI MABUK TERHADAP FATALITAS</div>', unsafe_allow_html=True)

fig9 = px.scatter(
    _df, x='number_of_drunk_drivers', y='number_of_fatalities',
    size='number_of_fatalities', color='kategori_waktu',
    hover_data=['state_name'],
    color_discrete_sequence=PALETTE_MAIN,
    title='Korelasi Pengemudi Mabuk vs Jumlah Fatalitas'
)
fig9.update_layout(**PLOTLY_LAYOUT)
st.plotly_chart(fig9, use_container_width=True)

# =========================================
# INSIGHT
# =========================================

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">▌ INSIGHT UTAMA</div>', unsafe_allow_html=True)

if len(_df) > 0:
    mode_hour  = _df['hour_of_crash'].dropna().mode()
    mode_day   = _df['nama_hari'].dropna().mode()
    mode_time  = _df['kategori_waktu'].dropna().mode()
    mode_bulan = _df['nama_bulan'].dropna().mode()

    peak_hour  = int(mode_hour[0])  if len(mode_hour)  > 0 else 0
    peak_day   = mode_day[0]        if len(mode_day)   > 0 else "-"
    peak_time  = mode_time[0]       if len(mode_time)  > 0 else "-"
    peak_bulan = mode_bulan[0]      if len(mode_bulan) > 0 else "-"

    state_fatal = _df.groupby('state_name')['number_of_fatalities'].sum()
    top_state   = state_fatal.idxmax() if len(state_fatal) > 0 else "-"

    akhir_pekan_pct = (_df['tipe_hari'] == 'Akhir Pekan').sum() / len(_df) * 100

    insights = [
        f"Puncak kecelakaan fatal paling sering terjadi pada jam <b>{peak_hour:02d}:00</b>.",
        f"Hari dengan kecelakaan tertinggi adalah <b>{peak_day}</b>.",
        f"Kategori waktu paling rawan adalah <b>{peak_time}</b>.",
        f"Bulan paling banyak kecelakaan: <b>{peak_bulan}</b>.",
        f"<b>{akhir_pekan_pct:.1f}%</b> kecelakaan terjadi di akhir pekan.",
        f"State dengan fatalitas tertinggi: <b>{top_state}</b>.",
        "Pengemudi mabuk berkorelasi positif dengan peningkatan jumlah fatalitas.",
    ]

    st.markdown('<div class="insight-grid">', unsafe_allow_html=True)
    for text in insights:
        st.markdown(f'<div class="insight-item">{text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

# =========================================
# FOOTER
# =========================================

st.markdown("""
<div style='height:2rem'></div>
<div class="footer-text">
    DASHBOARD · STREAMLIT + PANDAS + PLOTLY &nbsp;|&nbsp; DATA: NHTSA TRAFFIC FATALITIES 2015
</div>
""", unsafe_allow_html=True)
