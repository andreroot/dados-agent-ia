from crewai import Crew
from textwrap import dedent
from agents import TravelAgents
from tasks import TravelTasks
from dotenv import load_dotenv

load_dotenv()


class TripCrew:
    def __init__(self, question, status):
        self.question = question
        self.status = status

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = TravelAgents()
        tasks = TravelTasks()

        # Define your custom agents and tasks here
        expert_agent = agents.expert_engeiner_data()

        # Custom tasks include agent name and variables as input
        tasks_identify_process = tasks.identify_error(
            expert_agent, self.process
        )

        # identify_city = tasks.identify_city(
        #     city_selection_expert,
        #     self.origin,
        #     self.cities,
        #     self.interests,
        #     self.date_range,
        # )

        # gather_city_info = tasks.gather_city_info(
        #     local_tour_guide, self.cities, self.date_range, self.interests
        # )

        # Define your custom crew here
        crew = Crew(
            agents=[expert_agent],
            tasks=[tasks_identify_process],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Processos de Monitoramento Remoto ##")
    print("-------------------------------")
    question = input(
        dedent("""
      Quais processos deram erros?
    """)
    )

    eng_crew = TripCrew(question, "erros")
    result = eng_crew.run()
    print("\n\n########################")
    print("## Processo listados")
    print("########################\n")
    print(result)