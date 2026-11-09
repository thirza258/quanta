import {
  ExperimentComposer,
  SubmitFailure,
  type ComposerSubmit,
} from "@/features/research/components/registry/ExperimentComposer";
import {
  formFromSpec,
  readLabPrefill,
  specFromLab,
} from "@/features/research/model/grid";
import {
  researchApi,
  type ExperimentDetail,
  type ResearchOptions,
} from "@/features/research/model/registry";
import "@/features/research/research-registry.css";
import { ApiError } from "@/shared/api/client";
import { EmptyState, Loading } from "@/shared/components/ui";
import {
  ArrowLeft,
  CloudOff,
  FlaskConical,
  LoaderCircle,
  RotateCcw,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import {
  Link,
  useLocation,
  useNavigate,
  useSearchParams,
} from "react-router-dom";

type Loaded =
  | { status: "loading" }
  | { status: "error"; message: string; missing: boolean }
  | {
      status: "ready";
      options: ResearchOptions;
      experiment: ExperimentDetail | null;
    };

export default function NewExperiment() {
  const [params] = useSearchParams();
  const editId = params.get("edit");
  const location = useLocation();
  const navigate = useNavigate();
  // Router state from the strategy lab, read once: later navigation clears it.
  const [prefill] = useState(() => readLabPrefill(location.state));
  const [loaded, setLoaded] = useState<Loaded>({ status: "loading" });
  const [attempt, setAttempt] = useState(0);
  const [loadedFor, setLoadedFor] = useState(editId);
  if (loadedFor !== editId) {
    setLoadedFor(editId);
    setLoaded({ status: "loading" });
  }

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      researchApi.options(),
      editId ? researchApi.get(editId) : Promise.resolve(null),
    ])
      .then(([options, experiment]) => {
        if (!cancelled) setLoaded({ status: "ready", options, experiment });
      })
      .catch((error: Error) => {
        if (!cancelled)
          setLoaded({
            status: "error",
            message: error.message,
            missing: error instanceof ApiError && error.status === 404,
          });
      });
    return () => {
      cancelled = true;
    };
  }, [editId, attempt]);

  const initial = useMemo(() => {
    if (loaded.status !== "ready") return null;
    const { options, experiment } = loaded;
    if (experiment)
      return formFromSpec(
        experiment.spec,
        experiment.title,
        experiment.hypothesis,
      );
    if (prefill)
      return formFromSpec(
        specFromLab(
          prefill.code,
          prefill.config,
          options.defaults,
          prefill.title,
          options.limits.parameters,
        ),
        prefill.title?.slice(0, options.limits.title) ?? "",
      );
    return formFromSpec(options.defaults);
  }, [loaded, prefill]);

  const experiment = loaded.status === "ready" ? loaded.experiment : null;
  const submit: ComposerSubmit = async ({ title, hypothesis, spec }, run) => {
    if (!experiment) {
      const created = await researchApi.create({
        title,
        hypothesis,
        spec,
        run,
      });
      navigate(`/research/${created.id}`);
      return;
    }
    await researchApi.update(experiment.id, {
      title,
      spec,
      // A locked hypothesis is never sent: the server refuses any change to it.
      ...(experiment.hypothesis_locked ? {} : { hypothesis }),
    });
    if (run) {
      try {
        await researchApi.run(experiment.id);
      } catch (error) {
        throw new SubmitFailure({
          message: `Your changes were saved, but the run did not start: ${(error as Error).message}`,
          link: {
            to: `/research/${experiment.id}`,
            label: "Open the experiment",
          },
        });
      }
    }
    navigate(`/research/${experiment.id}`);
  };

  const back = editId ? (
    <Link className="text-link back-link" to={`/research/${editId}`}>
      <ArrowLeft size={15} />
      {experiment
        ? `Experiment #${experiment.number}`
        : "Back to the experiment"}
    </Link>
  ) : (
    <Link className="text-link back-link" to="/research">
      <ArrowLeft size={15} />
      Experiment registry
    </Link>
  );

  return (
    <div className="page registry-page">
      {back}
      <div className="page-eyebrow">
        <span className="green-dot" />
        {editId
          ? `EDIT EXPERIMENT${experiment ? ` #${experiment.number}` : ""}`
          : "NEW EXPERIMENT"}
      </div>
      <h1>
        {experiment
          ? experiment.title
          : editId
            ? "Edit the experiment"
            : "Register a hypothesis, then try to break it."}
      </h1>
      <p className="page-subtitle">
        {editId
          ? "Change the specification and run it again. Every run keeps a frozen copy of what it ran, so earlier results stay comparable."
          : "Five short sections. The hypothesis is timestamped before any result exists, and every setting is stored so the run can be reproduced."}
      </p>
      {loaded.status === "loading" ? (
        <Loading
          label={editId ? "Loading the experiment…" : "Preparing the composer…"}
        />
      ) : loaded.status === "error" ? (
        <div role="alert">
          <EmptyState
            icon={<CloudOff size={28} />}
            title={
              loaded.missing
                ? "This experiment isn’t in your registry."
                : "The research registry is unavailable."
            }
            description={loaded.message}
          >
            <div className="registry-empty-actions">
              {loaded.missing ? null : (
                <button
                  type="button"
                  className="button secondary"
                  onClick={() => {
                    setLoaded({ status: "loading" });
                    setAttempt((n) => n + 1);
                  }}
                >
                  <RotateCcw size={15} />
                  Try again
                </button>
              )}
              <Link className="button secondary" to="/research">
                Back to the registry
              </Link>
            </div>
          </EmptyState>
        </div>
      ) : initial ? (
        <>
          {experiment?.active ? (
            <p className="registry-note" role="status">
              <LoaderCircle size={14} className="spin" aria-hidden="true" />A
              run is in progress for this experiment. You can save changes now
              and start the next run once it finishes.
            </p>
          ) : null}
          {!experiment && prefill ? (
            <p className="registry-note">
              <FlaskConical size={14} aria-hidden="true" />
              Prefilled from the strategy lab
              {prefill.title ? `: “${prefill.title}”` : ""}. The code, market
              and costs are copied; write the hypothesis before you run it.
            </p>
          ) : null}
          <ExperimentComposer
            key={experiment?.id ?? "new"}
            options={loaded.options}
            initial={initial}
            editing={
              experiment
                ? {
                    number: experiment.number,
                    hypothesisLocked: experiment.hypothesis_locked,
                    registeredAt: experiment.hypothesis_registered_at,
                    active: experiment.active,
                  }
                : undefined
            }
            onSubmit={submit}
          />
        </>
      ) : null}
    </div>
  );
}
