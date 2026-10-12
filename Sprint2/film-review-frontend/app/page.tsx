export default function HomePage() {
  const apiUiUrl = process.env.NEXT_PUBLIC_API_UI_URL || 'http://localhost:8000/ui/films';

  return (
    <main
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        background: '#09090b',
        color: '#f4f4f6',
      }}
    >
      <header
        style={{
          padding: '0.9rem 2rem',
          background: 'rgba(18, 19, 24, 0.85)',
          backdropFilter: 'blur(12px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div
            style={{
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #a855f7 0%, #6366f1 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 12px rgba(168, 85, 247, 0.35)',
            }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
              <path d="M18 4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4h-4z"/>
            </svg>
          </div>
          <div>
            <h1
              style={{
                fontSize: '1.15rem',
                fontWeight: 700,
                letterSpacing: '-0.02em',
                color: '#f4f4f6',
              }}
            >
              Film Review Portal
            </h1>
            <p style={{ fontSize: '0.8rem', color: '#71717a' }}>
              Next.js Host Application · HTMX Live Embed
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div
            style={{
              fontSize: '0.75rem',
              background: 'rgba(255, 255, 255, 0.04)',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              padding: '0.3rem 0.75rem',
              borderRadius: '9999px',
              color: '#d8b4fe',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
            }}
          >
            <span
              style={{
                width: '6px',
                height: '6px',
                borderRadius: '50%',
                background: '#10b981',
                boxShadow: '0 0 8px #10b981',
              }}
            />
            <code>/ui/films</code>
          </div>
        </div>
      </header>

      <section style={{ flex: 1, padding: '1rem 1.5rem', display: 'flex' }}>
        <iframe
          src={apiUiUrl}
          title="FastAPI Film Search UI"
          style={{
            width: '100%',
            height: 'calc(100vh - 105px)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '16px',
            backgroundColor: '#09090b',
            boxShadow: '0 20px 40px -15px rgba(0, 0, 0, 0.7)',
          }}
        />
      </section>
    </main>
  );
}

