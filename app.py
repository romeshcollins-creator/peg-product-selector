import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="PEG Product Selector",
    layout="wide"
)

st.title("Interactive PEG Product Selector")
st.caption("Conceptual demo using publicly available PEG product attributes")

# Load CSV
@st.cache_data
def load_data():
    return pd.read_csv("peg_products_fixed.csv")

df = load_data()

# ---------------- FILTERS ----------------
st.sidebar.header("Filter PEG Products")

mw_min, mw_max = st.sidebar.slider(
    "Molecular Weight (kDa)",
    float(df["Molecular Weight (kDa)"].min()),
    float(df["Molecular Weight (kDa)"].max()),
    (
        float(df["Molecular Weight (kDa)"].min()),
        float(df["Molecular Weight (kDa)"].max())
    )
)

reactivity = st.sidebar.multiselect(
    "Functional Group / Reactivity",
    sorted(df["Functional Group / Reactivity"].unique())
)

architecture = st.sidebar.multiselect(
    "Polymer Architecture",
    sorted(df["Polymer Architecture"].unique())
)

solubility = st.sidebar.multiselect(
    "Solubility",
    sorted(df["Solubility"].unique())
)

application = st.sidebar.multiselect(
    "Intended Application",
    sorted(df["Intended Application"].unique())
)

# ---------------- APPLY FILTERS ----------------
filtered = df[
    (df["Molecular Weight (kDa)"] >= mw_min) &
    (df["Molecular Weight (kDa)"] <= mw_max)
]

if reactivity:
    filtered = filtered[filtered["Functional Group / Reactivity"].isin(reactivity)]

if architecture:
    filtered = filtered[filtered["Polymer Architecture"].isin(architecture)]

if solubility:
    filtered = filtered[filtered["Solubility"].isin(solubility)]

if application:
    filtered = filtered[filtered["Intended Application"].isin(application)]

# ---------------- RESULTS ----------------
st.subheader(f"{len(filtered)} PEG products match your criteria")

for _, row in filtered.iterrows():
    with st.expander(f"{row['Product Name']}  |  {row['Molecular Weight (kDa)']} kDa"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Commercial Partner:** {row['Commercial Partner']}")
            st.markdown(f"**Functional Group:** {row['Functional Group / Reactivity']}")
            st.markdown(f"**Polymer Architecture:** {row['Polymer Architecture']}")
            st.markdown(f"**Solubility:** {row['Solubility']}")

        with col2:
            st.markdown(f"**Intended Application:** {row['Intended Application']}")
            st.markdown(f"**PDI:** {row['Polydispersity Index (PDI)']}")
            st.markdown(f"**Application Notes:** {row['Application']}")
