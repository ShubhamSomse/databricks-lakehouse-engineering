# Architecture and engineering decisions

## 1. Scope

InsureAI is a portfolio-grade P&C insurance lakehouse using generated data. The engineering platform is the primary deliverable; insurance is the realistic domain used to exercise it. No employer or customer data is permitted.

## 2. Medallion layers

### Bronze
- Land source records with minimal transformation.
- Add `_source_file`, `_ingested_at`, and `_run_id`.
- Preserve source values and ingestion traceability.
- Make ingestion repeatable and observable.

### Silver
- Normalize types, timestamps, codes, and identifiers.
- Apply entity-specific required-field and domain checks.
- Deduplicate using business keys and deterministic ordering.
- Model changing dimensions with SCD Type 2 where history matters.
- Quarantine invalid records rather than silently discarding them.

### Gold
- Claim 360: claim, policy, claimant/customer, transactions, notes, documents.
- Policy 360: policy, customer, coverage and claims history.
- Customer 360: policy and loss experience.
- Fraud feature mart: explainable, time-aware indicators with leakage controls.
- AI retrieval corpus: approved claim text, metadata, chunk IDs and access labels.

## 3. AI scope

### Predictive analytics
Start with transparent baseline features and evaluation before model complexity:
- claim frequency and severity trends,
- time between policy inception and incident,
- repeated loss locations or contact details,
- payment / reserve movement patterns,
- historical claim similarity features.

Use chronological splits and avoid using post-outcome fields as predictors. Fraud labels are synthetic and model outputs must be treated as experimental.

### GenAI / RAG
- Prepare notes and document text as governed, claim-linked source records.
- Chunk with stable IDs and retain document / claim / timestamp metadata.
- Embeddings and vector search are a later optional stage, depending on workspace capability.
- Evaluate retrieval quality and answer grounding; never treat generated summaries as authoritative claim decisions.

## 4. Execution portability

Core configuration and validation are plain Python. Spark-specific code is imported only by the Spark ingestion module. This lets lightweight tests run without Spark installed. Databricks notebooks and cloud storage adapters will be added as separate execution adapters.

## 5. Initial table naming

Use `<layer>_<entity>` names in the starter implementation. A production deployment should place these in governed catalogs and schemas, with access controls and retention policies.

## 6. Non-functional requirements

- Idempotency: reruns must not create uncontrolled duplicate business records.
- Observability: every run carries a run ID and audit metadata.
- Data quality: explicit pass/fail results and quarantine counts.
- Security: least privilege, synthetic fixtures, and no secrets in source control.
- Reproducibility: pinned or bounded dependencies and deterministic test fixtures.
