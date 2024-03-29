import math
import random


def exp_help_func(start_step, delta_step, cur_step, delta_state):
    local_step = cur_step - start_step
    prev_local_step = local_step - 1 if local_step > 0 else 0
    cur_state = delta_state * math.exp(local_step / delta_step)
    prev_state = delta_state * math.exp(prev_local_step / delta_step)
    delta = cur_state - prev_state
    return delta


def nothing(index, reactor):
    pass


def reset(index, reactor):
    cur_step = reactor.cur_step
    for k in reactor.events:
        start_step = reactor.events_start.setdefault(k, cur_step)
        if start_step == cur_step:
            reactor.events_to_init[k] = reactor.events[k]
        reactor.events_end[k] = cur_step
        reactor.events_to_stop[k] = reactor.events[k]
    reactor.events = {k: {'name': 'nothing', 'source': 'reactor'}
                      for k in reactor.events}
    reactor.state = 0
    reactor.rate = 0
    reactor.chance = 0
    reactor.staff_cnt = 0
    reactor.govs_cnt = 0
    reactor.terrors_cnt = 0
    reactor.no_one_cnt = 0
    reactor.booms_cnt = 0


def iodine(index, reactor):
    delta_state = -0.1
    delta_step = 1
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step and 0 < reactor.state < 50:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def anti_terrorist_operation(index, reactor):
    delta_step = 12
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        for k, v in reactor.events.items():
            if v['source'] == 'terrors':
                if random.random() < 0.5:
                    ss = reactor.events_start.setdefault(k, cur_step)
                    if ss == cur_step:
                        reactor.events_to_init[k] = reactor.events[k]
                    reactor.events_end[k] = cur_step
                    reactor.events_to_stop[k] = reactor.events[k]
                    reactor.events[k] = {'name': 'nothing', 'source': 'reactor'}
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def plant_inspection(index, reactor):
    delta_step = 12
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        for k, v in reactor.events.items():
            if v['source'] == 'terrors':
                if random.random() < 0.5:
                    ss = reactor.events_start.setdefault(k, cur_step)
                    if ss == cur_step:
                        reactor.events_to_init[k] = reactor.events[k]
                    reactor.events_end[k] = cur_step
                    reactor.events_to_stop[k] = reactor.events[k]
                    reactor.events[k] = {'name': 'nothing', 'source': 'reactor'}
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def poison_staff(index, reactor):
    delta_step = 12
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        for k, v in reactor.events.items():
            if v['source'] == 'staff':
                if random.random() < 0.5:
                    ss = reactor.events_start.setdefault(k, cur_step)
                    if ss == cur_step:
                        reactor.events_to_init[k] = reactor.events[k]
                    reactor.events_end[k] = cur_step
                    reactor.events_to_stop[k] = reactor.events[k]
                    reactor.events[k] = {'name': 'nothing', 'source': 'reactor'}
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def insert_spy(index, reactor):
    delta_step = 12
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        for k, v in reactor.events.items():
            if v['source'] == 'govs':
                if random.random() < 0.5:
                    ss = reactor.events_start.setdefault(k, cur_step)
                    if ss == cur_step:
                        reactor.events_to_init[k] = reactor.events[k]
                    reactor.events_end[k] = cur_step
                    reactor.events_to_stop[k] = reactor.events[k]
                    reactor.events[k] = {'name': 'nothing', 'source': 'reactor'}
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def intimidate_staff(index, reactor):
    delta_step = 12
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        for k, v in reactor.events.items():
            if v['source'] == 'staff':
                if random.random() < 0.5:
                    ss = reactor.events_start.setdefault(k, cur_step)
                    if ss == cur_step:
                        reactor.events_to_init[k] = reactor.events[k]
                    reactor.events_end[k] = cur_step
                    reactor.events_to_stop[k] = reactor.events[k]
                    reactor.events[k] = {'name': 'nothing', 'source': 'reactor'}
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def bribe_govs(index, reactor):
    delta_step = 12
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        for k, v in reactor.events.items():
            if v['source'] == 'govs':
                if random.random() < 0.5:
                    ss = reactor.events_start.setdefault(k, cur_step)
                    if ss == cur_step:
                        reactor.events_to_init[k] = reactor.events[k]
                    reactor.events_end[k] = cur_step
                    reactor.events_to_stop[k] = reactor.events[k]
                    reactor.events[k] = {'name': 'nothing', 'source': 'reactor'}
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def tip(index, reactor):
    delta_state = 10
    delta_step = 60
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def boron(index, reactor):
    delta_state = -5
    delta_step = 2
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def pump_down(index, reactor):
    delta_state = 5
    delta_step = 10
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def pump_up(index, reactor):
    delta_state = -5
    delta_step = 10
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def rod_up(index, reactor):
    delta_state = 5
    delta_step = 5
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def rod_down(index, reactor):
    delta_state = -5
    delta_step = 5
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def pump_break(index, reactor):
    delta_state = 25
    delta_step = 10
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def pump_blow_up(index, reactor):
    delta_state = 25
    delta_step = 1
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def fire(index, reactor):
    delta_step = 0
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        reactor.state = 0
        reactor.rate = 0
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def press_operators(index, reactor):
    delta_state = 5
    delta_step = 5
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def scram(index, reactor):
    delta_step = 0
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        reactor.state = 0
        reactor.rate = 0
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def boom(index, reactor):
    delta_step = 0
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        reactor.state = 0
        reactor.rate = 0
        reactor.booms_cnt += 1
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def virus(index, reactor):
    delta_step = 15
    delta_state = random.random() * 15
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def hide_boom(index, reactor):
    delta_step = 0
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step:
        if reactor.booms_cnt > 0:
            reactor.booms_cnt -= 1
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def bribe_chief_engineer_plus(index, reactor):
    delta_state = 20
    delta_step = 20
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step and 0 < reactor.state < 50:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


def bribe_chief_engineer_minus(index, reactor):
    delta_state = -20
    delta_step = 20
    cur_step = reactor.cur_step
    start_step = reactor.events_start.setdefault(index, cur_step)
    end_step = reactor.events_end.setdefault(index, start_step + delta_step)
    if cur_step <= end_step and 0 < reactor.state < 50:
        d = exp_help_func(start_step, delta_step, cur_step, delta_state)
        reactor.state += d
    if cur_step >= end_step:
        reactor.events_to_stop[index] = reactor.events[index]
    if start_step == cur_step:
        reactor.events_to_init[index] = reactor.events[index]


factory = {
    'rod_up': rod_up,  # поднять стрежни
    'rod_down': rod_down,  # опустить стрежни
    'pump_up': pump_up,  # увеличить расход рабочего тела
    'pump_down': pump_down,  # уменьшить расход рабочего тела
    'pump_break': pump_break,  # сломать насос
    'pump_blow_up': pump_blow_up,  # взорвавть насос
    'iodine': iodine,  # иодная яма
    # 'replace_boron': replace_boron,  # заменить бор на топливо
    'boron': boron,  # добавить бор в активную зону
    'boom': boom,  # взрыв
    'tip': tip,  # концевой эффект
    'scram': scram,  # АЗ-5
    'bribe_chief_engineer_plus': bribe_chief_engineer_plus,
    # подкупить главного инженера на повышение мощности
    'bribe_chief_engineer_minus': bribe_chief_engineer_minus,
    # подкупить главного инженера на понижение мощности
    'press_operators': press_operators,  # надавить на персонал АЭС
    'fire': fire,  # пожар
    'hide_boom': hide_boom,  # скрыть аварию
    'virus': virus,  # запустить вирус в систему управления
    'reset': reset,
    'anti_terrorist_operation': anti_terrorist_operation,
    'plant_inspection': plant_inspection,
    'poison_staff': poison_staff,
    'intimidate_staff': intimidate_staff,
    'insert_spy': insert_spy,
    'bribe_govs': bribe_govs,
    'nothing': nothing
}

staff_factory = {
    'scram': scram,
    'rod_up': rod_up,
    'rod_down': rod_down,
    'pump_up': pump_up,
    'pump_down': pump_down,
    'boron': boron
}

terrors_factory = {
    'pump_break': pump_break,
    'pump_blow_up': pump_blow_up,
    # 'replace_boron': replace_boron,
    # 'deenergize': deenergize,
    'virus': virus,
    'fire': fire
}

govs_factory = {
    'hide_boom': hide_boom,
    # 'anti_terrorist_operation': anti_terrorist_operation,
    'bribe_chief_engineer_plus': bribe_chief_engineer_plus,
    # подкупить главного инженера
    'bribe_chief_engineer_minus': bribe_chief_engineer_minus,
    # подкупить главного инженера
    'press_operators': press_operators,
    'tip': tip
}
