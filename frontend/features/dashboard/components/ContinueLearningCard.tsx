import { ArrowRight } from "lucide-react";

import { Card } from "@/components/ui/card";

import { ContinueLearningItem } from "../types";

type Props = {
  topics: ContinueLearningItem[];
};

export function ContinueLearningCard({
  topics,
}: Props) {
  return (
    <Card className="h-full p-6">
      <div className="mb-6">
        <h3 className="text-lg font-semibold">
          Continue Learning
        </h3>

        <p className="text-sm text-muted-foreground">
          Resume your most recent topics.
        </p>
      </div>

      <div className="space-y-4">
        {topics.map((topic) => (
          <div
            key={topic.topicId}
            className="flex items-center justify-between rounded-xl border p-4 transition-all hover:bg-muted/50"
          >
            <div>
              <p className="font-medium">
                {topic.title}
              </p>

              <p className="text-sm text-muted-foreground">
                Continue studying
              </p>
            </div>

            <ArrowRight className="h-4 w-4" />
          </div>
        ))}
      </div>
    </Card>
  );
}