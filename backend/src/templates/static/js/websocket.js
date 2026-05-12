const from = document.querySelector("#join-room-form");
from.addEventListener("submit", async (e) => {
  const username = document.getElementById("username").value;
  const access_key = document.getElementById("room_access_key").value;

  const socket = new WebSocket(
    `ws://localhost:8000api/rooms/join?username=${username}&room_access_key=${access_key}`,
  );
});
