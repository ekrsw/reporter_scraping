class Calulator(object):
    def calc_wh(self, logon_time, today_shift):
        lt = logon_time.split(':')
        h_lt = float(lt[0])
        m_lt = float(lt[1]) / 60.0
        w_hours = round(h_lt + m_lt, 2) - 1.0

        if today_shift == '9_1730':
            if w_hours >= 8.0:
                core_time = 8.0
            else:
                core_time = w_hours

        elif today_shift == '9_20':
            core_time = 8.0

        elif today_shift == '8_1730':
            if w_hours - 1.0 >= 8.0:
                core_time = 8.0
            else:
                core_time = w_hours - 1.0

        elif today_shift == '830_1730':
            if w_hours - 0.5 >= 8.0:
                core_time = 8.0
            else:
                core_time = w_hours - 0.5

        elif today_shift == '13_22':
            core_time = 4.0
        elif today_shift == '22_8':
            # w_hours += 1.0
            core_time = 0.0
        else:
            w_hours = ''
            core_time = ''
        


        return w_hours, core_time

    def calc_work_total(self, work_time, af_incoming, af_outgoing):
        work_time = work_time.split(':')
        af_incoming = af_incoming.split(':')
        af_outgoing = af_outgoing.split(':')

        hours =  int(work_time[0]) + int(af_incoming[0]) + int(af_outgoing[0])
        minutes = int(work_time[1]) + int(af_incoming[1]) + int(af_outgoing[1])
        seconds = int(work_time[2]) + int(af_incoming[2]) + int(af_outgoing[2])

        _ = seconds // 60
        seconds = seconds % 60

        minutes = minutes + _
        _ = minutes // 60
        minutes = minutes % 60

        hours = hours + _
        hours = hours % 60

        def to_string(arg):
            s = str(arg)
            if len(s) == 1:
                return '0' + s
            else:
                return s

        hours = to_string(hours)
        minutes = to_string(minutes)
        seconds = to_string(seconds)
        work_total = ':'.join([hours, minutes, seconds])

        return work_total


if __name__ == '__main__':
    cal = Calulator()
    w, c = cal.calc_wh('11:00:30', '9_20')
    print(w, c)
