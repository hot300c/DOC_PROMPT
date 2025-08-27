// Usage:
//   node DOCS_PROMPT/BE-aladdin/TASK/TASK17_NEW/gen-apikey.js "TASK17-Key" "FullAccess"
// Outputs raw API key, SHA256 hash, and SQL INSERT for [Security]..[ApiKeys]

const crypto = require('crypto');

function toSha256HexLower(input) {
  const hash = crypto.createHash('sha256').update(input, 'utf8').digest('hex');
  return hash.toLowerCase();
}

function main() {
  const name = process.argv[2] || 'TASK-Key';
  const role = process.argv[3] || 'FullAccess';

  // Generate random 32-byte token, encode Base64 as raw API key
  const raw = crypto.randomBytes(32).toString('base64');
  const hash = toSha256HexLower(raw);

  console.log('+ Generated API key');
  console.log('Name:', name);
  console.log('Role:', role);
  console.log('RAW_API_KEY:', raw);
  console.log('SHA256(Key) HEX lower:', hash);

  console.log('\n+ SQL INSERT statement:');
  console.log("INSERT INTO [Security]..[ApiKeys] (KeyHash, Name, Role)");
  console.log(`VALUES ('${hash}', '${name}', '${role}');`);

  console.log('\n+ How to use:');
  console.log('- Run the SQL above in your Security database (SSMS).');
  console.log('- Then call your API with header: X-API-KEY: ' + raw);
}

main();


