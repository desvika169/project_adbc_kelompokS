import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================
# KONFIGURASI HALAMAN
# =========================================

st.set_page_config(
    page_title="Analisis Kecelakaan Fatal USA 2015",
    layout="wide"
)

# =========================================
# COLOR PALETTE & DESIGN SYSTEM
# =========================================
# Primary:   #0D1B2A  (navy deep)
# Accent:    #E63946  (red alert)
# Highlight: #457B9D  (steel blue)
# Muted:     #A8DADC  (soft teal)
# Light:     #F1FAEE  (off-white)
# Card bg:   #1D3557  (dark navy)

C_PRIMARY   = '#0D1B2A'
C_ACCENT    = '#E63946'
C_BLUE      = '#457B9D'
C_TEAL      = '#A8DADC'
C_LIGHT     = '#F1FAEE'
C_CARD      = '#1D3557'
C_MUTED     = '#6C757D'
C_BG        = '#F8F9FA'
C_WHITE     = '#FFFFFF'
C_BORDER    = '#DEE2E6'

PALETTE_CHART   = [C_BLUE, C_ACCENT, '#F4A261', '#2A9D8F', '#9B5DE5', '#F7B731']
PALETTE_TIME    = ['#264653', '#2A9D8F', '#E9C46A', '#E76F51']

CHART_LAYOUT = dict(
    plot_bgcolor=C_WHITE,
    paper_bgcolor=C_WHITE,
    font=dict(family='Inter, sans-serif', color='#333333', size=12),
    title_font=dict(size=14, color=C_PRIMARY, family='Inter, sans-serif'),
    margin=dict(t=50, b=30, l=20, r=20),
    hoverlabel=dict(bgcolor=C_WHITE, font_size=12, bordercolor=C_BORDER),
)

AXIS_STYLE = dict(
    showgrid=True,
    gridcolor='#F0F0F0',
    linecolor=C_BORDER,
    tickfont=dict(size=11, color='#555'),
    title_font=dict(size=12, color='#555'),
    zeroline=False,
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .main .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}

    /* ---- HEADER ---- */
    .dash-header {{
        background: linear-gradient(135deg, {C_PRIMARY} 0%, {C_CARD} 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        color: {C_WHITE};
    }}
    .dash-header h1 {{
        font-size: 1.9rem;
        font-weight: 700;
        color: {C_WHITE};
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }}
    .dash-header p {{
        font-size: 0.92rem;
        color: {C_TEAL};
        margin: 0;
        opacity: 0.9;
    }}
    .dash-subtitle {{
        font-size: 1rem;
        color: {C_TEAL};
        font-weight: 500;
        margin: 0 0 10px 0;
    }}

    /* ---- METRIC CARDS ---- */
    .metric-row {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 1.5rem;
    }}
    .metric-card {{
        background: {C_WHITE};
        border: 1px solid {C_BORDER};
        border-radius: 12px;
        padding: 20px 24px;
        position: relative;
        overflow: hidden;
        transition: box-shadow 0.2s;
    }}
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 4px; height: 100%;
        border-radius: 12px 0 0 12px;
    }}
    .metric-card.c1::before {{ background: {C_ACCENT}; }}
    .metric-card.c2::before {{ background: {C_BLUE}; }}
    .metric-card.c3::before {{ background: '#2A9D8F'; }}
    .metric-card.c4::before {{ background: '#F4A261'; }}
    .metric-label {{
        font-size: 0.75rem;
        font-weight: 600;
        color: {C_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }}
    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {C_PRIMARY};
        line-height: 1;
    }}

    /* ---- SECTION HEADERS ---- */
    .section-title {{
        font-size: 1rem;
        font-weight: 700;
        color: {C_PRIMARY};
        text-transform: uppercase;
        letter-spacing: 1px;
        padding-bottom: 10px;
        border-bottom: 2px solid {C_ACCENT};
        margin-bottom: 1.2rem;
        display: inline-block;
    }}

    /* ---- INSIGHT CARDS ---- */
    .insight-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-top: 8px;
    }}
    .insight-card {{
        background: {C_WHITE};
        border: 1px solid {C_BORDER};
        border-radius: 10px;
        padding: 14px 18px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }}
    .insight-number {{
        background: {C_PRIMARY};
        color: {C_WHITE};
        font-size: 0.75rem;
        font-weight: 700;
        width: 24px; height: 24px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }}
    .insight-text {{
        font-size: 0.88rem;
        color: #333;
        line-height: 1.5;
    }}
    .insight-text b {{ color: {C_ACCENT}; }}

    /* ---- DIVIDER ---- */
    .section-gap {{ margin: 2rem 0 1rem; }}

    /* ---- SIDEBAR ---- */
    section[data-testid="stSidebar"] {{
        background: {C_PRIMARY};
    }}
    section[data-testid="stSidebar"] * {{
        color: {C_WHITE} !important;
    }}
    section[data-testid="stSidebar"] .stMultiSelect > div {{
        background: rgba(255,255,255,0.1) !important;
        border-color: rgba(255,255,255,0.2) !important;
    }}

    /* ---- FOOTER ---- */
    .footer {{
        text-align: center;
        padding: 1.5rem 0 0.5rem;
        font-size: 0.8rem;
        color: {C_MUTED};
        border-top: 1px solid {C_BORDER};
        margin-top: 2rem;
    }}
</style>
""", unsafe_allow_html=True)

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
# HEADER
# =========================================

st.markdown("""
<div class="dash-header">
    <p class="dash-subtitle">Dashboard Analisis</p>
    <h1>Pola Kecelakaan Fatal di Amerika Serikat</h1>
    <p>Exploratory Data Analysis berdasarkan faktor waktu dan geografis &mdash; Data NHTSA Tahun 2015</p>
</div>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:
    st.markdown("### Filter Dashboard")
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
    st.caption(f"Data tersaring: **{len(_df):,}** baris")

# =========================================
# METRIC CARDS
# =========================================

val_kecelakaan = f"{len(_df):,}"
val_state      = str(_df['state_name'].nunique()) if 'state_name' in _df.columns else "-"
val_fatalitas  = f"{int(_df['number_of_fatalities'].sum()):,}" if 'number_of_fatalities' in _df.columns else "-"
val_drunk      = f"{int(_df['number_of_drunk_drivers'].sum()):,}" if 'number_of_drunk_drivers' in _df.columns else "-"

c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, 'c1', 'Total Kecelakaan',   val_kecelakaan),
    (c2, 'c2', 'Jumlah State',       val_state),
    (c3, 'c3', 'Total Fatalitas',    val_fatalitas),
    (c4, 'c4', 'Total Drunk Driver', val_drunk),
]
for col, cls, label, val in cards:
    with col:
        st.markdown(f"""
        <div class="metric-card {cls}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{val}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# =========================================
# SECTION: ANALISIS WAKTU
# =========================================

st.markdown('<span class="section-title">Analisis Waktu</span>', unsafe_allow_html=True)

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
        color_discrete_sequence=PALETTE_TIME,
        text_auto=True,
        title='Distribusi Kecelakaan per Kategori Waktu'
    )
    fig.update_layout(**CHART_LAYOUT, showlegend=False)
    fig.update_xaxes(**AXIS_STYLE, title='')
    fig.update_yaxes(**AXIS_STYLE, title='Jumlah Kecelakaan')
    fig.update_traces(textposition='outside', textfont_size=11)
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    per_tipe = _df['tipe_hari'].value_counts().reset_index()
    per_tipe.columns = ['Tipe', 'Jumlah']

    fig2 = px.pie(
        per_tipe, names='Tipe', values='Jumlah',
        color_discrete_sequence=[C_BLUE, C_ACCENT],
        hole=0.5,
        title='Hari Kerja vs Akhir Pekan'
    )
    fig2.update_layout(**CHART_LAYOUT)
    fig2.update_traces(
        textinfo='percent+label',
        pull=[0.04, 0.04],
        textfont_size=12
    )
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
            color_discrete_map={'Puncak': C_ACCENT, 'Normal': C_BLUE},
            title=f'Distribusi Kecelakaan per Jam  —  Puncak: {int(peak_jam):02d}:00'
        )
        fig3.update_layout(**CHART_LAYOUT, showlegend=False)
        fig3.update_xaxes(**AXIS_STYLE, title='Jam', dtick=2)
        fig3.update_yaxes(**AXIS_STYLE, title='Jumlah Kecelakaan')
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Tidak ada data untuk ditampilkan.")

with col_d:
    per_hari = _df['nama_hari'].value_counts().reindex(URUTAN_HARI).reset_index()
    per_hari.columns = ['Hari', 'Jumlah']

    fig4 = px.bar(
        per_hari, x='Hari', y='Jumlah',
        color='Jumlah',
        color_continuous_scale=[[0, '#D0E8F7'], [1, C_PRIMARY]],
        text_auto=True,
        title='Distribusi Kecelakaan per Hari'
    )
    fig4.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
    fig4.update_xaxes(**AXIS_STYLE, title='')
    fig4.update_yaxes(**AXIS_STYLE, title='Jumlah Kecelakaan')
    fig4.update_traces(textposition='outside', textfont_size=11)
    st.plotly_chart(fig4, use_container_width=True)

col_e, col_f = st.columns(2)

with col_e:
    per_bulan = _df['nama_bulan'].value_counts().reindex(URUTAN_BULAN).reset_index()
    per_bulan.columns = ['Bulan', 'Jumlah']

    fig5 = px.line(
        per_bulan, x='Bulan', y='Jumlah', markers=True,
        title='Tren Kecelakaan per Bulan',
        color_discrete_sequence=[C_BLUE]
    )
    fig5.update_traces(
        line_width=2.5, marker_size=8,
        marker_color=C_ACCENT, line_color=C_BLUE,
        fill='tozeroy', fillcolor='rgba(69,123,157,0.08)'
    )
    fig5.update_layout(**CHART_LAYOUT)
    fig5.update_xaxes(**AXIS_STYLE, title='')
    fig5.update_yaxes(**AXIS_STYLE, title='Jumlah Kecelakaan')
    st.plotly_chart(fig5, use_container_width=True)

with col_f:
    pivot = _df.groupby(['nama_hari','hour_of_crash']).size() \
               .unstack(fill_value=0).reindex(URUTAN_HARI)
    fig6 = px.imshow(
        pivot,
        color_continuous_scale=[[0,'#EEF4FB'],[0.5,'#457B9D'],[1,'#0D1B2A']],
        labels={'x':'Jam','y':'Hari','color':'Jumlah'},
        title='Heatmap Kecelakaan: Jam vs Hari'
    )
    fig6.update_layout(**CHART_LAYOUT)
    fig6.update_xaxes(title='Jam', dtick=2, tickfont_size=11)
    fig6.update_yaxes(title='', tickfont_size=11)
    st.plotly_chart(fig6, use_container_width=True)

# =========================================
# SECTION: ANALISIS GEOGRAFIS
# =========================================

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
st.markdown('<span class="section-title">Analisis Geografis</span>', unsafe_allow_html=True)

col_g, col_h = st.columns(2)

with col_g:
    per_state = (_df.groupby('state_name')['number_of_fatalities']
                   .sum().sort_values(ascending=False).head(10)
                   .sort_values().reset_index())
    per_state.columns = ['State', 'Fatalitas']

    fig7 = px.bar(
        per_state, x='Fatalitas', y='State', orientation='h',
        color='Fatalitas',
        color_continuous_scale=[[0,'#FDECEA'],[1, C_ACCENT]],
        text_auto=True,
        title='Top 10 State — Total Fatalitas'
    )
    fig7.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
    fig7.update_xaxes(**AXIS_STYLE, title='Total Fatalitas')
    fig7.update_yaxes(**AXIS_STYLE, title='')
    fig7.update_traces(textposition='outside', textfont_size=11)
    st.plotly_chart(fig7, use_container_width=True)

with col_h:
    df_map = (_df.groupby('state_name')['number_of_fatalities']
                 .sum().reset_index())
    df_map.columns = ['state_name', 'fatalities']

    fig8 = px.choropleth(
        df_map, locations='state_name', locationmode='USA-states',
        color='fatalities', scope='usa', hover_name='state_name',
        color_continuous_scale=[[0,'#EEF4FB'],[0.5,C_BLUE],[1,C_PRIMARY]],
        title='Peta Persebaran Fatalitas per State'
    )
    fig8.update_layout(
        **CHART_LAYOUT,
        geo=dict(bgcolor=C_WHITE, lakecolor=C_WHITE, landcolor='#F5F5F5',
                 showlakes=True, showland=True, subunitcolor=C_BORDER),
        coloraxis_colorbar=dict(title='Fatalitas', tickfont_size=10)
    )
    st.plotly_chart(fig8, use_container_width=True)

# =========================================
# SECTION: PENGEMUDI MABUK
# =========================================

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
st.markdown('<span class="section-title">Pengaruh Pengemudi Mabuk terhadap Fatalitas</span>', unsafe_allow_html=True)

fig9 = px.scatter(
    _df, x='number_of_drunk_drivers', y='number_of_fatalities',
    size='number_of_fatalities', color='kategori_waktu',
    hover_data=['state_name'],
    color_discrete_sequence=PALETTE_TIME,
    title='Korelasi Jumlah Pengemudi Mabuk vs Jumlah Fatalitas',
    size_max=30
)
fig9.update_layout(**CHART_LAYOUT)
fig9.update_xaxes(**AXIS_STYLE, title='Jumlah Pengemudi Mabuk')
fig9.update_yaxes(**AXIS_STYLE, title='Jumlah Fatalitas')
st.plotly_chart(fig9, use_container_width=True)

# =========================================
# SECTION: INSIGHT
# =========================================

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
st.markdown('<span class="section-title">Insight Utama</span>', unsafe_allow_html=True)

if len(_df) > 0:
    mode_hour  = _df['hour_of_crash'].dropna().mode()
    mode_day   = _df['nama_hari'].dropna().mode()
    mode_time  = _df['kategori_waktu'].dropna().mode()
    mode_bulan = _df['nama_bulan'].dropna().mode()

    peak_hour  = int(mode_hour[0])  if len(mode_hour)  > 0 else 0
    peak_day   = mode_day[0]        if len(mode_day)   > 0 else "-"
    peak_time  = mode_time[0]       if len(mode_time)  > 0 else "-"
    peak_bulan = mode_bulan[0]      if len(mode_bulan) > 0 else "-"

    state_fatal     = _df.groupby('state_name')['number_of_fatalities'].sum()
    top_state       = state_fatal.idxmax() if len(state_fatal) > 0 else "-"
    akhir_pekan_pct = (_df['tipe_hari'] == 'Akhir Pekan').sum() / len(_df) * 100

    insights = [
        f"Puncak kecelakaan fatal paling sering terjadi pada jam <b>{peak_hour:02d}:00</b>.",
        f"Hari dengan jumlah kecelakaan tertinggi adalah <b>{peak_day}</b>.",
        f"Kategori waktu paling rawan kecelakaan adalah <b>{peak_time}</b>.",
        f"Bulan dengan kecelakaan terbanyak adalah <b>{peak_bulan}</b>.",
        f"<b>{akhir_pekan_pct:.1f}%</b> dari total kecelakaan terjadi di akhir pekan.",
        f"State dengan jumlah fatalitas tertinggi adalah <b>{top_state}</b>.",
        "Jumlah pengemudi mabuk berkorelasi positif dengan meningkatnya jumlah fatalitas.",
    ]

    html_insights = ""
    for i, text in enumerate(insights, 1):
        html_insights += f"""
        <div class="insight-card">
            <div class="insight-number">{i}</div>
            <div class="insight-text">{text}</div>
        </div>"""

    st.markdown(f'<div class="insight-grid">{html_insights}</div>', unsafe_allow_html=True)
else:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

# =========================================
# FOOTER
# =========================================

st.markdown("""
<div class="footer">
    Dashboard Analisis Kecelakaan Fatal USA 2015 &nbsp;&middot;&nbsp;
    Dibuat menggunakan Streamlit, Pandas, dan Plotly &nbsp;&middot;&nbsp;
    Sumber data: NHTSA Traffic Fatalities
</div>
""", unsafe_allow_html=True)
