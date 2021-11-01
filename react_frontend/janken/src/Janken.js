import React, {useState} from 'react';
import GameSummary from './gameSummary';
import NamePrompt from './namePrompt';

const Janken = () => {
    const NAME_PROMPT = 'name', GAME_PLAY = 'play', SHOW_SUMMARY = 'summary';

    const [gameMode, setGameMode] = useState(SHOW_SUMMARY);

    const blankGameDetails = {
        'playerName': 'Vince',
        'matchID': 8,
        'rounds': []
    }
    const [gameDetails, setGameDetails] = useState(blankGameDetails);

    function alterGameDetails(newDetails) {
        setGameDetails({...gameDetails, ...newDetails});
    }

    React.useEffect(() => {
        console.log(gameDetails);
    }, [gameDetails]);

    switch (gameMode) {
        case SHOW_SUMMARY:
            return <GameSummary
                gameDetails={gameDetails}
                alterGameDetails={alterGameDetails}
                resetGame={() => setGameMode(NAME_PROMPT)}
                rematchGame={() => setGameMode(GAME_PLAY)}
            />;

        default:
            return <NamePrompt
                alterGameDetails={alterGameDetails}
                advanceMode={() => setGameMode(GAME_PLAY)}
            />;
    }
}

export default Janken;