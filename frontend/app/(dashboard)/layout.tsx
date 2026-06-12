import { AppShell } from "@/components/layout/AppShell";

type Props = {
  children: React.ReactNode;
};

export default function DashboardLayout({
  children,
}: Props) {
  return (
    <AppShell>
      {children}
    </AppShell>
  );
}