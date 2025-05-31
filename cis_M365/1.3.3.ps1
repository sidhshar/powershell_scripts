Import-Module "C:\Modules\ExchangeOnlineManagement\3.8.0\ExchangeOnlineManagement.psd1"

# Import the Exchange Online module
# Check if already connected to Exchange Online
if (-not (Get-ConnectionInformation)) {
    Write-Host "Connecting to Exchange Online..."
    Connect-ExchangeOnline
} else {
    Write-Host "Already connected to Exchange Online. Reusing session..."
}

# Get the Sharing policy
Get-SharingPolicy -Identity "Default Sharing Policy"
