import Base_api_url from "./ApiConfig.js";

const JoinRoom = async (data) => {
  response = await Base_api_url.post("/room", data);
  if (response?.status == 201) {
    return {
      user_data: response.data,
      status: "ok",
    };
  }
};
