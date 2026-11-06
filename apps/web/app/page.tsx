const modules = [
  ['01', 'Entrepreneur CRM & Admissions', 'Founder intake, applications, interviews and decisions'],
  ['02', 'Facilities & Hub Management', 'Seats, rooms, reservations and maintenance'],
  ['03', 'Programs & Project Management', 'Calls, milestones, budgets and delivery'],
  ['04', 'Startup Development', 'Incubation plans, TRL, teams and fundraising'],
  ['05', 'Events & Community', 'Events, registrations and member engagement'],
  ['06', 'International Relations', 'Partners, agreements and collaboration'],
  ['07', 'Credits & Rewards', 'Benefits, balances and auditable ledger'],
  ['08', 'Investors', 'Investor CRM, introductions and investment rounds'],
  ['09', 'Mentors & Experts', 'Expert directory, matching and assignments'],
  ['10', 'Documents & Compliance', 'Secure files, contracts and privacy workflows'],
  ['11', 'Analytics & Reporting', 'Operational KPIs and exportable reports'],
  ['12', 'Administration & AI', 'Tenant settings, permissions and reviewed AI tools'],
];

export default function Home() {
  return <main className="shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark">S</span><span>StarUB <small>HUB</small></span></div>
      <p className="nav-label">WORKSPACE</p>
      <a className="nav-active" href="#overview">Overview</a>
      <a href="#modules">Hub modules</a>
      <a href="#roadmap">Development roadmap</a>
      <div className="sidebar-foot"><span className="status-dot"/> Foundation workspace</div>
    </aside>
    <section className="content" id="overview">
      <header className="topbar"><div><p className="eyebrow">INNOVATION HUB OPERATING SYSTEM</p><h1>Good morning.</h1><p className="muted">Your ecosystem, connected in one workspace.</p></div><div className="tenant-chip">STARUB · WORKSPACE</div></header>
      <section className="hero"><div><p className="eyebrow light">STARUB HUB PLATFORM</p><h2>Build what’s next.</h2><p>One connected environment for founders, startups, programs and the people who help them grow.</p><a className="hero-link" href="#modules">Explore the platform <span>↗</span></a></div><div className="hero-orbit"><div className="orbit orbit-one"/><div className="orbit orbit-two"/><div className="orbit-core">S</div></div></section>
      <div className="section-heading" id="modules"><div><p className="eyebrow">YOUR ECOSYSTEM</p><h2>Platform modules</h2></div><span className="muted">12 connected domains</span></div>
      <div className="module-grid">{modules.map(([n, title, desc]) => <article className="module-card" key={n}><span className="module-number">{n}</span><h3>{title}</h3><p>{desc}</p><span className="card-arrow">↗</span></article>)}</div>
      <section className="roadmap" id="roadmap"><div><p className="eyebrow">DELIVERY STATUS</p><h2>Foundation first. Scale with confidence.</h2><p className="muted">This repository is at the initial scaffold stage. Authentication, tenant authorization, database migrations and the first CRM workflows are the next implementation milestones.</p></div><div className="roadmap-status"><span className="status-pill">IN FOUNDATION</span><strong>Phase 0</strong><span>Platform foundation</span><div className="progress"><i/></div></div></section>
      <footer>STARUB HUB <span>·</span> Product foundation v0.1 · Not for production use</footer>
    </section>
  </main>;
}
