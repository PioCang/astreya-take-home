import React, {useEffect, useState} from 'react';
import * as BACKEND from './constants';

const axios = require('axios');

const GameSummary = ({gameDetails, alterGameDetails, resetGame, commenceRematch}) => {

    const [summaryMessage, setSummaryMessage] = useState("");
    const [inError, setInError] = useState(false);

    async function fetchSummary() {
        try {
            const endpoint_url = BACKEND.DJANGO_API_ROOT_URL
                + 'janken/match_summary/?'
                + `name=${gameDetails.playerName}`
                + `&match_id=${gameDetails.matchID}`;

            const response = await axios({
                method: 'get',
                url: endpoint_url,
            });
            const payload = response.data;

            setInError(false);
            setSummaryMessage(payload.summary);
        } catch (error) {
            setInError(true);
            setSummaryMessage(error.response.data['message']);
        }
    }

    async function prepareRematch() {
        try {
            const endpoint_url = BACKEND.DJANGO_API_ROOT_URL + 'janken/register/';
            const registration_data = {
                'name': gameDetails.playerName,
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
                rounds: [],
                score: 0
            });
            commenceRematch();
        } catch (error) {
            setInError(true);
            setSummaryMessage("Rematch failed: " + error.response.data['message']);
        }
    }

    useEffect(() => {
        fetchSummary();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const gameSummaryStyles = {
        centeredDiv: {
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: `translateX(-50%) translateY(-50%)`,
            display: 'flex',
            flexDirection: 'column'
        },
        resetButton: {
            margin: "24px 20px",
            lineHeight: "32px",
            padding: "0px 10px",
            fontSize: 'larger',
            width: "15vw"
        },
        summaryText: {
            color: inError ? 'red' : 'black',
            fontSize: 'largest',
        },
    }

    return (
        <div style={gameSummaryStyles.centeredDiv}>
            <center>
                <h1>SUMMARY</h1>
                <span style={gameSummaryStyles.summaryText}>
                    {summaryMessage}
                </span>
            </center>
            <center>
                <button
                    onClick={resetGame}
                    style={gameSummaryStyles.resetButton}
                >
                    Back to Start
                </button>
                <button
                    onClick={prepareRematch}
                    style={gameSummaryStyles.resetButton}
                >
                    Rematch!
                </button>
            </center>
        </div>
    )
}

export default GameSummary;
