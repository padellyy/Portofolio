import numpy as np
import streamlit as st
from datasets import load_dataset
from sentence_transformers import CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity

EMB_PATH = "model/movie_embeddings_Hybrid_mBERT_XLM.npy"
FEATURES = {"genres": 0.15, "keywords": 0.20, "production_companies": 0.10}
W_SEM = 0.55
COLS = ["title", "overview", "genres", "keywords", "production_companies", "release_date"]

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")


@st.cache_resource(show_spinner="Loading data and models...")
def load_all():
    df = load_dataset("ada-datadruids/full_tmdb_movies_dataset")["train"].to_pandas()
    df["overview"] = df["overview"].fillna("")
    return df.dropna(subset=["title"]), np.load(EMB_PATH), CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def to_set(x):
    return set(x) if isinstance(x, (list, set)) else set(str(x).split(","))


def jaccard(a, b):
    u = a | b
    return len(a & b) / len(u) if u else 0.0


def fmt(v):
    if isinstance(v, (list, set, tuple, np.ndarray)):
        return ", ".join(map(str, v))
    return "-" if v is None or v != v else str(v)


def recommend(title, k, n):
    m = df[df["title"].str.lower() == title.strip().lower()]
    if m.empty:
        return None
    idx = m["vote_count"].idxmax() if len(m) > 1 else m.index[0]

    sims = cosine_similarity(emb[idx].reshape(1, -1), emb)[0]
    cands = [i for i in sims.argsort()[-k:][::-1] if i != idx]

    cross = cross_model.predict([[df.loc[idx, "overview"], df.loc[c, "overview"]] for c in cands])
    rng = cross.max() - cross.min()
    score = W_SEM * ((cross - cross.min()) / rng if rng > 0 else cross)
    for col, w in FEATURES.items():
        q = to_set(df.loc[idx, col])
        score += w * np.array([jaccard(q, to_set(df.loc[c, col])) for c in cands])

    top = np.argsort(score)[::-1][:n]
    res = df.iloc[[cands[i] for i in top]][COLS].copy()
    res["final_score"] = score[top]
    return df.loc[idx, COLS], res


df, emb, cross_model = load_all()

st.title("🎬 Movie Recommender")
st.caption("Hybrid recommendation: mBERT + XLM embeddings, cross-encoder re-ranking, and metadata similarity.")

with st.sidebar:
    st.header("Settings")
    n = st.slider("Number of recommendations", 1, 20, 5)
    k = st.slider("Retrieval candidates", 50, 1000, 500, step=50)

with st.form("search"):
    title = st.text_input("Movie title", placeholder="e.g. Frozen")
    submitted = st.form_submit_button("Recommend")

if submitted:
    if not title.strip():
        st.warning("Please enter a movie title.")
    else:
        with st.spinner("Finding similar movies..."):
            out = recommend(title, k, n)
        if out is None:
            st.error("Movie not found in the dataset.")
        else:
            q, res = out
            st.subheader(f"Selected movie: {q['title']}")
            st.write(q["overview"])
            st.write(f"**Genres:** {fmt(q['genres'])} | **Release date:** {fmt(q['release_date'])}")
            st.divider()
            st.subheader("Recommendations")
            for rank, (_, r) in enumerate(res.iterrows(), 1):
                with st.container(border=True):
                    left, right = st.columns([4, 1])
                    left.markdown(f"### {rank}. {r['title']}")
                    right.metric("Score", f"{r['final_score']:.3f}")
                    st.write(r["overview"])
                    st.write(f"**Genres:** {fmt(r['genres'])}")
                    st.write(f"**Keywords:** {fmt(r['keywords'])}")
                    st.write(f"**Studios:** {fmt(r['production_companies'])}")
                    st.write(f"**Release date:** {fmt(r['release_date'])}")