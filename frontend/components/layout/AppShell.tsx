import { Header } from "./Header";

import { Sidebar } from "./Sidebar";

type Props = {
  children: React.ReactNode;
};

export function AppShell({ children }: Props) {
  return (
    <div className="flex h-screen">
      <Sidebar />

      <div className="flex flex-1 flex-col">
        <Header />

        <main className="flex-1 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}
