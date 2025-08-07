$CustomPath = "C:\Modules"
New-Item -ItemType Directory -Path $CustomPath -Force

Import-Module "C:\Modules\ExchangeOnlineManagement\3.8.0\ExchangeOnlineManagement.psd1"

# Import the Exchange Online module
# Check if already connected to Exchange Online
if (-not (Get-ConnectionInformation)) {
    Write-Host "Connecting to Exchange Online..."
    Connect-ExchangeOnline
} else {
    Write-Host "Already connected to Exchange Online. Reusing session..."
}

Get-EXOMailbox | Select-Object -Unique RoleAssignmentPolicy | ForEach-Object { Get-RoleAssignmentPolicy -Identity $_.RoleAssignmentPolicy | Where-Object {$_.AssignedRoles -like "*Apps*"} } | Select-Object Identity, @{Name="AssignedRoles"; Expression={ Get-Mailbox | Select-Object -Unique RoleAssignmentPolicy | ForEach-Object { Get-RoleAssignmentPolicy -Identity $_.RoleAssignmentPolicy | Select-Object -ExpandProperty AssignedRoles | Where-Object {$_ -like "*Apps*"} } }}
