import React, {useState} from 'react';
import * as BACKEND from './constants';

const axios = require('axios');

const NamePrompt = ({alterGameDetails, advanceMode}) => {

    const [playerName, setPlayerName] = useState("");
    const [errorMsg, setErrorMsg] = useState("");

    async function startGame() {
        try {
            const endpoint_url = BACKEND.DJANGO_API_ROOT_URL + 'janken/register/';
            const registration_data = {
                'name': playerName,
            }

            const response = await axios({
                method: 'post',
                url: endpoint_url,
                data: registration_data
            });
            const payload = response.data;

            alterGameDetails({
                playerName: payload.name,
                matchID: payload.match_id,
            });
            advanceMode();
        } catch (error) {
            setErrorMsg(error.response.data['message']);
        }
    }

    const namePromptStyles = {
        centeredDiv: {
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: `translateX(-50%) translateY(-50%)`,
            display: 'flex',
            flexDirection: 'column'
        },
        inputElement: {
            lineHeight: "32px",
            padding: "0px 10px",
            fontSize: 'larger',
        },
        playButton: {
            marginTop: "24px",
            lineHeight: "32px",
            padding: "0px 10px",
            fontSize: 'larger',
            width: "15vw"
        },
        errorText: {
            color: 'red',
            fontSize: 'smaller',
        }
    }

    return (
        <div style={namePromptStyles.centeredDiv}>
            <h1>What's Your Name?</h1>
            <center>
                <input
                    height="128"
                    placeholder="Name"
                    value={playerName}
                    onChange={(e) => setPlayerName(e.target.value)}
                    style={namePromptStyles.inputElement}>
                </input>
                <br/>
                <span style={namePromptStyles.errorText}>
                    {errorMsg}
                </span>
            </center>
            <center>
                <button
                    disabled={!playerName}
                    onClick={startGame}
                    style={namePromptStyles.playButton}
                >
                    Play
                </button>
            </center>
        </div>
    )
}

export default NamePrompt;
