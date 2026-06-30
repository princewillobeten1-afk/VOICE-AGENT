# AI Sequence and Data Flow Diagrams

These diagrams define Task 011 architecture flows. They are not implementation code.

## Request Lifecycle

```mermaid
sequenceDiagram
    participant Channel as Channel Adapter
    participant Conversation as Conversation Manager
    participant Orchestrator as AI Orchestrator
    participant Context as Context Builder
    participant Memory as Memory Manager
    participant Knowledge as Knowledge Interface
    participant Prompt as Prompt Manager
    participant Planner as Planning Engine
    participant Tools as Tool Manager
    participant Provider as Provider Manager
    participant Events as Event System

    Channel->>Conversation: Normalize inbound request
    Conversation->>Orchestrator: Start AI turn
    Orchestrator->>Events: ai.request.received
    Orchestrator->>Context: Build context request
    Context->>Memory: Retrieve scoped memory
    Context->>Knowledge: Retrieve relevant knowledge references
    Context->>Prompt: Resolve prompt version and variables
    Context-->>Orchestrator: Context package
    Orchestrator->>Planner: Plan next action
    Planner-->>Orchestrator: Answer / tool / clarify / delegate
    Orchestrator->>Tools: Validate and execute tool if needed
    Tools-->>Orchestrator: Tool observation
    Orchestrator->>Provider: Generate response
    Provider-->>Orchestrator: Provider-neutral output
    Orchestrator->>Memory: Store memory updates if needed
    Orchestrator->>Events: ai.response.generated
    Orchestrator-->>Conversation: Final response
    Conversation-->>Channel: Channel-specific delivery
```

## Tool Execution Flow

```mermaid
sequenceDiagram
    participant Planner as Planning Engine
    participant ToolManager as Tool Manager
    participant Policy as Policy Guard
    participant Registry as Tool Registry
    participant Integration as Integration Framework
    participant Workflow as Workflow Adapter
    participant Events as Event System

    Planner->>ToolManager: Proposed tool call
    ToolManager->>Registry: Discover tool definition
    ToolManager->>Policy: Check organization, role, scope, and tool policy
    Policy-->>ToolManager: Allow or deny
    ToolManager->>ToolManager: Validate parameters against schema
    alt External integration tool
        ToolManager->>Integration: Execute connector action
        Integration-->>ToolManager: Structured result
    else Workflow tool
        ToolManager->>Workflow: Start workflow run
        Workflow-->>ToolManager: Run handle or result
    else Internal tool
        ToolManager->>ToolManager: Execute internal capability
    end
    ToolManager->>Events: ai.tool.invoked / ai.tool.completed
    ToolManager-->>Planner: Observation
```

## Memory Lifecycle

```mermaid
flowchart TD
    Turn[Conversation Turn] --> Extract[Memory Candidate Extraction]
    Extract --> Classify{Memory Type}
    Classify --> Short[Short-Term Memory]
    Classify --> Working[Working Memory]
    Classify --> Long[Long-Term Memory]
    Classify --> Org[Organizational Memory]
    Classify --> Shared[Shared Multi-Agent Memory]
    Short --> Expire[TTL / Session Expiry]
    Working --> TaskState[Task Completion Expiry]
    Long --> Policy[Retention Policy]
    Org --> Governance[Admin Governance]
    Shared --> Conflict[Conflict Resolution]
    Policy --> Retrieval[Future Retrieval]
    Governance --> Retrieval
    Conflict --> Retrieval
```

## Voice Pipeline

```mermaid
sequenceDiagram
    participant Audio as Audio Stream
    participant VAD as VAD and Turn Detection
    participant STT as STT Provider Adapter
    participant Orchestrator as AI Orchestrator
    participant TTS as TTS Provider Adapter
    participant Stream as Audio Response Stream

    Audio->>VAD: Frames
    VAD->>STT: Speech segment
    STT-->>Orchestrator: Transcript with timing
    Orchestrator-->>TTS: Response text / SSML plan
    TTS-->>Stream: Audio chunks
    Stream-->>Audio: Playback
```

## Multi-Agent Collaboration

```mermaid
sequenceDiagram
    participant Primary as Primary AI Employee
    participant Coordinator as Collaboration Coordinator
    participant Specialist as Specialist AI Employee
    participant Memory as Shared Memory
    participant Events as Event System

    Primary->>Coordinator: Delegation request
    Coordinator->>Memory: Create shared task context
    Coordinator->>Specialist: Assign bounded task
    Specialist->>Memory: Read shared context
    Specialist-->>Coordinator: Result and confidence
    Coordinator->>Coordinator: Resolve conflicts / aggregate
    Coordinator->>Events: ai.collaboration.completed
    Coordinator-->>Primary: Final result
```

## Data Flow Summary

```text
Channel Input
  -> normalized turn
  -> scoped context request
  -> ranked memory and knowledge references
  -> prompt package
  -> reasoning plan
  -> tool/workflow observations
  -> provider-neutral model response
  -> channel-specific response
  -> traces, events, analytics, memory updates
```