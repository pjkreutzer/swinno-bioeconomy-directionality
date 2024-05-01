.PHONY: all clean filter_bioeconomy filter_and_find pull_data

filter_bioeconomy:
	@echo "Filtering bioeconomy data"
	@python3 scripts/filter_bioeconomy.py

filter_and_find: filter_bioeconomy
	@echo "Finding source images"
	@python3 scripts/find_sources.py -i results/bioeconomy_definitions/$$(date +%Y%m%d)_bioeconomy-articles-to-check.txt -d data/raw-data/$$(date +%Y%m%d)_images

pull_data:
	@echo "Pulling data from SWINNO DB"
	@python3 scripts/analysis/00-pull_data.py

paper: 
	@echo "Creating paper..."
	@quarto render paper.qmd -o "$$(date '+%F')_pjk_draft_directionality.pdf"
