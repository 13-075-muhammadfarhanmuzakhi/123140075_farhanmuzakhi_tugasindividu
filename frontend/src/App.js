import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const API_URL = "http://localhost:6543/api";

function App() {
  const [reviewText, setReviewText] = useState("");
  const [productName, setProductName] = useState("");
  const [language, setLanguage] = useState("id");
  const [darkMode, setDarkMode] = useState(() => {
    try {
      const initialDark = localStorage.getItem("theme") === "dark";
      if (initialDark) {
        document.body.classList.add("dark");
      }
      return initialDark;
    } catch (e) {
      return false;
    }
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loadingReviews, setLoadingReviews] = useState(false);

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    setLoadingReviews(true);
    try {
      const response = await axios.get(`${API_URL}/reviews`);
      const sortedReviews = response.data.sort(
        (a, b) => new Date(b.created_at) - new Date(a.created_at)
      );
      setReviews(sortedReviews);
    } catch (err) {
      console.error("Error fetching reviews:", err);
    } finally {
      setLoadingReviews(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (reviewText.trim().length < 10) {
      setError("Review harus minimal 10 karakter");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/analyze-review`, {
        product_name: productName.trim() || "Tidak ada nama produk",
        review_text: reviewText,
        language: language,
      });

      setResult(response.data);
      setReviewText("");
      setProductName("");

      fetchReviews();
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Terjadi error saat analisis. Pastikan server backend berjalan."
      );
    } finally {
      setLoading(false);
    }
  };

  // Helper function: Warna Sentimen (Digunakan untuk Inline Style di Result Box)
  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case "positive":
        return "var(--color-positive)";
      case "negative":
        return "var(--color-negative)";
      default:
        return "var(--color-text-medium)";
    }
  };

  // Helper function: Emoji Sentimen
  const getSentimentEmoji = (sentiment) => {
    switch (sentiment) {
      case "positive":
        return "😊";
      case "negative":
        return "😞";
      default:
        return "😐";
    }
  };

  // Helper function: Toggle Dark Mode
  const toggleDarkMode = () => {
    const next = !darkMode;
    setDarkMode(next);
    try {
      localStorage.setItem("theme", next ? "dark" : "light");
    } catch (e) {
      console.error("Local storage error:", e);
    }
    document.body.classList.toggle("dark", next);
  };

  // Helper function: Sentiment Class untuk CSS Styling
  const getSentimentClass = (sentiment) => {
    switch (sentiment) {
      case "positive":
        return "sentiment-positive";
      case "negative":
        return "sentiment-negative";
      default:
        return "sentiment-neutral";
    }
  };

  return (
    <div className={`app-container ${darkMode ? "dark" : ""}`}>
      {/* Minimalist Header */}
      <header className="header">
        <div className="header-inner">
          <h1>Review Analyzer</h1>
          <div className="header-controls">
            <button
              className="theme-toggle"
              onClick={toggleDarkMode}
              aria-label="Toggle dark mode"
            >
              {darkMode ? "☀️" : "🌙"}
            </button>
          </div>
        </div>
      </header>

      <main className="main-content">
        {/* Analysis Form */}
        <section className="form-section">
          <h2>Kirim Review untuk Analisis</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              placeholder="Nama produk (opsional)"
              disabled={loading}
            />

            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              disabled={loading}
              aria-label="Pilih bahasa review"
            >
              <option value="id">Bahasa Indonesia</option>
              <option value="en">English</option>
            </select>

            <textarea
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              placeholder="Masukkan review produk Anda di sini... (minimal 10 karakter)"
              rows="6"
              disabled={loading}
            />

            <button
              type="submit"
              disabled={loading || reviewText.trim().length < 10}
            >
              {loading ? "Menganalisis..." : "Analisis Review"}
            </button>
          </form>

          {error && <div className="error-message">Error: {error}</div>}
        </section>

        {/* Analysis Result */}
        {result && (
          <section className="result-section">
            <h2>Hasil Analisis</h2>
            <div
              className="sentiment-box"
              style={{
                borderLeftColor: getSentimentColor(result.sentiment),
              }}
            >
              <h3>Analisis Sentimen</h3>
              <div className="sentiment-display">
                <span
                  className={`emoji ${getSentimentClass(result.sentiment)}`}
                >
                  {getSentimentEmoji(result.sentiment)}
                </span>
                <span
                  className={`sentiment-label ${getSentimentClass(
                    result.sentiment
                  )}`}
                >
                  {result.sentiment.toUpperCase()}
                </span>
              </div>
              <div className="confidence">
                Kepercayaan: {(result.confidence_score * 100).toFixed(2)}%
              </div>
            </div>

            <div className="key-points-box">
              <h3>Poin Penting (Insights)</h3>
              <div className="key-points-content">{result.key_points}</div>
            </div>

            <div className="review-text-box">
              <h3>Teks Review Asli</h3>
              {result.product_name && (
                <p className="review-product">Produk: {result.product_name}</p>
              )}
              <p className="review-language">
                Bahasa:{" "}
                {result.language === "en" ? "English" : "Bahasa Indonesia"}
              </p>
              <p className="review-text">{result.review_text}</p>
            </div>
          </section>
        )}

        {/* Previous Reviews */}
        <section className="reviews-section">
          <h2>Review Sebelumnya ({reviews.length})</h2>
          {loadingReviews ? (
            <p className="no-reviews-message">Memuat reviews...</p>
          ) : reviews.length === 0 ? (
            <p className="no-reviews-message">
              Belum ada review. Jadilah yang pertama!
            </p>
          ) : (
            <div className="reviews-list">
              {reviews.map((review) => (
                <div key={review.id} className="review-card">
                  <div className="review-header">
                    {/* Menggunakan class untuk styling warna sentimen */}
                    <span
                      className={`review-sentiment ${getSentimentClass(
                        review.sentiment
                      )}`}
                    >
                      <span className="emoji-icon">
                        {getSentimentEmoji(review.sentiment)}
                      </span>
                      {review.sentiment.toUpperCase()}
                    </span>
                    <span className="review-date">
                      {new Date(review.created_at).toLocaleDateString("id-ID", {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                      })}
                    </span>
                  </div>
                  {review.product_name && (
                    <div className="review-product">{review.product_name}</div>
                  )}
                  <div className="review-language-small">
                    Bahasa: {review.language === "en" ? "English" : "Indonesia"}
                  </div>
                  <p className="review-text">{review.review_text}</p>
                  <div className="review-key-points">{review.key_points}</div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
