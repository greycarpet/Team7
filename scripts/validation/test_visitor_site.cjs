// Offline DOM contract tests; live browser CORS/CSP remains a deployment check.
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { readFileSync } = require("node:fs");
const { resolve } = require("node:path");
const vm = require("node:vm");
const source = readFileSync(resolve(__dirname, "../../site/assets/visitor-counter-v1.js"), "utf8");
const endpoint = "https://test123.execute-api.us-east-2.amazonaws.com/visits";

async function run(url, fetchImpl) {
  const display = { textContent: "Loading..." };
  const calls = [];
  await vm.runInNewContext(source, {
    document: { getElementById: () => display, querySelector: () => ({ content: url }) },
    fetch: async (...args) => { calls.push(args); return fetchImpl(...args); },
    AbortController, setTimeout, clearTimeout,
  });
  return { display, calls };
}

test("one POST per load displays a numeric response", async () => {
  const { display, calls } = await run(endpoint, async () => ({ ok: true, json: async () => ({ count: 1234 }) }));
  assert.equal(display.textContent, "1,234");
  assert.equal(calls.length, 1);
  assert.equal(calls[0][1].method, "POST");
  assert.equal(calls[0][1].credentials, "omit");
  assert.equal(calls[0][1].body, "{}");
});

test("failed requests and malformed data show fallback without retry", async () => {
  for (const reply of [async () => { throw new Error("network"); },
    async () => ({ ok: false }),
    async () => ({ ok: true, json: async () => ({ count: "<script>bad</script>" }) }),
    async () => ({ ok: true, json: async () => ({ count: Number.MAX_SAFE_INTEGER + 1 }) })]) {
    const { display, calls } = await run(endpoint, reply);
    assert.equal(display.textContent, "Temporarily unavailable");
    assert.equal(calls.length, 1);
  }
});

test("missing or foreign endpoint makes no request", async () => {
  for (const url of ["", "https://example.org/visits"]) {
    const { calls, display } = await run(url, () => { throw new Error("must not fetch"); });
    assert.equal(calls.length, 0);
    assert.equal(display.textContent, "Temporarily unavailable");
  }
});
