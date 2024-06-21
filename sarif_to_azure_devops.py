import json, os

def parse_sarif(sarif_file):
    """Parse the SARIF file and return findings."""
    with open(sarif_file, 'r') as file:
        sarif_data = json.load(file)
    
    findings = []
    for run in sarif_data.get('runs', []):
        for result in run.get('results', []):
            finding = {
                'rule_id': result.get('ruleId'),
                'message': result.get('message', {}).get('text'),
                'severity': result.get('level'),
                'location': result.get('locations', [{}])[0].get('physicalLocation', {}).get('artifactLocation', {}).get('uri'),
                'line': result.get('locations', [{}])[0].get('physicalLocation', {}).get('region', {}).get('startLine', 0),
            }
            findings.append(finding)
    return findings

def convert_findings_to_azure_devops_commands(findings, repo_url):
    """Convert findings to Azure DevOps logging commands with clickable links."""
    for finding in findings:
        # Customize the logging command based on your needs. This example logs a warning.
        severity = 'warning' if finding['severity'] == 'warning' else 'error'
        
        # Construct the URL to the file and line in your repository
        # This example URL format is for GitHub. Adjust it according to your repo's hosting service.
        file_path = finding['location'].replace('\\', '/')
        line_number = finding['line']
        # Ensure your repo_url does not end with a slash
        file_url = f"{repo_url}?path=/{file_path}&version=GBmain&line={line_number+1}&lineEnd={line_number+2}&lineStartColumn=1&lineEndColumn=1&lineStyle=plain&_a=contents"
        
        # Embed the URL in the message
        message = f"{finding['rule_id']}: {finding['message']} at {finding['location']}:{finding['line']}  |  {file_url}"
        
        print(f"##vso[task.logissue type={severity}]{message}")


if __name__ == "__main__":
    sarif_file_path = 'results.sarif'  # Update this to your SARIF file path
    findings = parse_sarif(sarif_file_path)
    # Retrieve the repository URL from the Azure DevOps environment variable
    repo_url = os.getenv('BUILD_REPOSITORY_URI', 'https://dev.azure.com/nightvision1/_git/java-test')
    if "@" in repo_url:
        repo_url = "https://" + repo_url.split("@")[1]

    convert_findings_to_azure_devops_commands(findings, repo_url)
