# Orchestration with Prefect

- [Orchestration with Prefect](#orchestration-with-prefect)
  - [what is workflow orchestration](#what-is-workflow-orchestration)
  - [negative engineering](#negative-engineering)
  - [what is prefect](#what-is-prefect)
  - [prefect features](#prefect-features)
  - [prefect on VM](#prefect-on-vm)
  - [Prefect Orchestration Steps](#prefect-orchestration-steps)
  - [work queues](#work-queues)
  - [code snippets](#code-snippets)

## what is workflow orchestration

set of features that aim to eliminate negative engineering

- retries off-the-shelf
- observability into failure
- failure paths

## negative engineering

Coding against failure and coding to make negative scenarios from happening

data scientist spend 90% data cleaning, data engineers spend 90% on negative engineering

- retries when APIs go down
- malformed data
- notifications
- observability into failure
- conditional failure logic
- timeouts

## what is prefect

Open Source Workflow Orchestration Framework for eliminating Negative Engineering:

- Open Source
- Python-based
- Modern data stack
- Native Dask integration
- Very active Community
- Prefect Cloud/Prefect Server -> Cloud is hosted by Prefect, Server Self-hosted.

Features

- Tasks - They are functions having special runs when they should run; optionally take inputs, perform some work and optionally return an output.
- Workflows - They are basically containers of tasks defining dependencies among them.
- Modularity - Every component of Prefect is a modular design, making it easy to customize, to logging, to storage, to handle state.
- Concurrency - Supports massive concurrency
  Automation - Has a solid framework to support workflows

<https://www.prefect.io/>

## prefect features

- task = unit of monitoring
- data type hints can cause failures to be caught at compile time

## prefect on VM

- Create a VM on Cloud Provider of Choice
- Open port 4200 ingress on the VM from 0.0.0.0/0 (all traffic) as well as HTTP in.
- `pip install prefect 2.0b5`
- Set the UI_API_URL with
  - `prefect config set PREFECT_ORION_UI_API_URL="http://<external-ip>:4200/api"`
- Start Orion with:
  - `prefect orion start --host 0.0.0.0`
- From local machine, configure to hit the API with:
  - `prefect config set PREFECT_API_URL="http://<external-ip>:4200/api"`
  - `prefect config view` to verify
- The remote UI will be visible on :4200/

## Prefect Orchestration Steps

1. Create a script with @task and @flow decorators around functions or classes.

2. Create a deployment specification (will need to specify flow function or script, schedule, and flow runner)

   [Docs for deployment](https://orion-docs.prefect.io/concepts/deployments/)

   [Docs for schedule](https://orion-docs.prefect.io/concepts/schedules/)

   [Docs for flow runner](https://orion-docs.prefect.io/concepts/flow-runners/)

3. Specify the orchestration engine (Prefect Cloud or a local Prefect API server started with `prefect orion start`)
   [Docs for Orion Cloud](https://orion-docs.prefect.io/ui/cloud-getting-started/)

4. Specify storage for flow deployments and results

   [Docs for storage](https://orion-docs.prefect.io/concepts/storage/)

5. Specify a workqueue and an agent

   [Docs for work-queue](https://orion-docs.prefect.io/concepts/work-queues/)

## work queues

The work queue a queue that will prompt its attached Agents to run the scheduled runs.

To create a new work queue use the Prefect UI and select work queues in the side panel (A name is required for creating the queue), filtering by Tags is possible.

A window will pop that includes the command used to add an agent to the work-queue; `prefect agent start <UUID>`. With the UUID being the UUID of the work-queue.

We can check the state of the work-queue by using `prefect work-queue preview <UUID>` where it will show scheduled runs.

## code snippets

Launch prefect ui

```txt
prefect orion start
```

Create deployment

```txt
prefect deployment create <filename>
```

Other deployment commands

```txt
prefect deployment create | run | execute | inspect | ls
```

Prefect storage on cloud

```txt
prefect storage ls
prefect storage create
```

Create workqueue

```txt
prefect work-queue create [OPTIONS] NAME
```

Workqueue

```txt
prefect work-queue preview 'work-queue-id-string' #view scheduled flow runs
prefect work-queue ls #view all available work queues
```

Agent

```txt
prefect agent start 'agent'
```

Clear Prefect database - will delete all data in `orion.db`

```txt
prefect orion database reset
```
