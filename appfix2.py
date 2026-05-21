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
# CUSTOM CSS
# =========================================

st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f, #2d6a9f);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 8px 0 4px;
    }
    .metric-label {
        font-size: 0.85rem;
        opacity: 0.85;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-icon {
        font-size: 1.6rem;
    }
    .section-divider {
        border: none;
        border-top: 2px solid #e0e0e0;
        margin: 2rem 0 1rem;
    }
    .insight-box {
        background: #f0f7ff;
        border-left: 5px solid #1e6fbf;
        border-radius: 0 10px 10px 0;
        padding: 16px 20px;
        margin: 8px 0;
        color: #1a1a2e;
    }
    .insight-box b { color: #1e3a5f; }
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
WARNA_UTAMA  = ['#1e6fbf','#e84545','#f5a623','#2ecc71','#9b59b6','#e67e22','#1abc9c']

# =========================================
# HEADER
# =========================================

st.markdown("""
<div style='padding: 2rem 0 1rem;'>
    <h1 style='font-size:2.2rem; font-weight:800; color:#1e3a5f; margin:0;'>
        Analisis Pola Kecelakaan Fatal
    </h1>
    <h2 style='font-size:1.3rem; font-weight:400; color:#555; margin:4px 0 0;'>
        Amerika Serikat — Tahun 2015
    </h2>
    <p style='color:#777; margin-top:8px; font-size:0.95rem;'>
        Exploratory Data Analysis berdasarkan faktor waktu dan geografis menggunakan data NHTSA
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR FILTER
# =========================================

with st.sidebar:
    st.markdown("## Filter Dashboard")
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

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("### Ringkasan Data")

c1, c2, c3, c4 = st.columns(4)
metrics = [
    (c1, f"{len(_df):,}",                                          "Total Kecelakaan"),
    (c2, str(_df['state_name'].nunique()),                         "Jumlah State"),
    (c3, f"{int(_df['number_of_fatalities'].sum()):,}",            "Total Fatalitas"),
    (c4, f"{int(_df['number_of_drunk_drivers'].sum()):,}",         "Total Drunk Driver"),
]
for col, icon, val, label in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================
# BARIS 1 — KATEGORI WAKTU & TIPE HARI
# =========================================

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("### Analisis Waktu")

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
        color_discrete_sequence=['#4e89e8','#f5a623','#e84545','#2c3e8c'],
        text_auto=True,
        title='Distribusi per Kategori Waktu'
    )
    fig.update_layout(showlegend=False, plot_bgcolor='white',
                      paper_bgcolor='white', font_color='#333',
                      title_font_size=15)
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    per_tipe = _df['tipe_hari'].value_counts().reset_index()
    per_tipe.columns = ['Tipe', 'Jumlah']

    fig2 = px.pie(
        per_tipe, names='Tipe', values='Jumlah',
        color_discrete_sequence=['#1e6fbf','#e84545'],
        hole=0.45,
        title='Hari Kerja vs Akhir Pekan'
    )
    fig2.update_layout(title_font_size=15, font_color='#333',
                       paper_bgcolor='white')
    fig2.update_traces(textinfo='percent+label', pull=[0.03, 0.03])
    st.plotly_chart(fig2, use_container_width=True)

# =========================================
# BARIS 2 — JAM & HARI
# =========================================

col_c, col_d = st.columns(2)

with col_c:
    per_jam = _df['hour_of_crash'].value_counts().sort_index().reset_index()
    per_jam.columns = ['Jam', 'Jumlah']
    peak_jam = per_jam.loc[per_jam['Jumlah'].idxmax(), 'Jam']
    per_jam['warna'] = per_jam['Jam'].apply(lambda x: 'Puncak' if x == peak_jam else 'Normal')

    fig3 = px.bar(
        per_jam, x='Jam', y='Jumlah', color='warna',
        color_discrete_map={'Puncak':'#e84545','Normal':'#4e89e8'},
        title=f'Kecelakaan per Jam (Puncak: {int(peak_jam):02d}:00)'
    )
    fig3.update_layout(showlegend=False, plot_bgcolor='white',
                       paper_bgcolor='white', font_color='#333',
                       title_font_size=15)
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    per_hari = _df['nama_hari'].value_counts().reindex(URUTAN_HARI).reset_index()
    per_hari.columns = ['Hari', 'Jumlah']

    fig4 = px.bar(
        per_hari, x='Hari', y='Jumlah',
        color='Jumlah', color_continuous_scale='Blues',
        text_auto=True,
        title='Distribusi per Hari'
    )
    fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                       font_color='#333', title_font_size=15,
                       coloraxis_showscale=False)
    fig4.update_traces(textposition='outside')
    st.plotly_chart(fig4, use_container_width=True)

# =========================================
# BARIS 3 — BULAN & HEATMAP
# =========================================

col_e, col_f = st.columns(2)

with col_e:
    per_bulan = _df['nama_bulan'].value_counts().reindex(URUTAN_BULAN).reset_index()
    per_bulan.columns = ['Bulan', 'Jumlah']

    fig5 = px.line(
        per_bulan, x='Bulan', y='Jumlah', markers=True,
        title='Tren Kecelakaan per Bulan',
        color_discrete_sequence=['#1e6fbf']
    )
    fig5.update_traces(line_width=2.5, marker_size=8)
    fig5.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                       font_color='#333', title_font_size=15)
    fig5.update_xaxes(showgrid=True, gridcolor='#eee')
    fig5.update_yaxes(showgrid=True, gridcolor='#eee')
    st.plotly_chart(fig5, use_container_width=True)

with col_f:
    pivot = _df.groupby(['nama_hari','hour_of_crash']).size() \
               .unstack(fill_value=0).reindex(URUTAN_HARI)
    fig6 = px.imshow(
        pivot, color_continuous_scale='YlOrRd',
        labels={'x':'Jam','y':'Hari','color':'Jumlah'},
        title='Heatmap: Jam × Hari'
    )
    fig6.update_layout(paper_bgcolor='white', font_color='#333', title_font_size=15)
    st.plotly_chart(fig6, use_container_width=True)

# =========================================
# BARIS 4 — GEOGRAFIS
# =========================================

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("### Analisis Geografis")

col_g, col_h = st.columns(2)

with col_g:
    per_state = (_df.groupby('state_name')['number_of_fatalities']
                   .sum().sort_values(ascending=False).head(10)
                   .sort_values().reset_index())
    per_state.columns = ['State', 'Fatalitas']

    fig7 = px.bar(
        per_state, x='Fatalitas', y='State', orientation='h',
        color='Fatalitas', color_continuous_scale='Reds',
        text_auto=True, title='Top 10 State — Total Fatalitas'
    )
    fig7.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                       font_color='#333', title_font_size=15,
                       coloraxis_showscale=False)
    st.plotly_chart(fig7, use_container_width=True)

with col_h:
    df_map = (_df.groupby('state_name')['number_of_fatalities']
                 .sum().reset_index())
    df_map.columns = ['state_name', 'fatalities']

    fig8 = px.choropleth(
        df_map, locations='state_name', locationmode='USA-states',
        color='fatalities', scope='usa', hover_name='state_name',
        color_continuous_scale='Reds',
        title='Peta Fatalitas per State'
    )
    fig8.update_layout(paper_bgcolor='white', font_color='#333', title_font_size=15)
    st.plotly_chart(fig8, use_container_width=True)

# =========================================
# SCATTER — DRUNK DRIVER
# =========================================

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("### Pengaruh Pengemudi Mabuk terhadap Fatalitas")

fig9 = px.scatter(
    _df, x='number_of_drunk_drivers', y='number_of_fatalities',
    size='number_of_fatalities', color='kategori_waktu',
    hover_data=['state_name'],
    color_discrete_sequence=WARNA_UTAMA,
    title='Korelasi Pengemudi Mabuk vs Jumlah Fatalitas'
)
fig9.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                   font_color='#333', title_font_size=15)
fig9.update_xaxes(showgrid=True, gridcolor='#eee')
fig9.update_yaxes(showgrid=True, gridcolor='#eee')
st.plotly_chart(fig9, use_container_width=True)

# =========================================
# INSIGHT
# =========================================

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("### Insight Utama")

if len(_df) > 0:
    peak_hour = _df['hour_of_crash'].mode()[0]
    peak_day  = _df['nama_hari'].mode()[0]
    peak_time = _df['kategori_waktu'].mode()[0]
    peak_bulan = _df['nama_bulan'].mode()[0]
    top_state  = (_df.groupby('state_name')['number_of_fatalities']
                     .sum().idxmax())
    akhir_pekan_pct = (
        (_df['tipe_hari'] == 'Akhir Pekan').sum() / len(_df) * 100
    )

    insights = [
        (f"Puncak kecelakaan fatal paling sering terjadi pada jam <b>{int(peak_hour):02d}:00</b>."),
        (f"Hari dengan kecelakaan tertinggi adalah <b>{peak_day}</b>."),
        (f"Kategori waktu paling rawan adalah <b>{peak_time}</b>."),
        (f"Bulan paling banyak kecelakaan: <b>{peak_bulan}</b>."),
        (f"<b>{akhir_pekan_pct:.1f}%</b> kecelakaan terjadi di akhir pekan."),
        (f"State dengan fatalitas tertinggi: <b>{top_state}</b>."),
        ("Faktor pengemudi mabuk berkorelasi positif dengan meningkatnya jumlah fatalitas."),
    ]
    for i, text in enumerate(insights, 1):
        st.markdown(f'<div class="insight-box">🔹 {text}</div>', unsafe_allow_html=True)

# =========================================
# FOOTER
# =========================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Dashboard dibuat menggunakan Streamlit · Pandas · Plotly 🚀 | Data: NHTSA Traffic Fatalities 2015")
