/* SCRUM-22: a page-view counter, not a unique-visitor metric. */
(async () => {
  "use strict";
  const display = document.getElementById("visitor-count");
  const endpoint = document.querySelector('meta[name="visitor-api"]')?.content;
  if (!display) return;
  const unavailable = () => { display.textContent = "Temporarily unavailable"; };
  if (!/^https:\/\/[a-z0-9]+\.execute-api\.us-east-2\.amazonaws\.com\/visits$/.test(endpoint || "")) {
    unavailable();
    return;
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const result = await fetch(endpoint, {
      method: "POST",
      mode: "cors",
      credentials: "omit",
      redirect: "error",
      cache: "no-store",
      referrerPolicy: "no-referrer",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: "{}",
      signal: controller.signal,
    });
    if (!result.ok) throw new Error("Counter request failed");
    const data = await result.json();
    if (!Number.isSafeInteger(data.count) || data.count < 1) throw new Error("Invalid count");
    display.textContent = data.count.toLocaleString("en-US");
  } catch {
    unavailable();
  } finally {
    clearTimeout(timeout);
  }
})();
