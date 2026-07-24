/**
 * document.js
 * ============
 * จัดการฝั่ง "เอกสาร" (.page) เท่านั้น — ไม่รู้จัก suggestion card เลย
 * (แยก concern: document.js แก้ DOM ของเอกสาร, suggestions.js แก้ DOM ของ rail)
 *
 */

window.DocumentPanel = (function () {
  let container = null;

  function init(selector) {
    container = document.querySelector(selector);
  }

  function getPlainText() {
    const paragraphs = container.querySelectorAll("[data-para]");
    return Array.from(paragraphs)
      .map((p) => p.textContent)
      .join("\n\n");
  }

  function injectDiff(id, oldStr, newStr) {
    const paragraphs = container.querySelectorAll("[data-para]");

    for (const p of paragraphs) {
      const idx = p.innerHTML.indexOf(oldStr);
      if (idx === -1) continue;

      const before = p.innerHTML.slice(0, idx);
      const after = p.innerHTML.slice(idx + oldStr.length);
      p.innerHTML =
        `${before}<span class="pending-diff" data-suggestion-id="${id}">` +
        `<del>${oldStr}</del><ins>${newStr}</ins></span>${after}`;
      return true;
    }

    console.warn(
      `[document.js] ไม่พบข้อความ "${oldStr}" ในเอกสาร — ข้าม instruction นี้`
    );
    return false;
  }

  function apply(id, newStr) {
    const span = container.querySelector(
      `.pending-diff[data-suggestion-id="${id}"]`
    );
    if (!span) {
      console.warn(
        `[document.js] ไม่พบ pending-diff id=${id} (อาจถูก apply/dismiss ไปแล้ว)`
      );
      return false;
    }
    span.replaceWith(document.createTextNode(newStr));
    return true;
  }

  /** Dismiss: คืนค่าเป็น old text เดิม*/
  function dismiss(id, oldStr) {
    const span = container.querySelector(
      `.pending-diff[data-suggestion-id="${id}"]`
    );
    if (!span) return false;
    span.replaceWith(document.createTextNode(oldStr));
    return true;
  }

  return { init, getPlainText, injectDiff, apply, dismiss };
})();
