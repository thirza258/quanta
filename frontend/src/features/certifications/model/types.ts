export type Certificate = {
  id: string;
  trackId: string;
  courseTitle: string;
  recipientName: string;
  issuedAt: string;
  lessonIds: string[];
  examVersions: Record<string, number>;
  studyMinutes: number;
};
