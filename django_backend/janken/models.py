""" Models used by Janken """

from __future__ import annotations
from random import randrange

from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating ``created`` and
    ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        """ Meta info """
        abstract = True



class Player(TimeStampedModel):
    """
    A visitor of the site who wishes to challenge the Janken Bot.
    """

    INVALIDATED = '###INVALIDATED###'

    name = models.CharField(max_length=128, null=True)
    session_key = models.CharField(max_length=64, null=True, blank=True)


    def __str__(self):
        return self.name or '[unnamed]'

    @classmethod
    def register_new_player(cls, name: str, session_key: str) -> Player:
        """ Register a new player """

        if not name:
            raise ValueError("The name is invalid")
        if len(name) > 128:
            raise ValueError("Name is limited to 128 characters.")

        existing_players = cls.objects.filter(name=name,
                                              session_key=session_key)
        if existing_players.exists():
            existing_players.first().invalidate_key()

        return cls.objects.create(name=name, session_key=session_key)

    def invalidate_key(self) -> None:
        """ Invalidate the session key for this Player """

        self.session_key = self.INVALIDATED
        self.save()

    def start_new_match(self) -> int:
        """ Start a new match with Player """
        return self.matches_played.create(player=self).id



class Match(TimeStampedModel):
    """
    A Janken Match winner is decided after 3 JankenRound(s).
    """

    PLAYER_WON = 'W'
    PLAYER_LOST = 'L'
    PLAYER_TIED = 'T'
    UNDECIDED = 'U'

    MATCH_OUTCOMES = (
        (PLAYER_WON, "Player won match against bot."),
        (PLAYER_LOST, "Player lost match against bot."),
        (PLAYER_TIED, "Player tied match with bot."),
        (UNDECIDED, "Match undecided / unfinished.")
    )

    player = models.ForeignKey('Player', blank=True, null=True,
                               related_name='matches_played',
                               on_delete=models.SET_NULL)
    outcome = models.CharField(max_length=1, choices=MATCH_OUTCOMES,
                               default=UNDECIDED, null=True)


    def __str__(self):
        player_name = getattr(self.player, 'name', "[unnamed]")
        return f"Match {self.id} with {player_name}"

    def decide_outcome(self) -> str:
        """ Decide the outcome of the match """

        outcome_strings_as_dict = dict((x, y) for x, y in self.MATCH_OUTCOMES)

        rounds_played = getattr(self, 'rounds_played', Round.objects.none())
        if rounds_played.count() > 3:
            raise ValueError(
                f"More than 3 rounds were played for match {self.id}")

        player_wins = rounds_played.filter(outcome=Round.PLAYER_WON).count()
        bot_wins = rounds_played.filter(outcome=Round.PLAYER_LOST).count()

        if rounds_played.count() < 3:
            outcome = self.UNDECIDED
        else:
            if player_wins > bot_wins:
                outcome = self.PLAYER_WON
            elif player_wins < bot_wins:
                outcome = self.PLAYER_LOST
            else:
                outcome = self.PLAYER_TIED

            self.player.invalidate_key()

        self.outcome = outcome
        self.save()

        outcome_strings_as_dict = dict((x, y) for x, y in self.MATCH_OUTCOMES)
        return {
            'summary': outcome_strings_as_dict[outcome]
        }



class Round(TimeStampedModel):
    """
    A Janken Round is 1 "throw" of rocks-papers-scissors.
    """

    NO_SELECTION = 'X'
    ROCK = 'R'
    PAPER = 'P'
    SCISSORS = 'S'

    SELECTION_CHOICES = (
        (NO_SELECTION, 'No selection'),
        (ROCK, 'Rock'),
        (PAPER, 'Paper'),
        (SCISSORS, 'Scissors'),
    )

    PLAYER_WON = 'W'
    PLAYER_LOST = 'L'
    PLAYER_TIED = 'T'

    ROUND_OUTCOMES = (
        (PLAYER_WON, "Player won round against bot"),
        (PLAYER_LOST, "Player lost round against bot"),
        (PLAYER_TIED, "Player tied round with bot"),
    )

    match = models.ForeignKey('Match', related_name='rounds_played',
                              on_delete=models.CASCADE, null=True)
    player_selection = models.CharField(max_length=1, null=True,
                                        choices=SELECTION_CHOICES,
                                        default=NO_SELECTION)
    bot_selection = models.CharField(max_length=1, null=True,
                                     choices=SELECTION_CHOICES,
                                     default=NO_SELECTION)
    outcome = models.CharField(max_length=1, null=True,
                               choices=ROUND_OUTCOMES,
                               default=PLAYER_TIED)
    round_number = models.IntegerField(default=1)


    def __str__(self):
        return f"Match: {self.match.id}, Round: {self.round_number}"

    @classmethod
    def commence_round(cls, match, player_selection) -> dict:
        """ Play your selection agains the bot """

        valid_selections = dict((x, y) for x, y in cls.SELECTION_CHOICES)
        del valid_selections[cls.NO_SELECTION]

        if player_selection not in valid_selections.keys():
            raise ValueError(f"Selection must be in {valid_selections.keys()}")

        bot_selection = cls.generate_bot_selection()
        created_round = cls.objects.create(
            match=match,
            player_selection=player_selection,
            bot_selection=bot_selection,
            round_number=match.rounds_played.count() + 1)

        outcome_descriptive = created_round.decide_outcome()

        return {
            'round_no': created_round.round_number,
            'player_selection': valid_selections[player_selection],
            'bot_selection': valid_selections[bot_selection],
            'outcome': outcome_descriptive
        }


    @classmethod
    def generate_bot_selection(cls) -> str:
        """ Generates a random value for bot's selection """

        possible_selections = (cls.ROCK, cls.PAPER, cls.SCISSORS)
        return possible_selections[randrange(len(possible_selections))]

    def decide_outcome(self) -> str:
        """ Decides the outcome of this round """

        if self.player_selection == self.NO_SELECTION:
            raise ValueError("Player has no selection.")

        if self.bot_selection == self.NO_SELECTION:
            raise ValueError("Bot has no selection.")

        decision_matrix = {
            self.ROCK: {
                self.ROCK: self.PLAYER_TIED,
                self.PAPER: self.PLAYER_LOST,
                self.SCISSORS: self.PLAYER_WON
            },
            self.PAPER: {
                self.ROCK: self.PLAYER_WON,
                self.PAPER: self.PLAYER_TIED,
                self.SCISSORS: self.PLAYER_LOST
            },
            self.SCISSORS: {
                self.ROCK: self.PLAYER_LOST,
                self.PAPER: self.PLAYER_WON,
                self.SCISSORS: self.PLAYER_TIED
            }
        }

        self.outcome = \
            decision_matrix[self.player_selection][self.bot_selection]
        self.save()

        outcome_strings_as_dict = dict((x, y) for x, y in self.ROUND_OUTCOMES)
        return outcome_strings_as_dict[self.outcome]
