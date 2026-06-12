import { Card } from "@/components/ui/card";

import { ContinueLearningItem } from "../types";

type Props = {
  topics: ContinueLearningItem[];
};

export function ContinueLearningCard({
  topics,
}: Props) {
  return (
    <Card className="p-6">
      <h3 className="mb-4 font-semibold">
        Continue Learning
      </h3>

      <div className="space-y-3">
        {topics.map((topic) => (
          <div
            key={topic.topicId}
            className="rounded-lg border p-3"
          >
            {topic.title}
          </div>
        ))}
      </div>
    </Card>
  );
}