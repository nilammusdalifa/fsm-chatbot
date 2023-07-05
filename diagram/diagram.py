
def generate_dot_file(fsm):
    dot = 'digraph FSM {\n'

    # Add state nodes
    for state in fsm['states']:
        dot += f'  {state} [shape=circle];\n'

    # Add transitions
    for transition in fsm['transitions']:
        dot += f'  {transition["current_state"]} -> {transition["next_state"]} [label="{transition["input"]}"];\n'

    dot += '}'
    return dot


fsm = {
    'states': ['greeting', 'ask', 'ask_stock', 'ask_price', 'ask_description', 'recommendation', 'auth', 'login', 'register', 'exit', 'order', 'order_detail'],
    'transitions': [
        {'current_state': 'greeting', 'input': 'tanya_harga', 'next_state': 'ask_price'},
        {'current_state': 'greeting', 'input': 'tanya_deskripsi', 'next_state': 'ask_description'},
        {'current_state': 'greeting', 'input': 'tanya_stok', 'next_state': 'ask_stock'},
        {'current_state': 'greeting', 'input': 'tanya_rekomendasi', 'next_state': 'recommendation'},
        {'current_state': 'greeting', 'input': 'tambah_barang', 'next_state': 'order_detail'},
        {'current_state': 'greeting', 'input': 'tanya_pesan', 'next_state': 'order_detail'},
        {'current_state': 'greeting', 'input': 'salam_perpisahan', 'next_state': 'exit'},
        {'current_state': 'greeting', 'input': 'unknown', 'next_state': 'greeting'},
        {'current_state': 'ask', 'input': 'tolak', 'next_state': 'exit'},
        {'current_state': 'ask', 'input': 'tanya_harga', 'next_state': 'ask_price'},
        {'current_state': 'ask', 'input': 'tanya_stok', 'next_state': 'ask_stock'},
        {'current_state': 'ask', 'input': 'tanya_deskripsi', 'next_state': 'ask_description'},
        {'current_state': 'ask', 'input': 'tanya_rekomendasi', 'next_state': 'recommendation'},
        {'current_state': 'ask', 'input': 'tambah_barang', 'next_state': 'order_detail'},
        {'current_state': 'ask', 'input': 'tanya_pesan', 'next_state': 'order_detail'},
        {'current_state': 'ask', 'input': 'salam_perpisahan', 'next_state': 'exit'},
        {'current_state': 'ask', 'input': 'terimakasih', 'next_state': 'exit'},
        {'current_state': 'ask', 'input': 'another', 'next_state': 'ask'},
        {'current_state': 'ask_price', 'input': 'terima', 'next_state': 'order_detail'},
        {'current_state': 'ask_price', 'input': 'tolak', 'next_state': 'ask'},
        {'current_state': 'ask_price', 'input': 'another', 'next_state': 'ask_price'},
        {'current_state': 'ask_stock', 'input': 'terima', 'next_state': 'oder_detail'},
        {'current_state': 'ask_stock', 'input': 'tolak', 'next_state': 'ask'},
        {'current_state': 'ask_stock', 'input': 'another', 'next_state': 'ask_stock'},
        {'current_state': 'ask_description', 'input': 'terima', 'next_state': 'oder_detail'},
        {'current_state': 'ask_description', 'input': 'tolak', 'next_state': 'ask'},
        {'current_state': 'ask_description', 'input': 'another', 'next_state': 'ask_description'},
        {'current_state': 'recommendation', 'input': 'terima', 'next_state': 'order_detail'},
        {'current_state': 'recommendation', 'input': 'tolak', 'next_state': 'ask'},
        {'current_state': 'recommendation', 'input': 'salam_perpisahan', 'next_state': 'exit'},
        {'current_state': 'recommendation', 'input': 'terimakasih', 'next_state': 'exit'},
        {'current_state': 'recommendation', 'input': 'tanya_pesan', 'next_state': 'order_detail'},
        {'current_state': 'recommendation', 'input': 'another', 'next_state': 'recommendation'},
        {'current_state': 'auth', 'input': 'terima', 'next_state': 'login'},
        {'current_state': 'auth', 'input': 'tolak', 'next_state': 'register'},
        {'current_state': 'auth', 'input': 'salam_perpisahan', 'next_state': 'exit'},
        {'current_state': 'auth', 'input': 'another', 'next_state': 'auth'},
        {'current_state': 'login', 'input': 'tolak', 'next_state': 'ask'},
        {'current_state': 'login', 'input': 'another', 'next_state': 'login'},
        {'current_state': 'register', 'input': 'tolak', 'next_state': 'ask'},
        {'current_state': 'register', 'input': 'another', 'next_state': 'register'},
        {'current_state': 'order_detail', 'input': 'tolak', 'next_state': 'recommendation'},
        {'current_state': 'order_detail', 'input': 'terima', 'next_state': 'order'},
        {'current_state': 'order_detail', 'input': 'another', 'next_state': 'order_detail'},
        {'current_state': 'order', 'input': 'terimakasih', 'next_state': 'exit'},
        {'current_state': 'order', 'input': 'salam_perpisahan', 'next_state': 'exit'},
        {'current_state': 'order', 'input': 'tolak', 'next_state': 'ask'},
        {'current_state': 'order', 'input': 'another', 'next_state': 'order_detail'},
        {'current_state': 'exit', 'input': 'another', 'next_state': 'greeting'}
    ]
}

fsm_dot = generate_dot_file(fsm)
print(fsm_dot)
with open('fsm.dot', 'w') as file:
    file.write(generate_dot_file(fsm))