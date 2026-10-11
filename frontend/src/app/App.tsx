import Layout from "@/app/layout/Layout";
import Curriculum from "@/features/learning/pages/Curriculum";
import Overview from "@/features/learning/pages/Overview";
import { WorkspaceProvider } from "@/features/workspace/WorkspaceProvider";
import { Loading } from "@/shared/components/ui";

import { lazy, Suspense } from "react";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
const TrackDetail = lazy(() => import("@/features/learning/pages/TrackDetail"));
const LessonReader = lazy(
  () => import("@/features/learning/pages/LessonReader"),
);
const StrategyLab = lazy(() => import("@/features/research/pages/StrategyLab"));
const Notebook = lazy(() => import("@/features/notebook/pages/Notebook"));
const Experiments = lazy(() => import("@/features/research/pages/Experiments"));
const Library = lazy(() => import("@/features/references/pages/Library"));
const Resources = lazy(() => import("@/features/references/pages/Resources"));
const ExamRoom = lazy(() => import("@/features/assessments/pages/ExamRoom"));
const Certifications = lazy(
  () => import("@/features/certifications/pages/Certifications"),
);
const CertificateCourse = lazy(
  () => import("@/features/certifications/pages/CertificateCourse"),
);
const CertificateDetail = lazy(
  () => import("@/features/certifications/pages/CertificateDetail"),
);
const VerifyCertificate = lazy(
  () => import("@/features/certifications/pages/VerifyCertificate"),
);
const TradingSimulator = lazy(
  () => import("@/features/simulator/pages/TradingSimulator"),
);
export default function App() {
  return (
    <BrowserRouter>
      <WorkspaceProvider>
        <Suspense fallback={<Loading />}>
          <Routes>
            <Route path="verify" element={<VerifyCertificate />} />
            <Route
              path="verify/:certificateId"
              element={<VerifyCertificate />}
            />
            <Route element={<Layout />}>
              <Route index element={<Overview />} />
              <Route path="curriculum" element={<Curriculum />} />
              <Route path="curriculum/:trackId" element={<TrackDetail />} />
              <Route path="learn/:lessonId" element={<LessonReader />} />
              <Route path="exams/:examId" element={<ExamRoom />} />
              <Route path="certifications" element={<Certifications />} />
              <Route
                path="certifications/course/:trackId"
                element={<CertificateCourse />}
              />
              <Route
                path="certifications/:certificateId"
                element={<CertificateDetail />}
              />
              <Route path="simulator" element={<TradingSimulator />} />
              <Route path="lab" element={<StrategyLab />} />
              <Route path="notebook" element={<Notebook />} />
              <Route path="experiments" element={<Experiments />} />
              <Route path="library" element={<Library />} />
              <Route path="resources" element={<Resources />} />
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
