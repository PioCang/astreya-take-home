import React, {useState} from 'react';
import GameSummary from './gameSummary';
import NamePrompt from './namePrompt';

const Janken = () => {
    const NAME_PROMPT = 'name', GAME_PLAY = 'play', SHOW_SUMMARY = 'summary';

    const [gameMode, setGameMode] = useState(SHOW_SUMMARY);

    const blankGameDetails = {
        'playerName': 'Vince',
        'matchID': 8,
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
                advanceMode={() => setGameMode(NAME_PROMPT)}
            />;

        default:
            return <NamePrompt
                alterGameDetails={alterGameDetails}
                advanceMode={() => setGameMode(GAME_PLAY)}
            />;
    }
}

export default Janken;