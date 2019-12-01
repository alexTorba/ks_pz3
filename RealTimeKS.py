import math


def set_flow_rate() -> tuple:
    flow_rates = list()
    index = 1
    while True:
        rate = input("Enter A{0} (tap any word to exit) :".format(index))

        if rate.isalpha():
            break

        rate = int(rate)
        if rate <= 0:
            print("A{0}, must be >= 0".format(input()))
            continue

        flow_rates.append(rate / 3600)  ##### MODIFICATION
        index += 1

    if len(flow_rates) == 0:
        raise Exception("Flow rates must have any value !")

    return tuple(flow_rates)


def set_labor_input() -> tuple:
    labor_inputs = list()
    index = 1
    while True:
        labor_input = input("Enter O{0} (tap any word to exit) :".format(index))

        if labor_input.isalpha():
            break

        labor_input = int(labor_input)

        if labor_input <= 0:
            print("O{0}, must be >= 0".format(input()))
            continue

        labor_inputs.append(labor_input)
        index += 1

    if len(labor_input) == 0:
        raise Exception("Labor input must have any values !")

    return tuple(labor_inputs)


def calc_bmin(flow_rates: tuple, labor_input: tuple, is_print=False) -> float:
    if len(flow_rates) != len(labor_input):
        raise Exception("Each flow rate must have appropriate labor input !")

    result = 0
    count = len(flow_rates)
    index = 0
    str_print = ""
    while index < count:
        result += flow_rates[index] * labor_input[index]
        str_print += "+ {0} * {1} ".format(flow_rates[index], labor_input[index])
        index += 1
    str_print = str_print[1:].strip()
    if is_print:
        print("BMin = {0}= {1}".format(str_print, result))
    return result


def calc_bmin2(flow_rates: tuple, labor_input: tuple) -> float:
    if len(flow_rates) != len(labor_input):
        raise Exception("Each flow rate must have appropriate labor input !")

    result = 0
    index = 0
    count = len(flow_rates)

    while index < count:
        result += flow_rates[index] * 2 * labor_input[index] ** 2
        index += 1
    return result


def calc_bopt(flow_rates: tuple, labor_input: tuple, is_print=False) -> float:
    bmin = calc_bmin(flow_rates, labor_input)
    bmin2 = calc_bmin2(flow_rates, labor_input)
    k = 1
    string = "Bopt = "
    sum_flows = calc_sum_flow_rates(flow_rates, True)

    string += "{bmin} + 1 / (2 * {bmin}) * ({k}*{sum_flows}*{bmin2} + " \
              "[(2*{bmin}^2 + {k}*{sum_flows}*{bmin2}) * {k}*{sum_flows}*{bmin2}]^0.5)" \
        .format(bmin=bmin, k=k, bmin2=bmin2, sum_flows=sum_flows)

    temp = (2 * bmin ** 2 + k * sum_flows * bmin2) * k * sum_flows * bmin2
    temp = math.pow(temp, 0.5)
    temp = k * sum_flows * bmin2 + temp
    temp = temp / (2 * bmin)
    bopt = bmin + temp
    bopt = round(bopt, 3)
    string += " = {0}".format(bopt)

    if is_print:
        print(string)

    return bopt


def calc_sum_flow_rates(flow_rates: tuple, is_print=False) -> int:
    _sum = sum(flow_rates)
    if is_print:
        str_print = "A = "
        for i in flow_rates:
            str_print += " {0} +".format(i)
        str_print += "= {0}".format(_sum)
        print(str_print[0:-1])
    return _sum


def calc_time_service(bmin: float, labor_input: tuple, is_print=False) -> tuple:
    time_service = list()
    index = 0
    for i in labor_input:
        index += 1
        q = round(i / bmin, 6)
        if is_print:
            print("Q{0} = {1}".format(index, q))
        time_service.append(q)
    return tuple(time_service)


def calc_second_time_service(time_service: tuple, is_print=False) -> tuple:
    second_time_service = list()
    index = 0
    for i in time_service:
        index += 1
        q2 = 2 * i ** 2
        q2 = round(q2, 9)
        if is_print:
            print("(Q^2){0} = {1}".format(index, q2))
        second_time_service.append(q2)
    return tuple(second_time_service)


def calc_thread_loading(flow_rate: tuple, time_service: tuple, is_print=False) -> tuple:
    thread_loading = list()
    index = 0
    while index < len(flow_rate):
        p = flow_rate[index] * time_service[index]
        p *= 100
        p = math.floor(p)
        p /= 100

        index += 1
        if is_print:
            str_calc = "p{0} = {1}".format(index, p)
            print(str_calc)
        thread_loading.append(p)
    return tuple(thread_loading)  # to prevent changing collection


def sum_thread_loading(thread_loading: tuple, is_print=False) -> int:
    sum_thread = sum(thread_loading)
    if is_print:
        str_print = " SumP ="
        index = 0
        while index < len(thread_loading):
            str_print += "+ {0} ".format(thread_loading[index])
            index += 1
        str_print = str_print[1:]
        str_print += " = {0}".format(sum_thread)
        print(str_print)
    return sum_thread


def calc_time_pending_ABSOLUTE(time_service: tuple, second_time_service: tuple, thread_loading: tuple,
                               flow_rates: tuple,
                               thread_priority: tuple) -> float:
    to = thread_priority[0] + 1  # M1 + 1
    for k in range(1, to):
        rk_1 = calc_rk(k - 1, thread_loading)  # number of items to sum
        rk = calc_rk(k, thread_loading)
        qk = time_service[k - 1]
        sum_sts = sum_second_time_service(second_time_service, flow_rates, k)
        sum_sts = round(sum_sts, 6)

        foo = rk_1 * qk / (1 - rk_1)
        foo = round(foo, 4)

        w = foo + (sum_sts / (2 * (1 - rk_1) * (1 - rk)))
        print("W{k} = {rk_1} * {qk} / (1 - {rk_1}) + ({sum_sts} / (2 * (1 - {rk_1}) * (1 - {rk})) = {w}"
              .format(k=k, w=w, rk_1=rk_1, qk=qk, sum_sts=sum_sts, rk=rk))
        return w


def calc_time_pending_RELEVANT(time_service: tuple, second_time_service: tuple, thread_loading: tuple,
                               flow_rates: tuple,
                               thread_priority: tuple) -> float:
    M1 = thread_priority[0]
    f = M1 + 1  # M1 + 1
    to = sum(thread_priority[:2]) + 1  # M1 + M2 + 1
    M = sum(thread_priority)

    for k in range(f, to):
        rm1 = calc_rk(M1, thread_loading)
        rk_1 = calc_rk(k - 1, thread_loading)
        rk = calc_rk(k, thread_loading)
        qk = time_service[k - 1]
        sum_sts = sum_second_time_service(second_time_service, flow_rates, M)
        sum_sts = round(sum_sts, 6)

        foo = rk_1 * qk / (1 - rk_1)
        foo = round(foo, 4)

        w = foo + (sum_sts / (2 * (1 - rk_1) * (1 - rk)))
        print("W{k} = {rm1} * {qk} / (1 - {rm1}) + ({sum_sts} / (2 * (1 - {rk_1}) * (1 - {rk})) = {w}"
              .format(k=k, w=w, rk_1=rk_1, qk=qk, sum_sts=sum_sts, rk=rk, rm1=rm1))
        return w


def calc_time_pending_NOPRIO(time_service: tuple, second_time_service: tuple, thread_loading: tuple, flow_rates: tuple,
                             thread_priority: tuple) -> float:
    M1 = thread_priority[0]
    f = sum(thread_priority[:2]) + 1  # M1 + M2 + 1
    to = sum(thread_priority[:3]) + 1  # M1 + M2 + M3 + 1
    M = sum(thread_priority)

    for k in range(f, to):
        rm1 = calc_rk(M1, thread_loading)
        rk_1 = calc_rk(k - 1, thread_loading)
        rk = calc_rk(k, thread_loading)
        qk = time_service[k - 1]
        sum_sts = sum_second_time_service(second_time_service, flow_rates, M)
        sum_sts = round(sum_sts, 6)

        foo = rk_1 * qk / (1 - rk_1)
        foo = round(foo, 4)

        w = foo + (sum_sts / (2 * (1 - rk_1) * (1 - rk)))
        print("W{k} = {rm1} * {qk} / (1 - {rm1}) + ({sum_sts} / (2 * (1 - {rk_1}) * (1 - {rk})) = {w}"
              .format(k=k, w=w, rk_1=rk_1, qk=qk, sum_sts=sum_sts, rk=rk, rm1=rm1))
        return w


def calc_rk(_k: int, _thread_loading: tuple) -> float:
    summary = 0
    index = 0
    while index < _k:
        summary += _thread_loading[index]
        index += 1
    return round(summary, 8)


def sum_second_time_service(second_time_service: tuple, flow_rates: tuple, k: int) -> int:
    index = 0
    sum_time = 0
    while index < k:
        sum_time += second_time_service[index] * flow_rates[index]
        index += 1
    return sum_time
