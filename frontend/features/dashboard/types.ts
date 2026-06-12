export type ContinueLearningItem = {
  topicId: string;

  title: string;

  slug: string;
};

export type BookmarkItem = {
  id: string;

  topicTitle: string;

  topicSlug: string;
};

export type DashboardData = {
  interviewReadiness: number;

  continueLearning: ContinueLearningItem[];

  dueRevisions: number;

  bookmarks: BookmarkItem[];
};