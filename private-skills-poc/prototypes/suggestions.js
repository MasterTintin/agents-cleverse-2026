/**
 * suggestions.js
 * ==============
 * แหล่งข้อมูล suggestion + render เป็น
 * card ใน rail — ไม่รู้จัก DOM ของเอกสาร สั่งผ่าน DocumentPanel
 * เท่านั้น
 */

window.Suggestions = (function () {
  const GATEWAY_URL = "http://127.0.0.1:8000";
  const MOCK_INSTRUCTIONS = [
    {
      old_str: "ลูกจ้างเป็นระยะเวลา 6 เดือน",
      new_str: "ลูกจ้างเป็นระยะเวลา 1 ปี นับจากวันที่เริ่มปฏิบัติงาน",
      reason:
        "ระยะเวลาจ้างงานควรระบุให้ชัดเจนพร้อมวันเริ่มต้น เพื่อหลีกเลี่ยงความกำกวมทางกฎหมาย",
      category: "Legal Compliance",
      priority: "high"
    },
    {
      old_str: "ตามที่ตกลงกันด้วยวาจา",
      new_str: "ตามอัตราที่ระบุไว้ในเอกสารแนบท้ายสัญญาฉบับนี้",
      reason:
        "ข้อตกลงด้วยวาจาพิสูจน์ยากหากเกิดข้อพิพาท ควรอ้างอิงเอกสารที่ตรวจสอบได้",
      category: "Legal Compliance",
      priority: "medium"
    }
  ];

  let counter = 0;
  function nextId() {
    counter += 1;
    return `s${counter}`;
  }

  function fetchMock() {
    return new Promise((resolve) => {
      setTimeout(() => resolve(MOCK_INSTRUCTIONS), 900);
    });
  }

  /**
   * เรียก Gateway จริงตาม contract {skill, input} ->
   * {instructions: [{old_str, new_str, reason}]}
   */
  async function fetchReal(documentText) {
    const res = await fetch(`${GATEWAY_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        skill: "employment-contract-reviewer",
        input: { document: documentText }
      })
    });

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || `Gateway ตอบกลับผิดพลาด: ${res.status}`);
    }

    const data = await res.json();
    return data.instructions;
  }

  function renderCard(instruction, id) {
    const el = document.createElement("div");
    el.className = "suggestion";
    el.dataset.suggestionId = id;

    const categoryTag = instruction.category
      ? `<span class="category-tag">${instruction.category}</span>`
      : "";

    const priorityTag = instruction.priority
      ? `<span class="priority-tag priority-${instruction.priority}">${instruction.priority.toUpperCase()}</span>`
      : "";

    const tagsRow =
      categoryTag || priorityTag
        ? `<div class="tags-row">${priorityTag}${categoryTag}</div>`
        : "";

    el.innerHTML = `
      <div class="who">
        <div class="avatar">📄</div>
        <div class="name">Employment Contract Reviewer</div>
      </div>
      ${tagsRow}
      <div class="diff"><del>${escapeHtml(instruction.old_str)}</del><ins>${escapeHtml(instruction.new_str)}</ins></div>
      <div class="reason"><span class="label">Reason</span>${escapeHtml(instruction.reason)}</div>
      <div class="actions">
        <button class="accept">✓ Apply</button>
        <button class="dismiss">✕ Dismiss</button>
      </div>
    `;

    el.querySelector(".accept").addEventListener("click", () => {
      const ok = window.DocumentPanel.apply(id, instruction.new_str);
      if (!ok) {
        el.querySelector(".reason").innerHTML =
          '<span class="label">Reason</span>⚠️ ไม่พบข้อความนี้ในเอกสารแล้ว (อาจถูกแก้ไปก่อนหน้านี้)';
        return;
      }
      el.remove();
      updateEmptyState();
    });

    el.querySelector(".dismiss").addEventListener("click", () => {
      window.DocumentPanel.dismiss(id, instruction.old_str);
      el.remove();
      updateEmptyState();
    });

    return el;
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  function updateEmptyState() {
    const list = document.getElementById("rail-list");
    const remaining = list.querySelectorAll(".suggestion").length;
    if (remaining === 0) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.id = "empty-state";
      empty.textContent = "ไม่มีคำแนะนำที่รอดำเนินการแล้ว";
      list.appendChild(empty);
    }
  }

  function renderAll(instructions) {
    const list = document.getElementById("rail-list");
    list.innerHTML = "";

    if (instructions.length === 0) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.textContent = "ไม่พบจุดที่ควรแก้ไขในเอกสารนี้";
      list.appendChild(empty);
      return;
    }

    instructions.forEach((instruction) => {
      const id = nextId();
      window.DocumentPanel.injectDiff(
        id,
        instruction.old_str,
        instruction.new_str
      );
      list.appendChild(renderCard(instruction, id));
    });
  }

  function renderLoading() {
    const list = document.getElementById("rail-list");
    list.innerHTML = '<div class="loading-state">กำลังวิเคราะห์เอกสาร...</div>';
  }

  return { fetchMock, fetchReal, renderAll, renderLoading };
})();
