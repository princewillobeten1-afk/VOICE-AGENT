from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class NodeDefinition:
    type: str
    label: str
    group: str
    description: str
    inputs: list[str]
    outputs: list[str]
    config_schema: dict
    async_capable: bool = True
    pause_capable: bool = False


class NodeRegistry:
    def __init__(self) -> None:
        self._nodes: dict[str, NodeDefinition] = {}
        self._register_defaults()

    def register(self, definition: NodeDefinition) -> None:
        self._nodes[definition.type] = definition

    def get(self, node_type: str) -> NodeDefinition | None:
        return self._nodes.get(node_type)

    def catalog(self) -> list[dict]:
        return [asdict(item) for item in sorted(self._nodes.values(), key=lambda node: (node.group, node.label))]

    def _register_defaults(self) -> None:
        nodes = [
            ("start", "Start", "core", "Entry point for manual, scheduled, API, event, or webhook triggers."),
            ("end", "End", "core", "Terminal node for completed workflow branches."),
            ("delay", "Delay", "control", "Pause execution for a duration."),
            ("condition", "Condition", "control", "Route execution with if/else expressions."),
            ("loop", "Loop", "control", "Iterate over arrays or repeat while a condition is true."),
            ("switch", "Switch", "control", "Route by multiple matching cases."),
            ("merge", "Merge", "control", "Join multiple branches."),
            ("split", "Split", "control", "Fork parallel branches."),
            ("wait", "Wait", "control", "Wait until an event, time, or condition occurs."),
            ("human_approval", "Human Approval", "human", "Pause execution until a reviewer approves or rejects."),
            ("webhook", "Webhook", "trigger", "Receive external webhook events."),
            ("schedule", "Schedule", "trigger", "Run on a schedule."),
            ("variable", "Variable", "data", "Read or write workflow variables."),
            ("transform", "Transform", "data", "Map, reshape, or derive JSON payloads."),
            ("log", "Log", "utility", "Write structured execution logs."),
            ("error_handler", "Error Handler", "control", "Handle branch or workflow failures."),
            ("sub_workflow", "Sub Workflow", "control", "Invoke another workflow."),
            ("ai_employee", "AI Employee", "ai", "Delegate a task to a configured AI employee."),
            ("prompt", "Prompt", "ai", "Prepare prompt instructions for future AI execution."),
            ("memory", "Memory", "ai", "Read or write AI memory through the memory system."),
            ("knowledge_search", "Knowledge Search", "ai", "Retrieve governed context from the retrieval engine."),
            ("tool_call", "Tool Call", "ai", "Call an approved AI tool adapter."),
            ("ai_decision", "AI Decision", "ai", "Route by a future model decision."),
            ("ai_supervisor", "AI Supervisor", "ai", "Review or coordinate AI outputs."),
            ("multi_agent_coordinator", "Multi-Agent Coordinator", "ai", "Coordinate several AI employees."),
            ("email", "Email", "integration", "Send or receive email through an integration adapter."),
            ("crm", "CRM", "integration", "Read or update CRM records."),
            ("calendar", "Calendar", "integration", "Create, update, or inspect calendar events."),
            ("database", "Database", "integration", "Run governed database operations."),
            ("slack", "Slack", "integration", "Send or react to Slack events."),
            ("whatsapp", "WhatsApp", "integration", "Send or respond to WhatsApp messages."),
            ("storage", "Storage", "integration", "Read or write files through storage adapters."),
            ("payments", "Payments", "integration", "Prepare payment-provider actions."),
            ("http_request", "HTTP Request", "integration", "Call an external HTTP API."),
            ("custom_api", "Custom API", "integration", "Execute custom developer-defined API logic."),
        ]
        for node_type, label, group, description in nodes:
            self.register(NodeDefinition(type=node_type, label=label, group=group, description=description, inputs=["default"], outputs=["success", "error"] if node_type != "end" else [], config_schema={"type": "object"}, pause_capable=node_type in {"delay", "wait", "human_approval"}))


node_registry = NodeRegistry()
