const $ = (selector) => document.querySelector(selector);

async function checkHealth() {
  const status = $("#status");
  try {
    const response = await fetch("/health");
    const data = await response.json();
    status.textContent = data.gemini_configured
      ? `API ready • ${data.model}`
      : "API running • add GEMINI_API_KEY to enable AI";
  } catch {
    status.textContent = "API unavailable";
  }
}

function showOutput(element, content, error = false) {
  element.classList.remove("hidden");
  element.classList.toggle("error", error);
  element.innerHTML = content;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderQuiz(quiz, output) {
  output.innerHTML = "";
  output.classList.remove("hidden", "error");

  quiz.forEach((item, index) => {
    const wrapper = document.createElement("div");
    wrapper.className = "quiz-question";
    wrapper.innerHTML = `
      <strong>Q${index + 1}. ${escapeHtml(item.question)}</strong>
      <div class="quiz-options">
        ${item.options.map((option) => `
          <label>
            <input type="radio" name="quiz-${index}" value="${escapeHtml(option)}">
            ${escapeHtml(option)}
          </label>
        `).join("")}
      </div>
      <button type="button" class="check-answer">Check Answer</button>
      <div class="feedback"></div>
    `;

    const checkButton = wrapper.querySelector(".check-answer");
    const feedback = wrapper.querySelector(".feedback");
    checkButton.addEventListener("click", () => {
      const selected = wrapper.querySelector(`input[name="quiz-${index}"]:checked`);
      if (!selected) {
        feedback.textContent = "Please select an option.";
        return;
      }
      feedback.textContent = selected.value === item.answer
        ? "✅ Correct!"
        : `❌ Incorrect. Correct answer: ${item.answer}`;
    });
    output.appendChild(wrapper);
  });
}

async function submitForm(form) {
  const output = document.getElementById(form.dataset.output);
  const button = form.querySelector("button[type='submit']");
  const data = Object.fromEntries(new FormData(form).entries());
  const method = form.dataset.method;

  button.disabled = true;
  button.textContent = "Thinking...";
  showOutput(output, "Generating...");

  try {
    let url = form.dataset.endpoint;
    const options = { method, headers: {} };

    if (method === "GET") {
      url += "?" + new URLSearchParams(data);
    } else {
      options.headers["Content-Type"] = "application/json";
      options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || payload.error || "Request failed.");
    }

    if (form.dataset.kind === "question") {
      showOutput(output, `<strong>Answer:</strong>\n${escapeHtml(payload.answer)}`);
    } else if (form.dataset.kind === "topic") {
      showOutput(output, escapeHtml(payload.explanation || payload.recommendations));
    } else if (form.dataset.output === "summaryResult") {
      showOutput(output, `<strong>Summary:</strong>\n${escapeHtml(payload.summary)}`);
    } else if (form.dataset.output === "quizResult") {
      renderQuiz(payload.quiz, output);
    }
  } catch (error) {
    showOutput(output, escapeHtml(error.message), true);
  } finally {
    button.disabled = false;
    button.textContent =
      form.dataset.output === "qaResult" ? "Get Answer" :
      form.dataset.output === "explainResult" ? "Explain" :
      form.dataset.output === "summaryResult" ? "Summarize" :
      form.dataset.output === "quizResult" ? "Generate Quiz" :
      "Get Recommendations";
  }
}

document.querySelectorAll("form").forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    submitForm(form);
  });
});

checkHealth();
