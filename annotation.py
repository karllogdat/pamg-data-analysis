import ast
import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path

def graph_va_timeline(df):
    v_output_dir = Path("valence_timeline")
    v_output_dir.mkdir(exist_ok=True)
    a_output_dir = Path("arousal_timeline")
    a_output_dir.mkdir(exist_ok=True)

    for _index, row in df.iterrows():
        name = row["file_path"].split("\\")[2]
        v_timeline = ast.literal_eval(row["valence_timeline"])
        a_timeline = ast.literal_eval(row["arousal_timeline"])

        plt.plot(v_timeline)
        plt.xlabel("Time Step")
        plt.ylabel("Valence")
        plt.title(f"Valence values over time for {name}")
        plt.legend()
        save_path = v_output_dir / f"{name}_valence_timeline.png"
        plt.savefig(save_path)
        plt.clf()

        plt.plot(a_timeline)
        plt.xlabel("Time Step")
        plt.ylabel("Arousal")
        plt.title(f"Arousal values over time for {name}")
        plt.legend()
        save_path = a_output_dir / f"{name}_arousal_timeline.png"
        plt.savefig(save_path)
        plt.clf()

def main():
    df = pd.read_csv("annotations_2026-06-17.csv")

    df["preset"] = df["file_path"].str.extract(r"data\\dataset\\Preset_([A-Z])_\d+\.wav")
    df["v_count"] = df["valence_timeline"].apply(
        lambda x: len(ast.literal_eval(x))
    )

    print("---------------------------------------------")
    print("Average Valence and Arousal Values per Preset")
    print("---------------------------------------------")
    preset_va_means = df.groupby("preset")[["valence_mean", "arousal_mean"]].mean().reset_index()
    print(preset_va_means)
    print("---------------------------------------------")

    print("---------------------------------------------")
    print("Standard Deviation of Valence and Arousal Values per Preset")
    print("---------------------------------------------")
    preset_va_std = df.groupby("preset")[["valence_mean", "arousal_mean"]].std().reset_index()
    print(preset_va_std)
    print("---------------------------------------------")


    preset_va_timeline_count = df[["file_path", "v_count"]].reset_index()
    print(preset_va_timeline_count)

    # graph_va_timeline(df)

if __name__ == '__main__':
    main()