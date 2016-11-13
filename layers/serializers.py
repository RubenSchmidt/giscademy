import serpy


class LayerSerializer(serpy.Serializer):
    id = serpy.Field()
    name = serpy.Field()
