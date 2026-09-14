import { lazy, Suspense } from "react";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import { WorkspaceProvider } from "./lib/workspace";
import Layout from "./components/Layout";
import Overview, { Curriculum } from "./components/Overview";
import { Loading } from "./components/ui";
const TrackDetail = lazy(() => import("./components/TrackDetail"));
const LessonReader = lazy(() => import("./components/LessonReader"));
const StrategyLab = lazy(() => import("./components/StrategyLab"));
const Notebook = lazy(() => import("./components/Notebook"));
const Experiments = lazy(() => import("./components/Experiments"));
const Library = lazy(() => import("./components/Library"));
const ExamRoom = lazy(() => import("./components/ExamRoom"));
const TradingSimulator = lazy(
  () => import("./components/simulator/TradingSimulator"),
);
export default function App() {
  return (
    <BrowserRouter>
      <WorkspaceProvider>
        <Suspense fallback={<Loading />}>
          <Routes>
            <Route element={<Layout />}>
              <Route index element={<Overview />} />
              <Route path="curriculum" element={<Curriculum />} />
              <Route path="curriculum/:trackId" element={<TrackDetail />} />
              <Route path="learn/:lessonId" element={<LessonReader />} />
              <Route path="exams/:examId" element={<ExamRoom />} />
              <Route path="simulator" element={<TradingSimulator />} />
              <Route path="lab" element={<StrategyLab />} />
              <Route path="notebook" element={<Notebook />} />
              <Route path="experiments" element={<Experiments />} />
              <Route path="library" element={<Library />} />
              <Route path="methodology" element={<Library />} />
              <Route
                path="*"
                element={
                  <div className="page">
                    <h1>This page is outside the curriculum.</h1>
                    <p className="page-subtitle">
                      Return to your workspace and pick up a new idea.
                    </p>
                    <Link className="button primary" to="/">
                      Back to overview
                    </Link>
                  </div>
                }
              />
            </Route>
          </Routes>
        </Suspense>
      </WorkspaceProvider>
    </BrowserRouter>
  );
}
