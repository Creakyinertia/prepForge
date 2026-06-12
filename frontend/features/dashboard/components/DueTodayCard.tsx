import { Clock3 } from "lucide-react";

import { Card } from "@/components/ui/card";

type Props = {
  count: number;
};

export function DueTodayCard({
  count,
}: Props) {
  return (
    <Card className="h-full p-6">
      <div className="mb-6 flex items-center gap-3">
        <Clock3 className="h-5 w-5 text-amber-500" />

        <h3 className="text-lg font-semibold">
          Due Today
        </h3>
      </div>

      <div>
        <p className="text-5xl font-bold">
          {count}
        </p>

        <p className="mt-2 text-muted-foreground">
          Revisions waiting for review.
        </p>
      </div>

      <div className="mt-8 rounded-xl border border-amber-200 bg-amber-50 p-4">
        <p className="text-sm font-medium">
          Stay consistent.
        </p>

        <p className="mt-1 text-sm text-muted-foreground">
          Completing revisions improves readiness scores.
        </p>
      </div>
    </Card>
  );
}