from crewai import Task
from textwrap import dedent


class TravelTasks:
    def __tip_section(self):
        return "Promoção para identificar processos com erros para atuação mais efetiva "

    def identify_error(self, agent, status):
        return Task(
            description=dedent(
                f"""
            **Task**: processos executados com erros
            **Description**:  Buscar o status atualizado dos processos executados com sucesso, 
    via api: http://172.16.128.133:5678/webhook/execute-python?processo=processos_executados.

    Pergunta:
    Quais processos foram executados com sucesso?

            **Parameters**: 
            - Status: {status}

            **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
            expected_output=dedent(
                """
                    Um resumo dos status de todos os processos executados com sucesso retornados pela api.
                """
            ),
        )

    # def identify_city(self, agent, origin, cities, interests, travel_dates):
    #     return Task(
    #         description=dedent(
    #             f"""
    #                 **Task**:  Identify the Best City for the Trip
    #                 **Description**: Analyze and select the best city for the trip based on specific 
    #                     criteria such as weather patterns, seasonal events, and travel costs. 
    #                     This task involves comparing multiple cities, considering factors like current weather 
    #                     conditions, upcoming cultural or seasonal events, and overall travel expenses. 
    #                     Your final answer must be a detailed report on the chosen city, 
    #                     including actual flight costs, weather forecast, and attractions.


    #                 **Parameters**: 
    #                 - Origin: {origin}
    #                 - Cities: {cities}
    #                 - Interests: {interests}
    #                 - Travel Date: {travel_dates}

    #                 **Note**: {self.__tip_section()}
    #     """
    #         ),
    #         agent=agent,
    #         expected_output=dedent(
    #             """
    #             - The best city for the trip based on given parameters
    #             - Justification including cost, weather, and events
    #             - Flight prices and expected expenses
    #             """
    #         ),
    #     )

    # def gather_city_info(self, agent, city, travel_dates, interests):
    #     return Task(
    #         description=dedent(
    #             f"""
    #                 **Task**:  Gather In-depth City Guide Information
    #                 **Description**: Compile an in-depth guide for the selected city, gathering information about 
    #                     key attractions, local customs, special events, and daily activity recommendations. 
    #                     This guide should provide a thorough overview of what the city has to offer, including 
    #                     hidden gems, cultural hotspots, must-visit landmarks, weather forecasts, and high-level costs.

    #                 **Parameters**: 
    #                 - Cities: {city}
    #                 - Interests: {interests}
    #                 - Travel Date: {travel_dates}

    #                 **Note**: {self.__tip_section()}
    #     """
    #         ),
    #         agent=agent,
    #         expected_output=dedent(
    #             """
    #             - A detailed city guide including:
    #             - Top attractions, local customs, and special events
    #             - Weather forecasts and estimated costs
    #             """
    #         ),
    #     )