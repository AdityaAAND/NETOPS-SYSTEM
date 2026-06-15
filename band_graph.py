from graph.workflow import graph


class BandGraph:
    async def ainvoke(self,state,config=None):
        print("BAND INPUT :",state )

        #TEMPORARY TEST ALERT

        netops_state = {
            "alert": "CPU utilization 98% with OSPF adjacency resets."

        }

        return await graph.ainvoke(
            netops_state,
            config=config
        )