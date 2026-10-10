(() => {
  const groups = {
    ordersFields: [
      ["IXC_OS_TABLE", "Tabela de ordens", "Ex.: su_oss_chamado"],
      ["IXC_OS_ID_FIELD", "Número da OS"], ["IXC_OS_STATUS_FIELD", "Status"],
      ["IXC_OS_SUBJECT_ID_FIELD", "Código do assunto"], ["IXC_OS_BRANCH_ID_FIELD", "Código da filial"],
      ["IXC_OS_BRANCH_NAME_FIELD", "Nome da filial"], ["IXC_OS_TECH_ID_FIELD", "Código do técnico"],
      ["IXC_OS_OPENED_AT_FIELD", "Data de abertura"], ["IXC_OS_EXECUTION_AT_FIELD", "Data de execução"],
      ["IXC_OS_CLOSED_AT_FIELD", "Data de conclusão"], ["IXC_OS_DUE_AT_FIELD", "Prazo"],
    ],
    lookupFields: [
      ["IXC_SUBJECT_TABLE", "Tabela de assuntos"], ["IXC_SUBJECT_ID_FIELD", "Código do assunto"], ["IXC_SUBJECT_NAME_FIELD", "Nome do assunto"],
      ["IXC_TECH_TABLE", "Tabela de técnicos"], ["IXC_TECH_ID_FIELD", "Código do técnico"], ["IXC_TECH_NAME_FIELD", "Nome do técnico"],
      ["IXC_CITY_TABLE", "Tabela de cidades"], ["IXC_CITY_ID_FIELD", "Código da cidade"], ["IXC_CITY_NAME_FIELD", "Nome da cidade"],
    ],
    syncFields: [
      ["IXC_STATUS_CLOSED", "Status considerados concluídos", "wide"], ["IXC_STATUS_EXECUTION", "Status em execução", "wide"],
      ["IXC_PAGE_SIZE", "Registros por consulta", "number"], ["IXC_MAX_PAGES", "Limite de páginas", "number"],
      ["IXC_FULL_SYNC_EVERY_N_RUNS", "Sincronização completa a cada ciclos", "number"], ["IXC_SYNC_INTERVAL_SECONDS", "Intervalo (segundos)", "number"],
      ["IXC_HTTP_TIMEOUT_SECONDS", "Tempo limite (segundos)", "number"], ["IXC_INCREMENTAL_SYNC", "Sincronização incremental", "check"],
      ["IXC_SYNC_ON_STARTUP", "Sincronizar ao iniciar", "check"], ["IXC_AUTO_SYNC", "Sincronização automática", "check"],
      ["IXC_VERIFY_SSL", "Validar certificado SSL", "check"],
    ],
    preferencesFields: [
      ["APP_TIMEZONE", "Fuso horário", "text", "Ex.: America/Recife"], ["APP_DB_PATH", "Caminho do banco de dados"],
      ["APP_DASHBOARD_REFRESH_SECONDS", "Atualização do painel (segundos)", "number"],
      ["APP_FILTER_OPTIONS_REFRESH_SECONDS", "Atualização dos filtros (segundos)", "number"],
      ["APP_SUBJECT_GROUPS", "Grupos de assuntos", "wide", "grupo=termo1|termo2;outro=termo3|termo4"],
    ],
  };
  const numberFields = new Set(["IXC_PAGE_SIZE", "IXC_MAX_PAGES", "IXC_FULL_SYNC_EVERY_N_RUNS", "IXC_SYNC_INTERVAL_SECONDS", "IXC_HTTP_TIMEOUT_SECONDS", "APP_DASHBOARD_REFRESH_SECONDS", "APP_FILTER_OPTIONS_REFRESH_SECONDS"]);
  const checkFields = new Set(["IXC_INCREMENTAL_SYNC", "IXC_SYNC_ON_STARTUP", "IXC_AUTO_SYNC", "IXC_VERIFY_SSL"]);
  const form = document.getElementById("settingsForm");
  const feedback = document.getElementById("feedback");
  const saveBtn = document.getElementById("saveBtn");
  const testBtn = document.getElementById("testBtn");
  const discoverBtn = document.getElementById("discoverBtn");
  const dockFeedback = document.getElementById("dockFeedback");
  let isDirty = false;

  function createFields() {
    for (const [containerId, fields] of Object.entries(groups)) {
      const container = document.getElementById(containerId);
      for (const [id, label, kind = "text", placeholder = ""] of fields) {
        if (kind === "check") {
          const row = document.createElement("label");
          row.className = "check-row";
          row.innerHTML = `<input id="${id}" name="${id}" type="checkbox"><span>${label}</span>`;
          container.append(row);
          continue;
        }
        const wrapper = document.createElement("label");
        wrapper.className = `field${kind === "wide" ? " wide" : ""}`;
        const inputType = kind === "number" ? "number" : "text";
        const extra = kind === "number" ? ' inputmode="numeric" step="1"' : "";
        wrapper.innerHTML = `<span>${label}</span><input id="${id}" name="${id}" type="${inputType}"${extra}${placeholder ? ` placeholder="${placeholder}"` : ""}>`;
        container.append(wrapper);
      }
    }
  }

  function showMessage(message, kind = "") {
    feedback.textContent = message;
    feedback.className = `feedback${kind ? ` ${kind}` : ""}`;
    feedback.hidden = false;
    dockFeedback.textContent = message;
    dockFeedback.className = `dock-feedback${kind ? ` ${kind}` : ""}`;
    dockFeedback.hidden = false;
  }

  async function request(url, options = {}) {
    const response = await fetch(url, { cache: "no-store", ...options });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      const detail = data.detail;
      let message = typeof detail === "string" ? detail : Array.isArray(detail) ? detail.map((item) => item.msg || item.message || String(item)).join("; ") : detail?.message || detail?.msg;
      throw new Error(message || `Não foi possível concluir a solicitação (HTTP ${response.status}).`);
    }
    return data;
  }

  function fill(values) {
    for (const [id, value] of Object.entries(values)) {
      const input = document.getElementById(id);
      if (!input) continue;
      if (id === "IXC_TOKEN") {
        input.value = "";
        input.placeholder = value ? "Credencial salva · digite para substituir" : "Cole a credencial ID:token";
      } else if (checkFields.has(id)) input.checked = value === true || String(value).toLowerCase() === "true";
      else input.value = value ?? "";
    }
    document.getElementById("connectionState").textContent = values.IXC_BASE_URL
      ? (values.IXC_TOKEN ? "IXC configurado" : "Credencial pendente")
      : "Configure a conexão IXC";
    isDirty = false;
    for (const input of form.querySelectorAll("input")) input.disabled = false;
    saveBtn.disabled = false;
    testBtn.disabled = false;
    discoverBtn.disabled = false;
  }

  async function load() {
    try {
      const data = await request(`/api/settings?_ts=${Date.now()}`);
      fill(data.values || {});
    } catch (error) {
      showMessage(error.message || "Falha ao carregar as configurações.", "error");
      document.getElementById("connectionState").textContent = "Não foi possível carregar";
    }
  }

  function collect() {
    const values = {};
    for (const fields of Object.values(groups)) {
      for (const [id] of fields) {
        const input = document.getElementById(id);
        if (checkFields.has(id)) values[id] = input.checked;
        else if (numberFields.has(id)) values[id] = input.value.trim() === "" ? 0 : Number(input.value);
        else values[id] = input.value.trim();
      }
    }
    values.IXC_BASE_URL = document.getElementById("IXC_BASE_URL").value.trim();
    const token = document.getElementById("IXC_TOKEN").value.trim();
    // Empty means keep the server-side secret; the API also accepts its mask as unchanged.
    values.IXC_TOKEN = token || "********";
    return values;
  }

  async function save(event) {
    event?.preventDefault();
    saveBtn.disabled = true;
    saveBtn.textContent = "Salvando…";
    try {
      const data = await request("/api/settings", { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(collect()) });
      fill(data.values || {});
      showMessage(data.message || "Configurações salvas e aplicadas.", "success");
    } catch (error) { showMessage(error.message || "Falha ao salvar as configurações.", "error"); }
    finally { saveBtn.disabled = false; saveBtn.innerHTML = 'Salvar alterações <span aria-hidden="true">→</span>'; }
  }

  async function testConnection() {
    if (isDirty) {
      showMessage("Salve as alterações antes de testar a conexão.", "error");
      return;
    }
    testBtn.disabled = true;
    testBtn.textContent = "Testando conexão…";
    const result = document.getElementById("testResult");
    result.textContent = "";
    try {
      const data = await request("/api/settings/test-connection", { method: "POST" });
      const keys = (data.sample_keys || []).slice(0, 5).join(", ");
      result.textContent = `Conexão OK · ${data.table || "IXC"} · ${data.records_sampled ?? 0} registro(s)${keys ? ` · ${keys}` : ""}`;
      showMessage("Conexão com o IXC testada com sucesso.", "success");
    } catch (error) { result.textContent = ""; showMessage(error.message || "Falha no teste de conexão.", "error"); }
    finally { testBtn.disabled = false; testBtn.innerHTML = 'Testar conexão <span aria-hidden="true">↗</span>'; }
  }

  async function discover() {
    if (isDirty) {
      showMessage("Salve as alterações antes de descobrir campos.", "error");
      return;
    }
    discoverBtn.disabled = true;
    discoverBtn.textContent = "Buscando campos…";
    try {
      const [os, subject, tech] = await Promise.all([
        request("/api/discovery/os-fields"), request("/api/discovery/subject-fields"), request("/api/discovery/tech-fields"),
      ]);
      const suggestions = { ...(os.env_suggestions || {}) };
      if (subject.suggested_id_field) suggestions.IXC_SUBJECT_ID_FIELD = subject.suggested_id_field;
      if (subject.suggested_name_field) suggestions.IXC_SUBJECT_NAME_FIELD = subject.suggested_name_field;
      if (tech.suggested_id_field) suggestions.IXC_TECH_ID_FIELD = tech.suggested_id_field;
      if (tech.suggested_name_field) suggestions.IXC_TECH_NAME_FIELD = tech.suggested_name_field;
      let applied = 0;
      for (const [id, value] of Object.entries(suggestions)) {
        const input = document.getElementById(id);
        if (input && !checkFields.has(id) && value) { input.value = value; applied += 1; }
      }
      isDirty = applied > 0;
      showMessage(`${applied} sugestão(ões) aplicada(s) ao formulário. Salve para confirmar.`, "success");
    } catch (error) { showMessage(error.message || "Falha ao descobrir campos.", "error"); }
    finally { discoverBtn.disabled = false; discoverBtn.textContent = "Descobrir campos"; }
  }

  createFields();
  for (const input of form.querySelectorAll("input")) input.disabled = true;
  form.addEventListener("submit", save);
  form.addEventListener("input", () => { isDirty = true; });
  form.addEventListener("change", () => { isDirty = true; });
  testBtn.addEventListener("click", testConnection);
  discoverBtn.addEventListener("click", discover);
  load();
})();
