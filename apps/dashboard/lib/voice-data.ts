import { Activity, AlertTriangle, AudioWaveform, Bot, BrainCircuit, CheckCircle2, Clock3, Cpu, Gauge, Mic2, RadioTower, RefreshCw, ShieldCheck, Signal, SlidersHorizontal, Volume2, Zap } from "lucide-react";

export const voiceStats = [
  { label: "Active sessions", value: "42", detail: "8 browser, 34 phone-ready", icon: RadioTower, tone: "green" },
  { label: "Median latency", value: "612 ms", detail: "1.2s budget", icon: Zap, tone: "blue" },
  { label: "Interruptions", value: "128", detail: "Natural barge-in tracked", icon: Activity, tone: "amber" },
  { label: "Provider errors", value: "0.18%", detail: "Fallback ready", icon: ShieldCheck, tone: "purple" },
];

export const voicePipeline = [
  { label: "Audio stream", detail: "20ms chunks, full duplex", icon: AudioWaveform, latency: "24 ms" },
  { label: "VAD", detail: "Speech, silence, interruption", icon: Signal, latency: "12 ms" },
  { label: "STT", detail: "Incremental transcription", icon: Mic2, latency: "184 ms" },
  { label: "Conversation", detail: "State, context, memory preview", icon: BrainCircuit, latency: "96 ms" },
  { label: "TTS", detail: "Streaming speech synthesis", icon: Volume2, latency: "214 ms" },
];

export const activeVoiceSessions = [
  { id: "vs_1042", employee: "Maya", channel: "Browser", status: "Active", speaker: "Customer", latency: "584 ms", interrupts: 2, duration: "06:18" },
  { id: "vs_1041", employee: "Atlas", channel: "Mobile", status: "Recovering", speaker: "AI employee", latency: "940 ms", interrupts: 0, duration: "11:04" },
  { id: "vs_1039", employee: "Nova", channel: "Inbound-ready", status: "Idle", speaker: "None", latency: "--", interrupts: 1, duration: "02:42" },
];

export const providerMatrix = [
  { type: "STT", primary: "OpenAI", fallback: "Deepgram", status: "Ready", capabilities: ["Streaming", "Partials", "Multilingual"] },
  { type: "TTS", primary: "OpenAI", fallback: "Cartesia", status: "Ready", capabilities: ["Streaming", "Emotion", "Speed"] },
  { type: "VAD", primary: "Energy threshold", fallback: "Provider VAD", status: "Implemented", capabilities: ["Start", "Stop", "Silence"] },
  { type: "Transport", primary: "WebSocket", fallback: "WebRTC-ready", status: "Foundation", capabilities: ["Duplex", "Authenticated", "Session resume"] },
];

export const latencyBudget = [
  { stage: "Audio ingest", target: 30, actual: 24 },
  { stage: "VAD", target: 20, actual: 12 },
  { stage: "STT", target: 250, actual: 184 },
  { stage: "Reasoning", target: 700, actual: 296 },
  { stage: "TTS", target: 250, actual: 214 },
];

export const voiceSettings = [
  { label: "Streaming mode", value: "Full duplex", icon: RefreshCw },
  { label: "Language", value: "English", icon: Bot },
  { label: "Speed", value: "1.02x", icon: Gauge },
  { label: "Stability", value: "82%", icon: SlidersHorizontal },
  { label: "Timeout", value: "45 min", icon: Clock3 },
  { label: "Audio storage", value: "Metadata only", icon: ShieldCheck },
];

export const streamEvents = [
  { time: "10:42:31.120", event: "audio.chunk", stage: "stream", detail: "20ms inbound PCM16 chunk received", icon: AudioWaveform },
  { time: "10:42:31.132", event: "vad.speech_detected", stage: "vad", detail: "User speech detected with 0.88 confidence", icon: Signal },
  { time: "10:42:31.316", event: "stt.partial", stage: "stt", detail: "Partial transcript emitted", icon: Mic2 },
  { time: "10:42:31.388", event: "user.interrupt", stage: "interruption", detail: "Playback stopped and state preserved", icon: AlertTriangle },
  { time: "10:42:31.704", event: "tts.partial", stage: "tts", detail: "Outgoing speech chunk queued", icon: Volume2 },
];

export const monitoringChecks = [
  { label: "Provider failover", state: "Configured", icon: CheckCircle2 },
  { label: "Session authentication", state: "Required", icon: ShieldCheck },
  { label: "Raw audio storage", state: "Disabled", icon: ShieldCheck },
  { label: "Metrics collector", state: "Online", icon: Cpu },
];