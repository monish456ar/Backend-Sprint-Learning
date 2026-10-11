export default function HomePage() {
  const apiUiUrl = process.env.NEXT_PUBLIC_API_UI_URL || 'http://localhost:8000/ui/films';

  return (
    <main style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header
        style={{
          padding: '1rem 2rem',
          background: '#111827',
          borderBottom: '1px solid #1f2937',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <div>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#f9fafb' }}>
            Film Review Portal
          </h1>
          <p style={{ fontSize: '0.85rem', color: '#9ca3af' }}>
            Next.js Host Application Embedding FastAPI Server-Rendered UI
          </p>
        </div>
        <div
          style={{
            fontSize: '0.8rem',
            background: '#1f2937',
            padding: '0.35rem 0.75rem',
            borderRadius: '9999px',
            color: '#38bdf8',
          }}
        >
          Embedded: <code>/ui/films</code>
        </div>
      </header>

      <section style={{ flex: 1, padding: '1rem', display: 'flex' }}>
        <iframe
          src={apiUiUrl}
          title="FastAPI Film Search UI"
          style={{
            width: '100%',
            height: 'calc(100vh - 110px)',
            border: '1px solid #1f2937',
            borderRadius: '12px',
            backgroundColor: '#0f172a',
          }}
        />
      </section>
    </main>
  );
}
