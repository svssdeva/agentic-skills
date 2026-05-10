<!-- Source: https://skills.sh/anthropics/knowledge-work-plugins/system-design -->
<!-- Install: npx skills add https://github.com/anthropics/knowledge-work-plugins --skill system-design -->

# System Design

Help design systems and evaluate architectural decisions.

## Framework

### 1. Requirements Gathering

* Functional requirements (what it does)
* Non-functional requirements (scale, latency, availability, cost)
* Constraints (team size, timeline, existing tech stack)

### 2. High-Level Design

* Component diagram
* Data flow
* API contracts
* Storage choices

### 3. Deep Dive

* Data model design
* API endpoint design (REST, GraphQL, gRPC)
* Caching strategy
* Queue/event design
* Error handling and retry logic

### 4. Scale and Reliability

* Load estimation
* Horizontal vs. vertical scaling
* Failover and redundancy
* Monitoring and alerting

### 5. Trade-off Analysis

* Every decision has trade-offs. Make them explicit.
* Consider: complexity, cost, team familiarity, time to market, maintainability

## Output

Produce clear, structured design documents with diagrams (ASCII or described), explicit assumptions, and trade-off analysis. Always identify what you'd revisit as the system grows.
