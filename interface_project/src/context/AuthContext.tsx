"use client";

import { AuthResponse } from "@/types/auth";

import {
  createContext,useState,ReactNode} from "react";

interface AuthContextProps {
  auth: AuthResponse | undefined;
  setAuth: (auth: AuthResponse) => void;
}

export const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }){
  const [auth, setAuth] = useState<AuthResponse>();


  return (
      <AuthContext.Provider value={{auth,setAuth} }>
        {children}
      </AuthContext.Provider>
    );

}