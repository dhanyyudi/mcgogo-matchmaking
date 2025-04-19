import streamlit as st
import pandas as pd
import json
import requests
import base64
from datetime import datetime
from io import BytesIO
from PIL import Image

st.set_page_config(
    page_title="Magic Chess: GoGo Predictor",
    page_icon="https://assets.pikiran-rakyat.com/crop/0x0:0x0/1200x675/photo/2025/02/25/2262002161.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Magic Chess: GoGo Predictor | Versi 1.0"
    }
)

# Custom CSS untuk styling dengan tema dark
st.markdown("""
<style>
    /* Warna utama untuk dark theme */
    :root {
        --primary-color: #4F8BF9;
        --background-color: #0E1117;
        --second-background-color: #262730;
        --text-color: #FAFAFA;
        --font-family: 'Roboto', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .round-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        background-color: #2C3333;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .random-round {
        background-color: #0D253F;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .predicted-round {
        background-color: #113A51;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .matchup-status {
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .confirmed {
        color: #4CAF50;
    }
    
    .pending {
        color: #FFC107;
    }
    
    /* Styling untuk tabel */
    .table-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        background-color: #2C3333;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    /* Styling untuk radio buttons */
    div.row-widget.stRadio > div {
        background-color: #1E2021;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Styling untuk dropdown */
    div.stSelectbox > div > div {
        background-color: #1E2021;
    }
    
    /* Header styling dengan logo */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
    }
    
    .logo-img {
        height: 60px;
        margin-right: 15px;
    }
    
    .app-header {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #1E1E1E;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .app-title {
        color: #FFFFFF;
        margin: 0;
        margin-left: 15px;
        font-size: 28px;
        font-weight: bold;
    }
    
    .card {
        background-color: #1E2F3E;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .confirmed-badge {
        background-color: #4CAF50;
        color: white;
    }
    
    .pending-badge {
        background-color: #FFA726;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Function to load and display the logo
def display_logo():
    logo_url = "https://img.tapimg.net/market/images/84a6ec79df7b1a891a411faa358c8811.png/appicon"
    try:
        response = requests.get(logo_url)
        img = Image.open(BytesIO(response.content))
        # Resize the image
        img = img.resize((60, 60))
        # Convert the image to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Display the image and title in a nice header
        st.markdown(
            f"""
            <div class="app-header">
                <img src="data:image/png;base64,{img_str}" class="logo-img">
                <h1 class="app-title">Magic Chess: GoGo Predictor</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        # Fallback if image loading fails
        st.markdown('<h1 class="main-header">Magic Chess: GoGo Predictor</h1>', unsafe_allow_html=True)
        st.error(f"Failed to load logo: {e}")

# Fungsi untuk inisialisasi state
def initialize_state():
    if 'players' not in st.session_state:
        st.session_state.players = []
        
    if 'matchups' not in st.session_state:
        st.session_state.matchups = {
            # Round I
            "I-1": [], "I-2": [], "I-3": [],
            # Round II
            "II-1": [], "II-2": [], "II-4": [], "II-5": [], "II-6": [],
            # Round III
            "III-1": [], "III-2": [], "III-4": [], "III-5": [], "III-6": [],
            # Round IV
            "IV-1": [], "IV-2": [], "IV-4": [], "IV-5": [], "IV-6": [],
            # Round V
            "V-1": [], "V-2": [], "V-4": [], "V-5": [], "V-6": [],
            # Round VI
            "VI-1": [], "VI-2": [], "VI-4": [], "VI-5": [], "VI-6": [],
            # Round VII
            "VII-1": [], "VII-2": [], "VII-4": [], "VII-5": [], "VII-6": []
        }
    
    if 'round_status' not in st.session_state:
        st.session_state.round_status = {round_name: False for round_name in st.session_state.matchups.keys()}

    if 'opponent_selections' not in st.session_state:
        st.session_state.opponent_selections = {}
        
    if 'pairs' not in st.session_state:
        st.session_state.pairs = {}
    
    # Additional initialization for debug
    if 'debug_logs' not in st.session_state:
        st.session_state.debug_logs = []

# Fungsi untuk melakukan hard refresh pada UI
def force_rerun():
    log_debug("Forcing page rerun")
    st.rerun()

# Fungsi untuk log debug
def log_debug(message):
    st.session_state.debug_logs.append(f"{datetime.now().strftime('%H:%M:%S')}: {message}")
    if len(st.session_state.debug_logs) > 100:  # Limit log size
        st.session_state.debug_logs.pop(0)

# Fungsi callback untuk dropdown
def on_select_change(round_name, player):
    key = f"{round_name}_{player}"
    opponent = st.session_state[key]
    
    log_debug(f"on_select_change called: {round_name}, {player} selected {opponent}")
    
    # Jika ada nilai yang dipilih
    if opponent:
        # Pastikan round_name ada di pairs
        if round_name not in st.session_state.pairs:
            st.session_state.pairs[round_name] = {}
        
        # Hapus pasangan lama jika ada
        for p, opp in list(st.session_state.pairs[round_name].items()):
            if p == player or opp == player:
                del st.session_state.pairs[round_name][p]
        
        # Set pasangan baru (dua arah)
        st.session_state.pairs[round_name][player] = opponent
        st.session_state.pairs[round_name][opponent] = player
        
        # Update dropdown opponent juga
        opponent_key = f"{round_name}_{opponent}"
        if opponent_key in st.session_state:
            st.session_state[opponent_key] = player

# Fungsi untuk menyimpan pemain
def save_players():
    players = [player.strip() for player in st.session_state.player_input.split('\n') if player.strip()]
    
    # Validate we have exactly 8 players
    if len(players) != 8:
        st.error("Harus ada tepat 8 nama pemain!")
        return False
    
    # Check for duplicates
    if len(players) != len(set(players)):
        st.error("Nama pemain tidak boleh ada yang sama!")
        return False
        
    st.session_state.players = players
    
    # Reset matchups dan status
    st.session_state.matchups = {
        # Round I
        "I-1": [], "I-2": [], "I-3": [],
        # Round II
        "II-1": [], "II-2": [], "II-4": [], "II-5": [], "II-6": [],
        # Round III
        "III-1": [], "III-2": [], "III-4": [], "III-5": [], "III-6": [],
        # Round IV
        "IV-1": [], "IV-2": [], "IV-4": [], "IV-5": [], "IV-6": [],
        # Round V
        "V-1": [], "V-2": [], "V-4": [], "V-5": [], "V-6": [],
        # Round VI
        "VI-1": [], "VI-2": [], "VI-4": [], "VI-5": [], "VI-6": [],
        # Round VII
        "VII-1": [], "VII-2": [], "VII-4": [], "VII-5": [], "VII-6": []
    }
    st.session_state.round_status = {round_name: False for round_name in st.session_state.matchups.keys()}
    st.session_state.opponent_selections = {}
    st.session_state.pairs = {}
    st.session_state.debug_logs = []
    
    return True

# Fungsi untuk reset data
def reset_data():
    st.session_state.players = []
    st.session_state.matchups = {
        # Round I
        "I-1": [], "I-2": [], "I-3": [],
        # Round II
        "II-1": [], "II-2": [], "II-4": [], "II-5": [], "II-6": [],
        # Round III
        "III-1": [], "III-2": [], "III-4": [], "III-5": [], "III-6": [],
        # Round IV
        "IV-1": [], "IV-2": [], "IV-4": [], "IV-5": [], "IV-6": [],
        # Round V
        "V-1": [], "V-2": [], "V-4": [], "V-5": [], "V-6": [],
        # Round VI
        "VI-1": [], "VI-2": [], "VI-4": [], "VI-5": [], "VI-6": [],
        # Round VII
        "VII-1": [], "VII-2": [], "VII-4": [], "VII-5": [], "VII-6": []
    }
    st.session_state.round_status = {round_name: False for round_name in st.session_state.matchups.keys()}
    st.session_state.opponent_selections = {}
    st.session_state.pairs = {}
    st.session_state.debug_logs = []
    
    # Buat flag untuk mereset input pada siklus berikutnya
    if 'reset_player_input' not in st.session_state:
        st.session_state.reset_player_input = False
    st.session_state.reset_player_input = True

# Fungsi untuk menyimpan data ke file
def save_data_to_file():
    if not st.session_state.players:
        st.error("Tidak ada data pemain untuk disimpan!")
        return None
        
    data = {
        "players": st.session_state.players,
        "matchups": st.session_state.matchups,
        "round_status": st.session_state.round_status,
        "pairs": st.session_state.pairs
    }
    
    # Generate filename dengan timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"magic_chess_data_{timestamp}.json"
    
    # Convert to JSON string
    json_str = json.dumps(data, indent=4)
    
    # Return the filename and JSON string
    return filename, json_str

# Fungsi untuk memuat data dari file
def load_data_from_file(file_content):
    try:
        data = json.loads(file_content)
        
        st.session_state.players = data["players"]
        st.session_state.matchups = data["matchups"]
        st.session_state.round_status = data["round_status"]
        
        if "pairs" in data:
            st.session_state.pairs = data["pairs"]
        else:
            st.session_state.pairs = {}
        
        if 'player_input' in st.session_state:
            st.session_state.player_input = "\n".join(st.session_state.players)
            
        st.success("Data berhasil dimuat!")
        return True
    except Exception as e:
        st.error(f"Gagal memuat data: {str(e)}")
        return False

# Fungsi untuk mengonfirmasi matchup pada round tertentu
def confirm_matchups(round_name):
    log_debug(f"Confirming matchups for {round_name}")
    
    # Reset matchups untuk round ini
    st.session_state.matchups[round_name] = []
    
    # Gunakan pasangan yang ada di pairs
    if round_name in st.session_state.pairs:
        # Buat set pemain yang sudah diproses
        processed_players = set()
        
        for player, opponent in st.session_state.pairs[round_name].items():
            # Skip jika pemain sudah diproses
            if (player in processed_players or 
                opponent in processed_players):
                continue
                
            # Verifikasi bahwa opponent juga memilih player
            if (opponent in st.session_state.pairs[round_name] and 
                st.session_state.pairs[round_name][opponent] == player):
                st.session_state.matchups[round_name].append((player, opponent))
                processed_players.add(player)
                processed_players.add(opponent)
    
    # Validasi semua pemain memiliki pasangan
    active_players = st.session_state.players.copy()
    paired_players = set()
    
    for player1, player2 in st.session_state.matchups[round_name]:
        paired_players.add(player1)
        paired_players.add(player2)
    
    unpaired_players = [p for p in active_players if p not in paired_players]
    
    if unpaired_players:
        st.warning(f"Pemain berikut belum memiliki pasangan: {', '.join(unpaired_players)}")
        return False
    
    # Set status round ini menjadi confirmed
    st.session_state.round_status[round_name] = True
    
    # Simpan opponent selections untuk restorasi UI
    if round_name in st.session_state.pairs:
        if round_name not in st.session_state.opponent_selections:
            st.session_state.opponent_selections[round_name] = {}
        
        for player, opponent in st.session_state.pairs[round_name].items():
            st.session_state.opponent_selections[round_name][player] = opponent
    
    return True

# Updated function for predicting Round I-3
def predict_I3():
    log_debug("Predicting I-3")
    
    # Reset matchups untuk I-3
    st.session_state.matchups["I-3"] = []
    
    # Memastikan I-1 dan I-2 sudah diisi
    if not st.session_state.matchups["I-1"] or not st.session_state.matchups["I-2"]:
        log_debug("I-1 or I-2 not confirmed yet")
        st.warning("Matchup round I-1 atau I-2 belum dikonfirmasi!")
        return False
    
    log_debug(f"I-1 matchups: {st.session_state.matchups['I-1']}")
    log_debug(f"I-2 matchups: {st.session_state.matchups['I-2']}")
    
    # Buat dictionary untuk mempermudah pencarian
    i1_opponents = {}
    for player1, player2 in st.session_state.matchups["I-1"]:
        i1_opponents[player1] = player2
        i1_opponents[player2] = player1
    
    i2_opponents = {}
    for player1, player2 in st.session_state.matchups["I-2"]:
        i2_opponents[player1] = player2
        i2_opponents[player2] = player1
    
    log_debug(f"I-1 opponents mapping: {i1_opponents}")
    log_debug(f"I-2 opponents mapping: {i2_opponents}")
    
    # FIXED LOGIC: Untuk I-3, kita menggunakan I-1 dan I-2
    # Jika A lawan B di I-1, dan A lawan C di I-2, maka di I-3 A lawan D (lawan C di I-1)
    # Dictionary untuk menyimpan pasangan I-3
    i3_pairs = {}
    
    # Proses tiap pemain
    for player in st.session_state.players:
        # Skip jika sudah diproses
        if player in i3_pairs:
            continue
        
        # Dapatkan lawan di I-1 dan I-2
        i1_opponent = i1_opponents.get(player)
        i2_opponent = i2_opponents.get(player)
        
        if not i1_opponent or not i2_opponent:
            log_debug(f"No I-1 or I-2 opponent for {player}")
            continue
            
        # Dapatkan lawan di I-3: lawan dari I-2 di I-1
        i3_opponent = i1_opponents.get(i2_opponent)
        
        if not i3_opponent:
            log_debug(f"No I-1 opponent for {i2_opponent}")
            continue
            
        if i3_opponent == player:
            log_debug(f"Skipping self-match for {player}")
            continue
            
        # Cek jika sudah ditambahkan
        if i3_opponent in i3_pairs:
            if i3_pairs[i3_opponent] != player:
                log_debug(f"Warning: Conflict for I-3 pairing. {i3_opponent} already paired with {i3_pairs[i3_opponent]}, not with {player}")
            continue
            
        log_debug(f"Adding I-3 match: {player} vs {i3_opponent}")
        i3_pairs[player] = i3_opponent
        i3_pairs[i3_opponent] = player
        st.session_state.matchups["I-3"].append((player, i3_opponent))
    
    # Verifikasi semua pemain sudah mendapat pasangan
    if len(i3_pairs) < len(st.session_state.players):
        unpaired = [p for p in st.session_state.players if p not in i3_pairs]
        log_debug(f"Warning: Not all players paired in I-3. Unpaired: {unpaired}")
    
    # Jika tidak ada matchups yang berhasil dibuat, jangan set status confirmed
    if not st.session_state.matchups["I-3"]:
        log_debug("No valid I-3 matchups could be created")
        return False
    
    # Juga update pairs untuk I-3
    if "I-3" not in st.session_state.pairs:
        st.session_state.pairs["I-3"] = {}
    else:
        # Clear existing pairs for I-3
        st.session_state.pairs["I-3"] = {}
        
    for player1, player2 in st.session_state.matchups["I-3"]:
        st.session_state.pairs["I-3"][player1] = player2
        st.session_state.pairs["I-3"][player2] = player1
    
    log_debug(f"Final I-3 matchups: {st.session_state.matchups['I-3']}")
    log_debug(f"Final I-3 pairs: {st.session_state.pairs['I-3']}")
    
    # Only mark as confirmed if we have valid matchups
    if st.session_state.matchups["I-3"]:
        st.session_state.round_status["I-3"] = True
        return True
    else:
        st.session_state.round_status["I-3"] = False
        return False

# Updated function for predicting II-2
def predict_II2():
    log_debug("Predicting II-2")
    
    # Reset matchups untuk II-2
    st.session_state.matchups["II-2"] = []
    
    # Memastikan I-1 dan II-1 sudah diisi
    if not st.session_state.matchups["I-1"] or not st.session_state.matchups["II-1"]:
        log_debug("I-1 or II-1 not confirmed yet")
        st.warning("Matchup round I-1 atau II-1 belum dikonfirmasi!")
        return False
    
    # Buat dictionary untuk mempermudah pencarian
    i1_opponents = {}
    for player1, player2 in st.session_state.matchups["I-1"]:
        i1_opponents[player1] = player2
        i1_opponents[player2] = player1
        
    ii1_opponents = {}
    for player1, player2 in st.session_state.matchups["II-1"]:
        ii1_opponents[player1] = player2
        ii1_opponents[player2] = player1
    
    # Prediksi berdasarkan pola: player akan bertemu dengan lawan dari lawan di II-1 di I-1
    ii2_pairs = {}
    
    for player in st.session_state.players:
        if player in ii2_pairs:
            continue
            
        # Dapatkan lawan di II-1
        ii1_opponent = ii1_opponents.get(player)
        if not ii1_opponent:
            log_debug(f"No II-1 opponent for {player}")
            continue
            
        # Dapatkan lawan dari lawan di II-1 di I-1
        ii2_opponent = i1_opponents.get(ii1_opponent)
        if not ii2_opponent:
            log_debug(f"No I-1 opponent for {ii1_opponent}")
            continue
            
        if ii2_opponent == player:
            log_debug(f"Skipping self-match for {player}")
            continue
            
        if ii2_opponent in ii2_pairs:
            continue
            
        log_debug(f"Adding II-2 match: {player} vs {ii2_opponent}")
        ii2_pairs[player] = ii2_opponent
        ii2_pairs[ii2_opponent] = player
        st.session_state.matchups["II-2"].append((player, ii2_opponent))
    
    # Jika tidak ada matchups yang berhasil dibuat, jangan set status confirmed
    if not st.session_state.matchups["II-2"]:
        log_debug("No valid II-2 matchups could be created")
        return False
    
    # Juga update pairs untuk II-2
    if "II-2" not in st.session_state.pairs:
        st.session_state.pairs["II-2"] = {}
    else:
        # Clear existing pairs for II-2
        st.session_state.pairs["II-2"] = {}
        
    for player1, player2 in st.session_state.matchups["II-2"]:
        st.session_state.pairs["II-2"][player1] = player2
        st.session_state.pairs["II-2"][player2] = player1
    
    st.session_state.round_status["II-2"] = True
    return True

# Updated function for predicting II-4
def predict_II4():
    log_debug("Predicting II-4")
    
    # Reset matchups untuk II-4
    st.session_state.matchups["II-4"] = []
    
    # Memastikan I-3 dan II-1 sudah diisi (berdasarkan diagram)
    if not st.session_state.matchups["I-3"] or not st.session_state.matchups["II-1"]:
        log_debug("I-3 or II-1 not confirmed yet")
        st.warning("Matchup round I-3 atau II-1 belum dikonfirmasi!")
        return False
    
    log_debug(f"I-3 matchups: {st.session_state.matchups['I-3']}")
    log_debug(f"II-1 matchups: {st.session_state.matchups['II-1']}")
    
    # Buat dictionary untuk mempermudah pencarian
    i3_opponents = {}
    for player1, player2 in st.session_state.matchups["I-3"]:
        i3_opponents[player1] = player2
        i3_opponents[player2] = player1
        
    ii1_opponents = {}
    for player1, player2 in st.session_state.matchups["II-1"]:
        ii1_opponents[player1] = player2
        ii1_opponents[player2] = player1
    
    log_debug(f"I-3 opponent mapping: {i3_opponents}")
    log_debug(f"II-1 opponent mapping: {ii1_opponents}")
    
    # FIXED LOGIC: Untuk II-4
    # Jika A lawan E di II-1, dan B lawan E di I-3, maka A akan lawan B di II-4
    ii4_pairs = {}
    
    for player in st.session_state.players:
        if player in ii4_pairs:
            continue
        
        # Dapatkan lawan di II-1
        opponent_ii1 = ii1_opponents.get(player)
        if not opponent_ii1:
            log_debug(f"No II-1 opponent for {player}")
            continue
            
        # Temukan siapa yang melawan opponent_ii1 di I-3
        ii4_opponent = None
        for p, opp in st.session_state.matchups["I-3"]:
            if p == opponent_ii1:
                ii4_opponent = opp
                break
            elif opp == opponent_ii1:
                ii4_opponent = p
                break
                
        if not ii4_opponent:
            log_debug(f"No I-3 opponent for {opponent_ii1}")
            continue
            
        if ii4_opponent == player:
            log_debug(f"Skipping self-match for {player}")
            continue
            
        if ii4_opponent in ii4_pairs:
            continue
            
        log_debug(f"Adding II-4 match: {player} vs {ii4_opponent}")
        ii4_pairs[player] = ii4_opponent
        ii4_pairs[ii4_opponent] = player
        st.session_state.matchups["II-4"].append((player, ii4_opponent))
    
    # Jika tidak ada matchups yang berhasil dibuat, jangan set status confirmed
    if not st.session_state.matchups["II-4"]:
        log_debug("No valid II-4 matchups could be created")
        return False
    
    # Juga update pairs untuk II-4
    if "II-4" not in st.session_state.pairs:
        st.session_state.pairs["II-4"] = {}
    else:
        # Clear existing pairs for II-4
        st.session_state.pairs["II-4"] = {} 
        
    for player1, player2 in st.session_state.matchups["II-4"]:
        st.session_state.pairs["II-4"][player1] = player2
        st.session_state.pairs["II-4"][player2] = player1
    
    log_debug(f"Final II-4 matchups: {st.session_state.matchups['II-4']}")
    log_debug(f"Final II-4 pairs: {st.session_state.pairs['II-4']}")
    
    # Only mark as confirmed if we have valid matchups
    if st.session_state.matchups["II-4"]:
        st.session_state.round_status["II-4"] = True
        return True
    else:
        st.session_state.round_status["II-4"] = False
        return False

def predict_II5():
    log_debug("Predicting II-5")
    
    # Reset matchups untuk II-5
    st.session_state.matchups["II-5"] = []
    
    # Buat set pemain yang sudah punya lawan di round sebelumnya
    paired_with = {}
    for player in st.session_state.players:
        paired_with[player] = set()
    
    for round_name in ["I-1", "I-2", "I-3", "II-1", "II-2", "II-4"]:
        for player1, player2 in st.session_state.matchups.get(round_name, []):
            paired_with[player1].add(player2)
            paired_with[player2].add(player1)
    
    # Prediksi II-5: player akan bertemu dengan pemain yang belum pernah dilawan
    processed_players = set()
    for player in st.session_state.players:
        if player in processed_players:
            continue
            
        # Cari pemain yang belum pernah dilawan
        possible_opponents = [p for p in st.session_state.players if 
                             p != player and 
                             p not in paired_with[player] and 
                             p not in processed_players]
        
        if not possible_opponents:
            continue
            
        opponent = possible_opponents[0]  # Ambil opponent pertama yang valid
        st.session_state.matchups["II-5"].append((player, opponent))
        processed_players.add(player)
        processed_players.add(opponent)
    
    # Juga update pairs untuk II-5
    if "II-5" not in st.session_state.pairs:
        st.session_state.pairs["II-5"] = {}
    else:
        # Clear existing pairs
        st.session_state.pairs["II-5"] = {}
        
    for player1, player2 in st.session_state.matchups["II-5"]:
        st.session_state.pairs["II-5"][player1] = player2
        st.session_state.pairs["II-5"][player2] = player1
    
    st.session_state.round_status["II-5"] = True
    return True

def predict_II6():
    log_debug("Predicting II-6")
    
    # II-6 sama dengan I-1
    st.session_state.matchups["II-6"] = []
    
    # Memastikan I-1 sudah diisi
    if not st.session_state.matchups["I-1"]:
        log_debug("I-1 not confirmed yet")
        st.warning("Matchup round I-1 belum dikonfirmasi!")
        return False
        
    for player1, player2 in st.session_state.matchups["I-1"]:
        st.session_state.matchups["II-6"].append((player1, player2))
    
    # Juga update pairs untuk II-6
    if "II-6" not in st.session_state.pairs:
        st.session_state.pairs["II-6"] = {}
    else:
        # Clear existing pairs
        st.session_state.pairs["II-6"] = {}
        
    for player1, player2 in st.session_state.matchups["II-6"]:
        st.session_state.pairs["II-6"][player1] = player2
        st.session_state.pairs["II-6"][player2] = player1
    
    st.session_state.round_status["II-6"] = True
    return True

def predict_next_rounds():
    log_debug("Predicting next rounds")
    
    # Round III dan seterusnya
    for round_num in range(3, 8):  # III sampai VII
        roman = ["", "I", "II", "III", "IV", "V", "VI", "VII"][round_num]
        prev_roman = ["", "I", "II", "III", "IV", "V", "VI", "VII"][round_num-1]
        
        # III-1 sampai VII-1 sama dengan I-2 sampai VI-2
        source_round = f"{prev_roman}-2"
        target_round = f"{roman}-1"
        
        if st.session_state.round_status.get(source_round, False):
            st.session_state.matchups[target_round] = []
            for player1, player2 in st.session_state.matchups[source_round]:
                st.session_state.matchups[target_round].append((player1, player2))
            
            # Update pairs juga
            if target_round not in st.session_state.pairs:
                st.session_state.pairs[target_round] = {}
            else:
                st.session_state.pairs[target_round] = {}
                
            for player1, player2 in st.session_state.matchups[target_round]:
                st.session_state.pairs[target_round][player1] = player2
                st.session_state.pairs[target_round][player2] = player1
                
            st.session_state.round_status[target_round] = True
        
        # III-2 sampai VII-2 sama dengan I-3 sampai VI-3
        source_round = f"{prev_roman}-3" if prev_roman == "I" else f"{prev_roman}-2"
        target_round = f"{roman}-2"
        
        if st.session_state.round_status.get(source_round, False):
            st.session_state.matchups[target_round] = []
            for player1, player2 in st.session_state.matchups[source_round]:
                st.session_state.matchups[target_round].append((player1, player2))
            
            # Update pairs juga
            if target_round not in st.session_state.pairs:
                st.session_state.pairs[target_round] = {}
            else:
                st.session_state.pairs[target_round] = {}
                
            for player1, player2 in st.session_state.matchups[target_round]:
                st.session_state.pairs[target_round][player1] = player2
                st.session_state.pairs[target_round][player2] = player1
                
            st.session_state.round_status[target_round] = True
        
        # III-4 sampai VII-4 sama dengan II-4 sampai VI-4
        source_round = f"{prev_roman}-4"
        target_round = f"{roman}-4"
        
        if st.session_state.round_status.get(source_round, False):
            st.session_state.matchups[target_round] = []
            for player1, player2 in st.session_state.matchups[source_round]:
                st.session_state.matchups[target_round].append((player1, player2))
            
            # Update pairs juga
            if target_round not in st.session_state.pairs:
                st.session_state.pairs[target_round] = {}
            else:
                st.session_state.pairs[target_round] = {}
                
            for player1, player2 in st.session_state.matchups[target_round]:
                st.session_state.pairs[target_round][player1] = player2
                st.session_state.pairs[target_round][player2] = player1
                
            st.session_state.round_status[target_round] = True
        
        # III-5 sampai VII-5 sama dengan II-5 sampai VI-5
        source_round = f"{prev_roman}-5"
        target_round = f"{roman}-5"
        
        if st.session_state.round_status.get(source_round, False):
            st.session_state.matchups[target_round] = []
            for player1, player2 in st.session_state.matchups[source_round]:
                st.session_state.matchups[target_round].append((player1, player2))
            
            # Update pairs juga
            if target_round not in st.session_state.pairs:
                st.session_state.pairs[target_round] = {}
            else:
                st.session_state.pairs[target_round] = {}
                
            for player1, player2 in st.session_state.matchups[target_round]:
                st.session_state.pairs[target_round][player1] = player2
                st.session_state.pairs[target_round][player2] = player1
                
            st.session_state.round_status[target_round] = True
        
        # III-6 sampai VII-6 sama dengan II-6 sampai VI-6 (yang sama dengan I-1)
        source_round = f"{prev_roman}-6"
        target_round = f"{roman}-6"
        
        if st.session_state.round_status.get(source_round, False):
            st.session_state.matchups[target_round] = []
            for player1, player2 in st.session_state.matchups[source_round]:
                st.session_state.matchups[target_round].append((player1, player2))
            
            # Update pairs juga
            if target_round not in st.session_state.pairs:
                st.session_state.pairs[target_round] = {}
            else:
                st.session_state.pairs[target_round] = {}
                
            for player1, player2 in st.session_state.matchups[target_round]:
                st.session_state.pairs[target_round][player1] = player2
                st.session_state.pairs[target_round][player2] = player1
                
            st.session_state.round_status[target_round] = True
    
    return True

def predict_round(round_name):
    log_debug(f"Predicting round {round_name}")
    
    prediction_functions = {
        "I-3": predict_I3,
        "II-2": predict_II2,
        "II-4": predict_II4,
        "II-5": predict_II5,
        "II-6": predict_II6
    }
    
    if round_name in prediction_functions:
        return prediction_functions[round_name]()
    elif round_name.startswith(("III-", "IV-", "V-", "VI-", "VII-")):
        return predict_next_rounds()
    else:
        return False

# Inisialisasi state
initialize_state()

# Periksa dan proses flag reset
if 'reset_player_input' not in st.session_state:
    st.session_state.reset_player_input = False
    
if st.session_state.reset_player_input:
    st.session_state.player_input = ""
    st.session_state.reset_player_input = False

# Tampilkan logo dan judul
try:
    display_logo()
except:
    st.markdown('<h1 class="main-header">Magic Chess: GoGo Predictor</h1>', unsafe_allow_html=True)

# Sidebar untuk input dan kontrol
with st.sidebar:
    st.header("Kontrol")
    
    # Tab untuk input pemain dan pengaturan
    tab1, tab2, tab3 = st.tabs(["Input Pemain", "Data", "Debug"])
    
    with tab1:
        st.subheader("Daftar Pemain")
        st.text_area("Masukkan 8 nama pemain (satu per baris)", 
                    key="player_input", 
                    height=200, 
                    placeholder="Contoh:\nPlayer 1\nPlayer 2\nPlayer 3\nPlayer 4\nPlayer 5\nPlayer 6\nPlayer 7\nPlayer 8")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Simpan Pemain", use_container_width=True):
                if save_players():
                    st.success("Nama pemain disimpan!")
        
        with col2:
            if st.button("Reset Data", use_container_width=True):
                reset_data()
                st.success("Data berhasil direset")
    
    with tab2:
        st.subheader("Simpan/Muat Data")
        if st.button("Simpan Data ke File", use_container_width=True):
            result = save_data_to_file()
            if result:
                filename, json_str = result
                st.download_button(
                    label="Download File Data",
                    data=json_str,
                    file_name=filename,
                    mime="application/json"
                )
        
        uploaded_file = st.file_uploader("Pilih file data untuk dimuat", type=["json"])
        if uploaded_file is not None:
            if st.button("Muat Data dari File", use_container_width=True):
                content = uploaded_file.read().decode("utf-8")
                load_data_from_file(content)
    
    with tab3:
        st.subheader("Debug Log")
        if st.button("Clear Logs"):
            st.session_state.debug_logs = []
        
        st.text_area("Log Messages", value="\n".join(st.session_state.debug_logs), height=400, disabled=True)

# Tampilkan main content jika pemain sudah diinput
if st.session_state.players:
    # Tampilkan tabel pemain dan status
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Daftar Pemain")
        player_data = []
        for player in st.session_state.players:
            status = "Aktif"
            player_data.append({"Pemain": player, "Status": status})
        
        st.dataframe(pd.DataFrame(player_data), use_container_width=True)
    
    with col2:
        st.subheader("Statistik Matchup")
        # Hitung jumlah round yang sudah dikonfirmasi
        confirmed_rounds = sum(1 for status in st.session_state.round_status.values() if status)
        st.metric("Round Terkonfirmasi", confirmed_rounds)
        
        # Hitung jumlah pemain yang masih aktif
        active_players = len(st.session_state.players)
        st.metric("Jumlah Pemain", active_players)
    
    # Tombol untuk memprediksi semua round
    if st.button("Prediksi Semua Round yang Belum Terkonfirmasi", use_container_width=True):
        # Log status awal untuk debugging
        log_debug(f"Initial status before prediction: {st.session_state.round_status}")
        log_debug(f"Initial matchups I-3: {st.session_state.matchups.get('I-3', [])}")
        log_debug(f"Initial matchups II-4: {st.session_state.matchups.get('II-4', [])}")
        
        # Prediksi round I-3 jika I-1 dan I-2 sudah dikonfirmasi
        if (st.session_state.round_status.get("I-1", False) and 
            st.session_state.round_status.get("I-2", False) and 
            not st.session_state.round_status.get("I-3", False)):
            success = predict_I3()
            log_debug(f"I-3 prediction {'succeeded' if success else 'failed'}")
            log_debug(f"I-3 matchups after prediction: {st.session_state.matchups.get('I-3', [])}")
        
        # Prediksi round II-2 jika I-1 dan II-1 sudah dikonfirmasi
        if (st.session_state.round_status.get("I-1", False) and 
            st.session_state.round_status.get("II-1", False) and 
            not st.session_state.round_status.get("II-2", False)):
            success = predict_II2()
            log_debug(f"II-2 prediction {'succeeded' if success else 'failed'}")
        
        # Prediksi round II-4 jika I-3 dan II-1 sudah dikonfirmasi
        if (st.session_state.round_status.get("I-3", False) and 
            st.session_state.round_status.get("II-1", False) and 
            not st.session_state.round_status.get("II-4", False)):
            success = predict_II4()
            log_debug(f"II-4 prediction {'succeeded' if success else 'failed'}")
            log_debug(f"II-4 matchups after prediction: {st.session_state.matchups.get('II-4', [])}")
        
        # Prediksi round II-5 jika round sebelumnya sudah dikonfirmasi
        if all(st.session_state.round_status.get(r, False) for r in ["I-1", "I-2", "I-3", "II-1", "II-2", "II-4"]) and not st.session_state.round_status.get("II-5", False):
            success = predict_II5()
            log_debug(f"II-5 prediction {'succeeded' if success else 'failed'}")
        
        # Prediksi round II-6 jika I-1 sudah dikonfirmasi
        if st.session_state.round_status.get("I-1", False) and not st.session_state.round_status.get("II-6", False):
            success = predict_II6()
            log_debug(f"II-6 prediction {'succeeded' if success else 'failed'}")
        
        # Prediksi round III sampai VII
        success = predict_next_rounds()
        log_debug(f"Next rounds prediction {'succeeded' if success else 'failed'}")
        
        # Log status akhir untuk debugging
        log_debug(f"Final status after predictions: {st.session_state.round_status}")
        log_debug(f"Final matchups I-3: {st.session_state.matchups.get('I-3', [])}")
        log_debug(f"Final matchups II-4: {st.session_state.matchups.get('II-4', [])}")
        
        st.success("Semua round yang memungkinkan telah diprediksi!")
        force_rerun()
    
    # Tab untuk menampilkan matchup per round
    tabs = []
    for i in range(1, 8):  # I sampai VII
        tabs.append(f"Round {['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'][i-1]}")
    
    selected_tab = st.radio("Pilih Round:", tabs, horizontal=True)
    round_num = ["I", "II", "III", "IV", "V", "VI", "VII"][tabs.index(selected_tab)]
    
    # Tampilkan round berdasarkan tab yang dipilih
    st.markdown(f'<h2 class="round-header">Round {round_num}</h2>', unsafe_allow_html=True)
    
    # Rounds for current tab
    current_rounds = []
    if round_num == "I":
        current_rounds = ["I-1", "I-2", "I-3"]
    else:
        current_rounds = [f"{round_num}-1", f"{round_num}-2", f"{round_num}-4", f"{round_num}-5", f"{round_num}-6"]
    
    # Define columns untuk layout
    col_counts = len(current_rounds)
    cols = st.columns(col_counts)
    
    # Tampilkan setiap round dalam kolom terpisah
    for i, round_name in enumerate(current_rounds):
        with cols[i]:
            # Tentukan apakah round ini random atau prediksi
            is_random = round_name in ["I-1", "I-2", "II-1"]
            container_class = "random-round" if is_random else "predicted-round"
            
            # Status round
            status_class = "confirmed" if st.session_state.round_status.get(round_name, False) else "pending"
            status_text = "Terkonfirmasi" if st.session_state.round_status.get(round_name, False) else "Belum Terkonfirmasi"
            
            # Tampilkan header dan status round dengan desain card yang lebih baik
            st.markdown(f"""
            <div class="card">
                <h3>Round {round_name}</h3>
                <div class="status-badge {'confirmed-badge' if status_class == 'confirmed' else 'pending-badge'}">
                    {status_text}
                </div>
            """, unsafe_allow_html=True)
            
            # Jika round adalah random (perlu input manual)
            if is_random:
                st.markdown("</div>", unsafe_allow_html=True)  # Close card div
                
                active_players = st.session_state.players.copy()
                
                # Tampilkan dropdown untuk setiap pemain aktif
                for player in active_players:
                    # Daftar lawan yang mungkin (semua pemain aktif kecuali diri sendiri)
                    other_players = active_players.copy()
                    other_players.remove(player)
                    
                    # Filter lawan yang sudah dipilih oleh pemain lain
                    if round_name in st.session_state.pairs:
                        other_players_filtered = []
                        for p in other_players:
                            # Jika p sudah dipasangkan dengan pemain lain (bukan player), lewati
                            if (p in st.session_state.pairs[round_name] and 
                                st.session_state.pairs[round_name][p] != player):
                                continue
                            other_players_filtered.append(p)
                        other_players = other_players_filtered
                    
                    # Nilai default untuk dropdown
                    default_index = 0
                    
                    # Jika round sudah terkonfirmasi atau ada pasangan yang sudah dipilih
                    if round_name in st.session_state.pairs and player in st.session_state.pairs[round_name]:
                        opponent = st.session_state.pairs[round_name][player]
                        if opponent in other_players:
                            default_index = other_players.index(opponent) + 1
                    
                    # Persiapkan key unik
                    key = f"{round_name}_{player}"
                    
                    # Inisialisasi session state jika belum ada
                    if key not in st.session_state:
                        if round_name in st.session_state.pairs and player in st.session_state.pairs[round_name]:
                            st.session_state[key] = st.session_state.pairs[round_name][player]
                        else:
                            st.session_state[key] = ""
                    
                    # Tampilkan dropdown dengan callback on_change
                    st.selectbox(
                        f"{player} vs",
                        [""] + other_players,
                        key=key,
                        index=default_index,
                        disabled=st.session_state.round_status.get(round_name, False),
                        on_change=on_select_change,
                        args=(round_name, player)
                    )
                
                # Tombol konfirmasi jika round belum terkonfirmasi
                if not st.session_state.round_status.get(round_name, False):
                    if st.button(f"Konfirmasi {round_name}", key=f"confirm_{round_name}"):
                        if confirm_matchups(round_name):
                            st.success(f"Matchup round {round_name} berhasil dikonfirmasi!")
                            
                            # Otomatis prediksi round terkait
                            if round_name == "I-1" and st.session_state.round_status.get("I-2", False):
                                predict_I3()
                            elif round_name == "I-2" and st.session_state.round_status.get("I-1", False):
                                predict_I3()
                            elif round_name == "II-1":
                                if st.session_state.round_status.get("I-1", False):
                                    predict_II2()
                                if st.session_state.round_status.get("I-3", False):
                                    predict_II4()
                            
                            # Refresh halaman dengan force rerun
                            force_rerun()
                        else:
                            st.error("Ada kesalahan dalam konfirmasi matchup. Silakan periksa kembali pilihan lawan.")
            else:
                # Round prediksi (tampilkan hasil prediksi)
                if st.session_state.round_status.get(round_name, False):
                    # Tampilkan matchup yang sudah diprediksi
                    if st.session_state.matchups[round_name]:  # Pastikan matchups tidak kosong
                        for player1, player2 in st.session_state.matchups[round_name]:
                            st.markdown(f"<p>{player1} vs {player2}</p>", unsafe_allow_html=True)
                    else:
                        # Jika matchups kosong tapi status confirmed, ada masalah
                        st.markdown('<p style="color: #FFA726;">Status terkonfirmasi tetapi tidak ada data matchup</p>', unsafe_allow_html=True)
                        log_debug(f"Warning: {round_name} has confirmed status but no matchups")
                    
                    st.markdown("</div>", unsafe_allow_html=True)  # Close card div
                else:
                    st.markdown("</div>", unsafe_allow_html=True)  # Close card div
                    
                    # Tombol untuk memprediksi
                    if st.button(f"Prediksi {round_name}", key=f"predict_{round_name}"):
                        if predict_round(round_name):
                            st.success(f"Matchup round {round_name} berhasil diprediksi!")
                            
                            # Refresh halaman secara paksa untuk memastikan perubahan ditampilkan
                            force_rerun()
                        else:
                            st.error(f"Tidak dapat memprediksi round {round_name}. Pastikan round sebelumnya sudah terkonfirmasi.")
                            
    # Tampilkan tabel matchup penuh
    st.markdown('<h2 class="table-header">Tabel Matchup Lengkap</h2>', unsafe_allow_html=True)
    
    # Buat dataframe untuk semua matchup
    matchup_data = []
    
    for player in st.session_state.players:
        player_row = {"Pemain": player}
        
        for round_name in st.session_state.matchups.keys():
            if st.session_state.round_status.get(round_name, False):
                # Cari lawan di round ini
                opponent = ""
                for p1, p2 in st.session_state.matchups[round_name]:
                    if p1 == player:
                        opponent = p2
                        break
                    elif p2 == player:
                        opponent = p1
                        break
                
                player_row[round_name] = opponent
            else:
                player_row[round_name] = ""
        
        matchup_data.append(player_row)
    
    # Tampilkan dataframe
    matchup_df = pd.DataFrame(matchup_data)
    st.dataframe(matchup_df, use_container_width=True)

else:
    # Tampilkan instruksi jika belum ada pemain
    st.info("👈 Silakan masukkan 8 nama pemain di sidebar untuk memulai")
    
    # Tampilkan gambar petunjuk dengan desain yang lebih baik
    st.markdown("""
    <div class="card">
        <h3>Cara Penggunaan:</h3>
        <ol>
            <li>Masukkan 8 nama pemain di sidebar (satu nama per baris)</li>
            <li>Klik tombol "Simpan Pemain"</li>
            <li>Input matchup untuk round I-1, I-2, dan II-1 (babak random)</li>
            <li>Klik tombol "Konfirmasi" untuk setiap round</li>
            <li>Prediksi matchup pada round berikutnya akan muncul secara otomatis</li>
        </ol>
    </div>
    
    <div class="card">
        <h3>Pola Prediksi:</h3>
        <ul>
            <li><strong>Round I-3</strong>: Pemain bertemu dengan lawan dari orang yang dilawan di I-2 pada round I-1</li>
            <li><strong>Round II-2</strong>: Pemain bertemu dengan lawan dari lawan di II-1 di I-1</li>
            <li><strong>Round II-4</strong>: Pemain bertemu dengan orang yang dilawan lawan II-1 di I-3</li>
            <li><strong>Round II-5</strong>: Pemain bertemu dengan pemain yang belum pernah dilawan</li>
            <li><strong>Round II-6</strong>: Sama dengan I-1</li>
            <li><strong>Round berikutnya</strong>: Mengikuti pola yang sama</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)