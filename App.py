import pickle
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

st. set_page_config(layout="wide")
session = requests.Session()
retries = Retry(total=3, backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

API_KEY = "cda15a923022c46bea490dedfd5db290"

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id: int) -> str:
    tmdb_url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key={API_KEY}&language=en-US"
    )
    try:
        resp = session.get(tmdb_url, timeout = 5)
        resp.raise_for_status()
        data = resp.json()
        poster_path = data.get("poster_path")
        if not poster_path:
            raise ValueError("No poster_path in response")
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception as err:
        st.warning(f"Couldn't load poster for ID {movie_id}: {err}")
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(title: str, topn: int = 5):
    idx = movies_df[movies_df["title"] == title].index[0]
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores.sort(key=lambda x: x[1], reverse=True)
    names, posters = [], []
    for movie_idx, score in sim_scores[1 : topn + 1]:
        m_id = movies_df.iloc[movie_idx].movie_id
        names.append(movies_df.iloc[movie_idx].title)
        posters.append(fetch_poster(m_id))
    return names, posters

st.header("🎬 Movie Recommender System")

movies_df = pickle.load(open("results/movies.pkl", "rb"))
sim_matrix = pickle.load(open("results/cosine_similarity.pkl", "rb"))

selected = st.selectbox(
    "Type or select a movie from the dropdown", movies_df["title"].values
)

if st.button("Show Recommendation"):
    with st.spinner("Scouting for your next binge… 🍿"):
        names, posters = recommend(selected)
        cols = st.columns(len(names))
        for col, name, poster in zip(cols, names, posters):
            col.caption(name)
            col.image(poster, use_container_width = True)