import {
  ArrowRight,
  TrendingUp,
} from "lucide-react";

import { Card } from "@/components/ui/card";

type Props = {
  readiness: number;
};

export function ReadinessOverview({
  readiness,
}: Props) {
  return (
    <Card className="overflow-hidden border-0 bg-gradient-to-r from-blue-600 to-blue-500 text-white">
      <div className="p-8">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm text-blue-100">
              Interview Readiness
            </p>

            <div className="mt-2 flex items-center gap-3">
              <h2 className="text-6xl font-bold">
                {readiness}%
              </h2>

              <TrendingUp className="h-8 w-8" />
            </div>

            <p className="mt-3 max-w-xl text-blue-100">
              You're making steady progress toward your next interview.
            </p>
          </div>

          <button className="flex items-center gap-2 rounded-xl bg-white/15 px-4 py-2 text-sm backdrop-blur">
            Continue Learning
            <ArrowRight className="h-4 w-4" />
          </button>
        </div>

        <div className="mt-8 grid gap-6 md:grid-cols-3">
          <div>
            <div className="mb-2 flex justify-between text-sm">
              <span>JavaScript</span>
              <span>85%</span>
            </div>

            <div className="h-2 rounded-full bg-white/20">
              <div className="h-full w-[85%] rounded-full bg-white" />
            </div>
          </div>

          <div>
            <div className="mb-2 flex justify-between text-sm">
              <span>React</span>
              <span>72%</span>
            </div>

            <div className="h-2 rounded-full bg-white/20">
              <div className="h-full w-[72%] rounded-full bg-white" />
            </div>
          </div>

          <div>
            <div className="mb-2 flex justify-between text-sm">
              <span>System Design</span>
              <span>55%</span>
            </div>

            <div className="h-2 rounded-full bg-white/20">
              <div className="h-full w-[55%] rounded-full bg-white" />
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}