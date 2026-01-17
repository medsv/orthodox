class Assistant:
    def __init__(self, instructions, model, client):
        self.model = model
        self.instructions = instructions
        self.previous_response_id_map = {}
        self.client = client
        

    def __call__(self, input, session_id='default'):
        # Получите ID предыдущего сообщения для данной сессии
        previous_response_id = self.previous_response_id_map.get(session_id, None)
        # Сформируйте ответ модели
       
        res = self.client.responses.create(
            model = self.model,
            reasoning = { "effort" : "low" },
#            temperature = 0.2,
            store = True,
            previous_response_id = previous_response_id,
            instructions = self.instructions,
            input = input,
            tools=[
                {
                        "type": "web_search",
                        "filters": {
                            # до 5 штук
                            "content_type": "text",
                            "language": "ru",
                            "region": "RU",
                            "allowed_domains": [
                                "https://www.patriarchia.ru/", "https://pravoslavie.ru/", "https://azbyka.ru/",
                            ],
                            "user_location": {
                                "region": "225",
                            }
                        }
                    } # type: ignore
            ],
            max_output_tokens = 2000
        )
        
        # Запомните ID последнего ответа модели в словаре
        self.previous_response_id_map[session_id] = res.id
        return res.output_text
