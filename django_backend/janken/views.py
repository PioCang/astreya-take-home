""" Views of Janken """

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Player

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
            return Response({'message': str(err)},
                            status=status.HTTP_400_BAD_REQUEST)
