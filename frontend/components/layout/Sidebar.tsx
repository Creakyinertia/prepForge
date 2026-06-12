"use client";

import Link from "next/link";

import { usePathname } from "next/navigation";

import { navigation } from "./navigation";

import { cn } from "@/lib/utils";

export function Sidebar() {
  const pathname =
    usePathname();

  return (
    <aside className="hidden h-screen w-[280px] shrink-0 border-r lg:block">
      <div className="p-6">
        <h2 className="text-xl font-bold">
          PrepForge
        </h2>
      </div>

      <nav className="space-y-6 px-4">
        {navigation.map(
          (section) => (
            <div
              key={section.title}
            >
              <p className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                {section.title}
              </p>

              <div className="space-y-1">
                {section.items.map(
                  (item) => {
                    const Icon =
                      item.icon;

                    const active =
                      pathname ===
                      item.href;

                    return (
                      <Link
                        key={
                          item.href
                        }
                        href={
                          item.href
                        }
                        className={cn(
                          "flex items-center gap-3 rounded-xl px-3 py-2 text-sm transition-colors",

                          active
                            ? "bg-primary text-white"
                            : "hover:bg-muted"
                        )}
                      >
                        <Icon className="h-4 w-4" />

                        {
                          item.label
                        }
                      </Link>
                    );
                  }
                )}
              </div>
            </div>
          )
        )}
      </nav>
    </aside>
  );
}