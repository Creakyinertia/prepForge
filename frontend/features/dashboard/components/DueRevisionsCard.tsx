import { Card } from "@/components/ui/card";

type Props = {
  count: number;
};

export function DueRevisionsCard({
  count,
}: Props) {
  return (
    <Card className="p-6">
      <h3 className="text-sm text-muted-foreground">
        Due Revisions
      </h3>

      <p className="mt-3 text-4xl font-bold">
        {count}
      </p>
    </Card>
  );
}