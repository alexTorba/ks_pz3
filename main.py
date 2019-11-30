import RealTimeKS


def main():
    # flow_rate = RealTimeKS.set_flow_rate()  # alfa A
    # labor_input = RealTimeKS.set_labor_input()  # omega O
    flow_rate = list()
    flow_rate.append(1300 / 3600)
    flow_rate.append(2300 / 3600)
    flow_rate.append(3200 / 3600)
    labor_input = list()
    labor_input.append(2000)
    labor_input.append(3000)
    labor_input.append(4300)

    bmin = RealTimeKS.calc_bmin(flow_rate, labor_input, True)
    RealTimeKS.calc_bopt(flow_rate, labor_input, True)

    time_service = RealTimeKS.calc_time_service(bmin, labor_input, True)
    second_time_service = RealTimeKS.calc_second_time_service(time_service, True)
    thread_loading = RealTimeKS.calc_thread_loading(flow_rate, time_service, True)
    RealTimeKS.sum_thread_loading(thread_loading, True)
    RealTimeKS.calc_time_pending_ABSOLUTE(time_service, second_time_service, thread_loading, flow_rate)
    RealTimeKS.calc_time_pending_RELEVANT(time_service, second_time_service, thread_loading, flow_rate)
    RealTimeKS.calc_time_pending_NOPRIO(time_service, second_time_service, thread_loading, flow_rate)


if __name__ == "__main__":
    main()
    input("enter to exit")
