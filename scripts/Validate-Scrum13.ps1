# Local validation only. Does not authenticate, deploy, or call AWS.
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$taskLint = Join-Path $taskRoot '.venv\Scripts\cfn-lint.exe'
$taskGuard = Join-Path $taskRoot '.tools\cfn-guard\cfn-guard-v3-x86_64-windows-latest\cfn-guard.exe'
$taskTemplate = Join-Path $taskRoot 'infrastructure\cloudformation\week1\security.yaml'
$taskRules = Join-Path $PSScriptRoot 'validation\scrum-13.guard'
foreach ($taskFile in @($taskLint, $taskGuard, $taskTemplate, $taskRules)) {
    if (-not (Test-Path -LiteralPath $taskFile -PathType Leaf)) {
        throw "Required file missing: $taskFile. See docs/week1/SCRUM-13-security-controls.md."
    }
}
& $taskLint --format json --regions us-east-2 -- $taskTemplate
if ($LASTEXITCODE -ne 0) { throw "cfn-lint failed with exit code $LASTEXITCODE" }
& $taskGuard validate --rules $taskRules --data $taskTemplate --output-format json --show-summary none
if ($LASTEXITCODE -ne 0) { throw "cfn-guard failed with exit code $LASTEXITCODE" }
