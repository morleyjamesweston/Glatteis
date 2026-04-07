import geopandas as gpd


def get_weight(row):
    weight = (
        row.normalized_population
        + (1 - row.normalized_admin_rank) * 3
        + row.has_context
    )
    return weight


def resolve(candidates: gpd.GeoDataFrame) -> gpd.GeoDataFrame | None:
    candidates = candidates.copy(deep=True)

    # normalize population
    candidates["normalized_population"] = (
        candidates["population_column"] / candidates["population_column"].max()
    )
    # normalize admin rank
    candidates["normalized_admin_rank"] = (
        candidates["admin_rank"] / candidates["admin_rank"].max()
    )

    candidates["weight"] = candidates.apply(get_weight, axis=1)
    #  get highest weight for each place
    candidates.sort_values("weight", ascending=False, inplace=True)
    # print(candidates)
    candidates.drop_duplicates(subset="standardized_names", keep="first", inplace=True)
    # print("after drop duplicates")
    # print(candidates)
    candidates.sort_index(inplace=True)

    candidates = candidates.filter(
        items=[
            "original_index",
            "original_names",
            "gazetteer_name",
            "standardized_names",
            "geometry",
        ],
    )

    return candidates
