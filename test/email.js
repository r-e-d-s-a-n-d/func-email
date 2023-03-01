require('isomorphic-fetch');

const endpoint = 'http://127.0.0.1:7071/api/sendmail';
const email = {
    sendTo: 'rsandoval@REDACTED.com',
    subject: 'REDACTED Alert',
    template: 'default',
    data: {
      summary: 'This is a summary',
      content: {test: 'This is content'}
    }
}

const main = async () => {
    fetch(endpoint,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(email)
      })
    .then(res => res.text())
    .then(console.log)
}

(async () => {
    try { await main(); } 
    catch (e) { console.log(e); }
})();