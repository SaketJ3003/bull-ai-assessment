# Bull AI — Financial Research Report Generator

An AI-powered financial research report generator that converts company financial documents into structured, downloadable equity research PDF reports.

The application uses **Google Gemini** to extract financial information from source documents and maps the extracted data into a Geojit-style research report structure.

---

## 🚀 Features

- Upload financial documents in **PDF, CSV, or TXT** format
- Enter the company name
- AI-powered financial data extraction using **Google Gemini**
- Structured JSON extraction with Pydantic validation
- Automatic mapping from AI output to the financial report schema
- Professional multi-page PDF report generation
- Financial tables and metrics
- Company overview and business summary
- Key highlights and risks
- Recommendation and valuation information
- Annual and quarterly financial data
- Profit & Loss, Balance Sheet and Cash Flow sections
- Financial ratios
- Recommendation history
- Automatically generated financial charts
- Colorful, visually structured PDF design
- PDF bookmarks/navigation
- One-click PDF download
- Graceful handling of unavailable/missing financial fields
- Retry handling for temporary Gemini/API failures
- Responsive React frontend
- FastAPI backend

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │      React UI        │
                    │     React + Vite     │
                    └──────────┬───────────┘
                               │
                               │ File Upload
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    │      /api/upload     │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
          ┌─────────────┐             ┌──────────────┐
          │   Parsers   │             │  Gemini AI   │
          │  PDF/CSV/TXT│             │  Extraction  │
          └──────┬──────┘             └──────┬───────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌──────────────────────┐
                    │  Pydantic Financial  │
                    │       Models         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Mapper         │
                    │ AI → Report Schema   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    PDF Generator     │
                    │ ReportLab + Charts   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Downloadable PDF   │
                    └──────────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

### AI
- Google Gemini API
- `google-genai`
- Structured JSON output

### Document Processing
- `pypdf`
- `pandas`
- Custom TXT parser

### PDF Generation & Visualization
- ReportLab
- Matplotlib

### Configuration
- `python-dotenv`

---

## 📁 Project Structure

```text
bull-ai-assessment/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── parsers/
│   │   ├── routes/
│   │   ├── services/
│   │   └── pdf/
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── sample_data/
│   ├── test_financials.csv
│   └── test_financials.txt
│
├── sample_outputs/
│   ├── Eternal_Ltd_report.pdf
│   └── JSW_Energy_report.pdf
│
├── README.md
└── .gitignore
```

> The exact test filenames/folders may differ depending on the final cleaned repository structure.

---

# ⚙️ Installation & Setup

## 1. Clone the repository

```bash
git clone https://github.com/SaketJ3003/bull-ai-assessment
cd bull-ai-assessment
```

---

## 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a Python virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Gemini API

Create a file:

```text
backend/.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

The real `.env` file must **not** be committed to GitHub.

Use `.env.example` as the safe configuration template.

---

## 4. Start the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

---

# 💻 Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 📄 Supported Input Formats

The application supports three input formats.

### PDF

Financial reports, annual reports, research documents, and other financial PDFs.

### CSV

Structured financial data, for example:

```csv
Year,Sales,Sales Growth,EBITDA,EBITDA Margin,Adjusted PAT,EPS
FY25A,20243,67.1,637,3.1,527,0.6
FY26E,35020,73.0,1248,3.6,927,1.0
FY27E,54632,56.0,3575,6.5,2643,2.7
```

### TXT

Plain-text financial information containing company details, financial metrics, summaries, highlights, and other financial context.

---

# 🤖 AI Processing Pipeline

```text
Upload Document
       ↓
Validate File
       ↓
Parse Document
       ↓
Send Financial Context to Gemini
       ↓
Structured JSON Extraction
       ↓
Pydantic Validation
       ↓
AI Schema → Financial Report Schema
       ↓
Generate Financial Charts
       ↓
Generate PDF
       ↓
Return Download URL
```

The AI extraction process is designed to avoid fabricating unavailable financial information. When information is not present in the source document, the corresponding field can remain empty or null.

---

# 📊 Generated Report

The generated report follows the structure of the provided equity research sample.

### Page 1
- Research header
- Company information
- Recommendation
- Target price
- Current market price
- Company data
- Shareholding
- Price performance
- Outlook & valuation
- Quarterly financials
- Annual financial summary

### Page 2
- Estimate changes
- Key highlights
- Financial charts

### Page 3
- Consolidated financials
- Profit & Loss
- Balance Sheet
- Cash Flow
- Financial ratios

### Page 4
- Recommendation history
- Investment rating criteria
- Risks
- Disclaimer / disclosures

---

# 📈 Charts

Financial charts are generated programmatically from structured financial data.

Current chart types include:

- Revenue
- EBITDA
- Adjusted PAT

The chart generation module is designed so additional metrics can be added later.

---

# 🔌 API

## Generate Research Report

### Endpoint

```http
POST /api/upload
```

### Form Data

```text
company_name: string
file: PDF | CSV | TXT
```

### Example Successful Response

```json
{
  "success": true,
  "message": "Financial report generated successfully.",
  "company_name": "Example Company",
  "report": {
    "filename": "Example_Company_xxxxxxxx_financial_report.pdf",
    "download_url": "/api/reports/Example_Company_xxxxxxxx_financial_report.pdf"
  }
}
```

---

## Download Report

```http
GET /api/reports/{filename}
```

Returns the generated PDF report.

---

# 🧪 Testing

The project includes tests for document parsing and report generation workflows.

Examples include:

```bash
python -m app.test_pdf
```

CSV workflow:

```text
CSV → Gemini → Mapper → PDF
```

TXT workflow:

```text
TXT → Gemini → Mapper → PDF
```

Parser tests cover CSV and TXT input handling.

> Run the test commands from the final repository structure. Test module paths may change if the test files are moved into `backend/tests/`.

---

# 🔐 Security & Error Handling

The application includes:

- Environment-based API key configuration
- `.env` excluded from version control
- File extension validation
- File size validation
- Safe uploaded filenames
- Safe generated filenames
- Protection against path traversal when downloading reports
- User-friendly frontend error messages
- Handling for empty/unreadable files
- Handling for unsupported file types
- Retry logic for temporary Gemini failures
- Handling for rate-limit and service-unavailable responses

Temporary Gemini/API errors such as `429`, `500`, `502`, `503`, and `504` are retried with backoff where appropriate.

---

# 🎯 Assessment Requirements

| Requirement | Status |
|---|---|
| PDF input | ✅ |
| CSV input | ✅ |
| TXT input | ✅ |
| AI financial extraction | ✅ |
| Structured financial mapping | ✅ |
| Financial tables | ✅ |
| Narrative sections | ✅ |
| Financial charts | ✅ |
| Missing-field handling | ✅ |
| Downloadable PDF | ✅ |
| Multi-page research report | ✅ |
| Responsive UI | ✅ |
| Error handling | ✅ |
| Sample generated reports | ✅ |

---

# 📦 Sample Data & Outputs

Sample input files are provided in:

```text
sample_data/
```

Generated sample reports are provided in:

```text
sample_outputs/
```

These demonstrate the end-to-end document-to-report workflow.

---

# 🚀 Future Improvements

Possible future enhancements include:

- Additional financial chart types
- XLSX input support
- More advanced PDF/table extraction
- Persistent report history
- Authentication
- Database-backed report storage
- Cloud deployment
- Streaming AI progress updates
- Multiple research report templates
- More extensive financial validation

---

## 👨‍💻 Project

Developed as part of the **Bull AI Software Engineer Assessment**.

The project demonstrates:

- Full-stack application development
- AI integration with Google Gemini
- Structured financial data extraction
- Document processing
- API development
- PDF generation
- Financial data visualization
- Error handling
- Responsive frontend development
