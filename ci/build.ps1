$sdir = $PSScriptRoot

cd "$sdir\..\"

pipenv install --dev
pipenv run pyinstaller "$sdir\..\canvas-downloader.py" --onedir --hidden-import=win32timezone --noconfirm