from datetime import datetime
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
# st.title('Halo Wil')
st.title('Data Ketersediaan Kasur di Rumah Sakit Jawa Barat')
DATA_URL = ('satgas-covid-19-dp_cvd_bor_data_wilayah_data.csv')
colsize=[3.2,5]

@st.cache
def load_data():
    df = pd.read_csv(DATA_URL)
    df = df.drop('tanggal_update_api', axis=1)
    df['tanggal_update'] = pd.to_datetime(df['tanggal_update'])
    return df

def filter_agg(data, list_filter=None,kota=None):
    temp_data = data
    filter_ruangan = index_filter + list_filter['Tersedia'] + list_filter['Terpakai']
    # filter_ketersediaan = ['Terpakai','Tersedia']
    # for state in filter_ketersediaan:
    #     try:
    #         filter_ruangan += list_filter[state]
    #     except Exception:
    #         pass
    if (kota is not None) and ('Jawa Barat' not in kota):
        temp_data = temp_data[temp_data['kabupaten_kota'].isin(kota)]
    if list_filter is not None:
        temp_data = temp_data[filter_ruangan]
    return temp_data.groupby('tanggal_update', as_index=True).sum()

def plot_ketersediaan(kota,data,filter_ruangan,rename_columns,start_date,end_date,st_element=None,axis_mode=None):
    if st_element == None:
        st_element = st
    df_plot = filter_agg(data,filter_ruangan,[kota])
    df_plot = df_plot.loc[start_date:end_date]

    if axis_mode == 'Persentase':
        # a = df_plot.iloc[:,0] *100 / (df_plot.iloc[:,0] + df_plot.iloc[:,1])    #tersedia
        # b = df_plot.iloc[:,1] *100 / (df_plot.iloc[:,0] + df_plot.iloc[:,1])    #terpakai
        a = (df_plot.iloc[:,0]-df_plot.iloc[:,1]) *100 / (df_plot.iloc[:,0])    #kosong
        b = df_plot.iloc[:,1] *100 / (df_plot.iloc[:,0])    #terpakai
        try:
            df_plot.iloc[:,0] = a
            df_plot.iloc[:,1] = b
        except Exception:
            pass
        df_plot.fillna(0)

    selected_ruang = []
    for state in filter_ketersediaan:
        try:
            selected_ruang += filter_ruangan[state]
        except Exception:
            pass
    df_plot = df_plot[selected_ruang]
    df_plot = df_plot.rename(columns=rename_columns)

    if axis_mode == 'Persentase':
        header_list = df_plot.columns.values.tolist()
        rename_columns = {}
        for header_name in header_list:
            rename_columns[header_name] = f'{header_name} (persen)'
        df_plot = df_plot.rename(columns=rename_columns)

    df_plot=df_plot.rename(columns={'Tersedia (persen)':'Kosong (persen)'})
    st_element.line_chart(df_plot)
    # st_element.write(df_plot)
    df_list = []
    if 'Terpakai' in df_plot.columns:
        df_plot_terpakai_max = max(df_plot['Terpakai'])
        df_plot_terpakai_max_date = df_plot[df_plot['Terpakai'] == df_plot_terpakai_max].index.tolist()[0].strftime('%d %b %Y')
        df_plot_terpakai_min = min(df_plot['Terpakai'])
        df_plot_terpakai_min_date = df_plot[df_plot['Terpakai'] == df_plot_terpakai_min].index.tolist()[0].strftime('%d %b %Y')
        # st_element.write(
        #     f'Kamar terpakai maksimum sejumlah {df_plot_terpakai_max} pada {df_plot_terpakai_max_date}'
        # )
        # st_element.write(
        #     f'Kamar terpakai minimum sejumlah {df_plot_terpakai_min} pada {df_plot_terpakai_min_date}'
        # )
        df_tmp = pd.DataFrame({
            'Ketersediaan': ['Terpakai'],
            'Tanggal Maksimum': [df_plot_terpakai_max_date],
            'Maksimum': [df_plot_terpakai_max],
            'Tanggal Minimum': [df_plot_terpakai_min_date],
            'Minimum': [df_plot_terpakai_min],
            'Selisih': [abs(int(df_plot_terpakai_max) - int(df_plot_terpakai_min))],
        })
        df_list.append(df_tmp)
    if 'Terpakai (persen)' in df_plot.columns:
        df_plot_terpakai_max = max(df_plot['Terpakai (persen)'])
        df_plot_terpakai_max_date = df_plot[df_plot['Terpakai (persen)'] == df_plot_terpakai_max].index.tolist()[0].strftime('%d %b %Y')
        df_plot_terpakai_min = min(df_plot['Terpakai (persen)'])
        df_plot_terpakai_min_date = df_plot[df_plot['Terpakai (persen)'] == df_plot_terpakai_min].index.tolist()[0].strftime('%d %b %Y')
        # st_element.write(
        #     f'Kamar terpakai maksimum sejumlah {df_plot_terpakai_max:.2f}% pada {df_plot_terpakai_max_date}'
        # )
        # st_element.write(
        #     f'Kamar terpakai minimum sejumlah {df_plot_terpakai_min:.2f}% pada {df_plot_terpakai_min_date}'
        # )
        df_tmp = pd.DataFrame({
            'Ketersediaan': ['Terpakai (persen)'],
            'Tanggal Maksimum': [df_plot_terpakai_max_date],
            'Maksimum': [df_plot_terpakai_max],
            'Tanggal Minimum': [df_plot_terpakai_min_date],
            'Minimum': [df_plot_terpakai_min],
            'Selisih': [abs(float(df_plot_terpakai_max) - float(df_plot_terpakai_min))],
        })
        df_list.append(df_tmp)
    if 'Tersedia' in df_plot.columns:
        df_plot_tersedia_max = max(df_plot['Tersedia'])
        df_plot_tersedia_max_date = df_plot[df_plot['Tersedia'] == df_plot_tersedia_max].index.tolist()[0].strftime('%d %b %Y')
        df_plot_tersedia_min = min(df_plot['Tersedia'])
        df_plot_tersedia_min_date = df_plot[df_plot['Tersedia'] == df_plot_tersedia_min].index.tolist()[0].strftime('%d %b %Y')
        # st_element.write(
        #     f'Kamar tersedia maksimum sejumlah {df_plot_tersedia_max} pada {df_plot_tersedia_max_date}'
        # )
        # st_element.write(
        #     f'Kamar tersedia minimum sejumlah {df_plot_tersedia_min} pada {df_plot_tersedia_min_date}'
        # )
        df_tmp = pd.DataFrame({
            'Ketersediaan': ['Tersedia'],
            'Tanggal Maksimum': [df_plot_tersedia_max_date],
            'Maksimum': [df_plot_tersedia_max],
            'Tanggal Minimum': [df_plot_tersedia_min_date],
            'Minimum': [df_plot_tersedia_min],
            'Selisih': [abs(int(df_plot_tersedia_max) - int(df_plot_tersedia_min))],
        })
        df_list.append(df_tmp)
    if 'Kosong (persen)' in df_plot.columns:
        df_plot_tersedia_max = max(df_plot['Kosong (persen)'])
        df_plot_tersedia_max_date = df_plot[df_plot['Kosong (persen)'] == df_plot_tersedia_max].index.tolist()[0].strftime('%d %b %Y')
        df_plot_tersedia_min = min(df_plot['Kosong (persen)'])
        df_plot_tersedia_min_date = df_plot[df_plot['Kosong (persen)'] == df_plot_tersedia_min].index.tolist()[0].strftime('%d %b %Y')
        # st_element.write(
        #     f'Kamar tersedia maksimum sejumlah {df_plot_tersedia_max:.2f}% pada {df_plot_tersedia_max_date}'
        # )
        # st_element.write(
        #     f'Kamar tersedia minimum sejumlah {df_plot_tersedia_min:.2f}% pada {df_plot_tersedia_min_date}'
        # )
        df_tmp = pd.DataFrame({
            'Ketersediaan': ['Kosong (persen)'],
            'Tanggal Maksimum': [df_plot_tersedia_max_date],
            'Maksimum': [df_plot_tersedia_max],
            'Tanggal Minimum': [df_plot_tersedia_min_date],
            'Minimum': [df_plot_tersedia_min],
            'Selisih': [abs(float(df_plot_tersedia_max) - float(df_plot_tersedia_min))],
        })
        df_list.append(df_tmp)

    df_simpul = pd.DataFrame()
    for df_data in df_list:
        df_simpul = df_simpul.append(df_data)
    df_simpul = df_simpul.reset_index()
    df_simpul = df_simpul.drop(columns='index')
    df_simpul.index +=1
    print(df_simpul)
    st_element.write(df_simpul)
    st_element.markdown("""---""")


def plot_ketersediaan_tunggal(kota,data,filter_ruangan,rename_columns,date,st_element=None,axis_mode=None):
    if st_element == None:
        st_element = st
    df_plot = filter_agg(data,filter_ruangan,[kota])
    # st_element.write(df_plot.reset_index())
    c = alt.Chart(df_plot.reset_index()).mark_bar().encode(
        x='tanggal_update:O',
        # y='sum(yield):Q',
        # color='year:N',
        # column='site:N'
    )
    # st_element.write(df_plot)
    df_plot = df_plot.loc[date:date]
    # st_element.write(df_plot)

    if axis_mode == 'Persentase':
        # st_element.write(df_plot)
        # a = df_plot.iloc[:,0] *100 / (df_plot.iloc[:,0] + df_plot.iloc[:,1])
        # b = df_plot.iloc[:,1] *100 / (df_plot.iloc[:,0] + df_plot.iloc[:,1])
        a = (df_plot.iloc[:,0]-df_plot.iloc[:,1]) *100 / (df_plot.iloc[:,0])
        b = df_plot.iloc[:,1] *100 / (df_plot.iloc[:,0])
        if (a[0]<0) or (b[0]<0):
            st_element.write('(Data tidak valid)')
            st_element.markdown("""---""")
            return
        # st_element.write(a)
        # st_element.write(b)
        try:
            df_plot.iloc[:,0] = a
            df_plot.iloc[:,1] = b
        except Exception:
            pass
        df_plot.fillna(0)

    selected_ruang = []
    for state in filter_ketersediaan:
        try:
            selected_ruang += filter_ruangan[state]
        except Exception:
            pass
    df_plot = df_plot[selected_ruang]
    df_plot = df_plot.rename(columns=rename_columns)

    if axis_mode == 'Persentase':
        header_list = df_plot.columns.values.tolist()
        rename_columns = {}
        for header_name in header_list:
            rename_columns[header_name] = f'{header_name} (persen)'
        df_plot = df_plot.rename(columns=rename_columns)

    # st_element.bar_chart(df_plot.iloc[0])
    df_plot = df_plot.reset_index().rename(columns={'tanggal_update': 'Tanggal'})
    try:
        df_alt = pd.DataFrame({
            'Tanggal': [df_plot.iloc[0]['Tanggal'], df_plot.iloc[0]['Tanggal']],
            'Jumlah': [df_plot.iloc[0]['Terpakai'], df_plot.iloc[0]['Tersedia']],
            'Ketersediaan': ['Terpakai','Kosong']
        })
    except KeyError:
        tmp_terpakai = df_plot.iloc[0]['Terpakai (persen)']
        tmp_tersedia = df_plot.iloc[0]['Tersedia (persen)']
        df_alt = pd.DataFrame({
            'Tanggal': [df_plot.iloc[0]['Tanggal'], df_plot.iloc[0]['Tanggal']],
            'Jumlah': [df_plot.iloc[0]['Terpakai (persen)'], df_plot.iloc[0]['Tersedia (persen)']],
            'Ketersediaan': [f'Terpakai: {tmp_terpakai:.2f}%',f'Kosong: {tmp_tersedia:.2f}%']
        })
    # st_element.write(df_plot)
    # st_element.write(df_alt)
    if df_alt.iloc[0]['Jumlah'] > 0 or df_alt.iloc[1]['Jumlah'] > 0:
        if axis_mode == 'Absolut':
            c = alt.Chart(df_alt).mark_bar().encode(
                x=alt.X('Ketersediaan', scale=alt.Scale(), title=None, ),
                y=alt.Y('Jumlah', title='Jumlah'),
                color=alt.Color('Ketersediaan',legend=None),
            ).properties(
                width=500,
                height=400,
            )
            st_element.altair_chart(c,use_container_width=False)
        elif axis_mode == 'Persentase':
            # st_element.write(df_alt)
            c = alt.Chart(df_alt).mark_arc().encode(
                theta=alt.Theta(field="Jumlah", type="quantitative"),
                color=alt.Color(field="Ketersediaan", type="nominal"),
            )
            st_element.altair_chart(c,use_container_width=True)
    else:
        date_selected = df_alt.iloc[0]['Tanggal'].strftime('%Y/%m/%d')
        st_element.markdown(f'**(Data belum tersedia pada {date_selected})**')
    st_element.markdown("""---""")

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
icu_negpres_vent_filter = {
    'Tersedia':['icu_tekanan_negatif_dengan_ventilator_tersedia',],
    'Terpakai':['icu_tekanan_negatif_dengan_ventilator_terpakai',]
}
icu_negpres_tanpavent_filter = {
    'Tersedia':['icu_tekanan_negatif_tanpa_ventilator_tersedia',],
    'Terpakai':['icu_tekanan_negatif_tanpa_ventilator_terpakai']
}
icu_tanpanegpres_vent_filter = {
    'Tersedia':['icu_tanpa_tekanan_negatif_dengan_ventilator_tersedia',],
    'Terpakai':['icu_tanpa_tekanan_negatif_dengan_ventilator_terpakai',]
}
icu_tanpanegpres_tanpavent_filter = {
    'Tersedia':['icu_tanpa_tekanan_negatif_tanpa_ventilator_tersedia',],
    'Terpakai':['icu_tanpa_tekanan_negatif_tanpa_ventilator_terpakai',]
}

isolasi_negpres_filter = {
    'Tersedia':['isolasi_tekanan_negatif_tersedia'],
    'Terpakai':['isolasi_tekanan_negatif_terpakai']
}
isolasi_tanpanegpres_filter = {
    'Tersedia':['isolasi_tanpa_tekanan_negatif_tersedia',],
    'Terpakai':['isolasi_tanpa_tekanan_negatif_terpakai',]
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

filter_mode_tanggal = st.sidebar.radio(
    label='Opsi Tanggal',
    options=['Rentang','Tanggal Tunggal'],
)

if filter_mode_tanggal == 'Rentang':
    col1,col2 = st.sidebar.columns(2)
    start_date = col1.date_input('Tanggal awal',value=datetime(2020,10,6),min_value=datetime(2020,10,6),max_value=datetime(2022,3,3))
    end_date = col2.date_input('Tanggal akhir',value=datetime(2022,3,3),min_value=start_date,max_value=datetime(2022,3,3))
else:
    tanggal = st.sidebar.date_input('Tanggal',value=datetime(2020,10,6),min_value=datetime(2020,10,6),max_value=datetime(2022,3,3))

filter_kota = st.sidebar.selectbox(
    label='Kabupaten/Kota',
    options=list_kota,
    index=0,
)
axis_mode = st.sidebar.radio(
    label='Tampilan Nilai Grafik',
    options=['Absolut','Persentase'],
)

if filter_mode_tanggal == 'Rentang':
    filter_ketersediaan = st.sidebar.radio(
        label='Ketersediaan',
        options=['Semua','Terpakai','Tersedia'],
    )
    if filter_ketersediaan == 'Semua':
        filter_ketersediaan = ['Terpakai','Tersedia']
    else:
        filter_ketersediaan = [filter_ketersediaan]
else:
    filter_ketersediaan = ['Terpakai','Tersedia']


## Main content

if filter_mode_tanggal == 'Rentang':
    st.header(f'Ketersediaan Ruang ICU {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write(
        'Ruang Intensive Care Unit (ICU) adalah bagian khusus dari rumah sakit atau fasilitas kesehatan \
        lainnya yang melakukan pelayanan rawat intensif.\n\nInstalasi ini menangani pasien dengan \
        penyakit atau cedera yang parah atau membahayakan nyawa, dengan kebutuhan perawatan terus \
        menerus, pemantauan langsung dengan alat-alat, atau obat-obatan untuk menjaga fungsi tubuh normal.'
        )
    rename_columns={
        'icu_tanpa_tekanan_negatif_dengan_ventilator_tersedia':'Tersedia',
        'icu_tanpa_tekanan_negatif_dengan_ventilator_terpakai':'Terpakai',
        'icu_tanpa_tekanan_negatif_tanpa_ventilator_tersedia':'Tersedia',
        'icu_tanpa_tekanan_negatif_tanpa_ventilator_terpakai':'Terpakai',
        'icu_tekanan_negatif_dengan_ventilator_tersedia':'Tersedia',
        'icu_tekanan_negatif_dengan_ventilator_terpakai':'Terpakai',
        'icu_tekanan_negatif_tanpa_ventilator_tersedia':'Tersedia',
        'icu_tekanan_negatif_tanpa_ventilator_terpakai':'Terpakai',
        }
    col2.write('Bertekanan Negatif, Berventilator')
    plot_ketersediaan(filter_kota,data,icu_negpres_vent_filter,rename_columns,start_date,end_date,col2,axis_mode)
    col2.write('Bertekanan Negatif, tanpa Ventilator')
    plot_ketersediaan(filter_kota,data,icu_negpres_tanpavent_filter,rename_columns,start_date,end_date,col2,axis_mode)

    col2.write('Tanpa Tekanan Negatif, Berventilator')
    plot_ketersediaan(filter_kota,data,icu_tanpanegpres_vent_filter,rename_columns,start_date,end_date,col2,axis_mode)
    col2.write('Tanpa tekanan Negatif, tanpa Ventilator')
    plot_ketersediaan(filter_kota,data,icu_tanpanegpres_tanpavent_filter,rename_columns,start_date,end_date,col2,axis_mode)


    st.header(f'Ketersediaan Ruang Isolasi {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write(
        'Ruang isolasi merupakan area sementara yang diperuntukkan bagi orang suspek terinfeksi \
        untuk mencegah penularan penyakit yang akan menjadi wabah apabila dibiarkan. \n\n Ruang \
        isolasi yang menggunakan tekanan udara negatif digunakan untuk pasien yang terinfeksi \
        lewat udara. Dengan tekanan negatif ini, udara dari dalam ruang isolasi yang mungkin \
        mengandung kuman penyebab infeksi tidak keluar dan mengontaminasi udara luar.'
        )
    rename_columns={
        'isolasi_tekanan_negatif_tersedia':'Tersedia',
        'isolasi_tekanan_negatif_terpakai':'Terpakai',
        'isolasi_tanpa_tekanan_negatif_tersedia':'Tersedia',
        'isolasi_tanpa_tekanan_negatif_terpakai':'Terpakai'
        }
    col2.write('Bertekanan Negatif')
    plot_ketersediaan(filter_kota,data,isolasi_negpres_filter,rename_columns,start_date,end_date,col2,axis_mode)
    col2.write('Tanpa Tekanan Negatif')
    plot_ketersediaan(filter_kota,data,isolasi_tanpanegpres_filter,rename_columns,start_date,end_date,col2,axis_mode)



    st.header(f'Ketersediaan Ruang NICU {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write(
        'Ruangan Neonatal Intensive Care Unit (NICU) adalah ruang perawatan intensif untuk bayi \
        (sampai usia 28 hari) yang memerlukan pengobatan dan perawatan khusus, guna mencegah \
        dan mengobati terjadinya kegagalan organ-organ vital'
    )

    rename_columns={'nicu_covid_terpakai':'Terpakai','nicu_covid_tersedia':'Tersedia'}
    plot_ketersediaan(filter_kota,data,nicu_filter,rename_columns,start_date,end_date,col2,axis_mode)



    st.header(f'Ketersediaan Ruang PICU {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write('Ruang Pediatric Intensive Care Unit (PICU) merupakan ruangan yang melayani perawatan pasien kritis anak-anak')
    rename_columns={'picu_covid_terpakai':'Terpakai','picu_covid_tersedia':'Tersedia'}
    plot_ketersediaan(filter_kota,data,picu_filter,rename_columns,start_date,end_date,col2,axis_mode)


    st.header(f'Ketersediaan Ruang IGD {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write(
        'Ruang Instalasi Gawat Darurat (IGD) adalah salah satu unit dalam rumah sakit yang menyediakan \
        penanganan awal pasien, sesuai dengan tingkat kegawatannya. Di IGD dapat ditemukan dokter umum \
        maupun dokter spesialis bersama sejumlah perawat. \n\nSetelah penaksiran dan penanganan awal, pasien \
        bisa dirujuk ke RS, distabilkan dan dipindahkan ke RS lain karena berbagai alasan, atau dikeluarkan. \
        Kebanyakan UGD buka 24 jam, meski pada malam hari jumlah staf yang ada di sana akan lebih sedikit.'
    )
    rename_columns={'igd_covid_terpakai':'Terpakai','igd_covid_tersedia':'Tersedia'}
    plot_ketersediaan(filter_kota,data,igd_filter,rename_columns,start_date,end_date,col2,axis_mode)

    st.header(f'Ketersediaan Ruang VK {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write(
        'Ruang Verlos Kamer (VK) atau Ruang Bersalin adalah adalah sebuah unit layanan pada rumah sakit \
        yang berfungsi sebagai ruang persalinan. Meskipun persalinan normal dapat dilakukan di Puskesman, \
        Ruang VK juga dapat digunakan untuk persalinan normal pada pasien dengan indikasi tertentu yang \
        tidak dapat ditangani oleh Puskesmas, misalnya yaitu partus tidak maju dan partus dengan hipertensi. \
        Ruang VK juga dapat digunakan pada persiapan persalinan dengan operasi sesar.'
        )
    rename_columns={'vk_covid_terpakai':'Terpakai','vk_covid_tersedia':'Tersedia'}
    plot_ketersediaan(filter_kota,data,vk_filter,rename_columns,start_date,end_date,col2,axis_mode)
elif filter_mode_tanggal == 'Tanggal Tunggal':
    st.header(f'Ketersediaan Ruang ICU {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write(
        'Ruang Intensive Care Unit (ICU) adalah bagian khusus dari rumah sakit atau fasilitas kesehatan \
        lainnya yang melakukan pelayanan rawat intensif.\n\nInstalasi ini menangani pasien dengan \
        penyakit atau cedera yang parah atau membahayakan nyawa, dengan kebutuhan perawatan terus \
        menerus, pemantauan langsung dengan alat-alat, atau obat-obatan untuk menjaga fungsi tubuh normal.'
        )
    rename_columns={
        'icu_tanpa_tekanan_negatif_dengan_ventilator_tersedia':'Tersedia',
        'icu_tanpa_tekanan_negatif_dengan_ventilator_terpakai':'Terpakai',
        'icu_tanpa_tekanan_negatif_tanpa_ventilator_tersedia':'Tersedia',
        'icu_tanpa_tekanan_negatif_tanpa_ventilator_terpakai':'Terpakai',
        'icu_tekanan_negatif_dengan_ventilator_tersedia':'Tersedia',
        'icu_tekanan_negatif_dengan_ventilator_terpakai':'Terpakai',
        'icu_tekanan_negatif_tanpa_ventilator_tersedia':'Tersedia',
        'icu_tekanan_negatif_tanpa_ventilator_terpakai':'Terpakai',
        }
    col2.write('Bertekanan Negatif, Berventilator')
    plot_ketersediaan_tunggal(filter_kota,data,icu_negpres_vent_filter,rename_columns,tanggal,col2,axis_mode)
    col2.write('Bertekanan Negatif, tanpa Ventilator')
    plot_ketersediaan_tunggal(filter_kota,data,icu_negpres_tanpavent_filter,rename_columns,tanggal,col2,axis_mode)

    col2.write('Tanpa Tekanan Negatif, Berventilator')
    plot_ketersediaan_tunggal(filter_kota,data,icu_tanpanegpres_vent_filter,rename_columns,tanggal,col2,axis_mode)
    col2.write('Tanpa tekanan Negatif, tanpa Ventilator')
    plot_ketersediaan_tunggal(filter_kota,data,icu_tanpanegpres_tanpavent_filter,rename_columns,tanggal,col2,axis_mode)


    st.header(f'Ketersediaan Ruang Isolasi {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write(
        'Ruang isolasi merupakan area sementara yang diperuntukkan bagi orang suspek terinfeksi \
        untuk mencegah penularan penyakit yang akan menjadi wabah apabila dibiarkan. \n\n Ruang \
        isolasi yang menggunakan tekanan udara negatif digunakan untuk pasien yang terinfeksi \
        lewat udara. Dengan tekanan negatif ini, udara dari dalam ruang isolasi yang mungkin \
        mengandung kuman penyebab infeksi tidak keluar dan mengontaminasi udara luar.'
        )
    rename_columns={
        'isolasi_tekanan_negatif_tersedia':'Tersedia',
        'isolasi_tekanan_negatif_terpakai':'Terpakai',
        'isolasi_tanpa_tekanan_negatif_tersedia':'Tersedia',
        'isolasi_tanpa_tekanan_negatif_terpakai':'Terpakai'
        }
    col2.write('Bertekanan Negatif')
    plot_ketersediaan_tunggal(filter_kota,data,isolasi_negpres_filter,rename_columns,tanggal,col2,axis_mode)
    col2.write('Tanpa Tekanan Negatif')
    plot_ketersediaan_tunggal(filter_kota,data,isolasi_tanpanegpres_filter,rename_columns,tanggal,col2,axis_mode)



    st.header(f'Ketersediaan Ruang NICU {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write(
        'Ruangan Neonatal Intensive Care Unit (NICU) adalah ruang perawatan intensif untuk bayi \
        (sampai usia 28 hari) yang memerlukan pengobatan dan perawatan khusus, guna mencegah \
        dan mengobati terjadinya kegagalan organ-organ vital'
    )

    rename_columns={'nicu_covid_terpakai':'Terpakai','nicu_covid_tersedia':'Tersedia'}
    plot_ketersediaan_tunggal(filter_kota,data,nicu_filter,rename_columns,tanggal,col2,axis_mode)



    st.header(f'Ketersediaan Ruang PICU {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write('Ruang Pediatric Intensive Care Unit (PICU) merupakan ruangan yang melayani perawatan pasien kritis anak-anak')
    rename_columns={'picu_covid_terpakai':'Terpakai','picu_covid_tersedia':'Tersedia'}
    plot_ketersediaan_tunggal(filter_kota,data,picu_filter,rename_columns,tanggal,col2,axis_mode)


    st.header(f'Ketersediaan Ruang IGD {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write(
        'Ruang Instalasi Gawat Darurat (IGD) adalah salah satu unit dalam rumah sakit yang menyediakan \
        penanganan awal pasien, sesuai dengan tingkat kegawatannya. Di IGD dapat ditemukan dokter umum \
        maupun dokter spesialis bersama sejumlah perawat. \n\nSetelah penaksiran dan penanganan awal, pasien \
        bisa dirujuk ke RS, distabilkan dan dipindahkan ke RS lain karena berbagai alasan, atau dikeluarkan. \
        Kebanyakan UGD buka 24 jam, meski pada malam hari jumlah staf yang ada di sana akan lebih sedikit.'
    )
    rename_columns={'igd_covid_terpakai':'Terpakai','igd_covid_tersedia':'Tersedia'}
    plot_ketersediaan_tunggal(filter_kota,data,igd_filter,rename_columns,tanggal,col2,axis_mode)

    st.header(f'Ketersediaan Ruang VK {filter_kota}')
    col1,col2 = st.columns(colsize)
    col1.write(
        'Ruang Verlos Kamer (VK) atau Ruang Bersalin adalah adalah sebuah unit layanan pada rumah sakit \
        yang berfungsi sebagai ruang persalinan. Meskipun persalinan normal dapat dilakukan di Puskesman, \
        Ruang VK juga dapat digunakan untuk persalinan normal pada pasien dengan indikasi tertentu yang \
        tidak dapat ditangani oleh Puskesmas, misalnya yaitu partus tidak maju dan partus dengan hipertensi. \
        Ruang VK juga dapat digunakan pada persiapan persalinan dengan operasi sesar.'
        )
    rename_columns={'vk_covid_terpakai':'Terpakai','vk_covid_tersedia':'Tersedia'}
    plot_ketersediaan_tunggal(filter_kota,data,vk_filter,rename_columns,tanggal,col2,axis_mode)
