import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# --- 1. Data Loading & Cleanup ---
# We define the function but also call it immediately to ensure 'df' exists
@st.cache_data
def load_data():
    # Read CSV, skipping 4 rows of metadata
    data = pd.read_csv('GDP Data For Countries.csv', skiprows=4)
    data = data.dropna(subset=['Country Name'])

    # Transform to long format
    id_vars = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
    df_long = data.melt(id_vars=id_vars, var_name='Year', value_name='GDP')

    # Cleanup Year and GDP
    df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
    df_long = df_long.dropna(subset=['Year'])
    df_long['GDP_Billions'] = df_long['GDP'] / 1e9

    # Filter for the requested period
    return df_long[(df_long['Year'] >= 1973) & (df_long['Year'] <= 2022)]


# INITIALIZE df HERE
df = load_data()

st.title("GDP Evolution Assignment")

# --- 2. Filtering Logic ---
# Use your renamed variable 'ex_list'
ex_list = [
    'World', 'High income', 'OECD members', 'Post-demographic dividend', 'IDA & IBRD total',
    'Low & middle income', 'Middle income', 'IBRD only', 'East Asia & Pacific',
    'Upper middle income', 'North America', 'Late-demographic dividend',
    'Europe & Central Asia', 'European Union', 'East Asia & Pacific (excluding high income)',
    'East Asia & Pacific (IDA & IBRD countries)', 'Euro area', 'Early-demographic dividend',
    'Lower middle income', 'Latin America & Caribbean', 'Latin America & the Caribbean (IDA & IBRD countries)',
    'Latin America & Caribbean (excluding high income)', 'Europe & Central Asia (IDA & IBRD countries)',
    'Middle East & North Africa', 'South Asia', 'South Asia (IDA & IBRD)',
    'Europe & Central Asia (excluding high income)', 'Arab World', 'IDA total',
    'Sub-Saharan Africa', 'Sub-Saharan Africa (IDA & IBRD countries)',
    'Sub-Saharan Africa (excluding high income)', 'Central Europe and the Baltics',
    'Pre-demographic dividend', 'IDA only', 'Least developed countries: UN classification',
    'Fragile and conflict affected situations', 'Heavily indebted poor countries (HIPC)',
    'Low income', 'Small states', 'Other small states', 'IDA blend', 'Pacific island small states',
    'Caribbean small states', 'Africa Eastern and Southern', 'Africa Western and Central'
]

# Apply the filter - Now 'df' is definitely defined above
df_countries = df[~df['Country Name'].isin(ex_list)]

# Identify Top 20 for the background
df_2022 = df_countries[df_countries['Year'] == 2022].sort_values(by='GDP_Billions', ascending=False)
top_20_list = df_2022['Country Name'].head(20).tolist()

# Highlighted Group
highlight = ['United States', 'China', 'Japan', 'Germany', 'India']
colors = {'United States': '#1f77b4', 'China': '#d62728', 'Japan': '#e377c2', 'Germany': '#333333', 'India': '#2ca02c'}

# --- 3. Visualization ---
fig, ax = plt.subplots(figsize=(14, 8))

# Background Lines
for country in top_20_list:
    c_data = df_countries[df_countries['Country Name'] == country]
    if country not in highlight:
        ax.plot(c_data['Year'], c_data['GDP_Billions'], color='lightgrey', linewidth=1, alpha=0.6)

# Highlighted Lines
for country in highlight:
    c_data = df_countries[df_countries['Country Name'] == country]
    ax.plot(c_data['Year'], c_data['GDP_Billions'], color=colors[country], label=country, linewidth=2.5)
    # Dot at the end
    last = c_data[c_data['Year'] == 2022]
    if not last.empty:
        ax.scatter(2022, last['GDP_Billions'].values[0], color=colors[country], s=40, zorder=5)

# Styling
ax.set_title("Evolution of the 20 Richest Countries GDP over the Past 50 Years", fontsize=16, loc='left',
             fontweight='bold', pad=25)
ax.text(1973, 27500, "Focus on the current 5 richest countries from 1973 to 2022", fontsize=11)
ax.set_xlabel("Year of Record", fontweight='bold')
ax.set_ylabel("GDP (Billions USD)", fontweight='bold')
ax.set_ylim(0, 27000)
ax.set_xlim(1973, 2024)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left')

# Annotation
ax.annotate("During the 2000s,\nChina began experiencing rapid economic growth,\noutpacing all other countries.",
            xy=(2005, 2200), xytext=(1995, 18000),
            arrowprops=dict(facecolor='black', arrowstyle='->', connectionstyle="arc3,rad=0.2"))

plt.figtext(0.1, 0.02, "Source: World Bank - https://databank.worldbank.org/", fontsize=9, color='grey')
st.pyplot(fig)