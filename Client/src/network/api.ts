import axios from "axios";
import { AxiosError } from "axios";

const baseURL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface TestRouteResponse{
  message:string;
}
export const testRoute = async () => {
  try {
    const response = await api.get<TestRouteResponse>("/");
    return response.data;
  } catch (er) {
    if (er instanceof AxiosError) throw new Error(er.message);
  }
};

export interface loginCredentials {
  username: string;
  password: string;
  name:string;
}
