update_rates_resp = {
    409: {
        "description": "Bad external API response",
        "content": {"application/json": {"example": {"detail": "Couldn't get response from external API"}}},
    },
    425: {
        "description": "Rates are still fresh",
        "content": {"application/json": {"example": {"detail": "Rates are still fresh. Update in 56 seconds, please!"}}},
    },
}


last_update_resp = {
    425: {
        "description": "No data in DB yet",
        "content": {"application/json": {"example": {"detail": {"detail": "No data in DB, please update rates"}}}},
    }
}


convert_resp = {
    425: last_update_resp[425],
    422: {
        "description": "Bad value provided",
        "content": {"application/json": {"example": {"detail": {"detail": "Amount can't be lower than 0!"}}}},
    },
}
