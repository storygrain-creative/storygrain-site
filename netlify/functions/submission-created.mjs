// Branded form notification emails for storygrain.co.
//
// Netlify runs this automatically after every verified (non-spam) form
// submission. It sends one on-brand email per submission to hello@ through
// Resend. Netlify still stores every entry under Forms, so the dashboard is
// the record of truth and this email is the alert.
//
// Setup (once): add RESEND_API_KEY in Netlify > Project configuration >
// Environment variables. Until that key exists this function does nothing,
// and Netlify's built-in notification keeps working.

const TO = 'hello@storygrain.co';
const FROM = 'Storygrain Forms <forms@storygrain.co>';
const SITE = 'https://storygrain.co';
const DASH = 'https://app.netlify.com/projects/storygrain/forms';

const C = {
  forest: '#2D3A33', deep: '#243029', sage: '#A9B59B', cream: '#F1EDE6',
  ink: '#1C1F1D', muted: '#5B625C', line: '#D9D3C7', card: '#F8F5EF',
};
const SANS = "'Schibsted Grotesk','Helvetica Neue',Helvetica,Arial,sans-serif";
const MONO = "'IBM Plex Mono',Menlo,Consolas,'Courier New',monospace";

// Fields that are plumbing, not content.
const SKIP = new Set(['form-name', 'bot-field', 'company-url', 'website-url', 'subject', 'results', 'ip', 'user_agent', 'referrer']);

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const nl = (s) => esc(s).replace(/\r?\n/g, '<br>');
const pretty = (k) => k.replace(/[_-]+/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
const fileUrl = (v) => (v && typeof v === 'object' ? v.url : typeof v === 'string' && /^https?:\/\//.test(v) ? v : null);

// Per-form wording. Anything not listed falls back to a generic layout.
const FORMS = {
  contact: {
    label: 'New inquiry',
    subject: (d) => `New inquiry: ${d.name || 'someone'}${d.business ? `, ${d.business}` : ''}`,
    headline: (d) => `${d.name || 'Someone'} wants to talk.`,
    order: ['name', 'email', 'business'],
    long: ['message'],
  },
  'content-check': {
    label: 'Content Check',
    subject: (d) => `Content Check: ${d.business || d.name || 'new result'}${fitOf(d) ? ` (${fitOf(d)})` : ''}`,
    headline: (d) => `${d.business || d.name || 'A business'} took the Content Check.`,
    order: ['name', 'email', 'business', 'source'],
    long: [],
  },
  testimonial: {
    label: 'Testimonial',
    subject: (d) => `Testimonial from ${d.client || d.name || 'a client'}`,
    headline: (d) => `${d.name || 'A client'} left a testimonial.`,
    order: ['client', 'name'],
    long: ['testimonial'],
    after: (d) => row('OK to share', /^(yes|on|true)$/i.test(d.ok_to_share || '') ? 'Yes, with their name' : 'No, keep it private'),
  },
  release: {
    label: 'Signed release',
    subject: (d) => d.subject || `Signed release: ${d.name || 'talent'}${d.production ? ` (${d.production})` : ''}`,
    headline: (d) => `${d.name || 'Talent'} signed a release.`,
    order: ['production', 'name', 'email', 'phone', 'signing_for', 'signed_at', 'release_version'],
    long: [],
  },
};

function fitOf(d) {
  const m = String(d.results || '').match(/^Fit:\s*(.+)$/m);
  return m ? m[1].replace(/\.$/, '') : '';
}

function row(label, valueHtml) {
  return `<tr><td style="padding:14px 0;border-top:1px solid ${C.line};vertical-align:top;width:34%;font:500 11px/1.5 ${MONO};letter-spacing:.08em;text-transform:uppercase;color:${C.muted}">${esc(label)}</td>
<td style="padding:14px 0 14px 16px;border-top:1px solid ${C.line};vertical-align:top;font:400 16px/1.5 ${SANS};color:${C.ink}">${valueHtml}</td></tr>`;
}

function block(label, text, quote) {
  return `<tr><td colspan="2" style="padding:18px 0 4px;border-top:1px solid ${C.line};font:500 11px/1.5 ${MONO};letter-spacing:.08em;text-transform:uppercase;color:${C.muted}">${esc(label)}</td></tr>
<tr><td colspan="2" style="padding:0 0 18px"><div style="${quote ? `border-left:3px solid ${C.sage};padding:4px 0 4px 16px;font:400 19px/1.55 ${SANS};` : `font:400 16px/1.6 ${SANS};`}color:${C.ink}">${nl(text)}</div></td></tr>`;
}

function value(k, v) {
  const url = fileUrl(v);
  if (url) return `<a href="${esc(url)}" style="color:${C.forest};font-weight:600">View ${k === 'signed_release' ? 'signed release' : 'file'}</a>`;
  if (k === 'email' && v) return `<a href="mailto:${esc(v)}" style="color:${C.forest}">${esc(v)}</a>`;
  if (k === 'phone' && v) return `<a href="tel:${esc(String(v).replace(/[^\d+]/g, ''))}" style="color:${C.forest}">${esc(v)}</a>`;
  return nl(v);
}

// Content Check results arrive as "Question? Answer" lines plus Fit and Needs.
function resultsRows(results) {
  const lines = String(results || '').split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  let fit = '', needs = '', qa = [];
  for (const l of lines) {
    if (/^Fit:/.test(l)) fit = l.replace(/^Fit:\s*/, '');
    else if (/^Needs:/.test(l)) needs = l.replace(/^Needs:\s*/, '');
    else {
      const i = l.indexOf('? '), w = l.indexOf(' Website: ');
      if (i > 0) qa.push([l.slice(0, i + 1), l.slice(i + 2)]);
      else if (w > 0) qa.push([l.slice(0, w), l.slice(w + 1).replace(/;\s*/g, ' \u00b7 ')]);
      else qa.push(['', l]);
    }
  }
  let html = '';
  if (fit || needs) {
    html += `<tr><td colspan="2" style="padding:6px 0 22px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.forest};border-radius:8px"><tr><td style="padding:20px 22px">
${fit ? `<div style="font:500 11px/1.5 ${MONO};letter-spacing:.08em;text-transform:uppercase;color:${C.sage}">Fit</div><div style="font:800 22px/1.3 ${SANS};color:${C.cream};margin:2px 0 ${needs ? '14px' : '0'}">${esc(fit)}</div>` : ''}
${needs ? `<div style="font:500 11px/1.5 ${MONO};letter-spacing:.08em;text-transform:uppercase;color:${C.sage}">Recommended</div><div style="font:400 16px/1.55 ${SANS};color:${C.cream};margin-top:2px">${needs.split(/;\s*/).map(esc).join('<br>')}</div>` : ''}
</td></tr></table></td></tr>`;
  }
  if (qa.length) {
    html += `<tr><td colspan="2" style="padding:8px 0 6px;font:500 11px/1.5 ${MONO};letter-spacing:.08em;text-transform:uppercase;color:${C.muted}">Their answers</td></tr>`;
    for (const [q, a] of qa) {
      html += `<tr><td colspan="2" style="padding:12px 0;border-top:1px solid ${C.line}"><div style="font:400 14px/1.45 ${SANS};color:${C.muted}">${esc(q)}</div><div style="font:600 16px/1.45 ${SANS};color:${C.ink};margin-top:2px">${esc(a)}</div></td></tr>`;
    }
  }
  return html;
}

export function render(payload) {
  const name = payload.form_name || payload.data?.['form-name'] || 'form';
  const d = payload.data || {};
  const f = FORMS[name] || {
    label: pretty(name), subject: () => `New ${pretty(name)} submission`, headline: () => `New ${pretty(name)} submission.`, order: [], long: [],
  };

  const used = new Set();
  let rows = '';
  for (const k of f.order) { if (d[k] != null && d[k] !== '') { rows += row(pretty(k), value(k, d[k])); } used.add(k); }
  for (const k of f.long) { if (d[k]) rows += block(pretty(k), d[k], name === 'testimonial'); used.add(k); }
  if (f.after) { rows += f.after(d); used.add('ok_to_share'); }
  for (const [k, v] of Object.entries(d)) {
    if (used.has(k) || SKIP.has(k) || v == null || v === '') continue;
    rows += row(pretty(k), value(k, v));
  }
  if (name === 'content-check') rows += resultsRows(d.results);

  const when = new Date(payload.created_at || Date.now()).toLocaleString('en-US', { timeZone: 'America/Chicago', dateStyle: 'medium', timeStyle: 'short' });
  const replyName = (d.name || '').split(' ')[0];
  const cta = d.email
    ? `<tr><td style="padding:8px 32px 32px"><a href="mailto:${esc(d.email)}" style="display:inline-block;background:${C.sage};color:${C.ink};font:600 15px/1 ${SANS};text-decoration:none;padding:14px 22px;border-radius:999px">Reply to ${esc(replyName || d.email)}</a></td></tr>`
    : '';
  const subject = f.subject(d);

  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>${esc(subject)}</title></head>
<body style="margin:0;padding:0;background:${C.cream}">
<div style="display:none;max-height:0;overflow:hidden">${esc(f.headline(d))}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.cream}"><tr><td align="center" style="padding:28px 14px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:${C.card};border:1px solid ${C.line};border-radius:10px;overflow:hidden">
<tr><td bgcolor="${C.forest}" style="background:${C.forest};padding:22px 32px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td><a href="${SITE}"><img src="${SITE}/email/storygrain-logo.png" width="199" height="44" alt="StoryGrain" style="display:block;border:0;width:199px;height:44px"></a></td>
<td align="right" style="font:500 11px/1.5 ${MONO};letter-spacing:.1em;text-transform:uppercase;color:${C.sage};white-space:nowrap">&#9679;&nbsp;${esc(f.label)}</td>
</tr></table></td></tr>
<tr><td style="padding:32px 32px 8px">
<h1 style="margin:0;font:800 26px/1.2 ${SANS};letter-spacing:-.01em;color:${C.forest}">${esc(f.headline(d))}</h1>
<div style="margin-top:8px;font:400 12px/1.5 ${MONO};letter-spacing:.04em;color:${C.muted}">${esc(when)} &middot; storygrain.co</div>
</td></tr>
<tr><td style="padding:16px 32px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rows}</table></td></tr>
${cta}
</table>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px"><tr><td style="padding:18px 32px;font:400 12px/1.6 ${MONO};color:${C.muted};text-align:center">
Every entry is also saved in <a href="${DASH}" style="color:${C.forest}">Netlify Forms</a>.
</td></tr></table>
</td></tr></table></body></html>`;

  const text = [f.headline(d), when, '', ...Object.entries(d).filter(([k, v]) => !SKIP.has(k) && v !== '' && v != null).map(([k, v]) => `${pretty(k)}: ${fileUrl(v) || v}`), d.results ? `\n${d.results}` : '', '', `All entries: ${DASH}`].join('\n');

  return { subject, html, text, replyTo: d.email || undefined };
}

export const handler = async (event) => {
  const key = process.env.RESEND_API_KEY;
  if (!key) { console.log('RESEND_API_KEY not set; skipping branded email.'); return { statusCode: 200, body: 'skipped' }; }
  let payload;
  try { payload = JSON.parse(event.body).payload; } catch { return { statusCode: 400, body: 'bad payload' }; }

  const msg = render(payload);
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: FROM, to: [TO], subject: msg.subject, html: msg.html, text: msg.text, ...(msg.replyTo ? { reply_to: msg.replyTo } : {}) }),
  });
  if (!res.ok) { console.error('Resend error', res.status, await res.text()); return { statusCode: 502, body: 'send failed' }; }
  return { statusCode: 200, body: 'sent' };
};
