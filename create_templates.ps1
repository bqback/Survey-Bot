# This script generates .pot templates, resaves them with proper encoding and places .po copies in every locale directory

# Get all .py files
$py_files = Get-ChildItem -Path .\bot -filter *.py
# Cycle over them
foreach ($py_file in $py_files) {
	# Generate .pot files
	python .\i18n\pygettext.py -d $py_file.baseName -o ".\locales\$($py_file.baseName).pot" $py_file.FullName
}
# Get all .pot files
$pot_files = Get-ChildItem -Path .\locales -filter *.pot
# Get all locale folders
$locale_folders = Get-ChildItem -Path .\locales -Directory
# Cycle over .pot files
foreach ($pot_file in $pot_files) { 
	# Open the file and replace the automatically detected encoding
	$content = (Get-Content -Raw $pot_file.FullName) -replace 'cp1251','UTF-8'
	# Resave in UTF-8
	[IO.File]::WriteAllLines($pot_file.FullName, $content)
	# Cycle over locale folders
	foreach ($folder in $locale_folders) {
		# Copy resulting .pot file as .po
		Copy-Item $pot_file.FullName -Destination "$($folder.FullName)\LC_MESSAGES\$($pot_file.baseName).po"
	}
}

echo "Press any key to finish..."
$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")