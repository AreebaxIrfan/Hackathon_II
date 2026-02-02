'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';

type User = {
  id: string;
  email: string;
  created_at: string;
  is_active: boolean;
};

type AuthContextType = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in on initial load
    const token = localStorage.getItem('access_token');
    if (token) {
      // Verify token and get user info
      fetchUserInfo();
    } else {
      setIsLoading(false);
    }
  }, []);

  const fetchUserInfo = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        // Token is invalid, clear it
        localStorage.removeItem('access_token');
      }
    } catch (error) {
      console.error('Failed to fetch user info:', error);
      localStorage.removeItem('access_token');
    } finally {
      setIsLoading(false);
    }
  };

  const parseError = (errorData: any): string => {
    if (typeof errorData.detail === 'string') {
      return errorData.detail;
    }
    if (Array.isArray(errorData.detail)) {
      return errorData.detail.map((err: any) => err.msg).join(', ');
    }
    return 'An unexpected error occurred';
  };

  const login = async (email: string, password: string) => {
    console.log(`Logging in to: ${process.env.NEXT_PUBLIC_API_URL}/auth/login`);
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Login failed:', errorData);
      throw new Error(parseError(errorData));
    }

    const data = await response.json();

    // Store token in localStorage
    localStorage.setItem('access_token', data.access_token);

    // Fetch user info
    await fetchUserInfo();
  };

  const register = async (email: string, password: string) => {
    console.log(`Registering at: ${process.env.NEXT_PUBLIC_API_URL}/auth/register`);
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Registration failed:', errorData);
      throw new Error(parseError(errorData));
    }

    // Auto-login after successful registration
    await login(email, password);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    router.push('/auth/login');
    router.refresh();
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}