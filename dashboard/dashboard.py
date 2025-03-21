import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

#Memuat data main
try:
    main_df = pd.read_csv("dashboard/main_dataset.csv")
except FileNotFoundError:
    st.error("File main_dataset.csv tidak ditemukan di direktori dashboard/")
    st.stop()

# Konversi kolom ke datetime
main_df['order_purchase_timestamp'] = pd.to_datetime(main_df['order_purchase_timestamp'])

#Sidebar
with st.sidebar:
    st.image("dashboard/logo ecom.png")
    st.header("Filter Rentang Waktu")
    start_date = st.date_input("Tanggal Mulai", main_df['order_purchase_timestamp'].min().date())
    end_date = st.date_input("Tanggal Akhir", main_df['order_purchase_timestamp'].max().date())
    kategori_produk = main_df['product_category_name'].unique().tolist()
    kategori_produk.insert(0, "Semua") # Menambahkan opsi "Semua"
    pilih_kategori = st.selectbox("Pilih Kategori Produk", kategori_produk)

#Filter data berdasarkan rentang waktu
filtered_df = main_df[(main_df['order_purchase_timestamp'].dt.date >= start_date) & (main_df['order_purchase_timestamp'].dt.date <= end_date)]

# Filter data berdasarkan rentang waktu dan kategori
if pilih_kategori == "Semua":
    filtered_df = main_df[(main_df['order_purchase_timestamp'].dt.date >= start_date) & (main_df['order_purchase_timestamp'].dt.date <= end_date)]
else:
    filtered_df = main_df[(main_df['order_purchase_timestamp'].dt.date >= start_date) & (main_df['order_purchase_timestamp'].dt.date <= end_date) & (main_df['product_category_name'] == pilih_kategori)]

#Judul Dashboard
st.header("Dashboard E-Commerce")

#Statistik Skor Review
st.subheader("Statistik Skor Review")

byreview_df = filtered_df.groupby(by="review_score")["review_id"].nunique().reset_index()
byreview_df.rename(columns={"review_id": "review_count"}, inplace=True)

fig_review_stats, ax_review_stats = plt.subplots(figsize=(12, 8))
colors_review_stats = 'steelblue'
sns.barplot(
    y="review_count",
    x="review_score",
    data=byreview_df.sort_values(by="review_count", ascending=False),
    color=colors_review_stats,
    ax=ax_review_stats,
    width=0.5
)
ax_review_stats.set_title("Distribusi Statistik Skor Review", loc="center", fontsize=15)
ax_review_stats.set_ylabel(None)
ax_review_stats.set_xlabel(None)
ax_review_stats.tick_params(axis='x', labelsize=12)

st.pyplot(fig_review_stats)

#Skor review terbanyak
st.subheader("Skor Review dengan Jumlah Nilai Paling Banyak")

counts = filtered_df['review_score'].value_counts()
sorted_index = sorted(counts.index)

fig_highest_review, ax_max_review = plt.subplots(figsize=(10, 6))
max_value_color = 'steelblue'
default_color = 'skyblue'
colors = [max_value_color if value == counts.values[0] else default_color for value in counts.values]

ax_max_review.barh(counts.index, counts.values, color=colors)
ax_max_review.set_title('Skor Review dengan Jumlah Nilai Paling Banyak')
ax_max_review.set_yticks(sorted_index)

for index, value in enumerate(counts.values):
    ax_max_review.text(value + 1, counts.index[index], str(value))

st.pyplot(fig_highest_review)

# Visualisasi Skor Review dengan Jumlah Nilai Paling Sedikit
st.subheader("Skor Review dengan Jumlah Nilai Paling Sedikit")

counts = filtered_df['review_score'].value_counts()
sorted_index = sorted(counts.index)

fig_lowest_review, ax_lowest_review = plt.subplots(figsize=(12, 6))
min_value_color = 'red'
default_color = 'salmon'
colors_lowest_review = [min_value_color if value == counts.values[-1] else default_color for value in counts.values]

ax_lowest_review.barh(counts.index, counts.values, color=colors_lowest_review)
ax_lowest_review.set_title('Skor Review dengan Jumlah Nilai Paling Sedikit')
ax_lowest_review.set_yticks(sorted_index)

for index, value in enumerate(counts.values):
    ax_lowest_review.text(value + 1, counts.index[index], str(value))

st.pyplot(fig_lowest_review)

#Tren Penjualan Tahun ke Tahun
#Visualisasi data order_purchase_timestamp
filtered_df['year'] = filtered_df['order_purchase_timestamp'].dt.year

sales_by_year = filtered_df['year'].value_counts().sort_index()

st.subheader("Tren Penjualan dari Tahun ke Tahun")

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(sales_by_year.index, sales_by_year.values, marker='o')
ax.set_title('Tren Penjualan dari Tahun ke Tahun')
ax.set_xticks(sales_by_year.index)

st.pyplot(fig)

#Karena memang kategorinya terlalu banyak, hanya akan mengambil 5 kategori dari yang paling banyak terjual dan paling sedikit terjual.
category_counts = filtered_df['product_category_name'].value_counts()

#5 kategori teratas dan terbawah
top_5 = category_counts.head(5)
bottom_5 = category_counts.tail(5)

#Visualisasi 5 kategori paling banyak terjual
st.subheader("5 Kategori Produk Paling Banyak Terjual")
fig_top, ax_top = plt.subplots(figsize=(12, 6))
sns.barplot(x=top_5.values, y=top_5.index, color='steelblue', ax=ax_top)
ax_top.set_xlabel('Jumlah Pesanan')
ax_top.set_ylabel('Kategori Produk')

st.pyplot(fig_top)

#Visualisasi 5 Kategori paling sedikit terjual
st.subheader("5 Kategori Produk Paling Sedikit Terjual")
fig_bottom, ax_bottom = plt.subplots(figsize=(12, 6))
sns.barplot(x=bottom_5.values, y=bottom_5.index, color='salmon', ax=ax_bottom)
ax_bottom.set_xlabel('Jumlah Pesanan')
ax_bottom.set_ylabel('Kategori Produk')

st.pyplot(fig_bottom)