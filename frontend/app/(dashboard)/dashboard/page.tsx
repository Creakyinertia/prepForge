import {
  BookOpen,
  RefreshCcw,
  Target,
} from "lucide-react";

import { PageContainer } from "@/components/layout/PageContainer";

import { dashboardMockData } from "@/features/dashboard/mock-data";

import { ContinueLearningCard } from "@/features/dashboard/components/ContinueLearningCard";

import { DueTodayCard } from "@/features/dashboard/components/DueTodayCard";

import { MetricCard } from "@/features/dashboard/components/MetricCard";

import { ReadinessOverview } from "@/features/dashboard/components/ReadinessOverview";

import { RecentBookmarksCard } from "@/features/dashboard/components/RecentBookmarksCard";

export default function DashboardPage() {
  return (
    <PageContainer className="max-w-6xl">
      <div className="space-y-8">
        <div>
          <h1 className="text-4xl font-bold">
            Good Afternoon 👋
          </h1>

          <p className="mt-2 text-muted-foreground">
            You're making steady progress.
            Keep the momentum going.
          </p>
        </div>

        <ReadinessOverview
          readiness={
            dashboardMockData.interviewReadiness
          }
        />

        <div className="grid gap-6 md:grid-cols-3">
          <MetricCard
            title="Readiness"
            value="78%"
            description="Overall score"
            icon={Target}
          />

          <MetricCard
            title="Topics Completed"
            value="24"
            description="Topics mastered"
            icon={BookOpen}
          />

          <MetricCard
            title="Due Revisions"
            value="3"
            description="Need attention"
            icon={RefreshCcw}
          />
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <ContinueLearningCard
              topics={
                dashboardMockData.continueLearning
              }
            />
          </div>

          <DueTodayCard count={3} />
        </div>

        <RecentBookmarksCard
          bookmarks={
            dashboardMockData.bookmarks
          }
        />
      </div>
    </PageContainer>
  );
}