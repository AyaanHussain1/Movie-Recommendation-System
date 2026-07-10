# Movie Recommendation System

🔗 Live Demo: [https://movie-recommendation-system-md.streamlit.app/]

A content-based movie recommendation web app that suggests similar movies based on genre, cast, crew, and plot, using the TMDB 5000 movie dataset.

## Overview

Instead of relying on other users' ratings (collaborative filtering), this system recommends movies purely based on their **content** — combining each movie's overview, genres, keywords, top cast, and director/crew into a single "tag" profile, then finding the most similar movies using text vectorization and cosine similarity. The app lets a user pick any movie from the dataset and instantly see 5 similar titles with posters, fetched live from the TMDB API.

## How It Works

1. **Data** — Merged two TMDB datasets on movie title: `tmdb_5000_movies` (metadata: genres, keywords, overview) and `tmdb_5000_credits` (cast and crew), covering 4,803 movies.
2. **Feature Extraction** — Parsed the nested JSON-like fields (`genres`, `keywords`, `cast`, `crew`) using `ast.literal_eval`, extracting genre names, the top 3 cast members, and crew department/name pairs.
3. **Tag Construction** — Combined the overview, genres, keywords, cast, and crew into a single text "tag" per movie, lowercased, and applied **Porter stemming** (e.g. "acting", "actor" → "act") to normalize word forms.
4. **Vectorization** — Converted the tags into numerical vectors using `CountVectorizer` (bag-of-words, top 5000 features, English stop words removed).
5. **Similarity Computation** — Calculated pairwise **cosine similarity** between all movie vectors, producing a similarity matrix used to find each movie's closest matches.
6. **Recommendation Logic** — For a selected movie, sorts all other movies by similarity score and returns the top 5 closest matches.
7. **Deployment** — Built a Streamlit app that loads the precomputed movie data and similarity matrix, lets a user select a movie from a dropdown, and displays 5 recommended movies with posters fetched live from the TMDB API.

## Tech Stack

- **Language:** Python
- **Data Handling:** Pandas, NumPy
- **NLP/Text Processing:** NLTK (Porter Stemmer), Scikit-learn (CountVectorizer)
- **Similarity:** Scikit-learn (cosine similarity)
- **External API:** TMDB API (movie poster fetching)
- **App/Deployment:** Streamlit

## Project Structure

```
movie-recommendation-system/
├── recommendation_script.py   # Data merging, feature extraction, tag building, model creation
├── main.py                     # Streamlit web app (deployed entry point)
├── movies.pkl                  # Preprocessed movie data (title, tags, id)
├── similarity.pkl              # Precomputed cosine similarity matrix
└── requirements.txt            # Python dependencies
```

Note: the raw datasets (`tmdb_5000_movies.xls`, `tmdb_5000_credits.csv`) are not included in this repo due to size — they're only needed to regenerate `movies.pkl` and `similarity.pkl`, not to run the deployed app. The original dataset is publicly available on Kaggle as the "TMDB 5000 Movie Dataset."

## Installation & Usage

```bash
# Clone the repository
git clone https://github.com/AyaanHussain1/movie-recommendation-system.git
cd movie-recommendation-system

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
```

## Results

The system successfully reduces 4,803 movies into a content-based similarity space, returning relevant, thematically-similar recommendations (matching genre, cast, or narrative tone) in real time.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This project is built for educational and portfolio purposes, using the publicly available TMDB 5000 dataset. Movie posters are fetched live via the TMDB API.
