$py_files = Get-ChildItem -Path .\bot -filter *.py
foreach ($py_file in $py_files) {
	python .\i18n\pygettext.py -d $py_file.baseName -o ".\locales\$($py_file.baseName).pot" $py_file.FullName
}
$pot_files = Get-ChildItem -Path .\locales -filter *.pot
$locale_folders = Get-ChildItem -Path .\locales -Directory
foreach ($pot_file in $pot_files) { 
	$content = (Get-Content -Raw $pot_file.FullName) -replace 'cp1251','UTF-8'
	[IO.File]::WriteAllLines($pot_file.FullName, $content)
	foreach ($folder in $locale_folders) {
		Copy-Item $pot_file.FullName -Destination "$($folder.FullName)\LC_MESSAGES\$($pot_file.baseName).po"
	}
}
echo "Press any key to finish..."
$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")