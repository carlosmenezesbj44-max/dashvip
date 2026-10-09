const dateInput = document.getElementById("dateInput");
const startDateInput = document.getElementById("startDateInput");
const endDateInput = document.getElementById("endDateInput");
const subjectFilterRows = document.getElementById("subjectFilterRows");
const subjectAddBtn = document.getElementById("subjectAddBtn");
const subjectGroupFilter = document.getElementById("subjectGroupFilter");
const createSubjectGroupBtn = document.getElementById("createSubjectGroupBtn");
const deleteSubjectGroupBtn = document.getElementById("deleteSubjectGroupBtn");
const branchFilter = document.getElementById("branchFilter");
const applyFiltersBtn = document.getElementById("applyFiltersBtn");
const clearFiltersBtn = document.getElementById("clearFiltersBtn");

const syncBtn = document.getElementById("syncBtn");
const syncFullBtn = document.getElementById("syncFullBtn");
const meta = document.getElementById("meta");
const subjectsTable = document.getElementById("subjectsTable");
const techSlaTable = document.getElementById("techSlaTable");
const completedValue = document.getElementById("completedValue");
const activeValue = document.getElementById("activeValue");
const slaWithinValue = document.getElementById("slaWithinValue");
const slaOverdueValue = document.getElementById("slaOverdueValue");
const techniciansExecutingValue = document.getElementById("techniciansExecutingValue");
const technicianStartedOrdersValue = document.getElementById("technicianStartedOrdersValue");
const rescheduledTodayValue = document.getElementById("rescheduledTodayValue");
const avgExecutionMinutesValue = document.getElementById("avgExecutionMinutesValue");
const weeklyFinishedValue = document.getElementById("weeklyFinishedValue");
const weeklyInstallationsValue = document.getElementById("weeklyInstallationsValue");
const weeklyInstallationsPercent = document.getElementById("weeklyInstallationsPercent");
const weeklyProductiveDayValue = document.getElementById("weeklyProductiveDayValue");
const weeklyProductiveDayMeta = document.getElementById("weeklyProductiveDayMeta");
const weeklyTechniciansValue = document.getElementById("weeklyTechniciansValue");
const weeklyTechniciansMeta = document.getElementById("weeklyTechniciansMeta");
const weeklyRangeValue = document.getElementById("weeklyRangeValue");
const weeklyScopeValue = document.getElementById("weeklyScopeValue");
const weeklyBranchesTitle = document.getElementById("weeklyBranchesTitle");
const weeklyBranchesTable = document.getElementById("weeklyBranchesTable");
const weeklyDailyBars = document.getElementById("weeklyDailyBars");
const weeklyDailyTotalValue = document.getElementById("weeklyDailyTotalValue");
const weeklyDailyPeakValue = document.getElementById("weeklyDailyPeakValue");
const weeklyDailyPeakMeta = document.getElementById("weeklyDailyPeakMeta");
const weeklyDailyPeakPercentValue = document.getElementById("weeklyDailyPeakPercentValue");
const weeklyDailySundayValue = document.getElementById("weeklyDailySundayValue");
const weeklyShiftCards = document.getElementById("weeklyShiftCards");
const weeklyStartDateInput = document.getElementById("weeklyStartDateInput");
const weeklyEndDateInput = document.getElementById("weeklyEndDateInput");
const metricCards = Array.from(document.querySelectorAll("#dashboardTab .metric-card"));
const cardOrdersModalOverlay = document.getElementById("cardOrdersModalOverlay");
const cardOrdersModalClose = document.getElementById("cardOrdersModalClose");
const cardOrdersModalTitle = document.getElementById("cardOrdersModalTitle");
const cardOrdersModalMeta = document.getElementById("cardOrdersModalMeta");
const cardOrdersModalTable = document.getElementById("cardOrdersModalTable");

const tabDashboardBtn = document.getElementById("tabDashboardBtn");
const tabProductivityBtn = document.getElementById("tabProductivityBtn");
const tabInstallationsBtn = document.getElementById("tabInstallationsBtn");
const tabOperationsBtn = document.getElementById("tabOperationsBtn");
const tabSettingsBtn = document.getElementById("tabSettingsBtn");
const dashboardTab = document.getElementById("dashboardTab");
const productivityTab = document.getElementById("productivityTab");
const installationsTab = document.getElementById("installationsTab");
const operationsTab = document.getElementById("operationsTab");
const settingsTab = document.getElementById("settingsTab");

const prodStartDateInput = document.getElementById("prodStartDateInput");
const prodEndDateInput = document.getElementById("prodEndDateInput");
const prodSubjectFilterRows = document.getElementById("prodSubjectFilterRows");
const prodSubjectAddBtn = document.getElementById("prodSubjectAddBtn");
const prodSubjectGroupFilter = document.getElementById("prodSubjectGroupFilter");
const prodBranchFilter = document.getElementById("prodBranchFilter");
const prodTechnicianFilter = document.getElementById("prodTechnicianFilter");
const prodStatusFilter = document.getElementById("prodStatusFilter");
const prodApplyFiltersBtn = document.getElementById("prodApplyFiltersBtn");
const prodClearFiltersBtn = document.getElementById("prodClearFiltersBtn");
const productivityMeta = document.getElementById("productivityMeta");
const prodTechniciansTotalValue = document.getElementById("prodTechniciansTotalValue");
const prodOrdersHandledValue = document.getElementById("prodOrdersHandledValue");
const prodOrdersStartedValue = document.getElementById("prodOrdersStartedValue");
const prodOrdersFinishedValue = document.getElementById("prodOrdersFinishedValue");
const prodAvgSlaValue = document.getElementById("prodAvgSlaValue");
const prodAvgExecutionValue = document.getElementById("prodAvgExecutionValue");
const productivityTable = document.getElementById("productivityTable");
const productivityOrdersMeta = document.getElementById("productivityOrdersMeta");
const productivityOrdersTable = document.getElementById("productivityOrdersTable");
const installationsStartDateInput = document.getElementById("installationsStartDateInput");
const installationsEndDateInput = document.getElementById("installationsEndDateInput");
const installationsBranchSelect = document.getElementById("installationsBranchSelect");
const installationsCitySelect = document.getElementById("installationsCitySelect");
const installationsSubjectField = document.getElementById("installationsSubjectField");
const installationsSubjectFilterRows = document.getElementById("installationsSubjectFilterRows");
const installationsSubjectAddBtn = document.getElementById("installationsSubjectAddBtn");
const installationsSubjectGroupFilter = document.getElementById("installationsSubjectGroupFilter");
const installationsToggleSubjectsBtn = document.getElementById("installationsToggleSubjectsBtn");
const installationsSubjectSummary = document.getElementById("installationsSubjectSummary");
const installationsPresetSelect = document.getElementById("installationsPresetSelect");
const installationsPresetNameInput = document.getElementById("installationsPresetNameInput");
const installationsSavePresetBtn = document.getElementById("installationsSavePresetBtn");
const installationsLoadPresetBtn = document.getElementById("installationsLoadPresetBtn");
const installationsDeletePresetBtn = document.getElementById("installationsDeletePresetBtn");
const installationsToggleCollaboratorsBtn = document.getElementById("installationsToggleCollaboratorsBtn");
const installationsCollaboratorPanel = document.getElementById("installationsCollaboratorPanel");
const installationsCollaboratorSummary = document.getElementById("installationsCollaboratorSummary");
const installationsCollaboratorSearch = document.getElementById("installationsCollaboratorSearch");
const installationsCollaboratorList = document.getElementById("installationsCollaboratorList");
const installationsSelectAllBtn = document.getElementById("installationsSelectAllBtn");
const installationsClearCollaboratorsBtn = document.getElementById("installationsClearCollaboratorsBtn");
const installationsApplyDateBtn = document.getElementById("installationsApplyDateBtn");
const installationsRangeValue = document.getElementById("installationsRangeValue");
const installationsScopeValue = document.getElementById("installationsScopeValue");
const installationsTotalValue = document.getElementById("installationsTotalValue");
const installationsTopDayValue = document.getElementById("installationsTopDayValue");
const installationsTopDayMeta = document.getElementById("installationsTopDayMeta");
const installationsDailyBars = document.getElementById("installationsDailyBars");
const installationsTechnicianList = document.getElementById("installationsTechnicianList");
const installationsSubTabButtons = Array.from(document.querySelectorAll(".installations-subtab-btn"));
const installationsSubTabPanels = Array.from(document.querySelectorAll(".installations-subtab-panel"));
const installationsProductivityTable = document.getElementById("installationsProductivityTable");
const installationsProductivitySummary = document.getElementById("installationsProductivitySummary");
const installationsSubjectMedianBars = document.getElementById("installationsSubjectMedianBars");
const installationsSubjectMedianSummary = document.getElementById("installationsSubjectMedianSummary");
const installationsTopInstallerName = document.getElementById("installationsTopInstallerName");
const installationsTopInstallerCount = document.getElementById("installationsTopInstallerCount");
const installationsTopInstallerRate = document.getElementById("installationsTopInstallerRate");

const boardDateInput = document.getElementById("boardDateInput");
const boardResponsibleInput = document.getElementById("boardResponsibleInput");
const boardShiftInput = document.getElementById("boardShiftInput");
const boardTeamInput = document.getElementById("boardTeamInput");
const boardGeneralNotesInput = document.getElementById("boardGeneralNotesInput");
const boardTechnicianRows = document.getElementById("boardTechnicianRows");
const boardTechnicianAddBtn = document.getElementById("boardTechnicianAddBtn");
const boardStatusRows = document.getElementById("boardStatusRows");
const boardStatusAddBtn = document.getElementById("boardStatusAddBtn");
const boardBranchFilter = document.getElementById("boardBranchFilter");
const boardSubjectFilter = document.getElementById("boardSubjectFilter");
const boardLoadBtn = document.getElementById("boardLoadBtn");
const boardAddRowBtn = document.getElementById("boardAddRowBtn");
const boardSaveBtn = document.getElementById("boardSaveBtn");
const boardSavedListSelect = document.getElementById("boardSavedListSelect");
const boardDelayReportSavedListSelect = document.getElementById("boardDelayReportSavedListSelect");
const boardLoadSavedBtn = document.getElementById("boardLoadSavedBtn");
const boardDeleteListBtn = document.getElementById("boardDeleteListBtn");
const boardDelayReportBtn = document.getElementById("boardDelayReportBtn");
const boardFeedback = document.getElementById("boardFeedback");
const boardTotalOrdersValue = document.getElementById("boardTotalOrdersValue");
const boardOpenOrdersValue = document.getElementById("boardOpenOrdersValue");
const boardExecutionOrdersValue = document.getElementById("boardExecutionOrdersValue");
const boardClosedOrdersValue = document.getElementById("boardClosedOrdersValue");
const boardSummaryNote = document.getElementById("boardSummaryNote");
const operationsBoardTable = document.getElementById("operationsBoardTable");
const boardOsIdList = document.getElementById("boardOsIdList");
const boardTimeSlotList = document.getElementById("boardTimeSlotList");
const boardOrderDetailsMeta = document.getElementById("boardOrderDetailsMeta");
const boardOrderDetailsGrid = document.getElementById("boardOrderDetailsGrid");
const boardDelayReportModalOverlay = document.getElementById("boardDelayReportModalOverlay");
const boardDelayReportModalClose = document.getElementById("boardDelayReportModalClose");
const boardDelayReportPrintBtn = document.getElementById("boardDelayReportPrintBtn");
const boardDelayReportModalTitle = document.getElementById("boardDelayReportModalTitle");
const boardDelayReportMeta = document.getElementById("boardDelayReportMeta");
const boardDelayReportTableWrap = document.getElementById("boardDelayReportTableWrap");
const delayReportPrintHost = document.getElementById("delayReportPrintHost");
const boardCommentModalOverlay = document.getElementById("boardCommentModalOverlay");
const boardCommentModalClose = document.getElementById("boardCommentModalClose");
const boardCommentModalMeta = document.getElementById("boardCommentModalMeta");
const boardCommentTextarea = document.getElementById("boardCommentTextarea");
const boardCommentSaveBtn = document.getElementById("boardCommentSaveBtn");
const boardCommentCancelBtn = document.getElementById("boardCommentCancelBtn");

const settingsFeedback = document.getElementById("settingsFeedback");
const saveSettingsBtn = document.getElementById("saveSettingsBtn");
const testConnectionBtn = document.getElementById("testConnectionBtn");
const autoDiscoveryBtn = document.getElementById("autoDiscoveryBtn");

const settingsFields = [
  "IXC_BASE_URL",
  "IXC_TOKEN",
  "IXC_OS_TABLE",
  "IXC_OS_ID_FIELD",
  "IXC_OS_STATUS_FIELD",
  "IXC_OS_SUBJECT_ID_FIELD",
  "IXC_OS_BRANCH_ID_FIELD",
  "IXC_OS_BRANCH_NAME_FIELD",
  "IXC_OS_TECH_ID_FIELD",
  "IXC_OS_OPENED_AT_FIELD",
  "IXC_OS_EXECUTION_AT_FIELD",
  "IXC_OS_CLOSED_AT_FIELD",
  "IXC_OS_DUE_AT_FIELD",
  "IXC_SUBJECT_TABLE",
  "IXC_SUBJECT_ID_FIELD",
  "IXC_SUBJECT_NAME_FIELD",
  "IXC_TECH_TABLE",
  "IXC_TECH_ID_FIELD",
  "IXC_TECH_NAME_FIELD",
  "IXC_CITY_TABLE",
  "IXC_CITY_ID_FIELD",
  "IXC_CITY_NAME_FIELD",
  "IXC_STATUS_CLOSED",
  "IXC_STATUS_EXECUTION",
  "IXC_PAGE_SIZE",
  "IXC_MAX_PAGES",
  "IXC_INCREMENTAL_SYNC",
  "IXC_FULL_SYNC_EVERY_N_RUNS",
  "IXC_SYNC_ON_STARTUP",
  "IXC_AUTO_SYNC",
  "IXC_SYNC_INTERVAL_SECONDS",
  "IXC_VERIFY_SSL",
  "IXC_HTTP_TIMEOUT_SECONDS",
  "APP_TIMEZONE",
  "APP_DB_PATH",
  "APP_DASHBOARD_REFRESH_SECONDS",
  "APP_FILTER_OPTIONS_REFRESH_SECONDS",
  "APP_SUBJECT_GROUPS",
];

const checkboxFields = new Set([
  "IXC_SYNC_ON_STARTUP",
  "IXC_AUTO_SYNC",
  "IXC_VERIFY_SSL",
  "IXC_INCREMENTAL_SYNC",
]);

const numberFields = new Set([
  "IXC_PAGE_SIZE",
  "IXC_MAX_PAGES",
  "IXC_FULL_SYNC_EVERY_N_RUNS",
  "IXC_SYNC_INTERVAL_SECONDS",
  "IXC_HTTP_TIMEOUT_SECONDS",
  "APP_DASHBOARD_REFRESH_SECONDS",
  "APP_FILTER_OPTIONS_REFRESH_SECONDS",
]);

const BOARD_ROW_FIELDS = [
  "slot_label",
  "team_label",
  "os_id",
  "subject_name",
  "branch_name",
  "technician_names",
  "start_at",
  "displacement_at",
  "executed_at",
  "finalized_at",
  "status_label",
  "opening_note",
  "occurrence_note",
  "comment_note",
];

let subjectOptionsState = [];
let subjectGroupOptionsState = [];
let installationsPresetOptionsState = [];
let installationsTechnicianOptionsState = [];
let installationsSelectedTechniciansState = new Set();
let boardTechnicianOptionsState = [];
const BOARD_STATUS_LABEL_BY_KEY = Object.freeze({
  AGUARDANDO: "Aguardando",
  ABERTA: "Aberta",
  AGENDADA: "Agendada",
  REAGENDADA: "Reagendada",
  DESLOCAMENTO: "Deslocamento",
  EM_EXECUCAO: "Em execucao",
  FINALIZADA: "Finalizada",
  CANCELADA: "Cancelada",
});
const BOARD_STATUS_ORDER = Object.freeze([
  "AGUARDANDO",
  "ABERTA",
  "AGENDADA",
  "REAGENDADA",
  "DESLOCAMENTO",
  "EM_EXECUCAO",
  "FINALIZADA",
  "CANCELADA",
]);
const BOARD_STATUS_DEFAULT_OPTIONS = Object.freeze(
  BOARD_STATUS_ORDER.map((key) => BOARD_STATUS_LABEL_BY_KEY[key])
);
let boardStatusOptionsState = [...BOARD_STATUS_DEFAULT_OPTIONS];

function getLocalIsoDate(value = new Date()) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function getCurrentWeekStartIso() {
  const value = new Date();
  const day = value.getDay();
  const mondayOffset = day === 0 ? -6 : 1 - day;
  value.setDate(value.getDate() + mondayOffset);
  return getLocalIsoDate(value);
}

const today = getLocalIsoDate();
const currentWeekStart = getCurrentWeekStartIso();
dateInput.value = today;
startDateInput.value = currentWeekStart;
endDateInput.value = today;
if (weeklyStartDateInput) {
  weeklyStartDateInput.value = currentWeekStart;
}
if (weeklyEndDateInput) {
  weeklyEndDateInput.value = today;
}
prodStartDateInput.value = currentWeekStart;
prodEndDateInput.value = today;
if (installationsStartDateInput) {
  installationsStartDateInput.value = currentWeekStart;
}
if (installationsEndDateInput) {
  installationsEndDateInput.value = today;
}
if (boardDateInput) {
  boardDateInput.value = today;
}
ensureSubjectFilterRows(subjectFilterRows, []);
ensureSubjectFilterRows(prodSubjectFilterRows, []);
ensureSubjectFilterRows(installationsSubjectFilterRows, []);
ensureBoardTechnicianRows([]);
ensureBoardStatusRows([]);
if (boardDelayReportPrintBtn) {
  boardDelayReportPrintBtn.disabled = true;
}

let hourlyChart = null;
let subjectsChart = null;
let techPerformanceChart = null;
let productivityChart = null;
let autoRefreshMetricsMs = 30000;
let autoRefreshFiltersMs = 180000;
let metricsRefreshTimer = null;
let filtersRefreshTimer = null;
let isMetricsRefreshing = false;
let isProductivityRefreshing = false;
let isBoardRefreshing = false;
let activeTab = "dashboard";
let boardDirty = false;
let boardEntriesState = [];
let boardVisibleEntryIndexes = [];
let boardSavedListsState = [];
let boardSelectedTeamKey = "";
let boardSelectedSavedListId = "";
let boardReferencesState = {
  orders: [],
  technicians: [],
  all_technicians: [],
  branches: [],
  statuses: [],
  time_slots: [],
};
let boardSummaryState = {};
let boardGeneratedState = false;
const orderDetailsCache = new Map();
let cardOrdersModalOpen = false;
let boardDelayReportModalOpen = false;
let boardDelayReportDataState = null;
let boardCommentModalOpen = false;
let boardCommentEditingIndex = null;

const CHART_THEME = Object.freeze({
  axisText: "#ffffff",
  axisTextSoft: "#b0bec5",
  axisGrid: "rgba(57, 255, 20, 0.18)",
  tooltipBg: "rgba(10, 15, 28, 0.96)",
  tooltipTitle: "#ffffff",
  tooltipBody: "#d9fbe0",
  tooltipBorder: "rgba(57, 255, 20, 0.55)",
  hourlyBarTop: "rgba(57, 255, 20, 0.92)",
  hourlyBarBottom: "rgba(0, 200, 83, 0.25)",
  hourlyBarHover: "rgba(0, 200, 83, 0.95)",
  doughnutPalette: [
    "#39ff14",
    "#00c853",
    "#7cff6b",
    "#1de878",
    "#b8ffb0",
    "#00a86b",
    "#78f5c5",
    "#d9fbe0",
  ],
  techFinished: "rgba(57, 255, 20, 0.82)",
  techExecution: "rgba(0, 200, 83, 0.86)",
  productivityBar: "rgba(57, 255, 20, 0.72)",
  productivityLineBorder: "rgba(0, 200, 83, 0.95)",
  productivityLineBg: "rgba(0, 200, 83, 0.2)",
});

function buildChartTooltipOptions() {
  return {
    backgroundColor: CHART_THEME.tooltipBg,
    titleColor: CHART_THEME.tooltipTitle,
    bodyColor: CHART_THEME.tooltipBody,
    borderColor: CHART_THEME.tooltipBorder,
    borderWidth: 1,
  };
}

function formatDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleString("pt-BR");
}

function formatDateOnly(value, fallback = "-") {
  const raw = normalizeText(value || "").trim();
  const match = raw.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!match) {
    return raw || fallback;
  }
  const [, year, month, day] = match;
  return `${day}/${month}/${year}`;
}

function formatDateTimeCell(value, fallback = "-") {
  const raw = normalizeText(value || "").trim();
  if (!raw) {
    return fallback;
  }
  const match = raw.match(/^(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2})(?::\d{2})?)?$/);
  if (!match) {
    return raw || fallback;
  }
  const [, year, month, day, hour, minute] = match;
  if (hour && minute) {
    return `${day}/${month}/${year} ${hour}:${minute}`;
  }
  return `${day}/${month}/${year}`;
}

function normalizeText(value) {
  const text = value === null || value === undefined ? "" : String(value);
  if (!text || !/[ÃÂÐ]/.test(text)) {
    return text;
  }
  try {
    const bytes = Uint8Array.from([...text].map((char) => char.charCodeAt(0)));
    const normalized = new TextDecoder("utf-8").decode(bytes);
    return normalized.includes("\uFFFD") ? text : normalized;
  } catch (_error) {
    return text;
  }
}

function buildSubjectSelectOptions(selectedValue = "__all__") {
  const options = ['<option value="__all__">Selecione um tipo de OS</option>'];
  subjectOptionsState.forEach((subject) => {
    const safeValue = escapeHtmlAttr(subject);
    const label = escapeHtml(normalizeText(subject));
    const selected = subject === selectedValue ? " selected" : "";
    options.push(`<option value="${safeValue}"${selected}>${label}</option>`);
  });
  return options.join("");
}

function createSubjectFilterRow(selectedValue = "__all__") {
  const row = document.createElement("div");
  row.className = "subject-filter-row";
  row.innerHTML = `
    <select class="subject-filter-select">
      ${buildSubjectSelectOptions(selectedValue)}
    </select>
    <button type="button" class="subject-filter-remove" title="Remover tipo de OS">-</button>
  `;
  return row;
}

function getSubjectFilterValues(container) {
  if (!(container instanceof HTMLElement)) {
    return [];
  }
  const seen = new Set();
  const values = [];
  container.querySelectorAll(".subject-filter-select").forEach((element) => {
    if (!(element instanceof HTMLSelectElement)) {
      return;
    }
    const value = String(element.value || "").trim();
    if (!value || value === "__all__" || seen.has(value)) {
      return;
    }
    seen.add(value);
    values.push(value);
  });
  return values;
}

function ensureSubjectFilterRows(container, values = []) {
  if (!(container instanceof HTMLElement)) {
    return;
  }
  const normalized = [...values].filter((value) => String(value || "").trim());
  container.innerHTML = "";
  const targetValues = normalized.length ? normalized : ["__all__"];
  targetValues.forEach((value) => {
    container.appendChild(createSubjectFilterRow(value));
  });
  refreshSubjectRemoveButtons(container);
}

function addSubjectFilterRow(container) {
  if (!(container instanceof HTMLElement)) {
    return;
  }
  container.appendChild(createSubjectFilterRow("__all__"));
  refreshSubjectRemoveButtons(container);
}

function removeSubjectFilterRow(container, trigger) {
  if (!(container instanceof HTMLElement)) {
    return;
  }
  const row = trigger.closest(".subject-filter-row");
  if (!(row instanceof HTMLElement)) {
    return;
  }
  row.remove();
  if (!container.querySelector(".subject-filter-row")) {
    container.appendChild(createSubjectFilterRow("__all__"));
  }
  refreshSubjectRemoveButtons(container);
}

function clearSubjectFilterRows(container) {
  ensureSubjectFilterRows(container, []);
}

function refreshSubjectRowOptions(container) {
  if (!(container instanceof HTMLElement)) {
    return;
  }
  const selects = [...container.querySelectorAll(".subject-filter-select")];
  selects.forEach((element, index) => {
    if (!(element instanceof HTMLSelectElement)) {
      return;
    }
    const selected = String(element.value || "__all__");
    element.innerHTML = buildSubjectSelectOptions(selected);
  });
}

function refreshSubjectRemoveButtons(container) {
  if (!(container instanceof HTMLElement)) {
    return;
  }
  const rows = [...container.querySelectorAll(".subject-filter-row")];
  rows.forEach((row, index) => {
    const removeBtn = row.querySelector(".subject-filter-remove");
    if (!(removeBtn instanceof HTMLButtonElement)) {
      return;
    }
    removeBtn.disabled = rows.length <= 1;
    removeBtn.style.visibility = rows.length <= 1 && index === 0 ? "hidden" : "visible";
  });
}

function buildBoardTechnicianSelectOptions(selectedValue = "__all__") {
  const options = ['<option value="__all__">Selecione um tecnico</option>'];
  boardTechnicianOptionsState.forEach((technician) => {
    const safeValue = escapeHtmlAttr(technician);
    const label = escapeHtml(normalizeText(technician));
    const selected = technician === selectedValue ? " selected" : "";
    options.push(`<option value="${safeValue}"${selected}>${label}</option>`);
  });
  return options.join("");
}

function createBoardTechnicianRow(selectedValue = "__all__") {
  const row = document.createElement("div");
  row.className = "board-technician-row";
  row.innerHTML = `
    <select class="board-technician-select">
      ${buildBoardTechnicianSelectOptions(selectedValue)}
    </select>
    <button type="button" class="board-technician-remove" title="Remover tecnico">-</button>
  `;
  return row;
}

function ensureBoardTechnicianRows(values = []) {
  if (!(boardTechnicianRows instanceof HTMLElement)) {
    return;
  }
  const normalized = [...values]
    .map((value) => String(value || "").trim())
    .filter((value) => value.length > 0);
  boardTechnicianRows.innerHTML = "";
  const targetValues = normalized.length ? normalized : ["__all__"];
  targetValues.forEach((value) => {
    boardTechnicianRows.appendChild(createBoardTechnicianRow(value));
  });
  refreshBoardTechnicianRemoveButtons();
}

function addBoardTechnicianRow() {
  if (!(boardTechnicianRows instanceof HTMLElement)) {
    return;
  }
  boardTechnicianRows.appendChild(createBoardTechnicianRow("__all__"));
  refreshBoardTechnicianRemoveButtons();
}

function removeBoardTechnicianRow(trigger) {
  if (!(boardTechnicianRows instanceof HTMLElement)) {
    return;
  }
  const row = trigger.closest(".board-technician-row");
  if (!(row instanceof HTMLElement)) {
    return;
  }
  row.remove();
  if (!boardTechnicianRows.querySelector(".board-technician-row")) {
    boardTechnicianRows.appendChild(createBoardTechnicianRow("__all__"));
  }
  refreshBoardTechnicianRemoveButtons();
}

function refreshBoardTechnicianRowOptions() {
  if (!(boardTechnicianRows instanceof HTMLElement)) {
    return;
  }
  const selects = [...boardTechnicianRows.querySelectorAll(".board-technician-select")];
  selects.forEach((element) => {
    if (!(element instanceof HTMLSelectElement)) {
      return;
    }
    const selected = String(element.value || "__all__");
    element.innerHTML = buildBoardTechnicianSelectOptions(selected);
  });
}

function refreshBoardTechnicianRemoveButtons() {
  if (!(boardTechnicianRows instanceof HTMLElement)) {
    return;
  }
  const rows = [...boardTechnicianRows.querySelectorAll(".board-technician-row")];
  rows.forEach((row, index) => {
    const removeBtn = row.querySelector(".board-technician-remove");
    if (!(removeBtn instanceof HTMLButtonElement)) {
      return;
    }
    removeBtn.disabled = rows.length <= 1;
    removeBtn.style.visibility = rows.length <= 1 && index === 0 ? "hidden" : "visible";
  });
}

function getBoardTechnicianValues() {
  if (!(boardTechnicianRows instanceof HTMLElement)) {
    return [];
  }
  const seen = new Set();
  const values = [];
  boardTechnicianRows.querySelectorAll(".board-technician-select").forEach((element) => {
    if (!(element instanceof HTMLSelectElement)) {
      return;
    }
    const value = String(element.value || "").trim();
    if (!value || value === "__all__" || seen.has(value)) {
      return;
    }
    seen.add(value);
    values.push(value);
  });
  return values;
}

function normalizeBoardStatusToken(value) {
  const text = normalizeText(value || "").trim();
  if (!text) {
    return "";
  }
  return text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .toUpperCase();
}

function normalizeBoardStatusFilterKey(value) {
  const token = normalizeBoardStatusToken(value);
  const aliases = {
    AGUARDANDO: "AGUARDANDO",
    AGUARDANDO_RELATO: "AGUARDANDO",
    ABERTA: "ABERTA",
    ABERTO: "ABERTA",
    PENDENTE: "ABERTA",
    AGENDADA: "AGENDADA",
    AGENDA: "AGENDADA",
    AG: "AGENDADA",
    REAGENDADA: "REAGENDADA",
    REAGENDADO: "REAGENDADA",
    REAGENDAMENTO: "REAGENDADA",
    R: "REAGENDADA",
    DESLOCAMENTO: "DESLOCAMENTO",
    EM_DESLOCAMENTO: "DESLOCAMENTO",
    DS: "DESLOCAMENTO",
    EM_EXECUCAO: "EM_EXECUCAO",
    EM_ANDAMENTO: "EM_EXECUCAO",
    EXECUCAO: "EM_EXECUCAO",
    EX: "EM_EXECUCAO",
    EN: "EM_EXECUCAO",
    E: "EM_EXECUCAO",
    FINALIZADA: "FINALIZADA",
    CONCLUIDA: "FINALIZADA",
    F: "FINALIZADA",
    CANCELADA: "CANCELADA",
    CANCELADO: "CANCELADA",
    ANULADA: "CANCELADA",
    C: "CANCELADA",
    CA: "CANCELADA",
    AN: "CANCELADA",
  };
  return aliases[token] || "";
}

function boardStatusLabelFromKey(key) {
  return BOARD_STATUS_LABEL_BY_KEY[key] || "";
}

function setBoardStatusOptions(rawOptions = []) {
  const seen = new Set();
  const normalized = [];
  const register = (value) => {
    const key = normalizeBoardStatusFilterKey(value);
    if (!key || seen.has(key)) {
      return;
    }
    const label = boardStatusLabelFromKey(key);
    if (!label) {
      return;
    }
    seen.add(key);
    normalized.push(label);
  };
  BOARD_STATUS_DEFAULT_OPTIONS.forEach(register);
  (Array.isArray(rawOptions) ? rawOptions : []).forEach(register);
  boardStatusOptionsState = normalized.length ? normalized : [...BOARD_STATUS_DEFAULT_OPTIONS];
}

function buildBoardStatusSelectOptions(selectedValue = "__all__") {
  const normalizedSelected = String(selectedValue || "__all__").trim() || "__all__";
  const options = ['<option value="__all__">Selecione um status</option>'];
  const knownValues = new Set(boardStatusOptionsState);
  if (normalizedSelected !== "__all__" && !knownValues.has(normalizedSelected)) {
    const safeValue = escapeHtmlAttr(normalizedSelected);
    const label = escapeHtml(normalizeText(normalizedSelected));
    options.push(`<option value="${safeValue}" selected>${label}</option>`);
  }
  boardStatusOptionsState.forEach((statusLabel) => {
    const safeValue = escapeHtmlAttr(statusLabel);
    const label = escapeHtml(normalizeText(statusLabel));
    const selected = statusLabel === normalizedSelected ? " selected" : "";
    options.push(`<option value="${safeValue}"${selected}>${label}</option>`);
  });
  return options.join("");
}

function createBoardStatusRow(selectedValue = "__all__") {
  const row = document.createElement("div");
  row.className = "board-status-row";
  row.innerHTML = `
    <select class="board-status-select">
      ${buildBoardStatusSelectOptions(selectedValue)}
    </select>
    <button type="button" class="board-status-remove" title="Remover status">-</button>
  `;
  return row;
}

function ensureBoardStatusRows(values = []) {
  if (!(boardStatusRows instanceof HTMLElement)) {
    return;
  }
  const normalized = [...values]
    .map((value) => String(value || "").trim())
    .filter((value) => value.length > 0);
  boardStatusRows.innerHTML = "";
  const targetValues = normalized.length ? normalized : ["__all__"];
  targetValues.forEach((value) => {
    boardStatusRows.appendChild(createBoardStatusRow(value));
  });
  refreshBoardStatusRemoveButtons();
}

function addBoardStatusRow() {
  if (!(boardStatusRows instanceof HTMLElement)) {
    return;
  }
  boardStatusRows.appendChild(createBoardStatusRow("__all__"));
  refreshBoardStatusRemoveButtons();
}

function removeBoardStatusRow(trigger) {
  if (!(boardStatusRows instanceof HTMLElement)) {
    return;
  }
  const row = trigger.closest(".board-status-row");
  if (!(row instanceof HTMLElement)) {
    return;
  }
  row.remove();
  if (!boardStatusRows.querySelector(".board-status-row")) {
    boardStatusRows.appendChild(createBoardStatusRow("__all__"));
  }
  refreshBoardStatusRemoveButtons();
}

function refreshBoardStatusRowOptions() {
  if (!(boardStatusRows instanceof HTMLElement)) {
    return;
  }
  const selects = [...boardStatusRows.querySelectorAll(".board-status-select")];
  selects.forEach((element) => {
    if (!(element instanceof HTMLSelectElement)) {
      return;
    }
    const selected = String(element.value || "__all__");
    element.innerHTML = buildBoardStatusSelectOptions(selected);
  });
}

function refreshBoardStatusRemoveButtons() {
  if (!(boardStatusRows instanceof HTMLElement)) {
    return;
  }
  const rows = [...boardStatusRows.querySelectorAll(".board-status-row")];
  rows.forEach((row, index) => {
    const removeBtn = row.querySelector(".board-status-remove");
    if (!(removeBtn instanceof HTMLButtonElement)) {
      return;
    }
    removeBtn.disabled = rows.length <= 1;
    removeBtn.style.visibility = rows.length <= 1 && index === 0 ? "hidden" : "visible";
  });
}

function getBoardStatusValues() {
  if (!(boardStatusRows instanceof HTMLElement)) {
    return [];
  }
  const seen = new Set();
  const values = [];
  boardStatusRows.querySelectorAll(".board-status-select").forEach((element) => {
    if (!(element instanceof HTMLSelectElement)) {
      return;
    }
    const value = String(element.value || "").trim();
    const key = normalizeBoardStatusFilterKey(value);
    if (!value || value === "__all__" || !key || seen.has(key)) {
      return;
    }
    seen.add(key);
    values.push(boardStatusLabelFromKey(key));
  });
  return values;
}

function buildBoardTeamNameFromSelectedTechnicians() {
  const selectedTechnicians = getBoardTechnicianValues();
  const normalized = selectedTechnicians
    .map((value) => normalizeText(value || "").trim())
    .filter((value) => value.length > 0);
  return normalized.join(" + ");
}

function syncBoardTeamWithSelectedTechnicians({ markDirty = true } = {}) {
  const selectedTeamName = buildBoardTeamNameFromSelectedTechnicians();
  if (selectedTeamName) {
    boardTeamInput.value = selectedTeamName;
  }
  const matchedList = findBoardSavedListByTeamName(boardTeamInput.value.trim(), {
    entryDate: boardDateInput.value || "",
  });
  boardSelectedSavedListId = matchedList ? matchedList.list_id : "";
  boardSelectedTeamKey = matchedList ? matchedList.team_key : "";
  renderBoardSavedLists();
  if (markDirty) {
    boardDirty = true;
  }
}

function appendMultiParams(params, key, values) {
  values.forEach((value) => {
    const text = String(value || "").trim();
    if (!text || text === "__all__") {
      return;
    }
    params.append(key, text);
  });
}

function formatFilterLabel(value, fallback = "Todos") {
  if (Array.isArray(value)) {
    const items = value
      .map((item) => normalizeText(item))
      .map((item) => String(item || "").trim())
      .filter((item) => item.length > 0);
    return items.length ? items.join(", ") : fallback;
  }
  const text = normalizeText(value || "").trim();
  return text || fallback;
}

function formatRelatoMessage(value) {
  const raw = normalizeText(value || "")
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .trim();
  if (!raw || raw === "-") {
    return "";
  }
  return raw
    .replace(/\s*\|\s*/g, "\n")
    .replace(
      /\s+(?=(Processo:|Tarefa:|Descricao|Descrição|Instrucoes|Instruções|Contato:|Cliente:|Finalizar a OS|Diagnostico))/gi,
      "\n"
    )
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function buildRelatoPreview(text, maxLength = 40) {
  const compact = String(text || "").replace(/\s+/g, " ").trim();
  if (!compact) {
    return "Sem relato";
  }
  if (compact.length <= maxLength) {
    return compact;
  }
  return `${compact.slice(0, Math.max(0, maxLength - 1))}...`;
}

function formatOrderWithCustomer(osId, customerName) {
  const orderId = normalizeText(osId || "-");
  const customer = normalizeText(customerName || "").trim();
  if (!customer || orderId === "-") {
    return orderId;
  }
  return `${orderId} - ${customer}`;
}

function getOrderTechnicianDisplay(order) {
  const technicianName = normalizeText(order?.technician_name || "");
  if (technicianName) {
    return technicianName;
  }
  const technicianId = String(order?.technician_id || "").trim();
  if (technicianId) {
    return `Tecnico ID ${technicianId}`;
  }
  return "";
}

function setActiveTab(tab) {
  activeTab = tab;
  const isDashboard = tab === "dashboard";
  const isProductivity = tab === "productivity";
  const isInstallations = tab === "installations";
  const isOperations = tab === "operations";
  tabDashboardBtn.classList.toggle("active", isDashboard);
  tabProductivityBtn.classList.toggle("active", isProductivity);
  tabInstallationsBtn.classList.toggle("active", isInstallations);
  if (tabOperationsBtn) {
    tabOperationsBtn.classList.toggle("active", isOperations);
  }
  tabSettingsBtn.classList.toggle("active", tab === "settings");
  dashboardTab.classList.toggle("active", isDashboard);
  productivityTab.classList.toggle("active", isProductivity);
  installationsTab.classList.toggle("active", isInstallations);
  if (operationsTab) {
    operationsTab.classList.toggle("active", isOperations);
  }
  settingsTab.classList.toggle("active", tab === "settings");
  if (!isDashboard) {
    closeCardOrdersModal();
  }

  if (isProductivity) {
    Promise.all([loadProductivity(), loadProductivityOrders()]).catch((error) => {
      productivityMeta.textContent = error.message || "Erro ao carregar produtividade.";
      productivityOrdersMeta.textContent = error.message || "Erro ao carregar OS detalhadas.";
    });
  }
  if (isInstallations) {
    loadInstallations().catch((error) => {
      if (installationsScopeValue) {
        installationsScopeValue.textContent = error.message || "Erro ao carregar instalacoes.";
      }
    });
  }
  if (isOperations && operationsTab) {
    loadBoardSavedLists({ silent: true }).catch((error) => {
      console.error("Falha ao carregar listas salvas do mapa diario:", error);
    });
    loadBoard({ skipIfDirty: true }).catch((error) => {
      boardFeedback.textContent = error.message || "Erro ao carregar mapa diario.";
    });
  }
}

function buildMetricsQuery() {
  const params = new URLSearchParams();
  params.set("date", dateInput.value || today);

  if (startDateInput.value) {
    params.set("start_date", startDateInput.value);
  }
  if (endDateInput.value) {
    params.set("end_date", endDateInput.value);
  }
  if (weeklyStartDateInput?.value) {
    params.set("weekly_start_date", weeklyStartDateInput.value);
  }
  if (weeklyEndDateInput?.value) {
    params.set("weekly_end_date", weeklyEndDateInput.value);
  }
  appendMultiParams(params, "subject", getSubjectFilterValues(subjectFilterRows));
  if (subjectGroupFilter?.value && subjectGroupFilter.value !== "__all__") {
    params.set("subject_group", subjectGroupFilter.value);
  }
  if (branchFilter.value && branchFilter.value !== "__all__") {
    params.set("branch", branchFilter.value);
  }
  params.set("_ts", String(Date.now()));
  return params.toString();
}

function buildCardOrdersQuery(metric, limit = 250) {
  const params = new URLSearchParams();
  params.set("metric", metric);
  params.set("date", dateInput.value || today);
  if (startDateInput.value) {
    params.set("start_date", startDateInput.value);
  }
  if (endDateInput.value) {
    params.set("end_date", endDateInput.value);
  }
  appendMultiParams(params, "subject", getSubjectFilterValues(subjectFilterRows));
  if (subjectGroupFilter?.value && subjectGroupFilter.value !== "__all__") {
    params.set("subject_group", subjectGroupFilter.value);
  }
  if (branchFilter.value && branchFilter.value !== "__all__") {
    params.set("branch", branchFilter.value);
  }
  params.set("limit", String(limit));
  params.set("_ts", String(Date.now()));
  return params.toString();
}

async function loadMetrics() {
  const response = await fetch(`/api/metrics/overview?${buildMetricsQuery()}`, {
    cache: "no-store",
    headers: { "Cache-Control": "no-cache" },
  });
  if (!response.ok) {
    throw new Error(`Falha ao carregar metricas: ${response.status}`);
  }
  const data = await response.json();
  renderMetrics(data);
}

async function loadCardOrders(metric, label) {
  cardOrdersModalTable.innerHTML = "<tr><td colspan='11'>Carregando OS...</td></tr>";
  const response = await fetch(`/api/metrics/card-orders?${buildCardOrdersQuery(metric)}`, {
    cache: "no-store",
    headers: { "Cache-Control": "no-cache" },
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || `Falha ao carregar OS do card: ${response.status}`);
  }
  const data = await response.json();
  renderCardOrdersModalData(data, label);
}

function buildProductivityQuery() {
  const params = new URLSearchParams();
  params.set("date", prodEndDateInput.value || today);
  if (prodStartDateInput.value) {
    params.set("start_date", prodStartDateInput.value);
  }
  if (prodEndDateInput.value) {
    params.set("end_date", prodEndDateInput.value);
  }
  appendMultiParams(params, "subject", getSubjectFilterValues(prodSubjectFilterRows));
  if (prodSubjectGroupFilter?.value && prodSubjectGroupFilter.value !== "__all__") {
    params.set("subject_group", prodSubjectGroupFilter.value);
  }
  if (prodBranchFilter.value && prodBranchFilter.value !== "__all__") {
    params.set("branch", prodBranchFilter.value);
  }
  if (prodTechnicianFilter.value && prodTechnicianFilter.value !== "__all__") {
    params.set("technician", prodTechnicianFilter.value);
  }
  if (prodStatusFilter.value && prodStatusFilter.value !== "__all__") {
    params.set("status", prodStatusFilter.value);
  }
  params.set("_ts", String(Date.now()));
  return params.toString();
}

async function loadProductivity() {
  const response = await fetch(`/api/metrics/overview?${buildProductivityQuery()}`, {
    cache: "no-store",
    headers: { "Cache-Control": "no-cache" },
  });
  if (!response.ok) {
    throw new Error(`Falha ao carregar produtividade: ${response.status}`);
  }
  const data = await response.json();
  renderProductivity(data);
}

function shouldLoadTechnicianOrders() {
  return Boolean(prodTechnicianFilter.value && prodTechnicianFilter.value !== "__all__");
}

async function loadProductivityOrders() {
  if (!shouldLoadTechnicianOrders()) {
    renderProductivityOrdersEmpty(
      "Selecione um tecnico para listar as OS detalhadas (abertura, execucao, finalizacao e relato)."
    );
    return;
  }
  const response = await fetch(`/api/metrics/technician-orders?${buildProductivityQuery()}`, {
    cache: "no-store",
    headers: { "Cache-Control": "no-cache" },
  });
  if (!response.ok) {
    throw new Error(`Falha ao carregar OS detalhadas: ${response.status}`);
  }
  const data = await response.json();
  renderProductivityOrders(data);
}

function buildInstallationsQuery() {
  const params = new URLSearchParams();
  params.set("date", installationsEndDateInput?.value || installationsStartDateInput?.value || today);
  if (installationsStartDateInput?.value) {
    params.set("start_date", installationsStartDateInput.value);
  }
  if (installationsEndDateInput?.value) {
    params.set("end_date", installationsEndDateInput.value);
  }
  if (installationsBranchSelect?.value && installationsBranchSelect.value !== "__all__") {
    params.set("branch", installationsBranchSelect.value);
  }
  if (installationsCitySelect?.value && installationsCitySelect.value !== "__all__") {
    params.set("city", installationsCitySelect.value);
  }
  appendMultiParams(params, "subject", getSubjectFilterValues(installationsSubjectFilterRows));
  if (installationsSubjectGroupFilter?.value && installationsSubjectGroupFilter.value !== "__all__") {
    params.set("subject_group", installationsSubjectGroupFilter.value);
  }
  getSelectedInstallationTechnicians().forEach((technician) => {
    params.append("technician", technician);
  });
  params.set("_ts", String(Date.now()));
  return params.toString();
}

async function loadInstallations() {
  if (installationsApplyDateBtn instanceof HTMLButtonElement) {
    installationsApplyDateBtn.disabled = true;
  }
  try {
    const response = await fetch(`/api/metrics/installations?${buildInstallationsQuery()}`, {
      cache: "no-store",
      headers: { "Cache-Control": "no-cache" },
    });
    if (!response.ok) {
      throw new Error(`Falha ao carregar instalacoes: ${response.status}`);
    }
    const data = await response.json();
    renderInstallationsTab(data.installations || {}, data.filters || {});
  } finally {
    if (installationsApplyDateBtn instanceof HTMLButtonElement) {
      installationsApplyDateBtn.disabled = false;
    }
  }
}

async function loadInstallationPresets() {
  const response = await fetch(`/api/metrics/installations/presets?_ts=${Date.now()}`, {
    cache: "no-store",
    headers: { "Cache-Control": "no-cache" },
  });
  if (!response.ok) {
    throw new Error(`Falha ao carregar listas salvas: ${response.status}`);
  }
  const data = await response.json();
  installationsPresetOptionsState = Array.isArray(data.presets) ? data.presets : [];
  renderInstallationPresetSelect();
}

function renderInstallationPresetSelect() {
  if (!(installationsPresetSelect instanceof HTMLSelectElement)) {
    return;
  }
  const current = installationsPresetSelect.value;
  installationsPresetSelect.innerHTML = "";
  const defaultOption = document.createElement("option");
  defaultOption.value = "";
  defaultOption.textContent = installationsPresetOptionsState.length
    ? "Selecionar lista"
    : "Nenhuma lista salva";
  installationsPresetSelect.appendChild(defaultOption);
  installationsPresetOptionsState.forEach((preset) => {
    const option = document.createElement("option");
    option.value = String(preset.id || "");
    option.textContent = normalizeText(preset.name || "");
    installationsPresetSelect.appendChild(option);
  });
  if ([...installationsPresetSelect.options].some((option) => option.value === current)) {
    installationsPresetSelect.value = current;
  }
}

function getSelectedInstallationPreset() {
  const presetId = String(installationsPresetSelect?.value || "").trim();
  if (!presetId) {
    return null;
  }
  return installationsPresetOptionsState.find((preset) => String(preset.id) === presetId) || null;
}

function getSelectedCityName() {
  if (!(installationsCitySelect instanceof HTMLSelectElement)) {
    return "";
  }
  if (!installationsCitySelect.value || installationsCitySelect.value === "__all__") {
    return "";
  }
  return String(installationsCitySelect.selectedOptions[0]?.textContent || "").trim();
}

function collectInstallationPresetPayload() {
  return {
    name: String(installationsPresetNameInput?.value || "").trim(),
    branch:
      installationsBranchSelect?.value && installationsBranchSelect.value !== "__all__"
        ? installationsBranchSelect.value
        : "",
    city:
      installationsCitySelect?.value && installationsCitySelect.value !== "__all__"
        ? installationsCitySelect.value
        : "",
    city_name: getSelectedCityName(),
    subjects: getSubjectFilterValues(installationsSubjectFilterRows),
    subject_group:
      installationsSubjectGroupFilter?.value && installationsSubjectGroupFilter.value !== "__all__"
        ? installationsSubjectGroupFilter.value
        : "",
    technicians: getSelectedInstallationTechnicians(),
  };
}

function updateInstallationsSubjectSummary() {
  if (!(installationsSubjectSummary instanceof HTMLElement)) {
    return;
  }
  const subjects = getSubjectFilterValues(installationsSubjectFilterRows);
  const groupLabel =
    installationsSubjectGroupFilter instanceof HTMLSelectElement &&
    installationsSubjectGroupFilter.value &&
    installationsSubjectGroupFilter.value !== "__all__"
      ? normalizeText(installationsSubjectGroupFilter.selectedOptions[0]?.textContent || "")
      : "";
  if (groupLabel) {
    installationsSubjectSummary.textContent = `Grupo: ${groupLabel}`;
    return;
  }
  installationsSubjectSummary.textContent = subjects.length
    ? `${subjects.length} tipo(s) selecionado(s)`
    : "Todos os tipos";
}

function setInstallationsSubjectCollapsed(collapsed) {
  if (!(installationsSubjectField instanceof HTMLElement)) {
    return;
  }
  installationsSubjectField.classList.toggle("is-collapsed", Boolean(collapsed));
  if (installationsToggleSubjectsBtn instanceof HTMLButtonElement) {
    installationsToggleSubjectsBtn.textContent = collapsed
      ? "Mostrar tipos de OS"
      : "Ocultar tipos de OS";
  }
  updateInstallationsSubjectSummary();
}

async function saveInstallationPreset() {
  const payload = collectInstallationPresetPayload();
  if (!payload.name) {
    alert("Informe um nome para salvar a lista.");
    return;
  }
  const selectedPreset = getSelectedInstallationPreset();
  const url = selectedPreset
    ? `/api/metrics/installations/presets/${selectedPreset.id}`
    : "/api/metrics/installations/presets";
  const response = await fetch(url, {
    method: selectedPreset ? "PUT" : "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Falha ao salvar lista: ${response.status}`);
  }
  const data = await response.json();
  await loadInstallationPresets();
  if (installationsPresetSelect instanceof HTMLSelectElement && data.preset?.id) {
    installationsPresetSelect.value = String(data.preset.id);
  }
  setInstallationsSubjectCollapsed(true);
}

function applyInstallationPreset(preset) {
  if (!preset) {
    return;
  }
  if (installationsPresetNameInput instanceof HTMLInputElement) {
    installationsPresetNameInput.value = normalizeText(preset.name || "");
  }
  if (installationsBranchSelect instanceof HTMLSelectElement) {
    installationsBranchSelect.value = [...installationsBranchSelect.options].some(
      (option) => option.value === preset.branch
    )
      ? preset.branch
      : "__all__";
  }
  if (installationsCitySelect instanceof HTMLSelectElement) {
    installationsCitySelect.value = [...installationsCitySelect.options].some(
      (option) => option.value === preset.city
    )
      ? preset.city
      : "__all__";
  }
  ensureSubjectFilterRows(
    installationsSubjectFilterRows,
    Array.isArray(preset.subjects) ? preset.subjects : []
  );
  if (installationsSubjectGroupFilter instanceof HTMLSelectElement) {
    installationsSubjectGroupFilter.value = [...installationsSubjectGroupFilter.options].some(
      (option) => option.value === preset.subject_group
    )
      ? preset.subject_group
      : "__all__";
  }
  installationsSelectedTechniciansState = new Set(
    Array.isArray(preset.technicians)
      ? preset.technicians.map((value) => String(value || "").trim()).filter(Boolean)
      : []
  );
  if (installationsCollaboratorSearch instanceof HTMLInputElement) {
    installationsCollaboratorSearch.value = "";
  }
  renderInstallationCollaboratorPicker();
  setInstallationsSubjectCollapsed(true);
}

async function deleteSelectedInstallationPreset() {
  const selectedPreset = getSelectedInstallationPreset();
  if (!selectedPreset) {
    alert("Selecione uma lista para excluir.");
    return;
  }
  const confirmed = window.confirm(`Excluir a lista "${normalizeText(selectedPreset.name || "")}"?`);
  if (!confirmed) {
    return;
  }
  const response = await fetch(`/api/metrics/installations/presets/${selectedPreset.id}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Falha ao excluir lista: ${response.status}`);
  }
  if (installationsPresetNameInput instanceof HTMLInputElement) {
    installationsPresetNameInput.value = "";
  }
  await loadInstallationPresets();
}

async function loadFilterOptions() {
  const response = await fetch(`/api/metrics/filter-options?_ts=${Date.now()}`, {
    cache: "no-store",
    headers: { "Cache-Control": "no-cache" },
  });
  if (!response.ok) {
    throw new Error(`Falha ao carregar filtros: ${response.status}`);
  }
  const data = await response.json();
  subjectOptionsState = (data.subjects || [])
    .map((value) => String(value || "").trim())
    .filter((value) => value.length > 0);
  subjectGroupOptionsState = Array.isArray(data.subject_groups) ? data.subject_groups : [];
  if (!(subjectFilterRows instanceof HTMLElement) || !subjectFilterRows.children.length) {
    ensureSubjectFilterRows(subjectFilterRows, []);
  } else {
    refreshSubjectRowOptions(subjectFilterRows);
  }
  populateSubjectGroupSelect(subjectGroupFilter, subjectGroupOptionsState, "Todos os grupos");
  populateSelect(branchFilter, data.branches || [], "Todas as filiais");
  if (!(prodSubjectFilterRows instanceof HTMLElement) || !prodSubjectFilterRows.children.length) {
    ensureSubjectFilterRows(prodSubjectFilterRows, []);
  } else {
    refreshSubjectRowOptions(prodSubjectFilterRows);
  }
  populateSubjectGroupSelect(
    prodSubjectGroupFilter,
    subjectGroupOptionsState,
    "Todos os grupos"
  );
  populateSelect(prodBranchFilter, data.branches || [], "Todas as filiais");
  populateSelect(prodTechnicianFilter, data.technicians || [], "Todos os tecnicos");
  populateSelect(prodStatusFilter, data.statuses || [], "Todos os status");
  populateSelect(installationsBranchSelect, data.branches || [], "Todas as unidades");
  populateCitySelect(installationsCitySelect, data.cities || []);
  if (!(installationsSubjectFilterRows instanceof HTMLElement) || !installationsSubjectFilterRows.children.length) {
    ensureSubjectFilterRows(installationsSubjectFilterRows, []);
  } else {
    refreshSubjectRowOptions(installationsSubjectFilterRows);
  }
  populateSubjectGroupSelect(
    installationsSubjectGroupFilter,
    subjectGroupOptionsState,
    "Todos os grupos"
  );
  updateInstallationsSubjectSummary();
  installationsTechnicianOptionsState = (data.technicians || [])
    .map((value) => String(value || "").trim())
    .filter((value) => value.length > 0);
  renderInstallationCollaboratorPicker();
  boardTechnicianOptionsState = (data.technicians || [])
    .map((value) => String(value || "").trim())
    .filter((value) => value.length > 0);
  refreshBoardTechnicianRowOptions();
}

function getSelectedInstallationTechnicians() {
  return [...installationsSelectedTechniciansState];
}

function updateInstallationCollaboratorSummary() {
  if (!(installationsCollaboratorSummary instanceof HTMLElement)) {
    return;
  }
  const selected = getSelectedInstallationTechnicians();
  if (!selected.length) {
    installationsCollaboratorSummary.textContent = "Todos os tecnicos";
    return;
  }
  const preview = selected.slice(0, 2).map((value) => normalizeText(value)).join(", ");
  installationsCollaboratorSummary.textContent = selected.length > 2
    ? `${selected.length} tecnicos: ${preview}...`
    : `${selected.length} tecnico${selected.length > 1 ? "s" : ""}: ${preview}`;
}

function setInstallationCollaboratorSelection(checked) {
  if (!(installationsCollaboratorList instanceof HTMLElement)) {
    return;
  }
  installationsCollaboratorList.querySelectorAll("input[type='checkbox']").forEach((input) => {
    const value = String(input.value || "").trim();
    if (!value) {
      return;
    }
    input.checked = checked;
    if (checked) {
      installationsSelectedTechniciansState.add(value);
    } else {
      installationsSelectedTechniciansState.delete(value);
    }
  });
  updateInstallationCollaboratorSummary();
}

function renderInstallationCollaboratorPicker() {
  if (!(installationsCollaboratorList instanceof HTMLElement)) {
    updateInstallationCollaboratorSummary();
    return;
  }
  const search = normalizeText(installationsCollaboratorSearch?.value || "").trim().toLowerCase();
  const visibleTechnicians = installationsTechnicianOptionsState.filter((technician) => {
    if (!search) {
      return true;
    }
    return normalizeText(technician).toLowerCase().includes(search);
  });
  installationsCollaboratorList.innerHTML = "";
  if (!visibleTechnicians.length) {
    installationsCollaboratorList.innerHTML = "<div class='installations-empty'>Nenhum colaborador encontrado.</div>";
    return;
  }
  visibleTechnicians.forEach((technician) => {
    const label = document.createElement("label");
    label.className = "collaborator-option";
    label.innerHTML = `
      <input type="checkbox" value="${escapeHtmlAttr(technician)}"${installationsSelectedTechniciansState.has(technician) ? " checked" : ""} />
      <span>${escapeHtml(normalizeText(technician))}</span>
    `;
    installationsCollaboratorList.appendChild(label);
  });
  updateInstallationCollaboratorSummary();
}

function getSelectedMultiValues(select) {
  if (!(select instanceof HTMLSelectElement)) {
    return [];
  }
  return [...select.selectedOptions]
    .map((option) => String(option.value || "").trim())
    .filter((value) => value && value !== "__all__");
}

function populateMultiSelect(select, values) {
  if (!(select instanceof HTMLSelectElement)) {
    return;
  }
  const selected = new Set(getSelectedMultiValues(select));
  select.innerHTML = "";
  values.forEach((value) => {
    const normalized = String(value || "").trim();
    if (!normalized) {
      return;
    }
    const option = document.createElement("option");
    option.value = normalized;
    option.textContent = normalizeText(normalized);
    option.selected = selected.has(normalized);
    select.appendChild(option);
  });
}

function populateSelect(select, values, defaultLabel) {
  if (!(select instanceof HTMLSelectElement)) {
    return;
  }
  const current = select.value;
  select.innerHTML = "";
  const defaultOption = document.createElement("option");
  defaultOption.value = "__all__";
  defaultOption.textContent = defaultLabel;
  select.appendChild(defaultOption);

  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = normalizeText(value);
    select.appendChild(option);
  });

  if ([...select.options].some((option) => option.value === current)) {
    select.value = current;
  } else {
    select.value = "__all__";
  }
}

function populateCitySelect(select, values) {
  if (!(select instanceof HTMLSelectElement)) {
    return;
  }
  const current = select.value;
  select.innerHTML = "";
  const defaultOption = document.createElement("option");
  defaultOption.value = "__all__";
  defaultOption.textContent = "Todas as cidades";
  select.appendChild(defaultOption);

  values.forEach((value) => {
    const cityId = typeof value === "object" && value !== null
      ? String(value.id || "").trim()
      : String(value || "").trim();
    const cityName = typeof value === "object" && value !== null
      ? String(value.name || "").trim()
      : "";
    if (!cityId) {
      return;
    }
    const option = document.createElement("option");
    option.value = cityId;
    option.textContent = cityName
      ? normalizeText(cityName)
      : `Cidade ID ${normalizeText(cityId)}`;
    select.appendChild(option);
  });

  if ([...select.options].some((option) => option.value === current)) {
    select.value = current;
  } else {
    select.value = "__all__";
  }
}

function populateSubjectGroupSelect(select, groups, defaultLabel) {
  if (!(select instanceof HTMLSelectElement)) {
    return;
  }
  const current = String(select.value || "__all__");
  select.innerHTML = "";
  const defaultOption = document.createElement("option");
  defaultOption.value = "__all__";
  defaultOption.textContent = defaultLabel;
  select.appendChild(defaultOption);

  groups.forEach((group) => {
    const option = document.createElement("option");
    option.value = String(group.key || "").trim();
    const label = normalizeText(group.label || group.key || "Grupo");
    const count = Number(group.subjects_count || 0);
    option.textContent = count > 0 ? `${label} (${count})` : label;
    select.appendChild(option);
  });

  if ([...select.options].some((option) => option.value === current)) {
    select.value = current;
  } else {
    select.value = "__all__";
  }
  updateSubjectGroupActionButtons();
}

function parseSubjectGroupsRaw(rawValue) {
  const raw = String(rawValue || "").trim();
  if (!raw) {
    return [];
  }
  return raw
    .split(";")
    .map((chunk) => chunk.trim())
    .filter((chunk) => chunk.length > 0)
    .map((chunk) => {
      const separatorIndex = chunk.indexOf("=");
      if (separatorIndex < 0) {
        return {
          label: chunk,
          patterns: [],
        };
      }
      const label = chunk.slice(0, separatorIndex).trim();
      const patternsRaw = chunk.slice(separatorIndex + 1);
      const patterns = patternsRaw
        .split("|")
        .map((item) => item.trim())
        .filter((item) => item.length > 0);
      return { label, patterns };
    })
    .filter((group) => group.label);
}

function serializeSubjectGroupsRaw(groups) {
  return groups
    .map((group) => {
      const label = String(group.label || "").trim();
      if (!label) {
        return "";
      }
      const patterns = Array.isArray(group.patterns)
        ? group.patterns
            .map((item) => String(item || "").trim())
            .filter((item) => item.length > 0)
        : [];
      return patterns.length ? `${label}=${patterns.join("|")}` : label;
    })
    .filter((item) => item.length > 0)
    .join(";");
}

function normalizeSubjectGroupKey(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "_")
    .replace(/[^a-z0-9_]+/g, "")
    .replace(/^_+|_+$/g, "");
}

function updateSubjectGroupActionButtons() {
  if (!(deleteSubjectGroupBtn instanceof HTMLButtonElement)) {
    return;
  }
  const selectedGroup = String(subjectGroupFilter?.value || "").trim();
  deleteSubjectGroupBtn.disabled = !selectedGroup || selectedGroup === "__all__";
}

function renderMetrics(data) {
  completedValue.textContent = data.completed_today ?? 0;
  activeValue.textContent = data.sla?.active_orders ?? 0;
  slaWithinValue.textContent = data.sla?.within_sla ?? 0;
  slaOverdueValue.textContent = data.sla?.overdue ?? 0;
  const movementSummary = data.movements_summary || {};
  techniciansExecutingValue.textContent =
    movementSummary.technicians_in_execution ?? data.technicians_in_execution?.length ?? 0;
  technicianStartedOrdersValue.textContent = movementSummary.orders_started ?? 0;
  rescheduledTodayValue.textContent = data.rescheduled_today ?? 0;
  const avgExec = formatNumber(movementSummary.avg_execution_minutes);
  avgExecutionMinutesValue.textContent = formatMinutesAsHours(
    movementSummary.avg_execution_minutes
  );
  renderWeeklyOverview(data.weekly_overview || {});

  const sync = data.last_sync;
  const filters = data.filters || {};
  const filterText = [
    `Periodo: ${filters.start_date || "-"} a ${filters.end_date || "-"}`,
    `Grupo: ${formatFilterLabel(filters.subject_group_label, "Todos")}`,
    `Assunto: ${formatFilterLabel(filters.subject, "Todos")}`,
    `Filial: ${formatFilterLabel(filters.branch, "Todas")}`,
  ].join(" | ");

  if (!sync) {
    meta.textContent = `${filterText} | Sem sincronizacao registrada.`;
  } else {
    meta.textContent = `${filterText} | Ultima sincronizacao: ${formatDate(sync.finished_at || sync.started_at)} | Status: ${sync.status} | Registros: ${sync.fetched_count}`;
  }

  renderHourlyChart(data.hourly_completed || []);
  renderSubjectsChart(data.open_by_subject || []);
  renderTechPerformanceChart(data.technician_movements || data.technician_sla || []);
  renderSubjectsTable(data.open_by_subject || []);
  renderTechSlaTable(data.technician_movements || data.technician_sla || []);
}

function renderWeeklyOverview(weekly) {
  const installationPercent = Number(weekly.installation_percentage || 0);
  const productiveDay = weekly.most_productive_day || {};
  const selectedBranch = branchFilter?.value && branchFilter.value !== "__all__"
    ? normalizeText(branchFilter.value)
    : "";

  if (weeklyFinishedValue) {
    weeklyFinishedValue.textContent = weekly.finished_orders ?? 0;
  }
  if (weeklyInstallationsValue) {
    weeklyInstallationsValue.textContent = weekly.installations ?? 0;
  }
  if (weeklyInstallationsPercent) {
    weeklyInstallationsPercent.textContent = `${formatNumber(installationPercent)}% do total`;
  }
  if (weeklyProductiveDayValue) {
    weeklyProductiveDayValue.textContent = normalizeText(productiveDay.weekday || "-");
  }
  if (weeklyProductiveDayMeta) {
    const total = productiveDay.finished_orders ?? 0;
    weeklyProductiveDayMeta.textContent = total ? `${total} OS finalizadas` : "Sem OS finalizadas";
  }
  if (weeklyTechniciansValue) {
    weeklyTechniciansValue.textContent = weekly.active_technicians ?? 0;
  }
  if (weeklyTechniciansMeta) {
    weeklyTechniciansMeta.textContent = `${weekly.technician_order_count ?? 0} OS com tecnico`;
  }
  if (weeklyRangeValue) {
    weeklyRangeValue.textContent = `${formatDateOnly(weekly.period_start)} a ${formatDateOnly(weekly.period_end)}`;
  }
  if (weeklyScopeValue) {
    weeklyScopeValue.textContent = selectedBranch ? `Unidade: ${selectedBranch}` : "Unidades: todas";
  }
  if (weeklyBranchesTitle) {
    weeklyBranchesTitle.textContent = selectedBranch
      ? `Resultado da unidade ${selectedBranch}`
      : "Resultados por unidade";
  }
  renderWeeklyDailyFinished(weekly.finished_by_day || []);
  renderWeeklyShiftProductivity(weekly.productivity_by_shift || []);
  renderWeeklyBranchesTable(weekly.branches || []);
}

function renderInstallationsTab(weekly, filters = {}) {
  const total = Number(weekly.installations || 0);
  const techRows = Array.isArray(weekly.installations_by_technician)
    ? weekly.installations_by_technician
    : [];
  const topTech = techRows[0] || null;
  const periodStart = filters.start_date || weekly.period_start || today;
  const periodEnd = filters.end_date || weekly.period_end || periodStart;
  const selectedTechnicians = Array.isArray(filters.technicians) ? filters.technicians : [];
  const selectedBranch = normalizeText(filters.branch || "");
  const selectedCity = normalizeText(filters.city || "");
  const selectedSubjects = Array.isArray(filters.subject) ? filters.subject : [];
  const selectedSubjectGroup = normalizeText(filters.subject_group_label || "");
  const periodText = periodStart === periodEnd
    ? formatDateOnly(periodStart)
    : `${formatDateOnly(periodStart)} a ${formatDateOnly(periodEnd)}`;

  if (installationsRangeValue) {
    installationsRangeValue.textContent = `Periodo: ${periodText}`;
  }
  if (installationsScopeValue) {
    const scopeParts = [
      selectedBranch ? `Unidade: ${selectedBranch}` : "Unidades: todas",
      selectedCity ? `Cidade: ${selectedCity}` : "Cidades: todas",
      selectedSubjectGroup
        ? `Produtividade OS: ${selectedSubjectGroup}`
        : selectedSubjects.length
          ? `Produtividade OS: ${selectedSubjects.length} tipo(s)`
          : "Produtividade OS: todos os tipos",
      selectedTechnicians.length ? `Colaboradores: ${selectedTechnicians.length}` : "Colaboradores: todos",
    ];
    installationsScopeValue.textContent = scopeParts.join(" | ");
  }
  if (installationsTotalValue) {
    installationsTotalValue.textContent = formatNumber(total);
  }
  if (installationsTopDayValue) {
    installationsTopDayValue.textContent = formatNumber(techRows.length);
  }
  if (installationsTopDayMeta) {
    installationsTopDayMeta.textContent = techRows.length
      ? `${formatNumber(techRows.length)} tecnico(s) com instalacao`
      : "Sem instalacoes";
  }
  renderInstallationsDailyBars(weekly.installations_by_day || []);
  renderInstallationsTechnicians(techRows, total);
  renderInstallationsProductivityRanking(
    weekly.technician_productivity_ranking || [],
    periodText
  );
  renderInstallationsSubjectMedian(
    weekly.median_execution_by_subject || [],
    periodText
  );
  if (installationsTopInstallerName) {
    installationsTopInstallerName.textContent = topTech ? normalizeText(topTech.technician || "-") : "-";
  }
  if (installationsTopInstallerCount) {
    installationsTopInstallerCount.textContent = topTech ? `${formatNumber(topTech.installations)} instalacoes` : "0 instalacoes";
  }
  if (installationsTopInstallerRate) {
    const rate = topTech && total ? Number(topTech.installations || 0) / Math.max(1, total) : 0;
    installationsTopInstallerRate.textContent = `${formatNumber(rate)} inst./total`;
  }
}

function setInstallationsSubTab(tabName) {
  const targetName = tabName || "ranking";
  installationsSubTabButtons.forEach((button) => {
    const isActive = button.dataset.installationsTab === targetName;
    button.classList.toggle("active", isActive);
  });
  installationsSubTabPanels.forEach((panel) => {
    panel.hidden = panel.dataset.installationsPanel !== targetName;
  });
}

function renderInstallationsDailyBars(rows) {
  if (!installationsDailyBars) {
    return;
  }
  const dailyRows = Array.isArray(rows) ? rows : [];
  const maxCount = Math.max(...dailyRows.map((row) => Number(row.finished_orders || 0)), 0);
  installationsDailyBars.innerHTML = "";
  if (!dailyRows.length) {
    installationsDailyBars.innerHTML = "<div class='weekly-daily-empty'>Sem instalacoes no periodo.</div>";
    return;
  }
  dailyRows.forEach((row) => {
    const count = Number(row.finished_orders || 0);
    const height = maxCount ? Math.max(4, Math.round((count / maxCount) * 100)) : 2;
    const bar = document.createElement("div");
    bar.className = "weekly-daily-bar";
    bar.innerHTML = `
      <div class="weekly-daily-value">${formatNumber(count)}</div>
      <div class="weekly-daily-track">
        <div class="weekly-daily-fill" style="height: ${height}%"></div>
      </div>
      <div class="weekly-daily-label">${escapeHtml(normalizeText(row.weekday_short || "-"))}</div>
    `;
    installationsDailyBars.appendChild(bar);
  });
}

function renderInstallationsTechnicians(rows, totalInstallations) {
  if (!installationsTechnicianList) {
    return;
  }
  const maxCount = Math.max(...rows.map((row) => Number(row.installations || 0)), 0);
  installationsTechnicianList.innerHTML = "";
  if (!rows.length) {
    installationsTechnicianList.innerHTML = "<div class='installations-empty'>Sem instalacoes por tecnico.</div>";
    return;
  }
  rows.forEach((row, index) => {
    const count = Number(row.installations || 0);
    const width = maxCount ? Math.max(3, Math.round((count / maxCount) * 100)) : 0;
    const item = document.createElement("article");
    item.className = "installations-tech-card";
    item.innerHTML = `
      <div class="installations-tech-head">
        <strong class="installations-tech-name">
          <span class="installations-rank">${index + 1}</span>
          <span>${escapeHtml(normalizeText(row.technician || "Sem tecnico"))}</span>
        </strong>
        <span>${formatNumber(count)}</span>
      </div>
      <div class="installations-tech-track">
        <div class="installations-tech-fill" style="width: ${width}%"></div>
      </div>
    `;
    installationsTechnicianList.appendChild(item);
  });
}

function resolveMedianBarClass(value, maxValue) {
  if (!maxValue) {
    return "is-fast";
  }
  const ratio = value / maxValue;
  if (ratio >= 0.75) {
    return "is-slow";
  }
  if (ratio >= 0.5) {
    return "is-medium";
  }
  return "is-fast";
}

function renderInstallationsSubjectMedian(rows, periodText) {
  if (!installationsSubjectMedianBars) {
    return;
  }
  const subjectRows = Array.isArray(rows) ? rows : [];
  const orderedRows = [...subjectRows].sort((left, right) => {
    const leftAvg = Number(left.avg_execution_minutes || 0);
    const rightAvg = Number(right.avg_execution_minutes || 0);
    if (rightAvg !== leftAvg) {
      return rightAvg - leftAvg;
    }
    return Number(right.median_execution_minutes || 0) - Number(left.median_execution_minutes || 0);
  });
  const maxMinutes = Math.max(
    ...orderedRows.flatMap((row) => [
      Number(row.avg_execution_minutes || 0),
      Number(row.median_execution_minutes || 0),
    ]),
    0,
  );
  if (installationsSubjectMedianSummary) {
    const fastest = subjectRows.reduce((best, row) => {
      const value = Number(row.median_execution_minutes);
      if (!Number.isFinite(value)) {
        return best;
      }
      if (!best || value < Number(best.median_execution_minutes)) {
        return row;
      }
      return best;
    }, null);
    installationsSubjectMedianSummary.textContent = fastest
      ? `Periodo: ${periodText} | ${formatNumber(subjectRows.length)} tipo(s) | Azul: media | Laranja: mediana | Menor mediana: ${formatNumber(fastest.median_execution_minutes)} min`
      : `Periodo: ${periodText} | Sem tempos de execucao por tipo`;
  }
  installationsSubjectMedianBars.innerHTML = "";
  if (!orderedRows.length) {
    installationsSubjectMedianBars.innerHTML =
      "<div class='installations-empty'>Nenhum tipo de OS com tempo de execucao nos filtros atuais.</div>";
    return;
  }
  orderedRows.forEach((row) => {
    const average = Number(row.avg_execution_minutes || 0);
    const median = Number(row.median_execution_minutes || 0);
    const averageWidth = maxMinutes ? Math.max(4, Math.round((average / maxMinutes) * 100)) : 0;
    const medianWidth = maxMinutes ? Math.max(4, Math.round((median / maxMinutes) * 100)) : 0;
    const averageLabel = averageWidth >= 12 ? `${formatNumber(average)} min` : "";
    const medianLabel = medianWidth >= 12 ? `${formatNumber(median)} min` : "";
    const item = document.createElement("div");
    item.className = "subject-median-row";
    item.innerHTML = `
      <div class="subject-median-name">${escapeHtml(normalizeText(row.subject || "Sem assunto"))}</div>
      <div class="subject-median-plot">
        <div class="subject-median-track">
          <div class="subject-median-fill is-average" style="width: ${averageWidth}%">${escapeHtml(averageLabel)}</div>
        </div>
        <div class="subject-median-track">
          <div class="subject-median-fill is-median" style="width: ${medianWidth}%">${escapeHtml(medianLabel)}</div>
        </div>
      </div>
      <div class="subject-median-side-values">
        <span class="is-average">${formatNumber(average)} min</span>
        <span class="is-median">${formatNumber(median)} min</span>
      </div>
    `;
    installationsSubjectMedianBars.appendChild(item);
  });
}

function renderInstallationsProductivityRanking(rows, periodText) {
  if (!installationsProductivityTable) {
    return;
  }
  const rankingRows = Array.isArray(rows) ? rows : [];
  if (installationsProductivitySummary) {
    const withExecution = rankingRows.filter((row) => row.avg_execution_minutes !== null && row.avg_execution_minutes !== undefined);
    const bestMedian = withExecution.reduce((best, row) => {
      const value = Number(row.median_execution_minutes);
      if (!Number.isFinite(value)) {
        return best;
      }
      if (!best || value < Number(best.median_execution_minutes)) {
        return row;
      }
      return best;
    }, null);
    installationsProductivitySummary.textContent = bestMedian
      ? `${periodText} | ${formatNumber(rankingRows.length)} tecnico(s) | melhor mediana ${formatNumber(bestMedian.median_execution_minutes)} min`
      : `${periodText} | ${formatNumber(rankingRows.length)} tecnico(s) | sem tempos de execucao`;
  }
  installationsProductivityTable.innerHTML = "";
  if (!rankingRows.length) {
    installationsProductivityTable.innerHTML =
      "<tr><td colspan='8'>Nenhum tecnico encontrado para os filtros atuais.</td></tr>";
    return;
  }
  rankingRows.forEach((row, index) => {
    const rank = index + 1;
    const tr = document.createElement("tr");
    if (rank === 1) {
      tr.className = "is-top";
    }
    const technician = normalizeText(row.technician || "Sem tecnico");
    tr.innerHTML = `
      <td><span class="productivity-rank-badge">${rank}</span></td>
      <td>
        <div class="installations-tech-cell">
          <strong>${escapeHtml(technician)}</strong>
          <span>${rank === 1 ? "Melhor desempenho" : "Tecnico"}</span>
        </div>
      </td>
      <td><span class="installations-number-cell"><strong>${formatNumber(row.total_orders ?? 0)}</strong><span>OS</span></span></td>
      <td><span class="installations-number-cell"><strong>${formatNumber(row.installations ?? 0)}</strong><span>Inst.</span></span></td>
      <td><span class="installations-number-cell"><strong>${Number(row.active_days || 0) ? formatNumber(row.active_days) : "-"}</strong><span>Dias</span></span></td>
      <td><span class="installations-number-cell"><strong>${formatNumber(row.orders_per_day ?? 0)}</strong><span>OS/dia</span></span></td>
      <td><span class="installations-number-cell"><strong>${row.avg_execution_minutes === null || row.avg_execution_minutes === undefined ? "-" : formatNumber(row.avg_execution_minutes)}</strong><span>Medio</span></span></td>
      <td><span class="installations-number-cell"><strong>${row.median_execution_minutes === null || row.median_execution_minutes === undefined ? "-" : formatNumber(row.median_execution_minutes)}</strong><span>Mediana</span></span></td>
    `;
    installationsProductivityTable.appendChild(tr);
  });
}

function renderWeeklyDailyFinished(rows) {
  if (!weeklyDailyBars) {
    return;
  }
  const dailyRows = Array.isArray(rows) ? rows : [];
  const maxCount = Math.max(...dailyRows.map((row) => Number(row.finished_orders || 0)), 0);
  const total = dailyRows.reduce((sum, row) => sum + Number(row.finished_orders || 0), 0);
  const peakRow = dailyRows.reduce((best, row) => {
    const current = Number(row.finished_orders || 0);
    const bestValue = Number(best?.finished_orders || 0);
    return current > bestValue ? row : best;
  }, null);
  const sundayRow = dailyRows.find((row) => String(row.weekday_short || "") === "Dom");
  const peakCount = Number(peakRow?.finished_orders || 0);
  const peakPercent = total ? (peakCount / total) * 100 : 0;

  weeklyDailyBars.innerHTML = "";
  if (!dailyRows.length) {
    weeklyDailyBars.innerHTML = "<div class='weekly-daily-empty'>Sem dados no periodo.</div>";
  } else {
    dailyRows.forEach((row) => {
      const count = Number(row.finished_orders || 0);
      const height = maxCount ? Math.max(4, Math.round((count / maxCount) * 100)) : 2;
      const isPeak = peakCount > 0 && count === peakCount;
      const bar = document.createElement("div");
      bar.className = `weekly-daily-bar${isPeak ? " is-peak" : ""}`;
      bar.innerHTML = `
        <div class="weekly-daily-value">${formatNumber(count)}</div>
        <div class="weekly-daily-track">
          <div class="weekly-daily-fill" style="height: ${height}%"></div>
        </div>
        <div class="weekly-daily-label">${escapeHtml(normalizeText(row.weekday_short || "-"))}${isPeak ? " *" : ""}</div>
      `;
      weeklyDailyBars.appendChild(bar);
    });
  }

  if (weeklyDailyTotalValue) {
    weeklyDailyTotalValue.textContent = formatNumber(total);
  }
  if (weeklyDailyPeakValue) {
    weeklyDailyPeakValue.textContent = formatNumber(peakCount);
  }
  if (weeklyDailyPeakMeta) {
    weeklyDailyPeakMeta.textContent = peakRow?.weekday
      ? `Pico (${normalizeText(peakRow.weekday)})`
      : "Pico";
  }
  if (weeklyDailyPeakPercentValue) {
    weeklyDailyPeakPercentValue.textContent = `${formatNumber(peakPercent)}%`;
  }
  if (weeklyDailySundayValue) {
    weeklyDailySundayValue.textContent = formatNumber(sundayRow?.finished_orders || 0);
  }
}

function renderWeeklyShiftProductivity(rows) {
  if (!weeklyShiftCards) {
    return;
  }
  const shifts = Array.isArray(rows) ? rows : [];
  const toneByKey = {
    morning: "morning",
    afternoon: "afternoon",
    night: "night",
  };
  weeklyShiftCards.innerHTML = "";
  if (!shifts.length) {
    weeklyShiftCards.innerHTML = "<div class='weekly-daily-empty'>Sem dados por turno.</div>";
    return;
  }
  shifts.forEach((shift) => {
    const percent = Number(shift.percentage || 0);
    const tone = toneByKey[shift.key] || "morning";
    const card = document.createElement("article");
    card.className = `weekly-shift-card is-${tone}`;
    card.innerHTML = `
      <div class="weekly-shift-label">${escapeHtml(normalizeText(shift.label || "-"))} (${escapeHtml(normalizeText(shift.period || "-"))})</div>
      <div class="weekly-shift-percent">${formatNumber(percent)}%</div>
      <div class="weekly-shift-count">${formatNumber(shift.finished_orders || 0)} OS</div>
      <div class="weekly-shift-track">
        <div class="weekly-shift-fill" style="width: ${Math.max(0, Math.min(100, percent))}%"></div>
      </div>
    `;
    weeklyShiftCards.appendChild(card);
  });
}

function applyWeeklyPeriodInputs() {
  loadMetrics().catch((error) => {
    meta.textContent = error.message || "Erro ao aplicar periodo da visao semanal.";
  });
}

function renderWeeklyBranchesTable(rows) {
  if (!weeklyBranchesTable) {
    return;
  }
  weeklyBranchesTable.innerHTML = "";
  if (!rows.length) {
    weeklyBranchesTable.innerHTML =
      "<tr><td colspan='5'>Nenhuma OS finalizada no periodo.</td></tr>";
    return;
  }
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${escapeHtml(normalizeText(row.branch || "Sem unidade"))}</td>
      <td>${formatNumber(row.finished_orders ?? 0)}</td>
      <td>${formatNumber(row.installations ?? 0)}</td>
      <td>${formatNumber(row.installation_percentage ?? 0)}%</td>
      <td>${formatNumber(row.active_technicians ?? 0)}</td>
    `;
    weeklyBranchesTable.appendChild(tr);
  });
}

function updateBodyModalLock() {
  if (cardOrdersModalOpen || boardDelayReportModalOpen || boardCommentModalOpen) {
    document.body.classList.add("modal-open");
    return;
  }
  document.body.classList.remove("modal-open");
}

function openCardOrdersModal(metric, label) {
  if (!cardOrdersModalOverlay || !cardOrdersModalTitle || !cardOrdersModalMeta || !cardOrdersModalTable) {
    return;
  }
  cardOrdersModalOpen = true;
  cardOrdersModalTitle.textContent = `OS do card: ${normalizeText(label || metric)}`;
  cardOrdersModalMeta.textContent = "Carregando...";
  cardOrdersModalTable.innerHTML = "<tr><td colspan='11'>Carregando OS...</td></tr>";
  cardOrdersModalOverlay.hidden = false;
  cardOrdersModalOverlay.classList.add("open");
  updateBodyModalLock();

  loadCardOrders(metric, label).catch((error) => {
    cardOrdersModalMeta.textContent = error.message || "Falha ao carregar detalhes do card.";
    cardOrdersModalTable.innerHTML =
      "<tr><td colspan='11'>Nao foi possivel carregar as OS deste card.</td></tr>";
  });
}

function closeCardOrdersModal() {
  if (!cardOrdersModalOverlay) {
    return;
  }
  cardOrdersModalOpen = false;
  cardOrdersModalOverlay.classList.remove("open");
  cardOrdersModalOverlay.hidden = true;
  updateBodyModalLock();
}

function buildBoardDelayReportQuery() {
  const params = new URLSearchParams();
  params.set("date", boardDateInput.value || today);
  if (boardSelectedTeamKey) {
    params.set("team_key", boardSelectedTeamKey);
  } else {
    const teamName = normalizeBoardTeamName(boardTeamInput?.value || "");
    if (teamName) {
      params.set("team_name", teamName);
    }
  }
  params.set("_ts", String(Date.now()));
  return params.toString();
}

async function loadBoardDelayReport() {
  const payload = {
    selected_technicians: getBoardTechnicianValues(),
    entries: boardEntriesState,
  };
  const response = await fetch(`/api/operations-board/delay-report?${buildBoardDelayReportQuery()}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || `Falha ao gerar relatorio: ${response.status}`);
  }
  return data;
}

function renderBoardDelayType(value) {
  if (String(value || "").toLowerCase() === "atraso") {
    return `<span class="delay-type-chip">${renderChip("Atraso", "warn")}</span>`;
  }
  return `<span class="delay-type-chip">${renderChip("OS", "info")}</span>`;
}

function buildDelayReportCombinedNote(row) {
  return normalizeText(row.comment_note || "").trim();
}

function renderBoardDelayReport(data) {
  if (!boardDelayReportMeta || !boardDelayReportTableWrap) {
    return;
  }
  boardDelayReportDataState = data || null;
  if (boardDelayReportPrintBtn) {
    boardDelayReportPrintBtn.disabled = false;
  }
  const summary = data.summary || {};
  const selectedTechs = formatFilterLabel(data.selected_technicians, "Todos");
  boardDelayReportMeta.textContent =
    `Data: ${data.date || boardDateInput.value || "-"} | ` +
    `Tecnicos: ${selectedTechs} | ` +
    `OS: ${summary.orders_count ?? 0} | ` +
    `Registros de atraso: ${summary.delay_rows_count ?? 0} | ` +
    `Minutos de atraso (com medicao): ${formatNumber(summary.delay_minutes_total)}`;

  const technicians = data.technicians || [];
  if (!technicians.length) {
    boardDelayReportTableWrap.innerHTML =
      "<p class='meta'>Nenhum dado encontrado para o periodo/filtro selecionado.</p>";
    return;
  }

  const sectionsHtml = technicians
    .map((technician, techIndex) => {
      const rows = technician.rows || [];
      const rowsHtml = rows.length
        ? rows
            .map((row, rowIndex) => {
              const combinedNote = buildDelayReportCombinedNote(row);
              const formattedMessage = formatRelatoMessage(combinedNote);
              const hasMessage = Boolean(formattedMessage);
              const detailKey = `delay-relato-${techIndex}-${rowIndex}`;
              const previewMessage = buildRelatoPreview(formattedMessage, 56);
              return `
                <tr>
                  <td>${renderBoardDelayType(row.type)}</td>
                  <td>${escapeHtml(normalizeText(row.slot_label || "-"))}</td>
                  <td>${escapeHtml(formatOrderWithCustomer(row.os_id, row.customer_name))}</td>
                  <td>${escapeHtml(normalizeText(row.subject_name || "-"))}</td>
                  <td>${escapeHtml(normalizeText(row.branch_name || "-"))}</td>
                  <td>${escapeHtml(normalizeText(row.start_at || "-"))}</td>
                  <td>${escapeHtml(normalizeText(row.displacement_at || "-"))}</td>
                  <td>${escapeHtml(normalizeText(row.executed_at || "-"))}</td>
                  <td>${escapeHtml(normalizeText(row.finalized_at || "-"))}</td>
                  <td>${row.delay_minutes == null ? "-" : escapeHtml(String(row.delay_minutes))}</td>
                  <td>
                    ${
                      hasMessage
                        ? `
                          <div class="relato-preview">
                            <span class="relato-snippet">${escapeHtml(previewMessage)}</span>
                            <button type="button" class="relato-toggle-btn" data-detail-key="${escapeHtmlAttr(detailKey)}">Ver comentario</button>
                          </div>
                        `
                        : "<span class='relato-detail-empty'>Sem comentario</span>"
                    }
                  </td>
                </tr>
                ${
                  hasMessage
                    ? `
                      <tr class="relato-detail-row" data-detail-key="${escapeHtmlAttr(detailKey)}" hidden>
                        <td colspan="11">
                          <div class="relato-detail-box">${escapeHtml(formattedMessage).replace(/\n/g, "<br>")}</div>
                        </td>
                      </tr>
                    `
                    : ""
                }
              `;
            })
            .join("")
        : "<tr><td colspan='11'>Nenhum registro para este tecnico.</td></tr>";

      return `
        <section class="delay-report-tech">
          <h4>${escapeHtml(normalizeText(technician.technician || "Sem tecnico"))}</h4>
          <p class="meta">
            OS: ${technician.orders_count ?? 0} |
            Registros de atraso: ${technician.delay_rows_count ?? 0} |
            Minutos de atraso: ${formatNumber(technician.delay_minutes_total)}
          </p>
          <div class="table-shell table-scroll">
            <table class="modern-table">
              <thead>
                <tr>
                  <th>Tipo</th>
                  <th>Horario</th>
                  <th>OS / Cliente</th>
                  <th>Assunto</th>
                  <th>Filial</th>
                  <th>Inicio</th>
                  <th>Desloc.</th>
                  <th>Exec.</th>
                  <th>Fim</th>
                  <th>Atraso (min)</th>
                  <th>Comentario</th>
                </tr>
              </thead>
              <tbody>
                ${rowsHtml}
              </tbody>
            </table>
          </div>
        </section>
      `;
    })
    .join("");

  boardDelayReportTableWrap.innerHTML = sectionsHtml;
}

function buildBoardDelayReportPrintMarkup(data) {
  const summary = data.summary || {};
  const selectedTechs = formatFilterLabel(data.selected_technicians, "Todos");
  const generatedAt = new Date().toLocaleString("pt-BR");
  const technicians = Array.isArray(data.technicians) ? data.technicians : [];

  const sectionsHtml = technicians.length
    ? technicians
        .map((technician) => {
          const rows = Array.isArray(technician.rows) ? technician.rows : [];
          const rowsHtml = rows.length
            ? rows
                .map((row) => {
                  const note = formatRelatoMessage(buildDelayReportCombinedNote(row));
                  const noteText = note || "-";
                  const noteHtml = escapeHtml(noteText).replace(/\n/g, "<br>");
                  return `
                    <tr class="print-main-row">
                      <td>${escapeHtml(normalizeText(row.type || "-"))}</td>
                      <td>${escapeHtml(normalizeText(row.slot_label || "-"))}</td>
                      <td>${escapeHtml(formatOrderWithCustomer(row.os_id, row.customer_name))}</td>
                      <td>${escapeHtml(normalizeText(row.subject_name || "-"))}</td>
                      <td>${escapeHtml(normalizeText(row.branch_name || "-"))}</td>
                      <td>${escapeHtml(normalizeText(row.start_at || "-"))}</td>
                      <td>${escapeHtml(normalizeText(row.displacement_at || "-"))}</td>
                      <td>${escapeHtml(normalizeText(row.executed_at || "-"))}</td>
                      <td>${escapeHtml(normalizeText(row.finalized_at || "-"))}</td>
                      <td>${row.delay_minutes == null ? "-" : escapeHtml(String(row.delay_minutes))}</td>
                      <td class="print-comment-cell">${noteHtml}</td>
                    </tr>
                  `;
                })
                .join("")
            : "<tr><td colspan='11'>Nenhum registro para este tecnico.</td></tr>";

          return `
            <section class="tech-block">
              <h3>${escapeHtml(normalizeText(technician.technician || "Sem tecnico"))}</h3>
              <p class="tech-meta">
                OS: ${technician.orders_count ?? 0} |
                Registros de atraso: ${technician.delay_rows_count ?? 0} |
                Minutos de atraso: ${formatNumber(technician.delay_minutes_total)}
              </p>
              <table>
                <thead>
                  <tr>
                    <th>Tipo</th>
                    <th>Horario</th>
                    <th>OS / Cliente</th>
                    <th>Assunto</th>
                    <th>Filial</th>
                    <th>Inicio</th>
                    <th>Desloc.</th>
                    <th>Exec.</th>
                    <th>Fim</th>
                    <th>Atraso (min)</th>
                    <th>Comentario</th>
                  </tr>
                </thead>
                <tbody>
                  ${rowsHtml}
                </tbody>
              </table>
            </section>
          `;
        })
        .join("")
    : "<p>Nenhum dado encontrado para o periodo/filtro selecionado.</p>";

  return `
    <div class="print-report">
      <h1>Relatorio tecnico</h1>
      <p class="meta">Data: ${escapeHtml(normalizeText(data.date || boardDateInput.value || "-"))}</p>
      <p class="meta">Tecnicos: ${escapeHtml(normalizeText(selectedTechs))}</p>
      <p class="summary">
        OS: ${summary.orders_count ?? 0} |
        Registros de atraso: ${summary.delay_rows_count ?? 0} |
        Minutos de atraso (com medicao): ${escapeHtml(formatNumber(summary.delay_minutes_total))}
      </p>
      ${sectionsHtml}
      <p class="meta">Gerado em: ${escapeHtml(generatedAt)}</p>
    </div>
  `;
}

function clearBoardDelayReportPrintMode() {
  document.body.classList.remove("print-delay-report");
  if (delayReportPrintHost) {
    delayReportPrintHost.innerHTML = "";
  }
}

function printBoardDelayReport() {
  if (!boardDelayReportDataState) {
    alert("Gere o relatorio de atrasos antes de imprimir.");
    return;
  }
  if (!delayReportPrintHost) {
    alert("Nao foi possivel montar o layout de impressao.");
    return;
  }
  delayReportPrintHost.innerHTML = buildBoardDelayReportPrintMarkup(boardDelayReportDataState);
  document.body.classList.add("print-delay-report");
  setTimeout(() => {
    window.print();
  }, 80);
}

function setBoardDelayReportLoadingState(message = "Gerando relatorio...") {
  boardDelayReportDataState = null;
  if (boardDelayReportPrintBtn) {
    boardDelayReportPrintBtn.disabled = true;
  }
  if (boardDelayReportMeta) {
    boardDelayReportMeta.textContent = message;
  }
  if (boardDelayReportTableWrap) {
    boardDelayReportTableWrap.innerHTML = "<p class='meta'>Carregando dados...</p>";
  }
}

async function refreshBoardDelayReportModal(message = "Gerando relatorio...") {
  setBoardDelayReportLoadingState(message);
  try {
    const data = await loadBoardDelayReport();
    renderBoardDelayReport(data);
  } catch (error) {
    boardDelayReportDataState = null;
    if (boardDelayReportPrintBtn) {
      boardDelayReportPrintBtn.disabled = true;
    }
    if (boardDelayReportMeta) {
      boardDelayReportMeta.textContent = error.message || "Falha ao gerar relatorio.";
    }
    if (boardDelayReportTableWrap) {
      boardDelayReportTableWrap.innerHTML =
        "<p class='meta'>Nao foi possivel montar o relatorio de atrasos.</p>";
    }
    throw error;
  }
}

async function loadSavedMapForDelayReport(selectedListId) {
  if (!(boardDelayReportSavedListSelect instanceof HTMLSelectElement)) {
    return;
  }
  const normalizedListId = normalizeText(selectedListId || "").trim();
  if (!normalizedListId) {
    boardFeedback.textContent = "Selecione um mapa salvo para impressao.";
    renderBoardSavedLists();
    return;
  }

  boardDelayReportSavedListSelect.disabled = true;
  try {
    const selectedList = await loadBoardFromSavedListId(normalizedListId);
    await refreshBoardDelayReportModal("Carregando mapa salvo e gerando relatorio...");
    const listLabel = normalizeBoardTeamName(selectedList?.team_name || "") || "Sem equipe";
    boardFeedback.textContent = `Mapa salvo carregado automaticamente para impressao: ${listLabel}.`;
  } catch (error) {
    boardFeedback.textContent = error.message || "Erro ao carregar mapa salvo para impressao.";
  } finally {
    boardDelayReportSavedListSelect.disabled = false;
    renderBoardSavedLists();
  }
}

function openBoardDelayReportModal() {
  if (
    !boardDelayReportModalOverlay ||
    !boardDelayReportModalTitle ||
    !boardDelayReportMeta ||
    !boardDelayReportTableWrap
  ) {
    return;
  }
  boardDelayReportModalOpen = true;
  boardDelayReportModalTitle.textContent = "Relatorio tecnico";
  setBoardDelayReportLoadingState("Gerando relatorio...");
  renderBoardSavedLists();
  boardDelayReportModalOverlay.hidden = false;
  boardDelayReportModalOverlay.classList.add("open");
  updateBodyModalLock();

  if (boardDelayReportSavedListSelect instanceof HTMLSelectElement) {
    boardDelayReportSavedListSelect.disabled = true;
  }
  loadBoardSavedLists({ silent: true, allDates: true })
    .catch((error) => {
      console.error("Falha ao atualizar mapas salvos no modal de impressao:", error);
    })
    .finally(() => {
      if (boardDelayReportSavedListSelect instanceof HTMLSelectElement) {
        boardDelayReportSavedListSelect.disabled = false;
      }
      renderBoardSavedLists();
    });

  refreshBoardDelayReportModal("Gerando relatorio...").catch(() => {
    // Feedback ja definido no modal por refreshBoardDelayReportModal.
  });
}

function closeBoardDelayReportModal() {
  if (!boardDelayReportModalOverlay) {
    return;
  }
  boardDelayReportModalOpen = false;
  boardDelayReportModalOverlay.classList.remove("open");
  boardDelayReportModalOverlay.hidden = true;
  clearBoardDelayReportPrintMode();
  updateBodyModalLock();
}

function getBoardCommentPreview(value) {
  const text = String(value || "").trim();
  if (!text) {
    return "";
  }
  const preview = buildRelatoPreview(text, 34);
  return `Coment.: ${preview}`;
}

function openBoardCommentModal(rowIndex) {
  if (
    !boardCommentModalOverlay ||
    !boardCommentTextarea ||
    !boardCommentModalMeta ||
    !Number.isInteger(rowIndex) ||
    !boardEntriesState[rowIndex]
  ) {
    return;
  }
  boardCommentEditingIndex = rowIndex;
  boardCommentModalOpen = true;
  const entry = boardEntriesState[rowIndex];
  const osId = String(entry.os_id || "").trim() || "(sem OS)";
  boardCommentModalMeta.textContent = `Comentario para OS ${osId} - Tecnico: ${normalizeText(
    entry.technician_names || entry.team_label || "-"
  )}`;
  boardCommentTextarea.value = normalizeText(entry.comment_note || "");
  boardCommentModalOverlay.hidden = false;
  boardCommentModalOverlay.classList.add("open");
  updateBodyModalLock();
  boardCommentTextarea.focus();
  boardCommentTextarea.setSelectionRange(
    boardCommentTextarea.value.length,
    boardCommentTextarea.value.length
  );
}

function closeBoardCommentModal() {
  if (!boardCommentModalOverlay) {
    return;
  }
  boardCommentModalOpen = false;
  boardCommentEditingIndex = null;
  boardCommentModalOverlay.classList.remove("open");
  boardCommentModalOverlay.hidden = true;
  updateBodyModalLock();
}

function saveBoardCommentFromModal() {
  if (!(boardCommentTextarea instanceof HTMLTextAreaElement)) {
    return;
  }
  if (!Number.isInteger(boardCommentEditingIndex) || !boardEntriesState[boardCommentEditingIndex]) {
    closeBoardCommentModal();
    return;
  }
  boardEntriesState[boardCommentEditingIndex].comment_note = boardCommentTextarea.value;
  boardDirty = true;
  boardFeedback.textContent = "Comentario salvo na linha. Existem alteracoes nao salvas no mapa diario.";
  renderBoardEntries();
  closeBoardCommentModal();
}

function renderCardOrdersModalData(data, label) {
  const rows = data.orders || [];
  const filters = data.filters || {};
  const truncatedLabel = data.truncated
    ? ` | Exibindo ${data.returned_orders}/${data.total_orders}`
    : "";
  cardOrdersModalMeta.textContent =
    `Card: ${normalizeText(label || data.metric_label || data.metric || "-")} | ` +
    `Periodo: ${filters.start_date || "-"} a ${filters.end_date || "-"} | ` +
    `Grupo: ${formatFilterLabel(filters.subject_group_label, "Todos")} | ` +
    `Assunto: ${formatFilterLabel(filters.subject, "Todos")} | ` +
    `Filial: ${formatFilterLabel(filters.branch, "Todas")} | ` +
    `OS: ${data.total_orders ?? rows.length}${truncatedLabel}`;

  cardOrdersModalTable.innerHTML = "";
  if (!rows.length) {
    cardOrdersModalTable.innerHTML =
      "<tr><td colspan='11'>Nenhuma OS encontrada para este card com os filtros atuais.</td></tr>";
    return;
  }

  rows.forEach((row) => {
    const formattedMessage = formatRelatoMessage(row.technician_message || "");
    const hasMessage = Boolean(formattedMessage);
    const previewMessage = buildRelatoPreview(formattedMessage);
    const tr = document.createElement("tr");
    const detailKey = `relato-${String(row.os_id || "")}-${cardOrdersModalTable.childElementCount + 1}`;
    tr.innerHTML = `
      <td>${escapeHtml(formatOrderWithCustomer(row.os_id, row.customer_name))}</td>
      <td>${escapeHtml(normalizeText(row.technician_name || "-"))}</td>
      <td>${escapeHtml(normalizeText(row.subject_name || "-"))}</td>
      <td>${escapeHtml(normalizeText(row.branch_name || "-"))}</td>
      <td>${escapeHtml(formatDateTimeCell(row.opened_at, normalizeText(row.opened_time || "-")))}</td>
      <td>${escapeHtml(normalizeText(row.displacement_time || "-"))}</td>
      <td>${escapeHtml(normalizeText(row.execution_time || "-"))}</td>
      <td>${escapeHtml(formatDateTimeCell(row.rescheduled_at, normalizeText(row.rescheduled_time || "-")))}</td>
      <td>${escapeHtml(normalizeText(row.closed_time || "-"))}</td>
      <td>${escapeHtml(normalizeText(row.sla_label || "-"))}</td>
      <td>
        ${
          hasMessage
            ? `
              <div class="relato-preview">
                <span class="relato-snippet">${escapeHtml(previewMessage)}</span>
                <button type="button" class="relato-toggle-btn" data-detail-key="${escapeHtmlAttr(detailKey)}">Ver relato</button>
              </div>
            `
            : `<span class="relato-detail-empty">Sem relato</span>`
        }
      </td>
    `;
    cardOrdersModalTable.appendChild(tr);
    if (hasMessage) {
      const detailRow = document.createElement("tr");
      detailRow.className = "relato-detail-row";
      detailRow.hidden = true;
      detailRow.dataset.detailKey = detailKey;
      detailRow.innerHTML = `
        <td colspan="11">
          <div class="relato-detail-box">${escapeHtml(formattedMessage).replace(/\n/g, "<br>")}</div>
        </td>
      `;
      cardOrdersModalTable.appendChild(detailRow);
    }
  });
}

function renderProductivity(data) {
  const rows = [...(data.technician_movements || data.technician_sla || [])];
  rows.sort((left, right) => {
    const finishedDiff = (right.finished_orders ?? right.closed_orders ?? 0) - (left.finished_orders ?? left.closed_orders ?? 0);
    if (finishedDiff !== 0) {
      return finishedDiff;
    }
    const leftHandled = left.handled_orders ?? left.total_orders ?? 0;
    const rightHandled = right.handled_orders ?? right.total_orders ?? 0;
    const leftRate = leftHandled ? ((left.finished_orders ?? left.closed_orders ?? 0) / leftHandled) * 100 : 0;
    const rightRate = rightHandled ? ((right.finished_orders ?? right.closed_orders ?? 0) / rightHandled) * 100 : 0;
    if (rightRate !== leftRate) {
      return rightRate - leftRate;
    }
    return (right.sla_rate ?? 0) - (left.sla_rate ?? 0);
  });

  const summary = data.movements_summary || {};
  const techniciansTotal = summary.technicians_total ?? rows.length;
  const ordersHandled = summary.orders_handled ?? rows.reduce((acc, row) => acc + (row.handled_orders ?? row.total_orders ?? 0), 0);
  const ordersStarted = summary.orders_started ?? rows.reduce((acc, row) => acc + (row.started_orders ?? 0), 0);
  const ordersFinished = summary.orders_finished ?? rows.reduce((acc, row) => acc + (row.finished_orders ?? row.closed_orders ?? 0), 0);
  const avgExecution = summary.avg_execution_minutes;
  const slaDenominator = (data.sla?.within_sla ?? 0) + (data.sla?.overdue ?? 0);
  const avgSla = slaDenominator
    ? ((data.sla?.within_sla ?? 0) / slaDenominator) * 100
    : null;

  prodTechniciansTotalValue.textContent = techniciansTotal;
  prodOrdersHandledValue.textContent = ordersHandled;
  prodOrdersStartedValue.textContent = ordersStarted;
  prodOrdersFinishedValue.textContent = ordersFinished;
  prodAvgSlaValue.textContent = avgSla === null ? "-" : `${formatNumber(avgSla)}%`;
  prodAvgExecutionValue.textContent = avgExecution == null ? "-" : `${formatNumber(avgExecution)} min`;

  const filters = data.filters || {};
  const sync = data.last_sync;
  const filterText = [
    `Periodo: ${filters.start_date || "-"} a ${filters.end_date || "-"}`,
    `Grupo: ${formatFilterLabel(filters.subject_group_label, "Todos")}`,
    `Filial: ${formatFilterLabel(filters.branch, "Todas")}`,
    `Assunto: ${formatFilterLabel(filters.subject, "Todos")}`,
    `Tecnico: ${formatFilterLabel(filters.technician, "Todos")}`,
    `Status: ${formatFilterLabel(filters.status, "Todos")}`,
  ].join(" | ");
  const syncText = sync
    ? `Ultima sincronizacao: ${formatDate(sync.finished_at || sync.started_at)}`
    : "Sem sincronizacao registrada";
  productivityMeta.textContent = `${filterText} | ${syncText}`;
  renderProductivityChart(rows);

  productivityTable.innerHTML = "";
  if (!rows.length) {
    productivityTable.innerHTML =
      "<tr><td colspan='12'>Nenhum tecnico encontrado com os filtros aplicados.</td></tr>";
    return;
  }

  rows.forEach((row, index) => {
    const handledOrders = row.handled_orders ?? row.total_orders ?? 0;
    const startedOrders = row.started_orders ?? 0;
    const finishedOrders = row.finished_orders ?? row.closed_orders ?? 0;
    const inExecutionOrders = row.in_execution ?? 0;
    const completionRate = handledOrders ? (finishedOrders / handledOrders) * 100 : 0;
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${index + 1}</td>
      <td>${escapeHtml(normalizeText(row.technician || "-"))}</td>
      <td>${handledOrders}</td>
      <td>${startedOrders}</td>
      <td>${finishedOrders}</td>
      <td>${inExecutionOrders}</td>
      <td>${renderChip(`${formatNumber(completionRate)}%`, getSlaTone(completionRate))}</td>
      <td>${renderSlaChip(row.sla_rate)}</td>
      <td>${formatNumber(row.avg_response_minutes)}</td>
      <td>${formatNumber(row.avg_execution_minutes)}</td>
      <td>${formatNumber(row.avg_total_minutes)}</td>
      <td>${renderChip(String(row.overdue ?? 0), (row.overdue ?? 0) > 0 ? "danger" : "ok")}</td>
    `;
    productivityTable.appendChild(tr);
  });
}

function renderProductivityOrdersEmpty(message) {
  productivityOrdersTable.innerHTML = `<tr><td colspan='9'>${escapeHtml(normalizeText(message || "-"))}</td></tr>`;
  productivityOrdersMeta.textContent = normalizeText(message || "Sem detalhes para exibir.");
}

function renderProductivityOrders(data) {
  const rows = data.orders || [];
  const summary = data.summary || {};
  const filters = data.filters || {};
  const technicianLabel = normalizeText(filters.technician || prodTechnicianFilter.value || "-");
  productivityOrdersMeta.textContent =
    `Tecnico: ${technicianLabel} | Grupo: ${formatFilterLabel(filters.subject_group_label, "Todos")} | ` +
    `Assunto: ${formatFilterLabel(filters.subject, "Todos")} | OS: ${summary.total_orders ?? rows.length} | ` +
    `Com deslocamento: ${summary.with_displacement ?? 0} | ` +
    `Com execucao: ${summary.with_execution ?? 0} | Finalizadas: ${summary.with_closing ?? 0} | ` +
    `Com relato: ${summary.with_message ?? 0}`;

  productivityOrdersTable.innerHTML = "";
  if (!rows.length) {
    productivityOrdersTable.innerHTML =
      "<tr><td colspan='9'>Nenhuma OS encontrada para o tecnico e filtros selecionados.</td></tr>";
    return;
  }

  rows.forEach((row) => {
    const formattedMessage = formatRelatoMessage(row.technician_message || "");
    const hasMessage = Boolean(formattedMessage);
    const previewMessage = buildRelatoPreview(formattedMessage, 54);
    const tr = document.createElement("tr");
    const detailKey = `prod-relato-${String(row.os_id || "")}-${productivityOrdersTable.childElementCount + 1}`;
    tr.innerHTML = `
      <td>${escapeHtml(formatOrderWithCustomer(row.os_id, row.customer_name))}</td>
      <td>${escapeHtml(normalizeText(row.subject_name || "-"))}</td>
      <td>${escapeHtml(normalizeText(row.branch_name || "-"))}</td>
      <td>${escapeHtml(normalizeText(row.opened_time || "-"))}</td>
      <td>${escapeHtml(normalizeText(row.displacement_time || "-"))}</td>
      <td>${escapeHtml(normalizeText(row.execution_time || "-"))}</td>
      <td>${escapeHtml(normalizeText(row.closed_time || "-"))}</td>
      <td>${renderStatusChip(row.status || "-")}</td>
      <td>
        ${
          hasMessage
            ? `
              <div class="relato-preview">
                <span class="relato-snippet">${escapeHtml(previewMessage)}</span>
                <button type="button" class="relato-toggle-btn" data-detail-key="${escapeHtmlAttr(detailKey)}">Ver relato</button>
              </div>
            `
            : `<span class="relato-detail-empty">Sem relato</span>`
        }
      </td>
    `;
    productivityOrdersTable.appendChild(tr);
    if (hasMessage) {
      const detailRow = document.createElement("tr");
      detailRow.className = "relato-detail-row";
      detailRow.hidden = true;
      detailRow.dataset.detailKey = detailKey;
      detailRow.innerHTML = `
        <td colspan="9">
          <div class="relato-detail-box">${escapeHtml(formattedMessage).replace(/\n/g, "<br>")}</div>
        </td>
      `;
      productivityOrdersTable.appendChild(detailRow);
    }
  });
}

function renderHourlyChart(points) {
  const labels = points.map((point) => point.hour);
  const values = points.map((point) => point.count);
  const canvas = document.getElementById("hourlyChart");
  if (!(canvas instanceof HTMLCanvasElement)) {
    return;
  }
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    return;
  }
  if (hourlyChart) {
    hourlyChart.destroy();
  }
  const gradient = ctx.createLinearGradient(0, 0, 0, 280);
  gradient.addColorStop(0, CHART_THEME.hourlyBarTop);
  gradient.addColorStop(1, CHART_THEME.hourlyBarBottom);
  hourlyChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "OS efetuadas",
          data: values,
          borderWidth: 0,
          borderRadius: 10,
          maxBarThickness: 26,
          backgroundColor: gradient,
          hoverBackgroundColor: CHART_THEME.hourlyBarHover,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: buildChartTooltipOptions(),
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: CHART_THEME.axisTextSoft, maxRotation: 0, autoSkip: true, maxTicksLimit: 12 },
        },
        y: {
          beginAtZero: true,
          ticks: { precision: 0, color: CHART_THEME.axisTextSoft },
          grid: { color: CHART_THEME.axisGrid },
        },
      },
    },
  });
}

function renderSubjectsTable(rows) {
  subjectsTable.innerHTML = "";
  if (!rows.length) {
    subjectsTable.innerHTML = "<tr><td colspan='2'>Nenhuma ordem aberta encontrada.</td></tr>";
    return;
  }
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${escapeHtml(normalizeText(row.subject))}</td>
      <td>${renderChip(String(row.count ?? 0), "neutral")}</td>
    `;
    subjectsTable.appendChild(tr);
  });
}

function renderTechSlaTable(rows) {
  if (!(techSlaTable instanceof HTMLElement)) {
    return;
  }
  techSlaTable.innerHTML = "";
  if (!rows.length) {
    techSlaTable.innerHTML =
      "<tr><td colspan='11'>Nenhum tecnico encontrado com os filtros aplicados.</td></tr>";
    return;
  }

  rows.forEach((row) => {
    const handledOrders = row.handled_orders ?? row.total_orders ?? 0;
    const startedOrders = row.started_orders ?? 0;
    const inExecutionOrders = row.in_execution ?? 0;
    const finishedOrders = row.finished_orders ?? row.closed_orders ?? 0;
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${escapeHtml(normalizeText(row.technician))}</td>
      <td>${handledOrders}</td>
      <td>${startedOrders}</td>
      <td>${renderChip(String(inExecutionOrders), inExecutionOrders > 0 ? "info" : "neutral")}</td>
      <td>${renderChip(String(finishedOrders), finishedOrders > 0 ? "ok" : "neutral")}</td>
      <td>${renderSlaChip(row.sla_rate)}</td>
      <td>${renderChip(String(row.within_sla ?? 0), "ok")}</td>
      <td>${renderChip(String(row.overdue ?? 0), (row.overdue ?? 0) > 0 ? "danger" : "neutral")}</td>
      <td>${formatNumber(row.avg_response_minutes)}</td>
      <td>${formatNumber(row.avg_execution_minutes)}</td>
      <td>${formatNumber(row.avg_total_minutes)}</td>
    `;
    techSlaTable.appendChild(tr);
  });
}

function renderSubjectsChart(rows) {
  const canvas = document.getElementById("subjectsChart");
  if (!(canvas instanceof HTMLCanvasElement)) {
    return;
  }
  const chartRows = [...rows]
    .sort((left, right) => (right.count ?? 0) - (left.count ?? 0))
    .slice(0, 8);
  if (subjectsChart) {
    subjectsChart.destroy();
    subjectsChart = null;
  }
  if (!chartRows.length) {
    return;
  }
  const palette = CHART_THEME.doughnutPalette;
  subjectsChart = new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: chartRows.map((row) => normalizeText(row.subject || "Sem assunto")),
      datasets: [
        {
          data: chartRows.map((row) => row.count ?? 0),
          backgroundColor: chartRows.map((_row, index) => palette[index % palette.length]),
          borderColor: "rgba(10, 18, 52, 0.9)",
          borderWidth: 2,
          hoverOffset: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "60%",
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            boxWidth: 12,
            color: CHART_THEME.axisText,
          },
        },
        tooltip: buildChartTooltipOptions(),
      },
    },
  });
}

function renderTechPerformanceChart(rows) {
  const canvas = document.getElementById("techPerformanceChart");
  if (!(canvas instanceof HTMLCanvasElement)) {
    return;
  }
  const chartRows = [...rows]
    .sort(
      (left, right) =>
        (right.finished_orders ?? right.closed_orders ?? 0) -
        (left.finished_orders ?? left.closed_orders ?? 0)
    )
    .slice(0, 8);
  if (techPerformanceChart) {
    techPerformanceChart.destroy();
    techPerformanceChart = null;
  }
  if (!chartRows.length) {
    return;
  }
  techPerformanceChart = new Chart(canvas, {
    type: "bar",
    data: {
      labels: chartRows.map((row) => normalizeText(row.technician || "-")),
      datasets: [
        {
          label: "Finalizadas",
          data: chartRows.map((row) => row.finished_orders ?? row.closed_orders ?? 0),
          backgroundColor: CHART_THEME.techFinished,
          borderRadius: 8,
          maxBarThickness: 24,
        },
        {
          label: "Em execucao",
          data: chartRows.map((row) => row.in_execution ?? 0),
          backgroundColor: CHART_THEME.techExecution,
          borderRadius: 8,
          maxBarThickness: 24,
        },
      ],
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: CHART_THEME.axisText },
        },
        tooltip: buildChartTooltipOptions(),
      },
      scales: {
        x: {
          beginAtZero: true,
          ticks: { precision: 0, color: CHART_THEME.axisTextSoft },
          grid: { color: CHART_THEME.axisGrid },
        },
        y: {
          ticks: { color: CHART_THEME.axisTextSoft, font: { size: 11 } },
          grid: { display: false },
        },
      },
    },
  });
}

function renderProductivityChart(rows) {
  const canvas = document.getElementById("productivityChart");
  if (!(canvas instanceof HTMLCanvasElement)) {
    return;
  }
  if (productivityChart) {
    productivityChart.destroy();
    productivityChart = null;
  }
  if (!rows.length) {
    return;
  }
  const chartRows = [...rows].slice(0, 10);
  productivityChart = new Chart(canvas, {
    type: "bar",
    data: {
      labels: chartRows.map((row) => normalizeText(row.technician || "-")),
      datasets: [
        {
          label: "Taxa conclusao %",
          data: chartRows.map((row) => {
            const handled = row.handled_orders ?? row.total_orders ?? 0;
            const finished = row.finished_orders ?? row.closed_orders ?? 0;
            return handled ? Number(((finished / handled) * 100).toFixed(2)) : 0;
          }),
          backgroundColor: CHART_THEME.productivityBar,
          borderRadius: 8,
          maxBarThickness: 28,
        },
        {
          label: "SLA %",
          type: "line",
          data: chartRows.map((row) => Number(row.sla_rate ?? 0)),
          borderColor: CHART_THEME.productivityLineBorder,
          backgroundColor: CHART_THEME.productivityLineBg,
          tension: 0.28,
          pointRadius: 3,
          pointHoverRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: CHART_THEME.axisText },
        },
        tooltip: buildChartTooltipOptions(),
      },
      scales: {
        x: {
          ticks: { color: CHART_THEME.axisTextSoft, maxRotation: 45, minRotation: 0 },
          grid: { display: false },
        },
        y: {
          beginAtZero: true,
          max: 100,
          ticks: { color: CHART_THEME.axisTextSoft, callback: (value) => `${value}%` },
          grid: { color: CHART_THEME.axisGrid },
        },
      },
    },
  });
}

function getSlaTone(rateValue) {
  const rate = Number(rateValue);
  if (!Number.isFinite(rate)) {
    return "neutral";
  }
  if (rate >= 90) {
    return "ok";
  }
  if (rate >= 70) {
    return "warn";
  }
  return "danger";
}

function getStatusTone(statusValue) {
  const status = normalizeText(statusValue || "").trim().toUpperCase();
  if (!status || status === "-") {
    return "neutral";
  }
  if (["F", "FINALIZADA", "CONCLUIDA", "CONCLUÍDA"].includes(status)) {
    return "ok";
  }
  if (["EX", "EN", "E", "DS", "EM_EXECUCAO", "EM EXECUCAO", "EM_ANDAMENTO", "EM ANDAMENTO"].includes(status)) {
    return "info";
  }
  if (["AG", "AGENDA", "AGENDADA", "REAGENDADA", "REAGENDADO", "R", "PENDENTE"].includes(status)) {
    return "pending";
  }
  if (["C", "CA", "CANCELADA", "CANCELADO"].includes(status)) {
    return "danger";
  }
  return "neutral";
}

function renderChip(text, tone = "neutral") {
  const safeText = escapeHtml(normalizeText(text || "-"));
  const safeTone = ["ok", "danger", "warn", "info", "pending", "neutral"].includes(tone)
    ? tone
    : "neutral";
  return `<span class="chip chip-${safeTone}">${safeText}</span>`;
}

function renderSlaChip(rate) {
  if (rate === null || rate === undefined || Number.isNaN(Number(rate))) {
    return renderChip("-", "neutral");
  }
  return renderChip(`${formatNumber(rate)}%`, getSlaTone(rate));
}

function renderStatusChip(status) {
  return renderChip(status, getStatusTone(status));
}

function formatNumber(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "-";
  }
  return Number(value).toLocaleString("pt-BR", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  });
}

function formatMinutesAsHours(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "-";
  }
  const hours = Number(value) / 60;
  return `${hours.toLocaleString("pt-BR", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  })} h`;
}

async function refreshMetricsSilently() {
  if (isMetricsRefreshing) {
    return;
  }
  isMetricsRefreshing = true;
  try {
    await loadMetrics();
  } catch (error) {
    console.error("Falha no auto refresh de metricas:", error);
  } finally {
    isMetricsRefreshing = false;
  }
}

async function refreshProductivitySilently() {
  if (isProductivityRefreshing) {
    return;
  }
  isProductivityRefreshing = true;
  try {
    await Promise.all([loadProductivity(), loadProductivityOrders()]);
  } catch (error) {
    console.error("Falha no auto refresh de produtividade:", error);
  } finally {
    isProductivityRefreshing = false;
  }
}

function startAutoRefresh() {
  stopAutoRefresh();
  metricsRefreshTimer = setInterval(() => {
    if (!document.hidden) {
      refreshMetricsSilently();
      if (activeTab === "productivity") {
        refreshProductivitySilently();
      }
    }
  }, autoRefreshMetricsMs);
  filtersRefreshTimer = setInterval(() => {
    if (!document.hidden) {
      loadFilterOptions().catch((error) => {
        console.error("Falha no auto refresh de filtros:", error);
      });
    }
  }, autoRefreshFiltersMs);
}

function stopAutoRefresh() {
  if (metricsRefreshTimer) {
    clearInterval(metricsRefreshTimer);
    metricsRefreshTimer = null;
  }
  if (filtersRefreshTimer) {
    clearInterval(filtersRefreshTimer);
    filtersRefreshTimer = null;
  }
}

function normalizeBoardTeamName(value) {
  return normalizeText(value || "").trim();
}

function buildBoardSavedListId(entryDate, teamKey) {
  const normalizedDate = normalizeText(entryDate || "").trim();
  const normalizedKey = normalizeText(teamKey || "").trim().toLowerCase();
  if (!normalizedDate || !normalizedKey) {
    return "";
  }
  return `${normalizedDate}::${normalizedKey}`;
}

function formatBoardSavedListDate(entryDate) {
  const raw = normalizeText(entryDate || "").trim();
  const match = raw.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!match) {
    return raw || "-";
  }
  const [, year, month, day] = match;
  return `${day}/${month}/${year}`;
}

function findBoardSavedListById(listId) {
  const normalizedId = normalizeText(listId || "").trim();
  if (!normalizedId) {
    return null;
  }
  return (
    boardSavedListsState.find(
      (item) => normalizeText(item.list_id || "").trim() === normalizedId
    ) || null
  );
}

function findBoardSavedListByTeamName(teamName, { entryDate = null } = {}) {
  const normalizedName = normalizeBoardTeamName(teamName).toLowerCase();
  if (!normalizedName) {
    return null;
  }
  const normalizedEntryDate = normalizeText(entryDate || "").trim();
  return (
    boardSavedListsState.find(
      (item) =>
        normalizeBoardTeamName(item.team_name || "").toLowerCase() === normalizedName &&
        (!normalizedEntryDate || normalizeText(item.entry_date || "").trim() === normalizedEntryDate)
    ) || null
  );
}

function buildBoardSavedListOptionLabel(item) {
  const teamName = normalizeBoardTeamName(item.team_name || "") || "Sem equipe";
  const entryDate = formatBoardSavedListDate(item.entry_date);
  return `${entryDate} - ${teamName} (${Number(item.entry_count || 0)} linha(s))`;
}

function populateBoardSavedListSelect(selectElement, placeholderLabel) {
  if (!(selectElement instanceof HTMLSelectElement)) {
    return;
  }
  selectElement.innerHTML = "";
  const placeholderOption = document.createElement("option");
  placeholderOption.value = "";
  placeholderOption.textContent = placeholderLabel;
  selectElement.appendChild(placeholderOption);

  boardSavedListsState.forEach((item) => {
    const option = document.createElement("option");
    option.value = normalizeText(item.list_id || "").trim();
    option.textContent = buildBoardSavedListOptionLabel(item);
    selectElement.appendChild(option);
  });

  selectElement.value = boardSelectedSavedListId || "";
}

function renderBoardSavedLists() {
  populateBoardSavedListSelect(boardSavedListSelect, "Mapas salvos");
  populateBoardSavedListSelect(boardDelayReportSavedListSelect, "Mapas salvos para impressao");
  if (boardDeleteListBtn) {
    boardDeleteListBtn.disabled = !Boolean(findBoardSavedListById(boardSelectedSavedListId));
  }
  if (boardLoadSavedBtn) {
    boardLoadSavedBtn.disabled = !Boolean(findBoardSavedListById(boardSelectedSavedListId));
  }
}

function setBoardSavedListsState(
  lists,
  { preferredListId = "", preferredTeamKey = "", preferredTeamName = "", preferredEntryDate = "" } = {}
) {
  boardSavedListsState = Array.isArray(lists)
    ? lists
        .map((item) => ({
          ...item,
          entry_date: normalizeText(item?.entry_date || "").trim(),
          team_key: normalizeText(item?.team_key || "").trim().toLowerCase(),
          team_name: normalizeBoardTeamName(item?.team_name || ""),
          list_id: buildBoardSavedListId(item?.entry_date, item?.team_key),
        }))
        .filter((item) => item.list_id.length > 0)
    : [];

  let nextList = null;
  const normalizedPreferredListId = normalizeText(preferredListId || "").trim();
  if (normalizedPreferredListId) {
    nextList = findBoardSavedListById(normalizedPreferredListId);
  }

  if (!nextList) {
    const normalizedPreferredEntryDate = normalizeText(preferredEntryDate || "").trim();
    const normalizedPreferredKey = normalizeText(preferredTeamKey || "").trim().toLowerCase();
    if (normalizedPreferredEntryDate && normalizedPreferredKey) {
      nextList =
        boardSavedListsState.find(
          (item) =>
            item.entry_date === normalizedPreferredEntryDate &&
            item.team_key === normalizedPreferredKey
        ) || null;
    }
  }

  if (!nextList) {
    nextList = findBoardSavedListById(boardSelectedSavedListId);
  }

  if (!nextList) {
    const fromInput = findBoardSavedListByTeamName(boardTeamInput?.value || "", {
      entryDate: boardDateInput?.value || "",
    });
    if (fromInput) {
      nextList = fromInput;
    }
  }

  if (!nextList && boardSavedListsState.length) {
    const currentDate = normalizeText(boardDateInput?.value || "").trim();
    nextList =
      boardSavedListsState.find((item) => item.entry_date === currentDate) ||
      boardSavedListsState[0];
  }

  boardSelectedSavedListId = nextList ? nextList.list_id : "";
  boardSelectedTeamKey = nextList ? nextList.team_key : "";
  renderBoardSavedLists();
}

function buildBoardQuery() {
  const params = new URLSearchParams();
  params.set("date", boardDateInput.value || today);
  if (boardSelectedTeamKey) {
    params.set("team_key", boardSelectedTeamKey);
  } else {
    const teamName = normalizeBoardTeamName(boardTeamInput?.value || "");
    if (teamName) {
      params.set("team_name", teamName);
    }
  }
  const selectedTechnicians = getBoardTechnicianValues();
  if (selectedTechnicians.length) {
    appendMultiParams(params, "technician", selectedTechnicians);
  } else {
    params.append("technician", "__all__");
  }
  const selectedStatuses = getBoardStatusValues();
  if (selectedStatuses.length) {
    appendMultiParams(params, "status", selectedStatuses);
  } else {
    params.append("status", "__all__");
  }
  params.set("_ts", String(Date.now()));
  return params.toString();
}

function buildBoardDeleteQuery(teamKey, entryDate = null) {
  const params = new URLSearchParams();
  params.set("date", normalizeText(entryDate || "").trim() || boardDateInput.value || today);
  params.set("team_key", normalizeText(teamKey || "").trim().toLowerCase());
  params.set("_ts", String(Date.now()));
  return params.toString();
}

function buildBoardListsQuery({ allDates = false } = {}) {
  const params = new URLSearchParams();
  if (allDates) {
    params.set("all_dates", "true");
  } else {
    params.set("date", boardDateInput.value || today);
  }
  params.set("_ts", String(Date.now()));
  return params.toString();
}

async function loadBoardSavedLists({ silent = true, allDates = true } = {}) {
  const response = await fetch(`/api/operations-board/lists?${buildBoardListsQuery({ allDates })}`, {
    cache: "no-store",
    headers: { "Cache-Control": "no-cache" },
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Erro ao carregar listas salvas do mapa diario.");
  }
  setBoardSavedListsState(data.lists || [], {
    preferredListId: boardSelectedSavedListId,
    preferredTeamKey: boardSelectedTeamKey,
    preferredTeamName: boardTeamInput?.value || "",
    preferredEntryDate: boardDateInput?.value || "",
  });
  if (!silent && boardFeedback) {
    boardFeedback.textContent = "Listas salvas atualizadas.";
  }
  return data;
}

async function loadBoardFromSavedListId(selectedListId) {
  const normalizedListId = normalizeText(selectedListId || "").trim();
  if (!normalizedListId) {
    throw new Error("Selecione um mapa salvo para carregar.");
  }
  if (boardDirty) {
    throw new Error("Existem alteracoes nao salvas no mapa diario.");
  }
  const selectedList = findBoardSavedListById(normalizedListId);
  if (!selectedList) {
    throw new Error("Lista selecionada nao encontrada.");
  }

  boardSelectedSavedListId = selectedList.list_id;
  boardSelectedTeamKey = selectedList.team_key;
  boardDateInput.value = selectedList.entry_date || boardDateInput.value || today;
  boardTeamInput.value = selectedList.team_name || "";
  // Ao alternar para outro mapa salvo, limpa o filtro de tecnico atual
  // para permitir que o backend devolva os tecnicos gravados nesse mapa.
  ensureBoardTechnicianRows([]);
  refreshBoardTechnicianRowOptions();
  renderBoardSavedLists();
  await loadBoard();
  return selectedList;
}

async function loadBoardFromSavedSelection() {
  if (!(boardSavedListSelect instanceof HTMLSelectElement)) {
    return;
  }
  const selectedListId = normalizeText(boardSavedListSelect.value || boardSelectedSavedListId || "").trim();
  if (!selectedListId) {
    boardFeedback.textContent = "Selecione um mapa salvo para carregar.";
    boardSelectedSavedListId = "";
    boardSelectedTeamKey = "";
    renderBoardSavedLists();
    return;
  }
  await loadBoardFromSavedListId(selectedListId);
}

async function loadBoard({ silent = false, skipIfDirty = false } = {}) {
  if (skipIfDirty && boardDirty) {
    boardFeedback.textContent = "Existem alteracoes nao salvas no mapa diario.";
    return;
  }
  if (!silent) {
    boardFeedback.textContent = "Carregando mapa diario...";
  }
  const response = await fetch(`/api/operations-board?${buildBoardQuery()}`, {
    cache: "no-store",
    headers: { "Cache-Control": "no-cache" },
  });
  if (!response.ok) {
    throw new Error(`Falha ao carregar mapa diario: ${response.status}`);
  }
  const data = await response.json();
  const headerSelectedTechnicians = data.header?.selected_technicians || [];
  const headerSelectedStatuses = data.header?.selected_statuses || [];
  boardResponsibleInput.value = data.header?.responsible_name || "";
  boardShiftInput.value = data.header?.shift_label || "08:00 - 20:00";
  boardTeamInput.value = data.header?.team_name || "";
  boardGeneralNotesInput.value = data.header?.general_notes || "";
  boardSelectedTeamKey = normalizeText(data.header?.team_key || "").trim().toLowerCase();
  boardSelectedSavedListId = buildBoardSavedListId(boardDateInput.value || today, boardSelectedTeamKey);
  boardReferencesState = data.references || {
    orders: [],
    technicians: [],
    all_technicians: [],
    branches: [],
    statuses: [],
    time_slots: [],
  };
  setBoardStatusOptions(boardReferencesState.statuses || []);
  const referenceTechnicians = [
    ...(boardReferencesState.all_technicians || []),
    ...(boardReferencesState.technicians || []),
  ]
    .map((value) => String(value || "").trim())
    .filter((value) => value.length > 0);
  if (referenceTechnicians.length) {
    boardTechnicianOptionsState = [...new Set(referenceTechnicians)];
  }
  ensureBoardTechnicianRows(headerSelectedTechnicians);
  ensureBoardStatusRows(headerSelectedStatuses);
  refreshBoardTechnicianRowOptions();
  refreshBoardStatusRowOptions();
  boardEntriesState = (data.entries || []).map((entry) => ({
    ...entry,
    team_label: normalizeText(entry.team_label || entry.technician_names || ""),
    customer_name: normalizeText(entry.customer_name || ""),
    subject_name: normalizeText(entry.subject_name || ""),
    branch_name: normalizeText(entry.branch_name || ""),
    technician_names: normalizeText(entry.technician_names || entry.team_label || ""),
    opening_note: normalizeText(entry.opening_note || ""),
    occurrence_note: normalizeText(entry.occurrence_note || ""),
    comment_note: normalizeText(entry.comment_note || ""),
    status_label: normalizeText(entry.status_label || ""),
    os_exists_in_ixc: entry.os_exists_in_ixc !== false,
    os_validation_message: normalizeText(entry.os_validation_message || ""),
  }));
  if (!boardEntriesState.length) {
    boardEntriesState = [
      createEmptyBoardRow(
        boardReferencesState.time_slots?.[0] || "08:00 - 09:00",
        getBoardBranchFilterValue(),
        boardTeamInput.value || ""
      ),
    ];
  }
  boardDirty = false;
  boardSummaryState = data.summary || {};
  boardGeneratedState = Boolean(data.generated);
  setBoardSavedListsState(data.saved_lists || [], {
    preferredListId: boardSelectedSavedListId,
    preferredTeamKey: boardSelectedTeamKey,
    preferredTeamName: boardTeamInput.value || "",
    preferredEntryDate: boardDateInput.value || today,
  });
  renderBoardDataLists();
  renderBoardEntries();
  const feedbackTeam = normalizeText(boardTeamInput.value || "").trim();
  boardFeedback.textContent = Boolean(data.generated)
    ? `Mapa diario sugerido automaticamente com ${boardEntriesState.length} linha(s).${feedbackTeam ? ` Equipe: ${feedbackTeam}.` : ""}`
    : `Mapa diario carregado com ${boardEntriesState.length} linha(s).${feedbackTeam ? ` Equipe: ${feedbackTeam}.` : ""}`;
  renderBoardOrderDetails(null);
}

async function saveBoard() {
  const selectedTechnicians = getBoardTechnicianValues();
  const autoTeamName = selectedTechnicians.length ? selectedTechnicians.join(" + ") : "";
  const typedTeamName = normalizeBoardTeamName(boardTeamInput.value);
  const effectiveTeamName = autoTeamName || typedTeamName;
  if (autoTeamName && effectiveTeamName) {
    boardTeamInput.value = effectiveTeamName;
  }

  const normalizedEffectiveTeamKey = normalizeText(effectiveTeamName || "").trim().toLowerCase();
  const payloadTeamKey = normalizedEffectiveTeamKey || null;

  const payload = {
    responsible_name: boardResponsibleInput.value.trim(),
    shift_label: boardShiftInput.value.trim(),
    team_name: effectiveTeamName,
    team_key: payloadTeamKey,
    general_notes: boardGeneralNotesInput.value.trim(),
    selected_technicians: selectedTechnicians,
    entries: boardEntriesState,
  };
  const response = await fetch(`/api/operations-board?date=${boardDateInput.value}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Erro ao salvar mapa diario.");
  }
  boardReferencesState = data.references || boardReferencesState;
  const referenceTechnicians = [
    ...(boardReferencesState.all_technicians || []),
    ...(boardReferencesState.technicians || []),
  ]
    .map((value) => String(value || "").trim())
    .filter((value) => value.length > 0);
  if (referenceTechnicians.length) {
    boardTechnicianOptionsState = [...new Set(referenceTechnicians)];
  }
  setBoardStatusOptions(boardReferencesState.statuses || []);
  boardSelectedTeamKey = normalizeText(data.header?.team_key || "").trim().toLowerCase();
  boardSelectedSavedListId = buildBoardSavedListId(boardDateInput.value || today, boardSelectedTeamKey);
  boardTeamInput.value = data.header?.team_name || boardTeamInput.value || "";
  ensureBoardTechnicianRows(data.header?.selected_technicians || getBoardTechnicianValues());
  refreshBoardTechnicianRowOptions();
  refreshBoardStatusRowOptions();
  boardEntriesState = (data.entries || []).map((entry) => ({
    ...entry,
    team_label: normalizeText(entry.team_label || entry.technician_names || ""),
    customer_name: normalizeText(entry.customer_name || ""),
    subject_name: normalizeText(entry.subject_name || ""),
    branch_name: normalizeText(entry.branch_name || ""),
    technician_names: normalizeText(entry.technician_names || entry.team_label || ""),
    opening_note: normalizeText(entry.opening_note || ""),
    occurrence_note: normalizeText(entry.occurrence_note || ""),
    comment_note: normalizeText(entry.comment_note || ""),
    status_label: normalizeText(entry.status_label || ""),
    os_exists_in_ixc: entry.os_exists_in_ixc !== false,
    os_validation_message: normalizeText(entry.os_validation_message || ""),
  }));
  boardDirty = false;
  boardSummaryState = data.summary || {};
  boardGeneratedState = false;
  setBoardSavedListsState(data.saved_lists || [], {
    preferredListId: boardSelectedSavedListId,
    preferredTeamKey: boardSelectedTeamKey,
    preferredTeamName: boardTeamInput.value || "",
    preferredEntryDate: boardDateInput.value || today,
  });
  await loadBoardSavedLists({ silent: true, allDates: true });
  renderBoardDataLists();
  renderBoardEntries();
  boardFeedback.textContent = "Mapa diario salvo com sucesso.";
  renderBoardOrderDetails(null);
}

async function deleteBoardList(teamKey, entryDate = null) {
  const response = await fetch(`/api/operations-board?${buildBoardDeleteQuery(teamKey, entryDate)}`, {
    method: "DELETE",
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Erro ao excluir lista salva.");
  }
  return data;
}

async function refreshBoardSilently() {
  if (isBoardRefreshing || boardDirty) {
    return;
  }
  isBoardRefreshing = true;
  try {
    await loadBoard({ silent: true, skipIfDirty: true });
  } catch (error) {
    console.error("Falha no auto refresh do mapa diario:", error);
  } finally {
    isBoardRefreshing = false;
  }
}

function refreshBoardSummary() {
  const summary = boardSummaryState || {};
  const generated = boardGeneratedState;
  const selectedBranch = getBoardBranchFilterValue();
  const selectedSubject = getBoardSubjectFilterValue();
  const selectedTechnicians = getBoardTechnicianValues();
  const selectedStatuses = getBoardStatusValues();
  const visibleIndexes = getBoardVisibleEntryIndexes();
  const invalidVisibleCount = visibleIndexes.reduce((count, index) => {
    return count + (boardEntriesState[index]?.os_exists_in_ixc === false ? 1 : 0);
  }, 0);

  const totalOrders = summary.total_orders ?? 0;
  let openOrders = summary.open_orders ?? 0;
  let executionOrders = summary.execution_orders ?? 0;
  let closedOrders = summary.closed_orders ?? 0;
  let techniciansIdentified = summary.technicians_identified ?? 0;
  let entryCount = summary.entry_count ?? boardEntriesState.length;
  const hasSavedEntries = Boolean(summary.has_saved_entries);

  let visibleOrders = totalOrders;
  if (selectedBranch || selectedSubject || selectedTechnicians.length || selectedStatuses.length) {
    const visibleOrderIds = new Set();
    const technicians = new Set();
    openOrders = 0;
    executionOrders = 0;
    closedOrders = 0;
    visibleIndexes.forEach((index) => {
      const entry = boardEntriesState[index] || {};
      const osId = normalizeText(entry.os_id || "").trim();
      if (!osId || visibleOrderIds.has(osId)) {
        return;
      }
      visibleOrderIds.add(osId);
      const technician = normalizeText(
        entry.technician_names || entry.team_label || ""
      ).trim();
      if (technician) {
        technicians.add(technician);
      }
      const statusLabel = normalizeText(entry.status_label || "").trim().toUpperCase();
      if (statusLabel === "FINALIZADA") {
        closedOrders += 1;
      } else if (["EM EXECUCAO", "DESLOCAMENTO"].includes(statusLabel)) {
        executionOrders += 1;
      } else {
        openOrders += 1;
      }
    });
    visibleOrders = visibleOrderIds.size;
    techniciansIdentified = technicians.size;
    entryCount = visibleIndexes.length;
  }

  boardTotalOrdersValue.textContent = visibleOrders;
  boardOpenOrdersValue.textContent = openOrders;
  boardExecutionOrdersValue.textContent = executionOrders;
  boardClosedOrdersValue.textContent = closedOrders;

  if (!visibleOrders && !visibleIndexes.length) {
    const filtersLabel = [];
    if (selectedBranch) {
      filtersLabel.push(`filial ${normalizeText(selectedBranch)}`);
    }
    if (selectedSubject) {
      filtersLabel.push(`assunto ${normalizeText(selectedSubject)}`);
    }
    if (selectedStatuses.length) {
      filtersLabel.push(`status ${selectedStatuses.join(", ")}`);
    }
    boardSummaryNote.textContent = filtersLabel.length
      ? `Nenhuma OS encontrada para ${filtersLabel.join(" e ")} nesta data.`
      : "Nenhuma OS encontrada no IXC para esta data. O operador pode preencher o mapa manualmente.";
    return;
  }

  const filtersPrefix = [];
  if (selectedBranch) {
    filtersPrefix.push(`Filial selecionada: ${normalizeText(selectedBranch)}`);
  }
  if (selectedSubject) {
    filtersPrefix.push(`Assunto selecionado: ${normalizeText(selectedSubject)}`);
  }
  if (selectedTechnicians.length) {
    filtersPrefix.push(`Tecnicos selecionados: ${selectedTechnicians.join(", ")}`);
  }
  if (selectedStatuses.length) {
    filtersPrefix.push(`Status selecionados: ${selectedStatuses.join(", ")}`);
  }
  const selectedTeam = normalizeText(boardTeamInput.value || "").trim();
  if (selectedTeam) {
    filtersPrefix.push(`Equipe: ${selectedTeam}`);
  }
  const selectionPrefix = filtersPrefix.length ? `${filtersPrefix.join(". ")}. ` : "";

  if (generated && !hasSavedEntries) {
    boardSummaryNote.textContent =
      `${selectionPrefix}Sugestao automatica montada com ${entryCount} linha(s) visiveis. Tecnicos identificados: ${techniciansIdentified}. Revise e salve o mapa.`;
    if (invalidVisibleCount) {
      boardSummaryNote.textContent += ` ${invalidVisibleCount} linha(s) com OS invalida.`;
    }
    return;
  }

  boardSummaryNote.textContent =
    `${selectionPrefix}Mapa salvo com ${entryCount} linha(s) visiveis. Tecnicos identificados no IXC hoje: ${techniciansIdentified}.`;
  if (invalidVisibleCount) {
    boardSummaryNote.textContent += ` ${invalidVisibleCount} linha(s) com OS invalida.`;
  }
}

function renderBoardDataLists() {
  populateSelect(boardBranchFilter, getBoardBranchOptions(), "Todas as filiais");
  populateSelect(boardSubjectFilter, getBoardSubjectOptions(), "Todos os assuntos");
  setBoardStatusOptions([
    ...(boardReferencesState.statuses || []),
    ...boardEntriesState.map((entry) => normalizeText(entry.status_label || "")),
  ]);
  refreshBoardStatusRowOptions();

  boardOsIdList.innerHTML = "";
  (boardReferencesState.orders || []).forEach((order) => {
    const option = document.createElement("option");
    const label = [
      order.os_id,
      normalizeText(order.customer_name || "Sem cliente"),
      normalizeText(order.subject_name || "Sem assunto"),
      getOrderTechnicianDisplay(order) || "Sem tecnico",
    ].join(" | ");
    option.value = String(order.os_id || "");
    option.label = label;
    boardOsIdList.appendChild(option);
  });

  boardTimeSlotList.innerHTML = "";
  (boardReferencesState.time_slots || []).forEach((slot) => {
    const option = document.createElement("option");
    option.value = slot;
    boardTimeSlotList.appendChild(option);
  });
}

function renderBoardEntries() {
  operationsBoardTable.innerHTML = "";
  boardVisibleEntryIndexes = getBoardVisibleEntryIndexes();

  if (!boardVisibleEntryIndexes.length) {
    operationsBoardTable.innerHTML =
      "<tr><td colspan='5'>Nenhuma linha encontrada para os filtros selecionados.</td></tr>";
    refreshBoardSummary();
    return;
  }

  const technicianRanks = buildBoardTechnicianRenderRanks(boardVisibleEntryIndexes);
  const sortedVisibleIndexes = [...boardVisibleEntryIndexes].sort((leftIndex, rightIndex) =>
    compareBoardEntryDisplayOrder(leftIndex, rightIndex, technicianRanks)
  );

  sortedVisibleIndexes.forEach((index) => {
    const entry = boardEntriesState[index];
    const tr = document.createElement("tr");
    if (entry.os_exists_in_ixc === false) {
      tr.classList.add("board-row-warning");
    }
    tr.dataset.rowIndex = String(index);
    const osHint = entry.os_exists_in_ixc === false
      ? `<span class="field-hint warning">${escapeHtml(
          normalizeText(entry.os_validation_message || "OS nao encontrada na sincronizacao atual do IXC.")
        )}</span>`
      : "";
    tr.innerHTML = `
      <td><input list="boardTimeSlotList" data-field="slot_label" value="${escapeHtmlAttr(entry.slot_label || "")}" /></td>
      <td class="journal-main-cell">
        <div class="journal-main-grid">
          <div class="journal-os-wrap">
            <span class="journal-label">No OS</span>
            <input list="boardOsIdList" data-field="os_id" value="${escapeHtmlAttr(entry.os_id || "")}" />
            ${osHint}
          </div>
          <div class="journal-time-wrap">
            <span class="journal-label">Hora inicial</span>
            <input data-field="start_at" placeholder="08:30" value="${escapeHtmlAttr(entry.start_at || "")}" />
          </div>
        </div>
        <span class="journal-label">Equipe</span>
        <input data-field="team_label" value="${escapeHtmlAttr(normalizeText(entry.team_label || ""))}" />
        <span class="journal-label">Relato abertura</span>
        <textarea data-field="opening_note">${escapeHtml(normalizeText(entry.opening_note || ""))}</textarea>
        <div class="journal-meta">
          <span class="journal-meta-item">Assunto: ${escapeHtml(normalizeText(entry.subject_name || "-"))}</span>
          <span class="journal-meta-item">Filial: ${escapeHtml(normalizeText(entry.branch_name || "-"))}</span>
          <span class="journal-meta-item">Tecnico: ${escapeHtml(normalizeText(entry.technician_names || "-"))}</span>
        </div>
      </td>
      <td class="journal-customer-cell">
        <span class="journal-label">Cliente</span>
        <input
          data-field="customer_name"
          placeholder="Nome do cliente"
          value="${escapeHtmlAttr(normalizeText(entry.customer_name || ""))}"
        />
      </td>
      <td class="journal-occurrence-cell">
        <div class="journal-occurrence-grid">
          <div>
            <span class="journal-label">Deslocamento</span>
            <input data-field="displacement_at" value="${escapeHtmlAttr(entry.displacement_at || "")}" />
          </div>
          <div>
            <span class="journal-label">Executada</span>
            <input data-field="executed_at" value="${escapeHtmlAttr(entry.executed_at || "")}" />
          </div>
          <div>
            <span class="journal-label">Finalizada</span>
            <input data-field="finalized_at" value="${escapeHtmlAttr(entry.finalized_at || "")}" />
          </div>
          <div>
            <span class="journal-label">Status</span>
            <input data-field="status_label" value="${escapeHtmlAttr(normalizeText(entry.status_label || ""))}" />
          </div>
        </div>
        <span class="journal-label">Comentario</span>
        <textarea data-field="comment_note">${escapeHtml(normalizeText(entry.comment_note || ""))}</textarea>
      </td>
      <td class="journal-actions-cell">
        <div class="journal-actions-wrap">
          <button type="button" class="btn-ghost" data-action="remove-row">Remover</button>
          <button type="button" class="btn-ghost" data-action="insert-row-below">Adicionar linha</button>
        </div>
      </td>
    `;
    operationsBoardTable.appendChild(tr);
  });
  refreshBoardSummary();
}

function buildBoardTechnicianRenderRanks(indexes) {
  const ranks = new Map();
  indexes.forEach((index, order) => {
    const technician = getBoardEntryTechnicianLabel(boardEntriesState[index] || {});
    if (!ranks.has(technician)) {
      ranks.set(technician, order);
    }
  });
  return ranks;
}

function getBoardEntryTechnicianLabel(entry) {
  return normalizeText(entry?.technician_names || entry?.team_label || "Sem tecnico informado").trim();
}

function parseBoardClockToMinutes(value) {
  const match = normalizeText(value || "").match(/(\d{2}):(\d{2})/);
  if (!match) {
    return Number.POSITIVE_INFINITY;
  }
  return Number(match[1]) * 60 + Number(match[2]);
}

function parseBoardSlotStartToMinutes(slotLabel) {
  const match = normalizeText(slotLabel || "").match(/(\d{2}):(\d{2})\s*-/);
  if (!match) {
    return Number.POSITIVE_INFINITY;
  }
  return Number(match[1]) * 60 + Number(match[2]);
}

function getBoardEntryPrimaryDisplayMinutes(entry) {
  const candidates = [
    parseBoardClockToMinutes(entry?.displacement_at),
    parseBoardClockToMinutes(entry?.executed_at),
    parseBoardClockToMinutes(entry?.finalized_at),
    parseBoardClockToMinutes(entry?.start_at),
    parseBoardSlotStartToMinutes(entry?.slot_label),
  ].filter((value) => Number.isFinite(value));

  return candidates.length ? candidates[0] : Number.POSITIVE_INFINITY;
}

function compareBoardEntryDisplayOrder(leftIndex, rightIndex, technicianRanks) {
  const leftEntry = boardEntriesState[leftIndex] || {};
  const rightEntry = boardEntriesState[rightIndex] || {};

  const leftTechnician = getBoardEntryTechnicianLabel(leftEntry);
  const rightTechnician = getBoardEntryTechnicianLabel(rightEntry);
  const leftRank = technicianRanks.get(leftTechnician) ?? Number.MAX_SAFE_INTEGER;
  const rightRank = technicianRanks.get(rightTechnician) ?? Number.MAX_SAFE_INTEGER;
  if (leftRank !== rightRank) {
    return leftRank - rightRank;
  }

  const leftMinutes = getBoardEntryPrimaryDisplayMinutes(leftEntry);
  const rightMinutes = getBoardEntryPrimaryDisplayMinutes(rightEntry);
  if (leftMinutes !== rightMinutes) {
    return leftMinutes - rightMinutes;
  }

  const leftHasOs = normalizeText(leftEntry.os_id || "").trim() ? 0 : 1;
  const rightHasOs = normalizeText(rightEntry.os_id || "").trim() ? 0 : 1;
  if (leftHasOs !== rightHasOs) {
    return leftHasOs - rightHasOs;
  }

  return leftIndex - rightIndex;
}

function appendOrderDetailItem(label, value) {
  const card = document.createElement("div");
  card.className = "details-item";
  const key = document.createElement("div");
  key.className = "key";
  key.textContent = label;
  const val = document.createElement("div");
  val.className = "value";
  val.textContent = normalizeText(value || "-");
  card.appendChild(key);
  card.appendChild(val);
  boardOrderDetailsGrid.appendChild(card);
}

function renderBoardOrderDetails(details) {
  if (!boardOrderDetailsGrid || !boardOrderDetailsMeta) {
    return;
  }
  boardOrderDetailsGrid.innerHTML = "";
  if (!details) {
    boardOrderDetailsMeta.textContent = "Selecione uma OS no mapa para ver os detalhes completos.";
    return;
  }
  const osId = String(details.os_id || "").trim();
  const isMissing =
    osId &&
    !String(details.updated_at || "").trim() &&
    !String(details.subject || "").trim() &&
    !String(details.subject_name || "").trim();
  if (isMissing) {
    boardOrderDetailsMeta.textContent = `OS ${osId} nao encontrada na base sincronizada do app.`;
    appendOrderDetailItem("OS", osId);
    return;
  }

  const subject = details.subject || details.subject_name || "";
  const branch = details.branch || details.branch_name || "";
  const technician = details.technician_name || "";
  const technicianId = details.technician_id || "";
  const status = details.status || "";
  const slaLabel = details.sla?.label || "-";
  const durations = details.durations || {};
  const rawHighlights = details.raw_highlights || {};

  boardOrderDetailsMeta.textContent = `OS ${osId} carregada. Ultima atualizacao local: ${normalizeText(
    details.updated_at || "-"
  )}.`;

  appendOrderDetailItem("OS", osId);
  appendOrderDetailItem("Cliente", details.customer_name || "-");
  appendOrderDetailItem("Status", status || "-");
  appendOrderDetailItem("Assunto", subject || "-");
  appendOrderDetailItem("Filial", branch || "-");
  appendOrderDetailItem(
    "Tecnico",
    technician ? `${technician}${technicianId ? ` (ID ${technicianId})` : ""}` : "-"
  );
  appendOrderDetailItem("Abertura", details.opened_at || "-");
  appendOrderDetailItem("Assumido", details.assumed_at || "-");
  appendOrderDetailItem("Inicio execucao", details.execution_started_at || "-");
  if (details.execution_source_label) {
    appendOrderDetailItem("Origem inicio execucao", details.execution_source_label);
  }
  appendOrderDetailItem("Fechamento", details.closed_at || "-");
  appendOrderDetailItem("Prazo (SLA)", details.due_at || "-");
  appendOrderDetailItem("SLA", slaLabel);
  appendOrderDetailItem("Tempo resposta (min)", formatNumber(durations.response_minutes));
  appendOrderDetailItem("Tempo execucao (min)", formatNumber(durations.execution_minutes));
  appendOrderDetailItem("Tempo total (min)", formatNumber(durations.total_minutes));
  if (details.process_summary) {
    appendOrderDetailItem("Registro processo", details.process_summary);
  }

  const additionalKeys = Object.keys(rawHighlights).filter(
    (key) =>
      ![
        "id",
        "id_assunto",
        "id_filial",
        "funcionario",
        "data_abertura",
        "data_hora_assumido",
        "data_hora_execucao",
        "data_inicio",
        "data_final",
        "data_fechamento",
      ].includes(key)
  );
  additionalKeys.slice(0, 6).forEach((key) => {
    appendOrderDetailItem(key, rawHighlights[key]);
  });
}

function createEmptyBoardRow(defaultSlot, defaultBranch = "", defaultTeam = "") {
  const teamLabel = normalizeText(defaultTeam || boardTeamInput?.value || "");
  return {
    slot_label: defaultSlot || "",
    team_label: teamLabel,
    os_id: "",
    customer_name: "",
    subject_name: "",
    branch_name: defaultBranch || "",
    technician_names: "",
    opening_note: "",
    occurrence_note: "",
    comment_note: "",
    start_at: "",
    displacement_at: "",
    executed_at: "",
    finalized_at: "",
    status_label: "",
    os_exists_in_ixc: true,
    os_validation_message: "",
  };
}

async function fetchOrderDetails(osId, { force = false } = {}) {
  const normalized = String(osId || "").trim();
  if (!normalized) {
    return null;
  }
  if (!force && orderDetailsCache.has(normalized)) {
    return orderDetailsCache.get(normalized);
  }
  const response = await fetch(`/api/orders/${encodeURIComponent(normalized)}?_ts=${Date.now()}`, {
    cache: "no-store",
    headers: { "Cache-Control": "no-cache" },
  });
  if (response.status === 404) {
    orderDetailsCache.set(normalized, null);
    return null;
  }
  if (!response.ok) {
    throw new Error(`Falha ao buscar detalhes da OS ${normalized}: ${response.status}`);
  }
  const data = await response.json();
  orderDetailsCache.set(normalized, data);
  return data;
}

function getReferenceOrderById(osId) {
  return (boardReferencesState.orders || []).find(
    (order) => String(order.os_id || "").trim() === String(osId || "").trim()
  );
}

async function applyOrderReferenceToRow(index) {
  const entry = boardEntriesState[index];
  if (!entry || !entry.os_id) {
    updateBoardEntryValidation(index);
    renderBoardOrderDetails(null);
    return;
  }
  const osId = String(entry.os_id || "").trim();
  const match = getReferenceOrderById(osId);
  let fetched = null;
  if (!match) {
    fetched = await fetchOrderDetails(osId);
    if (!fetched) {
      updateBoardEntryValidation(index, false);
      renderBoardOrderDetails({
        os_id: osId,
        customer_name: "",
        status: "",
        subject: "",
        branch: "",
        technician_id: "",
        technician_name: "",
        opened_at: "",
        execution_started_at: "",
        closed_at: "",
        due_at: "",
        updated_at: "",
        sla: { status: "", label: "" },
        durations: {
          response_minutes: null,
          execution_minutes: null,
          total_minutes: null,
        },
        raw_highlights: {},
      });
      return;
    }
  }

  const source = match || fetched;
  if (!source) {
    updateBoardEntryValidation(index, false);
    renderBoardOrderDetails(null);
    return;
  }

  if (!entry.subject_name) {
    entry.subject_name = normalizeText(source.subject_name || source.subject || "");
  }
  if (!entry.customer_name) {
    entry.customer_name = normalizeText(source.customer_name || "");
  }
  if (!entry.branch_name) {
    entry.branch_name = normalizeText(source.branch_name || source.branch || "");
  }
  if (!entry.technician_names) {
    entry.technician_names = normalizeText(
      source.technician_name || getOrderTechnicianDisplay(source)
    );
  }
  entry.team_label = normalizeText(
    entry.team_label ||
      boardTeamInput.value ||
      entry.technician_names ||
      source.technician_name ||
      getOrderTechnicianDisplay(source)
  );
  updateBoardEntryValidation(index, true);
  if (fetched) {
    renderBoardOrderDetails(fetched);
    return;
  }
  const details = await fetchOrderDetails(osId).catch(() => null);
  renderBoardOrderDetails(details);
}

function getBoardBranchFilterValue() {
  return boardBranchFilter.value && boardBranchFilter.value !== "__all__"
    ? boardBranchFilter.value
    : "";
}

function getBoardSubjectFilterValue() {
  return boardSubjectFilter.value && boardSubjectFilter.value !== "__all__"
    ? boardSubjectFilter.value
    : "";
}

function getBoardEntryStatusFilterKeys(entry) {
  const keys = new Set();
  const statusKey = normalizeBoardStatusFilterKey(entry?.status_label || "");
  if (statusKey) {
    keys.add(statusKey);
    if (statusKey === "ABERTA") {
      keys.add("AGUARDANDO");
    }
  }
  const statusToken = normalizeBoardStatusToken(entry?.status_label || "");
  if (statusToken === "AGUARDANDO_RELATO") {
    keys.add("AGUARDANDO");
  }
  if (!keys.size) {
    if (String(entry?.finalized_at || "").trim()) {
      keys.add("FINALIZADA");
    } else if (String(entry?.executed_at || "").trim()) {
      keys.add("EM_EXECUCAO");
    } else if (String(entry?.displacement_at || "").trim()) {
      keys.add("DESLOCAMENTO");
    } else if (String(entry?.os_id || "").trim()) {
      keys.add("ABERTA");
      keys.add("AGUARDANDO");
    }
  }
  return keys;
}

function entryMatchesSelectedBoardStatuses(entry, selectedStatusSet) {
  if (!(selectedStatusSet instanceof Set) || !selectedStatusSet.size) {
    return true;
  }
  const statusKeys = getBoardEntryStatusFilterKeys(entry);
  if (!statusKeys.size) {
    return false;
  }
  for (const key of statusKeys) {
    if (selectedStatusSet.has(key)) {
      return true;
    }
  }
  return false;
}

function getBoardVisibleEntryIndexes() {
  const selectedBranch = getBoardBranchFilterValue();
  const selectedSubject = getBoardSubjectFilterValue();
  const selectedTechnicians = getBoardTechnicianValues();
  const selectedStatuses = getBoardStatusValues();
  const selectedTechnicianSet = new Set(
    selectedTechnicians
      .map((value) => normalizeBoardTechnicianToken(value))
      .filter((value) => value.length > 0)
  );
  const selectedStatusSet = new Set(
    selectedStatuses
      .map((value) => normalizeBoardStatusFilterKey(value))
      .filter((value) => value.length > 0)
  );
  const hasTechnicianFilter = selectedTechnicianSet.size > 0;
  const hasStatusFilter = selectedStatusSet.size > 0;
  if (!selectedBranch && !selectedSubject && !hasTechnicianFilter && !hasStatusFilter) {
    return boardEntriesState.map((_, index) => index);
  }
  return boardEntriesState.reduce((indexes, entry, index) => {
    const branchMatches =
      !selectedBranch || String(entry.branch_name || "").trim() === selectedBranch;
    const subjectMatches =
      !selectedSubject || String(entry.subject_name || "").trim() === selectedSubject;
    const technicianMatches =
      !hasTechnicianFilter || entryMatchesSelectedBoardTechnicians(entry, selectedTechnicianSet);
    const statusMatches = !hasStatusFilter || entryMatchesSelectedBoardStatuses(entry, selectedStatusSet);
    if (branchMatches && subjectMatches && technicianMatches && statusMatches) {
      indexes.push(index);
    }
    return indexes;
  }, []);
}

function normalizeBoardTechnicianToken(value) {
  const text = normalizeText(value || "").trim();
  if (!text) {
    return "";
  }
  return text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .toUpperCase();
}

function extractBoardTechnicianTokens(value) {
  const text = normalizeText(value || "").trim();
  if (!text) {
    return [];
  }
  return text
    .split(/[,;/|+]/)
    .map((item) => normalizeBoardTechnicianToken(item))
    .filter((item) => item.length > 0);
}

function entryMatchesSelectedBoardTechnicians(entry, selectedTechnicianSet) {
  const tokens = new Set([
    ...extractBoardTechnicianTokens(entry?.technician_names || ""),
    ...extractBoardTechnicianTokens(entry?.team_label || ""),
  ]);
  if (!tokens.size) {
    return false;
  }
  for (const token of tokens) {
    if (selectedTechnicianSet.has(token)) {
      return true;
    }
  }
  return false;
}

function getBoardBranchOptions() {
  const values = new Set();
  (boardReferencesState.branches || []).forEach((branch) => {
    if (String(branch || "").trim()) {
      values.add(String(branch).trim());
    }
  });
  boardEntriesState.forEach((entry) => {
    if (String(entry.branch_name || "").trim()) {
      values.add(String(entry.branch_name).trim());
    }
  });
  return [...values].sort((left, right) =>
    normalizeText(left).localeCompare(normalizeText(right), "pt-BR", {
      numeric: true,
      sensitivity: "base",
    })
  );
}

function getBoardSubjectOptions() {
  const values = new Set();
  (boardReferencesState.orders || []).forEach((order) => {
    if (String(order.subject_name || "").trim()) {
      values.add(String(order.subject_name).trim());
    }
  });
  boardEntriesState.forEach((entry) => {
    if (String(entry.subject_name || "").trim()) {
      values.add(String(entry.subject_name).trim());
    }
  });
  return [...values].sort((left, right) =>
    normalizeText(left).localeCompare(normalizeText(right), "pt-BR", {
      numeric: true,
      sensitivity: "base",
    })
  );
}

function updateBoardEntryValidation(index, knownExists = null) {
  const entry = boardEntriesState[index];
  if (!entry) {
    return;
  }
  const osId = String(entry.os_id || "").trim();
  if (!osId) {
    entry.os_exists_in_ixc = true;
    entry.os_validation_message = "";
    return;
  }
  if (knownExists !== null) {
    entry.os_exists_in_ixc = Boolean(knownExists);
    entry.os_validation_message = entry.os_exists_in_ixc
      ? ""
      : "OS nao encontrada na sincronizacao atual do IXC.";
    return;
  }
  const match = getReferenceOrderById(osId);
  if (match) {
    entry.os_exists_in_ixc = true;
    entry.os_validation_message = "";
    return;
  }
  if (orderDetailsCache.has(osId)) {
    entry.os_exists_in_ixc = Boolean(orderDetailsCache.get(osId));
    entry.os_validation_message = entry.os_exists_in_ixc
      ? ""
      : "OS nao encontrada na sincronizacao atual do IXC.";
    return;
  }
  entry.os_exists_in_ixc = false;
  entry.os_validation_message = match
    ? ""
    : "OS nao encontrada na sincronizacao atual do IXC.";
}

async function loadSettings() {
  settingsFeedback.textContent = "Carregando configuracoes...";
  const response = await fetch(`/api/settings?_ts=${Date.now()}`, {
    cache: "no-store",
    headers: { "Cache-Control": "no-cache" },
  });
  if (!response.ok) {
    throw new Error(`Falha ao carregar configuracoes: ${response.status}`);
  }
  const payload = await response.json();
  fillSettingsForm(payload.values || {});
  applyAutoRefreshFromSettings(payload.values || {});
  settingsFeedback.textContent = "Configuracoes carregadas.";
}

function fillSettingsForm(values) {
  settingsFields.forEach((field) => {
    const input = document.getElementById(field);
    if (!input) {
      return;
    }
    if (checkboxFields.has(field)) {
      input.checked = toBoolean(values[field]);
    } else {
      input.value = values[field] ?? "";
    }
  });
}

function collectSettingsPayload() {
  const payload = {};
  settingsFields.forEach((field) => {
    const input = document.getElementById(field);
    if (!input) {
      return;
    }
    if (checkboxFields.has(field)) {
      payload[field] = input.checked;
      return;
    }
    const raw = input.value.trim();
    if (numberFields.has(field)) {
      payload[field] = raw === "" ? 0 : Number(raw);
    } else {
      payload[field] = raw;
    }
  });
  return payload;
}

async function saveSettings() {
  const response = await fetch("/api/settings", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(collectSettingsPayload()),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = data.detail;
    const message = typeof detail === "string"
      ? detail
      : Array.isArray(detail)
        ? detail.map((item) => {
          if (typeof item === "string") return item;
          if (item && typeof item === "object") {
            const location = Array.isArray(item.loc) ? item.loc.join(" → ") : "";
            const description = item.msg || item.message || "";
            return [location, description].filter(Boolean).join(": ");
          }
          return String(item);
        }).filter(Boolean).join("; ")
        : detail && typeof detail === "object"
          ? detail.message || detail.msg || ""
          : "";
    throw new Error(message || `Erro ao salvar configuracoes (HTTP ${response.status}).`);
  }
  fillSettingsForm(data.values || {});
  applyAutoRefreshFromSettings(data.values || {});
  startAutoRefresh();
  settingsFeedback.textContent = data.message || "Configuracoes salvas.";
  await Promise.all([loadFilterOptions(), loadMetrics(), loadProductivity(), loadProductivityOrders()]);
}

async function saveSubjectGroupsConfig(serializedGroups, errorMessage) {
  const response = await fetch("/api/settings", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      APP_SUBJECT_GROUPS: serializedGroups,
    }),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || errorMessage || "Erro ao salvar grupos.");
  }

  fillSettingsForm(data.values || {});
  applyAutoRefreshFromSettings(data.values || {});
  startAutoRefresh();
  await loadFilterOptions();
  return data;
}

async function createSubjectGroupFromDashboard() {
  const selectedSubjects = getSubjectFilterValues(subjectFilterRows);
  if (!selectedSubjects.length) {
    throw new Error("Selecione pelo menos um assunto no dashboard para criar o grupo.");
  }

  const groupName = window.prompt(
    "Nome do grupo que sera criado com os assuntos selecionados:",
    ""
  );
  const normalizedGroupName = String(groupName || "").trim();
  if (!normalizedGroupName) {
    return;
  }

  const groupsInput = document.getElementById("APP_SUBJECT_GROUPS");
  if (!(groupsInput instanceof HTMLInputElement)) {
    throw new Error("Campo APP_SUBJECT_GROUPS nao encontrado no formulario.");
  }

  const currentGroups = parseSubjectGroupsRaw(groupsInput.value);
  const nextGroups = currentGroups.filter(
    (group) => normalizeSubjectGroupKey(group.label) !== normalizeSubjectGroupKey(normalizedGroupName)
  );
  const serializedGroups = serializeSubjectGroupsRaw([
    ...nextGroups,
    {
      label: normalizedGroupName,
      patterns: selectedSubjects,
    },
  ]);
  await saveSubjectGroupsConfig(serializedGroups, "Erro ao salvar o novo grupo.");
  const createdGroupKey = normalizeSubjectGroupKey(normalizedGroupName);
  if (subjectGroupFilter instanceof HTMLSelectElement) {
    subjectGroupFilter.value = createdGroupKey;
  }
  if (prodSubjectGroupFilter instanceof HTMLSelectElement) {
    prodSubjectGroupFilter.value = createdGroupKey;
  }
  updateSubjectGroupActionButtons();

  await Promise.all([loadMetrics(), loadProductivity(), loadProductivityOrders()]);
  settingsFeedback.textContent = `Grupo "${normalizedGroupName}" criado com ${selectedSubjects.length} assunto(s).`;
}

async function deleteSelectedSubjectGroupFromDashboard() {
  const selectedGroupKey = String(subjectGroupFilter?.value || "").trim();
  if (!selectedGroupKey || selectedGroupKey === "__all__") {
    throw new Error("Selecione um grupo para excluir.");
  }

  const selectedGroup = subjectGroupOptionsState.find(
    (group) => String(group.key || "").trim() === selectedGroupKey
  );
  const selectedGroupLabel = normalizeText(
    selectedGroup?.label || selectedGroupKey || "Grupo selecionado"
  );
  const confirmed = window.confirm(`Excluir o grupo "${selectedGroupLabel}"?`);
  if (!confirmed) {
    return;
  }

  const groupsInput = document.getElementById("APP_SUBJECT_GROUPS");
  if (!(groupsInput instanceof HTMLInputElement)) {
    throw new Error("Campo APP_SUBJECT_GROUPS nao encontrado no formulario.");
  }

  const currentGroups = parseSubjectGroupsRaw(groupsInput.value);
  const nextGroups = currentGroups.filter(
    (group) => normalizeSubjectGroupKey(group.label) !== selectedGroupKey
  );
  const serializedGroups = serializeSubjectGroupsRaw(nextGroups);
  await saveSubjectGroupsConfig(serializedGroups, "Erro ao excluir o grupo.");

  if (subjectGroupFilter instanceof HTMLSelectElement) {
    subjectGroupFilter.value = "__all__";
  }
  if (prodSubjectGroupFilter instanceof HTMLSelectElement) {
    prodSubjectGroupFilter.value = "__all__";
  }
  updateSubjectGroupActionButtons();

  await Promise.all([loadMetrics(), loadProductivity(), loadProductivityOrders()]);
  settingsFeedback.textContent = `Grupo "${selectedGroupLabel}" excluido.`;
}

async function testConnection() {
  settingsFeedback.textContent = "Testando conexao com IXC...";
  const response = await fetch("/api/settings/test-connection", { method: "POST" });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Falha no teste de conexao.");
  }
  const keys = (data.sample_keys || []).slice(0, 8).join(", ");
  settingsFeedback.textContent = `Conexao OK. Tabela ${data.table}; amostra ${data.records_sampled}. Campos: ${keys || "sem amostra."}`;
}

async function applyDiscoverySuggestions() {
  settingsFeedback.textContent = "Executando descoberta de campos...";
  const [osRes, subRes, techRes] = await Promise.all([
    fetch("/api/discovery/os-fields"),
    fetch("/api/discovery/subject-fields"),
    fetch("/api/discovery/tech-fields"),
  ]);
  const osData = await osRes.json();
  const subData = await subRes.json();
  const techData = await techRes.json();
  if (!osRes.ok) {
    throw new Error(osData.detail || "Falha na descoberta da OS.");
  }
  if (!subRes.ok) {
    throw new Error(subData.detail || "Falha na descoberta de assunto.");
  }
  if (!techRes.ok) {
    throw new Error(techData.detail || "Falha na descoberta de tecnico.");
  }

  Object.entries(osData.env_suggestions || {}).forEach(([envName, value]) => {
    if (!value) {
      return;
    }
    const input = document.getElementById(envName);
    if (input && !checkboxFields.has(envName)) {
      input.value = value;
    }
  });
  if (subData.suggested_id_field) {
    document.getElementById("IXC_SUBJECT_ID_FIELD").value = subData.suggested_id_field;
  }
  if (subData.suggested_name_field) {
    document.getElementById("IXC_SUBJECT_NAME_FIELD").value = subData.suggested_name_field;
  }
  if (techData.suggested_id_field) {
    document.getElementById("IXC_TECH_ID_FIELD").value = techData.suggested_id_field;
  }
  if (techData.suggested_name_field) {
    document.getElementById("IXC_TECH_NAME_FIELD").value = techData.suggested_name_field;
  }
  settingsFeedback.textContent = "Descoberta aplicada no formulario. Clique em 'Salvar configuracoes'.";
}

function toBoolean(value) {
  if (typeof value === "boolean") {
    return value;
  }
  return String(value).toLowerCase() === "true";
}

function applyAutoRefreshFromSettings(values) {
  const metricsSeconds = Number(values.APP_DASHBOARD_REFRESH_SECONDS);
  const filtersSeconds = Number(values.APP_FILTER_OPTIONS_REFRESH_SECONDS);
  autoRefreshMetricsMs = Number.isFinite(metricsSeconds) && metricsSeconds >= 5
    ? metricsSeconds * 1000
    : 30000;
  autoRefreshFiltersMs = Number.isFinite(filtersSeconds) && filtersSeconds >= 15
    ? filtersSeconds * 1000
    : 180000;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function escapeHtmlAttr(value) {
  return escapeHtml(value).replace(/\n/g, "&#10;");
}

syncBtn.addEventListener("click", async () => {
  syncBtn.disabled = true;
  syncBtn.textContent = "Sincronizando...";
  try {
    const response = await fetch("/api/sync", { method: "POST" });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Erro na sincronizacao.");
    }
    await Promise.all([loadFilterOptions(), loadMetrics(), loadProductivity(), loadProductivityOrders()]);
  } catch (error) {
    alert(error.message || "Erro na sincronizacao.");
  } finally {
    syncBtn.disabled = false;
    syncBtn.textContent = "Sincronizar agora";
  }
});

syncFullBtn.addEventListener("click", async () => {
  syncFullBtn.disabled = true;
  syncFullBtn.textContent = "Processando...";
  try {
    const response = await fetch("/api/sync?full=true", { method: "POST" });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Erro na sincronizacao completa.");
    }
    await Promise.all([loadFilterOptions(), loadMetrics(), loadProductivity(), loadProductivityOrders()]);
    settingsFeedback.textContent = "Sincronizacao completa finalizada com sucesso.";
  } catch (error) {
    alert(error.message || "Erro na sincronizacao completa.");
  } finally {
    syncFullBtn.disabled = false;
    syncFullBtn.textContent = "Sync completa";
  }
});

dateInput.addEventListener("change", () => {
  loadMetrics().catch((error) => {
    alert(error.message || "Erro ao atualizar data de referencia.");
  });
});

applyFiltersBtn.addEventListener("click", () => {
  loadMetrics().catch((error) => {
    alert(error.message || "Erro ao aplicar filtros.");
  });
});

if (weeklyStartDateInput) {
  weeklyStartDateInput.addEventListener("change", applyWeeklyPeriodInputs);
}

if (weeklyEndDateInput) {
  weeklyEndDateInput.addEventListener("change", applyWeeklyPeriodInputs);
}

if (createSubjectGroupBtn) {
  createSubjectGroupBtn.addEventListener("click", async () => {
    createSubjectGroupBtn.disabled = true;
    try {
      await createSubjectGroupFromDashboard();
    } catch (error) {
      alert(error.message || "Erro ao criar grupo.");
    } finally {
      createSubjectGroupBtn.disabled = false;
    }
  });
}

if (deleteSubjectGroupBtn) {
  deleteSubjectGroupBtn.addEventListener("click", async () => {
    deleteSubjectGroupBtn.disabled = true;
    try {
      await deleteSelectedSubjectGroupFromDashboard();
    } catch (error) {
      alert(error.message || "Erro ao excluir grupo.");
    } finally {
      updateSubjectGroupActionButtons();
    }
  });
}

if (subjectGroupFilter) {
  subjectGroupFilter.addEventListener("change", () => {
    updateSubjectGroupActionButtons();
  });
}

clearFiltersBtn.addEventListener("click", () => {
  startDateInput.value = currentWeekStart;
  endDateInput.value = today;
  clearSubjectFilterRows(subjectFilterRows);
  if (subjectGroupFilter) {
    subjectGroupFilter.value = "__all__";
  }
  updateSubjectGroupActionButtons();
  branchFilter.value = "__all__";
  loadMetrics().catch((error) => {
    alert(error.message || "Erro ao limpar filtros.");
  });
});

metricCards.forEach((card) => {
  const metric = String(card.dataset.metric || "").trim();
  const label = String(card.dataset.label || card.querySelector(".label")?.textContent || "").trim();
  if (!metric) {
    return;
  }
  card.addEventListener("click", () => {
    openCardOrdersModal(metric, label);
  });
  card.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openCardOrdersModal(metric, label);
    }
  });
});

if (cardOrdersModalClose) {
  cardOrdersModalClose.addEventListener("click", () => {
    closeCardOrdersModal();
  });
}

if (cardOrdersModalOverlay) {
  cardOrdersModalOverlay.addEventListener("click", (event) => {
    if (event.target === cardOrdersModalOverlay) {
      closeCardOrdersModal();
    }
  });
}

if (boardDelayReportModalClose) {
  boardDelayReportModalClose.addEventListener("click", () => {
    closeBoardDelayReportModal();
  });
}

if (boardDelayReportPrintBtn) {
  boardDelayReportPrintBtn.addEventListener("click", () => {
    printBoardDelayReport();
  });
}

window.addEventListener("afterprint", () => {
  clearBoardDelayReportPrintMode();
});

if (boardDelayReportModalOverlay) {
  boardDelayReportModalOverlay.addEventListener("click", (event) => {
    if (event.target === boardDelayReportModalOverlay) {
      closeBoardDelayReportModal();
    }
  });
}

if (boardCommentModalClose) {
  boardCommentModalClose.addEventListener("click", () => {
    closeBoardCommentModal();
  });
}

if (boardCommentCancelBtn) {
  boardCommentCancelBtn.addEventListener("click", () => {
    closeBoardCommentModal();
  });
}

if (boardCommentSaveBtn) {
  boardCommentSaveBtn.addEventListener("click", () => {
    saveBoardCommentFromModal();
  });
}

if (boardCommentModalOverlay) {
  boardCommentModalOverlay.addEventListener("click", (event) => {
    if (event.target === boardCommentModalOverlay) {
      closeBoardCommentModal();
    }
  });
}

if (boardDelayReportTableWrap) {
  boardDelayReportTableWrap.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) {
      return;
    }
    if (!target.classList.contains("relato-toggle-btn")) {
      return;
    }
    const detailKey = target.dataset.detailKey;
    if (!detailKey) {
      return;
    }
    const detailRows = [...boardDelayReportTableWrap.querySelectorAll(".relato-detail-row")];
    const targetDetailRow = detailRows.find((row) => row.dataset.detailKey === detailKey);
    if (!(targetDetailRow instanceof HTMLTableRowElement)) {
      return;
    }
    const willOpen = targetDetailRow.hidden;
    boardDelayReportTableWrap.querySelectorAll(".relato-toggle-btn").forEach((button) => {
      if (button instanceof HTMLButtonElement) {
        button.textContent = "Ver comentario";
      }
    });
    detailRows.forEach((row) => {
      row.hidden = true;
    });
    if (willOpen) {
      targetDetailRow.hidden = false;
      target.textContent = "Ocultar";
    }
  });
}

if (cardOrdersModalTable) {
  cardOrdersModalTable.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) {
      return;
    }
    if (!target.classList.contains("relato-toggle-btn")) {
      return;
    }
    const detailKey = target.dataset.detailKey;
    if (!detailKey) {
      return;
    }
    const detailRows = [...cardOrdersModalTable.querySelectorAll(".relato-detail-row")];
    const targetDetailRow = detailRows.find((row) => row.dataset.detailKey === detailKey);
    if (!(targetDetailRow instanceof HTMLTableRowElement)) {
      return;
    }
    const willOpen = targetDetailRow.hidden;
    cardOrdersModalTable.querySelectorAll(".relato-toggle-btn").forEach((button) => {
      if (button instanceof HTMLButtonElement) {
        button.textContent = "Ver relato";
      }
    });
    detailRows.forEach((row) => {
      row.hidden = true;
    });
    if (willOpen) {
      targetDetailRow.hidden = false;
      target.textContent = "Ocultar";
    }
  });
}

if (productivityOrdersTable) {
  productivityOrdersTable.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) {
      return;
    }
    if (!target.classList.contains("relato-toggle-btn")) {
      return;
    }
    const detailKey = target.dataset.detailKey;
    if (!detailKey) {
      return;
    }
    const detailRows = [...productivityOrdersTable.querySelectorAll(".relato-detail-row")];
    const targetDetailRow = detailRows.find((row) => row.dataset.detailKey === detailKey);
    if (!(targetDetailRow instanceof HTMLTableRowElement)) {
      return;
    }
    const willOpen = targetDetailRow.hidden;
    productivityOrdersTable.querySelectorAll(".relato-toggle-btn").forEach((button) => {
      if (button instanceof HTMLButtonElement) {
        button.textContent = "Ver relato";
      }
    });
    detailRows.forEach((row) => {
      row.hidden = true;
    });
    if (willOpen) {
      targetDetailRow.hidden = false;
      target.textContent = "Ocultar";
    }
  });
}

prodApplyFiltersBtn.addEventListener("click", () => {
  Promise.all([loadProductivity(), loadProductivityOrders()]).catch((error) => {
    alert(error.message || "Erro ao aplicar filtros de produtividade.");
  });
});

prodClearFiltersBtn.addEventListener("click", () => {
  prodStartDateInput.value = currentWeekStart;
  prodEndDateInput.value = today;
  clearSubjectFilterRows(prodSubjectFilterRows);
  if (prodSubjectGroupFilter) {
    prodSubjectGroupFilter.value = "__all__";
  }
  prodBranchFilter.value = "__all__";
  prodTechnicianFilter.value = "__all__";
  prodStatusFilter.value = "__all__";
  Promise.all([loadProductivity(), loadProductivityOrders()]).catch((error) => {
    alert(error.message || "Erro ao limpar filtros de produtividade.");
  });
});

if (subjectAddBtn) {
  subjectAddBtn.addEventListener("click", () => {
    addSubjectFilterRow(subjectFilterRows);
  });
}

if (prodSubjectAddBtn) {
  prodSubjectAddBtn.addEventListener("click", () => {
    addSubjectFilterRow(prodSubjectFilterRows);
  });
}

if (installationsSubjectAddBtn) {
  installationsSubjectAddBtn.addEventListener("click", () => {
    addSubjectFilterRow(installationsSubjectFilterRows);
    updateInstallationsSubjectSummary();
  });
}

if (installationsToggleSubjectsBtn) {
  installationsToggleSubjectsBtn.addEventListener("click", () => {
    const isCollapsed = installationsSubjectField?.classList.contains("is-collapsed");
    setInstallationsSubjectCollapsed(!isCollapsed);
  });
}

if (subjectFilterRows) {
  subjectFilterRows.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) {
      return;
    }
    if (!target.classList.contains("subject-filter-remove")) {
      return;
    }
    removeSubjectFilterRow(subjectFilterRows, target);
  });
}

if (prodSubjectFilterRows) {
  prodSubjectFilterRows.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) {
      return;
    }
    if (!target.classList.contains("subject-filter-remove")) {
      return;
    }
    removeSubjectFilterRow(prodSubjectFilterRows, target);
  });
}

if (installationsSubjectFilterRows) {
  installationsSubjectFilterRows.addEventListener("change", () => {
    updateInstallationsSubjectSummary();
  });
  installationsSubjectFilterRows.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) {
      return;
    }
    if (!target.classList.contains("subject-filter-remove")) {
      return;
    }
    removeSubjectFilterRow(installationsSubjectFilterRows, target);
    updateInstallationsSubjectSummary();
  });
}

if (boardTechnicianAddBtn) {
  boardTechnicianAddBtn.addEventListener("click", () => {
    addBoardTechnicianRow();
    syncBoardTeamWithSelectedTechnicians();
    renderBoardEntries();
    boardFeedback.textContent = "Tecnico adicionado ao filtro. Clique em Carregar mapa.";
  });
}

if (boardStatusAddBtn) {
  boardStatusAddBtn.addEventListener("click", () => {
    addBoardStatusRow();
    refreshBoardStatusRowOptions();
    renderBoardEntries();
    boardFeedback.textContent = "Status adicionado ao filtro. Clique em Carregar mapa.";
  });
}

if (boardTechnicianRows) {
  boardTechnicianRows.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) {
      return;
    }
    if (!target.classList.contains("board-technician-remove")) {
      return;
    }
    removeBoardTechnicianRow(target);
    syncBoardTeamWithSelectedTechnicians();
    renderBoardEntries();
    boardFeedback.textContent = "Filtro de tecnicos atualizado. Clique em Carregar mapa.";
  });
  boardTechnicianRows.addEventListener("change", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLSelectElement)) {
      return;
    }
    if (!target.classList.contains("board-technician-select")) {
      return;
    }
    syncBoardTeamWithSelectedTechnicians();
    renderBoardEntries();
    boardFeedback.textContent = "Filtro de tecnicos atualizado. Clique em Carregar mapa.";
  });
}

if (boardStatusRows) {
  boardStatusRows.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) {
      return;
    }
    if (!target.classList.contains("board-status-remove")) {
      return;
    }
    removeBoardStatusRow(target);
    refreshBoardStatusRowOptions();
    renderBoardEntries();
    boardFeedback.textContent = "Filtro de status atualizado. Clique em Carregar mapa.";
  });
  boardStatusRows.addEventListener("change", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLSelectElement)) {
      return;
    }
    if (!target.classList.contains("board-status-select")) {
      return;
    }
    renderBoardEntries();
    boardFeedback.textContent = "Filtro de status atualizado. Clique em Carregar mapa.";
  });
}

prodTechnicianFilter.addEventListener("change", () => {
  Promise.all([loadProductivity(), loadProductivityOrders()]).catch((error) => {
    alert(error.message || "Erro ao atualizar tecnico da produtividade.");
  });
});

tabDashboardBtn.addEventListener("click", () => setActiveTab("dashboard"));
tabProductivityBtn.addEventListener("click", () => setActiveTab("productivity"));
tabInstallationsBtn.addEventListener("click", () => setActiveTab("installations"));
if (tabOperationsBtn) {
  tabOperationsBtn.addEventListener("click", () => setActiveTab("operations"));
}
tabSettingsBtn.addEventListener("click", () => setActiveTab("settings"));

if (new URLSearchParams(window.location.search).get("tab") === "settings") {
  setActiveTab("settings");
}

if (installationsApplyDateBtn) {
  installationsApplyDateBtn.addEventListener("click", () => {
    loadInstallations().catch((error) => {
      if (installationsScopeValue) {
        installationsScopeValue.textContent = error.message || "Erro ao carregar instalacoes.";
      }
    });
  });
}

installationsSubTabButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setInstallationsSubTab(button.dataset.installationsTab || "ranking");
  });
});

if (installationsPresetSelect) {
  installationsPresetSelect.addEventListener("change", () => {
    const selectedPreset = getSelectedInstallationPreset();
    if (selectedPreset && installationsPresetNameInput instanceof HTMLInputElement) {
      installationsPresetNameInput.value = normalizeText(selectedPreset.name || "");
    }
  });
}

if (installationsSavePresetBtn) {
  installationsSavePresetBtn.addEventListener("click", () => {
    saveInstallationPreset().catch((error) => {
      alert(error.message || "Erro ao salvar lista.");
    });
  });
}

if (installationsLoadPresetBtn) {
  installationsLoadPresetBtn.addEventListener("click", () => {
    const selectedPreset = getSelectedInstallationPreset();
    if (!selectedPreset) {
      alert("Selecione uma lista salva para carregar.");
      return;
    }
    applyInstallationPreset(selectedPreset);
    loadInstallations().catch((error) => {
      if (installationsScopeValue) {
        installationsScopeValue.textContent = error.message || "Erro ao carregar instalacoes.";
      }
    });
  });
}

if (installationsDeletePresetBtn) {
  installationsDeletePresetBtn.addEventListener("click", () => {
    deleteSelectedInstallationPreset().catch((error) => {
      alert(error.message || "Erro ao excluir lista.");
    });
  });
}

if (installationsToggleCollaboratorsBtn) {
  installationsToggleCollaboratorsBtn.addEventListener("click", () => {
    if (!(installationsCollaboratorPanel instanceof HTMLElement)) {
      return;
    }
    const willOpen = installationsCollaboratorPanel.hidden;
    installationsCollaboratorPanel.hidden = !willOpen;
    installationsToggleCollaboratorsBtn.textContent = willOpen
      ? "Ocultar lista de colaboradores"
      : "Mostrar lista de colaboradores";
  });
}

if (installationsCollaboratorSearch) {
  installationsCollaboratorSearch.addEventListener("input", () => {
    renderInstallationCollaboratorPicker();
  });
}

if (installationsCollaboratorList) {
  installationsCollaboratorList.addEventListener("change", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement) || target.type !== "checkbox") {
      return;
    }
    const value = String(target.value || "").trim();
    if (!value) {
      return;
    }
    if (target.checked) {
      installationsSelectedTechniciansState.add(value);
    } else {
      installationsSelectedTechniciansState.delete(value);
    }
    updateInstallationCollaboratorSummary();
  });
}

if (installationsSelectAllBtn) {
  installationsSelectAllBtn.addEventListener("click", () => {
    setInstallationCollaboratorSelection(true);
  });
}

if (installationsClearCollaboratorsBtn) {
  installationsClearCollaboratorsBtn.addEventListener("click", () => {
    installationsSelectedTechniciansState.clear();
    renderInstallationCollaboratorPicker();
  });
}

if (installationsStartDateInput) {
  installationsStartDateInput.addEventListener("change", () => {
    loadInstallations().catch((error) => {
      if (installationsScopeValue) {
        installationsScopeValue.textContent = error.message || "Erro ao carregar instalacoes.";
      }
    });
  });
}

if (installationsEndDateInput) {
  installationsEndDateInput.addEventListener("change", () => {
    loadInstallations().catch((error) => {
      if (installationsScopeValue) {
        installationsScopeValue.textContent = error.message || "Erro ao carregar instalacoes.";
      }
    });
  });
}

if (installationsSubjectGroupFilter) {
  installationsSubjectGroupFilter.addEventListener("change", () => {
    updateInstallationsSubjectSummary();
    loadInstallations().catch((error) => {
      if (installationsScopeValue) {
        installationsScopeValue.textContent = error.message || "Erro ao carregar instalacoes.";
      }
    });
  });
}

if (boardLoadBtn) {
  boardLoadBtn.addEventListener("click", () => {
  boardSelectedSavedListId = "";
  boardSelectedTeamKey = "";
  if (boardSavedListSelect instanceof HTMLSelectElement) {
    boardSavedListSelect.value = "";
  }
  const selectedTechnicians = getBoardTechnicianValues();
  if (selectedTechnicians.length) {
    boardTeamInput.value = selectedTechnicians.join(" + ");
  }
  renderBoardSavedLists();
  loadBoard().catch((error) => {
    boardFeedback.textContent = error.message || "Erro ao carregar mapa diario.";
  });
  });
}

if (boardAddRowBtn) {
  boardAddRowBtn.addEventListener("click", () => {
  boardEntriesState.push(
    createEmptyBoardRow(
      boardReferencesState.time_slots?.[0] || "08:00 - 09:00",
      getBoardBranchFilterValue(),
      boardTeamInput.value || ""
    )
  );
  boardDirty = true;
  boardFeedback.textContent = "Linha adicionada. Existem alteracoes nao salvas.";
  renderBoardDataLists();
  renderBoardEntries();
  });
}

if (boardSaveBtn) {
  boardSaveBtn.addEventListener("click", async () => {
  boardSaveBtn.disabled = true;
  try {
    await saveBoard();
  } catch (error) {
    boardFeedback.textContent = error.message || "Erro ao salvar mapa diario.";
  } finally {
    boardSaveBtn.disabled = false;
  }
  });
}

if (boardSavedListSelect) {
  boardSavedListSelect.addEventListener("focus", () => {
    loadBoardSavedLists({ silent: true }).catch((error) => {
      console.error("Falha ao atualizar listas salvas no foco do seletor:", error);
    });
  });
  boardSavedListSelect.addEventListener("pointerdown", () => {
    loadBoardSavedLists({ silent: true }).catch((error) => {
      console.error("Falha ao atualizar listas salvas no clique do seletor:", error);
    });
  });
  boardSavedListSelect.addEventListener("change", () => {
    const selectedListId = normalizeText(boardSavedListSelect.value || "").trim();
    if (!selectedListId) {
      boardSelectedSavedListId = "";
      renderBoardSavedLists();
      boardFeedback.textContent = "Selecione um mapa salvo e clique em Carregar.";
      return;
    }
    const selectedList = findBoardSavedListById(selectedListId);
    if (!selectedList) {
      boardFeedback.textContent = "Lista selecionada nao encontrada.";
      boardSelectedSavedListId = "";
      renderBoardSavedLists();
      return;
    }
    boardSelectedSavedListId = selectedList.list_id;
    renderBoardSavedLists();
    boardFeedback.textContent = "Mapa salvo selecionado. Clique em Carregar.";
  });
}

if (boardDelayReportSavedListSelect) {
  boardDelayReportSavedListSelect.addEventListener("focus", () => {
    loadBoardSavedLists({ silent: true, allDates: true }).catch((error) => {
      console.error("Falha ao atualizar mapas salvos no foco do seletor de impressao:", error);
    });
  });
  boardDelayReportSavedListSelect.addEventListener("pointerdown", () => {
    loadBoardSavedLists({ silent: true, allDates: true }).catch((error) => {
      console.error("Falha ao atualizar mapas salvos no clique do seletor de impressao:", error);
    });
  });
  boardDelayReportSavedListSelect.addEventListener("change", () => {
    const selectedListId = normalizeText(boardDelayReportSavedListSelect.value || "").trim();
    loadSavedMapForDelayReport(selectedListId).catch((error) => {
      boardFeedback.textContent = error.message || "Erro ao carregar mapa salvo para impressao.";
    });
  });
}

if (boardLoadSavedBtn) {
  boardLoadSavedBtn.addEventListener("click", () => {
    loadBoardFromSavedSelection().catch((error) => {
      boardFeedback.textContent = error.message || "Erro ao carregar mapa salvo.";
    });
  });
}

if (boardDeleteListBtn) {
  boardDeleteListBtn.addEventListener("click", async () => {
    const selectedList = findBoardSavedListById(boardSelectedSavedListId);
    if (!selectedList) {
      boardFeedback.textContent = "Selecione uma lista salva para excluir.";
      renderBoardSavedLists();
      return;
    }
    if (boardDirty) {
      boardFeedback.textContent = "Existem alteracoes nao salvas no mapa diario.";
      return;
    }
    const listLabel = normalizeBoardTeamName(selectedList.team_name || "") || "Sem equipe";
    const listDate = selectedList.entry_date || boardDateInput.value || today;
    const confirmed = window.confirm(
      `Excluir a lista salva "${listLabel}" da data ${listDate}?`
    );
    if (!confirmed) {
      return;
    }

    boardDeleteListBtn.disabled = true;
    try {
      const data = await deleteBoardList(selectedList.team_key, listDate);
      const savedLists = Array.isArray(data.saved_lists) ? data.saved_lists : [];
      const nextList = savedLists.length > 0 ? savedLists[0] : null;
      boardSelectedSavedListId = nextList
        ? buildBoardSavedListId(nextList.entry_date, nextList.team_key)
        : "";
      boardSelectedTeamKey = nextList
        ? normalizeText(nextList.team_key || "").trim().toLowerCase()
        : "";
      boardDateInput.value = nextList ? normalizeText(nextList.entry_date || "").trim() : boardDateInput.value;
      boardTeamInput.value = nextList ? normalizeBoardTeamName(nextList.team_name || "") : "";
      setBoardSavedListsState(savedLists, {
        preferredListId: boardSelectedSavedListId,
        preferredTeamKey: boardSelectedTeamKey,
        preferredTeamName: boardTeamInput.value || "",
        preferredEntryDate: boardDateInput.value || today,
      });
      await loadBoard();
      boardFeedback.textContent = `Lista "${listLabel}" excluida com sucesso.`;
    } catch (error) {
      boardFeedback.textContent = error.message || "Erro ao excluir lista salva.";
      renderBoardSavedLists();
    } finally {
      if (boardDeleteListBtn) {
        boardDeleteListBtn.disabled = !Boolean(findBoardSavedListById(boardSelectedSavedListId));
      }
    }
  });
}

if (boardDelayReportBtn) {
  boardDelayReportBtn.addEventListener("click", () => {
    openBoardDelayReportModal();
  });
}

[boardDateInput, boardResponsibleInput, boardShiftInput, boardTeamInput, boardGeneralNotesInput]
  .filter((element) => element instanceof HTMLElement)
  .forEach((element) => {
  element.addEventListener("input", () => {
    if (element === boardDateInput) {
      return;
    }
    if (element === boardTeamInput) {
      const teamValue = boardTeamInput.value.trim();
      const matchedList = findBoardSavedListByTeamName(teamValue, {
        entryDate: boardDateInput.value || "",
      });
      boardSelectedSavedListId = matchedList ? matchedList.list_id : "";
      boardSelectedTeamKey = matchedList ? matchedList.team_key : "";
      renderBoardSavedLists();
      boardEntriesState.forEach((entry) => {
        if (!String(entry.team_label || "").trim()) {
          entry.team_label = teamValue;
        }
      });
      renderBoardEntries();
    }
    boardDirty = true;
    boardFeedback.textContent = "Existem alteracoes nao salvas no mapa diario.";
  });
});

if (boardDateInput) {
  boardDateInput.addEventListener("change", () => {
  boardDirty = false;
  boardSelectedSavedListId = "";
  boardSelectedTeamKey = "";
  loadBoard().catch((error) => {
    boardFeedback.textContent = error.message || "Erro ao carregar mapa diario.";
  });
  });
}

if (boardBranchFilter) {
  boardBranchFilter.addEventListener("change", () => {
  renderBoardEntries();
  });
}

if (boardSubjectFilter) {
  boardSubjectFilter.addEventListener("change", () => {
  renderBoardEntries();
  });
}

if (operationsBoardTable) {
  operationsBoardTable.addEventListener("input", (event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement)) {
    return;
  }
  const field = target.dataset.field;
  const row = target.closest("tr");
  if (!field || !row || row.dataset.rowIndex === undefined) {
    return;
  }
  const rowIndex = Number(row.dataset.rowIndex);
  if (!Number.isInteger(rowIndex) || !boardEntriesState[rowIndex]) {
    return;
  }
  boardEntriesState[rowIndex][field] = target.value;
  if (field === "team_label") {
    if (!String(boardEntriesState[rowIndex].technician_names || "").trim()) {
      boardEntriesState[rowIndex].technician_names = target.value;
    }
  }
  boardDirty = true;
  boardFeedback.textContent = "Existem alteracoes nao salvas no mapa diario.";
  });

  operationsBoardTable.addEventListener("change", async (event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement)) {
    return;
  }
  const field = target.dataset.field;
  const row = target.closest("tr");
  if (!field || !row || row.dataset.rowIndex === undefined) {
    return;
  }
  const rowIndex = Number(row.dataset.rowIndex);
  if (!Number.isInteger(rowIndex) || !boardEntriesState[rowIndex]) {
    return;
  }
  if (field === "os_id") {
    boardEntriesState[rowIndex][field] = target.value;
    let osLookupFailed = false;
    try {
      await applyOrderReferenceToRow(rowIndex);
    } catch (error) {
      console.error(error);
      boardFeedback.textContent = error.message || "Falha ao consultar detalhes da OS.";
      osLookupFailed = true;
    }
    boardDirty = true;
    if (!osLookupFailed) {
      boardFeedback.textContent = "OS aplicada na linha. Salve o mapa para persistir.";
    }
    renderBoardDataLists();
    renderBoardEntries();
    return;
  }
  if (field === "branch_name") {
    boardEntriesState[rowIndex][field] = target.value;
    boardDirty = true;
    boardFeedback.textContent = "Filial da linha atualizada. Existem alteracoes nao salvas.";
    renderBoardDataLists();
    renderBoardEntries();
    return;
  }
  if (field === "subject_name") {
    boardEntriesState[rowIndex][field] = target.value;
    boardDirty = true;
    boardFeedback.textContent = "Assunto da linha atualizado. Existem alteracoes nao salvas.";
    renderBoardDataLists();
    renderBoardEntries();
  }
  });

  operationsBoardTable.addEventListener("click", (event) => {
  const target = event.target;
  if (!(target instanceof HTMLButtonElement)) {
    return;
  }
  const row = target.closest("tr");
  if (!row || row.dataset.rowIndex === undefined) {
    return;
  }
  const rowIndex = Number(row.dataset.rowIndex);
  if (!Number.isInteger(rowIndex)) {
    return;
  }
  if (target.dataset.action === "comment-row") {
    openBoardCommentModal(rowIndex);
    return;
  }
  if (target.dataset.action === "insert-row-below") {
    const currentEntry = boardEntriesState[rowIndex] || {};
    const inheritedPrimaryTime = normalizeText(
      currentEntry.displacement_at ||
        currentEntry.executed_at ||
        currentEntry.finalized_at ||
        currentEntry.start_at ||
        ""
    );
    const newEntry = createEmptyBoardRow(
      currentEntry.slot_label || boardReferencesState.time_slots?.[0] || "08:00 - 09:00",
      currentEntry.branch_name || getBoardBranchFilterValue(),
      currentEntry.team_label || boardTeamInput.value || ""
    );
    newEntry.technician_names = normalizeText(
      currentEntry.technician_names || currentEntry.team_label || ""
    );
    if (inheritedPrimaryTime) {
      newEntry.start_at = inheritedPrimaryTime;
    }
    boardEntriesState.splice(rowIndex + 1, 0, newEntry);
    boardDirty = true;
    boardFeedback.textContent = "Linha adicionada abaixo da atual. Existem alteracoes nao salvas.";
    renderBoardDataLists();
    renderBoardEntries();
    return;
  }
  if (target.dataset.action !== "remove-row") {
    return;
  }
  boardEntriesState.splice(rowIndex, 1);
  if (!boardEntriesState.length) {
    boardEntriesState.push(
      createEmptyBoardRow(
        boardReferencesState.time_slots?.[0] || "08:00 - 09:00",
        getBoardBranchFilterValue(),
        boardTeamInput.value || ""
      )
    );
  }
  boardDirty = true;
  boardFeedback.textContent = "Linha removida. Existem alteracoes nao salvas.";
  renderBoardDataLists();
  renderBoardEntries();
  });
}

saveSettingsBtn.addEventListener("click", async () => {
  saveSettingsBtn.disabled = true;
  try {
    await saveSettings();
  } catch (error) {
    settingsFeedback.textContent = error.message || "Erro ao salvar configuracoes.";
  } finally {
    saveSettingsBtn.disabled = false;
  }
});

testConnectionBtn.addEventListener("click", async () => {
  testConnectionBtn.disabled = true;
  try {
    await testConnection();
  } catch (error) {
    settingsFeedback.textContent = error.message || "Erro no teste de conexao.";
  } finally {
    testConnectionBtn.disabled = false;
  }
});

autoDiscoveryBtn.addEventListener("click", async () => {
  autoDiscoveryBtn.disabled = true;
  try {
    await applyDiscoverySuggestions();
  } catch (error) {
    settingsFeedback.textContent = error.message || "Erro na descoberta.";
  } finally {
    autoDiscoveryBtn.disabled = false;
  }
});

document.addEventListener("visibilitychange", () => {
  if (!document.hidden) {
    refreshMetricsSilently();
    refreshProductivitySilently();
    loadFilterOptions().catch((error) => {
      console.error("Falha ao atualizar filtros ao voltar para a aba:", error);
    });
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && cardOrdersModalOpen) {
    closeCardOrdersModal();
    return;
  }
  if (event.key === "Escape" && boardDelayReportModalOpen) {
    closeBoardDelayReportModal();
    return;
  }
  if (event.key === "Escape" && boardCommentModalOpen) {
    closeBoardCommentModal();
  }
});

window.addEventListener("beforeunload", () => {
  stopAutoRefresh();
});

async function runInitialLoad() {
  const tasks = [
    {
      run: () => loadSettings(),
      onError: (error) => {
        settingsFeedback.textContent = error.message || "Erro ao carregar configuracoes.";
      },
    },
    {
      run: () => loadFilterOptions(),
      onError: (error) => {
        console.error("Erro ao carregar filtros:", error);
      },
    },
    {
      run: () => loadInstallationPresets(),
      onError: (error) => {
        console.error("Erro ao carregar listas salvas:", error);
      },
    },
    {
      run: () => loadMetrics(),
      onError: (error) => {
        meta.textContent = error.message || "Erro ao carregar dashboard.";
      },
    },
    {
      run: () => loadProductivity(),
      onError: (error) => {
        productivityMeta.textContent = error.message || "Erro ao carregar produtividade.";
      },
    },
    {
      run: () => loadProductivityOrders(),
      onError: (error) => {
        productivityOrdersMeta.textContent = error.message || "Erro ao carregar OS detalhadas.";
      },
    },
    {
      run: () => loadInstallations(),
      onError: (error) => {
        if (installationsScopeValue) {
          installationsScopeValue.textContent = error.message || "Erro ao carregar instalacoes.";
        }
      },
    },
  ];

  const results = await Promise.allSettled(tasks.map((task) => task.run()));
  results.forEach((result, index) => {
    if (result.status === "rejected") {
      const reason = result.reason instanceof Error ? result.reason : new Error(String(result.reason || "Erro desconhecido."));
      tasks[index].onError(reason);
    }
  });
}

runInitialLoad().finally(() => {
  startAutoRefresh();
});
