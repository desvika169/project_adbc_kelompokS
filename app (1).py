import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Dashboard Kecelakaan Fatal USA 2015",
    layout="wide"
)

# ─── LOAD & PREPROCESSING DATA ───────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("datadf_clean.csv")

    # Ganti nilai unknown
    df['hour_of_crash']  = df['hour_of_crash'].replace(99, np.nan)
    df['month_of_crash'] = df['month_of_crash'].replace(99, np.nan)
    df['day_of_week']    = df['day_of_week'].replace(9, np.nan)
    df = df.dropna(subset=['hour_of_crash', 'month_of_crash', 'day_of_week'])
    df = df.drop_duplicates()

    df['hour_of_crash']        = df['hour_of_crash'].astype(int)
    df['month_of_crash']       = df['month_of_crash'].astype(int)
    df['day_of_week']          = df['day_of_week'].astype(int)
    df['number_of_fatalities'] = df['number_of_fatalities'].astype(int)

    def kategorikan_waktu(h):
        if 0 <= h <= 5:     return 'Dini hari (00-05)'
        elif 6 <= h <= 11:  return 'Pagi (06-11)'
        elif 12 <= h <= 17: return 'Siang (12-17)'
        else:               return 'Malam (18-23)'

    df['waktu_kategori'] = df['hour_of_crash'].apply(kategorikan_waktu)
    df['tipe_hari']      = df['day_of_week'].apply(
        lambda d: 'Akhir Pekan' if d in [1, 7] else 'Hari Kerja'
    )
    nama_hari_map = {1:'Minggu', 2:'Senin', 3:'Selasa', 4:'Rabu',
                     5:'Kamis',  6:'Jumat', 7:'Sabtu'}
    df['nama_hari'] = df['day_of_week'].map(nama_hari_map)
    return df

df_clean = load_data()

NAMA_BULAN   = ['Jan','Feb','Mar','Apr','Mei','Jun',
                'Jul','Agu','Sep','Okt','Nov','Des']
URUTAN_HARI  = ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu']

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.title("Dashboard Kecelakaan Fatal di Amerika Serikat (2015)")
st.write("Analisis pola kecelakaan fatal berdasarkan waktu dan lokasi menggunakan data NHTSA.")

# ─── SIDEBAR FILTER ──────────────────────────────────────────────────────────
st.sidebar.header("Filter Data")

tipe_hari_options = ["Semua"] + list(df_clean['tipe_hari'].unique())
filter_tipe_hari  = st.sidebar.selectbox("Tipe Hari", tipe_hari_options)

waktu_options = ["Semua"] + list(df_clean['waktu_kategori'].unique())
filter_waktu  = st.sidebar.selectbox("Kategori Waktu", waktu_options)

all_states   = sorted(df_clean['state_name'].unique())
filter_state = st.sidebar.multiselect("Negara Bagian (kosongkan = semua)", all_states)

# Apply filter
df_filtered = df_clean.copy()
if filter_tipe_hari != "Semua":
    df_filtered = df_filtered[df_filtered['tipe_hari'] == filter_tipe_hari]
if filter_waktu != "Semua":
    df_filtered = df_filtered[df_filtered['waktu_kategori'] == filter_waktu]
if filter_state:
    df_filtered = df_filtered[df_filtered['state_name'].isin(filter_state)]

# ─── METRIK RINGKASAN ─────────────────────────────────────────────────────────
st.subheader("Ringkasan Data")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Kecelakaan",    f"{len(df_filtered):,}")
col2.metric("Total Fatalitas",     f"{df_filtered['number_of_fatalities'].sum():,}")
col3.metric("Jam Paling Fatal",    f"{df_filtered['hour_of_crash'].value_counts().idxmax():02d}:00" if len(df_filtered) > 0 else "-")
col4.metric("State Paling Fatal",  df_filtered.groupby('state_name')['number_of_fatalities'].sum().idxmax() if len(df_filtered) > 0 else "-")

st.markdown("---")

# ─── VISUALISASI ─────────────────────────────────────────────────────────────

# Baris 1: Jam & Bulan
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Kecelakaan Fatal per Jam")
    per_jam = df_filtered['hour_of_crash'].value_counts().sort_index().reset_index()
    per_jam.columns = ['jam', 'jumlah']
    peak = per_jam.loc[per_jam['jumlah'].idxmax(), 'jam'] if len(per_jam) > 0 else 0
    per_jam['warna'] = per_jam['jam'].apply(lambda x: 'Puncak' if x == peak else 'Lainnya')
    fig_jam = px.bar(
        per_jam, x='jam', y='jumlah', color='warna',
        color_discrete_map={'Puncak': 'crimson', 'Lainnya': 'steelblue'},
        title=f"Puncak kecelakaan: jam {int(peak):02d}:00",
        labels={'jam': 'Jam', 'jumlah': 'Jumlah Kecelakaan'}
    )
    fig_jam.update_layout(showlegend=False)
    st.plotly_chart(fig_jam, use_container_width=True)

with col_b:
    st.subheader("Kecelakaan Fatal per Bulan")
    per_bulan = df_filtered['month_of_crash'].value_counts().sort_index().reset_index()
    per_bulan.columns = ['bulan', 'jumlah']
    per_bulan['label'] = per_bulan['bulan'].apply(lambda x: NAMA_BULAN[int(x)-1])
    fig_bulan = px.line(
        per_bulan, x='label', y='jumlah', markers=True,
        title="Tren kecelakaan sepanjang tahun 2015",
        labels={'label': 'Bulan', 'jumlah': 'Jumlah Kecelakaan'},
        color_discrete_sequence=['steelblue']
    )
    st.plotly_chart(fig_bulan, use_container_width=True)

# Baris 2: Tipe Hari & Kategori Waktu
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Hari Kerja vs Akhir Pekan")
    per_tipe = df_filtered['tipe_hari'].value_counts().reset_index()
    per_tipe.columns = ['tipe', 'jumlah']
    fig_tipe = px.pie(
        per_tipe, names='tipe', values='jumlah',
        color_discrete_sequence=['#2196F3', '#FF5722'],
        title="Proporsi kecelakaan berdasarkan tipe hari"
    )
    st.plotly_chart(fig_tipe, use_container_width=True)

with col_d:
    st.subheader("Distribusi Kategori Waktu")
    per_waktu = df_filtered['waktu_kategori'].value_counts().reset_index()
    per_waktu.columns = ['waktu', 'jumlah']
    fig_waktu = px.bar(
        per_waktu, x='waktu', y='jumlah',
        color='waktu', title="Kecelakaan berdasarkan segmen waktu",
        labels={'waktu': 'Kategori Waktu', 'jumlah': 'Jumlah Kecelakaan'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_waktu.update_layout(showlegend=False)
    st.plotly_chart(fig_waktu, use_container_width=True)

# Baris 3: Heatmap Jam × Hari
st.subheader("Heatmap Kecelakaan: Jam × Hari")
pivot = df_filtered.groupby(['nama_hari', 'hour_of_crash']).size() \
                   .unstack(fill_value=0).reindex(URUTAN_HARI)
fig_heat = px.imshow(
    pivot,
    color_continuous_scale='YlOrRd',
    labels={'x': 'Jam', 'y': 'Hari', 'color': 'Jumlah Kecelakaan'},
    title="Pola kecelakaan berdasarkan jam dan hari"
)
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")

# Baris 4: Geografis
col_e, col_f = st.columns(2)

with col_e:
    st.subheader("Top 10 State - Total Fatalitas")
    per_state = df_filtered.groupby('state_name')['number_of_fatalities'] \
                            .sum().sort_values(ascending=False)
    top10 = per_state.head(10).sort_values().reset_index()
    top10.columns = ['state', 'fatalitas']
    top10['warna'] = top10['fatalitas'] == top10['fatalitas'].max()
    fig_state = px.bar(
        top10, x='fatalitas', y='state', orientation='h',
        color='warna', color_discrete_map={True: 'crimson', False: 'steelblue'},
        title="Negara bagian dengan korban meninggal terbanyak",
        labels={'fatalitas': 'Total Korban', 'state': 'State'}
    )
    fig_state.update_layout(showlegend=False)
    st.plotly_chart(fig_state, use_container_width=True)

with col_f:
    st.subheader("Top 10 State - Kecelakaan Malam Hari")
    malam_df    = df_filtered[df_filtered['waktu_kategori'] == 'Malam (18-23)']
    top10_malam = malam_df.groupby('state_name').size().nlargest(10) \
                          .sort_values().reset_index()
    top10_malam.columns = ['state', 'jumlah']
    fig_malam = px.bar(
        top10_malam, x='jumlah', y='state', orientation='h',
        color_discrete_sequence=['darkorange'],
        title="State dengan kecelakaan malam terbanyak",
        labels={'jumlah': 'Jumlah Kecelakaan', 'state': 'State'}
    )
    st.plotly_chart(fig_malam, use_container_width=True)

# Baris 5: Peta Choropleth USA
st.subheader("Peta Fatalitas Kecelakaan per State (USA)")
df_map = df_filtered.groupby('state_name')['number_of_fatalities'].sum().reset_index()
df_map.columns = ['state_name', 'fatalities']
fig_map = px.choropleth(
    df_map,
    locations='state_name',
    locationmode='USA-states',
    color='fatalities',
    scope='usa',
    hover_name='state_name',
    color_continuous_scale='Reds',
    title='Persebaran Fatalitas Kecelakaan di Amerika Serikat Tahun 2015'
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

# ─── INSIGHT ─────────────────────────────────────────────────────────────────
st.subheader("Insight Otomatis")
if len(df_filtered) > 0:
    per_jam_s    = df_filtered['hour_of_crash'].value_counts().sort_index()
    per_bulan_s  = df_filtered['month_of_crash'].value_counts().sort_index()
    per_tipe_s   = df_filtered['tipe_hari'].value_counts()
    per_state_s  = df_filtered.groupby('state_name')['number_of_fatalities'].sum().sort_values(ascending=False)

    st.write(f"1. **Jam paling berbahaya**: {int(per_jam_s.idxmax()):02d}:00 dengan **{per_jam_s.max()} kecelakaan**.")
    st.write(f"2. **Hari Kerja vs Akhir Pekan**: Akhir Pekan menyumbang **{per_tipe_s.get('Akhir Pekan', 0)/per_tipe_s.sum()*100:.1f}%** dari total kecelakaan.")
    st.write(f"3. **Bulan paling fatal**: {NAMA_BULAN[int(per_bulan_s.idxmax())-1]} dengan **{per_bulan_s.max()} kecelakaan**.")
    st.write(f"4. **State paling fatal**: {per_state_s.index[0]} dengan **{int(per_state_s.iloc[0])} korban meninggal**.")
else:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

# ─── PREVIEW DATA ────────────────────────────────────────────────────────────
with st.expander("Lihat Preview Data"):
    st.dataframe(df_filtered[['state_name', 'hour_of_crash', 'month_of_crash',
                               'nama_hari', 'waktu_kategori', 'tipe_hari',
                               'number_of_fatalities']].head(100))
