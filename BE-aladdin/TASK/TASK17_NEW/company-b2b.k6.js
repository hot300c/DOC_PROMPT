import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
  vus: Number(__ENV.K6_VUS || 1),
  iterations: Number(__ENV.K6_ITERS || 1),
  thresholds: {
    http_req_failed: ['rate==0'],
    http_req_duration: ['p(95)<1000'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:5000';
const SESSION_ID = __ENV.SESSION_ID || '';
const USER_ID = __ENV.USER_ID || '00000000-0000-0000-0000-000000000000';

function headersJson() {
  const headers = { 'Content-Type': 'application/json' };
  if (SESSION_ID) headers['Cookie'] = `SessionID=${SESSION_ID}`;
  return headers;
}

function parseJson(res) {
  try { return res.json(); } catch { return {}; }
}

export default function () {
  let createdId = null;

  group('CompanyB2B - Save (Create)', () => {
    const payload = {
      CompanyB2BID: null,
      CompanyTax: `9${Math.floor(Math.random() * 1e9).toString().padStart(9, '0')}`,
      CompanyCode: `K6_${Date.now()}`,
      CompanyName: 'K6 Test Company',
      CompanyAddress: '123 K6 Street',
      EffectiveFrom: new Date().toISOString(),
      EffectiveTo: null,
      IsActive: true,
      Hopdong: 'HD-K6',
      UserID: USER_ID,
    };
    const res = http.post(`${BASE_URL}/api/company-b2b/save`, JSON.stringify(payload), { headers: headersJson() });
    const body = parseJson(res);
    check(res, {
      'save(create) status 200': (r) => r.status === 200,
      'save(create) message ok': () => body.message === 'Success',
      'save(create) data present': () => body.data && body.data.Tables && body.data.Tables.length >= 1,
    });
    // Assert Result == Created
    try {
      const rows = body.data.Tables[0].Rows;
      check(rows, { 'save(create) result Created': (r) => r && r[0] && (r[0].Result || '').toLowerCase() === 'created' });
    } catch {}
    // Extract CompanyB2BID from Table1 row 0 if present
    try {
      const rows = body.data.Tables[0].Rows;
      createdId = rows && rows.length > 0 ? rows[0].CompanyB2BID || rows[0].CompanyB2Bid || rows[0].CompanyId : null;
    } catch { /* ignore */ }
  });

  group('CompanyB2B - Get by ID', () => {
    if (!createdId) return;
    const res = http.get(`${BASE_URL}/api/company-b2b/get?companyB2BID=${createdId}`, { headers: headersJson() });
    const body = parseJson(res);
    check(res, { 'get status 200': (r) => r.status === 200 });
    check(body, {
      'get message ok': (b) => b.message === 'Success',
      'get has Table2 one row': (b) => b.data && b.data.Tables && b.data.Tables[1] && b.data.Tables[1].Rows && b.data.Tables[1].Rows.length === 1,
    });
    // Optional sanity checks on fields
    try {
      const r = body.data.Tables[1].Rows[0];
      check(r, {
        'get row has CompanyB2Bid': (x) => !!(x.CompanyB2Bid || x.CompanyB2BID || x.CompanyId),
        'get row has CompanyName': (x) => !!x.CompanyName,
      });
    } catch {}
  });

  group('CompanyB2B - List (keyword + paging)', () => {
    const url = `${BASE_URL}/api/company-b2b/list?keyword=K6&sortBy=CreatedOn&sortDir=DESC&page=1&pageSize=10`;
    const res = http.get(url, { headers: headersJson() });
    const body = parseJson(res);
    check(res, { 'list status 200': (r) => r.status === 200 });
    check(body, {
      'list has Table1': (b) => b.data && b.data.Tables && b.data.Tables[0],
      'list has Table2 (meta)': (b) => b.data && b.data.Tables && b.data.Tables[1],
      'list meta has Total/Page/PageSize': (b) => {
        try {
          const meta = b.data.Tables[1].Rows[0];
          return typeof meta.Total === 'number' && typeof meta.Page === 'number' && typeof meta.PageSize === 'number';
        } catch { return false; }
      },
    });
  });

  group('CompanyB2B - Save (Update)', () => {
    if (!createdId) return;
    const payload = {
      CompanyB2BID: createdId,
      CompanyTax: `8${Math.floor(Math.random() * 1e9).toString().padStart(9, '0')}`,
      CompanyCode: `K6_${Date.now()}`,
      CompanyName: 'K6 Test Company Updated',
      CompanyAddress: '456 K6 Avenue',
      EffectiveFrom: new Date().toISOString(),
      EffectiveTo: null,
      IsActive: true,
      Hopdong: 'HD-K6-U',
      UserID: USER_ID,
    };
    const res = http.post(`${BASE_URL}/api/company-b2b/save`, JSON.stringify(payload), { headers: headersJson() });
    const body = parseJson(res);
    check(res, { 'save(update) status 200': (r) => r.status === 200 });
    check(body, { 'save(update) ok': (b) => b.message === 'Success' });
    try {
      const rows = body.data.Tables[0].Rows;
      check(rows, { 'save(update) result Updated': (r) => r && r[0] && (r[0].Result || '').toLowerCase() === 'updated' });
    } catch {}
  });

  group('CompanyB2B - Export', () => {
    const res = http.get(`${BASE_URL}/api/company-b2b/export?companyCode=&isActive=true`, { headers: headersJson() });
    const body = parseJson(res);
    check(res, { 'export status 200': (r) => r.status === 200 });
    check(body, {
      'export file meta present': (b) => b.data && b.data.Tables && b.data.Tables[1] && b.data.Tables[1].Rows && b.data.Tables[1].Rows[0] && b.data.Tables[1].Rows[0].FileData,
      'export file extension csv': (b) => {
        try { return b.data.Tables[1].Rows[0].FileExtension === '.csv'; } catch { return false; }
      },
    });
  });

  group('CompanyB2B - Import (CSV base64)', () => {
    const csv = [
      'CompanyTax,CompanyCode,CompanyName,CompanyAddress,EffectiveFrom,EffectiveTo,IsActive,Hopdong',
      `1234567890,K6_IMP_${Date.now()},K6 Import Co,Import Street,${new Date().toISOString()},,true,HD-K6-IMP`,
    ].join('\n');
    const base64 = typeof btoa !== 'undefined' ? btoa(csv) : Buffer.from(csv).toString('base64');
    const payload = { Base64Data: base64, FileName: 'k6-import.csv', UserID: USER_ID };
    const res = http.post(`${BASE_URL}/api/company-b2b/import`, JSON.stringify(payload), { headers: headersJson() });
    const body = parseJson(res);
    check(res, { 'import status 200': (r) => r.status === 200 });
    check(body, { 'import ok': (b) => b.message === 'Success' });
    try {
      const r = body.data.Tables[0].Rows[0];
      check(r, {
        'import result OK': (x) => (x.Result || '').toLowerCase() === 'ok',
        'import created >= 1': (x) => typeof x.Created === 'number' && x.Created >= 1,
      });
    } catch {}
  });

  group('CompanyB2B - Delete (Toggle IsActive)', () => {
    if (!createdId) return;
    const payload = { CompanyB2BID: createdId, UserID: USER_ID };
    const res = http.post(`${BASE_URL}/api/company-b2b/delete`, JSON.stringify(payload), { headers: headersJson() });
    const body = parseJson(res);
    check(res, { 'delete status 200': (r) => r.status === 200 });
    check(body, { 'delete ok': (b) => b.message === 'Success' });
    // Verify toggled by fetching again
    try {
      const res2 = http.get(`${BASE_URL}/api/company-b2b/get?companyB2BID=${createdId}`, { headers: headersJson() });
      const body2 = parseJson(res2);
      const row = body2.data && body2.data.Tables && body2.data.Tables[1] && body2.data.Tables[1].Rows && body2.data.Tables[1].Rows[0];
      check(row, { 'delete toggled inactive': (x) => x && x.IsActive === false });
    } catch {}
  });

  sleep(0.2);
}


