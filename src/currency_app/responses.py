no_db_data = {
    425: {
        "description": "No data in DB yet",
        "content": {"application/json": {"example": {"detail": {
                "detail": "No data in DB, please update rates"
        }
}
}
}
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
        "content": {"application/json": {"example": {"detail": {
                "detail": "No data in DB, please update rates"
                }

                }
                }
                }
        },
    429: {
        "description": "Bad value provided",
        "content": {"application/json": {"example": {"detail": {
            "detail": "Amount can't be lower than 0!"
        }

        }
        }
        },



    },



}

# no_currency_code = {
#     422: {
#         "description": "No such currency code or empty DB",
#         "content": {"application/json": {"example": {"detail": "One or both currency codes you have used doesn't exist in DB"}}},
#     }
# }
# ext_api_resp = {
#     200: {
#         "description": "External server is working",
#         "content": {"application/json": {"example": {'server_status': 'ok'}}},
#     },
#     504: {
#         "description": "External server is not reachable",
#         "content": {
#             "application/json": {"example": {'server_status': 'disabled'}}
#         },
#     },
# }