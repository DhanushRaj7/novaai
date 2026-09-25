const API_BASE_URL = "http://127.0.0.1:8000";

export async function getProcessIntelligence(processId: number) {
  const response = await fetch(
    `${API_BASE_URL}/processes/${processId}/intelligence`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch process intelligence: ${response.status}`
    );
  }

  return response.json();
}

export async function getEnterpriseIntelligence() {
  const response = await fetch(
    `${API_BASE_URL}/intelligence/enterprise`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch enterprise intelligence: ${response.status}`
    );
  }

  return response.json();
}



export async function analyzeNewProcess(
  name: string,
  description: string,
  valueChainStageId: number
) {
  const response = await fetch(
    `${API_BASE_URL}/processes/analyze-new`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        description,
        value_chain_stage_id: valueChainStageId,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      `Failed to analyze new process: ${response.status}`
    );
  }

  return response.json();
}