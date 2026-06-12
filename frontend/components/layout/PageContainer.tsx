import { cn } from "@/lib/utils";

type Props = {
  children: React.ReactNode;

  className?: string;
};

export function PageContainer({
  children,
  className,
}: Props) {
  return (
    <div
      className={cn(
        "mx-auto w-full max-w-7xl px-6 py-8",
        className,
      )}
    >
      {children}
    </div>
  );
}