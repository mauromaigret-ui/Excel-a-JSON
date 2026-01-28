const state = {
  fileId: null,
  sheets: [],
};

const statusEl = document.getElementById("status");
const fileInput = document.getElementById("fileInput");
const fileMeta = document.getElementById("fileMeta");
const sheetList = document.getElementById("sheetList");
const jsonPreview = document.getElementById("jsonPreview");
const auditResults = document.getElementById("auditResults");
const previewBtn = document.getElementById("previewBtn");
const auditBtn = document.getElementById("auditBtn");
const exportBtn = document.getElementById("exportBtn");
const includeAuditEl = document.getElementById("includeAudit");

function setStatus(message) {
  statusEl.textContent = message;
}

function setFileMeta(text) {
  fileMeta.textContent = text;
}

fileInput.addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  setStatus("Subiendo archivo...");
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/import", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(await response.text());
    }

    const data = await response.json();
    state.fileId = data.file_id;
    state.sheets = data.sheets || [];

    setFileMeta(`Archivo: ${file.name} · ${state.sheets.length} hojas detectadas`);
    renderSheets();
    setStatus("Archivo importado");
  } catch (error) {
    setStatus("Error al importar");
    setFileMeta("No se pudo leer el archivo.");
    console.error(error);
  }
});

function renderSheets() {
  sheetList.innerHTML = "";
  if (!state.sheets.length) {
    sheetList.innerHTML = '<div class="empty">Carga un Excel para ver las hojas.</div>';
    return;
  }

  state.sheets.forEach((sheet) => {
    const card = document.createElement("div");
    card.className = "sheet-card";
    card.dataset.sheet = sheet.name;

    const header = document.createElement("div");
    header.className = "sheet-header";

    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "sheet-enabled";
    checkbox.checked = true;
    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(` ${sheet.name}`));

    const meta = document.createElement("div");
    meta.className = "sheet-meta";
    meta.textContent = `${sheet.rows} filas · ${sheet.columns} columnas`;

    header.appendChild(label);
    header.appendChild(meta);

    const baseRow = document.createElement("div");
    baseRow.className = "sheet-meta";
    baseRow.style.marginTop = "8px";
    baseRow.innerHTML = `Base del censo: <input class="sheet-base" placeholder="censo_base_1" />`;

    const table = document.createElement("table");
    table.className = "mapping-table";
    table.innerHTML = `
      <thead>
        <tr>
          <th>Columna Excel</th>
          <th>Campo JSON</th>
          <th>Tipo</th>
          <th>Req.</th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    `;

    const tbody = table.querySelector("tbody");

    (sheet.columns_original || []).forEach((col) => {
      const row = document.createElement("tr");
      row.dataset.col = col;
      row.innerHTML = `
        <td>${col}</td>
        <td><input class="map-target" value="${col}" /></td>
        <td>
          <select class="map-type">
            <option value="string">Texto</option>
            <option value="number">Número</option>
            <option value="date">Fecha</option>
            <option value="boolean">Booleano</option>
          </select>
        </td>
        <td><input type="checkbox" class="map-required" /></td>
      `;
      tbody.appendChild(row);
    });

    const includeUnmapped = document.createElement("label");
    includeUnmapped.className = "sheet-meta";
    includeUnmapped.style.display = "block";
    includeUnmapped.style.marginTop = "10px";
    includeUnmapped.innerHTML = `<input type="checkbox" class="include-unmapped" /> Incluir columnas no mapeadas`;

    card.appendChild(header);
    card.appendChild(baseRow);
    card.appendChild(table);
    card.appendChild(includeUnmapped);

    sheetList.appendChild(card);
  });
}

function collectProfiles() {
  const profiles = [];
  const cards = sheetList.querySelectorAll(".sheet-card");

  cards.forEach((card) => {
    const sheetName = card.dataset.sheet;
    const enabled = card.querySelector(".sheet-enabled").checked;
    if (!enabled) return;

    const base = card.querySelector(".sheet-base").value || null;
    const includeUnmapped = card.querySelector(".include-unmapped").checked;
    const mappings = [];

    card.querySelectorAll("tbody tr").forEach((row) => {
      const from = row.dataset.col;
      const to = row.querySelector(".map-target").value || from;
      const type = row.querySelector(".map-type").value;
      const required = row.querySelector(".map-required").checked;
      mappings.push({ from, to, type, required });
    });

    profiles.push({ sheet: sheetName, base, mappings, include_unmapped: includeUnmapped });
  });

  return profiles;
}

previewBtn.addEventListener("click", async () => {
  if (!state.fileId) return;
  setStatus("Generando vista previa...");
  jsonPreview.textContent = "Cargando...";

  try {
    const profiles = collectProfiles();
    const response = await fetch("/map", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ file_id: state.fileId, profiles, preview_rows: 5, transformations: [] }),
    });

    if (!response.ok) {
      throw new Error(await response.text());
    }

    const data = await response.json();
    jsonPreview.textContent = JSON.stringify(data.preview, null, 2);
    setStatus("Vista previa lista");
  } catch (error) {
    jsonPreview.textContent = "Error al generar preview.";
    setStatus("Error en preview");
    console.error(error);
  }
});

auditBtn.addEventListener("click", async () => {
  if (!state.fileId) return;
  setStatus("Auditando...");
  auditResults.textContent = "Auditando...";

  try {
    const profiles = collectProfiles();
    const response = await fetch("/audit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ file_id: state.fileId, profiles, transformations: [] }),
    });

    if (!response.ok) {
      throw new Error(await response.text());
    }

    const data = await response.json();
    renderAudit(data.audits || []);
    setStatus("Auditoría lista");
  } catch (error) {
    auditResults.textContent = "Error al auditar.";
    setStatus("Error en auditoría");
    console.error(error);
  }
});

function renderAudit(audits) {
  if (!audits.length) {
    auditResults.textContent = "Sin auditoría.";
    return;
  }

  auditResults.innerHTML = "";
  audits.forEach((audit) => {
    const div = document.createElement("div");
    div.className = "audit-item";
    div.innerHTML = `
      <span class="audit-status ${audit.status}">${audit.status.toUpperCase()}</span>
      <strong>${audit.sheet}</strong><br />
      Filas Excel: ${audit.summary.rows_excel} · Filas JSON: ${audit.summary.rows_json} · Mismatches: ${audit.summary.mismatches}
    `;
    auditResults.appendChild(div);
  });
}

exportBtn.addEventListener("click", async () => {
  if (!state.fileId) return;
  setStatus("Exportando...");

  try {
    const profiles = collectProfiles();
    const response = await fetch("/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        file_id: state.fileId,
        profiles,
        transformations: [],
        include_audit: includeAuditEl.checked,
        pretty: true,
      }),
    });

    if (!response.ok) {
      throw new Error(await response.text());
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "censo_2024.json";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    setStatus("JSON exportado");
  } catch (error) {
    setStatus("Error al exportar");
    console.error(error);
  }
});
