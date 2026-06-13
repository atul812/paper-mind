def get_top_accelerating(
        velocity_table,
        topic_map,
        n=5
):

    filtered = [t for t in velocity_table if t["topic_id"] != -1]

    sorted_topics = sorted(
        filtered,
        key=lambda x: x["velocity"],
        reverse=True

    )
    results=[]

    for t in sorted_topics[:n]:

        results.append({
            "topic_id":
            t["topic_id"],
            "velocity":
            t["velocity"],
            "keywords":
            topic_map.get(
                t["topic_id"],
                ["Unknown"]
            )

        })

    return results