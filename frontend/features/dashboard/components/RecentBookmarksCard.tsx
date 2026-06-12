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
      <h3 className="mb-4 font-semibold">
        Recent Bookmarks
      </h3>

      <div className="space-y-3">
        {bookmarks.map(
          (bookmark) => (
            <div
              key={bookmark.id}
              className="rounded-lg border p-3"
            >
              {
                bookmark.topicTitle
              }
            </div>
          )
        )}
      </div>
    </Card>
  );
}