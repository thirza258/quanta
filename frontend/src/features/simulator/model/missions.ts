/**
 * Which practice mission serves which lesson.
 *
 * Lesson pages need this without waiting on a network call, so the map is held
 * here as well as in the API. `test_trading_missions.py` asserts the two agree,
 * so adding a mission on one side and forgetting the other fails the suite.
 */
export const MISSION_FOR_LESSON: Record<string, string> = {
  "0.4": "first-order",
  "0.5": "first-order",
  "0.7": "position-size",
  "8.1": "earnings-gap",
  "8.2": "earnings-gap",
  "8.3": "read-the-tape",
  "8.4": "read-the-tape",
  "12.13": "charter",
  "12.16": "charter",
};

export const MISSION_TITLES: Record<string, string> = {
  "first-order": "Place your first paper order",
  "position-size": "Size a position you could survive",
  "earnings-gap": "Hold a company through its results",
  "read-the-tape": "Trade what the tape actually said",
  "stop-discipline": "Protect a position before you need to",
  charter: "Trade inside your written limits",
};

export const missionFor = (lessonId: string): string | undefined =>
  MISSION_FOR_LESSON[lessonId];
