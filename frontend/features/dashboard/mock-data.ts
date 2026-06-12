import { DashboardData } from "./types";

export const dashboardMockData: DashboardData =
  {
    interviewReadiness: 78,

    dueRevisions: 3,

    continueLearning: [
      {
        topicId: "1",
        title: "Event Loop",
        slug: "event-loop",
      },

      {
        topicId: "2",
        title: "Closures",
        slug: "closures",
      },

      {
        topicId: "3",
        title: "Promises",
        slug: "promises",
      },
    ],

    bookmarks: [
      {
        id: "1",
        topicTitle: "Event Loop",
        topicSlug: "event-loop",
      },

      {
        id: "2",
        topicTitle: "Caching",
        topicSlug: "caching",
      },
    ],
  };