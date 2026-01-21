import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

#Membuat Judul
st.title("Catatan Keuangan")
st.markdown("Masukkan Rincian Keuangan Anda")

#Membuat Koneksi Ke GSheets
conn = st.connection("gsheets", type=GSheetsConnection)

#Koneksikan Table Dalam Gsheets
existing_data = conn.read(worksheet="Catatan", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

#List Jenis Tabungan dan Bank
tabungan =[
    "Tabungan",
    "Giro",
    "Deposit",
    "Anak",
    "Investasi"
]

bank =[
    "BCA",
    "BRI",
    "BNI",
    "Mandiri",
]

#Window Form Pengguna Baru
with st.form(key="Form Pengguna"):
    nama_pengguna = st.text_input(label="Nama pengguna*")
    jenis_tabungan = st.selectbox("Jenis Tabungan", options=tabungan, index=None)
    bank_tujuan = st.selectbox("Bank Yang Dituju", options=bank, index=None)
    nominal_tabungan = st.text_input("Nominal Bulan Ini")
    tanggal_input = st.date_input(label="Tanggal Hari Ini")
    info_tambahan = st.text_area(label="Informasi")

    st.markdown("**Diperlukan*")

    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        #Cek Ketentuan Form
        if not nama_pengguna or not jenis_tabungan:
            st.warning("Data Belum Lengkap")
            st.stop()
        elif existing_data["Nama Pengguna"].str.contains(nama_pengguna).any():
            st.warning("Nama Sudah Terdaftar")
            st.stop()
        else:
            #Membuat kolom baru pada data Gsheet
            data_pengguna = pd.DataFrame(
                [
                    {
                        "Nama Pengguna": nama_pengguna,
                        "Jenis Tabungan": jenis_tabungan,
                        "Bank": bank_tujuan,
                        "Nominal": nominal_tabungan,
                        "Tanggal": tanggal_input.strftime("%Y-%m-%d"),
                        "Info Tambahan": info_tambahan,
                    }
                ]
            )

            update_data = pd.concat([existing_data, data_pengguna], ignore_index=True)

            #Koneksikan GSheet dengan data form
            conn.update(worksheet="Catatan", data=update_data)

            st.success("Data Berhasil Ditambahkan")
            st.balloons()