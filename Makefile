.PHONY: preview wallpaper

# Real Omarchy staging in an isolated HOME; never changes the running desktop.
preview:
	python3 scripts/preview.py $(ARGS)

# Rebuild the distributable 4K wallpapers from their editable sources.
wallpaper:
	python3 scripts/clawd_wallpapers.py
