""" Views of Janken """

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Match, Player, Round
from .utils import dump_thorough_stack_trace

class RegisterPlayer(APIView):
    """ View for Registering Player name and starting a new match """

    permission_classes = [AllowAny]

    def post(self, request):
        """ Register name of player """

        try:
            name = request.data.get('name', '')
            player = Player.register_new_player(name,
                                                request.session.session_key)
            match_id = player.start_new_match()

            return Response(
                {
                    "name": player.name,
                    "match_id": match_id
                },
                status=status.HTTP_201_CREATED)


        except (TypeError, ValueError) as err:
            dump_thorough_stack_trace()
            return Response({'message': str(err)},
                            status=status.HTTP_400_BAD_REQUEST)


class PlayRound(APIView):
    """ View for Playing a Janken Round """

    permission_classes = [AllowAny]

    def post(self, request):
        """ Play a round of Janken """

        try:
            name = request.data.get('name', '')
            if not name:
                raise ValueError("The name is invalid")

            match_id = int(request.data.get('match_id', 0))
            if not match_id:
                raise ValueError("Invalid match ID")

            player_exists = Player.objects \
                .filter(name=name,
                        session_key=request.session.session_key) \
                .exists()
            if not player_exists:
                raise ValueError("Invalid Player")

            try:
                match = Match.objects.get(id=match_id)
            except Match.DoesNotExist as nonexistent:
                raise ValueError("Invalid Match ID") from nonexistent

            if match.rounds_played.count() >= 3:
                raise TypeError("3 rounds were already played for this match.")

            selection = request.data.get('selection', Round.NO_SELECTION)
            round_info = Round.commence_round(match, selection)

            return Response(round_info, status=status.HTTP_201_CREATED)

        except (TypeError, ValueError) as err:
            dump_thorough_stack_trace()
            return Response({'message': str(err)},
                            status=status.HTTP_400_BAD_REQUEST)


class MatchSummary(APIView):
    """ Get the summary for this Janken Match """

    permission_classes = [AllowAny]

    def get(self, request):
        """ Play a round of Janken """

        try:
            name = request.GET.get('name', '')
            if not name:
                raise ValueError("The name is invalid")

            match_id = int(request.GET.get('match_id', 0))
            if not match_id:
                raise ValueError("Invalid match ID")

            player_exists = Player.objects \
                .filter(name=name,
                        session_key=request.session.session_key) \
                .exists()
            if not player_exists:
                raise ValueError("Invalid Player")

            try:
                match = Match.objects.get(id=match_id)
            except Match.DoesNotExist as nonexistent:
                raise ValueError("Invalid Match ID") from nonexistent

            match_summary = match.decide_outcome()
            return Response(match_summary, status=status.HTTP_201_CREATED)

        except (TypeError, ValueError) as err:
            dump_thorough_stack_trace()
            return Response({'message': str(err)},
                            status=status.HTTP_400_BAD_REQUEST)
