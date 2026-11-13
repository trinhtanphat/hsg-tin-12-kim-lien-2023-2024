$ErrorActionPreference = 'Stop'
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Python is required to run the local test suite.'
}
python (Join-Path $PSScriptRoot '..\tests\run_tests.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
