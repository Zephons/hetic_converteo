def assign_group_name(zip_code: str) -> str:
    # On trouve les Group name à partir des Zip code.
    zipcode_groupname = {
        "92800": "PARIS NORD",
        "91160": "PARIS SUD",
        "77340": "PARIS SUD",
        "95460": "PARIS NORD",
        "75019": "PARIS NORD",
        "95610": "PARIS NORD",
        "33700": "NOUVELLE AQUITAINE",
        "76000": "NORD",
        "49070": "OUEST"
    }
    return zipcode_groupname.get(zip_code)