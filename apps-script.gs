/**
 * Backend ucapan & konfirmasi kehadiran (Google Sheets).
 *
 * Cara pasang (sekali saja):
 * 1. Buat Google Sheet baru, mis. "Ucapan Undangan Pernikahan".
 * 2. Di Sheet itu: Extensions > Apps Script. Hapus isi Code.gs, tempel seluruh file ini, lalu Save.
 * 3. Deploy > New deployment > pilih type "Web app".
 *      Execute as: Me
 *      Who has access: Anyone
 *    Klik Deploy, izinkan akses (Authorize access), lalu salin "Web app URL" (berakhiran /exec).
 * 4. Tempel URL itu ke CONFIG.rsvpEndpoint di index.html.
 *
 * Menghapus ucapan: hapus barisnya langsung di tab "Ucapan" pada Google Sheet.
 * Jika file ini diubah, deploy ulang lewat Deploy > Manage deployments > Edit > Version: New version
 * (URL tetap sama).
 */
const SHEET_NAME = 'Ucapan';
const HEADER = ['ts', 'name', 'att', 'msg'];

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(HEADER);
    sh.setFrozenRows(1);
  }
  return sh;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// Daftar ucapan, terbaru di atas.
function doGet() {
  const sh = sheet_();
  const last = sh.getLastRow();
  if (last < 2) return json_([]);
  const rows = sh.getRange(2, 1, last - 1, 4).getValues();
  const data = rows
    .filter(r => r[1] && r[3])
    .map(r => ({ ts: Number(r[0]) || 0, name: String(r[1]), att: String(r[2]) === 'n' ? 'n' : 'y', msg: String(r[3]) }))
    .sort((a, b) => b.ts - a.ts);
  return json_(data);
}

// Simpan satu ucapan baru.
function doPost(e) {
  let d;
  try { d = JSON.parse(e.postData.contents); } catch (err) { return json_({ ok: false, error: 'invalid json' }); }
  const clean = (s, n) => String(s || '').trim().slice(0, n).replace(/^[=+\-@]/, "'$&");
  const name = clean(d.name, 60), msg = clean(d.msg, 500), att = d.att === 'n' ? 'n' : (d.att === 'y' ? 'y' : '');
  if (!name || !msg || !att) return json_({ ok: false, error: 'missing fields' });

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sh = sheet_();
    const last = sh.getLastRow();
    if (last >= 2) {
      const from = Math.max(2, last - 19);
      const recent = sh.getRange(from, 1, last - from + 1, 4).getValues();
      const now = Date.now();
      if (recent.some(r => String(r[1]) === name && String(r[3]) === msg && now - Number(r[0]) < 120000)) {
        return json_({ ok: true, duplicate: true });
      }
    }
    sh.appendRow([Date.now(), name, att, msg]);
  } finally {
    lock.releaseLock();
  }
  return json_({ ok: true });
}
