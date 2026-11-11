import React, { useState, useEffect, useRef } from "react";
import {
  Search,
  BookOpen,
  Network,
  CheckCircle,
  ShieldCheck,
  Bookmark,
  Download,
  User,
  LogOut,
  X,
  ChevronRight,
  Sparkles,
  FileText,
  Activity,
  Layers,
  Filter,
  ExternalLink,
  Info
} from "lucide-react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

const PRESETS = [
  { label: "Water Cycle", query: "How does rain support life and nature?", lang: "english" },
  { label: "Astrophysics", query: "Astrophysics and celestial movement", lang: "english" },
  { label: "விண்வெளி (Tamil)", query: "விண்வெளி இயற்பியல்", lang: "tamil" },
  { label: "vinveli (Tanglish)", query: "vinveli iyarpiyal", lang: "tanglish" },
  { label: "Agriculture & Farming", query: "Crop cultivation and soil health", lang: "english" },
  { label: "Preventive Healthcare", query: "Preventive medicine and diagnosis", lang: "english" },
];

const RELATIONSHIP_EXPLANATIONS = {
  DIRECT: "Direct parallel identified between classical verse imagery and modern scientific concept.",
  STRONG_ANALOGY: "Strong structural analogy between classical literature and scientific principles.",
  THEMATIC: "Related by theme or idea, but not evidence of scientific equivalence.",
  METAPHORICAL: "Poetic metaphor depicting natural phenomena.",
  UNSUPPORTED: "Insufficient evidence was found to support the proposed connection."
};

export default function App() {
  const [activeTab, setActiveTab] = useState("explore");
  const [searchQuery, setSearchQuery] = useState("");
  const [searchLang, setSearchLang] = useState("english");
  const [loading, setLoading] = useState(false);
  const [searchResponse, setSearchResponse] = useState(null);
  const [selectedEvidence, setSelectedEvidence] = useState(null);
  const [evidenceTab, setEvidenceTab] = useState("overview");

  // Saved evidence & collections
  const [savedEvidence, setSavedEvidence] = useState([]);
  const [researchNotes, setResearchNotes] = useState("");

  // Auth & User State
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [loginForm, setLoginForm] = useState({ username: "researcher_1", password: "Research@123456" });
  const [loginError, setLoginError] = useState("");

  // Admin & Review Data
  const [adminStats, setAdminStats] = useState(null);
  const [auditLogs, setAuditLogs] = useState([]);
  const [pendingReviews, setPendingReviews] = useState([]);
  const [dbEvidenceRecords, setDbEvidenceRecords] = useState([]);

  useEffect(() => {
    // Initial fetch on mount for all tabs & execute default query
    fetchAdminStats();
    fetchDbEvidenceRecords();
    fetchPendingReviews();
    fetchAuditLogs();
    executeSearch("How does rain support life and nature?", "english");
  }, []);

  useEffect(() => {
    if (token) {
      fetchCurrentUser();
    }
  }, [token]);

  useEffect(() => {
    if (activeTab === "admin") {
      fetchAdminStats();
      fetchAuditLogs();
    } else if (activeTab === "review") {
      fetchPendingReviews();
    } else if (activeTab === "evidence") {
      fetchDbEvidenceRecords();
    }
  }, [activeTab]);

  const fetchCurrentUser = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
      } else {
        handleLogout();
      }
    } catch (err) {
      console.error("Auth check failed:", err);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError("");
    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginForm)
      });
      if (res.ok) {
        const data = await res.json();
        setToken(data.access_token);
        localStorage.setItem("token", data.access_token);
        setUser(data.user);
        setShowLoginModal(false);
      } else {
        const err = await res.json();
        setLoginError(err.detail || "Login failed");
      }
    } catch (err) {
      setLoginError("Could not connect to authentication server");
    }
  };

  const handleLogout = () => {
    setUser(null);
    setToken("");
    localStorage.removeItem("token");
  };

  const executeSearch = async (queryToRun, langToUse) => {
    const q = queryToRun || searchQuery;
    if (!q.trim()) return;

    setLoading(true);

    try {
      const headers = { "Content-Type": "application/json" };
      if (token) headers["Authorization"] = `Bearer ${token}`;

      const res = await fetch(`${API_BASE}/api/v1/search/analyze`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          query: q,
          language: langToUse || searchLang,
          top_k: 5
        })
      });

      if (res.ok) {
        const data = await res.json();
        setSearchResponse(data);

        // Auto-save top evidence item to workspace if empty
        if (data.tamil_evidence && data.tamil_evidence.length > 0) {
          setSavedEvidence((prev) => (prev.length === 0 ? [data.tamil_evidence[0]] : prev));
        }

        // Instantly refresh all tabs so Evidence Repository, Expert Review, System Health, and Audit Logs update!
        fetchDbEvidenceRecords();
        fetchPendingReviews();
        fetchAdminStats();
        fetchAuditLogs();
      } else {
        console.error("Search API error:", res.statusText);
      }
    } catch (err) {
      console.error("Failed to execute search:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAdminStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/statistics`);
      if (res.ok) {
        const data = await res.json();
        setAdminStats(data);
      }
    } catch (err) {
      console.error("Failed to fetch statistics:", err);
    }
  };

  const fetchAuditLogs = async () => {
    if (!token) return;
    try {
      const res = await fetch(`${API_BASE}/api/v1/audit/logs`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setAuditLogs(data.audit_logs || []);
      }
    } catch (err) {
      console.error("Failed to fetch audit logs:", err);
    }
  };

  const fetchPendingReviews = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/v1/reviews/pending`);
      if (res.ok) {
        const data = await res.json();
        setPendingReviews(data.pending_reviews || []);
      }
    } catch (err) {
      console.error("Failed to fetch pending reviews:", err);
    }
  };

  const fetchDbEvidenceRecords = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/v1/evidence/records`);
      if (res.ok) {
        const data = await res.json();
        setDbEvidenceRecords(data.evidence_records || []);
      }
    } catch (err) {
      console.error("Failed to fetch evidence records:", err);
    }
  };

  const handleReviewDecision = async (evidenceId, decision, comments) => {
    if (!token) return;
    try {
      const res = await fetch(`${API_BASE}/api/v1/reviews/submit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          evidence_id: evidenceId,
          status_decision: decision,
          comments: comments || ""
        })
      });
      if (res.ok) {
        fetchPendingReviews();
      }
    } catch (err) {
      console.error("Failed to submit review:", err);
    }
  };

  const toggleSaveEvidence = (item) => {
    const exists = savedEvidence.some((e) => e.source_id === item.source_id);
    if (exists) {
      setSavedEvidence(savedEvidence.filter((e) => e.source_id !== item.source_id));
    } else {
      setSavedEvidence([...savedEvidence, item]);
    }
  };

  const exportReport = async (format) => {
    if (!searchResponse) return;
    try {
      const res = await fetch(`${API_BASE}/api/v1/export/report?format=${format}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchResponse.query })
      });
      if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `research_report.${format}`;
        a.click();
      }
    } catch (err) {
      console.error("Export failed:", err);
    }
  };

  return (
    <div className="app-container">
      {/* Animated Moving Tamil Letters Background */}
      <MovingTamilLettersBackground />

      {/* Navbar Header */}
      <header className="app-header">
        <div className="nav-content">
          <div className="brand-section">
            <div className="brand-icon-box">தமிழ்</div>
            <div className="brand-title-group">
              <h1 className="brand-title">Tamil Literary & Scientific Knowledge Platform</h1>
              <span className="brand-subtitle">Evidence-Aware Cross-Domain Semantic Retrieval & Research</span>
            </div>
          </div>

          <nav className="nav-tabs">
            <button
              className={`nav-tab-btn ${activeTab === "explore" ? "active" : ""}`}
              onClick={() => setActiveTab("explore")}
            >
              <Search size={15} /> Explore
            </button>
            <button
              className={`nav-tab-btn ${activeTab === "workspace" ? "active" : ""}`}
              onClick={() => setActiveTab("workspace")}
            >
              <Bookmark size={15} /> Workspace {savedEvidence.length > 0 && `(${savedEvidence.length})`}
            </button>
            <button
              className={`nav-tab-btn ${activeTab === "evidence" ? "active" : ""}`}
              onClick={() => setActiveTab("evidence")}
            >
              <BookOpen size={15} /> Evidence Repository
            </button>
            <button
              className={`nav-tab-btn ${activeTab === "graph" ? "active" : ""}`}
              onClick={() => setActiveTab("graph")}
            >
              <Network size={15} /> Knowledge Graph
            </button>
            <button
              className={`nav-tab-btn ${activeTab === "review" ? "active" : ""}`}
              onClick={() => setActiveTab("review")}
            >
              <CheckCircle size={15} /> Expert Review
            </button>
            <button
              className={`nav-tab-btn ${activeTab === "admin" ? "active" : ""}`}
              onClick={() => setActiveTab("admin")}
            >
              <Activity size={15} /> System Health
            </button>
          </nav>

          <div className="user-section">
            {user ? (
              <div className="user-badge">
                <div className="avatar-circle">{user.username[0].toUpperCase()}</div>
                <span className="user-name-text">{user.full_name || user.username}</span>
                <button className="btn-secondary" style={{ padding: "4px 8px" }} onClick={handleLogout} title="Log out">
                  <LogOut size={14} />
                </button>
              </div>
            ) : (
              <button className="btn-primary" onClick={() => setShowLoginModal(true)}>
                <User size={15} /> Log In
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Workspace Area */}
      <main className="main-content">
        {/* EXPLORE TAB */}
        {activeTab === "explore" && (
          <div>
            <div className="hero-search-section">
              <h2 className="hero-title">Explore Classical Tamil Literature & Science</h2>
              <p className="hero-subtitle">
                Search modern scientific concepts across Sangam literature (Thirukkural and Thiruvarutpa) using evidence-aligned semantic retrieval.
              </p>

              <div className="search-box-card">
                <div className="search-icon-wrapper">
                  <Search size={20} />
                </div>
                <input
                  type="text"
                  className="main-search-input"
                  placeholder="Ask a scientific question or concept (e.g. Water Cycle, Rain, Gravity)..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && executeSearch()}
                />
                <button
                  className="search-submit-btn"
                  onClick={() => executeSearch()}
                  disabled={loading || !searchQuery.trim()}
                >
                  {loading ? "Analyzing..." : "Search"}
                </button>
              </div>

              <div className="search-presets-bar">
                <span className="preset-label">Suggested Research Queries:</span>
                {PRESETS.map((p, idx) => (
                  <button
                    key={idx}
                    className="preset-chip"
                    onClick={() => {
                      setSearchQuery(p.query);
                      setSearchLang(p.lang);
                      executeSearch(p.query, p.lang);
                    }}
                  >
                    {p.label}
                  </button>
                ))}
              </div>

              {/* Hero Dashboard Stats Bar */}
              <div className="hero-stats-bar">
                <div className="hero-stat-item">
                  <span className="hero-stat-val">1,330</span>
                  <span className="hero-stat-lbl">Thirukkural Verses</span>
                </div>
                <div className="hero-stat-divider" />
                <div className="hero-stat-item">
                  <span className="hero-stat-val">4,000+</span>
                  <span className="hero-stat-lbl">Sangam Stanzas</span>
                </div>
                <div className="hero-stat-divider" />
                <div className="hero-stat-item">
                  <span className="hero-stat-val">4D</span>
                  <span className="hero-stat-lbl">Multidimensional Engine</span>
                </div>
                <div className="hero-stat-divider" />
                <div className="hero-stat-item">
                  <span className="hero-stat-val">Empirical</span>
                  <span className="hero-stat-lbl">Scientific Evidence</span>
                </div>
              </div>
            </div>

            {/* Detected Concept Bar */}
            {searchResponse && (
              <div className="detected-concept-bar">
                <div className="concept-info">
                  <span className="concept-tag">Concept Identified</span>
                  <span className="concept-name-str">{searchResponse.normalized_concept}</span>
                  {searchResponse.scientific_domains?.length > 0 && (
                    <span className="concept-domain-str">• {searchResponse.scientific_domains.join(", ")}</span>
                  )}
                </div>
                <div className="processing-time-badge">
                  Processed in {searchResponse.processing_time_ms} ms
                </div>
              </div>
            )}

            {/* Results Grid */}
            {searchResponse && (
              <div className="results-grid">
                <div className="results-list-column">
                  {/* Interactive 4D Multidimensional Analysis Pipeline */}
                  <DimensionalAnalysisView dimensionalAnalysis={searchResponse.dimensional_analysis} />

                  <div className="section-header-title">
                    <span>Retrieved Literary Evidence ({searchResponse.tamil_evidence?.length || 0})</span>
                    <span style={{ fontSize: "0.82rem", fontWeight: "normal", color: "var(--text-secondary)" }}>
                      Ranked by Reciprocal Rank Fusion (BM25 + Dense Vectors)
                    </span>
                  </div>

                  {searchResponse.tamil_evidence?.length > 0 ? (
                    searchResponse.tamil_evidence.map((item, idx) => {
                      const relType = searchResponse.relationship_type || "THEMATIC";
                      const isSaved = savedEvidence.some((e) => e.source_id === item.source_id);

                      return (
                        <div key={idx} className="evidence-card">
                          <div className="evidence-card-header">
                            <div className="source-meta-tag">
                              <span className="work-name-badge">
                                {item.source_type === "thirukkural" ? "Thirukkural" : "Thiruvarutpa"}
                              </span>
                              <span className="verse-id-text">{item.source_id}</span>
                            </div>
                            <span className={`relationship-badge ${relType}`}>{relType}</span>
                          </div>

                          <p className="verse-tamil-excerpt">{item.text}</p>

                          <div className="relationship-explanation-box">
                            <p className="rel-explanation-text">
                              {RELATIONSHIP_EXPLANATIONS[relType] || RELATIONSHIP_EXPLANATIONS.THEMATIC}
                            </p>
                          </div>

                          <div className="evidence-card-footer">
                            <div className="score-indicators-row">
                              <div className="score-chip">
                                <span>Relevance:</span>
                                <span className="score-val">
                                  {Math.round((item.retrieval_relevance || searchResponse.retrieval_relevance || 0.8) * 100)}%
                                </span>
                              </div>
                              <div className="score-chip">
                                <span>Evidence Strength:</span>
                                <span className="score-val">{searchResponse.evidence_strength}</span>
                              </div>
                              <div className="score-chip">
                                <span>Confidence:</span>
                                <span className="score-val">
                                  {Math.round((searchResponse.interpretation_confidence || 0.5) * 100)}%
                                </span>
                              </div>
                            </div>

                            <div style={{ display: "flex", gap: "8px" }}>
                              <button
                                className="btn-secondary"
                                style={{ padding: "6px 10px" }}
                                onClick={() => toggleSaveEvidence(item)}
                                title={isSaved ? "Saved to workspace" : "Save evidence"}
                              >
                                <Bookmark size={14} fill={isSaved ? "currentColor" : "none"} />
                              </button>
                              <button className="view-evidence-btn" onClick={() => setSelectedEvidence(item)}>
                                View Evidence Detail
                              </button>
                            </div>
                          </div>
                        </div>
                      );
                    })
                  ) : (
                    <div className="empty-state-card">
                      <h4 className="empty-state-title">No direct literary match found</h4>
                      <p className="empty-state-text">Try adjusting your search query or selecting a suggested concept.</p>
                    </div>
                  )}
                </div>

                {/* Right Side Summary Panel */}
                <div className="side-column">
                  <div className="side-card">
                    <h3 className="side-card-title">AI Interpretive Synthesis</h3>
                    <p className="synthesis-text-p">{searchResponse.reasoning}</p>

                    <div style={{ borderTop: "1px solid var(--border-subtle)", paddingTop: "12px", marginTop: "12px" }}>
                      <span className="detail-label">Export Research Results</span>
                      <div style={{ display: "flex", gap: "8px", marginTop: "8px" }}>
                        <button className="btn-secondary" style={{ flex: 1 }} onClick={() => exportReport("json")}>
                          <Download size={14} /> JSON
                        </button>
                        <button className="btn-secondary" style={{ flex: 1 }} onClick={() => exportReport("csv")}>
                          <Download size={14} /> CSV
                        </button>
                        <button className="btn-secondary" style={{ flex: 1 }} onClick={() => exportReport("txt")}>
                          <Download size={14} /> TXT
                        </button>
                      </div>
                    </div>
                  </div>

                  <div className="side-card">
                    <h3 className="side-card-title">Academic Governance & Limitations</h3>
                    <ul style={{ paddingLeft: "18px", margin: 0, fontSize: "0.83rem", color: "var(--text-secondary)", lineHeight: "1.6" }}>
                      {searchResponse.limitations?.map((lim, idx) => (
                        <li key={idx} style={{ marginBottom: "6px" }}>{lim}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* WORKSPACE TAB */}
        {activeTab === "workspace" && (
          <div>
            <div className="section-header-title" style={{ marginBottom: "20px" }}>
              <h2>Research Workspace & Bookmarks</h2>
            </div>

            {savedEvidence.length > 0 ? (
              <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: "24px" }}>
                <div className="results-list-column">
                  {savedEvidence.map((item, idx) => (
                    <div key={idx} className="evidence-card">
                      <div className="evidence-card-header">
                        <span className="work-name-badge">{item.source_id}</span>
                        <button className="btn-secondary" style={{ padding: "4px 8px" }} onClick={() => toggleSaveEvidence(item)}>
                          Remove
                        </button>
                      </div>
                      <p className="verse-tamil-excerpt">{item.text}</p>
                    </div>
                  ))}
                </div>

                <div className="side-card">
                  <h3 className="side-card-title">Research Annotations & Notes</h3>
                  <textarea
                    style={{
                      width: "100%",
                      height: "200px",
                      borderRadius: "var(--radius-md)",
                      border: "1px solid var(--border-light)",
                      padding: "12px",
                      fontFamily: "var(--font-sans)",
                      fontSize: "0.88rem",
                      resize: "vertical"
                    }}
                    placeholder="Record your research insights and notes here..."
                    value={researchNotes}
                    onChange={(e) => setResearchNotes(e.target.value)}
                  />
                </div>
              </div>
            ) : (
              <div className="empty-state-card">
                <h4 className="empty-state-title">No saved research evidence yet</h4>
                <p className="empty-state-text">Use the Explore tab to search for scientific concepts and bookmark relevant verses.</p>
              </div>
            )}
          </div>
        )}

        {/* EVIDENCE REPOSITORY TAB */}
        {activeTab === "evidence" && (
          <div>
            <div className="section-header-title" style={{ marginBottom: "20px" }}>
              <h2>Evidence Repository</h2>
              <span style={{ fontSize: "0.85rem", color: "var(--text-secondary)", fontWeight: "normal" }}>
                {dbEvidenceRecords.length} records persisted in production database
              </span>
            </div>

            <div className="data-table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Evidence ID</th>
                    <th>Concept</th>
                    <th>Literary Source</th>
                    <th>Relationship</th>
                    <th>Evidence Strength</th>
                    <th>Confidence</th>
                    <th>Review Status</th>
                  </tr>
                </thead>
                <tbody>
                  {dbEvidenceRecords.length > 0 ? (
                    dbEvidenceRecords.map((r, idx) => (
                      <tr key={idx}>
                        <td style={{ fontWeight: "600", fontFamily: "monospace" }}>{r.evidence_id || r.id}</td>
                        <td>{r.scientific_concept_name}</td>
                        <td>{r.literary_source_id}</td>
                        <td>
                          <span className={`relationship-badge ${r.relationship_type}`}>{r.relationship_type}</span>
                        </td>
                        <td>{r.evidence_strength}</td>
                        <td>{Math.round((r.interpretation_confidence || 0.5) * 100)}%</td>
                        <td>
                          <span style={{ fontWeight: "600", color: r.review_status === "APPROVED" ? "#16A34A" : "#D97706" }}>
                            {r.review_status}
                          </span>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="7" style={{ textAlign: "center", padding: "24px" }}>
                        No evidence records found in the database.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* KNOWLEDGE GRAPH TAB */}
        {activeTab === "graph" && (
          <div>
            <div className="section-header-title" style={{ marginBottom: "16px" }}>
              <h2>Interactive Knowledge Graph Explorer</h2>
              <span style={{ fontSize: "0.85rem", color: "var(--text-secondary)", fontWeight: "normal" }}>
                Multi-Hop Conceptual & Literary Relationship Subgraph
              </span>
            </div>

            <div className="graph-preset-bar">
              <span className="preset-label">Explore Concept Graphs:</span>
              {PRESETS.map((p, idx) => (
                <button
                  key={idx}
                  className="preset-chip"
                  onClick={() => {
                    setSearchQuery(p.query);
                    setSearchLang(p.lang);
                    executeSearch(p.query, p.lang);
                  }}
                >
                  {p.label}
                </button>
              ))}
            </div>

            <div className="side-card" style={{ padding: "16px", minHeight: "550px" }}>
              {searchResponse?.knowledge_graph ? (
                <InteractiveGraphView graph={searchResponse.knowledge_graph} onSelectEvidence={(item) => setSelectedEvidence(item)} />
              ) : (
                <div className="empty-state-card">
                  <h4 className="empty-state-title">No Knowledge Graph Loaded</h4>
                  <p className="empty-state-text">Search for a concept or click any preset above to render its dynamic knowledge graph.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* EXPERT REVIEW TAB */}
        {activeTab === "review" && (
          <div>
            <div className="section-header-title" style={{ marginBottom: "20px" }}>
              <h2>Expert Review Queue</h2>
            </div>

            {pendingReviews.length > 0 ? (
              <div className="results-list-column">
                {pendingReviews.map((item, idx) => (
                  <div key={idx} className="evidence-card">
                    <div className="evidence-card-header">
                      <span className="work-name-badge">{item.evidence_id || item.id}</span>
                      <span className={`relationship-badge ${item.relationship_type}`}>{item.relationship_type}</span>
                    </div>
                    <p className="verse-tamil-excerpt">{item.supporting_text}</p>
                    <div style={{ display: "flex", gap: "10px", marginTop: "14px" }}>
                      <button
                        className="btn-primary"
                        style={{ background: "#16A34A" }}
                        onClick={() => handleReviewDecision(item.evidence_id || item.id, "APPROVED", "Approved by expert")}
                      >
                        Approve Evidence
                      </button>
                      <button
                        className="btn-secondary"
                        onClick={() => handleReviewDecision(item.evidence_id || item.id, "NEEDS_REVISION", "Needs revision")}
                      >
                        Request Revision
                      </button>
                      <button
                        className="btn-secondary"
                        style={{ color: "#DC2626" }}
                        onClick={() => handleReviewDecision(item.evidence_id || item.id, "REJECTED", "Rejected")}
                      >
                        Reject
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state-card">
                <h4 className="empty-state-title">No pending items for review</h4>
                <p className="empty-state-text">All generated evidence records have been processed by expert reviewers.</p>
              </div>
            )}
          </div>
        )}

        {/* SYSTEM HEALTH & ADMIN TAB */}
        {activeTab === "admin" && (
          <div>
            <div className="section-header-title" style={{ marginBottom: "20px" }}>
              <h2>System Health & Database Statistics</h2>
            </div>

            {adminStats && (
              <div className="scores-three-grid" style={{ marginBottom: "32px" }}>
                <div className="score-box">
                  <div className="score-box-title">Total Indexed Verses</div>
                  <div className="score-box-value">{adminStats.total_verses}</div>
                </div>
                <div className="score-box">
                  <div className="score-box-title">Thirukkural Verses</div>
                  <div className="score-box-value">{adminStats.thirukkural_verses}</div>
                </div>
                <div className="score-box">
                  <div className="score-box-title">Thiruvarutpa Verses</div>
                  <div className="score-box-value">{adminStats.thiruvarutpa_verses}</div>
                </div>
                <div className="score-box">
                  <div className="score-box-title">Scientific Concepts</div>
                  <div className="score-box-value">{adminStats.scientific_concepts}</div>
                </div>
                <div className="score-box">
                  <div className="score-box-title">Evidence Records</div>
                  <div className="score-box-value">{adminStats.evidence_records_persisted}</div>
                </div>
                <div className="score-box">
                  <div className="score-box-title">Expert Reviews</div>
                  <div className="score-box-value">{adminStats.expert_reviews_submitted}</div>
                </div>
              </div>
            )}

            <div className="section-header-title" style={{ marginBottom: "16px" }}>
              <h3>Security & Audit Log</h3>
            </div>

            <div className="data-table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Action</th>
                    <th>Resource</th>
                    <th>User ID</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {auditLogs.length > 0 ? (
                    auditLogs.map((log, idx) => (
                      <tr key={idx}>
                        <td style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
                          {new Date(log.timestamp).toLocaleString()}
                        </td>
                        <td style={{ fontWeight: "600" }}>{log.action}</td>
                        <td style={{ fontFamily: "monospace", fontSize: "0.82rem" }}>{log.resource}</td>
                        <td>{log.username || log.user_id || "ANONYMOUS"}</td>
                        <td>
                          <span style={{ color: log.status === "SUCCESS" ? "#16A34A" : "#DC2626", fontWeight: "600" }}>
                            {log.status}
                          </span>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="5" style={{ textAlign: "center", padding: "24px" }}>
                        No audit log entries available.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>

      {/* Evidence Detail Slide-Over Modal */}
      {selectedEvidence && (
        <div className="modal-overlay" onClick={() => setSelectedEvidence(null)}>
          <div className="slide-panel" onClick={(e) => e.stopPropagation()}>
            <div className="panel-header">
              <h3 className="panel-title-text">Evidence Detail: {selectedEvidence.source_id}</h3>
              <button className="close-btn" onClick={() => setSelectedEvidence(null)}>
                <X size={18} />
              </button>
            </div>

            <div className="panel-tabs-bar">
              <button
                className={`panel-tab-btn ${evidenceTab === "overview" ? "active" : ""}`}
                onClick={() => setEvidenceTab("overview")}
              >
                Overview
              </button>
              <button
                className={`panel-tab-btn ${evidenceTab === "dimensions" ? "active" : ""}`}
                onClick={() => setEvidenceTab("dimensions")}
              >
                4D Dimensions
              </button>
              <button
                className={`panel-tab-btn ${evidenceTab === "evidence" ? "active" : ""}`}
                onClick={() => setEvidenceTab("evidence")}
              >
                Literary Evidence
              </button>
              <button
                className={`panel-tab-btn ${evidenceTab === "scores" ? "active" : ""}`}
                onClick={() => setEvidenceTab("scores")}
              >
                Scores & Validation
              </button>
              <button
                className={`panel-tab-btn ${evidenceTab === "provenance" ? "active" : ""}`}
                onClick={() => setEvidenceTab("provenance")}
              >
                Provenance
              </button>
            </div>

            <div className="panel-body-content">
              {evidenceTab === "overview" && (
                <>
                  <div className="detail-block">
                    <span className="detail-label">Classical Tamil Verse</span>
                    <p className="detail-verse-text">{selectedEvidence.text}</p>
                  </div>

                  <div className="detail-block">
                    <span className="detail-label">Relationship Classification</span>
                    <div style={{ display: "flex", alignItems: "center", gap: "10px", marginTop: "4px" }}>
                      <span className={`relationship-badge ${searchResponse?.relationship_type || "THEMATIC"}`}>
                        {searchResponse?.relationship_type || "THEMATIC"}
                      </span>
                    </div>
                    <p className="detail-translation-text" style={{ marginTop: "8px" }}>
                      {RELATIONSHIP_EXPLANATIONS[searchResponse?.relationship_type] || RELATIONSHIP_EXPLANATIONS.THEMATIC}
                    </p>
                  </div>
                </>
              )}

              {evidenceTab === "dimensions" && (
                <div style={{ marginTop: "12px" }}>
                  <DimensionalAnalysisView dimensionalAnalysis={searchResponse?.dimensional_analysis} />
                </div>
              )}

              {evidenceTab === "evidence" && (
                <>
                  <div className="detail-block">
                    <span className="detail-label">Original Text</span>
                    <p className="detail-verse-text">{selectedEvidence.text}</p>
                  </div>
                  <div className="detail-block">
                    <span className="detail-label">English Translation / Paraphrase</span>
                    <p className="detail-translation-text">
                      {selectedEvidence.metadata?.translation || "Classical Tamil verse rendering describing natural law and moral order."}
                    </p>
                  </div>
                </>
              )}

              {evidenceTab === "scores" && (
                <div className="scores-three-grid">
                  <div className="score-box">
                    <div className="score-box-title">Retrieval Relevance</div>
                    <div className="score-box-value">
                      {Math.round((selectedEvidence.retrieval_relevance || searchResponse?.retrieval_relevance || 0.8) * 100)}%
                    </div>
                  </div>
                  <div className="score-box">
                    <div className="score-box-title">Evidence Strength</div>
                    <div className="score-box-value">{searchResponse?.evidence_strength || "MEDIUM"}</div>
                  </div>
                  <div className="score-box">
                    <div className="score-box-title">Interpretation Confidence</div>
                    <div className="score-box-value">
                      {Math.round((searchResponse?.interpretation_confidence || 0.5) * 100)}%
                    </div>
                  </div>
                </div>
              )}

              {evidenceTab === "provenance" && (
                <div className="detail-block">
                  <span className="detail-label">Source Metadata</span>
                  <pre style={{ fontSize: "0.8rem", background: "var(--bg-secondary)", padding: "12px", borderRadius: "var(--radius-sm)" }}>
                    {JSON.stringify(selectedEvidence.metadata || {}, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Login Modal */}
      {showLoginModal && (
        <div className="modal-overlay" onClick={() => setShowLoginModal(false)}>
          <div className="side-card" style={{ maxWidth: "400px", width: "100%", margin: "auto" }} onClick={(e) => e.stopPropagation()}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <h3 style={{ margin: 0 }}>Researcher Login</h3>
              <button className="close-btn" onClick={() => setShowLoginModal(false)}>
                <X size={16} />
              </button>
            </div>

            {loginError && (
              <div style={{ color: "#DC2626", fontSize: "0.85rem", marginBottom: "12px", fontWeight: "600" }}>
                {loginError}
              </div>
            )}

            <form onSubmit={handleLogin}>
              <div style={{ marginBottom: "12px" }}>
                <label style={{ display: "block", fontSize: "0.8rem", fontWeight: "600", marginBottom: "4px" }}>Username</label>
                <input
                  type="text"
                  style={{ width: "100%", padding: "8px 12px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-light)" }}
                  value={loginForm.username}
                  onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })}
                  required
                />
              </div>

              <div style={{ marginBottom: "18px" }}>
                <label style={{ display: "block", fontSize: "0.8rem", fontWeight: "600", marginBottom: "4px" }}>Password</label>
                <input
                  type="password"
                  style={{ width: "100%", padding: "8px 12px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-light)" }}
                  value={loginForm.password}
                  onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                  required
                />
              </div>

              <button className="btn-primary" style={{ width: "100%", justifyContent: "center" }} type="submit">
                Log In
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

// Enhanced Interactive SVG Knowledge Graph Subcomponent
function InteractiveGraphView({ graph, onSelectEvidence }) {
  const [selectedNode, setSelectedNode] = useState(null);
  const [hoveredNode, setHoveredNode] = useState(null);
  const [filterType, setFilterType] = useState("ALL");
  const [searchFilter, setSearchFilter] = useState("");
  const [zoomLevel, setZoomLevel] = useState(1.0);

  if (!graph || !graph.nodes || graph.nodes.length === 0) return null;

  const rawNodes = graph.nodes || [];
  const rawEdges = graph.edges || [];

  // Filter nodes based on user selection & search string
  const filteredNodes = rawNodes.filter((n) => {
    const typeMatch =
      filterType === "ALL" ||
      (filterType === "CONCEPT" && (n.type === "SCIENTIFIC_CONCEPT" || n.type === "concept")) ||
      (filterType === "DOMAIN" && (n.type === "DOMAIN" || n.type === "domain")) ||
      (filterType === "RELATIONSHIP" && (n.type === "RELATIONSHIP" || n.type === "relationship")) ||
      (filterType === "VERSE" && (n.type === "VERSE" || n.type === "verse" || n.type === "SOURCE" || n.type === "CHAPTER"));

    const textMatch =
      !searchFilter.trim() ||
      n.label?.toLowerCase().includes(searchFilter.toLowerCase()) ||
      n.id?.toLowerCase().includes(searchFilter.toLowerCase());

    return typeMatch && textMatch;
  });

  const filteredNodeIds = new Set(filteredNodes.map((n) => n.id));
  const filteredEdges = rawEdges.filter(
    (e) => filteredNodeIds.has(e.source) && filteredNodeIds.has(e.target)
  );

  const width = 1000;
  const height = 560;
  const centerX = width / 2;
  const centerY = height / 2;

  // Compute Solar-System Radial Layout Coords
  const nodeCoords = {};
  const conceptNodes = filteredNodes.filter(n => n.type === "SCIENTIFIC_CONCEPT" || n.type === "concept");
  const domainNodes = filteredNodes.filter(n => n.type === "DOMAIN" || n.type === "domain");
  const relNodes = filteredNodes.filter(n => n.type === "RELATIONSHIP" || n.type === "relationship" || n.type === "EVIDENCE");
  const verseNodes = filteredNodes.filter(n => !conceptNodes.includes(n) && !domainNodes.includes(n) && !relNodes.includes(n));

  // Center node
  conceptNodes.forEach((n, idx) => {
    nodeCoords[n.id] = { x: centerX + (idx * 50 - (conceptNodes.length - 1) * 25), y: centerY };
  });

  // Inner Orbit: Domains (r=150)
  domainNodes.forEach((n, idx) => {
    const angle = (idx / Math.max(1, domainNodes.length)) * 2 * Math.PI - Math.PI / 2;
    nodeCoords[n.id] = {
      x: centerX + Math.cos(angle) * 150,
      y: centerY + Math.sin(angle) * 120
    };
  });

  // Middle Orbit: Relationships (r=250)
  relNodes.forEach((n, idx) => {
    const angle = (idx / Math.max(1, relNodes.length)) * 2 * Math.PI + Math.PI / 4;
    nodeCoords[n.id] = {
      x: centerX + Math.cos(angle) * 250,
      y: centerY + Math.sin(angle) * 190
    };
  });

  // Outer Orbit: Verses & Chapters (r=350)
  verseNodes.forEach((n, idx) => {
    const angle = (idx / Math.max(1, verseNodes.length)) * 2 * Math.PI;
    nodeCoords[n.id] = {
      x: centerX + Math.cos(angle) * 350,
      y: centerY + Math.sin(angle) * 240
    };
  });

  // Fallback for any unmapped nodes
  filteredNodes.forEach((n, idx) => {
    if (!nodeCoords[n.id]) {
      const angle = (idx / filteredNodes.length) * 2 * Math.PI;
      nodeCoords[n.id] = {
        x: centerX + Math.cos(angle) * 220,
        y: centerY + Math.sin(angle) * 170
      };
    }
  });

  const getNodeFill = (n, isSel) => {
    if (isSel) return "#F59E0B";
    const type = n.type?.toUpperCase() || "";
    if (type.includes("CONCEPT")) return "#B45309";
    if (type.includes("DOMAIN")) return "#78350F";
    if (type.includes("RELATIONSHIP")) return "#D97706";
    if (type.includes("EVIDENCE")) return "#92400E";
    return "#451A03";
  };

  const getNodeBadgeText = (n) => {
    const type = n.type?.toUpperCase() || "";
    if (type.includes("CONCEPT")) return "SC";
    if (type.includes("DOMAIN")) return "DOM";
    if (type.includes("RELATIONSHIP")) return "REL";
    if (type.includes("EVIDENCE")) return "EVI";
    return "VS";
  };

  const getNodeRadius = (n) => {
    const type = n.type?.toUpperCase() || "";
    if (type.includes("CONCEPT")) return 24;
    if (type.includes("DOMAIN")) return 20;
    if (type.includes("RELATIONSHIP")) return 18;
    return 16;
  };

  const activeHoverTarget = hoveredNode || selectedNode?.id;

  return (
    <div style={{ display: "flex", flexDirection: "column", width: "100%" }}>
      {/* Interactive Toolbar */}
      <div className="graph-toolbar">
        <div className="graph-filter-group">
          <span style={{ fontSize: "0.8rem", fontWeight: "700", color: "#78350F", marginRight: "4px" }}>Filter:</span>
          {["ALL", "CONCEPT", "DOMAIN", "RELATIONSHIP", "VERSE"].map((type) => (
            <button
              key={type}
              className={`graph-filter-btn ${filterType === type ? "active" : ""}`}
              onClick={() => setFilterType(type)}
            >
              {type}
            </button>
          ))}
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <input
            type="text"
            className="graph-search-input"
            placeholder="Search nodes..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
          />
          <div style={{ display: "flex", gap: "4px" }}>
            <button className="graph-filter-btn" onClick={() => setZoomLevel(prev => Math.min(prev + 0.15, 1.6))}>+</button>
            <button className="graph-filter-btn" onClick={() => setZoomLevel(prev => Math.max(prev - 0.15, 0.7))}>-</button>
            <button className="graph-filter-btn" onClick={() => { setZoomLevel(1.0); setSearchFilter(""); setFilterType("ALL"); }}>Reset</button>
          </div>
        </div>
      </div>

      {/* Main SVG Knowledge Canvas */}
      <div style={{ position: "relative", overflow: "hidden", borderRadius: "var(--radius-lg)", border: "1px solid #FCD34D", background: "#FFFDF0" }}>
        <svg
          viewBox={`0 0 ${width} ${height}`}
          style={{
            width: "100%",
            height: "520px",
            transform: `scale(${zoomLevel})`,
            transformOrigin: "center center",
            transition: "transform 0.2s ease"
          }}
        >
          <defs>
            <pattern id="graph-grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#FDE68A" strokeWidth="0.6" opacity="0.6" />
            </pattern>
            <filter id="node-glow" x="-30%" y="-30%" width="160%" height="160%">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            <marker id="arrowhead" viewBox="0 0 10 10" refX="24" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#D97706" />
            </marker>
          </defs>

          {/* Grid Background */}
          <rect width={width} height={height} fill="url(#graph-grid)" />

          {/* Orbit Circles */}
          <circle cx={centerX} cy={centerY} r="150" fill="none" stroke="#FCD34D" strokeWidth="1.2" strokeDasharray="4 4" opacity="0.6" />
          <circle cx={centerX} cy={centerY} r="250" fill="none" stroke="#FDE68A" strokeWidth="1.2" strokeDasharray="6 6" opacity="0.5" />
          <circle cx={centerX} cy={centerY} r="350" fill="none" stroke="#FEF3C7" strokeWidth="1.2" strokeDasharray="8 8" opacity="0.4" />

          {/* Edge Connection Lines and Midpoint Tags */}
          <g>
            {filteredEdges.map((e, idx) => {
              const s = nodeCoords[e.source];
              const t = nodeCoords[e.target];
              if (!s || !t) return null;

              const isConnectedToHover = activeHoverTarget && (e.source === activeHoverTarget || e.target === activeHoverTarget);
              const edgeColor = isConnectedToHover ? "#F59E0B" : "#D97706";
              const strokeWidth = isConnectedToHover ? 3 : 1.5;
              const opacity = activeHoverTarget ? (isConnectedToHover ? 1.0 : 0.2) : 0.65;

              const midX = (s.x + t.x) / 2;
              const midY = (s.y + t.y) / 2;
              const relText = e.relationship || e.type || "";

              return (
                <g key={idx}>
                  <line
                    x1={s.x}
                    y1={s.y}
                    x2={t.x}
                    y2={t.y}
                    stroke={edgeColor}
                    strokeWidth={strokeWidth}
                    strokeDasharray={e.relationship === "METAPHORICAL" ? "5 5" : "none"}
                    markerEnd="url(#arrowhead)"
                    opacity={opacity}
                    style={{ transition: "all 0.2s ease" }}
                  />
                  {relText && (
                    <g transform={`translate(${midX}, ${midY})`} opacity={opacity}>
                      <rect
                        x={-(relText.length * 3.2 + 8)}
                        y="-9"
                        width={relText.length * 6.4 + 16}
                        height="18"
                        rx="9"
                        fill="#FFFDF0"
                        stroke="#FCD34D"
                        strokeWidth="1"
                      />
                      <text
                        dy="3.5"
                        textAnchor="middle"
                        fill="#78350F"
                        fontSize="9.5"
                        fontWeight="700"
                      >
                        {relText}
                      </text>
                    </g>
                  )}
                </g>
              );
            })}
          </g>

          {/* Graph Nodes */}
          <g>
            {filteredNodes.map((n) => {
              const pos = nodeCoords[n.id];
              if (!pos) return null;
              const isSel = selectedNode?.id === n.id;
              const isHovered = hoveredNode === n.id;
              const fill = getNodeFill(n, isSel);
              const radius = getNodeRadius(n);
              const labelStr = n.label || n.id;
              const pillWidth = Math.max(70, labelStr.length * 7 + 16);

              return (
                <g
                  key={n.id}
                  transform={`translate(${pos.x}, ${pos.y})`}
                  onClick={() => setSelectedNode(n)}
                  onMouseEnter={() => setHoveredNode(n.id)}
                  onMouseLeave={() => setHoveredNode(null)}
                  style={{ cursor: "pointer", transition: "transform 0.2s ease" }}
                >
                  <title>{`${labelStr} (${n.type})`}</title>

                  {/* Pulsing outer aura */}
                  {(isSel || isHovered || n.type === "SCIENTIFIC_CONCEPT" || n.type === "concept") && (
                    <circle
                      r={radius + 8}
                      fill="none"
                      stroke="#F59E0B"
                      strokeWidth="2"
                      opacity={isSel || isHovered ? "0.9" : "0.4"}
                      filter="url(#node-glow)"
                    />
                  )}

                  {/* Icon Circle Badge */}
                  <circle
                    r={radius}
                    fill={fill}
                    stroke="#FFFBEB"
                    strokeWidth="2.5"
                    filter={isSel || isHovered ? "url(#node-glow)" : "none"}
                  />

                  {/* Badge Symbol inside Circle */}
                  <text
                    dy="4"
                    textAnchor="middle"
                    fill="#FFFFFF"
                    fontSize="10"
                    fontWeight="800"
                    pointerEvents="none"
                  >
                    {getNodeBadgeText(n)}
                  </text>

                  {/* External Pill Label below circle */}
                  <g transform={`translate(0, ${radius + 14})`}>
                    <rect
                      x={-pillWidth / 2}
                      y="-10"
                      width={pillWidth}
                      height="20"
                      rx="10"
                      fill="#FFFDF0"
                      stroke={isSel || isHovered ? "#D97706" : "#FCD34D"}
                      strokeWidth={isSel || isHovered ? "2" : "1.2"}
                      filter="drop-shadow(0px 1px 2px rgba(0,0,0,0.1))"
                    />
                    <text
                      dy="3.5"
                      textAnchor="middle"
                      fill="#451A03"
                      fontSize="11"
                      fontWeight="700"
                      pointerEvents="none"
                    >
                      {labelStr.length > 22 ? labelStr.substring(0, 20) + "…" : labelStr}
                    </text>
                  </g>
                </g>
              );
            })}
          </g>
        </svg>
      </div>

      {/* Entity Inspector Panel */}
      {selectedNode ? (
        <div className="graph-node-inspector">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <Network size={20} color="#B45309" />
              <h3 style={{ margin: 0, fontSize: "1.05rem", color: "#451A03" }}>{selectedNode.label || selectedNode.id}</h3>
            </div>
            <span className="epoch-tag">{selectedNode.type}</span>
          </div>

          <p style={{ margin: "0 0 12px 0", fontSize: "0.88rem", color: "#78350F", lineHeight: "1.5" }}>
            {selectedNode.metadata?.text || selectedNode.metadata?.reason || selectedNode.description || `Entity in Tamil Literary Knowledge Graph.`}
          </p>

          <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", alignItems: "center" }}>
            {selectedNode.metadata?.verse_id && (
              <button
                className="btn-primary"
                style={{ padding: "5px 12px", fontSize: "0.8rem" }}
                onClick={() => onSelectEvidence && onSelectEvidence({ source_id: selectedNode.metadata.verse_id, text: selectedNode.metadata.text, metadata: selectedNode.metadata })}
              >
                View Evidence Detail
              </button>
            )}

            <span style={{ fontSize: "0.78rem", color: "#B45309", fontWeight: "600" }}>
              ID: <code style={{ background: "#FEF3C7", padding: "2px 6px", borderRadius: "4px" }}>{selectedNode.id}</code>
            </span>
          </div>
        </div>
      ) : (
        <div style={{ marginTop: "12px", fontSize: "0.84rem", color: "var(--text-secondary)", textAlign: "center", fontWeight: "500" }}>
          Click any node or relationship link in the graph to open the Entity Inspector.
        </div>
      )}
    </div>
  );
}

// 4D Multidimensional Interpretive Analysis Subcomponent
function DimensionalAnalysisView({ dimensionalAnalysis }) {
  const [activeStep, setActiveStep] = useState(0);

  if (!dimensionalAnalysis || dimensionalAnalysis.length === 0) return null;

  const current = dimensionalAnalysis[activeStep] || dimensionalAnalysis[0];
  const stepBadges = ["d1", "d2", "d3", "d4"];

  return (
    <div className="dimensional-analysis-container">
      <div className="dimensional-header">
        <div className="dimensional-title-group">
          <Layers size={18} color="var(--accent-indigo)" />
          <h3 className="dimensional-title">4D Multidimensional Interpretive Analysis</h3>
        </div>
        <span style={{ fontSize: "0.78rem", fontWeight: "600", color: "var(--text-secondary)", background: "var(--bg-secondary)", padding: "4px 8px", borderRadius: "var(--radius-sm)" }}>
          4 Levels of Research Abstraction
        </span>
      </div>

      <div className="dimension-stepper-grid">
        {dimensionalAnalysis.map((step, idx) => (
          <div
            key={idx}
            className={`dimension-step-card ${activeStep === idx ? "active" : ""}`}
            onClick={() => setActiveStep(idx)}
          >
            <span className={`dimension-step-badge ${stepBadges[idx] || "d1"}`}>
              Level {idx + 1}
            </span>
            <div className="dimension-step-name">{step.dimension_name || `Dimension ${idx + 1}`}</div>
            <div className="dimension-step-focus">{step.focus || step.question}</div>
          </div>
        ))}
      </div>

      <div className="dimension-detail-panel">
        <div className="dimension-detail-title">
          <Info size={16} color="var(--accent-indigo)" />
          <span>{current.dimension_name}: {current.focus}</span>
        </div>
        <div className="dimension-detail-text">
          <strong>Key Research Question:</strong> {current.question}
        </div>
        <div className="dimension-detail-text">
          {current.details}
        </div>

        {current.epoch_info && (
          <div className="epoch-badge-container">
            <span className="epoch-tag">
              Epoch: {current.epoch_info.epoch}
            </span>
            <div className="proof-distance-container">
              <div className="proof-distance-header">
                <span>Distance to Empirical Proof:</span>
                <span>{current.epoch_info.distance_to_proof || 25}%</span>
              </div>
              <div className="proof-distance-bar">
                <div
                  className="proof-distance-fill"
                  style={{ width: `${current.epoch_info.distance_to_proof || 25}%` }}
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Canvas Animated Moving Tamil Letters Background Subcomponent
function MovingTamilLettersBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let animationFrameId;

    const tamilChars = [
      "அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஐ", "ஒ", "ஓ", "ஔ", "ஃ",
      "க்", "ங", "ச", "ஞ", "ட", "ண", "த", "ந", "ப", "ம", "ய", "ர", "ல", "வ", "ழ", "ள", "ற", "ன",
      "தமிழ்", "அறம்", "பொருள்", "இன்பம்", "குறள்", "வள்ளுவர்", "அருட்பா", "ஞானம்", "இயற்பியல்", "வான்இயல்"
    ];

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", handleResize);

    const particles = Array.from({ length: 65 }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      char: tamilChars[Math.floor(Math.random() * tamilChars.length)],
      fontSize: Math.floor(Math.random() * 32) + 22,
      speedY: -(Math.random() * 0.6 + 0.2),
      speedX: (Math.random() - 0.5) * 0.3,
      opacity: Math.random() * 0.4 + 0.25,
      rotation: Math.random() * Math.PI * 2,
      rotationSpeed: (Math.random() - 0.5) * 0.005
    }));

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      particles.forEach((p) => {
        p.y += p.speedY;
        p.x += p.speedX;
        p.rotation += p.rotationSpeed;

        if (p.y < -50) {
          p.y = height + 50;
          p.x = Math.random() * width;
        }
        if (p.x < -50) p.x = width + 50;
        if (p.x > width + 50) p.x = -50;

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation);
        ctx.font = `700 ${p.fontSize}px "Noto Serif Tamil", "Latha", serif`;
        ctx.fillStyle = `rgba(180, 83, 9, ${p.opacity})`;
        ctx.fillText(p.char, 0, 0);
        ctx.restore();
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return <canvas ref={canvasRef} className="tamil-letters-canvas" />;
}