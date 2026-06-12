"use client";

import Link from "next/link";

import { usePathname } from "next/navigation";

import { navigation } from "./navigation";

import { cn } from "@/lib/utils";

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden h-screen w-[280px] shrink-0 border-r lg:block">
      <div className="px-6 py-5">
        <h1 className="text-2xl font-bold tracking-tight">PrepForge</h1>
      </div>

      <nav className="space-y-8 px-4 pt-4">
        {navigation.map((section) => (
          <div key={section.title}>
            <p className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {section.title}
            </p>

            <div className="space-y-1">
              {section.items.map((item) => {
                const Icon = item.icon;

                const active = pathname === item.href;

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      `
                      group
                      flex
                      items-center
                      gap-3
                      rounded-xl
                      px-3
                      py-2.5
                      text-sm
                      font-medium
                      transition-all
                      duration-200
                      `,
                      active
                        ? `
                          bg-blue-600
                          text-white
                          shadow-sm
                        `
                        : `
                          text-muted-foreground
                          hover:bg-muted
                          hover:text-foreground
                          hover:translate-x-1
                        `
                    )}
                  >
                    <Icon
                      className="
                          h-4
                          w-4
                          transition-transform
                          duration-200
                          group-hover:scale-110
                        "
                    />

                    {item.label}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>
      {/* <div className="mt-auto border-t p-4">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-full bg-slate-300" />

          <div>
            <p className="text-sm font-medium">Darshan</p>

            <p className="text-xs text-muted-foreground">Frontend Engineer</p>
          </div>
        </div>
      </div> */}
    </aside>
  );
}
