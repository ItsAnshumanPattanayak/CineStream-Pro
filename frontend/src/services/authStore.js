import { create } from 'zustand';
import { authAPI } from './api';

export const useAuthStore = create((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  loading: false,
  error: null,

  // Register user
  register: async (userData) => {
    set({ loading: true, error: null });
    try {
      const response = await authAPI.register(userData);
      const { user, token } = response.data;
      
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      
      set({
        user,
        token,
        isAuthenticated: true,
        loading: false
      });
      
      return { success: true, user };
    } catch (error) {
      const message = error.response?.data?.message || 'Registration failed';
      set({ error: message, loading: false });
      return { success: false, error: message };
    }
  },

  // Login user
  login: async (username, password) => {
    set({ loading: true, error: null });
    try {
      const response = await authAPI.login({ username, password });
      const { user, token } = response.data;
      
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      
      set({
        user,
        token,
        isAuthenticated: true,
        loading: false
      });
      
      return { success: true, user };
    } catch (error) {
      const message = error.response?.data?.message || 'Login failed';
      set({ error: message, loading: false });
      return { success: false, error: message };
    }
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    set({
      user: null,
      token: null,
      isAuthenticated: false,
      error: null
    });
  },

  // Load user from localStorage
  loadUser: () => {
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    
    if (token && userStr) {
      const user = JSON.parse(userStr);
      set({
        user,
        token,
        isAuthenticated: true
      });
    }
  },

  // Update user profile
  updateProfile: async (data) => {
    set({ loading: true, error: null });
    try {
      const response = await authAPI.updateProfile(data);
      const user = response.data.user;
      
      localStorage.setItem('user', JSON.stringify(user));
      
      set({
        user,
        loading: false
      });
      
      return { success: true, user };
    } catch (error) {
      const message = error.response?.data?.message || 'Update failed';
      set({ error: message, loading: false });
      return { success: false, error: message };
    }
  },

  // Change password
  changePassword: async (oldPassword, newPassword) => {
    set({ loading: true, error: null });
    try {
      await authAPI.changePassword({ old_password: oldPassword, new_password: newPassword });
      set({ loading: false });
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.message || 'Password change failed';
      set({ error: message, loading: false });
      return { success: false, error: message };
    }
  },

  // Clear error
  clearError: () => set({ error: null })
}));
