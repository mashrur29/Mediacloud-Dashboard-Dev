import pandas as pd
import os


group_colors = {
    "mostly left": "#4E79A7",
    "somewhat left": "#5FA2CE",
    "center": "#9467BD",
    "somewhat right": "#FF9D9A",
    "mostly right": "#E15759"
}




def get_data(data_path='data/'):
    keys = [
        'id',
        'name',
        'articles',
        'mostly_left_summary',
        'somewhat_left_summary',
        'center_summary',
        'somewhat_right_summary',
        'mostly_right_summary'
    ]

    processed_clusters = {}

    clusters = {}

    base_path_to_all_data = data_path
    json_files = [pos_json for pos_json in os.listdir(base_path_to_all_data) if pos_json.endswith('.jsonl')]
    json_files.sort()

    for file in json_files:

        json_file = pd.read_json(path_or_buf=f'{base_path_to_all_data}/{file}', lines=True)
        cur_cluster_name = file.replace('_', ' ').replace('.jsonl', '').replace(data_path, '')
        clusters[cur_cluster_name] = []
        len_cur_cluster = len(json_file['id'])


        for idx in range(len_cur_cluster):
            cur_item = {}

            for key in keys:
                cur_item[key] = json_file[key][idx]

            clusters[cur_cluster_name].append(cur_item)


    for week in clusters:

        cluster_week = []
        colors_list = ["#C8CFA0", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#DBB5B5", "#D1C4E9", "#E8C5E5", "#D6DAC8", "#D7CCC8", "#DCEDC8"]
        # colors_list = ["#4e79a7","#f28e2c","#e15759","#76b7b2","#59a14f","#edc949","#af7aa1","#ff9da7","#9c755f","#bab0ab"]

        for idx, c in enumerate(clusters[week]):
            c["color"] = colors_list[idx % 10]
            c['article_counts'] = len(c['articles'])
            c["distribution"] = {}
            c["distribution"]["mostly left"] = 0
            c["distribution"]["somewhat left"] = 0
            c["distribution"]["center"] = 0
            c["distribution"]["somewhat right"] = 0
            c["distribution"]["mostly right"] = 0
            
            # mostly_left, somewhat_left, center, somewhat_right, mostly_right
            
            for article in c["articles"]:
                article["collection"] = article["collection"].replace("_", " ")

                if article["collection"] == "mostly left":
                    c["distribution"]["mostly left"] += 1
                elif article["collection"] == "somewhat left":
                    c["distribution"]["somewhat left"] += 1
                elif article["collection"] == "center":
                    c["distribution"]["center"] += 1
                elif article["collection"] == "somewhat right":
                    c["distribution"]["somewhat right"] += 1
                else:
                    c["distribution"]["mostly right"] += 1

            cluster_week.append(c)

            if idx >= 9:
                break

        processed_clusters[week] = cluster_week

    return processed_clusters
