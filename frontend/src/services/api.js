import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Add token to requests if available
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Authentication APIs
export const authAPI = {
    register: (userData) => api.post('/auth/register', userData),
    login: (credentials) => api.post('/auth/login', credentials),
    getProfile: () => api.get('/auth/profile')
};

// Image Processing APIs
export const imageAPI = {
    upload: (formData) => {
        return api.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    },
    recognize: (formData) => {
        return api.post('/recognize', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    },
    ocr: (formData) => {
        return api.post('/ocr', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    }
};

// Recipe APIs
export const recipeAPI = {
    search: (params) => api.get('/recipes/search', { params }),
    recommend: (ingredients) => api.post('/recipes/recommend', { ingredients }),
    getById: (id) => api.get(`/recipes/${id}`)
};

export default api;
