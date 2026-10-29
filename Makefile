.PHONY: preview wallpaper

# Real Omarchy staging in an isolated HOME; never changes the running desktop.
preview:
	python3 scripts/preview.py $(ARGS)

# Rebuild the distributable 4K wallpaper from its editable source.
wallpaper:
	rsvg-convert --output backgrounds/01-clay-horizon.png artwork/clay-horizon.svg
