import { useRef, useState } from "react";
import "./App.css";

function App() {
  const [companyName, setCompanyName] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [report, setReport] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const validateFile = (selectedFile) => {
    if (!selectedFile) return false;

    const allowedTypes = [".pdf", ".csv", ".txt"];
    const extension =
      "." + selectedFile.name.split(".").pop().toLowerCase();

    if (!allowedTypes.includes(extension)) {
      setError("Please upload a PDF, CSV, or TXT file.");
      return false;
    }

    if (selectedFile.size > 50 * 1024 * 1024) {
      setError("File size must be less than 50 MB.");
      return false;
    }

    return true;
  };

  const selectFile = (selectedFile) => {
    setError("");
    setReport(null);

    if (!selectedFile) {
      setFile(null);
      return;
    }

    if (validateFile(selectedFile)) {
      setFile(selectedFile);
    } else {
      setFile(null);
    }
  };

  const handleFileChange = (event) => {
    selectFile(event.target.files?.[0]);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    if (!loading) setDragActive(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    setDragActive(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragActive(false);

    if (loading) return;

    const droppedFile = event.dataTransfer.files?.[0];
    selectFile(droppedFile);
  };

  const removeFile = () => {
    setFile(null);
    setError("");
    setReport(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const generateReport = async () => {
    setError("");
    setReport(null);

    if (!companyName.trim()) {
      setError("Please enter the company name.");
      return;
    }

    if (!file) {
      setError("Please upload a PDF, CSV, or TXT file.");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("company_name", companyName.trim());
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      let data;

      try {
        data = await response.json();
      } catch {
        throw new Error("The server returned an unexpected response.");
      }

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "We couldn't generate the report. Please try again."
        );
      }

      setReport(data.report);
    } catch (err) {
      setError(
        err.message ||
          "Something went wrong while generating the report."
      );
    } finally {
      setLoading(false);
    }
  };

  const generateAnother = () => {
    setReport(null);
    setError("");
    setFile(null);
    setCompanyName("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const getFileExtension = () => {
    if (!file) return "";
    return file.name.split(".").pop().toUpperCase();
  };

  const getFileSize = () => {
    if (!file) return "";

    const mb = file.size / (1024 * 1024);

    if (mb < 1) {
      return `${Math.max(1, Math.round(file.size / 1024))} KB`;
    }

    return `${mb.toFixed(2)} MB`;
  };

  return (
    <div className="app">
      <div className="background-grid" />
      <div className="background-glow glow-one" />
      <div className="background-glow glow-two" />
      <div className="background-glow glow-three" />

      <main className="container">
        <header className="topbar">
          <div className="brand">
            <div className="brand-mark">
              <span />
              <span />
              <span />
            </div>

            <div>
              <strong>BULL AI</strong>
              <small>Research Intelligence</small>
            </div>
          </div>

          <div className="status-pill">
            <span className="status-dot" />
            AI Engine Online
          </div>
        </header>

        <section className="hero">
          <div className="badge">
            <span className="badge-dot" />
            AI • FINANCIAL RESEARCH
          </div>

          <h1>
            Financial Research
            <span>Report Generator</span>
          </h1>

          <p>
            Transform financial documents into structured,
            analyst-style research reports powered by AI.
          </p>

          <div className="hero-features">
            <span><b>✦</b> AI Extraction</span>
            <span><b>▦</b> Financial Tables</span>
            <span><b>◒</b> Visual Analytics</span>
            <span><b>↓</b> PDF Ready</span>
          </div>
        </section>

        <section className="workspace">
          <div className="workspace-main">
            <div className="card-header">
              <div>
                <div className="eyebrow">CREATE NEW REPORT</div>
                <h2>Generate Research Report</h2>
                <p>
                  Enter the company details and provide its
                  financial context document.
                </p>
              </div>

              <div className="step-indicator">
                <span className="step-active">01</span>
                <span className="step-line" />
                <span>02</span>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="company">
                <span className="label-number">01</span>
                Company Name
              </label>

              <div className="input-wrapper">
                <span className="input-icon">⌂</span>

                <input
                  id="company"
                  type="text"
                  placeholder="e.g. Eternal Ltd."
                  value={companyName}
                  onChange={(event) => {
                    setCompanyName(event.target.value);
                    setError("");
                  }}
                  disabled={loading}
                />

                {companyName.trim() && (
                  <span className="input-check">✓</span>
                )}
              </div>
            </div>

            <div className="form-group">
              <label>
                <span className="label-number">02</span>
                Financial Context
              </label>

              <input
                ref={fileInputRef}
                id="file-upload"
                type="file"
                accept=".pdf,.csv,.txt"
                onChange={handleFileChange}
                hidden
                disabled={loading}
              />

              {!file ? (
                <label
                  htmlFor="file-upload"
                  className={`upload-box ${
                    dragActive ? "drag-active" : ""
                  }`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  <div className="upload-top-line">
                    <span className="upload-status">SECURE UPLOAD</span>
                    <span className="upload-limit">MAX 50 MB</span>
                  </div>

                  <div className="upload-icon-large">↑</div>

                  <strong>Drop your financial document here</strong>

                  <span className="upload-action">
                    or <b>browse files</b>
                  </span>

                  <div className="format-pills">
                    <span>PDF</span>
                    <span>CSV</span>
                    <span>TXT</span>
                  </div>
                </label>
              ) : (
                <div className="selected-file">
                  <div className="file-icon">{getFileExtension()}</div>

                  <div className="file-details">
                    <strong title={file.name}>{file.name}</strong>
                    <span>
                      {getFileExtension()} · {getFileSize()}
                    </span>

                    <div className="file-ready">
                      <span>✓</span>
                      File ready for analysis
                    </div>
                  </div>

                  {!loading && (
                    <button
                      type="button"
                      className="remove-file"
                      onClick={removeFile}
                      aria-label="Remove file"
                    >
                      ×
                    </button>
                  )}
                </div>
              )}
            </div>

            {error && (
              <div className="error" role="alert">
                <div className="error-icon">!</div>

                <div>
                  <strong>Unable to generate report</strong>
                  <p>{error}</p>
                </div>
              </div>
            )}

            <button
              className="generate-button"
              onClick={generateReport}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner" />
                  <span>Generating Research Report</span>
                </>
              ) : (
                <>
                  <span>Generate Research Report</span>
                  <span className="button-arrow">→</span>
                </>
              )}
            </button>
          </div>

          <aside className="workspace-side">
            {loading ? (
              <div className="side-panel processing-panel">
                <div className="panel-kicker">AI WORKFLOW</div>

                <div className="ai-orb">
                  <span />
                  <span />
                  <span />
                </div>

                <h3>Research engine running</h3>
                <p>
                  Your financial context is being converted
                  into structured research intelligence.
                </p>

                <div className="workflow">
                  <div className="workflow-step done">
                    <span>✓</span>
                    <div>
                      <strong>Read document</strong>
                      <small>Source context loaded</small>
                    </div>
                  </div>

                  <div className="workflow-step active">
                    <span className="mini-spinner" />
                    <div>
                      <strong>Extract financials</strong>
                      <small>AI analysis in progress</small>
                    </div>
                  </div>

                  <div className="workflow-step">
                    <span>3</span>
                    <div>
                      <strong>Build report</strong>
                      <small>Tables and narrative</small>
                    </div>
                  </div>

                  <div className="workflow-step">
                    <span>4</span>
                    <div>
                      <strong>Prepare PDF</strong>
                      <small>Final document output</small>
                    </div>
                  </div>
                </div>

                <div className="progress">
                  <div className="progress-text">
                    <span>Processing intelligence</span>
                    <span>In progress</span>
                  </div>

                  <div className="progress-bar">
                    <div className="progress-fill" />
                  </div>
                </div>
              </div>
            ) : report ? (
              <div className="side-panel report-panel">
                <div className="panel-kicker">GENERATION COMPLETE</div>

                <div className="report-check">✓</div>

                <h3>Report ready</h3>

                <p>
                  Your structured financial research report
                  has been generated successfully.
                </p>

                <div className="report-summary">
                  <div>
                    <span>COMPANY</span>
                    <strong>{companyName.trim()}</strong>
                  </div>

                  <div>
                    <span>OUTPUT</span>
                    <strong>PDF REPORT</strong>
                  </div>

                  <div>
                    <span>STATUS</span>
                    <strong className="ready-text">READY</strong>
                  </div>
                </div>

                <a
                  className="download-button"
                  href={`http://localhost:8000${report.download_url}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <span>↓</span>
                  Download PDF Report
                  <span>→</span>
                </a>

                <button
                  type="button"
                  className="another-button"
                  onClick={generateAnother}
                >
                  Generate Another Report
                </button>
              </div>
            ) : (
              <div className="side-panel intelligence-panel">
                <div className="panel-kicker">WHAT YOU GET</div>

                <h3>From raw financials to research-ready output.</h3>

                <p>
                  Bull AI extracts the important numbers,
                  maps them into a structured research template,
                  and prepares a professional PDF report.
                </p>

                <div className="intelligence-list">
                  <div>
                    <span>01</span>
                    <strong>Financial extraction</strong>
                  </div>

                  <div>
                    <span>02</span>
                    <strong>Structured tables</strong>
                  </div>

                  <div>
                    <span>03</span>
                    <strong>AI narrative</strong>
                  </div>

                  <div>
                    <span>04</span>
                    <strong>Charts & PDF output</strong>
                  </div>
                </div>

                <div className="supported">
                  <span>SUPPORTED INPUTS</span>
                  <div>
                    <b>PDF</b>
                    <b>CSV</b>
                    <b>TXT</b>
                  </div>
                </div>
              </div>
            )}
          </aside>
        </section>

        <section className="trust-row">
          <div>
            <strong>PDF</strong>
            <span>Professional reports</span>
          </div>

          <div>
            <strong>CSV</strong>
            <span>Structured financial data</span>
          </div>

          <div>
            <strong>TXT</strong>
            <span>Text-based context</span>
          </div>

          <div>
            <strong>50 MB</strong>
            <span>Maximum file size</span>
          </div>
        </section>

        <footer>
          <span>Powered by Gemini AI</span>
          <span className="footer-dot">•</span>
          <span>Bull AI Financial Research</span>
          <span className="footer-dot">•</span>
          <span>Research Intelligence Platform</span>
        </footer>
      </main>
    </div>
  );
}

export default App;
