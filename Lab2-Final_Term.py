# Mealy machine definition and conversion to an equivalent Moore machine.
inputs = ["00110", "11001", "1010110", "101111"]

# Mealy transition table: (current_state, input) -> (next_state, output)
mealy = {
    ('A','0'): ('A','A'), ('A','1'): ('B','B'),
    ('B','0'): ('C','A'), ('B','1'): ('D','B'),
    ('C','0'): ('D','C'), ('C','1'): ('B','B'),
    ('D','0'): ('B','B'), ('D','1'): ('C','C'),
    ('E','0'): ('D','C'), ('E','1'): ('E','C'),
}

def mealy_process(start, s):
    cur = start
    outputs = []
    states = [cur]
    for ch in s:
        nxt, out = mealy[(cur,ch)]
        outputs.append(out)
        cur = nxt
        states.append(cur)
    return outputs, states

# Convert Mealy to Moore: create Moore state "T|o" for every Mealy transition (S,a)->(T,o)
moore_states = {}
for (S,a), (T,o) in mealy.items():
    name = f"{T}|{o}"
    moore_states[name] = o

# Moore transition table: from Moore-state "S|p" on input a -> "T|o" where Mealy (S,a)->(T,o)
moore_trans = {}
for moore_state in moore_states:
    orig_state = moore_state.split('|')[0]
    moore_trans[moore_state] = {}
    for a in ['0','1']:
        T,o = mealy[(orig_state,a)]
        moore_trans[moore_state][a] = f"{T}|{o}"

# Pick an initial Moore-state corresponding to original A (choose first with original-state A)
initial_moore = next((name for name in moore_states if name.split('|')[0] == 'A'), next(iter(moore_states)))

def moore_process(start_moore, s):
    cur = start_moore
    outputs = []
    states = [cur]
    for ch in s:
        cur = moore_trans[cur][ch]
        outputs.append(moore_states[cur])  # output of entered state
        states.append(cur)
    return outputs, states

print("Mealy outputs:")
for inp in inputs:
    outs, states = mealy_process('A', inp)
    print(f"{inp} -> {''.join(outs)}")

print("\nMoore states and outputs:")
for name, out in sorted(moore_states.items()):
    print(f"{name} -> {out}")

print("\nMoore transitions:")
for name in sorted(moore_trans.keys()):
    print(f"{name}: 0->{moore_trans[name]['0']}, 1->{moore_trans[name]['1']}")

print("\nMoore outputs (reported after each input):")
for inp in inputs:
    outs, states = moore_process(initial_moore, inp)
    print(f"{inp} -> {''.join(outs)}")
