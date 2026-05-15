(function () {
  const config = window.__CHAT_CONFIG__;
  if (!config?.roomId || !config?.userId) {
    return;
  }

  const messagesList = document.getElementById("chat-messages-list");
  const messageInput = document.getElementById("chat-message-input");
  const sendBtn = document.getElementById("chat-send-btn");
  const connectionStatus = document.getElementById("chat-connection-status");

  if (!messagesList || !messageInput || !sendBtn) {
    return;
  }

  const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl =
    `${wsProtocol}//${window.location.host}/api/rooms/ws/chat` +
    `?room_id=${encodeURIComponent(config.roomId)}` +
    `&user_id=${encodeURIComponent(config.userId)}`;

  let socket = null;
  let reconnectTimer = null;

  function setConnectionStatus(text, isError) {
    if (!connectionStatus) return;
    connectionStatus.textContent = text;
    connectionStatus.classList.toggle("text-red-400", Boolean(isError));
    connectionStatus.classList.toggle("text-[#8a8a8a]", !isError);
  }

  function scrollChatToBottom() {
    if (typeof window.scrollChatToBottom === "function") {
      window.scrollChatToBottom();
    }
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function appendSystemMessage(payload) {
    const item = document.createElement("p");
    item.className =
      "system-message w-full shrink-0 text-center text-[0.8125rem] leading-snug text-[#8a8a8a]";
    const label =
      payload.type === "user_joined"
        ? "joined"
        : payload.type === "user_left"
          ? "left"
          : "update";
    item.textContent = `${payload.username || "Someone"} ${label} · ${payload.timestamp || ""}`;
    messagesList.appendChild(item);
    scrollChatToBottom();
  }

  function appendChatMessage(payload) {
    const article = document.createElement("article");
    article.className =
      "message-group flex max-w-[min(100%,28rem)] shrink-0 gap-3 self-start";

    const isSelf =
      config.username &&
      payload.username &&
      payload.username.toLowerCase() === config.username.toLowerCase();

    if (isSelf) {
      article.classList.remove("self-start");
      article.classList.add("self-end");
    }

    const authorColor = isSelf ? "text-[#60a5fa]" : "text-[#35d99d]";

    const content = document.createElement("div");
    content.className =
      "message-content min-w-0 rounded-[15px] border border-white/[0.06] bg-white/[0.04] px-3.5 py-2.5";

    const header = document.createElement("div");
    header.className =
      "message-header mb-1.5 flex flex-wrap items-baseline gap-x-3 gap-y-2";

    const author = document.createElement("span");
    author.className = `author font-semibold ${authorColor}`;
    author.textContent = payload.username || "unknown";

    const timestamp = document.createElement("span");
    timestamp.className = "timestamp text-xs tabular-nums text-gray-500";
    timestamp.textContent = payload.timestamp || "";

    const body = document.createElement("div");
    body.className =
      "message-body break-words text-[0.9375rem] leading-[1.55] text-[#e5e5e5] [overflow-wrap:anywhere]";
    body.textContent = payload.message || "";

    header.append(author, timestamp);
    content.append(header, body);
    article.append(content);

    messagesList.appendChild(article);
    scrollChatToBottom();
  }

  function handleIncomingMessage(event) {
    let payload;
    try {
      payload = JSON.parse(event.data);
    } catch {
      return;
    }

    if (payload.type === "user_joined" || payload.type === "user_left") {
      appendSystemMessage(payload);
      return;
    }

    appendChatMessage(payload);
  }

  function sendMessage() {
    const text = messageInput.value.trim();
    if (!text || !socket || socket.readyState !== WebSocket.OPEN) {
      return;
    }

    socket.send(text);
    messageInput.value = "";
    messageInput.focus();
  }

  function scheduleReconnect() {
    if (reconnectTimer) return;
    reconnectTimer = window.setTimeout(() => {
      reconnectTimer = null;
      connect();
    }, 2000);
  }

  function connect() {
    if (
      socket &&
      (socket.readyState === WebSocket.OPEN ||
        socket.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    setConnectionStatus("Connecting…", false);
    socket = new WebSocket(wsUrl);

    socket.addEventListener("open", () => {
      setConnectionStatus("Connected", false);
    });

    socket.addEventListener("message", handleIncomingMessage);

    socket.addEventListener("close", () => {
      setConnectionStatus("Disconnected — retrying…", true);
      scheduleReconnect();
    });

    socket.addEventListener("error", () => {
      setConnectionStatus("Connection error", true);
    });
  }

  sendBtn.addEventListener("click", sendMessage);
  messageInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });

  connect();
})();
