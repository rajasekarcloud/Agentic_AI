from crewai.flow import Flow, start, listen

class MyFlow(Flow):

    @start
    def begin(self, topic):
        print("Starting flow with:", topic)
        return self.next("research", topic)

    @listen("begin")
    def research(self, topic):
        print("Researching:", topic)
        return self.next("write", f"Research on {topic}")

    @listen("research")
    def write(self, research_output):
        print("Writing based on:", research_output)
        return "Final content ready"
