# -*- coding: utf-8 -*-
from rest_framework import serializers

from updateScore.models import Score


class Image_List(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('id', 'clientNum', 'score')