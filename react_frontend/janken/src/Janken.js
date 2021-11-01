import React, {useState} from 'react';
import NamePrompt from './namePrompt';

const Janken = () => {
    const NAME_PROMPT = 'name', GAME_PLAY = 'play';// SHOW_SUMMARY = 'summary';

    const [gameMode, setGameMode] = useState(NAME_PROMPT);

    const blankGameDetails = {
        'playerName': '',
        'matchID': 0,
    }
    const [gameDetails, setGameDetails] = useState(blankGameDetails);

    function alterGameDetails(newDetails, nextMode) {
        setGameDetails({...gameDetails, ...newDetails});

        if (nextMode) {
            setGameMode(nextMode);
        }
    }

    React.useEffect(() => {
        console.log(gameDetails);
    }, [gameDetails]);

    switch (gameMode) {
        default:
            return <NamePrompt
                alterGameDetails={alterGameDetails}
                nextMode={GAME_PLAY}
            />;
    }
}

export default Janken;