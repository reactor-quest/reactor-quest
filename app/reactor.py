from datetime import datetime
import time
# import matplotlib.pyplot as plt
import sqlite3
import json
import os

from app.events import factory
from app.strategies import strategy_factory
from app.counts import counts_factory


class Reactor:
    def __init__(self, step=1, work=120, chance_rate=0.05,
                 reactor_strategy='reactor_1', counts='state_range'):
        self.step = step  # state update period in seconds
        self.cur_step = 0  # current step
        self.cur_timestamp = None
        self.work = work  # working time in steps
        self.state = 0  # state
        self.rate = 0  # state rate per step
        self.queue = {}  # queue of current step events
        self.events_start = {}  # db events states (start time step)
        self.events = {}
        self.chance = 0  # boom chance for states > 100 (checked every step)
        self.chance_rate = chance_rate  # chance rate per step for states > 100
        self.times = []  # times history by steps
        self.states = []  # states history
        self.rates = []  # rates history
        self.chances = []  # disaster chances history
        self.dump_path = 'reactor.json'  # file or db path
        self.db = False  # dump to db?
        self.reactor_strategy = reactor_strategy
        self.counts = counts
        self.staff_cnt = 0
        self.govs_cnt = 0
        self.terrors_cnt = 0
        self.no_one_cnt = 0
        self.booms_cnt = 0

    def run(self, plot=True,
            dump_path='reactor.json', reset=True, last_dump=False,
            simulate=False, simulate_teams=None, simulate_strats=None):
        self.dump_path = dump_path
        if os.path.splitext(dump_path)[1] == '.db':
            self.db = True
            if reset:
                self.reset_db()
            else:  # load last state
                self.load_db()
        if plot:
            self.create_plot()
        while self.cur_step < self.work:
            self.cur_timestamp = datetime.utcnow()
            self.queue = {}
            if simulate:
                self.simulate(simulate_teams, simulate_strats)
            time.sleep(self.step)  # wait for the next step
            self.update()
            if last_dump:
                if self.cur_step == self.work:
                    self.dump()
            else:
                self.dump()
            if plot:
                self.plot()

    def update(self):
        prev_state = self.state
        # update events queue
        if self.db:
            self.update_events_db()
        else:
            self.update_events_local()
        # run events queue
        print(self.state)
        for i, (k, v) in enumerate(self.events.items()):
            e = factory.get(v['name'], None)
            if e is not None:
                e(k, self)
                print(v['name'], self.state)
        print(self.state)
        # fix state
        if self.state <= 0:
            self.state = 0
        # update rate
        self.rate = self.state - prev_state
        # update chance
        if 0 < self.state <= 100:
            self.chance -= self.chance_rate
            if self.chance < 0:
                self.chance = 0
        elif self.state <= 0:
            self.chance -= self.chance_rate
            if self.chance < 0:
                self.chance = 0
        else:  # self.state > 100
            k = self.state / 100
            self.chance += k * self.chance_rate
        # update teams scores
        counts_factory[self.counts](self)
        # update history
        self.cur_step += 1
        self.times.append(self.cur_timestamp)
        self.states.append(self.state)
        self.rates.append(self.rate)
        self.chances.append(self.chance)

    def dump(self):
        if self.db:
            self.dump_db()
        else:
            if os.path.splitext(self.dump_path)[1] == '.json':
                self.dump_json()

    def simulate(self, simulate_teams=None, simulate_strats=None):
        if simulate_strats is None:
            simulate_strats = ['staff_1', 'terrors_1', 'govs_1']
        if simulate_teams is None:
            simulate_teams = ['staff', 'terrors', 'govs']
        staff_events = strategy_factory[simulate_strats[0]](self, 'staff')
        terrors_events = strategy_factory[simulate_strats[1]](self, 'terrors')
        govs_events = strategy_factory[simulate_strats[2]](self, 'govs')
        events = list()
        if 'staff' in simulate_teams:
            events.extend(staff_events)
        if 'terrors' in simulate_teams:
            events.extend(terrors_events)
        if 'govs' in simulate_teams:
            events.extend(govs_events)
        if self.db:
            con = sqlite3.connect(self.dump_path)
            try:
                cur = con.cursor()
                cur.executemany('INSERT INTO events VALUES (?, ?)',
                                [(None, json.dumps(x)) for x in events])
                con.commit()
            except Exception as e:
                print(e)
            finally:
                con.close()
        else:
            self.events.update(events)

    def update_events_local(self):
        events = strategy_factory[self.reactor_strategy](self, 'reactor')
        self.events.update(events)

    def update_events_db(self):
        events = strategy_factory[self.reactor_strategy](self, 'reactor')
        con = sqlite3.connect(self.dump_path)
        try:
            cur = con.cursor()
            cur.executemany('INSERT INTO events VALUES (?, ?)',
                            [(None, json.dumps(x)) for x in events])
            con.commit()
            events_json = cur.execute('''SELECT * FROM events''').fetchall()
        except Exception as e:
            print(e)
        else:
            for e in events_json:
                rowid, event_json = e
                event = json.loads(event_json)
                self.events_start.setdefault(int(rowid), self.cur_step)
                self.events.setdefault(int(rowid), event)
        finally:
            con.close()

    def dump_db(self):
        state = self.__dict__.copy()
        state.pop('grid', None)  # from colab plot
        state.pop('events_start', None)
        state.pop('times', None)
        state.pop('rates', None)
        state.pop('states', None)
        state.pop('chances', None)
        state.pop('queue', None)
        state.pop('events', None)
        state_json = json.dumps(
            state,
            default=lambda x: x.isoformat() if isinstance(x, datetime) else x)
        con = sqlite3.connect(self.dump_path)
        try:
            cur = con.cursor()
            cur.execute('INSERT INTO states VALUES (?, ?)', [None, state_json])
            con.commit()
        except Exception as e:
            print(e)
        finally:
            con.close()

    def dump_json(self):
        state = self.__dict__.copy()
        state.pop('grid', None)  # from colab plot
        state.pop('events_start', None)
        state.pop('times', None)
        state.pop('rates', None)
        state.pop('states', None)
        state.pop('chances', None)
        state.pop('queue', None)
        state.pop('events', None)
        with open(self.dump_path, 'w') as f:
            json.dump(state, f, default=lambda x: x.isoformat() if isinstance(x,
                                                                              datetime) else x)

    def load_db(self):
        con = sqlite3.connect(self.dump_path)
        try:
            cur = con.cursor()
            cur.execute("SELECT * FROM states ORDER BY id DESC LIMIT 1")
            rowid, last_state_json = cur.fetchone()
        except Exception as e:
            print(e)
        else:
            last_state = json.loads(last_state_json)
            for i, t in enumerate(last_state['ts']):
                last_state['ts'][i] = datetime.strptime(
                    t, "%Y-%m-%dT%H:%M:%S.%f")
            for k in last_state:
                self.__dict__[k] = last_state[k]
        finally:
            con.close()

    def reset_db(self):
        con = sqlite3.connect(self.dump_path)
        try:
            cur = con.cursor()
            cur.execute('''DROP TABLE IF EXISTS states''')
            cur.execute('''CREATE TABLE IF NOT EXISTS states 
            (id INTEGER PRIMARY KEY, data TEXT)''')
            cur.execute('''DROP TABLE IF EXISTS events''')
            cur.execute('''CREATE TABLE IF NOT EXISTS events
            (id INTEGER PRIMARY KEY, data TEXT)''')
        except Exception as e:
            print(e)
        finally:
            con.close()

    def create_plot(self):
        # self.grid = widgets.Grid(3, 2, header_row=True, header_column=True)
        pass

    def plot(self):
        print('\ncur step: {}'.format(self.cur_step))
        print('cur timestamp: {}'.format(self.cur_timestamp))
        print('state: {}'.format(self.state))
        print('rate: {}'.format(self.rate))
        print('chance: {}'.format(self.chance))
        print('{:^4}|{:^4}|{:^7}|{:^10}|{:^20}|'.format(
            'n', 'id', 'start', 'source', 'event'))
        print('-'.join(['' for _ in range(51)]))
        print('\n'.join(
            ['{:^4}|{:^4}|{:^7}|{:^10}|{:^20}|'.format(
                i + 1, k, self.events_start[k], v['source'], v['name'])
             for i, (k, v) in enumerate(self.queue.items())]))
        print('staff_cnt: {}'.format(self.staff_cnt))
        print('govs_cnt: {}'.format(self.govs_cnt))
        print('terrors_cnt: {}'.format(self.terrors_cnt))
        print('no_one_cnt: {}'.format(self.no_one_cnt))

