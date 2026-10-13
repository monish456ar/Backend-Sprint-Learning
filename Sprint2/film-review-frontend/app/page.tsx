'use client';

import React, { useState, useEffect } from 'react';

interface FilmItem {
  id: string;
  title: string;
  release_year: number;
  genre: string;
  director: string;
}

interface UserProfile {
  username: string;
  role: string;
  token: string;
}

const API_BASE = 'http://localhost:8000';

export default function HomePage() {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [usernameInput, setUsernameInput] = useState('');
  const [passwordInput, setPasswordInput] = useState('');
  const [authError, setAuthError] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);

  // Review Form state
  const [films, setFilms] = useState<FilmItem[]>([]);
  const [selectedFilmId, setSelectedFilmId] = useState('');
  const [rating, setRating] = useState<number>(8);
  const [reviewBody, setReviewBody] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [reviewStatus, setReviewStatus] = useState<{
    type: 'success' | 'error';
    message: string;
    requestId?: string | null;
    processTime?: string | null;
  } | null>(null);

  // Iframe key to trigger reload upon review post
  const [iframeKey, setIframeKey] = useState(1);
  const apiUiUrl = `${API_BASE}/ui/films`;

  // Fetch films for the review dropdown
  const loadFilms = async () => {
    try {
      const res = await fetch(`${API_BASE}/films?page=1&page_size=50`);
      if (res.ok) {
        const data = await res.json();
        const items = data.items || [];
        setFilms(items);
        if (items.length > 0 && !selectedFilmId) {
          setSelectedFilmId(items[0].id);
        }
      }
    } catch (err) {
      console.error('Failed to load films list:', err);
    }
  };

  useEffect(() => {
    loadFilms();
    // Check saved session in localStorage
    const saved = localStorage.getItem('film_review_session');
    if (saved) {
      try {
        setUser(JSON.parse(saved));
      } catch {
        localStorage.removeItem('film_review_session');
      }
    }
  }, []);

  // Handle Login
  const handleLogin = async (e?: React.FormEvent, customUser?: string, customPass?: string) => {
    if (e) e.preventDefault();
    setAuthError('');
    setIsLoggingIn(true);

    const uname = customUser || usernameInput.trim();
    const pword = customPass || passwordInput;

    if (!uname || !pword) {
      setAuthError('Please enter both username and password.');
      setIsLoggingIn(false);
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: jsonEscape({ username: uname, password: pword }),
      });

      const reqId = res.headers.get('x-request-id');
      const timeMs = res.headers.get('x-process-time-ms');

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        setAuthError(errData.detail || errData.message || `Login failed (HTTP ${res.status})`);
        setIsLoggingIn(false);
        return;
      }

      const tokenData = await res.json();
      const accessToken = tokenData.access_token;

      // Fetch user profile (/me)
      const meRes = await fetch(`${API_BASE}/api/v1/me`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      let role = 'user';
      let finalUsername = uname;
      if (meRes.ok) {
        const meData = await meRes.json();
        role = meData.role || 'user';
        finalUsername = meData.username || uname;
      }

      const profile: UserProfile = {
        username: finalUsername,
        role: role.toLowerCase(),
        token: accessToken,
      };

      setUser(profile);
      localStorage.setItem('film_review_session', JSON.stringify(profile));
      setUsernameInput('');
      setPasswordInput('');
      loadFilms();
    } catch (err: any) {
      setAuthError(err.message || 'Network error connecting to API server.');
    } finally {
      setIsLoggingIn(false);
    }
  };

  const handleLogout = () => {
    if (user?.token) {
      fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${user.token}` },
      }).catch(() => {});
    }
    setUser(null);
    localStorage.removeItem('film_review_session');
    setReviewStatus(null);
  };

  // Handle Review Submission
  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    if (!selectedFilmId) {
      setReviewStatus({ type: 'error', message: 'Please select a film.' });
      return;
    }
    if (reviewBody.trim().length < 50) {
      setReviewStatus({
        type: 'error',
        message: `Review text must be at least 50 characters (currently ${reviewBody.trim().length}).`,
      });
      return;
    }

    setIsSubmitting(true);
    setReviewStatus(null);

    try {
      const res = await fetch(`${API_BASE}/films/${selectedFilmId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${user.token}`,
        },
        body: JSON.stringify({
          rating: Number(rating),
          review_body: reviewBody.trim(),
        }),
      });

      const reqId = res.headers.get('x-request-id');
      const processTime = res.headers.get('x-process-time-ms');

      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        const errMsg = errJson.detail || errJson.message || `Failed to submit review (HTTP ${res.status})`;
        setReviewStatus({
          type: 'error',
          message: typeof errMsg === 'string' ? errMsg : JSON.stringify(errMsg),
          requestId: reqId,
          processTime: processTime,
        });
        return;
      }

      const reviewData = await res.json();
      setReviewStatus({
        type: 'success',
        message: `Review created successfully! Background task scheduled to recalculate statistics.`,
        requestId: reqId,
        processTime: processTime,
      });

      setReviewBody('');
      // Reload HTMX iframe to reflect fresh statistics
      setIframeKey((prev) => prev + 1);
    } catch (err: any) {
      setReviewStatus({
        type: 'error',
        message: err.message || 'Network error submitting review.',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  function jsonEscape(data: any) {
    return JSON.stringify(data);
  }

  const isCriticOrAdmin = user && (user.role === 'critic' || user.role === 'admin');

  return (
    <main
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        background: '#09090b',
        color: '#f4f4f6',
        fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      {/* Navigation & Auth Bar */}
      <header
        style={{
          padding: '0.85rem 1.75rem',
          background: 'rgba(18, 19, 24, 0.95)',
          backdropFilter: 'blur(16px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1rem',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: 'linear-gradient(135deg, #a855f7 0%, #6366f1 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 14px rgba(168, 85, 247, 0.4)',
            }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
              <path d="M18 4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4h-4z" />
            </svg>
          </div>
          <div>
            <h1 style={{ fontSize: '1.15rem', fontWeight: 700, margin: 0, letterSpacing: '-0.02em' }}>
              Film Review Portal
            </h1>
            <p style={{ fontSize: '0.75rem', color: '#a1a1aa', margin: 0 }}>
              Sprint 3 Day 4 · Middleware, CORS & Background Tasks
            </p>
          </div>
        </div>

        {/* Auth State in Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <div
                style={{
                  background: 'rgba(255, 255, 255, 0.05)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  padding: '0.35rem 0.85rem',
                  borderRadius: '100px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  fontSize: '0.85rem',
                }}
              >
                <span style={{ color: '#e4e4e7', fontWeight: 600 }}>@{user.username}</span>
                <span
                  style={{
                    fontSize: '0.7rem',
                    textTransform: 'uppercase',
                    fontWeight: 700,
                    letterSpacing: '0.05em',
                    padding: '0.15rem 0.5rem',
                    borderRadius: '100px',
                    background:
                      user.role === 'admin'
                        ? 'rgba(239, 68, 68, 0.2)'
                        : user.role === 'critic'
                        ? 'rgba(168, 85, 247, 0.25)'
                        : 'rgba(59, 130, 246, 0.2)',
                    color:
                      user.role === 'admin'
                        ? '#f87171'
                        : user.role === 'critic'
                        ? '#c084fc'
                        : '#60a5fa',
                    border: `1px solid ${
                      user.role === 'admin'
                        ? 'rgba(239, 68, 68, 0.4)'
                        : user.role === 'critic'
                        ? 'rgba(168, 85, 247, 0.4)'
                        : 'rgba(59, 130, 246, 0.4)'
                    }`,
                  }}
                >
                  {user.role}
                </span>
              </div>
              <button
                onClick={handleLogout}
                style={{
                  background: 'transparent',
                  border: '1px solid rgba(255, 255, 255, 0.15)',
                  color: '#a1a1aa',
                  padding: '0.4rem 0.85rem',
                  borderRadius: '8px',
                  fontSize: '0.8rem',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
                onMouseOver={(e) => (e.currentTarget.style.color = '#ffffff')}
                onMouseOut={(e) => (e.currentTarget.style.color = '#a1a1aa')}
              >
                Sign Out
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
              <input
                type="text"
                placeholder="Username"
                value={usernameInput}
                onChange={(e) => setUsernameInput(e.target.value)}
                style={{
                  background: 'rgba(0,0,0,0.4)',
                  border: '1px solid rgba(255,255,255,0.12)',
                  borderRadius: '8px',
                  color: '#fff',
                  padding: '0.4rem 0.75rem',
                  fontSize: '0.82rem',
                  outline: 'none',
                  width: '120px',
                }}
              />
              <input
                type="password"
                placeholder="Password"
                value={passwordInput}
                onChange={(e) => setPasswordInput(e.target.value)}
                style={{
                  background: 'rgba(0,0,0,0.4)',
                  border: '1px solid rgba(255,255,255,0.12)',
                  borderRadius: '8px',
                  color: '#fff',
                  padding: '0.4rem 0.75rem',
                  fontSize: '0.82rem',
                  outline: 'none',
                  width: '120px',
                }}
              />
              <button
                onClick={() => handleLogin()}
                disabled={isLoggingIn}
                style={{
                  background: 'linear-gradient(135deg, #8b5cf6, #6366f1)',
                  border: 'none',
                  color: '#fff',
                  padding: '0.45rem 1rem',
                  borderRadius: '8px',
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  boxShadow: '0 2px 10px rgba(99, 102, 241, 0.35)',
                }}
              >
                {isLoggingIn ? '...' : 'Sign In'}
              </button>
            </div>
          )}
        </div>
      </header>

      {/* Quick Demo Credentials Banner (when logged out) */}
      {!user && (
        <div
          style={{
            background: 'rgba(24, 24, 27, 0.65)',
            borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
            padding: '0.55rem 1.75rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            fontSize: '0.78rem',
            color: '#71717a',
            flexWrap: 'wrap',
            gap: '0.5rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>Quick Login Presets:</span>
            <button
              onClick={() => handleLogin(undefined, 'critic_1791818885', 'Password123!')}
              style={{
                background: 'rgba(168, 85, 247, 0.15)',
                color: '#c084fc',
                border: '1px solid rgba(168, 85, 247, 0.3)',
                borderRadius: '6px',
                padding: '0.2rem 0.6rem',
                fontSize: '0.75rem',
                cursor: 'pointer',
              }}
            >
              Critic Demo
            </button>
            <button
              onClick={() => handleLogin(undefined, 'monish', 'Password123!')}
              style={{
                background: 'rgba(239, 68, 68, 0.15)',
                color: '#f87171',
                border: '1px solid rgba(239, 68, 68, 0.3)',
                borderRadius: '6px',
                padding: '0.2rem 0.6rem',
                fontSize: '0.75rem',
                cursor: 'pointer',
              }}
            >
              Admin Demo
            </button>
            <button
              onClick={() => handleLogin(undefined, 'sanji', 'Password123!')}
              style={{
                background: 'rgba(59, 130, 246, 0.15)',
                color: '#60a5fa',
                border: '1px solid rgba(59, 130, 246, 0.3)',
                borderRadius: '6px',
                padding: '0.2rem 0.6rem',
                fontSize: '0.75rem',
                cursor: 'pointer',
              }}
            >
              Viewer Demo
            </button>
          </div>
          {authError && <div style={{ color: '#f87171', fontWeight: 500 }}>{authError}</div>}
        </div>
      )}

      {/* Role Notice for Viewers */}
      {user && !isCriticOrAdmin && (
        <div
          style={{
            background: 'rgba(59, 130, 246, 0.08)',
            borderBottom: '1px solid rgba(59, 130, 246, 0.2)',
            padding: '0.65rem 1.75rem',
            fontSize: '0.82rem',
            color: '#93c5fd',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
          }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z" />
          </svg>
          Signed in as <strong>{user.role.toUpperCase()}</strong> (Read-only catalog mode). Review creation form is enabled for Critics and Administrators.
        </div>
      )}

      {/* Create Review Form Section (Visible only to Critics & Admins) */}
      {isCriticOrAdmin && (
        <section
          style={{
            margin: '1rem 1.75rem 0',
            padding: '1.25rem 1.5rem',
            background: 'rgba(18, 19, 24, 0.75)',
            border: '1px solid rgba(168, 85, 247, 0.25)',
            borderRadius: '14px',
            boxShadow: '0 8px 30px rgba(0, 0, 0, 0.4)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <span
                style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: '#a855f7',
                  boxShadow: '0 0 10px #a855f7',
                }}
              />
              <h2 style={{ fontSize: '1rem', fontWeight: 700, margin: 0, color: '#f4f4f6' }}>
                Create Review (Authenticated as {user?.role.toUpperCase()})
              </h2>
            </div>
            <span style={{ fontSize: '0.75rem', color: '#a1a1aa' }}>
              Endpoint: <code>POST /films/{'{film_id}'}/reviews</code>
            </span>
          </div>

          <form onSubmit={handleSubmitReview}>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                gap: '1rem',
                marginBottom: '1rem',
              }}
            >
              {/* Film Dropdown */}
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', color: '#a1a1aa', marginBottom: '0.35rem' }}>
                  Select Film
                </label>
                <select
                  value={selectedFilmId}
                  onChange={(e) => setSelectedFilmId(e.target.value)}
                  style={{
                    width: '100%',
                    background: '#09090b',
                    border: '1px solid rgba(255, 255, 255, 0.15)',
                    borderRadius: '8px',
                    color: '#fff',
                    padding: '0.55rem 0.75rem',
                    fontSize: '0.85rem',
                    outline: 'none',
                  }}
                >
                  {films.map((f) => (
                    <option key={f.id} value={f.id}>
                      {f.title} ({f.release_year}) · {f.genre}
                    </option>
                  ))}
                </select>
              </div>

              {/* Rating Selector */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                  <label style={{ fontSize: '0.8rem', color: '#a1a1aa' }}>Rating (1 - 10)</label>
                  <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#fbbf24' }}>
                    ★ {rating} / 10
                  </span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="10"
                  step="1"
                  value={rating}
                  onChange={(e) => setRating(Number(e.target.value))}
                  style={{
                    width: '100%',
                    accentColor: '#a855f7',
                    cursor: 'pointer',
                  }}
                />
              </div>
            </div>

            {/* Review Body */}
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                <label style={{ fontSize: '0.8rem', color: '#a1a1aa' }}>
                  Review Text (Minimum 50 characters required)
                </label>
                <span
                  style={{
                    fontSize: '0.75rem',
                    color: reviewBody.trim().length >= 50 ? '#34d399' : '#f87171',
                  }}
                >
                  {reviewBody.trim().length} / 50 min characters
                </span>
              </div>
              <textarea
                rows={3}
                placeholder="Share your detailed cinematic review, performance critique, and technical impressions..."
                value={reviewBody}
                onChange={(e) => setReviewBody(e.target.value)}
                style={{
                  width: '100%',
                  background: '#09090b',
                  border: `1px solid ${
                    reviewBody.trim().length >= 50 ? 'rgba(52, 211, 153, 0.4)' : 'rgba(255, 255, 255, 0.15)'
                  }`,
                  borderRadius: '8px',
                  color: '#fff',
                  padding: '0.6rem 0.75rem',
                  fontSize: '0.85rem',
                  outline: 'none',
                  boxSizing: 'border-box',
                  resize: 'vertical',
                }}
              />
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <button
                type="submit"
                disabled={isSubmitting || reviewBody.trim().length < 50}
                style={{
                  background:
                    reviewBody.trim().length >= 50
                      ? 'linear-gradient(135deg, #a855f7, #6366f1)'
                      : 'rgba(255, 255, 255, 0.08)',
                  color: reviewBody.trim().length >= 50 ? '#fff' : '#71717a',
                  border: 'none',
                  borderRadius: '8px',
                  padding: '0.55rem 1.4rem',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  cursor: reviewBody.trim().length >= 50 ? 'pointer' : 'not-allowed',
                  boxShadow:
                    reviewBody.trim().length >= 50 ? '0 4px 14px rgba(168, 85, 247, 0.35)' : 'none',
                }}
              >
                {isSubmitting ? 'Publishing...' : 'Submit Review'}
              </button>

              {reviewStatus && (
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    fontSize: '0.8rem',
                    color: reviewStatus.type === 'success' ? '#34d399' : '#f87171',
                  }}
                >
                  <span>{reviewStatus.message}</span>
                  {reviewStatus.processTime && (
                    <span
                      style={{
                        background: 'rgba(255, 255, 255, 0.06)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        padding: '0.15rem 0.5rem',
                        borderRadius: '4px',
                        color: '#a1a1aa',
                      }}
                    >
                      Duration: {reviewStatus.processTime}ms
                    </span>
                  )}
                  {reviewStatus.requestId && (
                    <span
                      style={{
                        background: 'rgba(255, 255, 255, 0.06)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        padding: '0.15rem 0.5rem',
                        borderRadius: '4px',
                        color: '#c084fc',
                      }}
                    >
                      Req-ID: {reviewStatus.requestId.slice(0, 8)}...
                    </span>
                  )}
                </div>
              )}
            </div>
          </form>
        </section>
      )}

      {/* Untouched HTMX Film Catalog Section */}
      <section style={{ flex: 1, padding: '1rem 1.75rem', display: 'flex', flexDirection: 'column' }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '0.5rem',
          }}
        >
          <span style={{ fontSize: '0.78rem', color: '#71717a' }}>
            Live HTMX Film List (Embedded via FastAPI /ui/films)
          </span>
          <button
            onClick={() => setIframeKey((k) => k + 1)}
            style={{
              background: 'transparent',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              color: '#a1a1aa',
              padding: '0.2rem 0.6rem',
              borderRadius: '6px',
              fontSize: '0.75rem',
              cursor: 'pointer',
            }}
          >
            ↻ Refresh Film List
          </button>
        </div>

        <iframe
          key={iframeKey}
          src={apiUiUrl}
          title="FastAPI Film Search UI"
          style={{
            width: '100%',
            height: isCriticOrAdmin ? 'calc(100vh - 360px)' : 'calc(100vh - 160px)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '16px',
            backgroundColor: '#09090b',
            boxShadow: '0 20px 40px -15px rgba(0, 0, 0, 0.7)',
            transition: 'height 0.2s ease',
          }}
        />
      </section>
    </main>
  );
}
