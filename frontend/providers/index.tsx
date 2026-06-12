"use client";

import { QueryProvider } from "./QueryProvider";
import { ThemeProvider } from "./ThemeProvider";

type Props = {
  children: React.ReactNode;
};

export function Providers({
  children,
}: Props) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <QueryProvider>
        {children}
      </QueryProvider>
    </ThemeProvider>
  );
}