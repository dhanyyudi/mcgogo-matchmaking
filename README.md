# Magic Chess: GoGo Predictor

![Magic Chess: GoGo](https://blog.rrqtopup.com/wp-content/uploads/2025/03/Go-Go-Card-di-Magic-Chess-Go-Go-3.jpeg)

A Streamlit application for predicting and managing matchups in Magic Chess: GoGo tournaments with 8 players.

## Overview

Magic Chess: GoGo Predictor helps tournament organizers predict matchups across multiple rounds based on established patterns in Magic Chess: GoGo tournaments. The app follows specific matchup rules to ensure fair pairings throughout a 7-round tournament format.

The app allows users to:

- Input 8 player names
- Configure random rounds (I-1, I-2, II-1)
- Auto-predict subsequent rounds based on established patterns
- Confirm matchups for each round
- Save and load tournament data
- View complete matchup tables

## Game Background

Magic Chess: GoGo is an auto-battler strategy game developed by Moonton, the same company behind Mobile Legends: Bang Bang. The game features:

- 8 players per tournament
- Multiple rounds of play
- Specific matchup rules and patterns across rounds

## Features

- **Player Management**: Input and manage 8 player names
- **Round Visualization**: Clearly see all matchups across 7 rounds
- **Matchup Prediction**: Auto-predict matchups based on game patterns
- **Data Export/Import**: Save and load tournament data as JSON files
- **Interactive UI**: Dark-themed intuitive interface
- **Debugging Tools**: Logging system for troubleshooting

## Matchup Prediction Patterns

The app implements the following matchup prediction patterns:

- **Round I-3**: Players face opponents who played against their Round I-2 opponent in Round I-1
- **Round II-2**: Players face the Round I-1 opponent of their Round II-1 opponent
- **Round II-4**: Players face opponents who played against their Round II-1 opponent in Round I-3
- **Round II-5**: Players face opponents they haven't played against yet
- **Round II-6**: Same matchups as Round I-1
- **Subsequent Rounds**: Follow consistent patterns from previous rounds

## Installation

1. Clone this repository:

```bash
git clone https://github.com/dhanyyudi/mcgogo-matchmaking.git
cd mcgogo-matchmaking
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run mcgogo.py
```

## How to Use

1. Enter 8 player names in the sidebar (one name per line)
2. Click "Simpan Pemain" (Save Players)
3. Configure matchups for random rounds (I-1, I-2, and II-1)
4. Click "Konfirmasi" (Confirm) for each round
5. Use "Prediksi" (Predict) to generate matchups for subsequent rounds
6. View the complete matchup table at the bottom of the page
7. Optionally save/load data using the Data tab in the sidebar

## Requirements

The app requires:

- Python 3.7+
- Streamlit
- Pandas
- Pillow (PIL)
- Requests

See `requirements.txt` for complete dependencies.

## Credits

This Streamlit application was inspired by and based on an Excel file created by cordX turu from the KB Discord community (https://discord.gg/klinikkb). The original Excel implementation provided the foundation for the matchup prediction patterns used in this app.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/dhanyyudi/mcgogo-matchmaking/blob/main/LICENSE) file for details.

## Contact

For questions, suggestions, or feedback, please contact: dhanyyudi.prasetyo@gmail.com
