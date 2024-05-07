# swinno-bioeconomy-directionality
## Quantifying Directionality and Innovation Output in Sweden’s Transition to a Forest-Based Bioeconomy
This repo holds code to reproduce the paper and additional code to help in the classification of sources.
Due to copyright of the source articles, only data needed to reproduce the paper is included.

### Abstract
> The transition to a bioeconomy is high on the agenda for research, industry and policy. Like other sustainability transition, the bioeconomy transition is characterized by contes- tation over desired outcomes and transition pathways. While shared visions are seen as pivotal in guiding transitions, the bioeconomy discourse is marked by the contention of three competing visions. The Swedish forest-based bioeconomy is well established as a case study in this arena. Yet, knowledge about innovation produced across the entire system is scarce. The use of detailed innovation data from a Swedish literature-based innovation output database, SWINNO, allows to capture the actual innovation output of the Swedish forest-based bioeconomy innovation system. Qualitative coding of the source material links innovation from 1970 to 2021 with visions of a bioresource, biotechnology and / or bioe- cology bioeconomy. Findings reveal a decrease in the innovation output of the forest-based bioeconomy relative to Sweden’s overall commercialized innovation. Notably, innovations associated with a bioresource vision surged during the energy crises of the 1970s, pre-dating their formalization in strategy documents, suggesting a significant role for path-dependency in shaping shared visions. Concurrently, the presence of innovations aligning with multiple visions indicates an open opportunity space for future development across various directions. This research underscores the dynamic interplay between historical contexts, shared visions, and innovation trajectories within the bioeconomy transition, and questions the extent to which visions can provide novel directionality to transitions.

### Reproduction

To reproduce the paper follow these steps:

1. Make sure that you have Python 3, R 4.0, and Quarto 1.4 installed.
2. Install python dependencies by creating a virtual environment and install requirements.txt.
    Some plots additionally depend on these R packages:
    * dplyr
    * ggplot2
    * scales
    * patchwork
    * showtext
    * paletteer
    * rio
    * here
    * hrbrthemes
    * stringr

3. If you are on a unix based OS, you can now simply run `make paper`.
    On Windows you need to render the paper.qmd file by either navigating to it and rendering it from your favorite IDE, or by running 
    `quarto render paper.qmd -o "pjk_draft_directionality.pdf" from the command line.


## Finding Source Articles

> [!NOTE]
> This will only work if you have set up correct links to the shared drive hosting source images.

1. run scripts/get_sinno_id_for_images.py

    this creates a text file with sinno ids for finding the source images in results/bioeconomy_definitions/ with the date on which the script was run and an excel file in data/raw-data for classification

2. run scripts/find_sources with .txt of sinno_ids as input 

both steps can be run with `make filter_and_find`.
