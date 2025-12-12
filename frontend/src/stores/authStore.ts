import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, AuthTokens } from '@/types';
import apiClient from '@/services/api';

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
  setUser: (user: User | null) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email: string, password: string) => {
        try {
          set({ isLoading: true });
          const tokens = await apiClient.login(email, password);
          set({ tokens, isAuthenticated: true });
          await get().loadUser();
        } catch (error) {
          set({ user: null, tokens: null, isAuthenticated: false });
          throw error;
        } finally {
          set({ isLoading: false });
        }
      },

      logout: async () => {
        try {
          const { tokens } = get();
          if (tokens?.refresh_token) {
            await apiClient.logout(tokens.refresh_token);
          }
        } catch (error) {
          console.error('Logout error:', error);
        } finally {
          set({ user: null, tokens: null, isAuthenticated: false });
        }
      },

      loadUser: async () => {
        try {
          const user = await apiClient.getCurrentUser();
          set({ user, isAuthenticated: true });
        } catch (error) {
          set({ user: null, isAuthenticated: false });
          throw error;
        }
      },

      setUser: (user: User | null) => {
        set({ user, isAuthenticated: !!user });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ tokens: state.tokens }),
    }
  )
);
