$ErrorActionPreference='Stop'
$taskPython='E:\Program Files\Python\python.exe'
& $taskPython -B (Join-Path $PSScriptRoot 'normalize_generated_v18.py') prepare
if($LASTEXITCODE){throw 'Source preservation preparation failed'}
$taskVs='E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$taskJobs=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'evidence/movement-state-v18/investigations/line-ending-build/jobs.json') -Raw | ConvertFrom-Json
Push-Location (Join-Path $PSScriptRoot 'ra2/build-original-c')
try {
 foreach($taskJob in $taskJobs){
  try {
   $taskArgs=@($taskJob.args);& cl @taskArgs
   if($LASTEXITCODE){throw 'Isolated source compilation failed'}
   Copy-Item -LiteralPath $taskJob.original_object -Destination $taskJob.output -Force
  } finally {Copy-Item -LiteralPath $taskJob.object_backup -Destination $taskJob.original_object -Force}
 }
 & $taskPython -B (Join-Path $PSScriptRoot 'normalize_generated_v18.py') finish
 if($LASTEXITCODE){throw 'Source equivalence proof failed'}
} catch {
 foreach($taskJob in $taskJobs){
  Copy-Item -LiteralPath $taskJob.backup -Destination $taskJob.source -Force
  Copy-Item -LiteralPath $taskJob.object_backup -Destination $taskJob.original_object -Force
 }
 throw
} finally {Pop-Location}
