""" Views of Janken """

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

class RegisterPlayer(APIView):
    """ View for Registering Player name and starting a new match """

    permission_classes = [AllowAny]

    def post(self, request):
        """ Register name of player """

        try:

            return Response(
                {
                    "name": player.name,
                    "match_id": match_id
                },
                status=status.HTTP_201_CREATED)


        except (TypeError, ValueError) as err:
            return Response({'error': str(err)},
                            status=status.HTTP_400_BAD_REQUEST)
