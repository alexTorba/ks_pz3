import RealTimeKS


def main():
    # flow_rate = RealTimeKS.set_flow_rate()  # alfa A
    # labor_input = RealTimeKS.set_labor_input()  # omega O
    flow_rate = [1300, 2300, 3200]
    flow_rate = tuple([i / 3600 for i in flow_rate])

    labor_input = (2000, 3000, 4300)

    thread_priority = (1, 1, 1)

    bmin = RealTimeKS.calc_bmin(flow_rate, labor_input, True)
    RealTimeKS.calc_bopt(flow_rate, labor_input, True)

    time_service = RealTimeKS.calc_time_service(bmin, labor_input, True)
    second_time_service = RealTimeKS.calc_second_time_service(time_service, True)
    thread_loading = RealTimeKS.calc_thread_loading(flow_rate, time_service, True)
    RealTimeKS.sum_thread_loading(thread_loading, True)
    RealTimeKS.calc_time_pending_ABSOLUTE(time_service, second_time_service, thread_loading, flow_rate, thread_priority)
    RealTimeKS.calc_time_pending_RELEVANT(time_service, second_time_service, thread_loading, flow_rate, thread_priority)
    RealTimeKS.calc_time_pending_NOPRIO(time_service, second_time_service, thread_loading, flow_rate, thread_priority)


if __name__ == "__main__":
    main()
    input("Enter any key to exit")
