import React, { createContext, useContext, useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { api } from "../api/client";

type User = { id: number; name: string; email: string };
type AuthContextType = {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
};

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    AsyncStorage.multiGet(["token", "user"]).then(([t, u]) => {
      if (t[1] && u[1]) {
        setToken(t[1]);
        setUser(JSON.parse(u[1]));
      }
      setLoading(false);
    });
  }, []);

  const login = async (email: string, password: string) => {
    const res = await api.login(email, password);
    await AsyncStorage.multiSet([["token", res.token], ["user", JSON.stringify(res.user)]]);
    setToken(res.token);
    setUser(res.user);
  };

  const register = async (name: string, email: string, password: string) => {
    const res = await api.register(name, email, password);
    await AsyncStorage.multiSet([["token", res.token], ["user", JSON.stringify(res.user)]]);
    setToken(res.token);
    setUser(res.user);
  };

  const logout = async () => {
    await AsyncStorage.multiRemove(["token", "user"]);
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
