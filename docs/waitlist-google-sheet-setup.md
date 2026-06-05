# Waitlist → Google Sheet (Apps Script) setup

> ⚠️ **LEGACY / optional.** Capture now runs through the FastAPI backend on the Hugging Face Space
> (`POST /api/waitlist` + `/api/request`, see [DECISIONS.md](DECISIONS.md) D13). Keep this only as a
> no-backend fallback.


The static landing page (`site/index.html` + `site/en.html`) sends each signup to a Google Sheet
you own, via a tiny Apps Script web app. No backend, no third-party service — just your Google account.

> The web-app URL you'll get (ends in `/exec`) is **public, not a secret** — it's the endpoint the
> page posts to. Safe to share. (There is no API key involved.)

## Steps (~5 min)

1. **Create the Sheet.** Go to [sheets.new](https://sheets.new), name it e.g. `Volante — Waitlist`.
2. **Open Apps Script.** In the Sheet: **Extensions → Apps Script**.
3. **Paste the code below** (replace anything already there in `Code.gs`), then **Save** (💾).
4. **Deploy.** Click **Deploy → New deployment** → gear ⚙️ → **Web app**. Set:
   - **Description:** `volante waitlist`
   - **Execute as:** **Me**
   - **Who has access:** **Anyone**
   - Click **Deploy**, authorize when asked (it's your own script).
5. **Copy the Web app URL** (ends in `/exec`).
6. **Send Daniel-Claude that `/exec` URL** → it gets dropped into the form and pushed (~30s redeploy).

That's it. New signups append as rows: `Timestamp · Contact · Zone · Lang · Source`.
A header row is created automatically on first run.

## Apps Script code (`Code.gs`)

```javascript
function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(10000);
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('signups') || ss.getActiveSheet();
    var p = (e && e.parameter) || {};

    // Honeypot: silently drop bots that fill the hidden _gotcha field.
    if (p._gotcha) {
      return ContentService.createTextOutput(JSON.stringify({ result: 'ok' }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Timestamp', 'Source', 'Status', 'Contact', 'Lang', 'Zone',
                       'Pickup', 'Dropoff', 'Passengers', 'Estimate', 'When']);
    }
    sheet.appendRow([new Date(), p.source || 'landing', 'new', p.contact || '', p.lang || '',
                     p.zone || '', p.pickup || '', p.dropoff || '', p.passengers || '',
                     p.estimate || '', p.when || '']);

    return ContentService.createTextOutput(JSON.stringify({ result: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ result: 'error', error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}
```

## Notes
- The page posts `application/x-www-form-urlencoded` with `fetch(..., { mode: 'no-cors' })`, so it
  doesn't trip CORS and shows success optimistically (good enough for a waitlist).
- If you ever change the code, **Deploy → Manage deployments → edit → Version: New version** to push it
  (the `/exec` URL stays the same).
- Light spam protection: a hidden honeypot field. If spam gets bad later, we can add a shared token or
  a captcha — or migrate to Supabase (the M3 database) and reuse this same data via CSV import.
- **One Sheet, two forms = your dispatch board.** `Source` `landing-*` rows are waitlist signups;
  `request-*` rows are pilot-ride requests (with Pickup / Dropoff / Estimate / When). The **`Status`
  column is the board**: filter to `request-*` + `Status = new`, work each ride (`new → assigned →
  done`), and message the customer on WhatsApp using their `Contact`. No admin app needed until you're
  past ~5 rides/weekend (then the FastAPI app in `src/volante/` becomes the M3 backend).
