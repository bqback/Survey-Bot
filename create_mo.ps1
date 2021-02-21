$locale_folders = Get-ChildItem -Path .\locales -Directory
foreach ($folder in $locale_folders) {
	$po = Get-ChildItem -Path "$($folder.FullName)\LC_MESSAGES\" -filter *.po
	echo $po
	foreach ($file in $po) {
		python .\i18n\msgfmt.py -o "$($folder.FullName)\LC_MESSAGES\$($file.baseName).mo" $file.FullName
	}
}
echo "Press any key to finish..."
$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")