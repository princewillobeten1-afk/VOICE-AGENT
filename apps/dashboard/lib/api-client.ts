export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/v1";

export type AuthTokens = {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
};

export type AuthResponse = {
  user: { id: string; name: string; display_name?: string | null; email: string };
  organization: { id: string; name: string; slug: string } | null;
  tokens: AuthTokens;
};

export type WorkspaceOut = { id: string; organization_id: string; name: string; slug: string; description?: string | null; settings: Record<string, unknown> };
export type ProjectOut = { id: string; organization_id: string; workspace_id: string; name: string; slug: string; description?: string | null; settings: Record<string, unknown> };
export type AgentOut = { id: string; workspace_id: string; project_id: string; name: string; slug: string; display_name?: string | null; role?: string | null; department?: string | null; description?: string | null; category?: string | null; status: string; lifecycle_stage: string; created_at: string; updated_at: string };
export type DemoBootstrapOut = { workspace: WorkspaceOut; project: ProjectOut; agents: AgentOut[] };

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export function getAccessToken() {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("vs_access_token");
}

export function getActiveWorkspaceId() {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("vs_workspace_id");
}

export function storeAuthSession(auth: AuthResponse) {
  window.localStorage.setItem("vs_access_token", auth.tokens.access_token);
  window.localStorage.setItem("vs_refresh_token", auth.tokens.refresh_token);
  if (auth.organization) window.localStorage.setItem("vs_organization_id", auth.organization.id);
  document.cookie = `vs_session=1; path=/; max-age=${auth.tokens.expires_in}; SameSite=Lax`;
}

export function storeDemoWorkspace(data: DemoBootstrapOut) {
  window.localStorage.setItem("vs_workspace_id", data.workspace.id);
  window.localStorage.setItem("vs_project_id", data.project.id);
}

export async function apiRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getAccessToken();
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers, cache: "no-store" });
  if (!response.ok) {
    let message = `Request failed with ${response.status}`;
    try {
      const body = await response.json();
      message = body?.error?.message ?? body?.detail ?? message;
    } catch {}
    throw new ApiError(message, response.status);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export async function signIn(email: string, password: string) {
  return apiRequest<AuthResponse>("/auth/signin", { method: "POST", body: JSON.stringify({ email, password }) });
}

export async function signUp(name: string, email: string, password: string, organizationName: string) {
  return apiRequest<AuthResponse>("/auth/signup", { method: "POST", body: JSON.stringify({ name, email, password, organization_name: organizationName }) });
}

export async function bootstrapDemoWorkspace() {
  const data = await apiRequest<DemoBootstrapOut>("/workspaces/bootstrap-demo", { method: "POST" });
  storeDemoWorkspace(data);
  return data;
}

export async function listAgents(workspaceId: string) {
  return apiRequest<AgentOut[]>(`/ai-employees?workspace_id=${encodeURIComponent(workspaceId)}`);
}