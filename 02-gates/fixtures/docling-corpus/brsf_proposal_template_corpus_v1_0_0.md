**PROJECT PROPOSAL**

*BRSF-Aligned Modular Template v6.0*

**Mission → Scope → Goals → Objectives → Backlog → Roadmap**

**PROJECT PROPOSAL — BRSF-Aligned Modular Template v6.0**

| Project Title            | [PROJECT TITLE]                                 |
|--------------------------|-------------------------------------------------|
| Project Type             | Academic ✓ / Industrial □ / Startup □ / Other □ |
| Version                  | 1.0                                             |
| Date                     | [Date]                                          |
| Author(s)                | [Names]                                         |
| Institution / Department | [Institution]                                   |
| Course Code              | [e.g., COM8090]                                 |
| Academic Year            | [e.g., 2026-2027]                               |
| Semester                 | [Fall / Spring / Summer]                        |
| Advisor                  | [Name, Title, e-mail]                           |
| Status                   | Draft                                           |

### MODULE SELECTION GUIDE

*BRSF Lineage (Part 0) and Core (Part I) are mandatory. All other parts are optional by context.*

| **Module**            | **Sections**   | **Required?**         | **BRSF Concepts**                                   |
|-----------------------|----------------|-----------------------|-----------------------------------------------------|
| BRSF LINEAGE (Part 0) | 0.1-0.6        | MANDATORY             | Mission, Scope, Goals, Objectives, Backlog, Roadmap |
| CORE (Part I)         | 1-9            | MANDATORY             | WorkItem, Deliverable, Gate, Risk, DoD              |
| ACADEMIC (Part II)    | 10             | If university         | Blueprint context, Learning Objectives              |
| INDUSTRIAL (Part III) | 11             | If corporate          | Stakeholder, Budget, ROI                            |
| STARTUP (Part IV)     | 12             | If commercial         | Benefit, Commitment, IP                             |
| GOVERNANCE (Part V)   | 13             | Recommended for teams | RACI, Accountability                                |
| TECHNOLOGY (Part VI)  | 14             | Select areas          | Stack, Architecture                                 |

## PART 0: BRSF LINEAGE (MANDATORY)

*This part declares the project’s complete formal intent chain before any work begins. The lineage is: Mission → Scope → Goals → Objectives → Backlog → Roadmap. Every element must be completed and consistent before execution starts.*

### 0.1 Mission

Why this project exists. Owner-declared root of the intent chain. One paragraph, declarative. **«backlog:Mission + hasMissionStatement»**

*[ State the problem, the scale of the gap, and why this project must exist now. No solution language. Reference foundational work. ]*

*[ [Mission statement — one paragraph, declarative, owner-signed.] ]*

### 0.2 Scope

Declared boundary: what the project covers and what it deliberately does not. **«backlog:ScopeStatement + ScopeExclusion + ScopeDeliverable»**

#### 0.2a In-Scope Areas

| **S-ID**   | **Area / Entity / Capability**   | **areaLocation**   | **areaMeasure**   | **Rationale**   |
|------------|----------------------------------|--------------------|-------------------|-----------------|
| S1         | [Domain entity / capability]     | [Files/modules]    | [Size/count]      | [Why in scope]  |
| S2         | [Domain entity / capability]     | [Files/modules]    | [Size/count]      | [Why in scope]  |
| S3         | [Domain entity / capability]     | [Files/modules]    | [Size/count]      | [Why in scope]  |
| S4         | [Domain entity / capability]     | [Files/modules]    | [Size/count]      | [Why in scope]  |
| S5         | [Domain entity / capability]     | [Files/modules]    | [Size/count]      | [Why in scope]  |
| S6         | [Domain entity / capability]     | [Files/modules]    | [Size/count]      | [Why in scope]  |

#### 0.2b Scope Deliverables

Capabilities the scope requires, enumerated before any WorkItem exists. **«backlog:ScopeDeliverable + requiresDeliverable + deliverableForArea»**

| **SD-ID**   | **Deliverable Statement**   | **Fills Area**   | **Functional / Quality**   | **Target Date**   |
|-------------|-----------------------------|------------------|----------------------------|-------------------|
| SD-1        | [What must be deliverable]  | S1               | Functional                 | [Date]            |
| SD-2        | [What must be deliverable]  | S2-S3            | Quality                    | [Date]            |
| SD-3        | [What must be deliverable]  | S4-S6            | Functional                 | [Date]            |

#### 0.2c Explicit Exclusions

Owner-decided things outside the boundary, each with rationale. **«backlog:ScopeExclusion + hasExclusionRationale»**

| **E-ID**   | **Excluded Area / Entity**   | **Rationale for Exclusion**                        |
|------------|------------------------------|----------------------------------------------------|
| E1         | [Excluded item]              | [Why explicitly excluded — not merely unaddressed] |
| E2         | [Excluded item]              | [Why explicitly excluded]                          |
| E3         | [Excluded item]              | [Why explicitly excluded]                          |

### 0.3 Goals

Durable outcomes the project exists to achieve. Each goal must derive from the mission and have a measurable instrument. **«backlog:Goal + contributesToMission + derivesFromScope + hasGoalFacing»**

| **G-ID**   | **Goal Statement**   | **Goal Facing**   | **Measurement Instrument**   | **Target Value**   | **Derives From Scope**   |
|------------|----------------------|-------------------|------------------------------|--------------------|--------------------------|
| G1         | [Durable outcome]    | Technical         | [Named metric]               | ≥ [x]              | S1-S2                    |
| G2         | [Durable outcome]    | Process           | [Named metric]               | ≤ [x] min          | S3-S4                    |
| G3         | [Durable outcome]    | Quality           | [Named metric]               | 100%               | All S                    |
| G4         | [Durable outcome]    | Stakeholder       | [Named metric]               | ≥ [x]%             | S5-S6                    |

### 0.4 Objectives

Measurable, time-bounded targets filling the scope. Objectives without metrics are not permitted. **«backlog:Objective + fillsScope + hasBaselineValue + hasTargetValue + hasObjectiveDeadline + hasMeasurementKind + hasCheckpoint + metricMovableBy»**

*[ The following objectives fill the declared scope (fillsScope) and are each paired with a measurable target: ]*

| **O-ID**   | **Objective Statement**   | **Fills Scope (S)**   | **Advances Goal**   | **Metric**   | **Measurement Kind**   | **Baseline**   | **Target**   | **Checkpoint Date**   |
|------------|---------------------------|-----------------------|---------------------|--------------|------------------------|----------------|--------------|-----------------------|
| O1         | [Statement]               | S1                    | G1                  | [Metric]     | Counted                | [Now]          | [Target]     | [Date]                |
| O2         | [Statement]               | S2-S3                 | G1                  | [Metric]     | Measured               | [Now]          | [Target]     | [Date]                |
| O3         | [Statement]               | S4                    | G2                  | [Metric]     | Counted                | [Now]          | [Target]     | [Date]                |
| O4         | [Statement]               | S5                    | G3                  | [Metric]     | Judged                 | [Now]          | [Target]     | [Date]                |
| O5         | [Statement]               | S1-S6                 | G4                  | [Metric]     | Measured               | [Now]          | [Target]     | [Date]                |
| O6         | [Statement]               | S1-S6                 | G1-G4               | [Metric]     | Counted                | [Now]          | [Target]     | [Date]                |

### 0.5 High-Level Backlog (Proposed PBIs)

Initiative and Epic level work items, in proposed state. RICE+DepFactor scores are estimates; they will be refined in backlog grooming. **«backlog:Initiative + backlog:Epic + backlog:ProductBacklogItem + hasState:Proposed + hasRiceScore + hasDepFactor»**

State: all items are **Proposed** (not Ready or In Progress). Package assignments are candidate, not confirmed. RICE scores are advisory at proposal stage.

#### 0.5a Initiatives

Portfolio-level strategic outcomes spanning multiple epics. **«backlog:Initiative + InitiativeKind + VersionIncrement»**

| **IN-ID**   | **Initiative Title**   | **Kind**       | **Objective(s)**   | **Expected Version Increment**   | **Priority (RICE est.)**   |
|-------------|------------------------|----------------|--------------------|----------------------------------|----------------------------|
| IN-1        | [Strategic initiative] | New Capability | O1-O3              | MAJOR                            | [High/Med/Low]             |
| IN-2        | [Strategic initiative] | New Capability | O4-O6              | MINOR                            | [High/Med/Low]             |

#### 0.5b Epics

Large bodies of work decomposed across multiple features. **«backlog:Epic + pursuesObjective + hasInvestmentCategory + hasPriorityScore»**

| **EP-ID**   | **Epic Title**   | **Investment Category**   | **Objective**   | **RICE Reach**   | **RICE Impact**   | **RICE Conf.**   | **RICE Effort**   |   **DepFactor** | **Score**   | **State**   |
|-------------|------------------|---------------------------|-----------------|------------------|-------------------|------------------|-------------------|-----------------|-------------|-------------|
| EP-1        | [Epic]           | New Capability            | O1-O2           | [1-10]           | [1-10]            | [0-1]            | [1-10]            |             1.0 | [R×I×C/E×D] | Proposed    |
| EP-2        | [Epic]           | New Capability            | O3              | [1-10]           | [1-10]            | [0-1]            | [1-10]            |             0.8 | [score]     | Proposed    |
| EP-3        | [Epic]           | New Capability            | O4-O5           | [1-10]           | [1-10]            | [0-1]            | [1-10]            |             1.0 | [score]     | Proposed    |
| EP-4        | [Epic]           | New Capability            | O6              | [1-10]           | [1-10]            | [0-1]            | [1-10]            |             0.9 | [score]     | Proposed    |

#### 0.5c Features (high-level PBIs)

Coherent capabilities deliverable in a single iteration. **«backlog:Feature + backlog:ProductBacklogItem + hasAcceptanceCriterion + satisfiesDeliverable»**

| **F-ID**   | **Feature Title**   | **Epic**   | **Scope Deliverable**   | **Priority**   | **Acceptance Criterion (summary)**   | **State**   |
|------------|---------------------|------------|-------------------------|----------------|--------------------------------------|-------------|
| F-1        | [Feature]           | EP-1       | SD-1                    | Must Have      | [Given/When/Then summary]            | Proposed    |
| F-2        | [Feature]           | EP-1       | SD-1                    | Must Have      | [Given/When/Then summary]            | Proposed    |
| F-3        | [Feature]           | EP-2       | SD-2                    | Must Have      | [Given/When/Then summary]            | Proposed    |
| F-4        | [Feature]           | EP-3       | SD-2                    | Should Have    | [Given/When/Then summary]            | Proposed    |
| F-5        | [Feature]           | EP-3       | SD-3                    | Must Have      | [Given/When/Then summary]            | Proposed    |
| F-6        | [Feature]           | EP-4       | SD-3                    | Must Have      | [Given/When/Then summary]            | Proposed    |

Note: *Features are high-level PBIs at proposal stage. They will be decomposed into Stories and Tasks during sprint planning. Acceptance criteria will be refined to full Given/When/Then format in backlog grooming.*

### 0.6 Proposed Roadmap and Package Definitions

A time-ordered view over the backlog by horizon (Now/Next/Later) and milestone-gate. Package definitions group coherent work into deployable business functions. All horizons and packages are **proposed** , not confirmed. **«backlog:Roadmap + RoadmapHorizon + Package + Milestone + ReleaseGate + Iteration + DeploymentUnit»**

#### 0.6a Roadmap Horizons (Now / Next / Later)

Three closed horizons per the BRSF standard. **«backlog:RoadmapHorizon: Now, Next, Later»**

| **Horizon**   | **Scope**                          | **Key Epics / Features**   | **Target Gate**             | **Milestone**   | **State**   |
|---------------|------------------------------------|----------------------------|-----------------------------|-----------------|-------------|
| NOW           | Committed, current iteration(s)    | EP-1, F-1, F-2             | Gate-1: Foundation Ready    | M1: [Name]      | Proposed    |
| NEXT          | Planned, 1-3 iterations out        | EP-2, EP-3, F-3, F-4       | Gate-2: Core Operational    | M2: [Name]      | Proposed    |
| LATER         | Candidate, beyond planning horizon | EP-4, F-5, F-6             | Gate-3: Evaluation Complete | M3: Final       | Proposed    |

#### 0.6b Package Definitions

Coherent groups of work items that together deliver a meaningful, demonstrable capability. Packages are the unit of delivery planning. **«backlog:Package + deliversPackage + targetsIteration»**

| **PKG-ID**   | **Package Name**   | **Description**               | **Features Included**   | **Target Iteration**   | **Proposed Release**   | **State**   |
|--------------|--------------------|-------------------------------|-------------------------|------------------------|------------------------|-------------|
| PKG-1        | [Package name]     | [What it delivers as a whole] | F-1, F-2                | IT-1                   | v0.1.0                 | Proposed    |
| PKG-2        | [Package name]     | [What it delivers as a whole] | F-3, F-4                | IT-2                   | v0.2.0                 | Proposed    |
| PKG-3        | [Package name]     | [What it delivers as a whole] | F-5, F-6                | IT-3                   | v1.0.0                 | Proposed    |

#### 0.6c Milestones and Release Gates

Milestones mark external significance points. Each milestone carries a gate: an executable check the project must pass before the next horizon opens. **«backlog:Milestone + ReleaseGate + hasGateCommand + hasGateResult + isLaunchGate + AdaptationGate»**

*[ Milestones must match gates and controls. A milestone is not reached until its gate passes. ]*

| **M-ID**   | **Milestone Name**   | **Target Date**   | **Gate ID**   | **Gate Check (hasGateCommand)**    | **Expected Result (hasGateResult)**   | **Objective Link**   | **Launch Gate?**   |
|------------|----------------------|-------------------|---------------|------------------------------------|---------------------------------------|----------------------|--------------------|
| M1         | Foundation Ready     | [Date]            | G-1           | [SHACL / test command]             | 0 violations                          | O1-O2                | No                 |
| M2         | Core Operational     | [Date]            | G-2           | [End-to-end test suite pass]       | ≥ 80% pass rate                       | O3-O4                | No                 |
| M3         | Evaluation Complete  | [Date]            | G-3           | [Evaluation study run]             | All targets met                       | O5                   | No                 |
| M4         | Final Delivery       | [Date]            | G-4           | [Advisor review + paper submitted] | Approved                              | O6                   | ✓ Launch Gate      |

#### 0.6d Definition of Done (Standing Gates)

Standing checks every WorkItem must pass before moving to Done. **«backlog:DefinitionOfDone + DoDCriterion + hasCheckQuery + hasExpectedResult + hasCriterionStatus»**

| **DoD-ID**   | **Criterion**                             | **Check Query / Command**   | **Expected Result**   | **Status**   |
|--------------|-------------------------------------------|-----------------------------|-----------------------|--------------|
| DoDC-1       | [Criterion — e.g. all tests pass]         | [Command to verify]         | [Expected output]     | □ Pending    |
| DoDC-2       | [Criterion — e.g. SHACL 0 violations]     | [Command]                   | 0 violations          | □ Pending    |
| DoDC-3       | [Criterion — e.g. code review approved]   | [Command or record]         | Approved sign-off     | □ Pending    |
| DoDC-4       | [Criterion — e.g. documentation complete] | [Command]                   | [Expected]            | □ Pending    |

#### 0.6e Risks Register (Proposed)

Known risks at proposal stage, each with a mitigation strategy. **«risk:Risk + hasRisk + hasMitigation + riskAcceptedBy»**

| **R-ID**   | **Description**   | **Type**   | **Probability**   | **Impact**   |   **Score** | **Affects Obj**   | **Mitigation**   |
|------------|-------------------|------------|-------------------|--------------|-------------|-------------------|------------------|
| R-1        | [Risk]            | Technical  | Medium            | High         |           6 | O2-O3             | [Plan]           |
| R-2        | [Risk]            | Schedule   | High              | Medium       |           6 | O5                | [Plan]           |
| R-3        | [Risk]            | Resource   | Low               | High         |           3 | O1                | [Plan]           |
| R-4        | [Risk]            | External   | Medium            | Medium       |           4 | O6                | [Plan]           |

#### 0.6f Benefits Register

Specific improvements expected from completing work, each owned by a stakeholder. **«backlog:Benefit + hasBenefitOwner + hasBenefitStatement + benefitFor + hasBaselineValue + hasTargetValue»**

| **B-ID**   | **Benefit Statement**   | **Benefit Owner (Stakeholder)**   | **Linked Objective**   | **Baseline**   | **Target**   | **Evidence Needed**     |
|------------|-------------------------|-----------------------------------|------------------------|----------------|--------------|-------------------------|
| B-1        | [Specific improvement]  | [Stakeholder name/role]           | O1                     | [Now]          | [Target]     | [What must be measured] |
| B-2        | [Specific improvement]  | [Stakeholder]                     | O5                     | [Now]          | [Target]     | [Evidence]              |
| B-3        | [Specific improvement]  | [Stakeholder]                     | O6                     | [Now]          | [Target]     | [Evidence]              |

## PART I: CORE SECTIONS (MANDATORY)

*Sections 1-9 elaborate the BRSF lineage with supporting engineering and execution detail.*

### 1. Executive Summary

#### 1.1 Project Overview

*[ 2-3 sentences. Derived from Mission (0.1). Write last. ]*

#### 1.2 Cross-Reference to BRSF Lineage

*[ Do not restate. Summarise: # goals, # objectives, # initiatives, # epics, # features, # packages, # milestones with gates. ]*

#### 1.3 Expected Benefits (cross-ref to 0.6f)

*[ Summary of the Benefits Register. Reference B-IDs only. ]*

### 2. Problem Context

#### 2.1 Current State

*[ [Describe the existing situation] ]*

#### 2.2 Desired State

*[ [Describe the target situation] ]*

#### 2.3 Gap Analysis

| **Gap**   | **Current State**   | **Desired State**   | **Addressed by**   |
|-----------|---------------------|---------------------|--------------------|
| [Gap 1]   | [Now]               | [Target]            | O1, F-1            |
| [Gap 2]   | [Now]               | [Target]            | O2, F-2            |

### 3. Requirements

*Requirements derive from Scope (0.2) and Objectives (0.4). Each FR traces to an S-ID and an O-ID.*

#### 3.1 Functional Requirements

| **FR-ID**   | **Description**   | **Priority**   | **Scope Ref**   | **Obj Ref**   | **Feature Ref**   |
|-------------|-------------------|----------------|-----------------|---------------|-------------------|
| FR-001      | [Requirement]     | Must Have      | S1              | O1            | F-1               |
| FR-002      | [Requirement]     | Must Have      | S2              | O2            | F-2, F-3          |

#### 3.2 Non-Functional Requirements

| **NFR-ID**   | **Type**    | **Description**   | **Metric**   | **Target**   | **Feature Ref**   |
|--------------|-------------|-------------------|--------------|--------------|-------------------|
| NFR-001      | Performance | [Description]     | [Metric]     | [Target]     | F-3               |
| NFR-002      | Security    | [Description]     | [Standard]   | [Target]     | All               |
| NFR-003      | Usability   | [Description]     | [Metric]     | [Target]     | F-4, F-5          |

### 4. Methodology

#### 4.1 Development Approach

| **Aspect**       | **Selection**                 | **Justification**   |
|------------------|-------------------------------|---------------------|
| Methodology      | [Agile / Predictive / Hybrid] | [Why chosen]        |
| Framework        | [Scrum / Kanban / Custom]     | [Why chosen]        |
| Iteration Length | [Duration]                    | [Rationale]         |

#### 4.2 Project Phases (aligned to Roadmap horizons)

| **Phase**       | **Roadmap Horizon**   | **Duration**   | **Key Activities**             | **Package**   | **Gate**                 |
|-----------------|-----------------------|----------------|--------------------------------|---------------|--------------------------|
| Initiation      | -                     | [Dur]          | Mission+Scope+Backlog grooming | -             | G-0: Proposal accepted   |
| Phase 1 (NOW)   | NOW                   | [Dur]          | [Activities]                   | PKG-1         | G-1: Foundation Ready    |
| Phase 2 (NEXT)  | NEXT                  | [Dur]          | [Activities]                   | PKG-2         | G-2: Core Operational    |
| Phase 3 (LATER) | LATER                 | [Dur]          | [Activities]                   | PKG-3         | G-3: Evaluation Complete |
| Closure         | -                     | [Dur]          | Final report, paper            | All           | G-4: Launch Gate         |

### 5. Team Structure

#### 5.1 Team Members

| **Name**   | **Role**   | **Objective Ownership**   | **Feature Ownership**   | **hrs/wk**   |
|------------|------------|---------------------------|-------------------------|--------------|
| [Name]     | Lead / PM  | O1, O5, O6                | EP-1                    | [hrs]        |
| [Name]     | Developer  | O2, O3                    | EP-2, EP-3              | [hrs]        |
| [Name]     | Analyst    | O4, O5                    | EP-4                    | [hrs]        |

#### 5.2 Stakeholders

| **Stakeholder**   | **Type**   | **Interest**   | **BRSF Role**   | **Communication**   |
|-------------------|------------|----------------|-----------------|---------------------|
| [Name/Role]       | Advisor    | [Interest]     | Mission owner   | [Frequency]         |
| [Name/Role]       | End User   | [Interest]     | Benefit owner   | [Frequency]         |

### 6. Timeline &amp; Milestones

*[ Milestones must align with the gates declared in 0.6c. A milestone is not reached until its gate passes. ]*

| **Phase / Package**   | **Start**   | **End**   | **Milestone**           | **Gate ID**   | **Gate Result Required**          |
|-----------------------|-------------|-----------|-------------------------|---------------|-----------------------------------|
| Initiation            | [Date]      | [Date]    | Proposal Signed         | G-0           | Proposal approved by advisor      |
| PKG-1 (NOW)           | [Date]      | [Date]    | M1: Foundation Ready    | G-1           | 0 gate violations                 |
| PKG-2 (NEXT)          | [Date]      | [Date]    | M2: Core Operational    | G-2           | All core features pass            |
| PKG-3 (LATER)         | [Date]      | [Date]    | M3: Evaluation Complete | G-3           | Study targets met                 |
| Closure               | [Date]      | [Date]    | M4: Final Delivery      | G-4           | Paper submitted; advisor approved |

### 7. Risk Management

*[ Risk register is pre-populated in 0.6e. This section adds mitigation detail. ]*

| **R-ID**   | **Mitigation Plan**   | **Contingency**   | **Owner**   | **Review Date**   |
|------------|-----------------------|-------------------|-------------|-------------------|
| R-1        | [Plan]                | [Fallback]        | [Name]      | [Date]            |
| R-2        | [Plan]                | [Fallback]        | [Name]      | [Date]            |

### 8. Deliverables

#### 8.1 Project Deliverables

Each deliverable maps to a Scope Deliverable (SD) and an Objective. **«backlog:WorkItem + pursuesObjective + satisfiesDeliverable + hasEvidence»**

| **Del-ID**   | **Deliverable**   | **Type**     | **SD Ref**   | **Obj Ref**   | **Due Date**   | **Acceptance Criteria**   |
|--------------|-------------------|--------------|--------------|---------------|----------------|---------------------------|
| D-1          | [Deliverable]     | Document     | SD-1         | O1            | [Date]         | [Criteria]                |
| D-2          | [Deliverable]     | Artefact     | SD-2         | O2-O3         | [Date]         | [Criteria]                |
| D-3          | [Deliverable]     | Application  | SD-3         | O4-O5         | [Date]         | [Criteria]                |
| D-4          | [Deliverable]     | Report/Paper | SD-1-3       | O6            | [Date]         | Advisor approved          |

#### 8.2 Definition of Done (standing — see also 0.6d)

*[ Cross-reference the DoD in 0.6d. Add item-specific criteria below. ]*

| **DoD-ID**   | **Criterion**             | **Check**       | **Expected**   | **Applies To**   |
|--------------|---------------------------|-----------------|----------------|------------------|
| DoDC-5       | [Item-specific criterion] | [Check command] | [Expected]     | D-1              |
| DoDC-6       | [Item-specific criterion] | [Check command] | [Expected]     | D-2              |

### 9. Recommended Resources

| **Type**     | **Citation / Reference**              | **Relevance**         |
|--------------|---------------------------------------|-----------------------|
| Foundational | [Author, Year. Title. Publisher.]     | [Why essential]       |
| Standard     | [W3C/ISO standard name, version, URL] | [Scope area]          |
| Tool         | [Name, version, URL]                  | [Feature / objective] |
| Dataset      | [Name, URL, licence]                  | [Objective]           |

## PART II: ACADEMIC CONTEXT MODULE

*Include for university capstone, thesis, or course projects.*

### 10. Academic Context

#### 10.1 Institutional Information

| Institution   | [University Name]        |
|---------------|--------------------------|
| Department    | [Department Name]        |
| Program       | [Degree Program]         |
| Course Code   | [e.g., COM8090]          |
| Academic Year | [e.g., 2026-2027]        |
| Semester      | [Fall / Spring / Summer] |
| Credit Hours  | [Number]                 |

#### 10.2 Academic Supervision

| **Role**        | **Name**   | **Title**   | **Email**   | **BRSF Role**   |
|-----------------|------------|-------------|-------------|-----------------|
| Primary Advisor | [Name]     | [Title]     | [Email]     | Mission owner   |
| Co-Advisor      | [Name]     | [Title]     | [Email]     | Scope reviewer  |
| Industry Mentor | [Name]     | [Title]     | [Email]     | Benefit owner   |

#### 10.3 Student Team

| **Student ID**   | **Name**   | **Role**       | **Email**   | **Objective &amp; Feature Ownership**   |
|------------------|------------|----------------|-------------|-----------------------------------------|
| [ID]             | [Name]     | Lead / PM      | [Email]     | O1, O6 / EP-1                           |
| [ID]             | [Name]     | Developer      | [Email]     | O2, O3 / EP-2, EP-3                     |
| [ID]             | [Name]     | Analyst / Test | [Email]     | O4, O5 / EP-4                           |

#### 10.4 Learning Objectives (aligned to BRSF Goals)

| **LO-ID**   | **Learning Objective**   | **Bloom Level**     | **Assessment Method**   | **BRSF Goal**   |
|-------------|--------------------------|---------------------|-------------------------|-----------------|
| LO-1        | [Knowledge objective]    | Remember/Understand | [Method]                | G1              |
| LO-2        | [Skill objective]        | Apply/Analyse       | [Method]                | G2              |
| LO-3        | [Competency]             | Evaluate/Create     | [Method]                | G3, G4          |

#### 10.5 Academic Milestones (aligned to Gates and BRSF Objectives)

*[ Milestones must match the gate schedule in Section 0.6c. ]*

| **Milestone**      | **Type**     | **Date**   | **Weight**   | **Gate Ref**   | **BRSF Objective**            |
|--------------------|--------------|------------|--------------|----------------|-------------------------------|
| Proposal Defense   | Presentation | [Date]     | [%]          | G-0            | O1 (Mission + Scope approved) |
| Progress Review    | Presentation | [Date]     | [%]          | G-1, G-2       | O2-O4                         |
| Final Presentation | Presentation | [Date]     | [%]          | G-3            | O5                            |
| Final Report       | Document     | [Date]     | [%]          | G-4            | O6 (Launch Gate)              |

#### 10.6 Peer Evaluation Framework

| **Criterion**   | **Weight**   | **Description**                     | **Scale**   | **Objective Link**   |
|-----------------|--------------|-------------------------------------|-------------|----------------------|
| Task Completion | 25%          | Timely completion of assigned tasks | 1-5         | O1-O5                |
| Task Quality    | 25%          | Quality of work produced            | 1-5         | All objectives       |
| Collaboration   | 20%          | Teamwork and cooperation            | 1-5         | Team-level           |
| Communication   | 15%          | Effective communication             | 1-5         | Team-level           |
| Initiative      | 15%          | Proactive contributions             | 1-5         | Goal-level           |

## PART III: INDUSTRIAL CONTEXT MODULE

*Include for corporate, enterprise, or government projects.*

### 11. Industrial Context

#### 11.1 Business Context

*[ [Organisation, Business Unit, Sponsor, Owner, Project Type] ]*

#### 11.2 Budget

*[ [Labor, Infrastructure, Contingency, Total — aligned to Package schedule] ]*

#### 11.3 ROI Projection

*[ [Expected ROI, Payback Period, Cost Savings — linked to Benefits Register (0.6f)] ]*

## PART IV: STARTUP MODULE

*Include if commercialisation potential exists.*

### 12. Startup Assessment

#### 12.1 Viability Assessment

*[ [Problem Significance, Market Size, Innovation Level, Team Readiness — each 1-5] ]*

#### 12.2 IP Ownership

*[ [IP Type, Description, Ownership %, Protection Status] ]*

## PART V: GOVERNANCE MODULE

*Recommended for team projects.*

### 13. Extended Governance

#### 13.1 RACI Matrix (by Objective/Package)

| **Objective / Package**   | **Member 1**   | **Member 2**   | **Member 3**   | **Advisor**   |
|---------------------------|----------------|----------------|----------------|---------------|
| O1-O2 / PKG-1             | R,A            | C              | I              | C             |
| O3-O4 / PKG-2             | C              | R,A            | R              | I             |
| O5-O6 / PKG-3             | C              | C              | R,A            | A             |

#### 13.2 Accountability and Communication

*[ [Violation escalation table + meeting protocol] ]*

## PART VI: TECHNOLOGY MODULE

### 14. Technology Stack

#### 14.1 Technology Selection

| **Category**         | **Technology**   | **Version**   | **Justification**   | **Feature / Obj Ref**   |
|----------------------|------------------|---------------|---------------------|-------------------------|
| Programming Language | [Language]       | [Ver]         | [Why]               | F-1                     |
| Framework            | [Framework]      | [Ver]         | [Why]               | F-2                     |
| Semantic Store       | [Triplestore]    | [Ver]         | [Why]               | F-3                     |
| AI / ML              | [Framework]      | [Ver]         | [Why]               | F-4                     |
| CI/CD                | [Platform]       | [Ver]         | [Why]               | All PKGs                |

#### 14.2 Architecture Overview

*[ [High-level description. Reference scope areas S1-S6 and packages PKG-1 to PKG-3.] ]*

#### 14.3 Integration Points

*[ [System, Type, Protocol, Data Format, Authentication, Feature Ref] ]*

## PART VII: APPENDICES

### A. BRSF Glossary

| **Term**            | **BRSF Class / Property**                                                                 | **Definition (from backlog\_tbox\_v1\_87\_0.ttl)**                                                                  |
|---------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Mission             | backlog:Mission + hasMissionStatement                                                     | Why the development exists: the standing purpose that outlives any particular release.                              |
| ScopeStatement      | backlog:ScopeStatement + hasScopeExclusion                                                | Declared boundary: what it covers and what it has been deliberately decided not to cover.                           |
| ScopeDeliverable    | backlog:ScopeDeliverable + requiresDeliverable                                            | A capability the scope requires, enumerated before any WorkItem exists.                                             |
| ScopeExclusion      | backlog:ScopeExclusion + hasExclusionRationale                                            | An explicit, owner-decided record that a concern is out of scope, with reasoning.                                   |
| Goal                | backlog:Goal + contributesToMission                                                       | A durable outcome the product exists to achieve, stated in terms of the change it makes.                            |
| Objective           | backlog:Objective + fillsScope + hasBaselineValue + hasTargetValue + hasObjectiveDeadline | Measurable, time-bounded target advancing a goal. Without a metric it cannot be missed.                             |
| Backlog             | backlog:Backlog + WorkItem                                                                | The single ordered register of all work items for one product or development.                                       |
| Initiative          | backlog:Initiative + InitiativeKind                                                       | Portfolio-granularity work item expressing a strategic outcome spanning multiple epics.                             |
| Epic                | backlog:Epic + pursuesObjective                                                           | Large body of work decomposed across multiple features; completion closes a measurable gap.                         |
| Feature / PBI       | backlog:Feature + ProductBacklogItem                                                      | Coherent, demonstrable capability deliverable in a single iteration.                                                |
| Package             | backlog:Package + deliversPackage                                                         | A coherent group of work items that together deliver meaningful, deployable capability.                             |
| Roadmap             | backlog:Roadmap + RoadmapHorizon                                                          | Derived, time-ordered view over a backlog by horizon (Now/Next/Later) and milestone.                                |
| Milestone           | backlog:Milestone + contributesToMilestone                                                | Named point of external significance whose achievement is determined by a gate passing.                             |
| ReleaseGate         | backlog:ReleaseGate + hasGateCommand + hasGateResult                                      | One check that must pass before a milestone state is trusted. Carries an executable command and an expected result. |
| Benefit             | backlog:Benefit + hasBenefitOwner                                                         | Specific improvement expected from completing work, owned by a named stakeholder.                                   |
| DefinitionOfDone    | backlog:DefinitionOfDone + DoDCriterion                                                   | Standing criteria every work item must satisfy before entering Done state.                                          |
| RICE Score          | backlog:RICEScore                                                                         | R×I×C / E, optionally multiplied by DepFactor. Advisory at proposal stage.                                          |
| DepFactor           | backlog:hasDepFactor                                                                      | Multiplier (0-1) reflecting dependency burden. 1.0 = no blocking dependencies.                                      |
| Commitment          | backlog:Commitment + commitsToGoal + commitsToObjective                                   | What an artifact commits to, against which progress is measured.                                                    |
| hasState (Proposed) | backlog:LifecycleState                                                                    | WorkItem or container lifecycle state. Proposed = not yet Ready or In Progress.                                     |

### B. Domain Glossary

| **Term**   | **Definition**   |
|------------|------------------|
| [Term 1]   | [Definition]     |
| [Term 2]   | [Definition]     |

### C. References

*[ [Full citations for all foundational works, standards, tools, and datasets referenced in the proposal.] ]*

### D. Document History

|   **Version** | **Date**   | **Author**   | **Changes**     |
|---------------|------------|--------------|-----------------|
|           1.0 | [Date]     | [Author]     | Initial version |
|           1.1 | [Date]     | [Author]     | [Changes]       |

### E. Approval Signatures

| **Role**               | **Name**   | **Signature**   | **Date**   |
|------------------------|------------|-----------------|------------|
| Project Manager / Lead | [Name]     |                 | [Date]     |
| Technical Lead         | [Name]     |                 | [Date]     |
| Sponsor / Advisor      | [Name]     |                 | [Date]     |

*BRSF-Aligned Modular Template v6.0  —  Ontology alignment: Part 0 → backlog\_tbox\_v1\_87\_0.ttl (backlog:Mission, ScopeStatement, Goal, Objective, ProductBacklogItem, Package, Roadmap, Milestone, ReleaseGate, Benefit)  ·  Parts I-VI → pp-core, pp-academic, pp-industrial, pp-startup, pp-governance, pp-tech-**