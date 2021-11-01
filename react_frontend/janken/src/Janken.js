import React, {useState} from 'react';
import GamePlay from './gamePlay';
import GameSummary from './gameSummary';
import NamePrompt from './namePrompt';

const Janken = () => {
    const NAME_PROMPT = 'name', GAME_PLAY = 'play', SHOW_SUMMARY = 'summary';

    const [gameMode, setGameMode] = useState(NAME_PROMPT);
    const blankGameDetails = {
        playerName: '',
        matchID: 0,
        rounds: [],
        score: 0,
    }
    const [gameDetails, setGameDetails] = useState(blankGameDetails);

    function alterGameDetails(newDetails) {
        setGameDetails({...gameDetails, ...newDetails});
    }

    React.useEffect(() => {
        console.log(gameDetails);
    }, [gameDetails]);

    switch (gameMode) {
        case GAME_PLAY:
            return <GamePlay
                gameDetails={gameDetails}
                alterGameDetails={alterGameDetails}
                advanceToSummary={() => setGameMode(SHOW_SUMMARY)}
            />;

        case SHOW_SUMMARY:
            return <GameSummary
                gameDetails={gameDetails}
                alterGameDetails={alterGameDetails}
                resetGame={() => {
                    setGameDetails(blankGameDetails);
                    setGameMode(NAME_PROMPT);
                }}
                commenceRematch={() => setGameMode(GAME_PLAY)}
            />;

        default:
            return <NamePrompt
                alterGameDetails={alterGameDetails}
                advanceMode={() => setGameMode(GAME_PLAY)}
            />;
    }
}

export default Janken;