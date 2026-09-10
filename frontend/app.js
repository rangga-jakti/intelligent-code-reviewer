const API_BASE = "http://127.0.0.1:8000";

const reviewButton = document.getElementById("reviewButton");
const buttonText = document.getElementById("buttonText");
const spinner = document.getElementById("spinner");
const errorBox = document.getElementById("error");

function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.remove("hidden");
}

function clearError() {
    errorBox.textContent = "";
    errorBox.classList.add("hidden");
}

function setLoading(loading) {
    reviewButton.disabled = loading;
    buttonText.textContent = loading ? "Analyzing..." : "Review Code";
    spinner.classList.toggle("hidden", !loading);
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderFindings(findings) {
    const container = document.getElementById("findings");
    container.innerHTML = "";

    if (!findings.length) {
        container.innerHTML = "<p>No issues detected. Nice work.</p>";
        return;
    }

    findings.forEach((finding) => {
        const item = document.createElement("div");
        item.className = "finding";

        const title = document.createElement("div");
        title.className = "finding-header";

        const issue = document.createElement("span");
        issue.className = "finding-title";
        issue.textContent = finding.issue;

        const badge = document.createElement("span");
        badge.className = "badge";
        badge.textContent = finding.severity;

        title.appendChild(issue);
        title.appendChild(badge);
        item.appendChild(title);

        const explanation = document.createElement("p");
        explanation.textContent = finding.explanation || "";
        item.appendChild(explanation);

        const suggestion = document.createElement("p");
        suggestion.innerHTML = "<strong>Suggestion:</strong> ";
        suggestion.appendChild(document.createTextNode(finding.suggestion || ""));
        item.appendChild(suggestion);

        if (finding.line) {
            const line = document.createElement("p");
            line.innerHTML = "<strong>Line:</strong> ";
            line.appendChild(document.createTextNode(String(finding.line)));
            item.appendChild(line);
        }

        if (finding.historical_rule) {
            const rule = document.createElement("div");
            rule.className = "rule";
            rule.innerHTML = "<strong>Historical Rule:</strong><br>";
            rule.appendChild(document.createTextNode(finding.historical_rule));
            item.appendChild(rule);
        }

        container.appendChild(item);
    });
}

function renderList(elementId, items) {
    const element = document.getElementById(elementId);
    element.innerHTML = "";

    if (!items.length) {
        element.innerHTML = "<li>None identified.</li>";
        return;
    }

    items.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        element.appendChild(li);
    });
}

function renderResult(data) {
    document.getElementById("qualityScore").textContent = data.quality_rating;
    document.getElementById("findingCount").textContent = data.findings.length;
    document.getElementById("practiceCount").textContent = data.best_practices.length;
    document.getElementById("optimizationCount").textContent = data.optimizations.length;
    document.getElementById("summary").textContent = data.summary;

    renderFindings(data.findings);
    renderList("bestPractices", data.best_practices);
    renderList("optimizations", data.optimizations);

    document.getElementById("resultSection").classList.remove("hidden");
    document.getElementById("resultSection").scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

async function loadProgress(apiKey) {
    const response = await fetch(`${API_BASE}/progress`, {
        headers: {
            "X-API-Key": apiKey
        }
    });

    if (!response.ok) {
        return;
    }

    const data = await response.json();

    document.getElementById("totalReviews").textContent = data.total_reviews;
    document.getElementById("averageQuality").textContent = data.average_quality ?? "-";
    document.getElementById("bestQuality").textContent = data.best_quality ?? "-";
    document.getElementById("improvement").textContent =
        data.improvement === null
            ? "-"
            : `${data.improvement > 0 ? "+" : ""}${data.improvement}`;

    document.getElementById("progressSection").classList.remove("hidden");
}

reviewButton.addEventListener("click", async () => {
    clearError();

    const apiKey = document.getElementById("apiKey").value.trim();
    const language = document.getElementById("language").value;
    const code = document.getElementById("code").value;

    if (!apiKey) {
        showError("Please enter your API key.");
        return;
    }

    if (!code.trim()) {
        showError("Please enter some code to review.");
        return;
    }

    setLoading(true);

    try {
        const response = await fetch(`${API_BASE}/review`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-API-Key": apiKey
            },
            body: JSON.stringify({
                language,
                code
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Review request failed.");
        }

        renderResult(data);
        await loadProgress(apiKey);
        await loadHistory(apiKey);

    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
});
async function loadHistory(apiKey) {
    const response = await fetch(`${API_BASE}/reviews`, {
        headers: {
            "X-API-Key": apiKey
        }
    });
    if (!response.ok) {
        return;
    }
    const data = await response.json();
    const container = document.getElementById("history");
    container.innerHTML = "";
    if (!data.reviews.length) {
        container.innerHTML = "<p>No previous reviews yet.</p>";
        document.getElementById("historySection").classList.remove("hidden");
        return;
    }
    data.reviews.forEach((review) => {
        const item = document.createElement("div");
        item.className = "history-item";
        const meta = document.createElement("div");
        meta.className = "history-meta";
        const language = document.createElement("span");
        language.className = "history-language";
        language.textContent = review.language.toUpperCase();
        const score = document.createElement("span");
        score.className = "history-score";
        score.textContent = `${review.quality_rating} / 10`;
        meta.appendChild(language);
        meta.appendChild(score);
        const date = document.createElement("div");
        date.className = "history-date";
        date.textContent = review.created_at;
        const summary = document.createElement("p");
        summary.className = "history-summary";
        summary.textContent = review.summary;
        item.appendChild(meta);
        item.appendChild(date);
        item.appendChild(summary);
        container.appendChild(item);
    });
    document.getElementById("historySection").classList.remove("hidden");
}

