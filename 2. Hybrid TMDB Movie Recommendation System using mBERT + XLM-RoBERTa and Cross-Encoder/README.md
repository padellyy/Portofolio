A content-based movie recommendation system built on the TMDB dataset. Candidate movies are first retrieved using hybrid mBERT + XLM-RoBERTa (small), then re-ranked by a cross-encoder, and finally scored again with genre, keyword, and studio similarity. The project is served through an interactive Streamlit app.

![App Screenshot](https://drive.google.com/uc?export=view&id=1hPChotzv3ZWmbyfV5xbodiUd7br2emni)

**Dataset**

The system uses [full_tmdb_movies_dataset](https://huggingface.co/datasets/ada-datadruids/full_tmdb_movies_dataset) from Hugging Face, which contains 1,142,342 movies.

**Pipeline**
- **Retrieval:** cosine similarity over the hybrid embeddings shortlists the most similar movies.
- **Re-ranking:** a cross-encoder (`ms-marco-MiniLM-L-6-v2`) compares the overview of each candidate with that of the selected movie.
- **Hybrid scoring:** the semantic score is blended with Jaccard similarity across genres, keywords, and production companies to produce the final ranking.

![testing](https://drive.google.com/uc?export=view&id=19_8hEpLF_aKIkzZCD_Wq8yvlfHrH7tsT)

**Hybrid Embeddings**

The precomputed embeddings (`movie_embeddings_Hybrid_mBERT_XLM.npy`) are too large for GitHub and are hosted on Google Drive:

[Download movie_embeddings_Hybrid_mBERT_XLM.npy](https://drive.google.com/file/d/1tRgL5WMEW3wMJC7ke15i0q_cgQ-cM0C4/view?usp=sharing)

After downloading, place the file in the `model/` folder before running the app:

    model/movie_embeddings_Hybrid_mBERT_XLM.npy

**Run locally**

    pip install -r requirements.txt
    streamlit run deployment.py
