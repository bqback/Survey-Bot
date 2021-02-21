# This script goes through every locale directory and generates .mo files required for gettext to function

# Get all locale directories
$locale_folders = Get-ChildItem -Path .\locales -Directory
# Cycle over them
foreach ($folder in $locale_folders) {
	# Get a list of .po files in the locale folder
	$po = Get-ChildItem -Path "$($folder.FullName)\LC_MESSAGES\" -filter *.po
	# Cycle over them
	foreach ($file in $po) {
		# Generate the respective .mo file
		python .\i18n\msgfmt.py -o "$($folder.FullName)\LC_MESSAGES\$($file.baseName).mo" $file.FullName
	}
}

echo "Press any key to finish..."
$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")