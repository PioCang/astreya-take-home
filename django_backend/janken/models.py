""" Models used by Janken """

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

    name = models.CharField(max_length=128, null=True)
    session_key = models.CharField(max_length=64, null=True, blank=True)


    def __str__(self):
        return self.name or '[unnamed]'



class Match(TimeStampedModel):
    """
    A Janken Match winner is decided after 3 JankenRound(s).
    """

    PLAYER_WON = 'W'
    PLAYER_LOST = 'L'
    PLAYER_TIED = 'T'
    UNDECIDED = 'U'

    MATCH_OUTCOMES = (
        (PLAYER_WON, "Player won match against bot"),
        (PLAYER_LOST, "Player lost match against bot"),
        (PLAYER_TIED, "Player tied match with bot"),
        (UNDECIDED, 'Match undecided / unfinished')
    )

    player = models.ForeignKey('Player', blank=True, null=True,
                               related_name='matches_played',
                               on_delete=models.SET_NULL)
    outcome = models.CharField(max_length=1, choices=MATCH_OUTCOMES,
                               default=UNDECIDED, null=True)


    def __str__(self):
        player_name = getattr(self.player, 'name', "[unnamed]")
        return f"Match {self.id} with {player_name}"



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
