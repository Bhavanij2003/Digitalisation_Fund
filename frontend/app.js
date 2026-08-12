// app.js - shared helpers used by all pages
// Change API_BASE if the backend runs somewhere other than localhost:8000
const API_BASE = "http://127.0.0.1:8000";

function toast(message, type = "") {
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = message;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3800);
}

async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function apiPostJSON(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.message || data.error || "Request failed");
    err.data = data;
    err.status = res.status;
    throw err;
  }
  return data;
}

function statusBadge(status) {
  const safe = (status || "Unknown").replace(/\s/g, "");
  return `<span class="badge" data-status="${status}" style="background:var(--orange-bg);color:var(--orange)">${status}</span>`;
}

function confidenceBadge(band, score) {
  const label = score !== null && score !== undefined ? `${Math.round(score)}%` : "—";
  return `<span class="badge ${band}">${label}</span>`;
}

function fileUrl(path) {
  if (!path) return "";
  // paths are stored as absolute server paths; map to the served /files routes.
  // Normalise Windows backslashes to forward slashes first, since os.path.join
  // on Windows produces "...\data\uploads\xxx.png" (backslashes), not "/data/".
  const normalised = path.replace(/\\/g, "/");
  const marker = "/data/";
  const idx = normalised.indexOf(marker);
  if (idx === -1) return "";
  const rel = normalised.slice(idx + marker.length); // e.g. "uploads/xxx.png" or "processed/xxx.png"
  return `${API_BASE}/files/${rel}`;
}
