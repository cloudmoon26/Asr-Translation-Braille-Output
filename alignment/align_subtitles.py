import os
import pysrt
import pandas as pd

from preprocessing.text_cleaner import clean_text
from preprocessing.time_utils import midpoint
from alignment.dtw import dtw

def align(en_path, ko_path, max_diff):
    en_subs = pysrt.open(en_path)
    ko_subs = pysrt.open(ko_path)

    # 중간 시간 시퀀스
    en_mid_seq = [midpoint(s.start, s.end) for s in en_subs]
    ko_mid_seq = [midpoint(s.start, s.end) for s in ko_subs]

    # DTW path 생성
    path = dtw(en_mid_seq, ko_mid_seq)

    result_pairs = []

    for (i, j) in path:
        en_text = clean_text(en_subs[i].text)
        ko_text = clean_text(ko_subs[j].text)

        # 너무 먼 매칭은 제거
        if abs(en_mid_seq[i] - ko_mid_seq[j]) <= max_diff:
            if en_text and ko_text:
                result_pairs.append((en_text, ko_text))


    return pd.DataFrame(result_pairs, columns=["source", "target"]).drop_duplicates()

def process_srt_file(sub_dir, output_file, max_diff):
    all_dfs = []

    en_files = [f for f in os.listdir(sub_dir) if f.endswith(".en.srt")]

    for en_file in en_files:
        title_name = en_file[:-7]
        ko_file = f"{title_name}.ko.srt"

        en_path = os.path.join(sub_dir, en_file)
        ko_path = os.path.join(sub_dir, ko_file)

        if not os.path.exists(ko_path):
            print(f"한국어 파일 없음: {title_name}")
            continue

        print(f"처리 중: {title_name}")
        df = align(en_path, ko_path, max_diff)
        all_dfs.append(df)

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        final_df.drop_duplicates(inplace=True)
        final_df.to_csv(output_file, sep="\t", index=False, encoding="utf-8-sig")
        print(f"총 {len(final_df)} 문장 쌍 → {output_file}")
