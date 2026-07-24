/**
 * script.js
 * =========
 * จุดต่อทุกอย่างเข้าด้วยกัน — ไม่มี business logic ของตัวเอง แค่ wire
 * event ของปุ่ม Analyze เข้ากับ DocumentPanel + Suggestions
 */

const USE_REAL_BACKEND = true;

document.addEventListener("DOMContentLoaded", () => {
  window.DocumentPanel.init("#doc-page");

  const analyzeBtn = document.getElementById("analyze-btn");
  const statusLine = document.getElementById("status-line");

  analyzeBtn.addEventListener("click", async () => {
    analyzeBtn.disabled = true;
    statusLine.textContent = "กำลังวิเคราะห์เอกสาร";
    statusLine.classList.remove("idle");
    window.Suggestions.renderLoading();

    try {
      const instructions = USE_REAL_BACKEND
        ? await window.Suggestions.fetchReal(
            window.DocumentPanel.getPlainText()
          )
        : await window.Suggestions.fetchMock();

      window.Suggestions.renderAll(instructions);
      statusLine.textContent = `พบ ${instructions.length} คำแนะนำ`;
    } catch (err) {
      statusLine.textContent = "วิเคราะห์ไม่สำเร็จ";
      const list = document.getElementById("rail-list");
      list.innerHTML = `<div class="empty-state">เกิดข้อผิดพลาด: ${err.message}</div>`;
    } finally {
      analyzeBtn.disabled = false;
    }
  });
});
