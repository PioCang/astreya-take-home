import React, {useState} from 'react';
import * as BACKEND from './constants';

const axios = require('axios');

const GamePlay = ({gameDetails, alterGameDetails, advanceToSummary}) => {

    const [selection, setSelection] = useState("Rock");
    const selectionChoices = ['Rock', 'Paper', 'Scissors']

    async function playSelection() {
        try {
            const endpoint_url = BACKEND.DJANGO_API_ROOT_URL + 'janken/play_round/';
            const registration_data = {
                name: gameDetails.playerName,
                match_id: gameDetails.matchID,
                selection: selection.substr(0, 1),
            }

            const response = await axios({
                method: 'post',
                url: endpoint_url,
                data: registration_data
            });
            const payload = response.data;

            const played_round_info = {
                round_no:  payload.round_no,
                player_selection: payload.player_selection,
                bot_selection: payload.bot_selection,
                outcome: payload.outcome,
                score: payload.outcome === "Player won round against bot"
                    ? gameDetails.score + 1 : gameDetails.score
            }

            let updated_rounds = [...gameDetails.rounds];
            updated_rounds.push(played_round_info);

            alterGameDetails({
                rounds: updated_rounds,
                score: played_round_info.score,
            });
        } catch (error) {
            // do nothing
        }
    }

    const gamePlayStyles = {
        centeredDiv: {
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: `translateX(-50%) translateY(-50%)`,
            display: 'flex',
            flexDirection: 'column',
            width: '80%',
        },
        playButton: {
            marginTop: "24px",
            lineHeight: "32px",
            padding: "0px 10px",
            fontSize: 'larger',
            width: "25vw"
        },
        radioButtons: {
            fontSize: 'larger',
            margin: '15px,'
        }
    }

    return (
        <div style={gamePlayStyles.centeredDiv}>
            {
                gameDetails.rounds.length > 0 &&
                <table>
                    <thead>
                        <tr>
                            <th>Round #</th>
                            <th>Player Selection</th>
                            <th>Bot Selection</th>
                            <th>Outcome</th>
                            <th>Cumulative Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            gameDetails.rounds.map((round, index) => {
                                return (
                                    <tr key={index}>
                                        <td>{round.round_no}</td>
                                        <td>{round.player_selection}</td>
                                        <td>{round.bot_selection}</td>
                                        <td>{round.outcome}</td>
                                        <td>{round.score}</td>
                                    </tr>
                                )
                            })
                        }
                    </tbody>
                </table>
            }

            <center>
                <h1>
                    {
                        gameDetails.rounds.length < 3
                        ? `Round ${gameDetails.rounds.length + 1}`
                        : 'Game Over'
                    }
                </h1>
                {
                    gameDetails.rounds.length < 3 &&
                    <div className="radio">
                        {
                            selectionChoices.map((choice, index) => {
                                return (
                                    <label key={index}
                                        style={gamePlayStyles.radioButtons}>
                                        <input
                                            type="radio"
                                            value={choice}
                                            checked={selection === choice}
                                            onChange={() => setSelection(choice)}
                                        />
                                        {choice}
                                        <br/>
                                        <br/>
                                    </label>
                                )
                            })
                        }
                    </div>
                }
            </center>
            <center>
                {
                    gameDetails.rounds.length === 3
                    ? <button
                        onClick={advanceToSummary}
                        style={gamePlayStyles.playButton}
                    >
                        Show Summary
                    </button>
                    : <button
                        onClick={playSelection}
                        style={gamePlayStyles.playButton}
                    >
                        Play "{selection}"
                    </button>
                }
            </center>
        </div>
    )
}

export default GamePlay;
