# AI Studio Architecture

AI Studio is the VoiceSense engineering workspace for prompt management, testing, evaluation, simulation, benchmarking, experimentation, deployment, replay, analytics, and collaboration.

## Lifecycle

Create AI Employee -> Configure Prompt -> Attach Knowledge -> Attach Memory -> Attach Tools -> Attach Workflow -> Run Simulation -> Evaluate -> Benchmark -> Deploy -> Monitor -> Iterate.

## Boundaries

- `app/aistudio` owns prompt versions, templates, playground runs, simulations, evaluations, test suites, benchmarks, experiments, deployments, collaboration, analytics, AI timelines, and replay sessions.
- `app/ai` owns AI employee identity and configuration.
- Voice, knowledge, memory, tools, workflows, conversations, AIOps, and security remain independent provider modules that AI Studio references.

## Runtime Policy

Task 027 creates durable workflow records and dashboard surfaces. Live provider execution, automatic prompt generation, autonomous optimization, RL systems, and model training pipelines are intentionally out of scope.