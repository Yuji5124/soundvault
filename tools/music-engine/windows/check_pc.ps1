# MONQUE SOUND LAB - Windows PC check (read-only: installs and changes nothing)
# Run:  powershell -ExecutionPolicy Bypass -File .\check_pc.ps1
# Writes pc_report.json next to this script. Paste or attach it back to Claude.

$ErrorActionPreference = 'SilentlyContinue'
$report = [ordered]@{}

$os = Get-CimInstance Win32_OperatingSystem
$report.os = "$($os.Caption) $($os.Version) ($($os.OSArchitecture))"

$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$report.cpu = [ordered]@{ name = $cpu.Name.Trim(); cores = $cpu.NumberOfCores; threads = $cpu.NumberOfLogicalProcessors }

$report.ram_gb = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)

# Win32_VideoController caps AdapterRAM at 4 GB, so prefer nvidia-smi when present.
$report.gpus = @(Get-CimInstance Win32_VideoController | ForEach-Object {
  [ordered]@{ name = $_.Name; driver = $_.DriverVersion; adapter_ram_gb_capped = [math]::Round($_.AdapterRAM / 1GB, 1) }
})
$smi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if ($smi) {
  $report.nvidia_smi = @(& nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version,compute_cap --format=csv,noheader 2>$null)
  $report.cuda_from_smi = ((& nvidia-smi 2>$null) | Select-String 'CUDA Version: ([0-9.]+)').Matches.Groups[1].Value
} else {
  $report.nvidia_smi = 'not found (no NVIDIA GPU or driver)'
}

$report.disks = @(Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
  [ordered]@{ drive = $_.DeviceID; free_gb = [math]::Round($_.FreeSpace / 1GB, 1); size_gb = [math]::Round($_.Size / 1GB, 1) }
})

function Ver($cmd, $arg) { $c = Get-Command $cmd -ErrorAction SilentlyContinue; if ($c) { (& $cmd $arg 2>&1 | Select-Object -First 1).ToString() } else { 'not installed' } }
$report.tools = [ordered]@{
  python = Ver 'python' '--version'; py_launcher = Ver 'py' '--version'; uv = Ver 'uv' '--version'
  git = Ver 'git' '--version'; ffmpeg = Ver 'ffmpeg' '-version'; fluidsynth = Ver 'fluidsynth' '--version'; node = Ver 'node' '--version'
}
$report.long_paths_enabled = (Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name LongPathsEnabled).LongPathsEnabled
$report.checked_at = (Get-Date).ToString('s')

$out = Join-Path $PSScriptRoot 'pc_report.json'
$report | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $out
Get-Content $out
Write-Host "`nSaved: $out"
