.PHONY: preview wallpaper

# Real Omarchy staging in an isolated HOME; never changes the running desktop.
preview:
	python3 scripts/preview.py $(ARGS)

# Rebuild the distributable 4K wallpapers and theme thumbnails for both variants.
wallpaper:
	python3 scripts/clawd_wallpapers.py --variant dark
	python3 scripts/clawd_wallpapers.py --variant light
	magick backgrounds/02-clawd-unit.png -resize 1280x720 preview.png
	magick light/backgrounds/02-clawd-unit.png -resize 1280x720 light/preview.png
