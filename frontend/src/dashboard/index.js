import React, { useState } from 'react';
import { Copy, Link2, Check, Trash2, ExternalLink } from 'lucide-react';
import axios from "axios"
import './index.css';

const DashBoard = () => {
  // Static sample data for UI display
  const [url, setUrl] = useState("")
  const [sampleUrls, setListUrl] = useState([])
  const [show, setShow] = useState(false)

  const onClickSubmitBtn = async (e) => {
    e.preventDefault()
    const { data } = await axios.post("https://url-shortener-9ql5.onrender.com/api/shorten", { url })
    setListUrl(data)
    setShow(!show)
    console.log(data)
  }
  console.log(sampleUrls.original_url)
  return (
    <div className="app">
      <div className="background-animation"></div>

      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="logo">
            <Link2 className="logo-icon" />
            <h1>LinkShort</h1>
          </div>
          <p className="subtitle">Transform long URLs into short, shareable links</p>
        </header>

        {/* URL Shortening Form */}
        <div className="main-card">
          <form className="url-form">
            <div className="input-group">
              <input
                type="text"
                defaultValue=""
                placeholder="Enter your long URL here..."
                className="url-input"
                onChange={(e) => setUrl(e.target.value)}
              />
              <button
                type="submit"
                className="shorten-btn"
                onClick={onClickSubmitBtn}
              >
                Shorten URL
              </button>
            </div>
          </form>
        </div>

        {/* Results */}
        {show && (<div className="results-section">
          <h2 className="results-title">Your Shortened URLs</h2>
          <div className="results-grid">
            <div className="result-card">
              <div className="result-header">
                <div className="url-info">
                  <p className="original-url">{sampleUrls.original_url}</p>
                  <div className="short-url-container">
                    <a
                      href={sampleUrls.short_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="short-url"
                    >
                      {sampleUrls.short_url}
                    </a>
                    <ExternalLink className="external-icon" />
                  </div>
                </div>
                <div className="result-actions">
                  <button
                    className="copy-btn"
                    title="Copy to clipboard"
                  >
                    <Copy className="action-icon" />
                  </button>
                  <button
                    className="delete-btn"
                    title="Delete URL"
                  >
                    <Trash2 className="action-icon" />
                  </button>
                </div>
              </div>
              <div className="result-footer">
                {/* <span className="clicks">{item.clicks} clicks</span> */}
                {/* <span className="date">
                  {item.createdAt.toLocaleDateString()}
                </span> */}
              </div>
            </div>
          </div>
        </div>)}


        {/* Features Section */}
        <div className="features">
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Lightning Fast</h3>
            <p>Generate short URLs in milliseconds</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Track Clicks</h3>
            <p>Monitor your link performance</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3>Secure Links</h3>
            <p>Safe and reliable URL shortening</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DashBoard;