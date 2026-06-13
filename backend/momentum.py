def compute_momentum(publication_velocity,citation_velocity):

    # Return empty list if either input is empty
    if not publication_velocity or not citation_velocity:
        return []
    
    citation_map={}
    for c in citation_velocity:
        citation_map[c["topic_id"]]=c
    results=[]

    for p in publication_velocity:
        topic_id=p["topic_id"]

        if topic_id not in citation_map:
            continue

        pub_vel=p["velocity"]
        cit_vel=citation_map[topic_id]["citation_velocity"]
        momentum=(0.5*pub_vel)+(0.5*cit_vel)

        if momentum>0.1:
            trend="↑"
        elif momentum<-0.1:
            trend="↓"
        else:
            trend="→"

        results.append({
            "topic_id":topic_id,
            "publication_velocity":pub_vel,
            "citation_velocity":cit_vel,
            "momentum":float(momentum),
            "momentum_trend":trend
        })
    return results