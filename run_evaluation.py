from evaluation import CVEvaluator
import os
import json
import pandas as pd

# Paths
results_dir = "results"
ground_truth_path = "ground_truth.json"
evaluation_results = {}

# Init evaluator
evaluator = CVEvaluator(ground_truth_path, results_dir)

# Loop over all model result files
for file in os.listdir(results_dir):
    if file.endswith(".json"):
        cv_id = file.replace(".json", "")
        with open(os.path.join(results_dir, file), "r", encoding="utf-8") as f:
            model_results = json.load(f)
            scores = evaluator.evaluate_cv(cv_id, model_results)
            if scores:
                evaluation_results[cv_id] = scores

# Generate report and save as CSV
df = evaluator.generate_report(evaluation_results)
df.to_csv("evaluation_summary.csv", index=True)

print("✅ Evaluation complete!")
print("📄 Saved: evaluation_summary.csv")
print("📊 Saved: model_comparison_by_field.png")
print("🕸️  Saved: model_overall_performance.png")
