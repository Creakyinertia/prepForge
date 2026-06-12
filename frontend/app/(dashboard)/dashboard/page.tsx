import { PageContainer } from "@/components/layout/PageContainer";

import { dashboardMockData } from "@/features/dashboard/mock-data";

import { ContinueLearningCard } from "@/features/dashboard/components/ContinueLearningCard";

import { DueRevisionsCard } from "@/features/dashboard/components/DueRevisionsCard";

import { ReadinessOverview } from "@/features/dashboard/components/ReadinessOverview";

import { RecentBookmarksCard } from "@/features/dashboard/components/RecentBookmarksCard";

export default function DashboardPage() {
  return (
    <PageContainer>
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold">
            Dashboard
          </h1>

          <p className="text-muted-foreground">
            Track your interview
            readiness.
          </p>
        </div>

        <ReadinessOverview
          readiness={
            dashboardMockData.interviewReadiness
          }
        />

        <div className="grid gap-6 lg:grid-cols-2">
          <ContinueLearningCard
            topics={
              dashboardMockData.continueLearning
            }
          />

          <DueRevisionsCard
            count={
              dashboardMockData.dueRevisions
            }
          />
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