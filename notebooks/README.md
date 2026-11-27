# Databricks notebooks

Notebook entry points will be added after the framework and local tests are established. Planned notebooks:

1. 01_bronze_ingestion
2. 02_silver_conformance_and_quality
3. 03_scd_type_2_dimensions
4. 04_gold_claim_360
5. 05_fraud_feature_engineering
6. 06_ai_ready_claim_corpus

Keep business logic in `src/insureai/` where practical so it can be tested independently of notebook state.
