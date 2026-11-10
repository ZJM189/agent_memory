param([Parameter(Mandatory=$true)][string]$PptxPath,[Parameter(Mandatory=$true)][string]$OutputDir,[int]$Width=1920,[int]$Height=1080)
$ErrorActionPreference='Stop'
$source=(Resolve-Path -LiteralPath $PptxPath).Path
$target=[System.IO.Path]::GetFullPath($OutputDir)
New-Item -ItemType Directory -Force -Path $target | Out-Null
$ppt=$null;$deck=$null
try {
 $ppt=New-Object -ComObject PowerPoint.Application
 $deck=$ppt.Presentations.Open($source,$true,$false,$false)
 for($i=1;$i -le $deck.Slides.Count;$i++) {
  $dest=Join-Path $target ('slide-{0:D2}.png' -f $i)
  if(Test-Path -LiteralPath $dest){throw "Preview exists: $dest. Choose a new output directory."}
  $deck.Slides.Item($i).Export($dest,'PNG',$Width,$Height)
  Write-Output $dest
 }
} finally {
 if($null -ne $deck){$deck.Close();[void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($deck)}
 if($null -ne $ppt){$ppt.Quit();[void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt)}
}
