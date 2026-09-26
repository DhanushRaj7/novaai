import { useEffect, useState } from "react";
import {
  getProcessIntelligence,
  getEnterpriseIntelligence,
  analyzeNewProcess,
} from "./services/api";

type Intelligence = {
  process: {
    id: number;
    name: string;
    description: string;
    priority_score: number;
  };
  roles: Role[];
  activities: Activity[];
  ai_opportunities: Opportunity[];
  initiatives: Initiative[];
  dependencies: Dependency[];
};

type Role = {
  id: number;
  name: string;
  skills: Skill[];
};

type Skill = {
  id: number;
  name: string;
  proficiency: number;
};

type Activity = {
  id: number;
  name: string;
  description: string;
  sequence: number;
  activity_type: string;
  decision_required: boolean;
  ai_opportunities: Opportunity[];
};

type Opportunity = {
  id: number;
  name: string;
  description: string;
  ai_capability: string;
  automation_potential: number;
  human_involvement: number;
  expected_benefit: number;
  feasibility: number;
  strategic_alignment: number;
  risk_level: number;
  priority_score: number;
  reasoning: string;
  governance?: Governance;
  evidence?: Evidence[];
  initiatives?: Initiative[];
  dependencies?: Dependency[];
};

type Governance = {
  id: number;
  overall_risk: number;
  data_risk: number;
  privacy_risk: number;
  bias_risk: number;
  security_risk: number;
  model_risk: number;
  human_oversight: boolean;
  explainability_required: boolean;
};

type Evidence = {
  id: number;
  claim: string;
  excerpt: string;
  relevance: number;
  confidence: number;
  source_id: number;
};

type Initiative = {
  id: number;
  name: string;
  description?: string;
  priority: number;
  status: string;
  relationship?: string;
  relationship_type?: string;
  dependencies?: Dependency[];
};

type Dependency = {
  initiative_id: number;
  name: string;
  dependency_type: string;
  description?: string;
  priority: number;
  status: string;
  dependencies?: Dependency[];
};

type EnterpriseOpportunity = {
  id: number;
  name: string;
  priority_score: number;
  expected_benefit: number;
  feasibility: number;
  risk_level: number;
};

function App() {
  const [intelligence, setIntelligence] =
    useState<Intelligence | null>(null);

  const [enterprise, setEnterprise] =
    useState<any>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [selectedOpportunity, setSelectedOpportunity] =
    useState<Opportunity | null>(null);

  const [selectedProcess, setSelectedProcess] =
    useState<Intelligence | null>(null);
  const [loadingSelectedProcess, setLoadingSelectedProcess] =
    useState(false);
  const [selectedProcessError, setSelectedProcessError] =
    useState("");

  const handleSelectProcess = async (processId: number) => {
    try {
      setLoadingSelectedProcess(true);
      setSelectedProcessError("");
      setSelectedOpportunity(null);

      const processData = await getProcessIntelligence(processId);

      const normalizedData: Intelligence = {
        ...processData,
        roles: (processData.roles ?? []).map((role: Role) => ({
          ...role,
          skills: role.skills ?? [],
        })),
        activities: (processData.activities ?? []).map((activity: Activity) => ({
          ...activity,
          ai_opportunities: activity.ai_opportunities ?? [],
        })),
        ai_opportunities: (processData.ai_opportunities ?? []).map((opportunity: any) => ({
          ...opportunity,
          evidence: (opportunity.evidence ?? []).map((item: any) => ({
            ...item,
            relevance: item.relevance ?? item.relevance_score ?? 0,
            confidence: item.confidence ?? item.confidence_score ?? 0,
          })),
          initiatives: (opportunity.initiatives ?? []).map((initiative: any) => ({
            ...initiative,
            relationship:
              initiative.relationship ??
              initiative.relationship_type ??
              "Supports",
            dependencies: initiative.dependencies ?? [],
          })),
          dependencies: opportunity.dependencies ?? [],
        })),
        initiatives: processData.initiatives ?? [],
        dependencies: processData.dependencies ?? [],
      };

      setSelectedProcess(normalizedData);
    } catch (err) {
      console.error(err);
      setSelectedProcessError(
        err instanceof Error
          ? err.message
          : "Unable to load process intelligence."
      );
    } finally {
      setLoadingSelectedProcess(false);
    }
  };

  const [newProcessName, setNewProcessName] = useState("");
  const [newProcessDescription, setNewProcessDescription] = useState("");
  const [newProcessStage, setNewProcessStage] = useState(5);
  const [analyzingNewProcess, setAnalyzingNewProcess] = useState(false);
  const [newProcessResult, setNewProcessResult] = useState<any>(null);
  const [newProcessError, setNewProcessError] = useState("");

  const handleAnalyzeNewProcess = async () => {
    if (!newProcessName.trim() || !newProcessDescription.trim()) {
      setNewProcessError("Process name and description are required.");
      return;
    }

    try {
      setAnalyzingNewProcess(true);
      setNewProcessError("");
      setNewProcessResult(null);

      const result = await analyzeNewProcess(
        newProcessName.trim(),
        newProcessDescription.trim(),
        newProcessStage
      );

      setNewProcessResult(result);
      setNewProcessName("");
      setNewProcessDescription("");
    } catch (err) {
      console.error(err);
      setNewProcessError(
        err instanceof Error
          ? err.message
          : "Failed to analyze process."
      );
    } finally {
      setAnalyzingNewProcess(false);
    }
  };

  useEffect(() => {
    async function loadData() {
      try {
        // Load process-level intelligence
        const processData = await getProcessIntelligence(1);

        const normalizedData: Intelligence = {
          ...processData,

          roles: (processData.roles ?? []).map(
            (role: Role) => ({
              ...role,
              skills: role.skills ?? [],
            })
          ),

          activities: (processData.activities ?? []).map(
            (activity: Activity) => ({
              ...activity,
              ai_opportunities:
                activity.ai_opportunities ?? [],
            })
          ),

          ai_opportunities: (
            processData.ai_opportunities ?? []
          ).map((opportunity: any) => {
            const evidence = (opportunity.evidence ?? []).map(
              (item: any) => ({
                ...item,
                relevance:
                  item.relevance ??
                  item.relevance_score ??
                  0,
                confidence:
                  item.confidence ??
                  item.confidence_score ??
                  0,
              })
            );

            const initiatives = (
              opportunity.initiatives ?? []
            ).map((initiative: any) => ({
              ...initiative,
              relationship:
                initiative.relationship ??
                initiative.relationship_type ??
                "Supports",
              dependencies:
                initiative.dependencies ?? [],
            }));

            const dependencies =
              opportunity.dependencies ??
              initiatives.flatMap(
                (initiative: Initiative) =>
                  initiative.dependencies ?? []
              );

            return {
              ...opportunity,
              evidence,
              initiatives,
              dependencies,
            };
          }),

          initiatives:
            processData.initiatives ?? [],

          dependencies:
            processData.dependencies ?? [],
        };

        setIntelligence(normalizedData);

        // Load enterprise-level intelligence
        const enterpriseData =
          await getEnterpriseIntelligence();

        setEnterprise(enterpriseData);

        

      } catch (err) {
        console.error(err);
        setError(
          "Unable to load transformation intelligence."
        );
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0b] text-gray-200 flex items-center justify-center">
        <div className="text-center">
          <div className="text-lg font-semibold">
            Loading NovaAI...
          </div>

          <div className="text-sm text-gray-500 mt-2">
            Building transformation intelligence
          </div>
        </div>
      </div>
    );
  }

  if (error || !intelligence) {
    return (
      <div className="min-h-screen bg-[#0a0a0b] text-gray-200 flex items-center justify-center">
        <div className="border border-red-500/20 bg-red-500/5 rounded-xl px-6 py-5">
          <div className="text-red-400 font-semibold">
            Something went wrong
          </div>

          <div className="text-sm text-gray-500 mt-2">
            {error || "No intelligence data available."}
          </div>
        </div>
      </div>
    );
  }

  const process = intelligence.process;

  const roles = intelligence.roles ?? [];

  const activities =
    intelligence.activities ?? [];

  const ai_opportunities =
    activities.flatMap(
      (activity) =>
        activity.ai_opportunities ?? []
    );

  const initiatives: Initiative[] = Array.from(
    new Map<number, Initiative>(
      ai_opportunities
        .flatMap(
          (opportunity) =>
            opportunity.initiatives ?? []
        )
        .map((initiative): [number, Initiative] => [
          initiative.id,
          initiative,
        ])
    ).values()
  );


  const enterpriseOpportunities: EnterpriseOpportunity[] =
  enterprise?.ai_opportunities ?? [];

const rankedEnterpriseOpportunities =
  [...enterpriseOpportunities].sort(
    (a, b) =>
      b.priority_score - a.priority_score
  );

  return (
    <div className="min-h-screen bg-[#0a0a0b] text-gray-200">

      {/* Header */}
      <header className="border-b border-white/5 bg-[#0c0c0e]">
        <div className="max-w-[1500px] mx-auto px-8 py-5 flex items-center justify-between">

          <div>
            <div className="flex items-center gap-3">

              <div className="w-9 h-9 rounded-lg bg-white text-black flex items-center justify-center font-bold">
                N
              </div>

              <div>
                <h1 className="text-lg font-semibold tracking-tight">
                  NovaAI
                </h1>

                <p className="text-xs text-gray-500">
                  Enterprise Transformation Intelligence
                </p>
              </div>

            </div>
          </div>

          <div className="flex items-center gap-3">

            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-emerald-500/20 bg-emerald-500/5">

              <div className="w-2 h-2 rounded-full bg-emerald-400" />

              <span className="text-xs text-emerald-400">
                Intelligence Online
              </span>

            </div>

            <div className="text-sm text-gray-500">
              NovaBank
            </div>

          </div>
        </div>
      </header>

      {/* Main */}
      <main className="max-w-[1500px] mx-auto px-8 py-8">

        {/* Enterprise Intelligence Summary */}
        {enterprise && (
          <section className="mb-8">

            <div className="mb-5">
              <div className="text-xs uppercase tracking-[0.2em] text-gray-500 mb-3">
                Enterprise Intelligence
              </div>

              <h2 className="text-2xl font-semibold tracking-tight text-white">
                NovaBank Transformation Overview
              </h2>

              <p className="text-sm text-gray-500 mt-2">
                Enterprise-wide transformation signals across
                processes, AI opportunities, roles, skills,
                and initiatives.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">

              <Metric
                label="Processes"
                value={
                  enterprise.summary?.process_count ?? 0
                }
                description="Processes analyzed"
              />

              <Metric
                label="AI Opportunities"
                value={
                  enterprise.summary
                    ?.ai_opportunity_count ?? 0
                }
                description="Transformation opportunities"
              />

              <Metric
                label="Roles"
                value={
                  enterprise.summary?.role_count ?? 0
                }
                description="Enterprise roles"
              />

              <Metric
                label="Skills"
                value={
                  enterprise.summary?.skill_count ?? 0
                }
                description="Skills tracked"
              />

              <Metric
                label="Initiatives"
                value={
                  enterprise.summary
                    ?.initiative_count ?? 0
                }
                description="Transformation initiatives"
              />

            </div>

          </section>
        )}

        {/* Surprise Record / New Process Analysis */}
        <section className="mb-8">
          <div className="border border-white/5 bg-[#0d0d10] rounded-2xl overflow-hidden">
            <div className="px-6 py-5 border-b border-white/5">
              <div className="text-xs uppercase tracking-[0.2em] text-gray-600 mb-2">
                Surprise Record Test
              </div>
              <h3 className="font-semibold text-white">
                Analyze a New Process
              </h3>
              <p className="text-xs text-gray-500 mt-1">
                Submit a completely new enterprise process and run the same analysis pipeline dynamically.
              </p>
            </div>

            <div className="p-6">
              <div className="grid grid-cols-12 gap-4">
                <div className="col-span-4">
                  <label className="text-xs text-gray-500">Process name</label>
                  <input
                    value={newProcessName}
                    onChange={(e) => setNewProcessName(e.target.value)}
                    placeholder="e.g. Fraud Investigation"
                    className="mt-2 w-full rounded-lg border border-white/10 bg-black/20 px-3 py-2.5 text-sm text-gray-200 outline-none focus:border-white/20"
                  />
                </div>

                <div className="col-span-5">
                  <label className="text-xs text-gray-500">Description</label>
                  <textarea
                    value={newProcessDescription}
                    onChange={(e) => setNewProcessDescription(e.target.value)}
                    placeholder="Describe what the process does..."
                    rows={3}
                    className="mt-2 w-full resize-none rounded-lg border border-white/10 bg-black/20 px-3 py-2.5 text-sm text-gray-200 outline-none focus:border-white/20"
                  />
                </div>

                <div className="col-span-3">
                  <label className="text-xs text-gray-500">Value chain stage</label>
                  <select
                    value={newProcessStage}
                    onChange={(e) => setNewProcessStage(Number(e.target.value))}
                    className="mt-2 w-full rounded-lg border border-white/10 bg-[#111114] px-3 py-2.5 text-sm text-gray-200 outline-none focus:border-white/20"
                  >
                    <option value={1}>Customer Acquisition</option>
                    <option value={2}>Customer Service</option>
                    <option value={3}>Lending</option>
                    <option value={4}>Payments</option>
                    <option value={5}>Risk & Compliance</option>
                  </select>
                </div>
              </div>

              <div className="mt-4 flex items-center justify-between">
                <div className="text-xs text-red-400">{newProcessError}</div>
                <button
                  onClick={handleAnalyzeNewProcess}
                  disabled={analyzingNewProcess}
                  className="rounded-lg bg-white px-4 py-2.5 text-sm font-medium text-black transition hover:bg-gray-200 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {analyzingNewProcess ? "Analyzing..." : "Analyze Process"}
                </button>
              </div>

              {newProcessResult && (
                <div className="mt-5 rounded-xl border border-emerald-500/10 bg-emerald-500/[0.03] p-5">
                  <div className="flex items-start justify-between gap-6">
                    <div>
                      <div className="text-xs uppercase tracking-widest text-emerald-400/70">
                        Analysis completed
                      </div>
                      <div className="text-base font-medium text-gray-200 mt-2">
                        {newProcessResult.process_name}
                      </div>
                      <div className="text-sm text-gray-500 mt-1">
                        {newProcessResult.summary || "Process analysis completed successfully."}
                      </div>
                    </div>

                    <div className="text-right">
                      <div className="text-[10px] uppercase tracking-widest text-gray-600">
                        Priority
                      </div>
                      <div className="text-3xl font-semibold text-white mt-1">
                        {Math.round((newProcessResult.priority_score ?? 0) * 100)}
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-3 mt-4">
                    <DetailMetric
                      label="Activities created"
                      value={newProcessResult.activities_created ?? 0}
                    />
                    <DetailMetric
                      label="AI opportunities created"
                      value={newProcessResult.ai_opportunities_created ?? 0}
                    />
                  </div>

                  <div className="mt-4 text-xs text-gray-600">
                    Stored as process #{newProcessResult.process_id}. Refresh the dashboard to load the updated enterprise dataset.
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Executive Transformation Priorities */}
<section className="mb-8">
  <div className="border border-white/5 bg-[#0d0d10] rounded-2xl overflow-hidden">

    <div className="px-6 py-5 border-b border-white/5">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-xs uppercase tracking-[0.2em] text-gray-600 mb-2">
            Executive Intelligence
          </div>

          <h3 className="font-semibold text-white">
            Transformation Priorities
          </h3>

          <p className="text-xs text-gray-500 mt-1">
            Enterprise AI opportunities ranked by transformation priority
          </p>
        </div>

        <div className="text-xs text-gray-600">
          {rankedEnterpriseOpportunities.length} opportunities
        </div>
      </div>
    </div>

    <div className="divide-y divide-white/5">

      {rankedEnterpriseOpportunities.map(
        (opportunity, index) => (
          <div
            key={opportunity.id}
            className="px-6 py-5"
          >

            <div className="flex items-center gap-5">

              {/* Rank */}
              <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-xs text-gray-500">
                {index + 1}
              </div>

              {/* Opportunity */}
              <div className="flex-1 min-w-0">

                <div className="font-medium text-gray-200">
                  {opportunity.name}
                </div>

                <div className="flex items-center gap-5 mt-3 text-xs">

                  <span className="text-gray-600">
                    Benefit{" "}
                    <span className="text-gray-400">
                      {Math.round(
                        opportunity.expected_benefit * 100
                      )}
                      %
                    </span>
                  </span>

                  <span className="text-gray-600">
                    Feasibility{" "}
                    <span className="text-gray-400">
                      {Math.round(
                        opportunity.feasibility * 100
                      )}
                      %
                    </span>
                  </span>

                  <span className="text-gray-600">
                    Risk{" "}
                    <span className="text-gray-400">
                      {Math.round(
                        opportunity.risk_level * 100
                      )}
                      %
                    </span>
                  </span>

                </div>

              </div>

              {/* Priority */}
              <div className="w-28 text-right">

                <div className="text-[10px] uppercase tracking-widest text-gray-600">
                  Priority
                </div>

                <div className="text-2xl font-semibold text-white mt-1">
                  {Math.round(
                    opportunity.priority_score * 100
                  )}
                </div>

              </div>

            </div>

            {/* Priority bar */}
            <div className="mt-4 ml-13">

              <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">

                <div
                  className="h-full bg-white/40 rounded-full"
                  style={{
                    width: `${
                      opportunity.priority_score * 100
                    }%`,
                  }}
                />

              </div>

            </div>

          </div>
        )
      )}

    </div>

  </div>
</section>



        {/* Executive Transformation View */}
        {enterprise && (
          <section className="mb-8 space-y-6">
            <div className="border border-white/5 bg-[#0d0d10] rounded-2xl overflow-hidden">
              <div className="px-6 py-5 border-b border-white/5">
                <div className="text-xs uppercase tracking-[0.2em] text-gray-600 mb-2">
                  Executive Intelligence
                </div>
                <h3 className="font-semibold text-white">
                  Enterprise Transformation View
                </h3>
                <p className="text-xs text-gray-500 mt-1">
                  Cross-entity intelligence connecting processes, opportunities, initiatives, roles, skills, and dependencies.
                </p>
              </div>

              <div className="p-6">
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                  {/* Transformation priorities */}
                  <div>
                    <SectionTitle title="Transformation priorities" />
                    <div className="space-y-3">
                      {(enterprise.ranked_processes ?? []).map(
                        (item: any, index: number) => (
                          <button
                            key={item.id}
                            type="button"
                            onClick={() => handleSelectProcess(item.id)}
                            className="w-full text-left rounded-xl border border-white/5 bg-white/[0.015] hover:bg-white/[0.03] hover:border-white/10 transition p-4 cursor-pointer"
                          >
                            <div className="flex items-start gap-4">
                              <div className="w-8 h-8 shrink-0 rounded-lg bg-white/5 flex items-center justify-center text-xs text-gray-500">
                                {index + 1}
                              </div>
                              <div className="min-w-0 flex-1">
                                <div className="flex items-start justify-between gap-4">
                                  <div>
                                    <div className="text-sm font-medium text-gray-200">
                                      {item.name}
                                    </div>
                                    <div className="text-xs text-gray-600 mt-1 line-clamp-2">
                                      {item.description}
                                    </div>
                                  </div>
                                  <div className="text-right shrink-0">
                                    <div className="text-[10px] uppercase tracking-widest text-gray-600">
                                      Priority
                                    </div>
                                    <div className="text-xl font-semibold text-white mt-1">
                                      {Math.round((item.priority_score ?? 0) * 100)}
                                    </div>
                                  </div>
                                </div>
                                <div className="mt-3 h-1.5 bg-white/5 rounded-full overflow-hidden">
                                  <div
                                    className="h-full bg-white/40 rounded-full"
                                    style={{ width: `${(item.priority_score ?? 0) * 100}%` }}
                                  />
                                </div>
                                <div className="flex flex-wrap gap-2 mt-3">
                                  {(item.ai_opportunities ?? []).map((opportunity: any) => (
                                    <span
                                      key={opportunity.id}
                                      className="px-2 py-1 rounded-md bg-purple-500/5 border border-purple-500/10 text-[10px] text-purple-400"
                                    >
                                      {opportunity.name} · {Math.round((opportunity.priority_score ?? 0) * 100)}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            </div>
                          </button>
                        )
                      )}
                    </div>
                  </div>

                  {/* Opportunity landscape */}
                  <div>
                    <SectionTitle title="AI opportunity landscape" />
                    <div className="space-y-3">
                      {(enterprise.ranked_ai_opportunities ?? []).map(
                        (opportunity: any, index: number) => (
                          <div
                            key={opportunity.id}
                            className="rounded-xl border border-white/5 bg-white/[0.015] p-4"
                          >
                            <div className="flex items-center gap-3">
                              <div className="text-xs text-gray-600 w-5">
                                {index + 1}
                              </div>
                              <div className="min-w-0 flex-1">
                                <div className="text-sm text-gray-200 truncate">
                                  {opportunity.name}
                                </div>
                                <div className="flex flex-wrap gap-4 mt-2 text-[11px]">
                                  <span className="text-gray-600">
                                    Benefit <span className="text-gray-400">{Math.round((opportunity.expected_benefit ?? 0) * 100)}%</span>
                                  </span>
                                  <span className="text-gray-600">
                                    Feasibility <span className="text-gray-400">{Math.round((opportunity.feasibility ?? 0) * 100)}%</span>
                                  </span>
                                  <span className="text-gray-600">
                                    Risk <span className="text-gray-400">{Math.round((opportunity.risk_level ?? 0) * 100)}%</span>
                                  </span>
                                </div>
                              </div>
                              <div className="text-right shrink-0">
                                <div className="text-[10px] uppercase tracking-widest text-gray-600">
                                  Priority
                                </div>
                                <div className="text-lg font-semibold text-white mt-1">
                                  {Math.round((opportunity.priority_score ?? 0) * 100)}
                                </div>
                              </div>
                            </div>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Initiative dependency graph */}
            <div className="border border-white/5 bg-[#0d0d10] rounded-2xl overflow-hidden">
              <div className="px-6 py-5 border-b border-white/5">
                <SectionTitle title="Transformation dependencies" />
                <p className="text-xs text-gray-500 -mt-2">
                  Dependency chains show which transformation foundations must exist before downstream initiatives can proceed.
                </p>
              </div>
              <div className="p-6 grid grid-cols-1 xl:grid-cols-3 gap-4">
                {(enterprise.ranked_initiatives ?? []).map((initiative: any) => (
                  <div
                    key={initiative.id}
                    className="rounded-xl border border-white/5 bg-white/[0.015] p-5"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="min-w-0">
                        <div className="text-sm font-medium text-gray-200">
                          {initiative.name}
                        </div>
                        <div className="text-xs text-gray-600 mt-1">
                          {initiative.status}
                        </div>
                      </div>
                      <div className="text-right shrink-0">
                        <div className="text-[10px] uppercase tracking-widest text-gray-600">
                          Priority
                        </div>
                        <div className="text-lg font-semibold text-white mt-1">
                          {Math.round((initiative.priority ?? 0) * 100)}
                        </div>
                      </div>
                    </div>

                    <div className="mt-4">
                      {initiative.dependencies?.length ? (
                        <DependencyList dependencies={initiative.dependencies} />
                      ) : (
                        <div className="rounded-lg border border-white/5 bg-white/[0.02] p-3 text-xs text-gray-600">
                          No upstream dependency.
                        </div>
                      )}
                    </div>

                    {initiative.ai_opportunities?.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-white/5">
                        <div className="text-[10px] uppercase tracking-widest text-gray-600 mb-2">
                          Connected opportunities
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {initiative.ai_opportunities.map((opportunity: any) => (
                            <span
                              key={opportunity.id}
                              className="px-2 py-1 rounded-md bg-white/5 text-[10px] text-gray-500"
                            >
                              {opportunity.name}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Role / skill impact */}
            <div className="border border-white/5 bg-[#0d0d10] rounded-2xl overflow-hidden">
              <div className="px-6 py-5 border-b border-white/5">
                <SectionTitle title="Role and skill impact" />
                <p className="text-xs text-gray-500 -mt-2">
                  Enterprise role-to-skill relationships surfaced from the transformation intelligence graph.
                </p>
              </div>
              <div className="p-6 grid grid-cols-1 xl:grid-cols-2 gap-6">
                <div>
                  <div className="text-[10px] uppercase tracking-widest text-gray-600 mb-3">
                    Roles → skills
                  </div>
                  <div className="space-y-3">
                    {(enterprise.roles ?? []).map((role: any) => (
                      <div
                        key={role.id}
                        className="rounded-xl border border-white/5 bg-white/[0.015] p-4"
                      >
                        <div className="text-sm text-gray-200">
                          {role.name}
                        </div>
                        <div className="flex flex-wrap gap-2 mt-3">
                          {(role.skills ?? []).map((skill: any) => (
                            <span
                              key={skill.id}
                              className="px-2 py-1 rounded-md bg-white/5 text-[10px] text-gray-500"
                            >
                              {skill.name}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-[10px] uppercase tracking-widest text-gray-600 mb-3">
                    Skills → roles
                  </div>
                  <div className="space-y-3">
                    {(enterprise.skills ?? []).map((skill: any) => (
                      <div
                        key={skill.id}
                        className="rounded-xl border border-white/5 bg-white/[0.015] p-4"
                      >
                        <div className="flex items-center justify-between gap-4">
                          <div className="text-sm text-gray-200">
                            {skill.name}
                          </div>
                          <div className="text-[10px] text-gray-600">
                            {(skill.roles ?? []).length} roles
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-2 mt-3">
                          {(skill.roles ?? []).map((role: any) => (
                            <span
                              key={role.id}
                              className="px-2 py-1 rounded-md bg-white/5 text-[10px] text-gray-500"
                            >
                              {role.name}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Intelligence gaps */}
            {(() => {
              const unmapped = (enterprise.ai_opportunities ?? []).filter(
                (opportunity: any) =>
                  !opportunity.initiatives || opportunity.initiatives.length === 0
              );

              return (
                <div className="border border-amber-500/10 bg-amber-500/[0.02] rounded-2xl overflow-hidden">
                  <div className="px-6 py-5 border-b border-amber-500/10">
                    <div className="text-xs uppercase tracking-[0.2em] text-amber-400/60 mb-2">
                      Intelligence Gap
                    </div>
                    <h3 className="font-semibold text-white">
                      AI opportunities without a transformation initiative
                    </h3>
                    <p className="text-xs text-gray-500 mt-1">
                      These opportunities were identified by the analysis pipeline but are not yet connected to a transformation initiative.
                    </p>
                  </div>
                  <div className="p-6">
                    {unmapped.length > 0 ? (
                      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
                        {unmapped.map((opportunity: any) => (
                          <div
                            key={opportunity.id}
                            className="rounded-xl border border-white/5 bg-white/[0.015] p-4"
                          >
                            <div className="text-sm text-gray-300">
                              {opportunity.name}
                            </div>
                            <div className="text-xs text-gray-600 mt-2">
                              Priority {Math.round((opportunity.priority_score ?? 0) * 100)}
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-sm text-gray-600">
                        All current AI opportunities are connected to an initiative.
                      </div>
                    )}
                  </div>
                </div>
              );
            })()}
          </section>
        )}

        {/* Process Header */}
        <section className="mb-8">

          <div className="flex items-start justify-between">

            <div>

              <div className="text-xs uppercase tracking-[0.2em] text-gray-500 mb-3">
                Process Intelligence
              </div>

              <h2 className="text-3xl font-semibold tracking-tight text-white">
                {process.name}
              </h2>

              <p className="max-w-3xl text-gray-500 mt-3 leading-relaxed">
                {process.description}
              </p>

            </div>

            <div className="text-right">

              <div className="text-xs uppercase tracking-widest text-gray-600 mb-2">
                Transformation Priority
              </div>

              <div className="text-5xl font-semibold text-white">
                {(process.priority_score * 100).toFixed(0)}
              </div>

              <div className="text-xs text-gray-500 mt-1">
                / 100 priority score
              </div>

            </div>

          </div>

        </section>

        {/* Process Metrics */}
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">

          <Metric
            label="Activities"
            value={activities.length}
            description="Process activities analyzed"
          />

          <Metric
            label="AI Opportunities"
            value={ai_opportunities.length}
            description="Transformation opportunities"
          />

          <Metric
            label="Affected Roles"
            value={roles.length}
            description="Roles connected to process"
          />

          <Metric
            label="Initiatives"
            value={initiatives.length}
            description="Transformation initiatives"
          />

        </section>

        {/* Main Grid */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-6">

          {/* Left */}
          <div className="lg:col-span-8 space-y-6">

            {/* AI Opportunities */}
            <div className="border border-white/5 bg-[#0d0d10] rounded-2xl overflow-hidden">

              <div className="px-6 py-5 border-b border-white/5">

                <div className="flex items-center justify-between">

                  <div>

                    <h3 className="font-semibold text-white">
                      AI Opportunities
                    </h3>

                    <p className="text-xs text-gray-500 mt-1">
                      Ranked opportunities derived from
                      process analysis
                    </p>

                  </div>

                  <div className="text-xs text-gray-600">
                    {ai_opportunities.length} opportunities
                  </div>

                </div>

              </div>

              <div className="p-4 space-y-3">

                {ai_opportunities.map(
                  (opportunity) => (
                    <OpportunityCard
                      key={opportunity.id}
                      opportunity={opportunity}
                      onClick={() =>
                        setSelectedOpportunity(
                          opportunity
                        )
                      }
                    />
                  )
                )}

              </div>

            </div>

            {/* Activities */}
            <div className="border border-white/5 bg-[#0d0d10] rounded-2xl overflow-hidden">

              <div className="px-6 py-5 border-b border-white/5">

                <h3 className="font-semibold text-white">
                  Process Activities
                </h3>

                <p className="text-xs text-gray-500 mt-1">
                  Activities analyzed for AI
                  transformation potential
                </p>

              </div>

              <div className="divide-y divide-white/5">

                {activities.map((activity) => (

                  <div
                    key={activity.id}
                    className="px-6 py-5 flex items-center justify-between"
                  >

                    <div className="flex items-start gap-4">

                      <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-xs text-gray-500">
                        {activity.sequence}
                      </div>

                      <div>

                        <div className="font-medium text-gray-200">
                          {activity.name}
                        </div>

                        <div className="text-xs text-gray-600 mt-1">
                          {activity.activity_type}
                        </div>

                        <div className="text-sm text-gray-500 mt-2 max-w-2xl">
                          {activity.description}
                        </div>

                      </div>

                    </div>

                    <div className="flex items-center gap-4">

                      {activity.decision_required && (
                        <span className="px-2 py-1 rounded-md bg-amber-500/5 border border-amber-500/10 text-xs text-amber-400">
                          Decision
                        </span>
                      )}

                      <div className="text-xs text-gray-600">
                        {activity.ai_opportunities?.length ?? 0}{" "}
                        AI opportunit
                        {(activity.ai_opportunities?.length ?? 0) !== 1
                          ? "ies"
                          : "y"}
                      </div>

                    </div>

                  </div>

                ))}

              </div>

            </div>

          </div>

          {/* Right */}
          <div className="lg:col-span-4 space-y-6">

            {/* Roles */}
            <div className="border border-white/5 bg-[#0d0d10] rounded-2xl overflow-hidden">

              <div className="px-6 py-5 border-b border-white/5">

                <h3 className="font-semibold text-white">
                  Affected Roles
                </h3>

                <p className="text-xs text-gray-500 mt-1">
                  Roles connected to this process
                </p>

              </div>

              <div className="p-4 space-y-3">

                {roles.map((role) => (

                  <div
                    key={role.id}
                    className="rounded-xl border border-white/5 bg-white/[0.015] p-4"
                  >

                    <div className="font-medium text-gray-200">
                      {role.name}
                    </div>

                    <div className="mt-3 flex flex-wrap gap-2">

                      {role.skills.map((skill) => (

                        <span
                          key={skill.id}
                          className="px-2 py-1 rounded-md bg-white/5 text-[11px] text-gray-500"
                        >
                          {skill.name}
                        </span>

                      ))}

                    </div>

                  </div>

                ))}

              </div>

            </div>

            {/* Initiatives */}
            <div className="border border-white/5 bg-[#0d0d10] rounded-2xl overflow-hidden">

              <div className="px-6 py-5 border-b border-white/5">

                <h3 className="font-semibold text-white">
                  Transformation Initiatives
                </h3>

                <p className="text-xs text-gray-500 mt-1">
                  Strategic actions connected to this
                  process
                </p>

              </div>

              <div className="p-4 space-y-3">

                {initiatives.map((initiative) => (

                  <div
                    key={initiative.id}
                    className="rounded-xl border border-white/5 p-4"
                  >

                    <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">

                      <div className="min-w-0 flex-1">

                        <div className="font-medium text-gray-200 break-words">
                          {initiative.name}
                        </div>

                        {initiative.description && (
                          <div className="text-xs text-gray-500 mt-2 leading-relaxed break-words">
                            {initiative.description}
                          </div>
                        )}

                      </div>

                      <span className="shrink-0 self-start px-2 py-1 rounded-md bg-blue-500/5 border border-blue-500/10 text-xs text-blue-400">
                        {initiative.status}
                      </span>

                    </div>

                    {initiative.dependencies && initiative.dependencies.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-white/5">
                        <div className="text-[10px] uppercase tracking-widest text-gray-600 mb-3">
                          Dependencies
                        </div>

                        <div className="min-w-0 overflow-hidden">
                          <DependencyList dependencies={initiative.dependencies} />
                        </div>
                      </div>
                    )}

                    <div className="mt-4">

                      <div className="flex items-center justify-between text-xs mb-1">

                        <span className="text-gray-600">
                          Priority
                        </span>

                        <span className="text-gray-400">
                          {(initiative.priority * 100).toFixed(0)}
                        </span>

                      </div>

                      <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">

                        <div
                          className="h-full bg-white/40 rounded-full"
                          style={{
                            width: `${
                              initiative.priority * 100
                            }%`,
                          }}
                        />

                      </div>

                    </div>

                  </div>

                ))}

              </div>

            </div>

          </div>

        </section>

      </main>

      {loadingSelectedProcess && (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="rounded-xl border border-white/10 bg-[#0d0d10] px-6 py-5 shadow-2xl">
            <div className="text-sm font-medium text-gray-200">Loading process intelligence...</div>
            <div className="text-xs text-gray-600 mt-2">Retrieving activities, roles, opportunities, governance, and evidence.</div>
          </div>
        </div>
      )}

      {selectedProcessError && !loadingSelectedProcess && (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="rounded-xl border border-red-500/20 bg-[#0d0d10] px-6 py-5 shadow-2xl max-w-md">
            <div className="text-sm font-medium text-red-400">Unable to load process intelligence</div>
            <div className="text-xs text-gray-500 mt-2">{selectedProcessError}</div>
            <button
              type="button"
              onClick={() => setSelectedProcessError("")}
              className="mt-4 rounded-lg bg-white px-4 py-2 text-xs font-medium text-black"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Process Intelligence Drawer */}
      {selectedProcess && (
        <ProcessDrawer
          intelligence={selectedProcess}
          onClose={() => setSelectedProcess(null)}
          onOpportunityClick={(opportunity) => {
            setSelectedProcess(null);
            setSelectedOpportunity(opportunity);
          }}
        />
      )}

      {/* Opportunity Drawer */}
      {selectedOpportunity && (
        <OpportunityDrawer
          opportunity={selectedOpportunity}
          onClose={() =>
            setSelectedOpportunity(null)
          }
        />
      )}

    </div>
  );
}

/* =========================================================
   METRIC
========================================================= */

function Metric({
  label,
  value,
  description,
}: {
  label: string;
  value: number | string;
  description: string;
}) {
  return (
    <div className="border border-white/5 bg-[#0d0d10] rounded-xl p-5">
      <div className="text-xs uppercase tracking-widest text-gray-600">
        {label}
      </div>

      <div className="text-3xl font-semibold text-white mt-3">
        {value}
      </div>

      <div className="text-xs text-gray-600 mt-2">
        {description}
      </div>
    </div>
  );
}

/* =========================================================
   OPPORTUNITY CARD
========================================================= */

function OpportunityCard({
  opportunity,
  onClick,
}: {
  opportunity: Opportunity;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left rounded-xl border border-white/5 bg-white/[0.015] hover:bg-white/[0.03] hover:border-white/10 transition p-5"
    >
      <div className="flex items-start justify-between gap-6">
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h4 className="font-medium text-gray-200">
              {opportunity.name}
            </h4>

            <span className="px-2 py-1 rounded-md bg-purple-500/5 border border-purple-500/10 text-[10px] text-purple-400">
              {opportunity.ai_capability}
            </span>
          </div>

          <p className="text-sm text-gray-500 mt-2 leading-relaxed">
            {opportunity.description}
          </p>

          <div className="flex items-center gap-6 mt-4">
            <Score
              label="Benefit"
              value={opportunity.expected_benefit}
            />

            <Score
              label="Feasibility"
              value={opportunity.feasibility}
            />

            <Score
              label="Automation"
              value={opportunity.automation_potential}
            />

            <Score
              label="Risk"
              value={opportunity.risk_level}
              inverse
            />
          </div>
        </div>

        <div className="text-right">
          <div className="text-[10px] uppercase tracking-widest text-gray-600">
            Priority
          </div>

          <div className="text-3xl font-semibold text-white mt-1">
            {(opportunity.priority_score * 100).toFixed(0)}
          </div>

          <div className="text-[10px] text-gray-600">
            / 100
          </div>
        </div>
      </div>

      <div className="mt-5 pt-4 border-t border-white/5 flex items-center justify-between">
        <div className="text-xs text-gray-600">
          {opportunity.evidence?.length || 0} research evidence item
          {(opportunity.evidence?.length || 0) !== 1 ? "s" : ""}
        </div>

        <div className="text-xs text-gray-500">
          View intelligence →
        </div>
      </div>
    </button>
  );
}

/* =========================================================
   SCORE
========================================================= */

function Score({
  label,
  value,
  inverse = false,
}: {
  label: string;
  value: number;
  inverse?: boolean;
}) {
  const percentage = Math.round(value * 100);

  return (
    <div className="min-w-[70px]">
      <div className="text-[10px] uppercase tracking-widest text-gray-600">
        {label}
      </div>

      <div className="text-sm text-gray-300 mt-1">
        {percentage}
      </div>

      <div className="h-1 bg-white/5 rounded-full mt-1 overflow-hidden">
        <div
          className="h-full bg-white/30 rounded-full"
          style={{
            width: `${percentage}%`,
            opacity: inverse ? 0.5 : 1,
          }}
        />
      </div>
    </div>
  );
}

/* =========================================================
   PROCESS INTELLIGENCE DRAWER
========================================================= */

function ProcessDrawer({
  intelligence,
  onClose,
  onOpportunityClick,
}: {
  intelligence: Intelligence;
  onClose: () => void;
  onOpportunityClick: (opportunity: Opportunity) => void;
}) {
  const activities = intelligence.activities ?? [];

  // The process intelligence API exposes AI opportunities through
  // their activities. Derive the process-level opportunity list from
  // those activity relationships so the executive drill-down stays
  // consistent with the main dashboard.
  const opportunities = Array.from(
    new Map(
      activities
        .flatMap((activity) => activity.ai_opportunities ?? [])
        .map((opportunity) => [opportunity.id, opportunity])
    ).values()
  );

  const roles = intelligence.roles ?? [];
  const initiatives = intelligence.initiatives ?? [];

  return (
    <div className="fixed inset-0 z-50">
      <button
        type="button"
        onClick={onClose}
        className="absolute inset-0 bg-black/60 backdrop-blur-sm cursor-default"
        aria-label="Close process intelligence"
      />

      <aside className="absolute top-0 right-0 h-full w-full max-w-3xl bg-[#0d0d10] border-l border-white/10 shadow-2xl overflow-y-auto">
        <div className="sticky top-0 z-10 bg-[#0d0d10]/95 backdrop-blur border-b border-white/5 px-7 py-5">
          <div className="flex items-start justify-between gap-6">
            <div>
              <div className="text-[10px] uppercase tracking-[0.2em] text-gray-600">
                Process Intelligence
              </div>
              <h2 className="text-xl font-semibold text-white mt-2">
                {intelligence.process.name}
              </h2>
              <p className="text-xs text-gray-500 mt-2 max-w-2xl leading-relaxed">
                {intelligence.process.description}
              </p>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="w-9 h-9 shrink-0 rounded-lg border border-white/5 bg-white/[0.02] text-gray-500 hover:text-white hover:bg-white/5 transition"
            >
              ✕
            </button>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-5">
            <DetailMetric
              label="Priority"
              value={`${Math.round((intelligence.process.priority_score ?? 0) * 100)}/100`}
            />
            <DetailMetric label="Activities" value={activities.length} />
            <DetailMetric label="AI opportunities" value={opportunities.length} />
            <DetailMetric label="Affected roles" value={roles.length} />
          </div>
        </div>

        <div className="p-7 space-y-8">
          <section>
            <SectionTitle title="AI opportunities" />
            {opportunities.length > 0 ? (
              <div className="space-y-3">
                {opportunities
                  .slice()
                  .sort((a, b) => (b.priority_score ?? 0) - (a.priority_score ?? 0))
                  .map((opportunity) => (
                    <button
                      type="button"
                      key={opportunity.id}
                      onClick={() => onOpportunityClick(opportunity)}
                      className="w-full text-left rounded-xl border border-white/5 bg-white/[0.015] hover:bg-white/[0.03] hover:border-white/10 transition p-5"
                    >
                      <div className="flex items-start justify-between gap-5">
                        <div className="min-w-0">
                          <div className="text-sm font-medium text-gray-200">
                            {opportunity.name}
                          </div>
                          <div className="text-xs text-gray-600 mt-2 leading-relaxed">
                            {opportunity.description}
                          </div>
                          <div className="flex flex-wrap gap-4 mt-3 text-[11px]">
                            <span className="text-gray-600">
                              Benefit <span className="text-gray-400">{Math.round((opportunity.expected_benefit ?? 0) * 100)}%</span>
                            </span>
                            <span className="text-gray-600">
                              Feasibility <span className="text-gray-400">{Math.round((opportunity.feasibility ?? 0) * 100)}%</span>
                            </span>
                            <span className="text-gray-600">
                              Risk <span className="text-gray-400">{Math.round((opportunity.risk_level ?? 0) * 100)}%</span>
                            </span>
                          </div>
                        </div>
                        <div className="text-right shrink-0">
                          <div className="text-[10px] uppercase tracking-widest text-gray-600">
                            Priority
                          </div>
                          <div className="text-2xl font-semibold text-white mt-1">
                            {Math.round((opportunity.priority_score ?? 0) * 100)}
                          </div>
                          <div className="text-[10px] text-gray-600 mt-1">
                            View intelligence →
                          </div>
                        </div>
                      </div>
                    </button>
                  ))}
              </div>
            ) : (
              <div className="rounded-xl border border-white/5 bg-white/[0.015] p-5 text-sm text-gray-600">
                No AI opportunities identified.
              </div>
            )}
          </section>

          <section>
            <SectionTitle title="Process activities" />
            <div className="rounded-xl border border-white/5 bg-white/[0.015] overflow-hidden">
              <div className="divide-y divide-white/5">
                {activities.map((activity) => (
                  <div key={activity.id} className="px-5 py-4">
                    <div className="flex items-start gap-4">
                      <div className="w-8 h-8 shrink-0 rounded-lg bg-white/5 flex items-center justify-center text-xs text-gray-500">
                        {activity.sequence}
                      </div>
                      <div className="min-w-0 flex-1">
                        <div className="flex items-start justify-between gap-4">
                          <div>
                            <div className="text-sm font-medium text-gray-200">
                              {activity.name}
                            </div>
                            <div className="text-xs text-gray-600 mt-1">
                              {activity.activity_type}
                            </div>
                          </div>
                          {activity.decision_required && (
                            <span className="shrink-0 px-2 py-1 rounded-md bg-amber-500/5 border border-amber-500/10 text-[10px] text-amber-400">
                              Decision
                            </span>
                          )}
                        </div>
                        <div className="text-xs text-gray-500 mt-2 leading-relaxed">
                          {activity.description}
                        </div>
                        {activity.ai_opportunities?.length > 0 && (
                          <div className="flex flex-wrap gap-2 mt-3">
                            {activity.ai_opportunities.map((opportunity) => (
                              <button
                                type="button"
                                key={opportunity.id}
                                onClick={() => onOpportunityClick(opportunity)}
                                className="px-2 py-1 rounded-md bg-purple-500/5 border border-purple-500/10 text-[10px] text-purple-400 hover:bg-purple-500/10 transition"
                              >
                                {opportunity.name}
                              </button>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section>
            <SectionTitle title="Affected roles and skills" />
            {roles.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {roles.map((role) => (
                  <div key={role.id} className="rounded-xl border border-white/5 bg-white/[0.015] p-4">
                    <div className="text-sm font-medium text-gray-200">{role.name}</div>
                    <div className="flex flex-wrap gap-2 mt-3">
                      {(role.skills ?? []).map((skill) => (
                        <span key={skill.id} className="px-2 py-1 rounded-md bg-white/5 text-[10px] text-gray-500">
                          {skill.name}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="rounded-xl border border-white/5 bg-white/[0.015] p-5 text-sm text-gray-600">
                No affected roles identified.
              </div>
            )}
          </section>

          <section>
            <SectionTitle title="Transformation initiatives" />
            {initiatives.length > 0 ? (
              <div className="space-y-3">
                {initiatives.map((initiative) => (
                  <div key={initiative.id} className="rounded-xl border border-white/5 bg-white/[0.015] p-5">
                    <div className="flex items-start justify-between gap-4">
                      <div className="min-w-0">
                        <div className="text-sm font-medium text-gray-200">{initiative.name}</div>
                        {initiative.description && (
                          <div className="text-xs text-gray-500 mt-2 leading-relaxed">{initiative.description}</div>
                        )}
                      </div>
                      <span className="shrink-0 px-2 py-1 rounded-md bg-blue-500/5 border border-blue-500/10 text-[10px] text-blue-400">
                        {initiative.status}
                      </span>
                    </div>
                    <div className="mt-4">
                      <div className="flex items-center justify-between text-[11px] mb-2">
                        <span className="text-gray-600">Priority</span>
                        <span className="text-gray-400">{Math.round((initiative.priority ?? 0) * 100)}</span>
                      </div>
                      <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                        <div className="h-full bg-white/40 rounded-full" style={{ width: `${(initiative.priority ?? 0) * 100}%` }} />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="rounded-xl border border-white/5 bg-white/[0.015] p-5 text-sm text-gray-600">
                No transformation initiatives linked.
              </div>
            )}
          </section>
        </div>
      </aside>
    </div>
  );
}

/* =========================================================
   OPPORTUNITY DRAWER
========================================================= */

function OpportunityDrawer({
  opportunity,
  onClose,
}: {
  opportunity: Opportunity;
  onClose: () => void;
}) {
  const governance = opportunity.governance;

  const dependencies = (
    opportunity.dependencies &&
    opportunity.dependencies.length > 0
      ? opportunity.dependencies
      : (opportunity.initiatives ?? []).flatMap(
          (initiative) => initiative.dependencies ?? []
        )
  );

  return (
    <div className="fixed inset-0 z-50">
      {/* Backdrop */}
      <button
        onClick={onClose}
        className="absolute inset-0 bg-black/60 backdrop-blur-sm cursor-default"
        aria-label="Close opportunity details"
      />

      {/* Drawer */}
      <aside className="absolute top-0 right-0 h-full w-full max-w-2xl bg-[#0d0d10] border-l border-white/10 shadow-2xl overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 z-10 bg-[#0d0d10]/95 backdrop-blur border-b border-white/5 px-7 py-5">
          <div className="flex items-start justify-between gap-6">
            <div>
              <div className="text-[10px] uppercase tracking-[0.2em] text-gray-600">
                AI Opportunity
              </div>

              <h2 className="text-xl font-semibold text-white mt-2">
                {opportunity.name}
              </h2>

              <div className="text-xs text-gray-500 mt-2">
                {opportunity.ai_capability}
              </div>
            </div>

            <button
              onClick={onClose}
              className="w-9 h-9 rounded-lg border border-white/5 bg-white/[0.02] text-gray-500 hover:text-white hover:bg-white/5 transition"
            >
              ✕
            </button>
          </div>
        </div>

        <div className="p-7 space-y-8">
          {/* What could change? */}
          <section>
            <SectionTitle title="What could change?" />

            <div className="rounded-xl border border-white/5 bg-white/[0.015] p-5">
              <p className="text-sm text-gray-400 leading-relaxed">
                {opportunity.description}
              </p>
            </div>
          </section>

          {/* Transformation Assessment */}
          <section>
            <SectionTitle title="Transformation assessment" />

            <div className="grid grid-cols-2 gap-3">
              <DetailMetric
                label="Priority"
                value={`${Math.round(
                  opportunity.priority_score * 100
                )}/100`}
              />

              <DetailMetric
                label="Expected benefit"
                value={`${Math.round(
                  opportunity.expected_benefit * 100
                )}%`}
              />

              <DetailMetric
                label="Feasibility"
                value={`${Math.round(
                  opportunity.feasibility * 100
                )}%`}
              />

              <DetailMetric
                label="Automation potential"
                value={`${Math.round(
                  opportunity.automation_potential * 100
                )}%`}
              />
            </div>
          </section>

          {/* AI Reasoning */}
          <section>
            <SectionTitle title="AI reasoning" />

            <div className="rounded-xl border border-white/5 bg-white/[0.015] p-5">
              <p className="text-sm text-gray-400 leading-relaxed">
                {opportunity.reasoning}
              </p>
            </div>
          </section>

          {/* Governance */}
          {governance && (
            <section>
              <SectionTitle title="Governance assessment" />

              <div className="rounded-xl border border-white/5 bg-white/[0.015] p-5 space-y-5">
                <div className="flex items-center justify-between pb-4 border-b border-white/5">
                  <div>
                    <div className="text-xs text-gray-600">
                      Overall risk
                    </div>

                    <div className="text-2xl font-semibold text-white mt-1">
                      {Math.round(governance.overall_risk * 100)}%
                    </div>
                  </div>

                  <div className="px-3 py-1.5 rounded-lg bg-amber-500/5 border border-amber-500/10 text-xs text-amber-400">
                    Governance review
                  </div>
                </div>

                <div className="space-y-4">
                  <RiskRow
                    label="Data risk"
                    value={governance.data_risk}
                  />

                  <RiskRow
                    label="Privacy risk"
                    value={governance.privacy_risk}
                  />

                  <RiskRow
                    label="Bias / fairness"
                    value={governance.bias_risk}
                  />

                  <RiskRow
                    label="Security risk"
                    value={governance.security_risk}
                  />

                  <RiskRow
                    label="Model risk"
                    value={governance.model_risk}
                  />
                </div>

                <div className="pt-4 border-t border-white/5 grid grid-cols-2 gap-3">
                  <div className="rounded-lg bg-white/[0.02] p-3">
                    <div className="text-[10px] uppercase tracking-widest text-gray-600">
                      Human oversight
                    </div>

                    <div className="text-sm text-gray-300 mt-2">
                      {governance.human_oversight
                        ? "Required"
                        : "Not required"}
                    </div>
                  </div>

                  <div className="rounded-lg bg-white/[0.02] p-3">
                    <div className="text-[10px] uppercase tracking-widest text-gray-600">
                      Explainability
                    </div>

                    <div className="text-sm text-gray-300 mt-2">
                      {governance.explainability_required
                        ? "Required"
                        : "Not required"}
                    </div>
                  </div>
                </div>
              </div>
            </section>
          )}

          {/* Evidence */}
          <section>
            <SectionTitle title="Research evidence" />

            {opportunity.evidence &&
            opportunity.evidence.length > 0 ? (
              <div className="space-y-3">
                {opportunity.evidence.map((evidence) => (
                  <div
                    key={evidence.id}
                    className="rounded-xl border border-white/5 bg-white/[0.015] p-5"
                  >
                    <div className="text-sm text-gray-300 font-medium">
                      {evidence.claim}
                    </div>

                    <div className="mt-3 text-sm text-gray-500 leading-relaxed">
                      {evidence.excerpt}
                    </div>

                    <div className="mt-4 flex items-center gap-4 text-[11px]">
                      <span className="text-gray-600">
                        Relevance:{" "}
                        <span className="text-gray-400">
                          {Math.round(evidence.relevance * 100)}%
                        </span>
                      </span>

                      <span className="text-gray-600">
                        Confidence:{" "}
                        <span className="text-gray-400">
                          {Math.round(evidence.confidence * 100)}%
                        </span>
                      </span>

                      <span className="text-gray-700">
                        Source #{evidence.source_id}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="rounded-xl border border-white/5 bg-white/[0.015] p-5 text-sm text-gray-600">
                No research evidence available.
              </div>
            )}
          </section>

          {/* Transformation Initiative */}
          <section>
            <SectionTitle title="Transformation initiative" />

            {opportunity.initiatives &&
            opportunity.initiatives.length > 0 ? (
              <div className="space-y-3">
                {opportunity.initiatives.map((initiative) => (
                  <div
                    key={initiative.id}
                    className="rounded-xl border border-white/5 bg-white/[0.015] p-5"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <div className="font-medium text-gray-200">
                          {initiative.name}
                        </div>

                        {initiative.description && (
                          <p className="text-xs text-gray-500 mt-2 leading-relaxed">
                            {initiative.description}
                          </p>
                        )}
                      </div>

                      <span className="px-2 py-1 rounded-md bg-blue-500/5 border border-blue-500/10 text-xs text-blue-400">
                        {initiative.status}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-3 mt-4">
                      <DetailMetric
                        label="Priority"
                        value={`${Math.round(
                          initiative.priority * 100
                        )}/100`}
                      />

                      <DetailMetric
                        label="Relationship"
                        value={
                          initiative.relationship || initiative.relationship_type || "Supports"
                        }
                        text
                      />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="rounded-xl border border-white/5 bg-white/[0.015] p-5 text-sm text-gray-600">
                No transformation initiative linked.
              </div>
            )}
          </section>

          {/* Dependencies */}
          <section>
            <SectionTitle title="Transformation dependencies" />

            {dependencies.length > 0 ? (
              <div className="rounded-xl border border-white/5 bg-white/[0.015] p-5">
                <DependencyList
                  dependencies={dependencies}
                  depth={0}
                />
              </div>
            ) : (
              <div className="rounded-xl border border-white/5 bg-white/[0.015] p-5 text-sm text-gray-600">
                No transformation dependencies identified.
              </div>
            )}
          </section>
        </div>
      </aside>
    </div>
  );
}

/* =========================================================
   SECTION TITLE
========================================================= */

function SectionTitle({ title }: { title: string }) {
  return (
    <div className="flex items-center gap-3 mb-4">
      <div className="w-1 h-4 rounded-full bg-white/40" />

      <h3 className="text-xs uppercase tracking-[0.16em] text-gray-500">
        {title}
      </h3>
    </div>
  );
}

/* =========================================================
   DETAIL METRIC
========================================================= */

function DetailMetric({
  label,
  value,
  text = false,
}: {
  label: string;
  value: number | string;
  text?: boolean;
}) {
  return (
    <div className="rounded-lg border border-white/5 bg-white/[0.02] p-4">
      <div className="text-[10px] uppercase tracking-widest text-gray-600">
        {label}
      </div>

      <div
        className={`mt-2 ${
          text
            ? "text-sm text-gray-300"
            : "text-xl font-semibold text-white"
        }`}
      >
        {value}
      </div>
    </div>
  );
}

/* =========================================================
   RISK ROW
========================================================= */

function RiskRow({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  const percentage = Math.round(value * 100);

  return (
    <div>
      <div className="flex items-center justify-between text-xs mb-2">
        <span className="text-gray-500">{label}</span>

        <span className="text-gray-400">
          {percentage}%
        </span>
      </div>

      <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
        <div
          className="h-full bg-white/30 rounded-full"
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>
    </div>
  );
}

/* =========================================================
   DEPENDENCY LIST
========================================================= */

function DependencyList({
  dependencies,
  depth = 0,
}: {
  dependencies: Dependency[];
  depth?: number;
}) {
  return (
    <div className="space-y-3">
      {dependencies.map((dependency, index) => (
        <div
          key={`${dependency.initiative_id}-${index}`}
          className="relative"
          style={{
            marginLeft: `${depth * 20}px`,
          }}
        >
          <div className="rounded-lg border border-white/5 bg-white/[0.02] p-4 min-w-0 overflow-hidden">
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
              <div className="min-w-0 flex-1">
                <div className="text-sm text-gray-300 break-words">
                  {dependency.name}
                </div>

                <div className="text-xs text-gray-600 mt-1 break-words">
                  {dependency.dependency_type}
                </div>
              </div>

              <span className="shrink-0 self-start text-[10px] uppercase tracking-wider text-gray-600">
                {dependency.status}
              </span>
            </div>

            {dependency.description && (
              <div className="text-xs text-gray-600 mt-3 leading-relaxed break-words">
                {dependency.description}
              </div>
            )}

            <div className="flex items-center gap-4 mt-3 text-[11px] text-gray-600">
              <span>
                Priority:{" "}
                <span className="text-gray-400">
                  {Math.round(dependency.priority * 100)}
                </span>
              </span>
            </div>
          </div>

          {dependency.dependencies &&
            dependency.dependencies.length > 0 && (
              <div className="mt-3 pl-4 border-l border-white/5">
                <DependencyList
                  dependencies={dependency.dependencies}
                  depth={depth + 1}
                />
              </div>
            )}
        </div>
      ))}
    </div>
  );
}

export default App;