import { LucideIcon } from "lucide-react";

import { Card } from "@/components/ui/card";

type Props = {
  title: string;

  value: string | number;

  description?: string;

  icon: LucideIcon;
};

export function MetricCard({
  title,
  value,
  description,
  icon: Icon,
}: Props) {
  return (
    <Card className="p-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-muted-foreground">
            {title}
          </p>

          <h3 className="mt-3 text-3xl font-bold">
            {value}
          </h3>

          {description && (
            <p className="mt-2 text-sm text-muted-foreground">
              {description}
            </p>
          )}
        </div>

        <div className="rounded-xl bg-muted p-3">
          <Icon className="h-5 w-5" />
        </div>
      </div>
    </Card>
  );
}