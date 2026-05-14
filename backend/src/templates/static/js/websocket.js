(function () {
  function scrollChatToBottom() {
    const el = document.getElementById("chat-messages-scroll");
    if (el) el.scrollTop = el.scrollHeight;
  }

  window.scrollChatToBottom = scrollChatToBottom;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scrollChatToBottom);
  } else {
    scrollChatToBottom();
  }
})();
