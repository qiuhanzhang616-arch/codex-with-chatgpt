import path from "node:path";
import { getStateDir, readJsonIfExists, writeSecureJson } from "../config/paths.js";

export type TunnelPreference = "unset" | "quick" | "named";

export interface TunnelState {
  workspaceId: string;
  preference: TunnelPreference;
  askedAt?: string;
  provider?: "cloudflare-quick" | "cloudflare-named";
  tunnelName?: string;
  tunnelId?: string;
  hostname?: string;
  zone?: string;
  configuredAt?: string;
  fallbackReason?: string;
}

export function tunnelStateFile(workspaceId: string): string {
  return path.join(getStateDir(), "tunnels", `${workspaceId}.json`);
}

export function readTunnelState(workspaceId: string): TunnelState {
  return (
    readJsonIfExists<TunnelState>(tunnelStateFile(workspaceId)) ?? {
      workspaceId,
      preference: "unset",
    }
  );
}

export function writeTunnelState(state: TunnelState): TunnelState {
  writeSecureJson(tunnelStateFile(state.workspaceId), state);
  return state;
}

export function needsTunnelChoice(state: TunnelState): boolean {
  return state.preference === "unset" || !state.askedAt;
}

export function isNamedTunnelReady(state: TunnelState): boolean {
  return (
    state.preference === "named" &&
    Boolean(state.tunnelName?.trim()) &&
    Boolean(state.hostname?.trim())
  );
}

export function namedTunnelBinding(state: TunnelState): { tunnelName: string; hostname: string } | null {
  if (!isNamedTunnelReady(state) || !state.tunnelName || !state.hostname) return null;
  return { tunnelName: state.tunnelName, hostname: state.hostname };
}

export const TUNNEL_CHOICE_PROMPT = `Before connecting ChatGPT, choose one connection option.
Do you have a Cloudflare account and a domain already managed by Cloudflare?
- Yes: use a stable domain. Configure the plugin once and it should keep working across restarts. You will sign in to Cloudflare once and add a subdomain.
- No: use a temporary address. Registration is not required and features are the same, but the address often changes after restart. I will recreate this workspace's connector when needed, although repair is slower and may require another ChatGPT sign-in.
You do not need a Cloudflare account. Choose an option, or provide your domain, for example example.com.`;

export const NAMED_LOGIN_PROMPT =
  "A browser window will open. Sign in to Cloudflare, select your domain, and tell me when it is done.";

export const NAMED_FALLBACK_MESSAGE =
  "Using a temporary address for now. Features are the same, but future repairs may be slower. Ask to switch to a stable domain at any time.";

export const NAMED_REPAIR_MESSAGE =
  "The stable domain is temporarily unavailable. Sign in to Cloudflare in the window that opens, select your domain, and tell me when it is done.";
