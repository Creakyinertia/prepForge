import { BookMarked } from "lucide-react";

import { Card } from "@/components/ui/card";

import { BookmarkItem } from "../types";

type Props = {
  bookmarks: BookmarkItem[];
};

export function RecentBookmarksCard({
  bookmarks,
}: Props) {
  return (
    <Card className="p-6">
      <div className="mb-4">
        <h3 className="font-semibold">
          Recent Bookmarks
        </h3>

        <p className="text-sm text-muted-foreground">
          Saved topics for later review.
        </p>
      </div>

      <div className="space-y-3">
        {bookmarks.map((bookmark) => (
          <div
            key={bookmark.id}
            className="flex items-center gap-3 rounded-xl border p-4"
          >
            <BookMarked className="h-4 w-4" />

            <span>
              {bookmark.topicTitle}
            </span>
          </div>
        ))}
      </div>
    </Card>
  );
}