import React, {useEffect, useState} from 'react';
import * as BACKEND from './constants';

const axios = require('axios');

const GameSummary = ({gameDetails, advanceMode}) => {

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
            setInError(true)
            setSummaryMessage(error.response.data['message']);
        }
    }

    useEffect(() => {
        fetchSummary();
    }, []);

    const namePromptStyles = {
        centeredDiv: {
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: `translateX(-50%) translateY(-50%)`,
            display: 'flex',
            flexDirection: 'column'
        },
        resetButton: {
            marginTop: "24px",
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
        <div style={namePromptStyles.centeredDiv}>
            <h1>SUMMARY</h1>
            <span style={namePromptStyles.summaryText}>
                {summaryMessage}
            </span>
            <center>
                <button
                    onClick={advanceMode}
                    style={namePromptStyles.resetButton}
                >
                    Back to Start
                </button>
            </center>
        </div>
    )
}

export default GameSummary;
