import json
from datetime import datetime


def sarif_to_gitlab(sarif_file, output_file):
    # Load SARIF data
    with open(sarif_file, 'r') as file:
        sarif_data = json.load(file)

    # Initialize GitLab report structure
    gitlab_report = {
        "version": "15.0.0",
        "vulnerabilities": [],
        "remediations": [],
        "scan": {
            "scanner": {
                "id": "custom_sarif_import",
                "name": "Custom SARIF Importer",
                "version": "1.0",
                "vendor": {
                    "name": "Custom Vendor"  # Updated to be an object
                }
            },
            "analyzer": {
                "name": "Custom Analyzer",
                "version": "1.0",
                "id": "custom_analyzer",  # Example ID, adjust as needed
                "vendor": {
                    "name": "Custom Analyzer Vendor"  # Example vendor, adjust as needed
                }
            },
            "start_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "end_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "status": "success",
            "type": "sast"
        }
    }

    # Map SARIF data to GitLab format
    for run in sarif_data.get("runs", []):
        for result in run.get("results", []):
            vulnerability = {
                "id": result.get("ruleId"),
                "category": "sast",
                "name": result.get("message", {}).get("text"),
                "message": result.get("message", {}).get("text"),
                "description": result.get("message", {}).get("text"),
                "severity": map_severity(result.get("properties", {}).get("nightvision-risk")),  # Mapping function to ensure correct severity
                "confidence": result.get("properties", {}).get("nightvision-confidence"),
                "solution": "Please refer to the rule documentation.",
                "scanner": gitlab_report["scan"]["scanner"],
                "identifiers": [{"type": "cve", "name": result.get("ruleId"), "value": result.get("ruleId")}],
                "location": {
                    "file": result.get("locations", [{}])[0].get("physicalLocation", {}).get("artifactLocation", {}).get("uri"),
                }
            }
            # Conditionally add start and end lines if they are numbers
            if isinstance(result.get("locations", [{}])[0].get("physicalLocation", {}).get("region", {}).get("startLine"), int):
                vulnerability["location"]["start_line"] = result.get("locations", [{}])[0].get("physicalLocation", {}).get("region", {}).get("startLine")
            if isinstance(result.get("locations", [{}])[0].get("physicalLocation", {}).get("region", {}).get("endLine"), int):
                vulnerability["location"]["end_line"] = result.get("locations", [{}])[0].get("physicalLocation", {}).get("region", {}).get("endLine")

            gitlab_report["vulnerabilities"].append(vulnerability)

    # Write GitLab report to file
    with open(output_file, 'w') as file:
        json.dump(gitlab_report, file, indent=4)

def map_severity(sarif_severity):
    """Map SARIF severity to GitLab severity levels."""
    severity_mapping = {
        "CRITICAL": "Critical",
        "HIGH": "High",
        "MEDIUM": "Medium",
        "LOW": "Low",
        "INFO": "Info",
    }
    return severity_mapping.get(sarif_severity, "Unknown")

# Example usage
sarif_to_gitlab('results.sarif', 'gitlab_security_report.json')
