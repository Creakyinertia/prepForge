export function Header() {
  return (
    <header className="sticky top-0 z-20 border-b bg-background">
      <div className="flex h-16 items-center justify-between px-6">
        <div>
          <h1 className="font-semibold">
            PrepForge
          </h1>
        </div>

        <div className="flex items-center gap-4">
          <div className="h-8 w-8 rounded-full bg-slate-300" />
        </div>
      </div>
    </header>
  );
}