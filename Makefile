filter_bioeconomy:
	@echo "Filtering bioeconomy data"
	@python3 scripts/filter_bioeconomy.py

filter_and_find: filter_bioeconomy
	@echo "Finding source images"
	@python3 scripts/find_sources.py -i results/bioeconomy_definitions/$$(date +%Y%m%d)_bioeconomy-articles-to-check.txt -d data/raw-data/$$(date +%Y%m%d)_images
