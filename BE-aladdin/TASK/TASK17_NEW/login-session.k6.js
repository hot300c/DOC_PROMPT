import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1,
  iterations: 1,
};

export default function () {
  const baseUrl = __ENV.BASE_URL || 'http://localhost:5272';
  const username = __ENV.USERNAME || '';
  const passwordMd5 = __ENV.PASSWORD_MD5 || '';
  const facId = __ENV.FAC_ID || '';

  if (!username || !passwordMd5) {
    throw new Error('USERNAME and PASSWORD_MD5 are required.');
  }

  const url = `${baseUrl}/Login`;
  const payload = JSON.stringify({ Username: username, PasswordHash: passwordMd5, FacId: facId });
  const params = { headers: { 'Content-Type': 'application/json' } };

  const res = http.post(url, payload, params);

  check(res, {
    'login status is 200': (r) => r.status === 200,
  });

  const sCookie = res.cookies && res.cookies['s'] && res.cookies['s'][0] ? res.cookies['s'][0].value : null;
  if (sCookie) {
    console.log(`SESSION_COOKIE_s=${sCookie}`);
  } else {
    console.error('No session cookie "s" returned.');
  }

  // small pause for readability in logs
  sleep(0.2);
}


