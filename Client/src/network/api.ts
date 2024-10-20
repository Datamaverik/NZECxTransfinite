import axios from "axios";
import { CodeBody } from "../components/InputBox";

const baseURL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface TestRouteResponse {
  message: string;
}
export const testRoute = async () => {
  try {
    const response = await api.get<TestRouteResponse>("/");
    return response.data;
  } catch (er) {
    throw new Error(er.message);
  }
};

export interface loginCredentials {
  username: string;
  password: string;
  name: string;
}

export const vulnRes = async (input: CodeBody) => {
  try {
    const response = await api.post("/api/check_vuln", input);
    return response.data;
  } catch (er) {
    throw new Error(er);
  }
};

export const gitResponse = async (input: string) => {
  try {
    const response = await api.get("/api/evaluate_repo", {
      params: { github_link: input },
    });
    return response.data;
  } catch (er) {
    throw new Error(er);
  }
};
