import { Card } from "@/components/ui/card";

type Props = {
  readiness: number;
};

export function ReadinessOverview({
  readiness,
}: Props) {
  return (
    <Card className="p-6">
      <div className="space-y-4">
        <div>
          <p className="text-sm text-muted-foreground">
            Interview Readiness
          </p>

          <h2 className="mt-2 text-5xl font-bold">
            {readiness}%
          </h2>
        </div>

        <div className="h-3 overflow-hidden rounded-full bg-slate-200">
          <div
            className="h-full bg-blue-600"
            style={{
              width: `${readiness}%`,
            }}
          />
        </div>
      </div>
    </Card>
  );
}