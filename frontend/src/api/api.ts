import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "https://web-crawler-backend1.onrender.com/",
    headers: {
        "Content-Type": "application/json",
    },
    timeout: 120000,
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error("API Error:", error);

        return Promise.reject(error);
    }
);

export default api;