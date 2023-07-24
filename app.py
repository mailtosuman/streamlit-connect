import streamlit as st
import pandas as pd
from supabase import create_client

st.header('Sample App using Supabase and Streamlit!')

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()
# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query():
    return supabase.table("skiratingsapp").select('*').execute()

rows = run_query()
df = pd.DataFrame(rows.data)
# --- STREAMLIT SELECTION
year = df['year'].unique().tolist()

year_selection = st.multiselect('Year of Ski Manufacturing:',
                                    year,
                                    default=year)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['year'].isin(year_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Ski Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['year']).count()[['make']]
df_grouped = df_grouped.rename(columns={'year': 'make'})
df_grouped = df_grouped.reset_index()

st.table(df[mask])

