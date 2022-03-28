from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
st.title('Data Ketersediaan Kasur di Rumah Sakit Jawa Barat')
DATA_URL = ('satgas-covid-19-dp_cvd_bor_data_wilayah_data.csv')

@st.cache
def load_data():
    df = pd.read_csv(DATA_URL)
    df = df.drop('tanggal_update_api', 1)
    df['tanggal_update'] = pd.to_datetime(df['tanggal_update'])
    return df

def filter_agg(data, list_filter=None,filter_ketersediaan=None,kota=None):
    temp_data = data
    filter_ruangan = []
    filter_ruangan += index_filter
    for state in filter_ketersediaan:
        try:
            filter_ruangan += list_filter[state]
        except Exception:
            pass
    if (kota is not None) and ('Jawa Barat' not in kota):
        temp_data = temp_data[temp_data['kabupaten_kota'].isin(kota)]
    if list_filter is not None and filter_ketersediaan is not None:
        temp_data = temp_data[filter_ruangan]
    return temp_data.groupby('tanggal_update', as_index=True).sum()


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
data_load_state.text('')
list_kota = ['Jawa Barat','Bandung','Bandung Barat','Bekasi','Bogor','Ciamis','Cianjur','Cirebon','Garut','Indramayu','Karawang','Kota Bandung','Kota Banjar','Kota Bekasi','Kota Bogor','Kota Cimahi','Kota Cirebon','Kota Depok','Kota Sukabumi','Kota Tasikmalaya','Kuningan','Majalengka','Pangandaran','Purwakarta','Subang','Sukabumi','Sumedang','Tasikmalaya']
index_filter = [
    'tanggal_update',
    'kabupaten_kota',
]
icu_filter = {
    'Tersedia':[
        'icu_tanpa_tekanan_negatif_dengan_ventilator_tersedia',
        'icu_tanpa_tekanan_negatif_tanpa_ventilator_tersedia',
        'icu_tekanan_negatif_dengan_ventilator_tersedia',
        'icu_tekanan_negatif_tanpa_ventilator_tersedia',
    ],
    'Terpakai':[
        'icu_tanpa_tekanan_negatif_dengan_ventilator_terpakai',
        'icu_tanpa_tekanan_negatif_tanpa_ventilator_terpakai',
        'icu_tekanan_negatif_dengan_ventilator_terpakai',
        'icu_tekanan_negatif_tanpa_ventilator_terpakai'
    ]
}
isolasi_filter = {
    'Tersedia':[
        'isolasi_tanpa_tekanan_negatif_tersedia',
        'isolasi_tekanan_negatif_tersedia',
    ],
    'Terpakai':[
        'isolasi_tanpa_tekanan_negatif_terpakai',
        'isolasi_tekanan_negatif_terpakai'
    ]
}
nicu_filter = {
    'Tersedia':['nicu_covid_tersedia'],
    'Terpakai':['nicu_covid_terpakai']
}
picu_filter = {
    'Tersedia':['picu_covid_tersedia'],
    'Terpakai':['picu_covid_terpakai']
}
igd_filter = {
    'Tersedia':['igd_covid_tersedia'],
    'Terpakai':['igd_covid_terpakai']
}
vk_filter = {
    'Tersedia':['vk_covid_tersedia'],
    'Terpakai':['vk_covid_terpakai']
}

## Sidebar
st.sidebar.header("**Filter**")
col1,col2 = st.sidebar.columns(2)
start_date = col1.date_input('Tanggal awal',value=datetime(2020,10,6),min_value=datetime(2020,10,6),max_value=datetime(2022,3,3))
end_date = col2.date_input('Tanggal akhir',value=datetime(2022,3,3),min_value=start_date,max_value=datetime(2022,3,3))

filter_kota = st.sidebar.selectbox(
    label='Kabupaten/Kota',
    options=list_kota
)

filter_ketersediaan = st.sidebar.multiselect(
    label='Ketersediaan',
    options=['Terpakai','Tersedia'],
    default=['Terpakai','Tersedia']
)


## Main content
st.subheader(f'Ketersediaan Ruang ICU {filter_kota}')

jabar_icu = filter_agg(data,icu_filter,filter_ketersediaan,[filter_kota])
jabar_icu = jabar_icu.loc[start_date:end_date]
st.line_chart(jabar_icu)

st.subheader(f'Ketersediaan Ruang Isolasi {filter_kota}')
jabar_isolasi = filter_agg(data,isolasi_filter,filter_ketersediaan,[filter_kota])
jabar_isolasi = jabar_isolasi.loc[start_date:end_date]
st.line_chart(jabar_isolasi)

st.subheader(f'Ketersediaan Ruang NICU {filter_kota}')
jabar_nicu = filter_agg(data,nicu_filter,filter_ketersediaan,[filter_kota])
jabar_nicu = jabar_nicu.loc[start_date:end_date]
st.line_chart(jabar_nicu)

st.subheader(f'Ketersediaan Ruang PICU {filter_kota}')
jabar_picu = filter_agg(data,picu_filter,filter_ketersediaan,[filter_kota])
jabar_picu = jabar_picu.loc[start_date:end_date]
st.line_chart(jabar_picu)

st.subheader(f'Ketersediaan Ruang IGD {filter_kota}')
jabar_igd = filter_agg(data,igd_filter,filter_ketersediaan,[filter_kota])
jabar_igd = jabar_igd.loc[start_date:end_date]
st.line_chart(jabar_igd)

st.subheader(f'Ketersediaan Ruang VK {filter_kota}')
jabar_igd = filter_agg(data,vk_filter,filter_ketersediaan,[filter_kota])
jabar_igd = jabar_igd.loc[start_date:end_date]
st.line_chart(jabar_igd)