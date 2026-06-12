import {
  BookMarked,
  FolderKanban,
  LayoutDashboard,
  NotebookPen,
  RefreshCcw,
  User,
} from "lucide-react";

export const navigation = [
  {
    title: "Main",

    items: [
      {
        label: "Dashboard",
        href: "/dashboard",
        icon: LayoutDashboard,
      },
    ],
  },

  {
    title: "Learn",

    items: [
      {
        label: "Roadmaps",
        href: "/roadmaps",
        icon: FolderKanban,
      },
    ],
  },

  {
    title: "Study",

    items: [
      {
        label: "Revisions",
        href: "/revisions",
        icon: RefreshCcw,
      },

      {
        label: "Notes",
        href: "/notes",
        icon: NotebookPen,
      },
    ],
  },

  {
    title: "Personal",

    items: [
      {
        label: "Bookmarks",
        href: "/bookmarks",
        icon: BookMarked,
      },
    ],
  },

  {
    title: "Account",

    items: [
      {
        label: "Profile",
        href: "/profile",
        icon: User,
      },
    ],
  },
];