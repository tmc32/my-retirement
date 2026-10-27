const iso = (d) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;

// 28th of the month, rolled back to the previous working day (midnight local time)
function targetFor(year, month) {
  const d = new Date(year, month, 28);
  while (d.getDay() === 0 || d.getDay() === 6 || UK_HOLIDAYS.includes(iso(d))) {
    d.setDate(d.getDate() - 1);
  }
  return d;
}

function getTarget(now) {
  let target = targetFor(now.getFullYear(), now.getMonth());
  if (now >= target) target = targetFor(now.getFullYear(), now.getMonth() + 1);
  return target;
}

const fmt = (n, dp = 0) => n.toLocaleString("en-GB", { minimumFractionDigits: dp, maximumFractionDigits: dp });

function render() {
  const now = new Date();
  const target = getTarget(now);
  const secs = (target - now) / 1000;

  document.getElementById("title").textContent =
    "Target: " + target.toLocaleDateString("en-GB", { month: "long", year: "numeric" });
  document.getElementById("date").textContent =
    target.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long", year: "numeric" });

  const s = Math.floor(secs);
  document.getElementById("big").textContent =
    `${Math.floor(s / 86400)}d ${Math.floor((s % 86400) / 3600)}h ${Math.floor((s % 3600) / 60)}m ${s % 60}s`;

  const rows = [
    ["Weeks", fmt(secs / 604800, 2)],
    ["Days", fmt(secs / 86400, 2)],
    ["Hours", fmt(secs / 3600, 1)],
    ["Minutes", fmt(secs / 60)],
    ["Seconds", fmt(secs)],
  ];
  document.getElementById("units").innerHTML = rows.map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join("");
}

render();
setInterval(render, 1000);

if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js");
