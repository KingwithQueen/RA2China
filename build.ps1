param([switch]$DebugBuild, [switch]$AddressSanitizer)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$out = Join-Path $root 'build'
if ($AddressSanitizer) { $out = Join-Path $out 'asan' }
elseif ($DebugBuild) { $out = Join-Path $out 'debug' }
New-Item -ItemType Directory -Path $out -Force | Out-Null
$env:TEMP = $out
$env:TMP = $out
if (-not (Get-Command cl.exe -ErrorAction SilentlyContinue)) {
    $vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
    if (-not (Test-Path -LiteralPath $vswhere)) { throw 'MSVC Build Tools are required.' }
    $installation = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    if (-not $installation) { throw 'No MSVC C toolchain found.' }
    $vcvars = Join-Path $installation 'VC\Auxiliary\Build\vcvars64.bat'
    $command = '"' + $vcvars + '" >nul && set'
    $environment = & $env:ComSpec /d /s /c $command
    if ($LASTEXITCODE) { throw 'Unable to configure MSVC.' }
    foreach ($line in $environment) {
        if ($line -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process') }
    }
}
$common = @('/nologo','/std:c17','/TC','/W4','/WX','/utf-8','/MT','/Zi',('/I' + (Join-Path $root 'include')),('/I' + (Join-Path $root 'src')))
if ($DebugBuild) { $common += @('/Od','/D_DEBUG') } else { $common += '/O2' }
if ($AddressSanitizer) { $common += '/fsanitize=address' }
$sources = @('core','crypto','mix','vfs','ini','rules','rules_schema','rules_json','pal','shp','csf','asset_profile','vxl','hva','vpl','voxel_render','voxel_scene','map_pack','tmp','map','map_scene','map_render','battle','battle_layers','battle_bridges','battle_matrix','battle_motion','battle_tracks','battle_target','battle_number','battle_ballistics','battle_rules','battle_missions','battle_combat','battle_replay','battle_economy','battle_economy_hash','battle_people','battle_sea_air','battle_campaign','battle_campaign_hash','battle_infantry_scene','battle_campaign_report','battle_economy_scene','battle_structures','structure_scene','battle_scenario','battle_scene') | ForEach-Object { Join-Path $root ('src\' + $_ + '.c') }
Push-Location $out
try {
    & cl.exe @common /c @sources
    if ($LASTEXITCODE) { throw 'C library compilation failed.' }
    $objects = @('core.obj','crypto.obj','mix.obj','vfs.obj','ini.obj','rules.obj','rules_schema.obj','rules_json.obj','pal.obj','shp.obj','csf.obj','asset_profile.obj','vxl.obj','hva.obj','vpl.obj','voxel_render.obj','voxel_scene.obj','map_pack.obj','tmp.obj','map.obj','map_scene.obj','map_render.obj','battle.obj','battle_layers.obj','battle_bridges.obj','battle_matrix.obj','battle_motion.obj','battle_tracks.obj','battle_target.obj','battle_number.obj','battle_ballistics.obj','battle_rules.obj','battle_missions.obj','battle_combat.obj','battle_replay.obj','battle_economy.obj','battle_economy_hash.obj','battle_people.obj','battle_sea_air.obj','battle_campaign.obj','battle_campaign_hash.obj','battle_infantry_scene.obj','battle_campaign_report.obj','battle_economy_scene.obj','battle_structures.obj','structure_scene.obj','battle_scenario.obj','battle_scene.obj')
    & lib.exe /nologo /OUT:ra2resources.lib @objects
    if ($LASTEXITCODE) { throw 'Static library creation failed.' }
    & cl.exe @common (Join-Path $root 'src\tool.c') /Fe:ra2tool.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Resource tool compilation failed.' }
    if (Test-Path -LiteralPath (Join-Path $root 'tests\test_main.c')) {
        & cl.exe @common (Join-Path $root 'tests\test_main.c') /Fe:ra2tests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
        if ($LASTEXITCODE) { throw 'Test compilation failed.' }
    }
    if (Test-Path -LiteralPath (Join-Path $root 'tests\rules_test.c')) {
        & cl.exe @common (Join-Path $root 'tests\rules_test.c') /Fe:ra2rulestests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
        if ($LASTEXITCODE) { throw 'Rule test compilation failed.' }
    }
    & cl.exe @common (Join-Path $root 'src\assetcheck.c') /Fe:ra2assetcheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Asset corpus tool compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\assets_test.c') /Fe:ra2assettests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Asset test compilation failed.' }
    & cl.exe @common (Join-Path $root 'src\viewer.c') /Fe:ra2viewer.exe /link ra2resources.lib user32.lib gdi32.lib comdlg32.lib dwmapi.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Resource viewer compilation failed.' }
    & cl.exe @common (Join-Path $root 'src\voxelcheck.c') /Fe:ra2voxelcheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Voxel corpus compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\voxel_test.c') /Fe:ra2voxeltests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Voxel tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'src\voxel_viewer.c') /Fe:ra2voxelviewer.exe /link ra2resources.lib user32.lib gdi32.lib comdlg32.lib dwmapi.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Voxel viewer compilation failed.' }
    & cl.exe @common (Join-Path $root 'src\mapcheck.c') /Fe:ra2mapcheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Map corpus compilation failed.' }
    & cl.exe @common (Join-Path $root 'src\map_viewer.c') /Fe:ra2mapviewer.exe /link ra2resources.lib user32.lib gdi32.lib comdlg32.lib dwmapi.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Map viewer compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\map_test.c') /Fe:ra2maptests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Map test compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\battle_test.c') /Fe:ra2battletests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Battle tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\combat_test.c') /Fe:ra2combattests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Combat tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\missions_test.c') /Fe:ra2missiontests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Mission tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\physics_test.c') /Fe:ra2physicstests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Physics tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\locomotor_test.c') /Fe:ra2locomotortests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Locomotor tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\bridges_test.c') /Fe:ra2bridgetests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Bridge tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\layers_test.c') /Fe:ra2layerstests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Layer tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\calibration_vectors.c') /Fe:ra2calibrationcheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Calibration vectors compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\motion_vectors.c') /Fe:ra2motioncheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Motion vectors compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\bridge_mapcheck.c') /Fe:ra2bridgemapcheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Original broken bridge map check compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\render_test.c') /Fe:ra2rendertests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Render geometry tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'src\battlecheck.c') /Fe:ra2battlecheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Battle corpus compilation failed.' }
    & cl.exe @common (Join-Path $root 'src\battle_viewer.c') /Fe:ra2battle.exe /link ra2resources.lib user32.lib gdi32.lib comdlg32.lib dwmapi.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Battle viewer compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\structures_test.c') /Fe:ra2structuretests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Structure tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'src\structurecheck.c') /Fe:ra2structurecheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Scenario corpus tool compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\economy_test.c') /Fe:ra2economytests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Economy tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'src\campaigncheck.c') /Fe:ra2campaigncheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Campaign check compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\campaign_test.c') /Fe:ra2campaigntests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Campaign tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\infantry_asset_check.c') /Fe:ra2infantrycheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Infantry resource check compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\sea_air_test.c') /Fe:ra2seaairtests.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Sea and air tests compilation failed.' }
    & cl.exe @common (Join-Path $root 'src\firstmissioncheck.c') /Fe:ra2firstmissioncheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'First mission check compilation failed.' }
    & cl.exe @common (Join-Path $root 'tests\sea_air_assets.c') /Fe:ra2seaaircheck.exe /link ra2resources.lib /INCREMENTAL:NO /DEBUG
    if ($LASTEXITCODE) { throw 'Sea and air asset check compilation failed.' }
    if ($AddressSanitizer) {
        $compilerFolder = Split-Path (Get-Command cl.exe).Source
        Get-ChildItem -LiteralPath $compilerFolder -Filter 'clang_rt.asan*.dll' -File |
            ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $out -Force }
    }
} finally { Pop-Location }




