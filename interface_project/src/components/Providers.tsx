'use client';

import { AuthProvider } from "@/context/AuthContext";
import { ReactNode } from "react";



export function AuthProviders({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}



export function Providers({ children }: { children: ReactNode }) {
  return (

      <AuthProvider>
     
        {children}

      </AuthProvider>
     

  );
}
