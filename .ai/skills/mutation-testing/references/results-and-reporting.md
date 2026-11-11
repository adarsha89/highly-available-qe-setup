# Mutation Results and Reporting

Detailed guidance for measuring, logging, and reporting outcomes from resilience and fault-injection testing.

## Key Metrics to Capture

1. **Detection Rate**: Percentage of injected faults that triggered their corresponding Prometheus / Alertmanager alerts within the defined SLA.
2. **Recovery Time Objective (RTO)**: The elapsed time in seconds from fault injection until the target pod / node / service returned to full health (`readinessProbe` passing, HTTP 200).
3. **Data Integrity / Zero Loss**: Verification that in-flight data, persistent volume claims, or JCasC states were not corrupted during recovery.
4. **Survivors / Undetected Faults**: Any scenario where a service degraded or failed without triggering an alert or failing health checks.

## Report Storage
Reports must be saved to:
`docs/mutation/<slug>-mutation-report.md`
