import traci


def simulation(time=10800):
    traci.start([
        r"E:\sumo1.20\bin\sumo.exe", "-c",
        r"scenario\wangjing.sumocfg"
    ])
    for i in range(time):
        traci.simulationStep()
    traci.close()


if __name__ == "__main__":
    simulation()
