import { Bell, Search } from "lucide-react";

export function Header() {
  return (
    <header
      className="
        sticky
        top-0
        z-50
        h-16
        border-b
        bg-background
      "
    >
      <div className="flex h-full items-center justify-between px-6">
        <div className="relative w-full max-w-md">
          <Search
            className="
              absolute
              left-3
              top-1/2
              h-4
              w-4
              -translate-y-1/2
              text-muted-foreground
            "
          />

          <input
            placeholder="Search topics, roadmaps..."
            className="
              h-10
              w-full
              rounded-xl
              border
              bg-background
              pl-10
              pr-4
              text-sm
              outline-none
              transition-all
              focus:ring-2
              focus:ring-blue-500
            "
          />
        </div>

        <div className="flex items-center gap-3">
          <button
            className="
              flex
              h-10
              w-10
              items-center
              justify-center
              rounded-xl
              transition-colors
              hover:bg-muted
            "
          >
            <Bell className="h-5 w-5" />
          </button>

          <div className="h-9 w-9 rounded-full bg-slate-300" />
        </div>
      </div>
    </header>
  );
}
