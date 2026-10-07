from collections import Counter
from math import log2
from music21 import converter
from pathlib import Path
import sys

import matplotlib.pyplot as plt

def get_key_corr(file_path):
    score = converter.parse(file_path)
    key = score.analyze('key')
    return (key, key.correlationCoefficient)

def get_windowed_key_corr(file_path, window_size=16):
    score = converter.parse(file_path)
    key_corrs = []
    
    for measure in score.parts[0].getElementsByClass('Measure'):
        k = measure.analyze('key')
        key_corrs.append((k, k.correlationCoefficient))
    
    return key_corrs

def pitch_class_entropy(file_path):
    score = converter.parse(file_path)
    pitch_classes = []
    for note in score.recurse().notes:
        if note.isNote:
            pitch_classes.append(note.pitch.pitchClass)
        elif note.isChord:
            for pitch in note.pitches:
                pitch_classes.append(pitch.pitchClass)
    
    counts = Counter(pitch_classes)
    total = sum(counts.values())
    entropy = -sum((count / total) * log2(count / total) for count in counts.values())

    return entropy

def main():
    dir_path = sys.argv[1] if len(sys.argv) > 1 else "./midi"
    dir_path = Path(dir_path)

    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.csv"

    key_corrs = {}
    pces = {}

    with open(output_path, "w") as f:
        f.write("File,Preset,Key,Correlation,Pitch_Class_Entropy\n")
        for file in dir_path.glob("*.mid"):
            preset = file.stem.split("_")[0]
            key, corr = get_key_corr(file)
            entropy = pitch_class_entropy(file)

            if preset not in key_corrs:
                key_corrs[preset] = []
            if preset not in pces:
                pces[preset] = []

            key_corrs[preset].append(corr)
            pces[preset].append(entropy)

            # windowed correlation analysis and graphing - commented out for now 
            # due to time consuming nature
            # with open("windowed_output.csv", "a") as wf:
            #     windowed_corrs = get_windowed_key_corr(file)
            #     for w_key, w_corr in windowed_corrs:
            #         wf.write(f"{file.name},{preset},{w_key},{w_corr}\n")

            #     measures = [i for i in range(len(windowed_corrs))]
            #     keys = [w_key for w_key, _ in windowed_corrs]

            #     output_dir = Path("windowed_corr_graphs")
            #     output_dir.mkdir(exist_ok=True)
            #     plt.plot(measures, [w_corr for _, w_corr in windowed_corrs], label=file.name)

            #     # for annotating key but results in cluttered mess so commented out for now
            #     # for i, key in enumerate(keys):
            #     #     plt.annotate(
            #     #         str(key), 
            #     #         (measures[i], windowed_corrs[i][1]), 
            #     #         textcoords="offset points", 
            #     #         xytext=(0,10), 
            #     #         ha='center')

            #     plt.xlabel("Measure")
            #     plt.ylabel("Key Correlation Coefficient")
            #     plt.title(f"Windowed Key Correlation for {file.name}")
            #     plt.legend()
            #     save_path = output_dir / f"{file.stem}_windowed_corr.png"
            #     plt.savefig(save_path)
            #     plt.clf()

            print(f"{file.name}: Key={key}, Correlation={corr:.4f}, Pitch Class Entropy={entropy:.4f}")
            f.write(f"{file.name},{preset},{key},{corr},{entropy}\n")

    print("\nAverage Key Correlation Coefficients:")
    for preset, corrs in key_corrs.items():
        print(f"  {preset}: {sum(corrs) / len(corrs):.4f}")
    print("\nAverage Pitch Class Entropies:")
    for preset, entropies in pces.items():
        print(f"  {preset}: {sum(entropies) / len(entropies):.4f}")

    print("\nStandard Deviation of Key Correlation Coefficients:")
    for preset, corrs in key_corrs.items():
        print(f"  {preset}: {sum((x - sum(corrs)/len(corrs))**2 for x in corrs) / len(corrs) ** 0.5:.4f}")
    print("\nStandard Deviation of Pitch Class Entropies:")
    for preset, entropies in pces.items():
        print(f"  {preset}: {sum((x - sum(entropies)/len(entropies))**2 for x in entropies) / len(entropies) ** 0.5:.4f}")
        
if __name__ == "__main__":
    main()