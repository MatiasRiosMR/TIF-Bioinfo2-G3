set -e
true
true
/usr/bin/python3 /usr/share/spades/spades_pipeline/scripts/preprocess_contigs.py --args_filename /home/matias/Escritorio/TP_Set3/spades_hybrid/split_input/tmp/contigs --dst /home/matias/Escritorio/TP_Set3/spades_hybrid/split_input --threshold_for_breaking_additional_contigs 10
true
true
/usr/libexec/spades/spades-core /home/matias/Escritorio/TP_Set3/spades_hybrid/K21/configs/config.info /home/matias/Escritorio/TP_Set3/spades_hybrid/K21/configs/isolate_mode.info
/usr/libexec/spades/spades-core /home/matias/Escritorio/TP_Set3/spades_hybrid/K33/configs/config.info /home/matias/Escritorio/TP_Set3/spades_hybrid/K33/configs/isolate_mode.info
/usr/libexec/spades/spades-core /home/matias/Escritorio/TP_Set3/spades_hybrid/K55/configs/config.info /home/matias/Escritorio/TP_Set3/spades_hybrid/K55/configs/isolate_mode.info
/usr/libexec/spades/spades-core /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/configs/config.info /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/configs/isolate_mode.info
/usr/bin/python3 /usr/share/spades/spades_pipeline/scripts/copy_files.py /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/before_rr.fasta /home/matias/Escritorio/TP_Set3/spades_hybrid/before_rr.fasta /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/assembly_graph_after_simplification.gfa /home/matias/Escritorio/TP_Set3/spades_hybrid/assembly_graph_after_simplification.gfa /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/final_contigs.fasta /home/matias/Escritorio/TP_Set3/spades_hybrid/contigs.fasta /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/first_pe_contigs.fasta /home/matias/Escritorio/TP_Set3/spades_hybrid/first_pe_contigs.fasta /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/strain_graph.gfa /home/matias/Escritorio/TP_Set3/spades_hybrid/strain_graph.gfa /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/scaffolds.fasta /home/matias/Escritorio/TP_Set3/spades_hybrid/scaffolds.fasta /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/scaffolds.paths /home/matias/Escritorio/TP_Set3/spades_hybrid/scaffolds.paths /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/assembly_graph_with_scaffolds.gfa /home/matias/Escritorio/TP_Set3/spades_hybrid/assembly_graph_with_scaffolds.gfa /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/assembly_graph.fastg /home/matias/Escritorio/TP_Set3/spades_hybrid/assembly_graph.fastg /home/matias/Escritorio/TP_Set3/spades_hybrid/K77/final_contigs.paths /home/matias/Escritorio/TP_Set3/spades_hybrid/contigs.paths
true
/usr/bin/python3 /usr/share/spades/spades_pipeline/scripts/breaking_scaffolds_script.py --result_scaffolds_filename /home/matias/Escritorio/TP_Set3/spades_hybrid/scaffolds.fasta --misc_dir /home/matias/Escritorio/TP_Set3/spades_hybrid/misc --threshold_for_breaking_scaffolds 3
true
