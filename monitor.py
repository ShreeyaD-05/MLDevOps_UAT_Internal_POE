"""Evidently data-drift monitor: reference.csv vs current.csv."""
import os
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

ref = pd.read_csv("reference.csv")
cur = pd.read_csv("current.csv")

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref, current_data=cur)

os.makedirs("reports", exist_ok=True)
report.save_html("reports/drift_report.html")

res = next(m["result"] for m in report.as_dict()["metrics"] if m["metric"] == "DataDriftTable")
rows = []
for col, d in res["drift_by_columns"].items():
    rows.append({"column": col,
                 "drift_detected": d["drift_detected"],
                 "stat_test": d["stattest_name"],
                 "drift_score": round(d["drift_score"], 4)})
summary = pd.DataFrame(rows)
summary.to_csv("reports/drift_summary.csv", index=False)

print(summary.to_string(index=False))
print()
print("Columns drifted:", res["number_of_drifted_columns"], "/", res["number_of_columns"])
print("Dataset drift  :", res["dataset_drift"])
print("Saved: reports/drift_report.html and reports/drift_summary.csv")