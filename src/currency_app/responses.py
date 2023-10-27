no_db_data = {
    425: {
        "description": "No data in DB yet",
        "content": {"application/json": {"example": {"detail": {"detail": "No data in DB, please update rates"}}}},
    }
}


bad_ext_api_resp = {
    409: {
        "description": "Bad external API response",
        "content": {"application/json": {"example": {"detail": "Couldn't get response from external API"}}},
    }
}


convert_bad_responses = {
    425: {
        "description": "No data in DB yet",
        "content": {"application/json": {"example": {"detail": {"detail": "No data in DB, please update rates"}}}},
    },
    429: {
        "description": "Bad value provided",
        "content": {"application/json": {"example": {"detail": {"detail": "Amount can't be lower than 0!"}}}},
    },
}
